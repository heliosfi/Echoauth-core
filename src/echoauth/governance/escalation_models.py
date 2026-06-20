"""Canonical escalation-routing models for Sprint 2I."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from echoauth.policy.refusal_models import RefusalCategory


class EscalationCategory(str, Enum):
    HUMAN_REVIEW_REQUIRED = "human_review_required"
    GUARDIAN_REVIEW_REQUIRED = "guardian_review_required"
    PARENT_REVIEW_REQUIRED = "parent_review_required"
    ADMIN_REVIEW_REQUIRED = "admin_review_required"
    CLINICAL_REVIEW_REQUIRED = "clinical_review_required"
    SYSTEM_HOLD = "system_hold"
    NO_ESCALATION_AVAILABLE = "no_escalation_available"


class EscalationReviewType(str, Enum):
    """Explicit review routes supported without a reviewer registry."""

    HUMAN = "human"
    GUARDIAN = "guardian"
    PARENT = "parent"
    ADMIN = "admin"
    CLINICAL = "clinical"
    NONE = "none"


class EscalationState(str, Enum):
    OPENED = "opened"
    EXPIRED = "expired"


@dataclass(frozen=True)
class EscalationRequest:
    escalation_id: str
    request_id: str
    subject_id: str
    trigger_state: str
    trigger_reason: str
    required_authority_type: EscalationReviewType
    evidence: Mapping[str, Any]
    authorization_decision_id: str
    refusal_decision_id: str
    refusal_category: RefusalCategory
    deadline_at: str | None = None


@dataclass(frozen=True)
class EscalationReason:
    category: EscalationCategory
    trigger_state: str
    trigger_reason: str
    refusal_category: RefusalCategory
    required_authority_type: EscalationReviewType
    mapping_version: str


@dataclass(frozen=True)
class EscalationDecision:
    escalation_decision_id: str
    escalation_id: str
    request_id: str
    category: EscalationCategory
    escalation_state: EscalationState
    resolution: str
    reason: EscalationReason
    evidence_hash: str
    evidence: Mapping[str, Any]
    created_at: str
    deadline_at: str | None = None
    audit_event_id: str | None = None
