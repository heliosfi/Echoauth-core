"""Canonical declarative policy models for Sprint 2F."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class PolicyType(str, Enum):
    AUTHORITY = "authority"
    DELEGATION = "delegation"
    RUNTIME = "runtime"
    SECURITY = "security"
    NOTIFICATION = "notification"
    EMERGENCY = "emergency"


class PolicyEffect(str, Enum):
    AUTHORIZE = "authorize"
    DENY = "deny"


class PolicyStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    RETIRED = "retired"
    REVOKED = "revoked"
    EXPIRED = "expired"


class PolicyEvaluationOutcome(str, Enum):
    AUTHORIZED = "authorized"
    DENIED = "denied"
    CONFLICT = "conflict"
    EXPIRED = "expired"
    REVOKED = "revoked"
    INVALID_POLICY = "invalid_policy"


class PolicyScopeMatch(str, Enum):
    MATCH = "match"
    MISMATCH = "mismatch"
    AMBIGUOUS = "ambiguous"


@dataclass(frozen=True)
class PolicyRule:
    rule_id: str
    policy_id: str
    policy_version: str
    policy_type: PolicyType
    effect: PolicyEffect
    actions: tuple[str, ...]
    resources: tuple[str, ...]
    scope: Mapping[str, Any]
    priority: int
    reason: str
    status: PolicyStatus
    created_by: str
    effective_at: str
    expires_at: str | None
    policy_hash: str


@dataclass(frozen=True)
class StoredPolicyRule:
    policy_rule: PolicyRule
    reason: str


@dataclass(frozen=True)
class PolicyHistoryEntry:
    sequence: int
    operation: str
    policy_rule: PolicyRule
    actor_id: str
    reason: str
    occurred_at: str
    audit_event_id: str
    audit_event_hash: str
    previous_audit_hash: str | None


@dataclass(frozen=True)
class PolicyEvaluationRequest:
    policy_evaluation_id: str
    request_id: str
    subject_id: str
    requester_id: str
    authority_verdict_id: str
    action: str
    resource: str
    context: Mapping[str, Any]
    policy_version: str
    delegation_id: str | None = None


@dataclass(frozen=True)
class PolicyEvaluationResult:
    policy_decision_id: str
    policy_evaluation_id: str
    outcome: PolicyEvaluationOutcome
    reason: str
    matched_rules: tuple[str, ...]
    failed_rules: tuple[str, ...]
    evidence_hash: str
    evaluated_at: str
    audit_event_id: str | None = None
