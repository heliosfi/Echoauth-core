import ast
import inspect
import unittest
from dataclasses import FrozenInstanceError
from types import MappingProxyType

import hawk.transition_envelope as module
from hawk.transition_envelope import (
    Disposition,
    ReasonCode,
    ResolvedFactState,
    TransitionEnvelopeValidationResult,
    ValidationState,
    validate_transition_envelope,
)


def freeze(value):
    if isinstance(value, dict):
        return MappingProxyType({key: freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(freeze(item) for item in value)
    return value


def schema():
    return freeze({
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "NI AI Transition Envelope",
        "type": "object",
        "additionalProperties": False,
        "required": ["contractName", "contractVersion", "transitionId", "correlationId",
                     "validityBoundary", "semanticCorrespondence"],
        "properties": {
            "contractName": {"const": "NI AI Transition Envelope"},
            "contractVersion": {"type": "string"},
            "transitionId": {"type": "string", "format": "uuid"},
            "correlationId": {"type": "string", "format": "uuid"},
            "validityBoundary": {
                "type": "object", "additionalProperties": False,
                "required": ["notBefore", "notAfter"],
                "properties": {
                    "notBefore": {"type": "string", "format": "date-time", "pattern": "Z$"},
                    "notAfter": {"type": "string", "format": "date-time", "pattern": "Z$"},
                },
            },
            "semanticCorrespondence": {
                "type": "object", "additionalProperties": False,
                "required": ["ambiguityState"],
                "properties": {"ambiguityState": {"enum": ["NONE", "DETECTED", "UNRESOLVED", "RESOLVED"]}},
            },
        },
        "$defs": {},
    })


def envelope(**overrides):
    values = {
        "contractName": "NI AI Transition Envelope",
        "contractVersion": "1.0.0",
        "transitionId": "11111111-1111-4111-8111-111111111111",
        "correlationId": "22222222-2222-4222-8222-222222222222",
        "validityBoundary": {"notBefore": "2026-08-08T00:00:00Z", "notAfter": "2026-08-09T00:00:00Z"},
        "semanticCorrespondence": {"ambiguityState": "NONE"},
    }
    values.update(overrides)
    return freeze(values)


def context(**overrides):
    facts = {name: "CONFIRMED" for name in module._FACT_NAMES}
    facts["authority_revocation"] = "REFUTED"
    values = {
        "schema_document": schema(),
        "schema_repository": "heliosfi/heliosfi-ni-ai-spine",
        "schema_path": "schemas/ni-ai-transition-envelope.schema.json",
        "schema_checkpoint": "6fe29594b4b5c7e4ceea1907c87cc7049e9a0e80",
        "schema_blob": "acfe2dc5c4bd722163b123545fbf41a09fa2509d",
        "trusted_evaluation_time_utc": "2026-08-08T12:00:00Z",
        "validation_id": "validation-1",
        "passage_consumption_reference": "consumption-1",
        "passage_exhaustion_reference": "exhaustion-1",
        "resolved_facts": facts,
    }
    values.update(overrides)
    return freeze(values)


def with_fact(name, value):
    values = {key: "CONFIRMED" for key in module._FACT_NAMES}
    values["authority_revocation"] = "REFUTED"
    values[name] = value
    return context(resolved_facts=values)


class HawkTransitionEnvelopeTests(unittest.TestCase):
    def test_closed_contract_and_public_api(self):
        self.assertEqual(len(ResolvedFactState), 6)
        self.assertEqual(len(ValidationState), 3)
        self.assertEqual(len(Disposition), 5)
        self.assertEqual(len(ReasonCode), 28)
        self.assertEqual(len(module._FACT_NAMES), 21)
        self.assertEqual(len(module._CHECK_NAMES), 19)
        self.assertEqual(module._EXCLUDED, ("DISPATCH", "PERMISSION_ENFORCEMENT", "EXECUTION", "ACCEPTANCE", "CONTINUATION"))

    def test_complete_conformance_is_the_only_proceed_path(self):
        result = validate_transition_envelope(envelope(), context())
        self.assertEqual((result.validation_state, result.disposition, result.reason_codes),
                         (ValidationState.CONFORMANT, Disposition.PROCEED, (ReasonCode.VALIDATION_PASSED,)))
        self.assertEqual(len(result.evaluated_checks), 19)
        self.assertEqual(result.evaluated_checks[-1].check_name, "SUCCESS")
        self.assertEqual(result.authority_exercised, ())
        self.assertEqual(result.authority_excluded, module._EXCLUDED)
        self.assertEqual(result.continuation_posture, "WAIT_FOR_SEPARATE_AUTHORITY")

    def test_results_are_equal_distinct_frozen_and_preserve_opaque_references(self):
        first = validate_transition_envelope(envelope(), context())
        second = validate_transition_envelope(envelope(), context())
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        self.assertEqual(first.passage_consumption_reference, "consumption-1")
        self.assertEqual(first.passage_exhaustion_reference, "exhaustion-1")
        with self.assertRaises(FrozenInstanceError):
            first.validation_id = "changed"
        self.assertEqual(len(TransitionEnvelopeValidationResult.__dataclass_fields__), 20)

    def test_mutable_cyclic_and_unsupported_inputs_stop_at_public_boundary(self):
        for bad_envelope, bad_context in [
            ({}, context()),
            (envelope(), {}),
            (object(), context()),
        ]:
            result = validate_transition_envelope(bad_envelope, bad_context)
            self.assertEqual((result.disposition, result.reason_codes, len(result.evaluated_checks)),
                             (Disposition.STOP, (ReasonCode.PUBLIC_INPUT_INVALID,), 1))
        cyclic = {}
        cyclic["self"] = cyclic
        result = validate_transition_envelope(freeze({}), cyclic)
        self.assertEqual(result.reason_codes, (ReasonCode.PUBLIC_INPUT_INVALID,))

    def test_context_binding_integrity_document_and_structure_precedence(self):
        incomplete = dict({key: value for key, value in context().items() if key != "validation_id"})
        result = validate_transition_envelope(envelope(), freeze(incomplete))
        self.assertEqual(result.reason_codes, (ReasonCode.VALIDATION_CONTEXT_INVALID,))
        result = validate_transition_envelope(envelope(), context(schema_blob="wrong"))
        self.assertEqual(result.reason_codes, (ReasonCode.SCHEMA_BINDING_INVALID,))
        result = validate_transition_envelope(envelope(), with_fact("schema_integrity", "REFUTED"))
        self.assertEqual(result.reason_codes, (ReasonCode.SCHEMA_INTEGRITY_INVALID,))
        result = validate_transition_envelope(envelope(), context(schema_document=freeze({"$defs": {}})))
        self.assertEqual(result.reason_codes, (ReasonCode.SCHEMA_DOCUMENT_INVALID,))
        malformed = dict(schema())
        malformed["type"] = "unsupported"
        result = validate_transition_envelope(
            envelope(), context(schema_document=freeze(malformed)))
        self.assertEqual(
            (result.disposition, result.reason_codes, len(result.evaluated_checks)),
            (Disposition.STOP, (ReasonCode.SCHEMA_DOCUMENT_INVALID,), 4),
        )
        malformed = dict(schema())
        malformed["properties"] = {"contractName": {"pattern": "["}}
        result = validate_transition_envelope(
            envelope(), context(schema_document=freeze(malformed)))
        self.assertEqual(result.reason_codes, (ReasonCode.SCHEMA_DOCUMENT_INVALID,))
        result = validate_transition_envelope(envelope(extra="unknown"), context())
        self.assertEqual((result.disposition, result.reason_codes),
                         (Disposition.RETURN, (ReasonCode.ENVELOPE_SCHEMA_NONCONFORMANT,)))

    def test_json_semantic_unique_items_and_uuid_boundaries(self):
        item_schema = freeze({
            "type": "array",
            "uniqueItems": True,
            "items": {"type": "object"},
        })
        first = freeze({"reference": "evidence-1", "nested": {"a": 1, "b": 2}})
        reordered = freeze({"nested": {"b": 2, "a": 1}, "reference": "evidence-1"})
        different = freeze({"nested": {"b": 3, "a": 1}, "reference": "evidence-1"})
        self.assertFalse(module._schema_valid((first, reordered), item_schema, item_schema))
        self.assertTrue(module._schema_valid((first, different), item_schema, item_schema))

        array_schema = freeze({"type": "array", "uniqueItems": True})
        self.assertTrue(module._schema_valid(((1, 2), (2, 1)), array_schema, array_schema))
        self.assertTrue(module._schema_valid((True, 1), array_schema, array_schema))
        self.assertFalse(module._schema_valid((1, 1.0), array_schema, array_schema))

        uuid_schema = freeze({"type": "string", "format": "uuid"})
        valid = "ABCDEF12-3456-4789-ABCD-EF1234567890"
        self.assertTrue(module._schema_valid(valid, uuid_schema, uuid_schema))
        for invalid in (
            "abcdef1234564789abcdef1234567890",
            "{abcdef12-3456-4789-abcd-ef1234567890}",
            "abcdef12-3456-4789-abcd-ef123456789",
            "abcdef12-3456-4789-abcd-ef12345678900",
            "not-a-uuid",
        ):
            with self.subTest(uuid=invalid):
                self.assertFalse(module._schema_valid(invalid, uuid_schema, uuid_schema))

    def test_contract_participant_and_lineage_mappings(self):
        result = validate_transition_envelope(envelope(contractVersion="2.0.0"), context())
        self.assertEqual(result.reason_codes, (ReasonCode.CONTRACT_IDENTITY_INVALID,))
        cases = [
            ("issuer_identity", "REFUTED", Disposition.STOP, ReasonCode.PARTICIPANT_IDENTITY_INVALID),
            ("receiver_identity", "UNVERIFIABLE", Disposition.WAIT, ReasonCode.PARTICIPANT_IDENTITY_INVALID),
            ("lineage_verifiability", "REFUTED", Disposition.STOP, ReasonCode.LINEAGE_INVALID),
            ("lineage_verifiability", "CONTRADICTORY", Disposition.ESCALATE, ReasonCode.LINEAGE_INVALID),
            ("lineage_verifiability", "STALE", Disposition.WAIT, ReasonCode.LINEAGE_INVALID),
        ]
        for name, value, disposition, reason in cases:
            with self.subTest(name=name, value=value):
                result = validate_transition_envelope(envelope(), with_fact(name, value))
                self.assertEqual((result.disposition, result.reason_codes), (disposition, (reason,)))

    def test_authority_first_match_precedence(self):
        cases = [
            ("authority_revocation", "CONFIRMED", Disposition.STOP, ReasonCode.AUTHORITY_REVOKED, 7),
            ("authority_consistency", "CONTRADICTORY", Disposition.ESCALATE, ReasonCode.AUTHORITY_CONTRADICTORY, 8),
            ("authority_scope", "REFUTED", Disposition.STOP, ReasonCode.AUTHORITY_INVALID, 9),
            ("authority_currentness", "STALE", Disposition.WAIT, ReasonCode.AUTHORITY_STALE, 10),
            ("authority_evidence_verifiability", "UNAVAILABLE", Disposition.WAIT, ReasonCode.AUTHORITY_UNVERIFIABLE, 10),
        ]
        for name, value, disposition, reason, step in cases:
            with self.subTest(name=name, value=value):
                result = validate_transition_envelope(envelope(), with_fact(name, value))
                self.assertEqual((result.disposition, result.reason_codes, len(result.evaluated_checks)),
                                 (disposition, (reason,), step))

        facts = {name: "CONFIRMED" for name in module._FACT_NAMES}
        facts["authority_revocation"] = "REFUTED"
        facts["governing_source_verifiability"] = "CONTRADICTORY"
        facts["authority_currentness"] = "STALE"
        result = validate_transition_envelope(
            envelope(), context(resolved_facts=facts))
        self.assertEqual(
            (result.disposition, result.reason_codes, len(result.evaluated_checks),
             result.unresolved_conditions),
            (Disposition.ESCALATE, (ReasonCode.AUTHORITY_CONTRADICTORY,), 8,
             ("governing_source_verifiability",)),
        )

    def test_passed_checks_preserve_safe_evidence_references(self):
        result = validate_transition_envelope(envelope(), context())
        self.assertEqual(result.evaluated_checks[0].evidence_references, ())
        self.assertEqual(result.evaluated_checks[1].evidence_references, ())
        bound = (
            "heliosfi/heliosfi-ni-ai-spine",
            "schemas/ni-ai-transition-envelope.schema.json",
            "6fe29594b4b5c7e4ceea1907c87cc7049e9a0e80",
            "acfe2dc5c4bd722163b123545fbf41a09fa2509d",
        )
        self.assertEqual(result.evaluated_checks[2].evidence_references, bound)
        self.assertEqual(result.evaluated_checks[3].evidence_references, bound)
        for check in result.evaluated_checks[4:]:
            self.assertEqual(check.evidence_references, bound)

    def test_semantic_policy_evidence_time_and_consequence_mappings(self):
        result = validate_transition_envelope(envelope(semanticCorrespondence={"ambiguityState": "DETECTED"}), context())
        self.assertEqual(result.reason_codes, (ReasonCode.SEMANTIC_AMBIGUITY_DETECTED,))
        result = validate_transition_envelope(envelope(semanticCorrespondence={"ambiguityState": "UNRESOLVED"}), context())
        self.assertEqual(result.reason_codes, (ReasonCode.SEMANTIC_AMBIGUITY_UNRESOLVED,))
        for name, reason in [
            ("policy_reference_verifiability", ReasonCode.POLICY_UNVERIFIABLE),
            ("evidence_reference_verifiability", ReasonCode.EVIDENCE_UNVERIFIABLE),
            ("trusted_time_verifiability", ReasonCode.TIME_INVALID),
            ("consequence_reference_verifiability", ReasonCode.CONSEQUENCE_INVALID),
        ]:
            result = validate_transition_envelope(envelope(), with_fact(name, "UNVERIFIABLE"))
            self.assertEqual((result.disposition, result.reason_codes), (Disposition.WAIT, (reason,)))
        result = validate_transition_envelope(envelope(), context(trusted_evaluation_time_utc="2026-08-10T00:00:00Z"))
        self.assertEqual((result.disposition, result.reason_codes), (Disposition.RETURN, (ReasonCode.TIME_INVALID,)))

    def test_confidentiality_integrity_ordering_lifecycle_and_return_mappings(self):
        cases = [
            ("confidentiality_verifiability", "REFUTED", Disposition.STOP, ReasonCode.CONFIDENTIALITY_INVALID),
            ("integrity_proof_verifiability", "UNAVAILABLE", Disposition.WAIT, ReasonCode.INTEGRITY_INVALID),
            ("idempotency_replay_retry_ordering", "REFUTED", Disposition.RETURN, ReasonCode.IDEMPOTENCY_ORDERING_INVALID),
            ("lifecycle_separation", "REFUTED", Disposition.RETURN, ReasonCode.LIFECYCLE_INVALID),
            ("return_path_verifiability", "CONTRADICTORY", Disposition.ESCALATE, ReasonCode.RETURN_PATH_INVALID),
        ]
        for name, value, disposition, reason in cases:
            with self.subTest(name=name, value=value):
                result = validate_transition_envelope(envelope(), with_fact(name, value))
                self.assertEqual((result.disposition, result.reason_codes), (disposition, (reason,)))

    def test_each_nonconfirmed_fact_cannot_proceed(self):
        for name in module._FACT_NAMES:
            value = "CONFIRMED" if name == "authority_revocation" else "UNVERIFIABLE"
            result = validate_transition_envelope(envelope(), with_fact(name, value))
            with self.subTest(name=name):
                self.assertIsNot(result.disposition, Disposition.PROCEED)

    def test_no_input_mutation_or_hidden_capability_imports(self):
        supplied_envelope = envelope()
        supplied_context = context()
        before_envelope = repr(supplied_envelope)
        before_context = repr(supplied_context)
        validate_transition_envelope(supplied_envelope, supplied_context)
        self.assertEqual(repr(supplied_envelope), before_envelope)
        self.assertEqual(repr(supplied_context), before_context)
        tree = ast.parse(inspect.getsource(module))
        imports = {alias.name.split(".")[0] for node in ast.walk(tree)
                   if isinstance(node, ast.Import) for alias in node.names}
        from_imports = {node.module.split(".")[0] for node in ast.walk(tree)
                        if isinstance(node, ast.ImportFrom) and node.module}
        allowed = {"__future__", "collections", "dataclasses", "datetime", "enum", "re", "types", "typing", "uuid"}
        self.assertTrue((imports | from_imports) <= allowed)


if __name__ == "__main__":
    unittest.main()
