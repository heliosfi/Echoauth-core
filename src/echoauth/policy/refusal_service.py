"""Deterministic dependency-aware Refusal Service for Sprint 2H."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from threading import RLock

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth.authorization_models import AuthorizationDecision, AuthorizationOutcome
from echoauth.auth.authority_models import freeze_authority_value
from echoauth.canonical import CanonicalDataError, canonical_json_text, canonical_sha256
from echoauth.models import AuditAppendState, AuditRecord
from echoauth.policy.refusal_models import (
    RefusalCategory,
    RefusalDecision,
    RefusalFailureSource,
    RefusalReason,
    RefusalRequest,
    RefusalSeverity,
)

REFUSAL_MAPPING_VERSION = "echoauth.refusal.v1"


class RefusalValidationError(ValueError):
    pass


class RefusalAuditError(RuntimeError):
    pass


class RefusalService:
    """Translate an existing failed authorization decision without modifying it."""

    def __init__(
        self,
        audit_repository: InMemoryAuditLogRepository,
        *,
        audit_chain_id: str,
        component_id: str = "refusal_service",
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if not audit_chain_id:
            raise ValueError("audit_chain_id must not be empty")
        self._audit_repository = audit_repository
        self._audit_chain_id = audit_chain_id
        self._component_id = component_id
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._cache: dict[str, RefusalDecision] = {}
        self._lock = RLock()

    def refuse(
        self,
        request: RefusalRequest,
        authorization_decision: AuthorizationDecision,
    ) -> RefusalDecision:
        """Return a deterministic explanation for a non-authorized decision."""

        validate_refusal_request(request)
        if authorization_decision.outcome is AuthorizationOutcome.AUTHORIZED:
            raise RefusalValidationError("authorized decisions cannot produce refusals")
        category, expected_source = _map_authorization_decision(authorization_decision)
        if (
            request.request_id != authorization_decision.request_id
            or request.authorization_decision_id
            != authorization_decision.authorization_decision_id
            or request.authorization_outcome != authorization_decision.outcome.value
            or request.failure_code != authorization_decision.reason
            or request.failure_source is not expected_source
        ):
            category = RefusalCategory.MALFORMED_REQUEST
            expected_source = RefusalFailureSource.RUNTIME

        recovery_path = "retry_dependency" if (
            category is RefusalCategory.UNAVAILABLE_DEPENDENCY and request.recoverable
        ) else "none"
        reason = RefusalReason(
            category=category,
            failure_source=expected_source,
            failure_code=request.failure_code,
            severity=request.severity,
            recoverable=request.recoverable,
            recovery_path=recovery_path,
            mapping_version=REFUSAL_MAPPING_VERSION,
        )
        evidence_package = {
            "authorization_decision_id": authorization_decision.authorization_decision_id,
            "authorization_evidence_hash": authorization_decision.evidence_hash,
            "authorization_outcome": authorization_decision.outcome.value,
            "failure_code": request.failure_code,
            "failure_source": expected_source.value,
            "mapping_version": REFUSAL_MAPPING_VERSION,
            "request_evidence_hash": canonical_sha256(request.evidence),
            "request_id": request.request_id,
        }
        evidence_hash = canonical_sha256(evidence_package)
        decision_hash = canonical_sha256(
            {
                "category": category.value,
                "evidence_hash": evidence_hash,
                "reason": request.failure_code,
            }
        )
        with self._lock:
            cached = self._cache.get(decision_hash)
            if cached is not None:
                return cached
            now = self._utc_now()
            refusal_decision_id = f"rdec_{decision_hash}"
            audit_event_id = f"audit_{refusal_decision_id}"
            audit = self._audit_repository.append(
                AuditRecord(
                    event_type="authorization.refusal",
                    actor_id=self._component_id,
                    request_id=request.request_id,
                    authority_verdict_id=authorization_decision.authority_resolution_id,
                    reason=request.failure_code,
                    details={
                        "category": category.value,
                        "evidence_hash": evidence_hash,
                        "failure_source": expected_source.value,
                        "mapping_version": REFUSAL_MAPPING_VERSION,
                        "refusal_decision_id": refusal_decision_id,
                        "severity": request.severity.value,
                    },
                    occurred_at=_timestamp(now),
                ),
                audit_event_id=audit_event_id,
                chain_id=self._audit_chain_id,
            )
            if audit.append_state is not AuditAppendState.ACCEPTED:
                raise RefusalAuditError(f"refusal audit append failed: {audit.reason}")
            decision = RefusalDecision(
                refusal_decision_id=refusal_decision_id,
                refusal_request_id=request.refusal_request_id,
                request_id=request.request_id,
                category=category,
                reason=reason,
                evidence_hash=evidence_hash,
                evidence=freeze_authority_value(evidence_package),
                created_at=_timestamp(now),
                audit_event_id=audit_event_id,
            )
            self._cache[decision_hash] = decision
            return decision

    def _utc_now(self) -> datetime:
        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise RefusalValidationError("refusal clock must be timezone-aware")
        return now.astimezone(timezone.utc)


def refusal_request_from_decision(
    decision: AuthorizationDecision,
    *,
    refusal_request_id: str,
    severity: RefusalSeverity = RefusalSeverity.HIGH,
    recoverable: bool = False,
    evidence: Mapping[str, object] | None = None,
) -> RefusalRequest:
    """Build contract-shaped refusal input from an immutable gate decision."""

    if decision.outcome is AuthorizationOutcome.AUTHORIZED:
        raise RefusalValidationError("authorized decisions cannot produce refusals")
    _, source = _map_authorization_decision(decision)
    return RefusalRequest(
        refusal_request_id=refusal_request_id,
        request_id=decision.request_id,
        failure_source=source,
        failure_code=decision.reason,
        severity=severity,
        recoverable=recoverable,
        evidence=freeze_authority_value(evidence or {}),
        authorization_decision_id=decision.authorization_decision_id,
        authorization_outcome=decision.outcome.value,
    )


def validate_refusal_request(request: RefusalRequest) -> None:
    if not isinstance(request, RefusalRequest):
        raise RefusalValidationError("request must be a RefusalRequest")
    for field_name in (
        "refusal_request_id",
        "request_id",
        "failure_code",
        "authorization_decision_id",
        "authorization_outcome",
    ):
        value = getattr(request, field_name)
        if not isinstance(value, str) or not value:
            raise RefusalValidationError(f"{field_name} must be non-empty")
    if not isinstance(request.failure_source, RefusalFailureSource):
        raise RefusalValidationError("failure_source must be canonical")
    if not isinstance(request.severity, RefusalSeverity):
        raise RefusalValidationError("severity must be canonical")
    if not isinstance(request.recoverable, bool):
        raise RefusalValidationError("recoverable must be boolean")
    if not isinstance(request.evidence, Mapping):
        raise RefusalValidationError("evidence must be a canonical JSON object")
    try:
        canonical_json_text(request.evidence)
    except (CanonicalDataError, TypeError, ValueError) as exc:
        raise RefusalValidationError(f"evidence is not canonical JSON: {exc}") from exc


def _map_authorization_decision(
    decision: AuthorizationDecision,
) -> tuple[RefusalCategory, RefusalFailureSource]:
    if "dependency_failed" in decision.reason:
        return RefusalCategory.UNAVAILABLE_DEPENDENCY, _source_from_reason(decision.reason)
    if decision.reason == "invalid_authorization_request":
        return RefusalCategory.MALFORMED_REQUEST, RefusalFailureSource.RUNTIME
    mapping = {
        AuthorizationOutcome.INVALID_IDENTITY: (
            RefusalCategory.INVALID_IDENTITY,
            RefusalFailureSource.IDENTITY,
        ),
        AuthorizationOutcome.INVALID_AUTHORITY: (
            RefusalCategory.INVALID_AUTHORITY,
            RefusalFailureSource.AUTHORITY,
        ),
        AuthorizationOutcome.INVALID_DELEGATION: (
            RefusalCategory.INVALID_DELEGATION,
            RefusalFailureSource.DELEGATION,
        ),
        AuthorizationOutcome.INVALID_POLICY: (
            RefusalCategory.UNAVAILABLE_DEPENDENCY,
            RefusalFailureSource.POLICY,
        ),
        AuthorizationOutcome.DENIED: (
            RefusalCategory.POLICY_DENIED,
            RefusalFailureSource.POLICY,
        ),
        AuthorizationOutcome.REVOKED: (
            RefusalCategory.REVOKED,
            _source_from_reason(decision.reason),
        ),
        AuthorizationOutcome.EXPIRED: (
            RefusalCategory.EXPIRED,
            _source_from_reason(decision.reason),
        ),
        AuthorizationOutcome.CONFLICT: (
            RefusalCategory.CONFLICT,
            _source_from_reason(decision.reason),
        ),
    }
    try:
        return mapping[decision.outcome]
    except KeyError as exc:
        raise RefusalValidationError(
            f"unsupported authorization outcome: {decision.outcome}"
        ) from exc


def _source_from_reason(reason: str) -> RefusalFailureSource:
    prefix = reason.split("_", 1)[0]
    return {
        "identity": RefusalFailureSource.IDENTITY,
        "authority": RefusalFailureSource.AUTHORITY,
        "delegation": RefusalFailureSource.DELEGATION,
        "policy": RefusalFailureSource.POLICY,
        "audit": RefusalFailureSource.AUDIT,
    }.get(prefix, RefusalFailureSource.RUNTIME)


def _timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
