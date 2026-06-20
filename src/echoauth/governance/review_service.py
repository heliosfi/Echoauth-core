"""Deterministic, non-authorizing Review Service for Sprint 2J."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from datetime import datetime, timezone
from threading import RLock

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth.authority_models import freeze_authority_value
from echoauth.canonical import CanonicalDataError, canonical_json_text, canonical_sha256
from echoauth.governance.escalation_models import (
    EscalationCategory,
    EscalationDecision,
    EscalationReviewType,
    EscalationState,
)
from echoauth.governance.review_models import (
    ReviewDecision,
    ReviewerAssignment,
    ReviewOutcome,
    ReviewRequest,
)
from echoauth.models import AuditAppendState, AuditRecord

REVIEW_FORMAT_VERSION = "echoauth.review.v1"


class ReviewValidationError(ValueError):
    pass


class ReviewAuditError(RuntimeError):
    pass


class ReviewService:
    """Record deterministic review outcomes from escalation decisions only."""

    def __init__(
        self,
        audit_repository: InMemoryAuditLogRepository,
        *,
        audit_chain_id: str,
        reviewer_assignments: Mapping[
            EscalationReviewType, Sequence[ReviewerAssignment]
        ],
        component_id: str = "review_service",
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if not audit_chain_id:
            raise ValueError("audit_chain_id must not be empty")
        self._assignments = _validate_assignments(reviewer_assignments)
        self._audit_repository = audit_repository
        self._audit_chain_id = audit_chain_id
        self._component_id = component_id
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._cache: dict[str, ReviewDecision] = {}
        self._lock = RLock()

    def review(
        self,
        request: ReviewRequest,
        escalation_decision: EscalationDecision,
    ) -> ReviewDecision:
        """Consume one escalation outcome without authorizing or executing it."""

        validate_review_request(request)
        self._validate_escalation(request, escalation_decision)
        assignment = self._assign_reviewer(request, escalation_decision)
        if assignment is None or assignment.reviewer_id != request.reviewer_id:
            assignment = None
            outcome = ReviewOutcome.UNRESOLVED
            reason = "reviewer_unavailable"
        else:
            outcome = request.requested_outcome
            reason = "review_recorded"

        evidence_package = {
            "assignment_authority_reference": (
                assignment.authority_reference if assignment else None
            ),
            "audit_references": list(request.audit_references),
            "authority_references": list(request.authority_references),
            "delegation_references": list(request.delegation_references),
            "escalation_audit_event_id": escalation_decision.audit_event_id,
            "escalation_category": escalation_decision.category.value,
            "escalation_decision_id": escalation_decision.escalation_decision_id,
            "escalation_evidence_hash": escalation_decision.evidence_hash,
            "format_version": REVIEW_FORMAT_VERSION,
            "policy_evidence_hash": canonical_sha256(request.policy_evidence),
            "refusal_evidence_hash": canonical_sha256(request.refusal_evidence),
            "request_evidence_hash": canonical_sha256(request.evidence),
            "request_id": request.request_id,
            "reviewer_id": assignment.reviewer_id if assignment else None,
        }
        evidence_hash = canonical_sha256(evidence_package)
        decision_hash = canonical_sha256(
            {
                "escalation_decision_id": escalation_decision.escalation_decision_id,
                "evidence_hash": evidence_hash,
                "outcome": outcome.value,
                "review_request_id": request.review_request_id,
            }
        )
        with self._lock:
            cached = self._cache.get(decision_hash)
            if cached is not None:
                return cached
            now = self._utc_now()
            review_decision_id = f"revdec_{decision_hash}"
            audit_event_id = f"audit_{review_decision_id}"
            audit = self._audit_repository.append(
                AuditRecord(
                    event_type="authorization.review",
                    actor_id=self._component_id,
                    request_id=request.request_id,
                    reason=outcome.value,
                    details={
                        "escalation_decision_id": escalation_decision.escalation_decision_id,
                        "evidence_hash": evidence_hash,
                        "format_version": REVIEW_FORMAT_VERSION,
                        "outcome": outcome.value,
                        "review_decision_id": review_decision_id,
                        "reviewer_id": assignment.reviewer_id if assignment else None,
                    },
                    occurred_at=_timestamp(now),
                ),
                audit_event_id=audit_event_id,
                chain_id=self._audit_chain_id,
            )
            if audit.append_state is not AuditAppendState.ACCEPTED:
                raise ReviewAuditError(f"review audit append failed: {audit.reason}")
            decision = ReviewDecision(
                review_decision_id=review_decision_id,
                review_request_id=request.review_request_id,
                request_id=request.request_id,
                escalation_decision_id=escalation_decision.escalation_decision_id,
                outcome=outcome,
                reviewer_id=assignment.reviewer_id if assignment else None,
                reviewer_authority_reference=(
                    assignment.authority_reference if assignment else None
                ),
                reason=reason,
                evidence_hash=evidence_hash,
                evidence=freeze_authority_value(evidence_package),
                created_at=_timestamp(now),
                audit_event_id=audit_event_id,
            )
            self._cache[decision_hash] = decision
            return decision

    @staticmethod
    def _validate_escalation(
        request: ReviewRequest,
        escalation_decision: EscalationDecision,
    ) -> None:
        if not isinstance(escalation_decision, EscalationDecision):
            raise ReviewValidationError("escalation_decision must be canonical")
        if (
            request.request_id != escalation_decision.request_id
            or request.escalation_decision_id
            != escalation_decision.escalation_decision_id
        ):
            raise ReviewValidationError("review request does not match escalation")
        if escalation_decision.resolution != "none":
            raise ReviewValidationError("review cannot consume a resolved escalation")
        required_evidence = (
            "authorization_decision_id",
            "authorization_evidence_hash",
            "refusal_decision_id",
            "refusal_evidence_hash",
        )
        if any(not escalation_decision.evidence.get(key) for key in required_evidence):
            raise ReviewValidationError("escalation history evidence is incomplete")
        if (
            request.refusal_evidence.get("refusal_decision_id")
            != escalation_decision.evidence.get("refusal_decision_id")
            or request.refusal_evidence.get("refusal_evidence_hash")
            != escalation_decision.evidence.get("refusal_evidence_hash")
        ):
            raise ReviewValidationError("refusal evidence does not match escalation")
        required_audit_references = {
            reference
            for reference in (
                escalation_decision.audit_event_id,
                escalation_decision.evidence.get("authorization_audit_event_id"),
                escalation_decision.evidence.get("refusal_audit_event_id"),
            )
            if reference
        }
        if not required_audit_references.issubset(set(request.audit_references)):
            raise ReviewValidationError("audit history references are incomplete")

    def _assign_reviewer(
        self,
        request: ReviewRequest,
        escalation_decision: EscalationDecision,
    ) -> ReviewerAssignment | None:
        if (
            escalation_decision.escalation_state is not EscalationState.OPENED
            or escalation_decision.category
            in {
                EscalationCategory.SYSTEM_HOLD,
                EscalationCategory.NO_ESCALATION_AVAILABLE,
            }
        ):
            return None
        review_type = escalation_decision.reason.required_authority_type
        expected_category = _CATEGORY_BY_REVIEW_TYPE.get(review_type)
        if expected_category is not escalation_decision.category:
            return None
        for assignment in self._assignments.get(review_type, ()):
            if assignment.authority_reference in request.authority_references:
                return assignment
        return None

    def _utc_now(self) -> datetime:
        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise ReviewValidationError("review clock must be timezone-aware")
        return now.astimezone(timezone.utc)


def validate_review_request(request: ReviewRequest) -> None:
    if not isinstance(request, ReviewRequest):
        raise ReviewValidationError("request must be a ReviewRequest")
    for field_name in (
        "review_request_id",
        "request_id",
        "escalation_decision_id",
        "reviewer_id",
    ):
        value = getattr(request, field_name)
        if not isinstance(value, str) or not value:
            raise ReviewValidationError(f"{field_name} must be non-empty")
    if not isinstance(request.requested_outcome, ReviewOutcome):
        raise ReviewValidationError("requested_outcome must be canonical")
    for field_name in (
        "authority_references",
        "delegation_references",
        "audit_references",
    ):
        _validate_references(getattr(request, field_name), field_name)
    for field_name in ("policy_evidence", "refusal_evidence", "evidence"):
        value = getattr(request, field_name)
        if not isinstance(value, Mapping):
            raise ReviewValidationError(f"{field_name} must be a canonical JSON object")
        try:
            canonical_json_text(value)
        except (CanonicalDataError, TypeError, ValueError) as exc:
            raise ReviewValidationError(
                f"{field_name} is not canonical JSON: {exc}"
            ) from exc


def _validate_assignments(
    assignments: Mapping[EscalationReviewType, Sequence[ReviewerAssignment]],
) -> dict[EscalationReviewType, tuple[ReviewerAssignment, ...]]:
    if not isinstance(assignments, Mapping):
        raise ReviewValidationError("reviewer_assignments must be a mapping")
    validated: dict[EscalationReviewType, tuple[ReviewerAssignment, ...]] = {}
    reviewer_ids: set[str] = set()
    for review_type, candidates in assignments.items():
        if not isinstance(review_type, EscalationReviewType):
            raise ReviewValidationError("reviewer assignment type must be canonical")
        if not isinstance(candidates, (list, tuple)):
            raise ReviewValidationError("reviewer candidates must be ordered")
        checked: list[ReviewerAssignment] = []
        for candidate in candidates:
            if not isinstance(candidate, ReviewerAssignment):
                raise ReviewValidationError("reviewer candidate must be canonical")
            if candidate.review_type is not review_type:
                raise ReviewValidationError("reviewer type does not match assignment route")
            if not candidate.reviewer_id or not candidate.authority_reference:
                raise ReviewValidationError("reviewer assignment fields must be non-empty")
            if candidate.reviewer_id in reviewer_ids:
                raise ReviewValidationError("reviewer_id must be unique")
            reviewer_ids.add(candidate.reviewer_id)
            checked.append(candidate)
        validated[review_type] = tuple(checked)
    return validated


def _validate_references(value: object, field_name: str) -> None:
    if not isinstance(value, tuple):
        raise ReviewValidationError(f"{field_name} must be a tuple")
    if any(not isinstance(item, str) or not item for item in value):
        raise ReviewValidationError(f"{field_name} entries must be non-empty strings")
    if len(set(value)) != len(value):
        raise ReviewValidationError(f"{field_name} entries must be unique")


_CATEGORY_BY_REVIEW_TYPE = {
    EscalationReviewType.HUMAN: EscalationCategory.HUMAN_REVIEW_REQUIRED,
    EscalationReviewType.GUARDIAN: EscalationCategory.GUARDIAN_REVIEW_REQUIRED,
    EscalationReviewType.PARENT: EscalationCategory.PARENT_REVIEW_REQUIRED,
    EscalationReviewType.ADMIN: EscalationCategory.ADMIN_REVIEW_REQUIRED,
    EscalationReviewType.CLINICAL: EscalationCategory.CLINICAL_REVIEW_REQUIRED,
}


def _timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
