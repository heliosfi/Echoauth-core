import ast
import json
import unittest
from dataclasses import FrozenInstanceError, asdict
from pathlib import Path

from sniperbot.crypto.deferral_decision import (
    AssetClass,
    AuthorityEvidence,
    Decision,
    EmittableReasonCode,
    GenericAssetClassContext,
    CryptoLaneConfirmation,
    CryptoRequest,
    Outcome,
    ReasonCode,
    RequiredAction,
    create_request,
    evaluate,
)


def make(**overrides):
    values = dict(
        crypto_reference="crypto-ref",
        crypto_evidence_present=True,
        crypto_evidence_current=True,
        crypto_evidence_sufficient=True,
        crypto_evidence_contradictory=False,
        crypto_deferral=False,
        crypto_no_action=False,
        crypto_restricted=False,
        crypto_excluded=False,
        correlation_reference="correlation-ref",
        crypto_lane_confirmation=CryptoLaneConfirmation.CONFIRMED,
    )
    values.update(overrides)
    return create_request(**values)


def generic(**overrides):
    values = dict(
        asset_class=AssetClass.CRYPTO,
        validity="VALID",
        current=True,
        contradictory=False,
        in_scope=True,
        context_reference="generic-ref",
    )
    values.update(overrides)
    return GenericAssetClassContext(**values)


def authority(**overrides):
    values = dict(
        validity="VALID",
        current=True,
        revoked=False,
        contradictory=False,
        in_scope=True,
        evidence_reference="authority-ref",
    )
    values.update(overrides)
    return AuthorityEvidence(**values)


def mapping(request):
    decision = evaluate(request)
    return decision.outcome, decision.reason_code, decision.required_action


class CryptoDeferralNoActionTests(unittest.TestCase):
    def test_vocabularies_match_schema_and_decision_restrictions(self):
        schema = json.loads(
            Path("schemas/sniperbot-crypto-deferral-no-action-decision.schema.json").read_text(
                encoding="utf-8"
            )
        )
        definitions = schema["$defs"]
        self.assertEqual({item.value for item in Outcome}, set(definitions["Outcome"]["enum"]))
        self.assertEqual({item.value for item in ReasonCode}, set(definitions["ReasonCode"]["enum"]))
        self.assertEqual({item.value for item in EmittableReasonCode}, set(definitions["ReasonCode"]["enum"]))
        self.assertEqual({item.value for item in RequiredAction}, set(definitions["RequiredAction"]["enum"]))
        self.assertEqual({item.value for item in CryptoLaneConfirmation}, set(definitions["CryptoLaneConfirmation"]["enum"]))
        self.assertEqual({item.value for item in AssetClass}, set(definitions["AssetClass"]["enum"]))
        self.assertEqual({"VALID", "INVALID", "AMBIGUOUS"}, set(definitions["Validity"]["enum"]))
        self.assertEqual((len(Outcome), len(ReasonCode), len(RequiredAction), len(CryptoLaneConfirmation), len(AssetClass)), (2, 22, 5, 3, 3))
        self.assertEqual(len(definitions["EmittableAction"]["enum"]), 3)
        self.assertNotIn("UNKNOWN", {item.name for item in ReasonCode})
        for action in (RequiredAction.FOUNDER_AUTHORITY_REQUIRED, RequiredAction.RESET_REQUIRED):
            with self.assertRaises(ValueError):
                Decision("o", Outcome.NO_ACTION, ReasonCode.NO_ACTION_REQUIRED, action, "c")

    def test_all_twenty_first_match_branches(self):
        cases = [
            (dict(crypto_evidence_contradictory=True), (Outcome.NO_ACTION, ReasonCode.CRYPTO_EVIDENCE_CONTRADICTORY, RequiredAction.HUMAN_REVIEW)),
            (dict(crypto_deferral=True, crypto_no_action=True), (Outcome.NO_ACTION, ReasonCode.CRYPTO_DEFERRAL_NO_ACTION_CONFLICT, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(crypto_evidence_present=False, crypto_evidence_current=True, crypto_evidence_sufficient=False), (Outcome.NO_ACTION, ReasonCode.UNDEFINED_INPUT_COMBINATION, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(crypto_lane_confirmation=None), (Outcome.NO_ACTION, ReasonCode.CRYPTO_LANE_CONFIRMATION_MISSING, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(crypto_lane_confirmation=CryptoLaneConfirmation.CONTRADICTORY), (Outcome.NO_ACTION, ReasonCode.CRYPTO_LANE_CONTRADICTORY, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(crypto_lane_confirmation=CryptoLaneConfirmation.NOT_CONFIRMED), (Outcome.NO_ACTION, ReasonCode.CRYPTO_LANE_NOT_CONFIRMED, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(generic_asset_class_context=generic(contradictory=True)), (Outcome.NO_ACTION, ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(generic_asset_class_context=generic(validity="AMBIGUOUS")), (Outcome.NO_ACTION, ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(generic_asset_class_context=generic(asset_class=AssetClass.STOCK)), (Outcome.NO_ACTION, ReasonCode.GENERIC_ASSET_CLASS_NOT_CRYPTO, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(generic_asset_class_context=generic(current=False)), (Outcome.NO_ACTION, ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_STALE, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(generic_asset_class_context=generic(in_scope=False)), (Outcome.NO_ACTION, ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(crypto_excluded=True), (Outcome.NO_ACTION, ReasonCode.CRYPTO_EXCLUDED, RequiredAction.NONE)),
            (dict(crypto_restricted=True), (Outcome.NO_ACTION, ReasonCode.CRYPTO_RESTRICTED, RequiredAction.NONE)),
            (dict(authority_evidence=authority(validity="INVALID")), (Outcome.NO_ACTION, ReasonCode.AUTHORITY_EVIDENCE_INVALID, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(crypto_evidence_present=False, crypto_evidence_current=False, crypto_evidence_sufficient=False), (Outcome.DEFER, ReasonCode.CRYPTO_EVIDENCE_MISSING, RequiredAction.HUMAN_REVIEW)),
            (dict(crypto_evidence_current=False, crypto_evidence_sufficient=False), (Outcome.DEFER, ReasonCode.CRYPTO_EVIDENCE_STALE, RequiredAction.HUMAN_REVIEW)),
            (dict(crypto_evidence_sufficient=False), (Outcome.DEFER, ReasonCode.CRYPTO_EVIDENCE_INSUFFICIENT, RequiredAction.HUMAN_REVIEW)),
            (dict(crypto_deferral=True), (Outcome.DEFER, ReasonCode.CRYPTO_DEFERRAL_EXTERNALLY_REQUIRED, RequiredAction.HUMAN_REVIEW)),
            (dict(crypto_no_action=True), (Outcome.NO_ACTION, ReasonCode.NO_ACTION_REQUIRED, RequiredAction.NONE)),
            (dict(), (Outcome.NO_ACTION, ReasonCode.NO_ACTION_REQUIRED, RequiredAction.NONE)),
        ]
        for values, expected in cases:
            with self.subTest(values=values):
                self.assertEqual(mapping(make(**values)), expected)

    def test_three_undefined_predicates_are_valid_typed_requests(self):
        cases = (
            dict(crypto_evidence_present=False, crypto_evidence_current=True, crypto_evidence_sufficient=False),
            dict(crypto_evidence_present=False, crypto_evidence_current=False, crypto_evidence_sufficient=True),
            dict(crypto_evidence_present=True, crypto_evidence_current=False, crypto_evidence_sufficient=True),
        )
        for values in cases:
            request = make(**values)
            self.assertIsInstance(request, CryptoRequest)
            self.assertEqual(evaluate(request).reason_code, ReasonCode.UNDEFINED_INPUT_COMBINATION)

    def test_contradiction_and_conflict_global_precedence(self):
        lower = dict(
            crypto_evidence_present=False,
            crypto_evidence_current=True,
            crypto_evidence_sufficient=False,
            crypto_deferral=True,
            crypto_no_action=True,
            crypto_lane_confirmation=CryptoLaneConfirmation.CONTRADICTORY,
            generic_asset_class_context=generic(contradictory=True),
            crypto_excluded=True,
            crypto_restricted=True,
            authority_evidence=authority(contradictory=True),
        )
        self.assertEqual(evaluate(make(crypto_evidence_contradictory=True, **lower)).reason_code, ReasonCode.CRYPTO_EVIDENCE_CONTRADICTORY)
        lower["crypto_evidence_present"] = True
        lower["crypto_evidence_current"] = True
        lower["crypto_evidence_sufficient"] = True
        self.assertEqual(evaluate(make(**lower)).reason_code, ReasonCode.CRYPTO_DEFERRAL_NO_ACTION_CONFLICT)

    def test_undefined_and_lane_failures_over_lower_categories(self):
        lower = [
            dict(generic_asset_class_context=generic(contradictory=True)),
            dict(crypto_excluded=True),
            dict(crypto_restricted=True),
            dict(authority_evidence=authority(validity="INVALID")),
            dict(crypto_deferral=True),
            dict(crypto_no_action=True),
        ]
        for overrides in lower:
            values = dict(crypto_evidence_present=False, crypto_evidence_current=True, crypto_evidence_sufficient=False)
            values.update(overrides)
            self.assertEqual(evaluate(make(**values)).reason_code, ReasonCode.UNDEFINED_INPUT_COMBINATION)
        for lane, expected in (
            (None, ReasonCode.CRYPTO_LANE_CONFIRMATION_MISSING),
            (CryptoLaneConfirmation.CONTRADICTORY, ReasonCode.CRYPTO_LANE_CONTRADICTORY),
            (CryptoLaneConfirmation.NOT_CONFIRMED, ReasonCode.CRYPTO_LANE_NOT_CONFIRMED),
        ):
            for overrides in lower:
                self.assertEqual(evaluate(make(crypto_lane_confirmation=lane, **overrides)).reason_code, expected)

    def test_generic_subprecedence_and_lower_category_precedence(self):
        contexts = [
            (generic(contradictory=True, validity="AMBIGUOUS", asset_class=AssetClass.STOCK, current=False, in_scope=False), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY),
            (generic(validity="AMBIGUOUS", asset_class=AssetClass.STOCK, current=False, in_scope=False), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID),
            (generic(validity="INVALID", asset_class=AssetClass.STOCK, current=False, in_scope=False), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID),
            (generic(asset_class=AssetClass.STOCK, current=False, in_scope=False), ReasonCode.GENERIC_ASSET_CLASS_NOT_CRYPTO),
            (generic(asset_class=AssetClass.OPTIONS), ReasonCode.GENERIC_ASSET_CLASS_NOT_CRYPTO),
            (generic(current=False, in_scope=False), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_STALE),
            (generic(in_scope=False), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE),
        ]
        for context, expected in contexts:
            for lower in (
                dict(crypto_excluded=True),
                dict(crypto_restricted=True),
                dict(authority_evidence=authority(validity="INVALID")),
                dict(crypto_evidence_present=False, crypto_evidence_current=False, crypto_evidence_sufficient=False),
                dict(crypto_evidence_current=False, crypto_evidence_sufficient=False),
                dict(crypto_evidence_sufficient=False),
                dict(crypto_deferral=True),
                dict(crypto_no_action=True),
            ):
                self.assertEqual(evaluate(make(generic_asset_class_context=context, **lower)).reason_code, expected)
        self.assertEqual(
            mapping(make(generic_asset_class_context=generic(), crypto_excluded=True)),
            (Outcome.NO_ACTION, ReasonCode.CRYPTO_EXCLUDED, RequiredAction.NONE),
        )
        self.assertEqual(evaluate(make(generic_asset_class_context=None)).reason_code, ReasonCode.NO_ACTION_REQUIRED)
        self.assertEqual(evaluate(make(generic_asset_class_context=generic())).reason_code, ReasonCode.NO_ACTION_REQUIRED)

    def test_exclusion_restriction_and_authority_precedence(self):
        authority_failure = authority(validity="INVALID")
        lower_categories = (
            dict(crypto_restricted=True),
            dict(authority_evidence=authority_failure),
            dict(crypto_evidence_present=False, crypto_evidence_current=False, crypto_evidence_sufficient=False),
            dict(crypto_evidence_current=False, crypto_evidence_sufficient=False),
            dict(crypto_evidence_sufficient=False),
            dict(crypto_deferral=True),
            dict(crypto_no_action=True),
        )
        for lower in lower_categories:
            self.assertEqual(evaluate(make(crypto_excluded=True, **lower)).reason_code, ReasonCode.CRYPTO_EXCLUDED)
        for lower in lower_categories[1:]:
            self.assertEqual(evaluate(make(crypto_restricted=True, **lower)).reason_code, ReasonCode.CRYPTO_RESTRICTED)
        for lower in lower_categories[2:] + (dict(),):
            self.assertEqual(evaluate(make(authority_evidence=authority_failure, **lower)).reason_code, ReasonCode.AUTHORITY_EVIDENCE_INVALID)

    def test_authority_subprecedence_absent_and_valid(self):
        cases = [
            (authority(contradictory=True, validity="AMBIGUOUS", revoked=True, current=False, in_scope=False), ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            (authority(validity="AMBIGUOUS", revoked=True, current=False, in_scope=False), ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            (authority(validity="INVALID", revoked=True, current=False, in_scope=False), ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            (authority(revoked=True, current=False, in_scope=False), ReasonCode.AUTHORITY_EVIDENCE_REVOKED),
            (authority(current=False, in_scope=False), ReasonCode.AUTHORITY_EVIDENCE_STALE),
            (authority(in_scope=False), ReasonCode.AUTHORITY_EVIDENCE_OUT_OF_SCOPE),
        ]
        for evidence, expected in cases:
            self.assertEqual(evaluate(make(authority_evidence=evidence)).reason_code, expected)
        self.assertEqual(evaluate(make(authority_evidence=None)).reason_code, ReasonCode.NO_ACTION_REQUIRED)
        self.assertEqual(evaluate(make(authority_evidence=authority())).reason_code, ReasonCode.NO_ACTION_REQUIRED)

    def test_evidence_ordering_deferral_and_no_action(self):
        evidence_cases = [
            (dict(crypto_evidence_present=False, crypto_evidence_current=False, crypto_evidence_sufficient=False), ReasonCode.CRYPTO_EVIDENCE_MISSING),
            (dict(crypto_evidence_present=False, crypto_evidence_current=False, crypto_evidence_sufficient=False), ReasonCode.CRYPTO_EVIDENCE_MISSING),
            (dict(crypto_evidence_current=False, crypto_evidence_sufficient=False), ReasonCode.CRYPTO_EVIDENCE_STALE),
        ]
        for values, expected in evidence_cases:
            self.assertEqual(evaluate(make(**values)).reason_code, expected)
        self.assertEqual(evaluate(make(crypto_deferral=True, crypto_no_action=True)).reason_code, ReasonCode.CRYPTO_DEFERRAL_NO_ACTION_CONFLICT)
        self.assertEqual(evaluate(make(crypto_deferral=True)).reason_code, ReasonCode.CRYPTO_DEFERRAL_EXTERNALLY_REQUIRED)
        explicit = mapping(make(crypto_no_action=True))
        fallback = mapping(make())
        self.assertEqual(explicit, fallback)

    def test_strict_boolean_empty_reference_and_nested_object_rejection(self):
        boolean_fields = (
            "crypto_evidence_present", "crypto_evidence_current", "crypto_evidence_sufficient",
            "crypto_evidence_contradictory", "crypto_deferral", "crypto_no_action",
            "crypto_restricted", "crypto_excluded",
        )
        for field in boolean_fields:
            for value in (0, 1, "true", None, object()):
                with self.subTest(field=field, value=value):
                    with self.assertRaises(ValueError):
                        make(**{field: value})
        for field in ("crypto_reference", "correlation_reference"):
            with self.assertRaises(ValueError):
                make(**{field: ""})
        with self.assertRaises(ValueError):
            generic(context_reference="")
        with self.assertRaises(ValueError):
            authority(evidence_reference="")
        for values in (
            dict(generic_asset_class_context="bad"),
            dict(authority_evidence="bad"),
            dict(crypto_lane_confirmation="CONFIRMED"),
        ):
            with self.assertRaises(ValueError):
                make(**values)
        for factory, fields in (
            (generic, ("current", "contradictory", "in_scope")),
            (authority, ("current", "revoked", "contradictory", "in_scope")),
        ):
            for field in fields:
                for value in (0, 1, "true", None, object()):
                    with self.subTest(factory=factory.__name__, field=field, value=value):
                        with self.assertRaises(ValueError):
                            factory(**{field: value})

    def test_raw_enum_and_typed_decision_rejection(self):
        with self.assertRaises(ValueError):
            generic(asset_class="CRYPTO")
        with self.assertRaises(ValueError):
            generic(validity="UNKNOWN")
        with self.assertRaises(ValueError):
            authority(validity="UNKNOWN")
        with self.assertRaises(ValueError):
            Outcome("UNKNOWN")
        with self.assertRaises(ValueError):
            ReasonCode("UNKNOWN")
        with self.assertRaises(ValueError):
            RequiredAction("UNKNOWN")
        for values in (
            ("", Outcome.NO_ACTION, ReasonCode.NO_ACTION_REQUIRED, RequiredAction.NONE, "c"),
            ("o", Outcome.NO_ACTION, ReasonCode.NO_ACTION_REQUIRED, RequiredAction.NONE, ""),
            ("o", "NO_ACTION", ReasonCode.NO_ACTION_REQUIRED, RequiredAction.NONE, "c"),
            ("o", Outcome.NO_ACTION, "NO_ACTION_REQUIRED", RequiredAction.NONE, "c"),
        ):
            with self.assertRaises(ValueError):
                Decision(*values)
        with self.assertRaises(TypeError):
            evaluate("not-a-request")
        with self.assertRaises(TypeError):
            make(unexpected_field=True)

    def test_production_import_and_side_effect_boundaries(self):
        source = Path("src/sniperbot/crypto/deferral_decision.py").read_text(
            encoding="utf-8"
        )
        tree = ast.parse(source)
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module)
        self.assertEqual(imports, {"__future__", "dataclasses", "enum"})
        prohibited_calls = {
            "open", "print", "input", "exec", "eval", "compile", "__import__"
        }
        called_names = {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        self.assertTrue(prohibited_calls.isdisjoint(called_names))
        prohibited_imports = {
            "os", "sys", "pathlib", "subprocess", "logging", "socket",
            "requests", "urllib", "json", "sqlite3", "sniperbot.stock",
            "sniperbot.options", "sniperbot.rollback", "sniperbot.asset_class",
        }
        self.assertTrue(prohibited_imports.isdisjoint(imports))

    def test_immutability_nonmutation_reference_preservation_and_determinism(self):
        context = generic()
        evidence = authority()
        request = make(
            crypto_reference="opaque-crypto-reference",
            correlation_reference="opaque-correlation-reference",
            generic_asset_class_context=context,
            authority_evidence=evidence,
        )
        before = (asdict(request), asdict(context), asdict(evidence))
        first = evaluate(request)
        second = evaluate(request)
        self.assertEqual(first, second)
        self.assertIsNot(first, request)
        self.assertEqual(first.crypto_reference, request.crypto_reference)
        self.assertEqual(first.correlation_reference, request.correlation_reference)
        self.assertEqual((asdict(request), asdict(context), asdict(evidence)), before)
        for obj, field, value in (
            (context, "asset_class", AssetClass.STOCK),
            (evidence, "validity", "INVALID"),
            (request, "crypto_reference", "changed"),
            (first, "reason_code", ReasonCode.CRYPTO_RESTRICTED),
        ):
            with self.assertRaises(FrozenInstanceError):
                setattr(obj, field, value)


if __name__ == "__main__":
    unittest.main()
