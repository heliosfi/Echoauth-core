"""Deterministic, refusal-preserving escalation routing for Sprint 2I."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from threading import RLock

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth.authorization_models import AuthorizationDecision, AuthorizationOutcome
from echoauth.auth.authority_models import freeze_authority_value
from echoauth.canonical import CanonicalDataError, canonical_json_text, canonical_sha256
from echoauth.governance.escalation_models import (
    EscalationCategory,
    EscalationDecision,
    EscalationReason,
    EscalationRequest,
    EscalationReviewType,
    EscalationState,
)
from echoauth.models import AuditAppendState, AuditRecord
from echoauth.policy.refusal_models import RefusalCategory, RefusalDecision

ESCALATION_MAPPING_VERSION = "echoauth.escalation.v1"


class EscalationValidationError(ValueError):
    pass


class EscalationAuditError(RuntimeError):
    pass


class EscalationService:
    """Classify review routing from immutable authorization and refusal outputs."""

    def __init__(
        self,
        audit_repository: InMemoryAuditLogRepository,
        *,
        audit_chain_id: str,
        component_id: str = "escalation_service",
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if not audit_chain_id:
            raise ValueError("audit_chain_id must not be empty")
        self._audit_repository = audit_repository
        self._audit_chain_id = audit_chain_id
        self._component_id = component_id
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._cache: dict[str, EscalationDecision] = {}
        self._lock = RLock()

    def escalate(
        self,
        request: EscalationRequest,
        authorization_decision: AuthorizationDecision,
        refusal_decision: RefusalDecision,
    ) -> EscalationDecision:
        """Open a review route without re-evaluating or changing authorization."""

        validate_escalation_request(request)
        self._validate_dependencies(request, authorization_decision, refusal_decision)
        now = self._utc_now()
        expired = request.deadline_at is not None and _parse_utc(request.deadline_at) <= now
        category = _classify(request, expired=expired)
        state = EscalationState.EXPIRED if expired else EscalationState.OPENED
        reason = EscalationReason(
            category=category,
            trigger_state=request.trigger_state,
            trigger_reason=request.trigger_reason,
            refusal_category=request.refusal_category,
            required_authority_type=request.required_authority_type,
            mapping_version=ESCALATION_MAPPING_VERSION,
        )
        evidence_package = {
            "authorization_audit_event_id": authorization_decision.audit_event_id,
            "authorization_decision_id": authorization_decision.authorization_decision_id,
            "authorization_evidence_hash": authorization_decision.evidence_hash,
            "authorization_outcome": authorization_decision.outcome.value,
            "deadline_at": request.deadline_at,
            "mapping_version": ESCALATION_MAPPING_VERSION,
            "refusal_audit_event_id": refusal_decision.audit_event_id,
            "refusal_category": refusal_decision.category.value,
            "refusal_decision_id": refusal_decision.refusal_decision_id,
            "refusal_evidence_hash": refusal_decision.evidence_hash,
            "request_evidence_hash": canonical_sha256(request.evidence),
            "request_id": request.request_id,
            "required_authority_type": request.required_authority_type.value,
        }
        evidence_hash = canonical_sha256(evidence_package)
        decision_hash = canonical_sha256(
            {
                "category": category.value,
                "escalation_id": request.escalation_id,
                "evidence_hash": evidence_hash,
                "state": state.value,
            }
        )
        with self._lock:
            cached = self._cache.get(decision_hash)
            if cached is not None:
                return cached
            escalation_decision_id = f"edec_{decision_hash}"
            audit_event_id = f"audit_{escalation_decision_id}"
            audit = self._audit_repository.append(
                AuditRecord(
                    event_type="authorization.escalation",
                    actor_id=self._component_id,
                    request_id=request.request_id,
                    authority_verdict_id=authorization_decision.authority_resolution_id,
                    reason=category.value,
                    details={
                        "category": category.value,
                        "escalation_decision_id": escalation_decision_id,
                        "escalation_id": request.escalation_id,
                        "evidence_hash": evidence_hash,
                        "mapping_version": ESCALATION_MAPPING_VERSION,
                        "refusal_decision_id": refusal_decision.refusal_decision_id,
                        "state": state.value,
                    },
                    occurred_at=_timestamp(now),
                ),
                audit_event_id=audit_event_id,
                chain_id=self._audit_chain_id,
            )
            if audit.append_state is not AuditAppendState.ACCEPTED:
                raise EscalationAuditError(f"escalation audit append failed: {audit.reason}")
            decision = EscalationDecision(
                escalation_decision_id=escalation_decision_id,
                escalation_id=request.escalation_id,
                request_id=request.request_id,
                category=category,
                escalation_state=state,
                resolution="none",
                reason=reason,
                evidence_hash=evidence_hash,
                evidence=freeze_authority_value(evidence_package),
                created_at=_timestamp(now),
                deadline_at=request.deadline_at,
                audit_event_id=audit_event_id,
            )
            self._cache[decision_hash] = decision
            return decision

    @staticmethod
    def _validate_dependencies(
        request: EscalationRequest,
        authorization_decision: AuthorizationDecision,
        refusal_decision: RefusalDecision,
    ) -> None:
        if not isinstance(authorization_decision, AuthorizationDecision):
            raise EscalationValidationError("authorization_decision must be canonical")
        if not isinstance(refusal_decision, RefusalDecision):
            raise EscalationValidationError("refusal_decision must be canonical")
        if authorization_decision.outcome is AuthorizationOutcome.AUTHORIZED:
            raise EscalationValidationError("authorized decisions cannot be escalated")
        if (
            request.request_id != authorization_decision.request_id
            or request.request_id != refusal_decision.request_id
            or request.authorization_decision_id
            != authorization_decision.authorization_decision_id
            or request.refusal_decision_id != refusal_decision.refusal_decision_id
            or request.refusal_category is not refusal_decision.category
            or refusal_decision.evidence.get("authorization_decision_id")
            != authorization_decision.authorization_decision_id
            or refusal_decision.evidence.get("authorization_evidence_hash")
            != authorization_decision.evidence_hash
        ):
            raise EscalationValidationError(
                "authorization and refusal evidence do not match escalation request"
            )

    def _utc_now(self) -> datetime:
        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise EscalationValidationError("escalation clock must be timezone-aware")
        return now.astimezone(timezone.utc)


def validate_escalation_request(request: EscalationRequest) -> None:
    if not isinstance(request, EscalationRequest):
        raise EscalationValidationError("request must be an EscalationRequest")
    for field_name in (
        "escalation_id",
        "request_id",
        "subject_id",
        "trigger_state",
        "trigger_reason",
        "authorization_decision_id",
        "refusal_decision_id",
    ):
        value = getattr(request, field_name)
        if not isinstance(value, str) or not value:
            raise EscalationValidationError(f"{field_name} must be non-empty")
    if not isinstance(request.required_authority_type, EscalationReviewType):
        raise EscalationValidationError("required_authority_type must be canonical")
    if not isinstance(request.refusal_category, RefusalCategory):
        raise EscalationValidationError("refusal_category must be canonical")
    if not isinstance(request.evidence, Mapping):
        raise EscalationValidationError("evidence must be a canonical JSON object")
    try:
        canonical_json_text(request.evidence)
    except (CanonicalDataError, TypeError, ValueError) as exc:
        raise EscalationValidationError(f"evidence is not canonical JSON: {exc}") from exc
    if request.deadline_at is not None:
        _parse_utc(request.deadline_at)


def _classify(request: EscalationRequest, *, expired: bool) -> EscalationCategory:
    if expired or request.refusal_category is RefusalCategory.MALFORMED_REQUEST:
        return EscalationCategory.NO_ESCALATION_AVAILABLE
    if request.refusal_category is RefusalCategory.UNAVAILABLE_DEPENDENCY:
        return EscalationCategory.SYSTEM_HOLD
    return {
        EscalationReviewType.HUMAN: EscalationCategory.HUMAN_REVIEW_REQUIRED,
        EscalationReviewType.GUARDIAN: EscalationCategory.GUARDIAN_REVIEW_REQUIRED,
        EscalationReviewType.PARENT: EscalationCategory.PARENT_REVIEW_REQUIRED,
        EscalationReviewType.ADMIN: EscalationCategory.ADMIN_REVIEW_REQUIRED,
        EscalationReviewType.CLINICAL: EscalationCategory.CLINICAL_REVIEW_REQUIRED,
        EscalationReviewType.NONE: EscalationCategory.NO_ESCALATION_AVAILABLE,
    }[request.required_authority_type]


def _parse_utc(value: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise EscalationValidationError("deadline_at must be a non-empty timestamp")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise EscalationValidationError("deadline_at must be ISO 8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise EscalationValidationError("deadline_at must be timezone-aware")
    if parsed.utcoffset().total_seconds() != 0:
        raise EscalationValidationError("deadline_at must be UTC")
    return parsed.astimezone(timezone.utc)


def _timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
