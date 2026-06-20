"""Canonical structured refusal models for Sprint 2H."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class RefusalCategory(str, Enum):
    INVALID_IDENTITY = "invalid_identity"
    INVALID_AUTHORITY = "invalid_authority"
    INVALID_DELEGATION = "invalid_delegation"
    POLICY_DENIED = "policy_denied"
    REVOKED = "revoked"
    EXPIRED = "expired"
    CONFLICT = "conflict"
    UNAVAILABLE_DEPENDENCY = "unavailable_dependency"
    MALFORMED_REQUEST = "malformed_request"


class RefusalFailureSource(str, Enum):
    IDENTITY = "identity"
    AUTHORITY = "authority"
    DELEGATION = "delegation"
    POLICY = "policy"
    INVARIANT = "invariant"
    RUNTIME = "runtime"
    AUDIT = "audit"


class RefusalSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class RefusalRequest:
    refusal_request_id: str
    request_id: str
    failure_source: RefusalFailureSource
    failure_code: str
    severity: RefusalSeverity
    recoverable: bool
    evidence: Mapping[str, Any]
    authorization_decision_id: str
    authorization_outcome: str


@dataclass(frozen=True)
class RefusalReason:
    category: RefusalCategory
    failure_source: RefusalFailureSource
    failure_code: str
    severity: RefusalSeverity
    recoverable: bool
    recovery_path: str
    mapping_version: str


@dataclass(frozen=True)
class RefusalDecision:
    refusal_decision_id: str
    refusal_request_id: str
    request_id: str
    category: RefusalCategory
    reason: RefusalReason
    evidence_hash: str
    evidence: Mapping[str, Any]
    created_at: str
    audit_event_id: str | None = None
