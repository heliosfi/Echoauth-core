"""Canonical review-routing models for Sprint 2J."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from echoauth.governance.escalation_models import EscalationReviewType


class ReviewOutcome(str, Enum):
    APPROVED_FOR_OVERRIDE_REVIEW = "approved_for_override_review"
    DENIED_AFTER_REVIEW = "denied_after_review"
    RETURNED_FOR_INFORMATION = "returned_for_information"
    DELEGATED_REVIEW_REQUIRED = "delegated_review_required"
    GUARDIAN_REVIEW_REQUIRED = "guardian_review_required"
    PARENT_REVIEW_REQUIRED = "parent_review_required"
    CLINICAL_REVIEW_REQUIRED = "clinical_review_required"
    ADMINISTRATIVE_REVIEW_REQUIRED = "administrative_review_required"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True)
class ReviewerAssignment:
    """One configured reviewer route; this is not an identity lookup."""

    reviewer_id: str
    review_type: EscalationReviewType
    authority_reference: str


@dataclass(frozen=True)
class ReviewRequest:
    review_request_id: str
    request_id: str
    escalation_decision_id: str
    reviewer_id: str
    requested_outcome: ReviewOutcome
    authority_references: tuple[str, ...]
    delegation_references: tuple[str, ...]
    policy_evidence: Mapping[str, Any]
    refusal_evidence: Mapping[str, Any]
    audit_references: tuple[str, ...]
    evidence: Mapping[str, Any]


@dataclass(frozen=True)
class ReviewDecision:
    review_decision_id: str
    review_request_id: str
    request_id: str
    escalation_decision_id: str
    outcome: ReviewOutcome
    reviewer_id: str | None
    reviewer_authority_reference: str | None
    reason: str
    evidence_hash: str
    evidence: Mapping[str, Any]
    created_at: str
    audit_event_id: str | None = None
