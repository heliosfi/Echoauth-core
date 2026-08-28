import json
import unittest
from dataclasses import FrozenInstanceError, asdict, fields, replace
from pathlib import Path
from types import MappingProxyType

from echoauth.auth.authorization_models import AuthorizationRequest
from echoauth.models import ActorType, AssuranceLevel
from echoauth.sai import (
    HAWK_WAIT_POSTURE,
    SaiBindingError,
    SaiContractConfiguration,
    SaiReason,
    SourceCurrentness,
    form_sai_binding_record,
)
from hawk.transition_envelope import (
    Disposition, ReasonCode, TransitionEnvelopeValidationResult, ValidationState,
)
import hawk.transition_envelope as hawk_module


def freeze(value):
    if isinstance(value, dict):
        return MappingProxyType({key: freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(freeze(item) for item in value)
    return value


def envelope(**changes):
    value = {
        "contractName": "NI AI Transition Envelope",
        "contractVersion": "1.0.0",
        "transitionId": "transition-1",
        "correlationId": "correlation-1",
        "issuerReference": "issuer-1",
        "submittingActor": {"identity": "actor-1", "nativeAuthoritySource": "source-1"},
        "intendedReceiver": {"identity": "echoauth", "nativeAuthoritySource": "source-2"},
        "validityBoundary": {"notBefore": "2026-08-28T10:00:00Z", "notAfter": "2026-08-28T12:00:00Z"},
        "transitionSubject": {
            "currentAuthoritativeState": "state-observe",
            "proposedDestinationState": "state-confirm",
            "governingSource": "governance-1",
            "currentLineageCheckpoint": "lineage-1",
        },
        "authorityBinding": {"exactScope": "scope-1", "revocationStateOrReference": "revocation-1"},
        "governingConditions": {
            "permittedScope": "limits-1",
            "requiredEvidence": [{"reference": "evidence-1", "source": "source-1"}],
        },
        "idempotencyAndOrdering": {"orderingReference": "ordering-1"},
    }
    value.update(changes)
    return freeze(value)


def request(**changes):
    value = dict(
        request_id="request-1", requester_id="requester-1", requester_type=ActorType.HUMAN,
        subject_id="subject-1", action="read", resource="record-1",
        credential_set=freeze({"proof": "credential-reference"}), required_assurance=AssuranceLevel.HIGH,
        payload=freeze({"field": "value"}), context=freeze({"channel": "test"}),
        policy_version="policy-1", correlation_id="correlation-1", idempotency_key="idempotency-1",
    )
    value.update(changes)
    for name in ("credential_set", "payload", "context"):
        if isinstance(value[name], dict):
            value[name] = freeze(value[name])
    return AuthorizationRequest(**value)


def hawk(**changes):
    value = dict(
        validation_id="validation-1", contract_name="NI AI Transition Envelope",
        contract_version="1.0.0", transition_id="transition-1", correlation_id="correlation-1",
        schema_checkpoint="schema-checkpoint", schema_blob="schema-blob",
        passage_consumption_reference="consumption-1", passage_exhaustion_reference="exhaustion-1",
        evaluated_at_utc="2026-08-28T10:10:00Z", validation_state=ValidationState.CONFORMANT,
        disposition=Disposition.PROCEED, reason_codes=(ReasonCode.VALIDATION_PASSED,), evaluated_checks=(),
        evidence_references=("evidence-1",), unresolved_conditions=(), authority_exercised=(),
        authority_excluded=("DISPATCH", "PERMISSION_ENFORCEMENT", "EXECUTION", "ACCEPTANCE", "CONTINUATION"),
        source_provenance=("source-1",), continuation_posture=HAWK_WAIT_POSTURE,
    )
    value.update(changes)
    return TransitionEnvelopeValidationResult(**value)


def configuration(**changes):
    value = dict(
        contract_name="echoauth-sai-binding-record", contract_version="1.0.0",
        upstream_repository="heliosfi/heliosfi-ni-ai-spine",
        upstream_checkpoint="f050dc82f20a0866e477cba0e4e74806454f8940",
        schema_path="schemas/ni-ai-transition-envelope.schema.json", schema_blob="acfe2dc",
        forming_component_id="echoauth_sai_binding_record_former", forming_component_version="1.0.0",
        accepted_state_vocabularies=(("ni-ai.state", "1.0.0", "state-observe"),),
    )
    value.update(changes)
    return SaiContractConfiguration(**value)


def currentness(**changes):
    value = dict(reference="currentness-1", verified=True, revoked=False, superseded=False,
                 replay_state_reference="replay-state-1")
    value.update(changes)
    return SourceCurrentness(**value)


def form(**changes):
    values = dict(
        envelope=envelope(), hawk_result=hawk(), request=request(),
        state_vocabulary_namespace="ni-ai.state", state_vocabulary_version="1.0.0",
        state_value="state-observe", source_currentness=currentness(), configuration=configuration(),
        formed_at="2026-08-28T10:15:00Z", expires_at="2026-08-28T11:00:00Z",
        binding_record_id="binding-1", nonce="nonce-1", audit_event_reference="audit-1",
    )
    values.update(changes)
    return form_sai_binding_record(**values)


class SaiBindingTests(unittest.TestCase):
    def test_schema_is_closed_and_matches_the_immutable_record(self):
        schema_document = freeze(json.loads(Path(
            "schemas/echoauth-sai-binding-record.schema.json").read_text()))
        self.assertTrue(hawk_module._schema_document_valid(schema_document))
        self.assertEqual(set(schema_document["required"]),
                         {field.name for field in fields(type(form()))})
        self.assertTrue(hawk_module._schema_valid(freeze(asdict(form())),
                                                  schema_document, schema_document))

    def test_complete_record_is_immutable_non_authorizing_and_preserves_sources(self):
        record = form()
        self.assertEqual(record.action, "read")
        self.assertEqual(record.resource, "record-1")
        self.assertEqual(record.state_value, "state-observe")
        self.assertNotEqual(record.binding_record_hash, "")
        self.assertFalse(hasattr(record, "credential_set"))
        self.assertFalse(hasattr(record, "payload"))
        with self.assertRaises(FrozenInstanceError):
            record.action = "write"

    def test_action_resource_and_state_have_independent_exact_sources(self):
        record = form(request=request(action="write", resource="record-2"))
        self.assertEqual((record.action, record.resource, record.state_value),
                         ("write", "record-2", "state-observe"))
        with self.assertRaises(SaiBindingError) as caught:
            form(state_value="state-confirm")
        self.assertEqual(caught.exception.reason, SaiReason.STATE_VOCABULARY_UNKNOWN)

    def test_missing_or_unverifiable_producer_fails_closed(self):
        broken = dict(envelope())
        broken.pop("issuerReference")
        for kwargs, reason in [
            ({"envelope": freeze(broken)}, SaiReason.PRODUCER_UNVERIFIABLE),
            ({"source_currentness": currentness(verified=False)}, SaiReason.CURRENTNESS_UNVERIFIABLE),
        ]:
            with self.subTest(reason=reason), self.assertRaises(SaiBindingError) as caught:
                form(**kwargs)
            self.assertEqual(caught.exception.reason, reason)

    def test_mutable_inputs_fail_closed(self):
        with self.assertRaises(SaiBindingError) as caught:
            form(envelope=dict(envelope()))
        self.assertEqual(caught.exception.reason, SaiReason.UPSTREAM_BINDING_INVALID)
        with self.assertRaises(SaiBindingError) as caught:
            form(request=replace(request(), payload={"mutable": True}))
        self.assertEqual(caught.exception.reason, SaiReason.REQUEST_BINDING_INVALID)

    def test_correlation_and_hawk_substitution_fail_closed(self):
        cases = [
            ({"request": request(correlation_id="other")}, SaiReason.CORRELATION_MISMATCH),
            ({"hawk_result": hawk(transition_id="other")}, SaiReason.HAWK_BINDING_INVALID),
            ({"hawk_result": hawk(validation_state=ValidationState.NONCONFORMANT)}, SaiReason.HAWK_NOT_CONFORMANT),
            ({"hawk_result": hawk(disposition=Disposition.WAIT)}, SaiReason.HAWK_DISPOSITION_NOT_PROCEED),
            ({"hawk_result": hawk(continuation_posture="CONTINUE")}, SaiReason.HAWK_BINDING_INVALID),
            ({"hawk_result": hawk(authority_excluded=("EXECUTION",))}, SaiReason.HAWK_AUTHORITY_EXCLUSION_INVALID),
        ]
        for kwargs, reason in cases:
            with self.subTest(reason=reason), self.assertRaises(SaiBindingError) as caught:
                form(**kwargs)
            self.assertEqual(caught.exception.reason, reason)

    def test_unknown_or_translated_state_fails_closed(self):
        with self.assertRaises(SaiBindingError) as caught:
            form(state_value="state-confirm", configuration=configuration(
                accepted_state_vocabularies=(("ni-ai.state", "1.0.0", "state-confirm"),)))
        self.assertEqual(caught.exception.reason, SaiReason.STATE_TRANSLATION_ATTEMPTED)

    def test_revoked_superseded_and_invalid_time_fail_closed(self):
        cases = [
            ({"source_currentness": currentness(revoked=True)}, SaiReason.REVOKED),
            ({"source_currentness": currentness(superseded=True)}, SaiReason.SUPERSEDED),
            ({"expires_at": "2026-08-28T13:00:00Z"}, SaiReason.EXPIRED),
            ({"formed_at": "invalid"}, SaiReason.CONTRACT_INVALID),
        ]
        for kwargs, reason in cases:
            with self.subTest(reason=reason), self.assertRaises(SaiBindingError) as caught:
                form(**kwargs)
            self.assertEqual(caught.exception.reason, reason)

    def test_missing_scope_evidence_and_audit_fail_closed(self):
        cases = []
        no_scope = dict(envelope()); no_scope["authorityBinding"] = {"revocationStateOrReference": "revocation-1"}
        cases.append(({"envelope": freeze(no_scope)}, SaiReason.SCOPE_INVALID))
        no_evidence = dict(envelope()); no_evidence["governingConditions"] = {
            "permittedScope": "limits-1", "requiredEvidence": []}
        cases.append(({"envelope": freeze(no_evidence)}, SaiReason.EVIDENCE_INVALID))
        no_limits = dict(envelope()); no_limits["governingConditions"] = {
            "requiredEvidence": [{"reference": "evidence-1", "source": "source-1"}]}
        cases.append(({"envelope": freeze(no_limits)}, SaiReason.LIMITS_INVALID))
        for kwargs, reason in cases:
            with self.subTest(reason=reason), self.assertRaises(SaiBindingError) as caught:
                form(**kwargs)
            self.assertEqual(caught.exception.reason, reason)
