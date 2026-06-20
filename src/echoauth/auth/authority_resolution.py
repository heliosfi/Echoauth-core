"""Deterministic Authority Resolution foundation for Sprint 2D.

Specifications: specs/authority-resolution.md, specs/authority-registry.md,
specs/authority-revocation.md
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from threading import RLock
from typing import Any

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth.authority_models import (
    AuthorityRecord,
    AuthorityStatus,
    AuthorityType,
    freeze_authority_value,
)
from echoauth.auth.authority_registry import AuthorityRepository
from echoauth.auth.authority_validation import parse_authority_timestamp
from echoauth.canonical import CanonicalDataError, canonical_json_text, canonical_sha256
from echoauth.models import (
    AuditAppendState,
    AuditRecord,
    AuthorityResolutionRequest,
    CanonicalJsonObject,
)


class AuthorityResolutionOutcome(str, Enum):
    """Canonical Sprint 2D authority resolution outcomes."""

    AUTHORIZED = "authorized"
    DENIED = "denied"
    REVOKED = "revoked"
    EXPIRED = "expired"
    CONFLICT = "conflict"
    INSUFFICIENT_AUTHORITY = "insufficient_authority"


class ScopeMatchResult(str, Enum):
    """Provider-neutral result for domain-specific authority scope matching."""

    MATCH = "match"
    MISMATCH = "mismatch"
    AMBIGUOUS = "ambiguous"


@dataclass(frozen=True)
class AuthorityResolutionResult:
    """Deterministic result of evaluating explicit authority records."""

    authority_resolution_id: str
    request_id: str
    outcome: AuthorityResolutionOutcome
    reason: str
    evidence_hash: str
    resolved_at: str
    evaluated_authority_record_ids: tuple[str, ...]
    authority_record_id: str | None = None
    authority_source_id: str | None = None
    authority_type: AuthorityType | None = None
    scope: Mapping[str, Any] | None = None
    audit_event_id: str | None = None


class AuthorityResolutionValidationError(ValueError):
    """Raised when a resolution request cannot be evaluated safely."""


class AuthorityResolutionAuditError(RuntimeError):
    """Raised when required authority resolution audit evidence cannot append."""


class AuthorityScopeMatcher(ABC):
    """Boundary for scope semantics not defined by canonical object contracts."""

    @abstractmethod
    def match(
        self,
        scope: CanonicalJsonObject,
        *,
        action: str,
        resource: str,
        context: CanonicalJsonObject,
    ) -> ScopeMatchResult:
        """Return match, mismatch, or ambiguity without expanding scope."""


class AuthorityResolutionService:
    """Resolve explicit authority without identity, policy, or execution inference."""

    def __init__(
        self,
        repository: AuthorityRepository,
        scope_matcher: AuthorityScopeMatcher,
        audit_repository: InMemoryAuditLogRepository,
        *,
        audit_chain_id: str,
        component_id: str = "authority_resolution_service",
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if not audit_chain_id:
            raise ValueError("audit_chain_id must not be empty")
        if not component_id:
            raise ValueError("component_id must not be empty")
        self._repository = repository
        self._scope_matcher = scope_matcher
        self._audit_repository = audit_repository
        self._audit_chain_id = audit_chain_id
        self._component_id = component_id
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._result_cache: dict[str, AuthorityResolutionResult] = {}
        self._result_lock = RLock()

    def resolve(self, request: AuthorityResolutionRequest) -> AuthorityResolutionResult:
        """Evaluate repository authority and append one result audit record."""

        now = self._utc_now()
        try:
            validate_authority_resolution_request(request)
        except AuthorityResolutionValidationError:
            return self._complete(
                request,
                records=(),
                outcome=AuthorityResolutionOutcome.DENIED,
                reason="invalid_authority_resolution_request",
                now=now,
            )

        records = tuple(
            stored.authority_record
            for stored in self._repository.find_by_subject(request.subject_id)
            if stored.authority_record.authority_source_id == request.requester_id
        )
        if not records:
            return self._complete(
                request,
                records=(),
                outcome=AuthorityResolutionOutcome.INSUFFICIENT_AUTHORITY,
                reason="no_explicit_authority_record",
                now=now,
            )

        revoked_record_ids = _effective_revoked_record_ids(
            request.revocation_records, now
        )

        active: list[AuthorityRecord] = []
        revoked: list[AuthorityRecord] = []
        expired: list[AuthorityRecord] = []
        suspended: list[AuthorityRecord] = []
        for record in records:
            if (
                record.status is AuthorityStatus.REVOKED
                or record.authority_record_id in revoked_record_ids
            ):
                revoked.append(record)
            elif record.status is AuthorityStatus.EXPIRED or _is_expired(record, now):
                expired.append(record)
            elif record.status is AuthorityStatus.SUSPENDED:
                suspended.append(record)
            else:
                active.append(record)

        matches: list[AuthorityRecord] = []
        scope_ambiguous = False
        for record in active:
            if record.authority_type in (AuthorityType.DELEGATED, AuthorityType.EMERGENCY):
                continue
            match = self._scope_matcher.match(
                record.scope,
                action=request.action,
                resource=request.resource,
                context=request.context,
            )
            if match is ScopeMatchResult.MATCH:
                matches.append(record)
            elif match is ScopeMatchResult.AMBIGUOUS:
                scope_ambiguous = True

        if len(matches) > 1:
            return self._complete(
                request,
                records=records,
                outcome=AuthorityResolutionOutcome.CONFLICT,
                reason="multiple_applicable_authority_records",
                now=now,
            )
        if len(matches) == 1:
            return self._complete(
                request,
                records=records,
                outcome=AuthorityResolutionOutcome.AUTHORIZED,
                reason="explicit_authority_record_matched",
                now=now,
                selected=matches[0],
            )
        if scope_ambiguous:
            return self._complete(
                request,
                records=records,
                outcome=AuthorityResolutionOutcome.DENIED,
                reason="authority_scope_ambiguous",
                now=now,
            )
        if active:
            if all(
                record.authority_type in (AuthorityType.DELEGATED, AuthorityType.EMERGENCY)
                for record in active
            ):
                return self._complete(
                    request,
                    records=records,
                    outcome=AuthorityResolutionOutcome.INSUFFICIENT_AUTHORITY,
                    reason="deferred_authority_category",
                    now=now,
                )
            return self._complete(
                request,
                records=records,
                outcome=AuthorityResolutionOutcome.DENIED,
                reason="authority_scope_mismatch",
                now=now,
            )
        if revoked:
            return self._complete(
                request,
                records=records,
                outcome=AuthorityResolutionOutcome.REVOKED,
                reason="authority_record_revoked",
                now=now,
            )
        if expired:
            return self._complete(
                request,
                records=records,
                outcome=AuthorityResolutionOutcome.EXPIRED,
                reason="authority_record_expired",
                now=now,
            )
        if suspended:
            return self._complete(
                request,
                records=records,
                outcome=AuthorityResolutionOutcome.DENIED,
                reason="authority_record_suspended",
                now=now,
            )
        return self._complete(
            request,
            records=records,
            outcome=AuthorityResolutionOutcome.INSUFFICIENT_AUTHORITY,
            reason="no_applicable_authority_record",
            now=now,
        )

    def _complete(
        self,
        request: AuthorityResolutionRequest,
        *,
        records: Sequence[AuthorityRecord],
        outcome: AuthorityResolutionOutcome,
        reason: str,
        now: datetime,
        selected: AuthorityRecord | None = None,
    ) -> AuthorityResolutionResult:
        evidence_hash = authority_resolution_evidence_hash(request, records, now)
        authority_resolution_id = f"ares_{canonical_sha256({'evidence_hash': evidence_hash, 'outcome': outcome.value, 'reason': reason})}"
        with self._result_lock:
            cached = self._result_cache.get(authority_resolution_id)
            if cached is not None:
                return cached
            audit_event_id = f"audit_{authority_resolution_id}"
            audit = self._audit_repository.append(
                AuditRecord(
                    event_type="authority.resolution",
                    actor_id=self._component_id,
                    request_id=request.request_id or None,
                    authority_verdict_id=authority_resolution_id,
                    reason=reason,
                    details={
                        "authority_resolution_id": authority_resolution_id,
                        "evaluated_authority_record_ids": [
                            record.authority_record_id for record in records
                        ],
                        "evidence_hash": evidence_hash,
                        "identity_verdict_id": request.identity_verdict_id,
                        "outcome": outcome.value,
                        "policy_version": request.policy_version,
                    },
                    occurred_at=_timestamp(now),
                ),
                audit_event_id=audit_event_id,
                chain_id=self._audit_chain_id,
            )
            if audit.append_state is not AuditAppendState.ACCEPTED:
                raise AuthorityResolutionAuditError(
                    f"authority resolution audit append failed: {audit.reason}"
                )
            result = AuthorityResolutionResult(
                authority_resolution_id=authority_resolution_id,
                request_id=request.request_id,
                outcome=outcome,
                reason=reason,
                evidence_hash=evidence_hash,
                resolved_at=_timestamp(now),
                evaluated_authority_record_ids=tuple(
                    record.authority_record_id for record in records
                ),
                authority_record_id=selected.authority_record_id if selected else None,
                authority_source_id=selected.authority_source_id if selected else None,
                authority_type=selected.authority_type if selected else None,
                scope=freeze_authority_value(selected.scope) if selected else None,
                audit_event_id=audit_event_id,
            )
            self._result_cache[authority_resolution_id] = result
            return result

    def _utc_now(self) -> datetime:
        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise AuthorityResolutionValidationError(
                "authority resolution clock must be timezone-aware"
            )
        return now.astimezone(timezone.utc)


def validate_authority_resolution_request(request: AuthorityResolutionRequest) -> None:
    """Validate request fields without treating identity evidence as authority."""

    if not isinstance(request, AuthorityResolutionRequest):
        raise AuthorityResolutionValidationError(
            "request must be an AuthorityResolutionRequest"
        )
    for field_name in (
        "request_id",
        "subject_id",
        "requester_id",
        "action",
        "resource",
        "identity_verdict_id",
        "policy_version",
    ):
        value = getattr(request, field_name)
        if not isinstance(value, str) or not value:
            raise AuthorityResolutionValidationError(
                f"{field_name} must be a non-empty string"
            )
    if not isinstance(request.context, Mapping):
        raise AuthorityResolutionValidationError(
            "context must be a canonical JSON object"
        )
    try:
        canonical_json_text(request.context)
    except (CanonicalDataError, TypeError, ValueError) as exc:
        raise AuthorityResolutionValidationError(
            f"context is not canonical JSON: {exc}"
        ) from exc
    if request.delegation_records:
        raise AuthorityResolutionValidationError(
            "delegation records are deferred from authority resolution"
        )
    for revocation in request.revocation_records:
        if not isinstance(revocation, Mapping):
            raise AuthorityResolutionValidationError(
                "revocation records must be canonical JSON objects"
            )
        for field_name in ("revocation_id", "target_type", "target_id", "effective_at"):
            value = revocation.get(field_name)
            if not isinstance(value, str) or not value:
                raise AuthorityResolutionValidationError(
                    f"revocation {field_name} must be a non-empty string"
                )
        if revocation["target_type"] != "authority":
            raise AuthorityResolutionValidationError(
                "authority resolution accepts only authority revocation records"
            )
        parse_authority_timestamp(revocation["effective_at"], "effective_at")


def authority_resolution_evidence_hash(
    request: AuthorityResolutionRequest,
    records: Sequence[AuthorityRecord],
    resolved_at: datetime,
) -> str:
    """Hash request facts and ordered authority evidence deterministically."""

    return canonical_sha256(
        {
            "action": request.action,
            "authority_records": [
                {
                    "authority_record_id": record.authority_record_id,
                    "authority_source_id": record.authority_source_id,
                    "authority_type": record.authority_type.value,
                    "evidence_hash": record.evidence_hash,
                    "expires_at": record.expires_at,
                    "priority": record.priority,
                    "status": record.status.value,
                }
                for record in records
            ],
            "context": request.context,
            "identity_verdict_id": request.identity_verdict_id,
            "policy_version": request.policy_version,
            "request_id": request.request_id,
            "requester_id": request.requester_id,
            "revocation_records": _safe_revocation_evidence(request.revocation_records),
            "resolved_at": _timestamp(resolved_at),
            "resource": request.resource,
            "subject_id": request.subject_id,
        }
    )


def _is_expired(record: AuthorityRecord, now: datetime) -> bool:
    return record.expires_at is not None and parse_authority_timestamp(
        record.expires_at, "expires_at"
    ) <= now


def _effective_revoked_record_ids(
    revocations: Sequence[CanonicalJsonObject], now: datetime
) -> frozenset[str]:
    return frozenset(
        revocation["target_id"]
        for revocation in revocations
        if parse_authority_timestamp(revocation["effective_at"], "effective_at") <= now
    )


def _safe_revocation_evidence(revocations: Sequence[object]) -> list[dict[str, str]]:
    evidence: list[dict[str, str]] = []
    for revocation in revocations:
        if isinstance(revocation, Mapping):
            evidence.append(
                {
                    "effective_at": str(revocation.get("effective_at", "")),
                    "revocation_id": str(revocation.get("revocation_id", "")),
                    "target_id": str(revocation.get("target_id", "")),
                    "target_type": str(revocation.get("target_type", "")),
                }
            )
        else:
            evidence.append(
                {
                    "effective_at": "",
                    "revocation_id": "",
                    "target_id": repr(revocation),
                    "target_type": "invalid",
                }
            )
    return sorted(evidence, key=lambda item: (item["effective_at"], item["revocation_id"]))


def _timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
