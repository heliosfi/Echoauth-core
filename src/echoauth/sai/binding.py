"""Pure formation of an inert SAI-to-EchoAuth correspondence record."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Any

from echoauth.auth.authorization_models import AuthorizationRequest
from echoauth.canonical import CanonicalDataError, canonical_sha256
from echoauth.sai.models import (
    HAWK_WAIT_POSTURE,
    NON_AUTHORIZING_STATUS,
    SaiBindingError,
    SaiBindingRecord,
    SaiContractConfiguration,
    SaiReason,
    SourceCurrentness,
)
from hawk.transition_envelope import Disposition, TransitionEnvelopeValidationResult, ValidationState


_REQUIRED_EXCLUSIONS = frozenset(
    {"DISPATCH", "PERMISSION_ENFORCEMENT", "EXECUTION", "ACCEPTANCE", "CONTINUATION"}
)
_CONTRACT_NAME = "echoauth-sai-binding-record"
_CONTRACT_VERSION = "1.0.0"
_UPSTREAM_REPOSITORY = "heliosfi/heliosfi-ni-ai-spine"
_SCHEMA_PATH = "schemas/ni-ai-transition-envelope.schema.json"
_FORMER_ID = "echoauth_sai_binding_record_former"


def _deeply_immutable(value: Any) -> bool:
    if value is None or isinstance(value, (str, int, float, bool)):
        return True
    if isinstance(value, MappingProxyType):
        return all(isinstance(key, str) and _deeply_immutable(item)
                   for key, item in value.items())
    if isinstance(value, tuple):
        return all(_deeply_immutable(item) for item in value)
    return False


def _utc(value: str) -> datetime | None:
    if not isinstance(value, str) or not value.endswith("Z"):
        return None
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except (TypeError, ValueError):
        return None
    return parsed if parsed is not None and parsed.tzinfo == timezone.utc else None


def _required(mapping: Mapping[str, Any], name: str, reason: SaiReason) -> Any:
    value = mapping.get(name)
    if value is None or value == "":
        raise SaiBindingError(reason)
    return value


def _identity(mapping: Mapping[str, Any], name: str) -> str:
    value = _required(mapping, name, SaiReason.PRODUCER_UNVERIFIABLE)
    if not isinstance(value, Mapping):
        raise SaiBindingError(SaiReason.PRODUCER_UNVERIFIABLE)
    identity = value.get("identity")
    if not isinstance(identity, str) or not identity:
        raise SaiBindingError(SaiReason.PRODUCER_UNVERIFIABLE)
    return identity


def _request_document(request: AuthorizationRequest) -> Mapping[str, Any]:
    return {
        "request_id": request.request_id,
        "requester_id": request.requester_id,
        "requester_type": request.requester_type.value,
        "subject_id": request.subject_id,
        "action": request.action,
        "resource": request.resource,
        "credential_set": request.credential_set,
        "required_assurance": request.required_assurance.value,
        "payload": request.payload,
        "context": request.context,
        "policy_version": request.policy_version,
        "correlation_id": request.correlation_id,
        "idempotency_key": request.idempotency_key,
        "delegation_id": request.delegation_id,
        "session_id": request.session_id,
    }


def _plain(value: Any) -> Any:
    """Detach immutable Mapping/tuple inputs into canonical JSON containers."""
    if isinstance(value, Mapping):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_plain(item) for item in value]
    return value


def _hawk_document(result: TransitionEnvelopeValidationResult) -> Mapping[str, Any]:
    value = asdict(result)
    value["validation_state"] = result.validation_state.value
    value["disposition"] = result.disposition.value
    value["reason_codes"] = tuple(item.value for item in result.reason_codes)
    value["evaluated_checks"] = tuple(
        {
            **asdict(item),
            "reason_codes": tuple(reason.value for reason in item.reason_codes),
        }
        for item in result.evaluated_checks
    )
    return value


def _record_document(record: SaiBindingRecord, *, include_hash: bool = True) -> Mapping[str, Any]:
    value = asdict(record)
    if not include_hash:
        value.pop("binding_record_hash", None)
    return value


def form_sai_binding_record(
    envelope: Mapping[str, Any],
    hawk_result: TransitionEnvelopeValidationResult,
    request: AuthorizationRequest,
    *,
    state_vocabulary_namespace: str,
    state_vocabulary_version: str,
    state_value: str,
    source_currentness: SourceCurrentness,
    configuration: SaiContractConfiguration,
    formed_at: str,
    expires_at: str,
    binding_record_id: str,
    nonce: str,
    audit_event_reference: str,
) -> SaiBindingRecord:
    """Bind exact evidence without interpreting it or invoking authorization."""

    if not isinstance(envelope, Mapping) or not _deeply_immutable(envelope):
        raise SaiBindingError(SaiReason.UPSTREAM_BINDING_INVALID)
    if not all(_deeply_immutable(item) for item in (
        request.credential_set, request.payload, request.context,
    )):
        raise SaiBindingError(SaiReason.REQUEST_BINDING_INVALID)
    if not all((binding_record_id, nonce, audit_event_reference)):
        raise SaiBindingError(SaiReason.CONTRACT_INVALID)
    if (
        configuration.contract_name != _CONTRACT_NAME
        or configuration.contract_version != _CONTRACT_VERSION
        or configuration.upstream_repository != _UPSTREAM_REPOSITORY
        or configuration.schema_path != _SCHEMA_PATH
        or configuration.forming_component_id != _FORMER_ID
        or not configuration.upstream_checkpoint
        or not configuration.schema_blob
        or not configuration.forming_component_version
    ):
        raise SaiBindingError(SaiReason.CONTRACT_INVALID)
    if not source_currentness.reference or not source_currentness.replay_state_reference:
        raise SaiBindingError(SaiReason.CURRENTNESS_UNVERIFIABLE)
    if not source_currentness.verified:
        raise SaiBindingError(SaiReason.CURRENTNESS_UNVERIFIABLE)
    if source_currentness.revoked:
        raise SaiBindingError(SaiReason.REVOKED)
    if source_currentness.superseded:
        raise SaiBindingError(SaiReason.SUPERSEDED)
    formed = _utc(formed_at)
    expiry = _utc(expires_at)
    if formed is None or expiry is None or formed >= expiry:
        raise SaiBindingError(SaiReason.CONTRACT_INVALID)

    transition_id = _required(envelope, "transitionId", SaiReason.UPSTREAM_BINDING_INVALID)
    correlation_id = _required(envelope, "correlationId", SaiReason.UPSTREAM_BINDING_INVALID)
    if request.correlation_id != correlation_id:
        raise SaiBindingError(SaiReason.CORRELATION_MISMATCH)
    if hawk_result.transition_id != transition_id or hawk_result.correlation_id != correlation_id:
        raise SaiBindingError(SaiReason.HAWK_BINDING_INVALID)
    if hawk_result.validation_state is not ValidationState.CONFORMANT:
        raise SaiBindingError(SaiReason.HAWK_NOT_CONFORMANT)
    if hawk_result.disposition is not Disposition.PROCEED:
        raise SaiBindingError(SaiReason.HAWK_DISPOSITION_NOT_PROCEED)
    # The current validator contract emits WAIT_FOR_SEPARATE_AUTHORITY.  The
    # later connection contract's longer phrase is the caller posture, not a
    # value emitted by Hawk itself.
    if hawk_result.continuation_posture != HAWK_WAIT_POSTURE:
        raise SaiBindingError(SaiReason.HAWK_BINDING_INVALID)
    if not _REQUIRED_EXCLUSIONS.issubset(hawk_result.authority_excluded):
        raise SaiBindingError(SaiReason.HAWK_AUTHORITY_EXCLUSION_INVALID)
    vocabulary = (state_vocabulary_namespace, state_vocabulary_version, state_value)
    if vocabulary not in configuration.accepted_state_vocabularies:
        raise SaiBindingError(SaiReason.STATE_VOCABULARY_UNKNOWN)

    subject = _required(envelope, "transitionSubject", SaiReason.UPSTREAM_BINDING_INVALID)
    authority = _required(envelope, "authorityBinding", SaiReason.UPSTREAM_BINDING_INVALID)
    governing = _required(envelope, "governingConditions", SaiReason.UPSTREAM_BINDING_INVALID)
    validity = _required(envelope, "validityBoundary", SaiReason.UPSTREAM_BINDING_INVALID)
    ordering = _required(envelope, "idempotencyAndOrdering", SaiReason.UPSTREAM_BINDING_INVALID)
    if not all(isinstance(item, Mapping) for item in (subject, authority, governing, validity, ordering)):
        raise SaiBindingError(SaiReason.UPSTREAM_BINDING_INVALID)
    if state_value != subject.get("currentAuthoritativeState"):
        raise SaiBindingError(SaiReason.STATE_TRANSLATION_ATTEMPTED)
    valid_from = _required(validity, "notBefore", SaiReason.UPSTREAM_BINDING_INVALID)
    valid_until = _required(validity, "notAfter", SaiReason.UPSTREAM_BINDING_INVALID)
    source_start = _utc(valid_from)
    source_end = _utc(valid_until)
    if source_start is None or source_end is None or source_start >= source_end or expiry > source_end:
        raise SaiBindingError(SaiReason.EXPIRED)

    required_evidence = governing.get("requiredEvidence")
    if not isinstance(required_evidence, (tuple, list)) or not required_evidence:
        raise SaiBindingError(SaiReason.EVIDENCE_INVALID)
    evidence_refs = tuple(
        item.get("reference", "") for item in required_evidence if isinstance(item, Mapping)
    )
    if len(evidence_refs) != len(required_evidence) or not all(evidence_refs):
        raise SaiBindingError(SaiReason.EVIDENCE_INVALID)
    audit_refs = tuple(
        value for value in (
            ordering.get("orderingReference"),
            hawk_result.passage_consumption_reference,
            hawk_result.passage_exhaustion_reference,
        ) if isinstance(value, str) and value
    )
    if not audit_refs:
        raise SaiBindingError(SaiReason.AUDIT_INVALID)

    try:
        request_hash = canonical_sha256(_plain(_request_document(request)))
        payload_hash = canonical_sha256(_plain(request.payload))
        context_hash = canonical_sha256(_plain(request.context))
        hawk_hash = canonical_sha256(_plain(_hawk_document(hawk_result)))
    except (CanonicalDataError, TypeError, ValueError):
        raise SaiBindingError(SaiReason.REQUEST_BINDING_INVALID) from None

    values = dict(
        contract_name=configuration.contract_name,
        contract_version=configuration.contract_version,
        non_authorizing_status=NON_AUTHORIZING_STATUS,
        upstream_repository=configuration.upstream_repository,
        upstream_checkpoint=configuration.upstream_checkpoint,
        schema_path=configuration.schema_path,
        schema_blob=configuration.schema_blob,
        transition_id=transition_id,
        correlation_id=correlation_id,
        issuer_reference=_required(envelope, "issuerReference", SaiReason.PRODUCER_UNVERIFIABLE),
        submitting_actor_reference=_identity(envelope, "submittingActor"),
        intended_receiver_reference=_identity(envelope, "intendedReceiver"),
        current_state_reference=_required(subject, "currentAuthoritativeState", SaiReason.UPSTREAM_BINDING_INVALID),
        destination_state_reference=_required(subject, "proposedDestinationState", SaiReason.UPSTREAM_BINDING_INVALID),
        state_vocabulary_namespace=state_vocabulary_namespace,
        state_vocabulary_version=state_vocabulary_version,
        state_value=state_value,
        governing_source_reference=_required(subject, "governingSource", SaiReason.UPSTREAM_BINDING_INVALID),
        lineage_checkpoint_reference=_required(subject, "currentLineageCheckpoint", SaiReason.UPSTREAM_BINDING_INVALID),
        upstream_scope_reference=_required(authority, "exactScope", SaiReason.SCOPE_INVALID),
        upstream_limits_reference=_required(governing, "permittedScope", SaiReason.LIMITS_INVALID),
        valid_from=valid_from,
        valid_until=valid_until,
        revocation_reference=_required(authority, "revocationStateOrReference", SaiReason.CURRENTNESS_UNVERIFIABLE),
        supersession_reference=source_currentness.reference,
        upstream_evidence_references=evidence_refs,
        upstream_audit_references=audit_refs,
        hawk_validation_id=hawk_result.validation_id,
        hawk_transition_id=hawk_result.transition_id,
        hawk_correlation_id=hawk_result.correlation_id,
        hawk_schema_checkpoint=hawk_result.schema_checkpoint,
        hawk_schema_blob=hawk_result.schema_blob,
        hawk_validation_state=hawk_result.validation_state.value,
        hawk_disposition=hawk_result.disposition.value,
        hawk_continuation_posture=hawk_result.continuation_posture,
        hawk_authority_excluded=hawk_result.authority_excluded,
        hawk_evidence_references=hawk_result.evidence_references,
        hawk_result_hash=hawk_hash,
        request_id=request.request_id,
        request_correlation_id=request.correlation_id,
        action=request.action,
        resource=request.resource,
        request_hash=request_hash,
        payload_hash=payload_hash,
        context_hash=context_hash,
        policy_version=request.policy_version,
        idempotency_key=request.idempotency_key,
        binding_record_id=binding_record_id,
        forming_component_id=configuration.forming_component_id,
        forming_component_version=configuration.forming_component_version,
        formed_at=formed_at,
        expires_at=expires_at,
        nonce=nonce,
        source_currentness_reference=source_currentness.reference,
        replay_state_reference=source_currentness.replay_state_reference,
        audit_event_reference=audit_event_reference,
        binding_record_hash="",
    )
    provisional = SaiBindingRecord(**values)
    values["binding_record_hash"] = canonical_sha256(_record_document(provisional, include_hash=False))
    return SaiBindingRecord(**values)
