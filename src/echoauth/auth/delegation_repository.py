"""Append-history delegation repository with authority and audit integration."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import replace
from threading import RLock

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth.authority_models import AuthorityStatus, freeze_authority_value
from echoauth.auth.authority_registry import AuthorityRepository
from echoauth.auth.authority_resolution import (
    AuthorityResolutionOutcome,
    AuthorityResolutionResult,
    AuthorityScopeMatcher,
    ScopeMatchResult,
)
from echoauth.auth.authority_validation import parse_authority_timestamp
from echoauth.auth.delegation_models import (
    DelegationGrant,
    DelegationHistoryEntry,
    DelegationState,
    StoredDelegationGrant,
)
from echoauth.auth.delegation_validation import (
    DelegationValidationError,
    validate_delegation_grant,
)
from echoauth.models import AuditAppendState, AuditRecord


class DelegationRepositoryError(ValueError):
    """Base deterministic delegation repository error."""


class DelegationNotFoundError(KeyError):
    """Raised when a delegation grant is absent."""


class DuplicateDelegationError(DelegationRepositoryError):
    """Raised when a delegation identifier is already registered."""


class InvalidDelegationTransitionError(DelegationRepositoryError):
    """Raised when a grant lifecycle transition is not permitted."""


class DelegationAuditError(DelegationRepositoryError):
    """Raised when required delegation audit evidence cannot append."""


class DelegationRepository(ABC):
    """Delegation grant persistence boundary."""

    @abstractmethod
    def create(
        self,
        grant: DelegationGrant,
        authority_result: AuthorityResolutionResult,
        *,
        actor_id: str,
        reason: str,
        occurred_at: str,
        audit_event_id: str,
    ) -> StoredDelegationGrant:
        """Validate authority and persist one issued grant."""

    @abstractmethod
    def get(self, delegation_id: str) -> StoredDelegationGrant:
        """Return the current immutable grant."""

    @abstractmethod
    def update_state(
        self,
        delegation_id: str,
        state: DelegationState,
        *,
        actor_id: str,
        reason: str,
        occurred_at: str,
        audit_event_id: str,
    ) -> StoredDelegationGrant:
        """Apply one audited lifecycle transition."""

    @abstractmethod
    def revoke(
        self,
        delegation_id: str,
        *,
        actor_id: str,
        reason: str,
        occurred_at: str,
        audit_event_id: str,
    ) -> StoredDelegationGrant:
        """Revoke a grant while preserving its evidence."""

    @abstractmethod
    def history(self, delegation_id: str) -> tuple[DelegationHistoryEntry, ...]:
        """Return immutable lifecycle history."""


_ALLOWED_TRANSITIONS = {
    DelegationState.ISSUED: {
        DelegationState.ACTIVE,
        DelegationState.EXPIRED,
        DelegationState.REVOKED,
        DelegationState.INVALID,
    },
    DelegationState.ACTIVE: {DelegationState.EXPIRED, DelegationState.REVOKED},
    DelegationState.DRAFT: {DelegationState.ISSUED, DelegationState.INVALID},
    DelegationState.EXPIRED: set(),
    DelegationState.REVOKED: set(),
    DelegationState.OUT_OF_SCOPE: set(),
    DelegationState.INVALID: set(),
}


class InMemoryDelegationRepository(DelegationRepository):
    """Thread-safe delegation repository with immutable audit-bound history."""

    def __init__(
        self,
        authority_repository: AuthorityRepository,
        authority_scope_matcher: AuthorityScopeMatcher,
        audit_repository: InMemoryAuditLogRepository,
        *,
        audit_chain_id: str,
    ) -> None:
        if not audit_chain_id:
            raise DelegationRepositoryError("audit_chain_id must not be empty")
        self._authority_repository = authority_repository
        self._authority_scope_matcher = authority_scope_matcher
        self._audit_repository = audit_repository
        self._audit_chain_id = audit_chain_id
        self._records: dict[str, StoredDelegationGrant] = {}
        self._history: dict[str, list[DelegationHistoryEntry]] = {}
        self._lock = RLock()

    def create(
        self,
        grant: DelegationGrant,
        authority_result: AuthorityResolutionResult,
        *,
        actor_id: str,
        reason: str,
        occurred_at: str,
        audit_event_id: str,
    ) -> StoredDelegationGrant:
        validate_delegation_grant(grant)
        grant = replace(
            grant,
            context_constraints=freeze_authority_value(grant.context_constraints),
            chain_metadata=freeze_authority_value(grant.chain_metadata),
        )
        operation_time = parse_authority_timestamp(occurred_at, "occurred_at")
        if operation_time < parse_authority_timestamp(grant.issued_at, "issued_at"):
            raise DelegationValidationError("grant creation cannot precede issued_at")
        if grant.state is not DelegationState.ISSUED:
            raise DelegationValidationError("new delegation grants must be issued")
        if parse_authority_timestamp(grant.expires_at, "expires_at") <= operation_time:
            raise DelegationValidationError("new delegation grant is already expired")
        self._validate_operation(actor_id, reason, audit_event_id)
        self._validate_grantor(grant, authority_result, operation_time)

        with self._lock:
            if grant.delegation_id in self._records:
                raise DuplicateDelegationError("duplicate delegation_id")
            audit = self._append_audit(
                grant,
                operation="created",
                actor_id=actor_id,
                reason=reason,
                occurred_at=occurred_at,
                audit_event_id=audit_event_id,
            )
            stored = StoredDelegationGrant(grant, reason)
            self._records[grant.delegation_id] = stored
            self._history[grant.delegation_id] = [
                self._history_entry(grant, "created", actor_id, reason, occurred_at, audit)
            ]
            return stored

    def get(self, delegation_id: str) -> StoredDelegationGrant:
        with self._lock:
            try:
                return self._records[delegation_id]
            except KeyError as exc:
                raise DelegationNotFoundError(delegation_id) from exc

    def update_state(
        self,
        delegation_id: str,
        state: DelegationState,
        *,
        actor_id: str,
        reason: str,
        occurred_at: str,
        audit_event_id: str,
    ) -> StoredDelegationGrant:
        self._validate_operation(actor_id, reason, audit_event_id)
        operation_time = parse_authority_timestamp(occurred_at, "occurred_at")
        if not isinstance(state, DelegationState):
            raise DelegationValidationError("state must be a canonical delegation state")
        with self._lock:
            current = self.get(delegation_id)
            if operation_time < parse_authority_timestamp(
                current.delegation_grant.issued_at, "issued_at"
            ):
                raise DelegationValidationError(
                    "delegation transition cannot precede issued_at"
                )
            previous_time = parse_authority_timestamp(
                self._history[delegation_id][-1].occurred_at, "occurred_at"
            )
            if operation_time < previous_time:
                raise DelegationValidationError(
                    "delegation transition time must preserve history order"
                )
            if state not in _ALLOWED_TRANSITIONS[current.delegation_grant.state]:
                raise InvalidDelegationTransitionError(
                    f"transition from {current.delegation_grant.state.value} to {state.value} is not allowed"
                )
            if state is DelegationState.EXPIRED and operation_time < parse_authority_timestamp(
                current.delegation_grant.expires_at, "expires_at"
            ):
                raise DelegationValidationError(
                    "delegation cannot expire before expires_at"
                )
            revoked_at = (
                occurred_at if state is DelegationState.REVOKED else current.delegation_grant.revoked_at
            )
            updated = replace(current.delegation_grant, state=state, revoked_at=revoked_at)
            validate_delegation_grant(updated)
            audit = self._append_audit(
                updated,
                operation=state.value,
                actor_id=actor_id,
                reason=reason,
                occurred_at=occurred_at,
                audit_event_id=audit_event_id,
            )
            stored = StoredDelegationGrant(updated, reason)
            self._records[delegation_id] = stored
            self._history[delegation_id].append(
                self._history_entry(updated, state.value, actor_id, reason, occurred_at, audit)
            )
            return stored

    def revoke(
        self,
        delegation_id: str,
        *,
        actor_id: str,
        reason: str,
        occurred_at: str,
        audit_event_id: str,
    ) -> StoredDelegationGrant:
        return self.update_state(
            delegation_id,
            DelegationState.REVOKED,
            actor_id=actor_id,
            reason=reason,
            occurred_at=occurred_at,
            audit_event_id=audit_event_id,
        )

    def history(self, delegation_id: str) -> tuple[DelegationHistoryEntry, ...]:
        with self._lock:
            try:
                return tuple(self._history[delegation_id])
            except KeyError as exc:
                raise DelegationNotFoundError(delegation_id) from exc

    def _validate_grantor(
        self,
        grant: DelegationGrant,
        authority_result: AuthorityResolutionResult,
        operation_time,
    ) -> None:
        if authority_result.outcome is not AuthorityResolutionOutcome.AUTHORIZED:
            raise DelegationValidationError("grantor authority result is not authorized")
        if authority_result.authority_source_id != grant.grantor_id:
            raise DelegationValidationError("grantor does not match authority source")
        if authority_result.authority_record_id != grant.source_authority_reference:
            raise DelegationValidationError("source authority reference does not match")
        if authority_result.authority_resolution_id != grant.authority_resolution_id:
            raise DelegationValidationError("authority resolution reference does not match")
        if authority_result.scope is None:
            raise DelegationValidationError("authority result has no effective scope")
        authority_records = {
            stored.authority_record.authority_record_id: stored.authority_record
            for stored in self._authority_repository.find_by_subject(grant.subject_id)
        }
        authority_record = authority_records.get(grant.source_authority_reference)
        if authority_record is None:
            raise DelegationValidationError("source authority record was not found")
        if authority_record.authority_source_id != grant.grantor_id:
            raise DelegationValidationError("source authority grantor mismatch")
        if authority_record.status is not AuthorityStatus.ACTIVE:
            raise DelegationValidationError("source authority record is not active")
        if authority_record.expires_at is not None and parse_authority_timestamp(
            authority_record.expires_at, "expires_at"
        ) <= operation_time:
            raise DelegationValidationError("source authority record is expired")
        for action in grant.allowed_actions:
            for resource in grant.allowed_resources:
                match = self._authority_scope_matcher.match(
                    authority_result.scope,
                    action=action,
                    resource=resource,
                    context=grant.context_constraints,
                )
                if match is not ScopeMatchResult.MATCH:
                    raise DelegationValidationError(
                        "delegation scope exceeds or ambiguously matches grantor authority"
                    )

    def _append_audit(
        self,
        grant: DelegationGrant,
        *,
        operation: str,
        actor_id: str,
        reason: str,
        occurred_at: str,
        audit_event_id: str,
    ):
        result = self._audit_repository.append(
            AuditRecord(
                event_type=f"delegation.grant_{operation}",
                actor_id=actor_id,
                authority_verdict_id=grant.authority_resolution_id,
                reason=reason,
                details={
                    "delegate_id": grant.delegate_id,
                    "delegation_id": grant.delegation_id,
                    "evidence_hash": grant.evidence_hash,
                    "grantor_id": grant.grantor_id,
                    "source_authority_reference": grant.source_authority_reference,
                    "state": grant.state.value,
                    "subject_id": grant.subject_id,
                },
                occurred_at=occurred_at,
            ),
            audit_event_id=audit_event_id,
            chain_id=self._audit_chain_id,
        )
        if result.append_state is not AuditAppendState.ACCEPTED:
            raise DelegationAuditError(f"delegation audit append failed: {result.reason}")
        return result

    def _history_entry(
        self,
        grant: DelegationGrant,
        operation: str,
        actor_id: str,
        reason: str,
        occurred_at: str,
        audit,
    ) -> DelegationHistoryEntry:
        return DelegationHistoryEntry(
            sequence=len(self._history.get(grant.delegation_id, ())) + 1,
            operation=operation,
            delegation_grant=grant,
            actor_id=actor_id,
            reason=reason,
            occurred_at=occurred_at,
            audit_event_id=audit.audit_event_id,
            audit_event_hash=audit.event_hash,
            previous_audit_hash=audit.previous_hash,
        )

    @staticmethod
    def _validate_operation(actor_id: str, reason: str, audit_event_id: str) -> None:
        for field_name, value in (
            ("actor_id", actor_id),
            ("reason", reason),
            ("audit_event_id", audit_event_id),
        ):
            if not isinstance(value, str) or not value:
                raise DelegationValidationError(f"{field_name} must be a non-empty string")
