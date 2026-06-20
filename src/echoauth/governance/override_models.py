"""Canonical non-executing override models for Sprint 2K."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class OverrideOutcome(str, Enum):
    APPROVED = "approved"
    DENIED = "denied"
    DEFERRED = "deferred"
    EXPIRED = "expired"


@dataclass(frozen=True)
class OverrideAuthority:
    """One explicitly configured override authority; no discovery is performed."""

    authority_id: str
    authority_reference: str


@dataclass(frozen=True)
class OverrideRequest:
    override_id: str
    request_id: str
    subject_id: str
    declared_by: str
    emergency_type: str
    requested_action: str
    override_authority_id: str
    override_authority_reference: str
    policy_version: str
    expires_at: str
    effective_scope: Mapping[str, Any]
    evidence: Mapping[str, Any]
    audit_references: tuple[str, ...]


@dataclass(frozen=True)
class OverrideReason:
    outcome: OverrideOutcome
    code: str
    authority_valid: bool
    review_outcome: str
    format_version: str


@dataclass(frozen=True)
class OverrideEvidence:
    authorization_decision_id: str
    authorization_evidence_hash: str
    refusal_decision_id: str
    refusal_evidence_hash: str
    escalation_decision_id: str
    escalation_evidence_hash: str
    review_decision_id: str
    review_evidence_hash: str
    override_authority_id: str
    override_authority_reference: str
    declared_by: str
    emergency_type: str
    requested_action: str
    policy_version: str
    review_outcome: str
    expires_at: str
    effective_scope_hash: str
    request_evidence_hash: str
    audit_references: tuple[str, ...]


@dataclass(frozen=True)
class OverrideDecision:
    override_decision_id: str
    override_id: str
    request_id: str
    outcome: OverrideOutcome
    reason: OverrideReason
    evidence: OverrideEvidence
    evidence_hash: str
    effective_scope: Mapping[str, Any]
    review_required: bool
    expires_at: str
    created_at: str
    audit_event_id: str | None = None
