"""Canonical EchoAuth contract models.

Specifications: specs/*.md
Contracts: schemas/*.json, api/openapi.yaml, contracts/protobuf/echoauth.proto

Canonical JSON object fields remain domain-specific because the specifications
define deterministic serialization and hashing requirements but not nested
business schemas.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Sequence

CanonicalJsonObject = Mapping[str, Any]
OpenObject = CanonicalJsonObject


class RuntimeState(str, Enum):
    """Runtime states from specs/runtime-state-machine.md."""

    NEW = "new"
    PROPOSED = "proposed"
    UNDER_GOVERNANCE = "under_governance"
    RESOLVING_AUTHORITY = "resolving_authority"
    VALIDATING_DELEGATION = "validating_delegation"
    EVALUATING_POLICY = "evaluating_policy"
    VALIDATING_INVARIANTS = "validating_invariants"
    CREATING_ENVELOPE = "creating_envelope"
    AUTHORIZED = "authorized"
    TOKEN_ISSUED = "token_issued"
    EXECUTING = "executing"
    COMPLETED = "completed"
    REFUSED = "refused"
    HOLD = "hold"
    HALTED = "halted"
    REVOKED = "revoked"
    EXPIRED = "expired"
    ESCALATED = "escalated"


class ActorType(str, Enum):
    """Actor types from specs/identity-model.md."""

    HUMAN = "human"
    DELEGATE = "delegate"
    INSTITUTION = "institution"
    SERVICE = "service"
    EXECUTOR = "executor"
    AUDITOR = "auditor"


class AssuranceLevel(str, Enum):
    """Assurance levels from specs/identity-resolution.md."""

    LOW = "low"
    STANDARD = "standard"
    HIGH = "high"
    CRITICAL = "critical"


class AuditAppendState(str, Enum):
    """Append outcomes from specs/audit-log-spec.md."""

    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CONFLICT = "conflict"
    DEGRADED = "degraded"


class AuditStorageState(str, Enum):
    """Audit service outcomes from specs/audit-record.md."""

    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DEGRADED = "degraded"


@dataclass(frozen=True)
class EchoAuthRequest:
    """Input contract from specs/echoauth-spec.md."""

    request_id: str
    requester_id: str
    subject_id: str
    action: str
    resource: str
    payload: CanonicalJsonObject
    context: CanonicalJsonObject
    correlation_id: str
    idempotency_key: str
    session_id: str | None = None


@dataclass(frozen=True)
class EchoAuthResult:
    """Output contract from specs/echoauth-spec.md."""

    request_state: RuntimeState
    reason: str
    identity_verdict_id: str | None = None
    authority_verdict_id: str | None = None
    policy_decision_id: str | None = None
    invariant_result_id: str | None = None
    envelope_id: str | None = None
    execution_token_id: str | None = None
    audit_chain_id: str | None = None


@dataclass(frozen=True)
class IdentityResolutionRequest:
    """Input contract from specs/identity-resolution.md."""

    identity_request_id: str
    actor_id: str
    actor_type: ActorType
    credential_set: CanonicalJsonObject
    context: CanonicalJsonObject
    required_assurance: AssuranceLevel
    subject_id: str | None = None
    session_id: str | None = None


@dataclass(frozen=True)
class IdentityVerdict:
    """Output contract from specs/identity-resolution.md."""

    identity_verdict_id: str
    state: str
    resolved_actor_id: str
    assurance_level: AssuranceLevel
    evidence_hash: str
    expires_at: str
    reason: str


@dataclass(frozen=True)
class AuthorityResolutionRequest:
    """Input contract from specs/authority-resolution.md."""

    request_id: str
    subject_id: str
    requester_id: str
    action: str
    resource: str
    context: CanonicalJsonObject
    identity_verdict_id: str
    authority_records: Sequence[CanonicalJsonObject]
    policy_version: str
    delegation_records: Sequence[CanonicalJsonObject] = field(default_factory=tuple)
    revocation_records: Sequence[CanonicalJsonObject] = field(default_factory=tuple)


@dataclass(frozen=True)
class AuthorityVerdict:
    """Output contract from specs/authority-resolution.md."""

    authority_verdict_id: str
    request_id: str
    state: str
    reason: str
    evidence_hash: str
    expires_at: str
    authority_source_id: str | None = None
    authority_type: str | None = None
    scope: CanonicalJsonObject | None = None


@dataclass(frozen=True)
class RuntimeEnvelope:
    """Input contract from specs/runtime-envelope.md."""

    envelope_id: str
    request_id: str
    subject_id: str
    requester_id: str
    authority_verdict_id: str
    action: str
    resource: str
    payload_hash: str
    policy_version: str
    invariant_version: str
    channel_id: str
    nonce: str
    expires_at: str
    audit_sink_id: str
    delegation_id: str | None = None


@dataclass(frozen=True)
class ExecutionToken:
    """Input contract from specs/execution-token.md."""

    execution_token_id: str
    envelope_id: str
    request_id: str
    authority_verdict_id: str
    action: str
    resource: str
    payload_hash: str
    nonce: str
    issued_at: str
    expires_at: str
    issuer_id: str


@dataclass(frozen=True)
class AuditRecord:
    """Input contract from specs/audit-record.md."""

    event_type: str
    actor_id: str
    reason: str
    details: CanonicalJsonObject
    occurred_at: str
    request_id: str | None = None
    envelope_id: str | None = None
    authority_verdict_id: str | None = None
    execution_token_id: str | None = None
    state_before: str | None = None
    state_after: str | None = None


@dataclass(frozen=True)
class AuditRecordResult:
    """Audit service output from specs/audit-record.md."""

    audit_event_id: str
    event_hash: str
    storage_state: AuditStorageState
    previous_hash: str | None = None


@dataclass(frozen=True)
class AuditAppendResult:
    """Append result from specs/audit-log-spec.md.

    ``previous_hash`` is retained because the audit-record contract exposes it
    alongside the stored event hash.
    """

    append_state: AuditAppendState
    reason: str
    audit_event_id: str | None = None
    event_hash: str | None = None
    previous_hash: str | None = None
    chain_position: int | None = None
