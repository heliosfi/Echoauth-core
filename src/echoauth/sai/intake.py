"""Fail-closed, inert SAI intake validation."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone

from echoauth.auth.authorization_models import AuthorizationRequest
from echoauth.canonical import canonical_sha256
from echoauth.sai.binding import _deeply_immutable, _plain, _record_document, _request_document
from echoauth.sai.models import (
    ACCEPTED_OUTCOME,
    HAWK_WAIT_POSTURE,
    NON_AUTHORIZING_STATUS,
    WAIT_POSTURE,
    SaiBindingRecord,
    SaiContractConfiguration,
    SaiIntakeEvidence,
    SaiIntakeResult,
    SaiReason,
)


def _utc(value: str) -> datetime | None:
    if not isinstance(value, str) or not value.endswith("Z"):
        return None
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except (TypeError, ValueError):
        return None
    return parsed if parsed is not None and parsed.tzinfo == timezone.utc else None


def _reject(reason: SaiReason) -> SaiIntakeResult:
    return SaiIntakeResult(False, None, reason, WAIT_POSTURE)


def validate_sai_intake(
    record: SaiBindingRecord,
    request: AuthorizationRequest,
    evidence: SaiIntakeEvidence,
    configuration: SaiContractConfiguration,
) -> SaiIntakeResult:
    """Validate correspondence only; never invoke the authorization gate."""

    try:
        if not all(_deeply_immutable(item) for item in (
            request.credential_set, request.payload, request.context,
        )):
            return _reject(SaiReason.REQUEST_BINDING_INVALID)
        if record.contract_name != configuration.contract_name or record.contract_version != configuration.contract_version:
            return _reject(SaiReason.CONTRACT_INVALID)
        if record.non_authorizing_status != NON_AUTHORIZING_STATUS:
            return _reject(SaiReason.CONTRACT_INVALID)
        if (record.upstream_repository, record.upstream_checkpoint, record.schema_path, record.schema_blob) != (
            configuration.upstream_repository, configuration.upstream_checkpoint,
            configuration.schema_path, configuration.schema_blob,
        ):
            return _reject(SaiReason.UPSTREAM_BINDING_INVALID)
        expected_hash = canonical_sha256(_record_document(replace(record, binding_record_hash=""), include_hash=False))
        if record.binding_record_hash != expected_hash:
            return _reject(SaiReason.UPSTREAM_BINDING_INVALID)
        if record.hawk_transition_id != record.transition_id or record.hawk_correlation_id != record.correlation_id:
            return _reject(SaiReason.HAWK_BINDING_INVALID)
        if record.hawk_validation_state != "CONFORMANT":
            return _reject(SaiReason.HAWK_NOT_CONFORMANT)
        if record.hawk_disposition != "PROCEED":
            return _reject(SaiReason.HAWK_DISPOSITION_NOT_PROCEED)
        if record.hawk_continuation_posture != HAWK_WAIT_POSTURE:
            return _reject(SaiReason.HAWK_BINDING_INVALID)
        required = {"DISPATCH", "PERMISSION_ENFORCEMENT", "EXECUTION", "ACCEPTANCE", "CONTINUATION"}
        if not required.issubset(record.hawk_authority_excluded):
            return _reject(SaiReason.HAWK_AUTHORITY_EXCLUSION_INVALID)
        if request.request_id != record.request_id:
            return _reject(SaiReason.REQUEST_BINDING_INVALID)
        if request.correlation_id != record.request_correlation_id or record.correlation_id != record.request_correlation_id:
            return _reject(SaiReason.CORRELATION_MISMATCH)
        if request.action != record.action:
            return _reject(SaiReason.ACTION_MISMATCH)
        if request.resource != record.resource:
            return _reject(SaiReason.RESOURCE_MISMATCH)
        if canonical_sha256(_plain(request.payload)) != record.payload_hash:
            return _reject(SaiReason.PAYLOAD_HASH_MISMATCH)
        if canonical_sha256(_plain(request.context)) != record.context_hash:
            return _reject(SaiReason.CONTEXT_HASH_MISMATCH)
        if request.policy_version != record.policy_version:
            return _reject(SaiReason.POLICY_VERSION_MISMATCH)
        if request.idempotency_key != record.idempotency_key:
            return _reject(SaiReason.REQUEST_BINDING_INVALID)
        if canonical_sha256(_plain(_request_document(request))) != record.request_hash:
            return _reject(SaiReason.REQUEST_HASH_MISMATCH)
        if (record.state_vocabulary_namespace, record.state_vocabulary_version, record.state_value) not in configuration.accepted_state_vocabularies:
            return _reject(SaiReason.STATE_VOCABULARY_UNKNOWN)
        if not evidence.currentness_verified:
            return _reject(SaiReason.CURRENTNESS_UNVERIFIABLE)
        if evidence.revoked:
            return _reject(SaiReason.REVOKED)
        if evidence.superseded:
            return _reject(SaiReason.SUPERSEDED)
        if record.nonce in evidence.replayed_nonces:
            return _reject(SaiReason.REPLAYED)
        now = _utc(evidence.evaluated_at)
        start = _utc(record.valid_from)
        end = _utc(record.expires_at)
        if now is None or start is None or end is None:
            return _reject(SaiReason.CURRENTNESS_UNVERIFIABLE)
        if now < start:
            return _reject(SaiReason.NOT_YET_EFFECTIVE)
        if now >= end:
            return _reject(SaiReason.EXPIRED)
        if not evidence.audit_available or not record.audit_event_reference or not record.upstream_audit_references:
            return _reject(SaiReason.AUDIT_INVALID)
        if not record.upstream_evidence_references or not record.hawk_evidence_references:
            return _reject(SaiReason.EVIDENCE_INVALID)
        return SaiIntakeResult(True, ACCEPTED_OUTCOME, SaiReason.ACCEPTED, WAIT_POSTURE)
    except Exception:
        return _reject(SaiReason.INTERNAL_VALIDATION_ERROR)
