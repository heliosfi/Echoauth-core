"""Deterministic, non-executing Override Service for Sprint 2K."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import asdict
from datetime import datetime, timezone
from threading import RLock

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth.authorization_models import AuthorizationDecision, AuthorizationOutcome
from echoauth.auth.authority_models import freeze_authority_value
from echoauth.canonical import CanonicalDataError, canonical_json_text, canonical_sha256
from echoauth.governance.escalation_models import EscalationDecision
from echoauth.governance.override_models import (
    OverrideAuthority,
    OverrideDecision,
    OverrideEvidence,
    OverrideOutcome,
    OverrideReason,
    OverrideRequest,
)
from echoauth.governance.review_models import ReviewDecision, ReviewOutcome
from echoauth.models import AuditAppendState, AuditRecord
from echoauth.policy.refusal_models import RefusalDecision

OVERRIDE_FORMAT_VERSION = "echoauth.override.v1"


class OverrideValidationError(ValueError):
    pass


class OverrideAuditError(RuntimeError):
    pass


class OverrideService:
    """Classify override records without authorizing or executing an action."""

    def __init__(
        self,
        audit_repository: InMemoryAuditLogRepository,
        *,
        audit_chain_id: str,
        override_authorities: Sequence[OverrideAuthority],
        component_id: str = "override_service",
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if not audit_chain_id:
            raise ValueError("audit_chain_id must not be empty")
        self._authorities = _validate_authorities(override_authorities)
        self._audit_repository = audit_repository
        self._audit_chain_id = audit_chain_id
        self._component_id = component_id
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._cache: dict[str, OverrideDecision] = {}
        self._lock = RLock()

    def decide(
        self,
        request: OverrideRequest,
        authorization_decision: AuthorizationDecision,
        refusal_decision: RefusalDecision,
        escalation_decision: EscalationDecision,
        review_decision: ReviewDecision,
    ) -> OverrideDecision:
        """Produce an inert override classification from the complete evidence chain."""

        validate_override_request(request)
        self._validate_evidence_chain(
            request,
            authorization_decision,
            refusal_decision,
            escalation_decision,
            review_decision,
        )
        now = self._utc_now()
        authority_valid = self._authority_is_valid(request)
        outcome, reason_code = _classify(
            expired=_parse_utc(request.expires_at) <= now,
            authority_valid=authority_valid,
            review_outcome=review_decision.outcome,
        )
        reason = OverrideReason(
            outcome=outcome,
            code=reason_code,
            authority_valid=authority_valid,
            review_outcome=review_decision.outcome.value,
            format_version=OVERRIDE_FORMAT_VERSION,
        )
        evidence = OverrideEvidence(
            authorization_decision_id=authorization_decision.authorization_decision_id,
            authorization_evidence_hash=authorization_decision.evidence_hash,
            refusal_decision_id=refusal_decision.refusal_decision_id,
            refusal_evidence_hash=refusal_decision.evidence_hash,
            escalation_decision_id=escalation_decision.escalation_decision_id,
            escalation_evidence_hash=escalation_decision.evidence_hash,
            review_decision_id=review_decision.review_decision_id,
            review_evidence_hash=review_decision.evidence_hash,
            override_authority_id=request.override_authority_id,
            override_authority_reference=request.override_authority_reference,
            declared_by=request.declared_by,
            emergency_type=request.emergency_type,
            requested_action=request.requested_action,
            policy_version=request.policy_version,
            review_outcome=review_decision.outcome.value,
            expires_at=request.expires_at,
            effective_scope_hash=canonical_sha256(request.effective_scope),
            request_evidence_hash=canonical_sha256(request.evidence),
            audit_references=request.audit_references,
        )
        evidence_hash = canonical_sha256(asdict(evidence))
        decision_hash = canonical_sha256(
            {
                "evidence_hash": evidence_hash,
                "outcome": outcome.value,
                "override_id": request.override_id,
                "reason": reason_code,
            }
        )
        with self._lock:
            cached = self._cache.get(decision_hash)
            if cached is not None:
                return cached
            override_decision_id = f"ovrdec_{decision_hash}"
            audit_event_id = f"audit_{override_decision_id}"
            audit = self._audit_repository.append(
                AuditRecord(
                    event_type="authorization.override",
                    actor_id=self._component_id,
                    request_id=request.request_id,
                    reason=reason_code,
                    details={
                        "authority_reference": request.override_authority_reference,
                        "declared_by": request.declared_by,
                        "effective_scope_hash": evidence.effective_scope_hash,
                        "emergency_type": request.emergency_type,
                        "evidence_hash": evidence_hash,
                        "expires_at": request.expires_at,
                        "format_version": OVERRIDE_FORMAT_VERSION,
                        "outcome": outcome.value,
                        "override_decision_id": override_decision_id,
                        "override_id": request.override_id,
                        "requested_action": request.requested_action,
                        "review_decision_id": review_decision.review_decision_id,
                        "review_required": True,
                    },
                    occurred_at=_timestamp(now),
                ),
                audit_event_id=audit_event_id,
                chain_id=self._audit_chain_id,
            )
            if audit.append_state is not AuditAppendState.ACCEPTED:
                raise OverrideAuditError(f"override audit append failed: {audit.reason}")
            decision = OverrideDecision(
                override_decision_id=override_decision_id,
                override_id=request.override_id,
                request_id=request.request_id,
                outcome=outcome,
                reason=reason,
                evidence=evidence,
                evidence_hash=evidence_hash,
                effective_scope=freeze_authority_value(request.effective_scope),
                review_required=True,
                expires_at=request.expires_at,
                created_at=_timestamp(now),
                audit_event_id=audit_event_id,
            )
            self._cache[decision_hash] = decision
            return decision

    @staticmethod
    def _validate_evidence_chain(
        request: OverrideRequest,
        authorization: AuthorizationDecision,
        refusal: RefusalDecision,
        escalation: EscalationDecision,
        review: ReviewDecision,
    ) -> None:
        if not isinstance(authorization, AuthorizationDecision):
            raise OverrideValidationError("authorization_decision must be canonical")
        if not isinstance(refusal, RefusalDecision):
            raise OverrideValidationError("refusal_decision must be canonical")
        if not isinstance(escalation, EscalationDecision):
            raise OverrideValidationError("escalation_decision must be canonical")
        if not isinstance(review, ReviewDecision):
            raise OverrideValidationError("review_decision must be canonical")
        if authorization.outcome is AuthorizationOutcome.AUTHORIZED:
            raise OverrideValidationError("authorized decisions cannot enter override")
        if any(
            item.request_id != request.request_id
            for item in (authorization, refusal, escalation, review)
        ):
            raise OverrideValidationError("override evidence request IDs do not match")
        if (
            refusal.evidence.get("authorization_decision_id")
            != authorization.authorization_decision_id
            or refusal.evidence.get("authorization_evidence_hash")
            != authorization.evidence_hash
            or escalation.evidence.get("authorization_decision_id")
            != authorization.authorization_decision_id
            or escalation.evidence.get("refusal_decision_id")
            != refusal.refusal_decision_id
            or escalation.evidence.get("refusal_evidence_hash") != refusal.evidence_hash
            or review.escalation_decision_id != escalation.escalation_decision_id
            or review.evidence.get("escalation_evidence_hash")
            != escalation.evidence_hash
        ):
            raise OverrideValidationError("override evidence chain is inconsistent")
        required_audits = {
            reference
            for reference in (
                authorization.audit_event_id,
                refusal.audit_event_id,
                escalation.audit_event_id,
                review.audit_event_id,
            )
            if reference
        }
        if not required_audits.issubset(set(request.audit_references)):
            raise OverrideValidationError("override audit references are incomplete")

    def _authority_is_valid(self, request: OverrideRequest) -> bool:
        authority = self._authorities.get(request.override_authority_id)
        return (
            authority is not None
            and authority.authority_reference == request.override_authority_reference
            and request.declared_by == authority.authority_id
        )

    def _utc_now(self) -> datetime:
        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise OverrideValidationError("override clock must be timezone-aware")
        return now.astimezone(timezone.utc)


def validate_override_request(request: OverrideRequest) -> None:
    if not isinstance(request, OverrideRequest):
        raise OverrideValidationError("request must be an OverrideRequest")
    for field_name in (
        "override_id",
        "request_id",
        "subject_id",
        "declared_by",
        "emergency_type",
        "requested_action",
        "override_authority_id",
        "override_authority_reference",
        "policy_version",
        "expires_at",
    ):
        value = getattr(request, field_name)
        if not isinstance(value, str) or not value:
            raise OverrideValidationError(f"{field_name} must be non-empty")
    _parse_utc(request.expires_at)
    for field_name in ("effective_scope", "evidence"):
        value = getattr(request, field_name)
        if not isinstance(value, Mapping) or not value:
            raise OverrideValidationError(
                f"{field_name} must be a non-empty canonical JSON object"
            )
        try:
            canonical_json_text(value)
        except (CanonicalDataError, TypeError, ValueError) as exc:
            raise OverrideValidationError(
                f"{field_name} is not canonical JSON: {exc}"
            ) from exc
    if not isinstance(request.audit_references, tuple):
        raise OverrideValidationError("audit_references must be a tuple")
    if any(not isinstance(item, str) or not item for item in request.audit_references):
        raise OverrideValidationError(
            "audit_references entries must be non-empty strings"
        )
    if len(set(request.audit_references)) != len(request.audit_references):
        raise OverrideValidationError("audit_references entries must be unique")


def _validate_authorities(
    authorities: Sequence[OverrideAuthority],
) -> dict[str, OverrideAuthority]:
    if not isinstance(authorities, (list, tuple)):
        raise OverrideValidationError("override_authorities must be ordered")
    result: dict[str, OverrideAuthority] = {}
    references: set[str] = set()
    for authority in authorities:
        if not isinstance(authority, OverrideAuthority):
            raise OverrideValidationError("override authority must be canonical")
        if not authority.authority_id or not authority.authority_reference:
            raise OverrideValidationError("override authority fields must be non-empty")
        if authority.authority_id in result or authority.authority_reference in references:
            raise OverrideValidationError("override authorities must be unique")
        result[authority.authority_id] = authority
        references.add(authority.authority_reference)
    return result


def _classify(
    *,
    expired: bool,
    authority_valid: bool,
    review_outcome: ReviewOutcome,
) -> tuple[OverrideOutcome, str]:
    if expired:
        return OverrideOutcome.EXPIRED, "override_expired"
    if not authority_valid:
        return OverrideOutcome.DENIED, "override_authority_invalid"
    if review_outcome is ReviewOutcome.DENIED_AFTER_REVIEW:
        return OverrideOutcome.DENIED, "review_denied"
    if review_outcome is ReviewOutcome.APPROVED_FOR_OVERRIDE_REVIEW:
        return OverrideOutcome.APPROVED, "override_record_approved"
    return OverrideOutcome.DEFERRED, "additional_review_required"


def _parse_utc(value: str) -> datetime:
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise OverrideValidationError("expires_at must be ISO 8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise OverrideValidationError("expires_at must be timezone-aware")
    if parsed.utcoffset().total_seconds() != 0:
        raise OverrideValidationError("expires_at must be UTC")
    return parsed.astimezone(timezone.utc)


def _timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
