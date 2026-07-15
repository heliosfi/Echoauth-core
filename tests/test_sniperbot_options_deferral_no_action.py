import json
import unittest
from dataclasses import FrozenInstanceError, asdict
from pathlib import Path

from sniperbot.options.deferral_decision import (
    AssetClass,
    AuthorityEvidence,
    Decision,
    EmittableReasonCode,
    GenericAssetClassContext,
    OptionsLaneConfirmation,
    OptionsRequest,
    Outcome,
    ReasonCode,
    RequiredAction,
    create_request,
    evaluate,
)


def make(**overrides):
    values = dict(
        options_reference="option-ref",
        options_evidence_present=True,
        options_evidence_current=True,
        options_evidence_sufficient=True,
        options_evidence_contradictory=False,
        options_deferral=False,
        options_no_action=False,
        options_restricted=False,
        options_excluded=False,
        correlation_reference="correlation-ref",
        options_lane_confirmation=OptionsLaneConfirmation.CONFIRMED,
    )
    values.update(overrides)
    return create_request(**values)


def generic(**overrides):
    values = dict(
        asset_class=AssetClass.OPTIONS,
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


class OptionsDeferralNoActionTests(unittest.TestCase):
    def test_vocabularies_match_schema_and_decision_restrictions(self):
        schema = json.loads(
            Path("schemas/sniperbot-options-deferral-no-action-decision.schema.json").read_text(
                encoding="utf-8"
            )
        )
        definitions = schema["$defs"]
        self.assertEqual({item.value for item in Outcome}, set(definitions["Outcome"]["enum"]))
        self.assertEqual({item.value for item in ReasonCode}, set(definitions["ReasonCode"]["enum"]))
        self.assertEqual({item.value for item in EmittableReasonCode}, set(definitions["ReasonCode"]["enum"]))
        self.assertEqual({item.value for item in RequiredAction}, set(definitions["RequiredAction"]["enum"]))
        self.assertEqual({item.value for item in OptionsLaneConfirmation}, set(definitions["OptionsLaneConfirmation"]["enum"]))
        self.assertEqual({item.value for item in AssetClass}, set(definitions["GenericAssetClassContext"]["properties"]["asset_class"]["enum"]))
        self.assertEqual((len(Outcome), len(ReasonCode), len(RequiredAction), len(OptionsLaneConfirmation), len(AssetClass)), (2, 22, 5, 3, 3))
        self.assertEqual(len(definitions["EmittableAction"]["enum"]), 3)
        self.assertNotIn("UNKNOWN", {item.name for item in ReasonCode})
        for action in (RequiredAction.FOUNDER_AUTHORITY_REQUIRED, RequiredAction.RESET_REQUIRED):
            with self.assertRaises(ValueError):
                Decision("o", Outcome.NO_ACTION, ReasonCode.NO_ACTION_REQUIRED, action, "c")

    def test_all_twenty_first_match_branches(self):
        cases = [
            (dict(options_evidence_contradictory=True), (Outcome.NO_ACTION, ReasonCode.OPTIONS_EVIDENCE_CONTRADICTORY, RequiredAction.HUMAN_REVIEW)),
            (dict(options_deferral=True, options_no_action=True), (Outcome.NO_ACTION, ReasonCode.OPTIONS_DEFERRAL_NO_ACTION_CONFLICT, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(options_evidence_present=False, options_evidence_current=True, options_evidence_sufficient=False), (Outcome.NO_ACTION, ReasonCode.UNDEFINED_INPUT_COMBINATION, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(options_lane_confirmation=None), (Outcome.NO_ACTION, ReasonCode.OPTIONS_LANE_CONFIRMATION_MISSING, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(options_lane_confirmation=OptionsLaneConfirmation.CONTRADICTORY), (Outcome.NO_ACTION, ReasonCode.OPTIONS_LANE_CONTRADICTORY, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(options_lane_confirmation=OptionsLaneConfirmation.NOT_CONFIRMED), (Outcome.NO_ACTION, ReasonCode.OPTIONS_LANE_NOT_CONFIRMED, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(generic_asset_class_context=generic(contradictory=True)), (Outcome.NO_ACTION, ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(generic_asset_class_context=generic(validity="AMBIGUOUS")), (Outcome.NO_ACTION, ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(generic_asset_class_context=generic(asset_class=AssetClass.STOCK)), (Outcome.NO_ACTION, ReasonCode.GENERIC_ASSET_CLASS_NOT_OPTIONS, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(generic_asset_class_context=generic(current=False)), (Outcome.NO_ACTION, ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_STALE, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(generic_asset_class_context=generic(in_scope=False)), (Outcome.NO_ACTION, ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(options_excluded=True), (Outcome.NO_ACTION, ReasonCode.OPTIONS_EXCLUDED, RequiredAction.NONE)),
            (dict(options_restricted=True), (Outcome.NO_ACTION, ReasonCode.OPTIONS_RESTRICTED, RequiredAction.NONE)),
            (dict(authority_evidence=authority(validity="INVALID")), (Outcome.NO_ACTION, ReasonCode.AUTHORITY_EVIDENCE_INVALID, RequiredAction.GOVERNANCE_REVIEW)),
            (dict(options_evidence_present=False, options_evidence_current=False, options_evidence_sufficient=False), (Outcome.DEFER, ReasonCode.OPTIONS_EVIDENCE_MISSING, RequiredAction.HUMAN_REVIEW)),
            (dict(options_evidence_current=False, options_evidence_sufficient=False), (Outcome.DEFER, ReasonCode.OPTIONS_EVIDENCE_STALE, RequiredAction.HUMAN_REVIEW)),
            (dict(options_evidence_sufficient=False), (Outcome.DEFER, ReasonCode.OPTIONS_EVIDENCE_INSUFFICIENT, RequiredAction.HUMAN_REVIEW)),
            (dict(options_deferral=True), (Outcome.DEFER, ReasonCode.OPTIONS_DEFERRAL_EXTERNALLY_REQUIRED, RequiredAction.HUMAN_REVIEW)),
            (dict(options_no_action=True), (Outcome.NO_ACTION, ReasonCode.NO_ACTION_REQUIRED, RequiredAction.NONE)),
            (dict(), (Outcome.NO_ACTION, ReasonCode.NO_ACTION_REQUIRED, RequiredAction.NONE)),
        ]
        for values, expected in cases:
            with self.subTest(values=values):
                self.assertEqual(mapping(make(**values)), expected)

    def test_three_undefined_predicates_are_valid_typed_requests(self):
        cases = (
            dict(options_evidence_present=False, options_evidence_current=True, options_evidence_sufficient=False),
            dict(options_evidence_present=False, options_evidence_current=False, options_evidence_sufficient=True),
            dict(options_evidence_present=True, options_evidence_current=False, options_evidence_sufficient=True),
        )
        for values in cases:
            request = make(**values)
            self.assertIsInstance(request, OptionsRequest)
            self.assertEqual(evaluate(request).reason_code, ReasonCode.UNDEFINED_INPUT_COMBINATION)

    def test_contradiction_and_conflict_global_precedence(self):
        lower = dict(
            options_evidence_present=False,
            options_evidence_current=True,
            options_evidence_sufficient=False,
            options_deferral=True,
            options_no_action=True,
            options_lane_confirmation=OptionsLaneConfirmation.CONTRADICTORY,
            generic_asset_class_context=generic(contradictory=True),
            options_excluded=True,
            options_restricted=True,
            authority_evidence=authority(contradictory=True),
        )
        self.assertEqual(evaluate(make(options_evidence_contradictory=True, **lower)).reason_code, ReasonCode.OPTIONS_EVIDENCE_CONTRADICTORY)
        lower["options_evidence_present"] = True
        lower["options_evidence_current"] = True
        lower["options_evidence_sufficient"] = True
        self.assertEqual(evaluate(make(**lower)).reason_code, ReasonCode.OPTIONS_DEFERRAL_NO_ACTION_CONFLICT)

    def test_undefined_and_lane_failures_over_lower_categories(self):
        lower = [
            dict(generic_asset_class_context=generic(contradictory=True)),
            dict(options_excluded=True),
            dict(options_restricted=True),
            dict(authority_evidence=authority(validity="INVALID")),
            dict(options_deferral=True),
            dict(options_no_action=True),
        ]
        for overrides in lower:
            values = dict(options_evidence_present=False, options_evidence_current=True, options_evidence_sufficient=False)
            values.update(overrides)
            self.assertEqual(evaluate(make(**values)).reason_code, ReasonCode.UNDEFINED_INPUT_COMBINATION)
        for lane, expected in (
            (None, ReasonCode.OPTIONS_LANE_CONFIRMATION_MISSING),
            (OptionsLaneConfirmation.CONTRADICTORY, ReasonCode.OPTIONS_LANE_CONTRADICTORY),
            (OptionsLaneConfirmation.NOT_CONFIRMED, ReasonCode.OPTIONS_LANE_NOT_CONFIRMED),
        ):
            for overrides in lower:
                self.assertEqual(evaluate(make(options_lane_confirmation=lane, **overrides)).reason_code, expected)

    def test_generic_subprecedence_and_lower_category_precedence(self):
        contexts = [
            (generic(contradictory=True, validity="AMBIGUOUS", asset_class=AssetClass.STOCK, current=False, in_scope=False), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY),
            (generic(validity="AMBIGUOUS", asset_class=AssetClass.STOCK, current=False, in_scope=False), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID),
            (generic(validity="INVALID", asset_class=AssetClass.STOCK, current=False, in_scope=False), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID),
            (generic(asset_class=AssetClass.STOCK, current=False, in_scope=False), ReasonCode.GENERIC_ASSET_CLASS_NOT_OPTIONS),
            (generic(asset_class=AssetClass.CRYPTO), ReasonCode.GENERIC_ASSET_CLASS_NOT_OPTIONS),
            (generic(current=False, in_scope=False), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_STALE),
            (generic(in_scope=False), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE),
        ]
        for context, expected in contexts:
            for lower in (
                dict(options_excluded=True),
                dict(options_restricted=True),
                dict(authority_evidence=authority(validity="INVALID")),
                dict(options_evidence_present=False, options_evidence_current=False, options_evidence_sufficient=False),
                dict(options_evidence_current=False, options_evidence_sufficient=False),
                dict(options_evidence_sufficient=False),
                dict(options_deferral=True),
                dict(options_no_action=True),
            ):
                self.assertEqual(evaluate(make(generic_asset_class_context=context, **lower)).reason_code, expected)
        self.assertEqual(evaluate(make(generic_asset_class_context=None)).reason_code, ReasonCode.NO_ACTION_REQUIRED)
        self.assertEqual(evaluate(make(generic_asset_class_context=generic())).reason_code, ReasonCode.NO_ACTION_REQUIRED)

    def test_exclusion_restriction_and_authority_precedence(self):
        authority_failure = authority(validity="INVALID")
        lower_categories = (
            dict(options_restricted=True),
            dict(authority_evidence=authority_failure),
            dict(options_evidence_present=False, options_evidence_current=False, options_evidence_sufficient=False),
            dict(options_evidence_current=False, options_evidence_sufficient=False),
            dict(options_evidence_sufficient=False),
            dict(options_deferral=True),
            dict(options_no_action=True),
        )
        for lower in lower_categories:
            self.assertEqual(evaluate(make(options_excluded=True, **lower)).reason_code, ReasonCode.OPTIONS_EXCLUDED)
        for lower in lower_categories[1:]:
            self.assertEqual(evaluate(make(options_restricted=True, **lower)).reason_code, ReasonCode.OPTIONS_RESTRICTED)
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
            (dict(options_evidence_present=False, options_evidence_current=False, options_evidence_sufficient=False), ReasonCode.OPTIONS_EVIDENCE_MISSING),
            (dict(options_evidence_present=False, options_evidence_current=False, options_evidence_sufficient=False), ReasonCode.OPTIONS_EVIDENCE_MISSING),
            (dict(options_evidence_current=False, options_evidence_sufficient=False), ReasonCode.OPTIONS_EVIDENCE_STALE),
        ]
        for values, expected in evidence_cases:
            self.assertEqual(evaluate(make(**values)).reason_code, expected)
        self.assertEqual(evaluate(make(options_deferral=True, options_no_action=True)).reason_code, ReasonCode.OPTIONS_DEFERRAL_NO_ACTION_CONFLICT)
        self.assertEqual(evaluate(make(options_deferral=True)).reason_code, ReasonCode.OPTIONS_DEFERRAL_EXTERNALLY_REQUIRED)
        explicit = mapping(make(options_no_action=True))
        fallback = mapping(make())
        self.assertEqual(explicit, fallback)

    def test_strict_boolean_empty_reference_and_nested_object_rejection(self):
        boolean_fields = (
            "options_evidence_present", "options_evidence_current", "options_evidence_sufficient",
            "options_evidence_contradictory", "options_deferral", "options_no_action",
            "options_restricted", "options_excluded",
        )
        for field in boolean_fields:
            for value in (0, 1, "true", None):
                with self.subTest(field=field, value=value):
                    with self.assertRaises(ValueError):
                        make(**{field: value})
        for field in ("options_reference", "correlation_reference"):
            with self.assertRaises(ValueError):
                make(**{field: ""})
        with self.assertRaises(ValueError):
            generic(context_reference="")
        with self.assertRaises(ValueError):
            authority(evidence_reference="")
        for values in (
            dict(generic_asset_class_context="bad"),
            dict(authority_evidence="bad"),
            dict(options_lane_confirmation="CONFIRMED"),
        ):
            with self.assertRaises(ValueError):
                make(**values)
        for factory, fields in (
            (generic, ("current", "contradictory", "in_scope")),
            (authority, ("current", "revoked", "contradictory", "in_scope")),
        ):
            for field in fields:
                for value in (0, 1, "true", None):
                    with self.subTest(factory=factory.__name__, field=field, value=value):
                        with self.assertRaises(ValueError):
                            factory(**{field: value})

    def test_raw_enum_and_typed_decision_rejection(self):
        with self.assertRaises(ValueError):
            generic(asset_class="OPTIONS")
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

    def test_immutability_nonmutation_reference_preservation_and_determinism(self):
        context = generic()
        evidence = authority()
        request = make(
            options_reference="opaque-options-reference",
            correlation_reference="opaque-correlation-reference",
            generic_asset_class_context=context,
            authority_evidence=evidence,
        )
        before = (asdict(request), asdict(context), asdict(evidence))
        first = evaluate(request)
        second = evaluate(request)
        self.assertEqual(first, second)
        self.assertIsNot(first, request)
        self.assertEqual(first.options_reference, request.options_reference)
        self.assertEqual(first.correlation_reference, request.correlation_reference)
        self.assertEqual((asdict(request), asdict(context), asdict(evidence)), before)
        for obj, field, value in (
            (context, "asset_class", AssetClass.STOCK),
            (evidence, "validity", "INVALID"),
            (request, "options_reference", "changed"),
            (first, "reason_code", ReasonCode.OPTIONS_RESTRICTED),
        ):
            with self.assertRaises(FrozenInstanceError):
                setattr(obj, field, value)


if __name__ == "__main__":
    unittest.main()
