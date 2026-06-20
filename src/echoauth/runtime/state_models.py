"""Canonical validation-only runtime state models for Sprint 2L."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class RuntimeState(str, Enum):
    REQUESTED = "requested"
    AUTHORIZED = "authorized"
    REFUSED = "refused"
    ESCALATED = "escalated"
    UNDER_REVIEW = "under_review"
    OVERRIDDEN = "overridden"
    READY = "ready"
    EXECUTION_BLOCKED = "execution_blocked"
    EXPIRED = "expired"
    HALTED = "halted"


class RuntimeTransition(str, Enum):
    AUTHORIZE = "authorize"
    REFUSE = "refuse"
    ESCALATE = "escalate"
    BEGIN_REVIEW = "begin_review"
    OVERRIDE = "override"
    MARK_READY = "mark_ready"
    BLOCK_EXECUTION = "block_execution"
    RELEASE_BLOCK = "release_block"
    EXPIRE = "expire"
    HALT = "halt"


@dataclass(frozen=True)
class RuntimeTransitionRequest:
    transition_request_id: str
    request_id: str
    current_state: RuntimeState
    transition: RuntimeTransition
    requested_state: RuntimeState
    actor_id: str
    reason: str
    evidence: Mapping[str, Any]
    occurred_at: str


@dataclass(frozen=True)
class RuntimeStateEvidence:
    graph_version: str
    request_id: str
    current_state: RuntimeState
    transition: RuntimeTransition
    requested_state: RuntimeState
    validated_state: RuntimeState
    actor_id: str
    reason: str
    source_evidence_hash: str
    occurred_at: str


@dataclass(frozen=True)
class RuntimeTransitionDecision:
    transition_decision_id: str
    transition_request_id: str
    request_id: str
    allowed: bool
    current_state: RuntimeState
    next_state: RuntimeState
    transition: RuntimeTransition
    reason: str
    evidence: RuntimeStateEvidence
    evidence_hash: str
    validated_at: str
    audit_event_id: str | None = None
