"""Immutable, non-authorizing SAI correspondence models."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


NON_AUTHORIZING_STATUS = "VALID_FOR_INDEPENDENT_ECHOAUTH_AUTHORIZATION_EVALUATION_ONLY"
ACCEPTED_OUTCOME = "ACCEPTED_FOR_INDEPENDENT_AUTHORIZATION_EVALUATION"
WAIT_POSTURE = "WAIT_FOR_SEPARATE_AUTHORIZATION"
HAWK_WAIT_POSTURE = "WAIT_FOR_SEPARATE_AUTHORITY"


class SaiReason(str, Enum):
    ACCEPTED = "ACCEPTED"
    CONTRACT_INVALID = "CONTRACT_INVALID"
    PRODUCER_UNVERIFIABLE = "PRODUCER_UNVERIFIABLE"
    UPSTREAM_BINDING_INVALID = "UPSTREAM_BINDING_INVALID"
    HAWK_BINDING_INVALID = "HAWK_BINDING_INVALID"
    HAWK_NOT_CONFORMANT = "HAWK_NOT_CONFORMANT"
    HAWK_DISPOSITION_NOT_PROCEED = "HAWK_DISPOSITION_NOT_PROCEED"
    HAWK_AUTHORITY_EXCLUSION_INVALID = "HAWK_AUTHORITY_EXCLUSION_INVALID"
    REQUEST_BINDING_INVALID = "REQUEST_BINDING_INVALID"
    CORRELATION_MISMATCH = "CORRELATION_MISMATCH"
    ACTION_MISMATCH = "ACTION_MISMATCH"
    RESOURCE_MISMATCH = "RESOURCE_MISMATCH"
    REQUEST_HASH_MISMATCH = "REQUEST_HASH_MISMATCH"
    PAYLOAD_HASH_MISMATCH = "PAYLOAD_HASH_MISMATCH"
    CONTEXT_HASH_MISMATCH = "CONTEXT_HASH_MISMATCH"
    POLICY_VERSION_MISMATCH = "POLICY_VERSION_MISMATCH"
    STATE_VOCABULARY_UNKNOWN = "STATE_VOCABULARY_UNKNOWN"
    STATE_TRANSLATION_ATTEMPTED = "STATE_TRANSLATION_ATTEMPTED"
    SCOPE_INVALID = "SCOPE_INVALID"
    LIMITS_INVALID = "LIMITS_INVALID"
    NOT_YET_EFFECTIVE = "NOT_YET_EFFECTIVE"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    SUPERSEDED = "SUPERSEDED"
    REPLAYED = "REPLAYED"
    CURRENTNESS_UNVERIFIABLE = "CURRENTNESS_UNVERIFIABLE"
    EVIDENCE_INVALID = "EVIDENCE_INVALID"
    AUDIT_INVALID = "AUDIT_INVALID"
    UNKNOWN_FIELD = "UNKNOWN_FIELD"
    INTERNAL_VALIDATION_ERROR = "INTERNAL_VALIDATION_ERROR"


class SaiBindingError(ValueError):
    def __init__(self, reason: SaiReason) -> None:
        super().__init__(reason.value)
        self.reason = reason


@dataclass(frozen=True)
class SourceCurrentness:
    reference: str
    verified: bool
    revoked: bool
    superseded: bool
    replay_state_reference: str


@dataclass(frozen=True)
class SaiContractConfiguration:
    contract_name: str
    contract_version: str
    upstream_repository: str
    upstream_checkpoint: str
    schema_path: str
    schema_blob: str
    forming_component_id: str
    forming_component_version: str
    accepted_state_vocabularies: tuple[tuple[str, str, str], ...]


@dataclass(frozen=True)
class SaiBindingRecord:
    contract_name: str
    contract_version: str
    non_authorizing_status: str
    upstream_repository: str
    upstream_checkpoint: str
    schema_path: str
    schema_blob: str
    transition_id: str
    correlation_id: str
    issuer_reference: str
    submitting_actor_reference: str
    intended_receiver_reference: str
    current_state_reference: str
    destination_state_reference: str
    state_vocabulary_namespace: str
    state_vocabulary_version: str
    state_value: str
    governing_source_reference: str
    lineage_checkpoint_reference: str
    upstream_scope_reference: str
    upstream_limits_reference: str
    valid_from: str
    valid_until: str
    revocation_reference: str
    supersession_reference: str
    upstream_evidence_references: tuple[str, ...]
    upstream_audit_references: tuple[str, ...]
    hawk_validation_id: str
    hawk_transition_id: str
    hawk_correlation_id: str
    hawk_schema_checkpoint: str
    hawk_schema_blob: str
    hawk_validation_state: str
    hawk_disposition: str
    hawk_continuation_posture: str
    hawk_authority_excluded: tuple[str, ...]
    hawk_evidence_references: tuple[str, ...]
    hawk_result_hash: str
    request_id: str
    request_correlation_id: str
    action: str
    resource: str
    request_hash: str
    payload_hash: str
    context_hash: str
    policy_version: str
    idempotency_key: str
    binding_record_id: str
    forming_component_id: str
    forming_component_version: str
    formed_at: str
    expires_at: str
    nonce: str
    source_currentness_reference: str
    replay_state_reference: str
    audit_event_reference: str
    binding_record_hash: str


@dataclass(frozen=True)
class SaiIntakeEvidence:
    evaluated_at: str
    source_currentness_reference: str
    replay_state_reference: str
    currentness_verified: bool
    revoked: bool
    superseded: bool
    replayed_nonces: tuple[str, ...]
    audit_available: bool


@dataclass(frozen=True)
class SaiIntakeResult:
    accepted: bool
    outcome: str | None
    reason: SaiReason
    continuation_posture: str
