"""Contract-backed, evidence-only Recovery Eligibility models for Sprint 2P."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class RecoverySourceState(str, Enum):
    EXECUTION_BLOCKED = "execution_blocked"
    HALTED = "halted"


class RecoveryFailureCode(str, Enum):
    MISSING_EVIDENCE = "missing_evidence"
    DEPENDENCY_UNAVAILABLE = "dependency_unavailable"
    AUDIT_PATH_DEGRADED = "audit_path_degraded"
    COORDINATION_INTERRUPTED = "coordination_interrupted"
    CRITICAL_INVARIANT_FAILURE = "critical_invariant_failure"
    INVALID_STATE = "invalid_state"
    UNSAFE_EXECUTION = "unsafe_execution"
    EVIDENCE_INTEGRITY_FAILURE = "evidence_integrity_failure"
    AUDIT_CHAIN_FAILURE = "audit_chain_failure"


class RecoveryPath(str, Enum):
    REVALIDATE_REQUEST = "revalidate_request"
    CREATE_NEW_REQUEST = "create_new_request"


class RecoveryOutcome(str, Enum):
    REVALIDATION_REQUIRED = "revalidation_required"
    REJECTED = "rejected"
    NEW_REQUEST_REQUIRED = "new_request_required"


class RecoveryProtocolStatus(str, Enum):
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"


@dataclass(frozen=True)
class RecoveryReviewProtocol:
    protocol_id: str
    protocol_version: str
    protocol_status: RecoveryProtocolStatus
    request_id: str
    halt_decision_id: str
    halt_decision_evidence_hash: str
    review_decision_id: str
    review_decision_evidence_hash: str
    reviewer_id: str
    reviewer_authority_reference: str
    reviewer_authority_resolution_id: str
    reviewer_authority_evidence_hash: str
    permitted_recovery_path: RecoveryPath
    scope: Mapping[str, Any]
    expires_at: str
    evidence_hash: str


@dataclass(frozen=True)
class RecoveryEligibilityRequest:
    recovery_id: str
    request_id: str
    source_state: RecoverySourceState
    failure_code: RecoveryFailureCode
    requested_recovery_path: RecoveryPath
    recovery_actor_id: str
    recovery_authority_reference: str
    authority_resolution_id: str
    authority_evidence_hash: str
    halt_decision_id: str
    halt_decision_evidence_hash: str
    original_failure_evidence_hash: str
    original_failure_audit_event_id: str
    changed_evidence_reference: str
    changed_evidence_hash: str
    recovery_policy_version: str
    guard_evidence: Mapping[str, Any]
    invalidated_token_refs: tuple[str, ...]
    requested_at: str
    recovery_review_protocol: RecoveryReviewProtocol | None = None


@dataclass(frozen=True)
class RecoveryEligibilityResult:
    recovery_decision_id: str
    recovery_id: str
    request_id: str
    source_state: RecoverySourceState
    outcome: RecoveryOutcome
    reason: str
    required_validations: tuple[str, ...]
    evidence_hash: str
    decided_at: str
    audit_event_id: str

