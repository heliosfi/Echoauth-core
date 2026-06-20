"""Deterministic Delegation Validation service for Sprint 2E."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from threading import RLock

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth.authority_models import AuthorityStatus, freeze_authority_value
from echoauth.auth.authority_registry import AuthorityRepository
from echoauth.auth.authority_validation import parse_authority_timestamp
from echoauth.auth.delegation_models import (
    DelegationContextMatch,
    DelegationGrant,
    DelegationState,
    DelegationValidationOutcome,
    DelegationValidationRequest,
    DelegationValidationResult,
)
from echoauth.auth.delegation_repository import (
    DelegationNotFoundError,
    DelegationRepository,
)
from echoauth.auth.delegation_validation import (
    DelegationValidationError,
    validate_delegation_request,
)
from echoauth.canonical import canonical_sha256
from echoauth.models import AuditAppendState, AuditRecord, CanonicalJsonObject


class DelegationValidationAuditError(RuntimeError):
    """Raised when required delegation validation audit evidence cannot append."""


class DelegationContextMatcher(ABC):
    """Boundary for context semantics absent from the canonical object contract."""

    @abstractmethod
    def match(
        self,
        constraints: CanonicalJsonObject,
        context: CanonicalJsonObject,
    ) -> DelegationContextMatch:
        """Return match, mismatch, or ambiguity without expanding grant scope."""


class DelegationValidationService:
    """Validate one explicit grant without policy or execution behavior."""

    def __init__(
        self,
        repository: DelegationRepository,
        authority_repository: AuthorityRepository,
        context_matcher: DelegationContextMatcher,
        audit_repository: InMemoryAuditLogRepository,
        *,
        audit_chain_id: str,
        component_id: str = "delegation_validation_service",
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if not audit_chain_id:
            raise ValueError("audit_chain_id must not be empty")
        if not component_id:
            raise ValueError("component_id must not be empty")
        self._repository = repository
        self._authority_repository = authority_repository
        self._context_matcher = context_matcher
        self._audit_repository = audit_repository
        self._audit_chain_id = audit_chain_id
        self._component_id = component_id
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._cache: dict[str, DelegationValidationResult] = {}
        self._lock = RLock()

    def validate(
        self, request: DelegationValidationRequest
    ) -> DelegationValidationResult:
        """Return a deterministic, fail-closed delegation outcome."""

        now = self._utc_now()
        try:
            validate_delegation_request(request)
        except DelegationValidationError:
            return self._complete(
                request,
                grant=None,
                outcome=DelegationValidationOutcome.CONFLICT,
                reason="invalid_delegation_validation_request",
                now=now,
            )
        try:
            grant = self._repository.get(request.delegation_id).delegation_grant
        except DelegationNotFoundError:
            return self._complete(
                request,
                grant=None,
                outcome=DelegationValidationOutcome.CONFLICT,
                reason="delegation_not_found",
                now=now,
            )

        if grant.subject_id != request.subject_id:
            return self._complete(
                request,
                grant=grant,
                outcome=DelegationValidationOutcome.INVALID_SUBJECT,
                reason="delegation_subject_mismatch",
                now=now,
            )
        if grant.delegate_id != request.requester_id:
            return self._complete(
                request,
                grant=grant,
                outcome=DelegationValidationOutcome.CONFLICT,
                reason="delegate_identity_mismatch",
                now=now,
            )
        if grant.authority_resolution_id != request.authority_verdict_id:
            return self._complete(
                request,
                grant=grant,
                outcome=DelegationValidationOutcome.INVALID_GRANTOR,
                reason="authority_resolution_reference_mismatch",
                now=now,
            )
        if grant.state is DelegationState.REVOKED or grant.revoked_at is not None:
            return self._complete(
                request,
                grant=grant,
                outcome=DelegationValidationOutcome.REVOKED,
                reason="delegation_revoked",
                now=now,
            )
        if grant.state is DelegationState.EXPIRED or parse_authority_timestamp(
            grant.expires_at, "expires_at"
        ) <= now:
            return self._complete(
                request,
                grant=grant,
                outcome=DelegationValidationOutcome.EXPIRED,
                reason="delegation_expired",
                now=now,
            )
        if grant.state is not DelegationState.ACTIVE:
            return self._complete(
                request,
                grant=grant,
                outcome=DelegationValidationOutcome.CONFLICT,
                reason="delegation_not_active",
                now=now,
            )
        if grant.chain_metadata:
            return self._complete(
                request,
                grant=grant,
                outcome=DelegationValidationOutcome.CONFLICT,
                reason="delegation_chain_validation_deferred",
                now=now,
            )
        if not self._grantor_is_current(grant, now):
            return self._complete(
                request,
                grant=grant,
                outcome=DelegationValidationOutcome.INVALID_GRANTOR,
                reason="grantor_authority_inactive",
                now=now,
            )
        if request.action not in grant.allowed_actions or request.resource not in grant.allowed_resources:
            return self._complete(
                request,
                grant=grant,
                outcome=DelegationValidationOutcome.INVALID_SCOPE,
                reason="delegation_scope_mismatch",
                now=now,
            )
        context_match = self._context_matcher.match(
            grant.context_constraints, request.context
        )
        if context_match is DelegationContextMatch.AMBIGUOUS:
            return self._complete(
                request,
                grant=grant,
                outcome=DelegationValidationOutcome.CONFLICT,
                reason="delegation_context_ambiguous",
                now=now,
            )
        if context_match is not DelegationContextMatch.MATCH:
            return self._complete(
                request,
                grant=grant,
                outcome=DelegationValidationOutcome.INVALID_SCOPE,
                reason="delegation_context_mismatch",
                now=now,
            )
        return self._complete(
            request,
            grant=grant,
            outcome=DelegationValidationOutcome.VALID,
            reason="delegation_valid",
            now=now,
            effective_scope={
                "actions": grant.allowed_actions,
                "context_constraints": grant.context_constraints,
                "resources": grant.allowed_resources,
            },
        )

    def _grantor_is_current(self, grant: DelegationGrant, now: datetime) -> bool:
        records = {
            stored.authority_record.authority_record_id: stored.authority_record
            for stored in self._authority_repository.find_by_subject(grant.subject_id)
        }
        authority = records.get(grant.source_authority_reference)
        if authority is None:
            return False
        if authority.authority_source_id != grant.grantor_id:
            return False
        if authority.status is not AuthorityStatus.ACTIVE:
            return False
        return authority.expires_at is None or parse_authority_timestamp(
            authority.expires_at, "expires_at"
        ) > now

    def _complete(
        self,
        request: DelegationValidationRequest,
        *,
        grant: DelegationGrant | None,
        outcome: DelegationValidationOutcome,
        reason: str,
        now: datetime,
        effective_scope: Mapping[str, object] | None = None,
    ) -> DelegationValidationResult:
        evidence_hash = delegation_validation_evidence_hash(request, grant, now)
        cache_key = canonical_sha256(
            {
                "evidence_hash": evidence_hash,
                "outcome": outcome.value,
                "reason": reason,
            }
        )
        with self._lock:
            cached = self._cache.get(cache_key)
            if cached is not None:
                return cached
            audit_event_id = f"audit_dval_{cache_key}"
            audit = self._audit_repository.append(
                AuditRecord(
                    event_type="delegation.validation",
                    actor_id=self._component_id,
                    authority_verdict_id=request.authority_verdict_id or None,
                    reason=reason,
                    details={
                        "delegation_id": request.delegation_id,
                        "evidence_hash": evidence_hash,
                        "outcome": outcome.value,
                        "requester_id": request.requester_id,
                        "subject_id": request.subject_id,
                        "validation_id": request.validation_id,
                    },
                    occurred_at=_timestamp(now),
                ),
                audit_event_id=audit_event_id,
                chain_id=self._audit_chain_id,
            )
            if audit.append_state is not AuditAppendState.ACCEPTED:
                raise DelegationValidationAuditError(
                    f"delegation validation audit append failed: {audit.reason}"
                )
            result = DelegationValidationResult(
                validation_id=request.validation_id,
                delegation_id=request.delegation_id,
                outcome=outcome,
                reason=reason,
                evidence_hash=evidence_hash,
                validated_at=_timestamp(now),
                effective_scope=(
                    freeze_authority_value(effective_scope)
                    if effective_scope is not None
                    else None
                ),
                audit_event_id=audit_event_id,
            )
            self._cache[cache_key] = result
            return result

    def _utc_now(self) -> datetime:
        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise DelegationValidationError(
                "delegation validation clock must be timezone-aware"
            )
        return now.astimezone(timezone.utc)


def delegation_validation_evidence_hash(
    request: DelegationValidationRequest,
    grant: DelegationGrant | None,
    validated_at: datetime,
) -> str:
    """Hash request, grant, and evaluation time deterministically."""

    return canonical_sha256(
        {
            "action": request.action,
            "authority_verdict_id": request.authority_verdict_id,
            "context": request.context,
            "delegation_evidence_hash": grant.evidence_hash if grant else None,
            "delegation_id": request.delegation_id,
            "delegation_state": grant.state.value if grant else None,
            "requester_id": request.requester_id,
            "resource": request.resource,
            "subject_id": request.subject_id,
            "validated_at": _timestamp(validated_at),
            "validation_id": request.validation_id,
        }
    )


def _timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
