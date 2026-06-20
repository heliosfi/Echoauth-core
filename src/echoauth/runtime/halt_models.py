"""Canonical evidence-only Halt Decision models for Sprint 2O."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class HaltCause(str, Enum):
    MISSING_AUTHORITY = "missing_authority"
    MISSING_EVIDENCE = "missing_evidence"
    INVALID_STATE = "invalid_state"
    FAILED_INVARIANT = "failed_invariant"
    EXPIRED_DEPENDENCY = "expired_dependency"
    INVALID_DEPENDENCY = "invalid_dependency"
    UNRESOLVED_OVERRIDE = "unresolved_override"
    UNSAFE_EXECUTION = "unsafe_execution"


class HaltSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class HaltOutcome(str, Enum):
    REFUSED = "refused"
    HOLD = "hold"
    HALTED = "halted"
    REVOKED = "revoked"
    ESCALATED = "escalated"


@dataclass(frozen=True)
class HaltRequest:
    halt_event_id: str
    request_id: str
    detected_by: str
    failure_type: HaltCause
    severity: HaltSeverity
    state_before: str
    evidence: Mapping[str, Any]
    occurred_at: str
    envelope_id: str | None = None
    execution_token_id: str | None = None


@dataclass(frozen=True)
class HaltDecisionEvidence:
    classifier_version: str
    halt_event_id: str
    failure_type: HaltCause
    severity: HaltSeverity
    state_before: str
    source_evidence_hash: str
    source_references: tuple[str, ...]
    occurred_at: str


@dataclass(frozen=True)
class HaltDecision:
    halt_decision_id: str
    halt_event_id: str
    request_id: str
    runtime_state: HaltOutcome
    reason: str
    recovery_allowed: bool
    required_reviewer: str | None
    evidence: HaltDecisionEvidence
    evidence_hash: str
    decided_at: str
    audit_event_id: str | None = None
