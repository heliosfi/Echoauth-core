"""Append-history authority registry with Sprint 2A audit integration."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import replace
from threading import RLock

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth.authority_models import (
    AuthorityHistoryEntry,
    AuthorityRecord,
    AuthorityRegistryState,
    AuthorityStatus,
    StoredAuthorityRecord,
    freeze_authority_value,
)
from echoauth.auth.authority_validation import (
    AuthorityValidationError,
    parse_authority_timestamp,
    validate_authority_record,
)
from echoauth.canonical import canonical_sha256
from echoauth.models import AuditAppendState, AuditRecord


class AuthorityRepositoryError(ValueError):
    """Base deterministic authority repository error."""


class AuthorityNotFoundError(KeyError):
    """Raised when an authority record is absent."""


class DuplicateAuthorityError(AuthorityRepositoryError):
    """Raised when an authority record ID already exists."""


class InvalidAuthorityTransitionError(AuthorityRepositoryError):
    """Raised when a lifecycle transition is not permitted."""


class AuthorityAuditError(AuthorityRepositoryError):
    """Raised when required authority audit evidence cannot be appended."""


class AuthorityRepository(ABC):
    """Authority registry persistence boundary."""

    @abstractmethod
    def create(
        self,
        record: AuthorityRecord,
        *,
        actor_id: str,
        reason: str,
        occurred_at: str,
        audit_event_id: str,
    ) -> StoredAuthorityRecord:
        """Create and audit one explicit authority record."""

    @abstractmethod
    def retrieve(
        self,
        authority_record_id: str,
        *,
        actor_id: str,
        occurred_at: str,
        audit_event_id: str,
    ) -> StoredAuthorityRecord:
        """Retrieve and audit one authority record lookup."""

    @abstractmethod
    def update_status(
        self,
        authority_record_id: str,
        status: AuthorityStatus,
        *,
        actor_id: str,
        reason: str,
        occurred_at: str,
        audit_event_id: str,
    ) -> StoredAuthorityRecord:
        """Apply and audit one valid lifecycle transition."""

    @abstractmethod
    def revoke(
        self,
        authority_record_id: str,
        *,
        actor_id: str,
        reason: str,
        occurred_at: str,
        audit_event_id: str,
    ) -> StoredAuthorityRecord:
        """Revoke one authority record without deleting its evidence."""

    @abstractmethod
    def history(self, authority_record_id: str) -> tuple[AuthorityHistoryEntry, ...]:
        """Return immutable lifecycle history in append order."""

    @abstractmethod
    def find_by_subject(self, subject_id: str) -> tuple[StoredAuthorityRecord, ...]:
        """Return current records for resolution in deterministic order."""


_ALLOWED_TRANSITIONS = {
    AuthorityStatus.ACTIVE: {
        AuthorityStatus.SUSPENDED,
        AuthorityStatus.REVOKED,
        AuthorityStatus.EXPIRED,
    },
    AuthorityStatus.SUSPENDED: {AuthorityStatus.ACTIVE, AuthorityStatus.REVOKED},
    AuthorityStatus.REVOKED: set(),
    AuthorityStatus.EXPIRED: set(),
}


class InMemoryAuthorityRepository(AuthorityRepository):
    """Thread-safe authority registry with immutable history and audit evidence."""

    def __init__(
        self,
        audit_repository: InMemoryAuditLogRepository,
        *,
        audit_chain_id: str,
    ) -> None:
        if not audit_chain_id:
            raise AuthorityRepositoryError("audit_chain_id must not be empty")
        self._audit_repository = audit_repository
        self._audit_chain_id = audit_chain_id
        self._records: dict[str, StoredAuthorityRecord] = {}
        self._history: dict[str, list[AuthorityHistoryEntry]] = {}
        self._lock = RLock()

    def create(
        self,
        record: AuthorityRecord,
        *,
        actor_id: str,
        reason: str,
        occurred_at: str,
        audit_event_id: str,
    ) -> StoredAuthorityRecord:
        validate_authority_record(record)
        record = replace(record, scope=freeze_authority_value(record.scope))
        operation_time = parse_authority_timestamp(occurred_at, "occurred_at")
        if record.status is not AuthorityStatus.ACTIVE:
            raise AuthorityValidationError("new authority records must be active")
        if record.expires_at is not None and parse_authority_timestamp(
            record.expires_at, "expires_at"
        ) <= operation_time:
            raise AuthorityValidationError("new authority record is already expired")
        self._validate_operation(actor_id, reason, audit_event_id)

        with self._lock:
            if record.authority_record_id in self._records:
                raise DuplicateAuthorityError("duplicate authority_record_id")
            if any(
                current.authority_record.subject_id == record.subject_id
                and current.authority_record.priority == record.priority
                and current.authority_record.status is AuthorityStatus.ACTIVE
                for current in self._records.values()
            ):
                raise AuthorityValidationError(
                    "active equal-priority authority conflict requires policy resolution"
                )
            audit = self._append_audit(
                record,
                operation="created",
                actor_id=actor_id,
                reason=reason,
                occurred_at=occurred_at,
                audit_event_id=audit_event_id,
            )
            stored = StoredAuthorityRecord(
                registry_result_id=_result_id("registered", audit_event_id),
                state=AuthorityRegistryState.REGISTERED,
                authority_record=record,
                reason=reason,
            )
            self._records[record.authority_record_id] = stored
            self._history[record.authority_record_id] = [
                self._history_entry(record, "created", actor_id, reason, occurred_at, audit)
            ]
            return stored

    def retrieve(
        self,
        authority_record_id: str,
        *,
        actor_id: str,
        occurred_at: str,
        audit_event_id: str,
    ) -> StoredAuthorityRecord:
        self._validate_operation(actor_id, "lookup", audit_event_id)
        parse_authority_timestamp(occurred_at, "occurred_at")
        with self._lock:
            try:
                current = self._records[authority_record_id]
            except KeyError as exc:
                self._append_lookup_miss(
                    authority_record_id, actor_id, occurred_at, audit_event_id
                )
                raise AuthorityNotFoundError(authority_record_id) from exc
            self._append_audit(
                current.authority_record,
                operation="lookup_hit",
                actor_id=actor_id,
                reason="lookup_hit",
                occurred_at=occurred_at,
                audit_event_id=audit_event_id,
            )
            return replace(
                current,
                registry_result_id=_result_id("found", audit_event_id),
                state=AuthorityRegistryState.FOUND,
                reason="found",
            )

    def update_status(
        self,
        authority_record_id: str,
        status: AuthorityStatus,
        *,
        actor_id: str,
        reason: str,
        occurred_at: str,
        audit_event_id: str,
    ) -> StoredAuthorityRecord:
        self._validate_operation(actor_id, reason, audit_event_id)
        parse_authority_timestamp(occurred_at, "occurred_at")
        if not isinstance(status, AuthorityStatus):
            raise AuthorityValidationError("status must be a canonical authority status")

        with self._lock:
            try:
                current = self._records[authority_record_id]
            except KeyError as exc:
                raise AuthorityNotFoundError(authority_record_id) from exc
            current_status = current.authority_record.status
            if status not in _ALLOWED_TRANSITIONS[current_status]:
                raise InvalidAuthorityTransitionError(
                    f"transition from {current_status.value} to {status.value} is not allowed"
                )
            updated_record = replace(current.authority_record, status=status)
            validate_authority_record(updated_record)
            audit = self._append_audit(
                updated_record,
                operation=status.value,
                actor_id=actor_id,
                reason=reason,
                occurred_at=occurred_at,
                audit_event_id=audit_event_id,
            )
            stored = StoredAuthorityRecord(
                registry_result_id=_result_id("updated", audit_event_id),
                state=AuthorityRegistryState.UPDATED,
                authority_record=updated_record,
                reason=reason,
            )
            self._records[authority_record_id] = stored
            self._history[authority_record_id].append(
                self._history_entry(
                    updated_record,
                    status.value,
                    actor_id,
                    reason,
                    occurred_at,
                    audit,
                )
            )
            return stored

    def revoke(
        self,
        authority_record_id: str,
        *,
        actor_id: str,
        reason: str,
        occurred_at: str,
        audit_event_id: str,
    ) -> StoredAuthorityRecord:
        return self.update_status(
            authority_record_id,
            AuthorityStatus.REVOKED,
            actor_id=actor_id,
            reason=reason,
            occurred_at=occurred_at,
            audit_event_id=audit_event_id,
        )

    def history(self, authority_record_id: str) -> tuple[AuthorityHistoryEntry, ...]:
        with self._lock:
            try:
                return tuple(self._history[authority_record_id])
            except KeyError as exc:
                raise AuthorityNotFoundError(authority_record_id) from exc

    def find_by_subject(self, subject_id: str) -> tuple[StoredAuthorityRecord, ...]:
        if not isinstance(subject_id, str) or not subject_id:
            raise AuthorityValidationError("subject_id must be a non-empty string")
        status_order = {
            AuthorityStatus.ACTIVE: 0,
            AuthorityStatus.SUSPENDED: 1,
            AuthorityStatus.REVOKED: 2,
            AuthorityStatus.EXPIRED: 3,
        }
        with self._lock:
            records = (
                stored
                for stored in self._records.values()
                if stored.authority_record.subject_id == subject_id
            )
            return tuple(
                sorted(
                    records,
                    key=lambda stored: (
                        status_order[stored.authority_record.status],
                        stored.authority_record.priority,
                        stored.authority_record.issued_at,
                        stored.authority_record.authority_record_id,
                    ),
                )
            )

    def _append_audit(
        self,
        record: AuthorityRecord,
        *,
        operation: str,
        actor_id: str,
        reason: str,
        occurred_at: str,
        audit_event_id: str,
    ):
        result = self._audit_repository.append(
            AuditRecord(
                event_type=f"authority.record_{operation}",
                actor_id=actor_id,
                reason=reason,
                details={
                    "authority_record_id": record.authority_record_id,
                    "authority_source_id": record.authority_source_id,
                    "authority_type": record.authority_type.value,
                    "evidence_hash": record.evidence_hash,
                    "status": record.status.value,
                    "subject_id": record.subject_id,
                },
                occurred_at=occurred_at,
            ),
            audit_event_id=audit_event_id,
            chain_id=self._audit_chain_id,
        )
        if result.append_state is not AuditAppendState.ACCEPTED:
            raise AuthorityAuditError(f"authority audit append failed: {result.reason}")
        return result

    def _append_lookup_miss(
        self,
        authority_record_id: str,
        actor_id: str,
        occurred_at: str,
        audit_event_id: str,
    ) -> None:
        result = self._audit_repository.append(
            AuditRecord(
                event_type="authority.record_lookup_miss",
                actor_id=actor_id,
                reason="not_found",
                details={"authority_record_id": authority_record_id},
                occurred_at=occurred_at,
            ),
            audit_event_id=audit_event_id,
            chain_id=self._audit_chain_id,
        )
        if result.append_state is not AuditAppendState.ACCEPTED:
            raise AuthorityAuditError(f"authority audit append failed: {result.reason}")

    def _history_entry(
        self,
        record: AuthorityRecord,
        operation: str,
        actor_id: str,
        reason: str,
        occurred_at: str,
        audit,
    ) -> AuthorityHistoryEntry:
        return AuthorityHistoryEntry(
            sequence=len(self._history.get(record.authority_record_id, ())) + 1,
            operation=operation,
            authority_record=record,
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
                raise AuthorityValidationError(f"{field_name} must be a non-empty string")


def _result_id(operation: str, audit_event_id: str) -> str:
    return f"areg_{canonical_sha256({'audit_event_id': audit_event_id, 'operation': operation})}"
