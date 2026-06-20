"""Canonical execution eligibility models for Sprint 2M."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from echoauth.runtime import RuntimeState


class ExecutionOutcome(str, Enum):
    ELIGIBLE = "eligible"
    BLOCKED = "blocked"
    INVALID_STATE = "invalid_state"
    MISSING_AUTHORITY = "missing_authority"
    MISSING_EVIDENCE = "missing_evidence"
    EXPIRED = "expired"
    HALTED = "halted"


@dataclass(frozen=True)
class ExecutionConstraint:
    constraint_id: str
    required_state: RuntimeState
    expires_at: str
    execution_enabled: bool = True
    require_refusal_evidence: bool = False
    require_escalation_evidence: bool = False
    require_review_evidence: bool = False
    require_override_evidence: bool = False


@dataclass(frozen=True)
class ExecutionRequest:
    execution_request_id: str
    request_id: str
    runtime_transition_decision_id: str
    actor_id: str
    action: str
    resource: str
    authority_evidence: Mapping[str, Any]
    refusal_evidence: Mapping[str, Any]
    escalation_evidence: Mapping[str, Any]
    review_evidence: Mapping[str, Any]
    override_evidence: Mapping[str, Any]
    evidence: Mapping[str, Any]
    audit_references: tuple[str, ...]
    requested_at: str
    constraint: ExecutionConstraint


@dataclass(frozen=True)
class ExecutionEvidence:
    control_version: str
    request_id: str
    actor_id: str
    action: str
    resource: str
    requested_at: str
    runtime_transition_decision_id: str
    runtime_transition_evidence_hash: str
    runtime_state: RuntimeState
    constraint_hash: str
    authority_evidence_hash: str | None
    refusal_evidence_hash: str | None
    escalation_evidence_hash: str | None
    review_evidence_hash: str | None
    override_evidence_hash: str | None
    request_evidence_hash: str
    audit_references: tuple[str, ...]


@dataclass(frozen=True)
class ExecutionDecision:
    execution_decision_id: str
    execution_request_id: str
    request_id: str
    outcome: ExecutionOutcome
    eligible: bool
    reason: str
    evidence: ExecutionEvidence
    evidence_hash: str
    decided_at: str
    audit_event_id: str | None = None
