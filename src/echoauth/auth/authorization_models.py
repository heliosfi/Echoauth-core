"""Dependency-neutral Runtime Authorization Gate models."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from echoauth.models import ActorType, AssuranceLevel


class AuthorizationOutcome(str, Enum):
    AUTHORIZED = "authorized"
    DENIED = "denied"
    REVOKED = "revoked"
    EXPIRED = "expired"
    CONFLICT = "conflict"
    INVALID_IDENTITY = "invalid_identity"
    INVALID_AUTHORITY = "invalid_authority"
    INVALID_DELEGATION = "invalid_delegation"
    INVALID_POLICY = "invalid_policy"


@dataclass(frozen=True)
class AuthorizationRequest:
    request_id: str
    requester_id: str
    requester_type: ActorType
    subject_id: str
    action: str
    resource: str
    credential_set: Mapping[str, Any]
    required_assurance: AssuranceLevel
    payload: Mapping[str, Any]
    context: Mapping[str, Any]
    policy_version: str
    correlation_id: str
    idempotency_key: str
    delegation_id: str | None = None
    session_id: str | None = None


@dataclass(frozen=True)
class AuthorizationDecision:
    authorization_decision_id: str
    request_id: str
    outcome: AuthorizationOutcome
    reason: str
    evidence_hash: str
    evidence: Mapping[str, Any]
    decided_at: str
    identity_verdict_id: str | None = None
    authority_resolution_id: str | None = None
    delegation_validation_id: str | None = None
    policy_decision_id: str | None = None
    audit_event_id: str | None = None
