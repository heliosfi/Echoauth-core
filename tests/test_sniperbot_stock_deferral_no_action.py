import unittest
from dataclasses import FrozenInstanceError, asdict

from sniperbot.stock.deferral_decision import (
    AssetClass, AuthorityEvidence, Decision, EmittableReasonCode, GenericAssetClassContext,
    Outcome, ReasonCode, RequiredAction, StockLaneConfirmation, StockRequest,
    create_request, evaluate,
)


def make(**overrides):
    values = dict(stock_reference="opaque-stock-1", stock_evidence_present=True,
                  stock_evidence_current=True, stock_evidence_sufficient=True,
                  stock_evidence_contradictory=False, stock_deferral=False,
                  stock_no_action=False, stock_restricted=False, stock_excluded=False,
                  correlation_reference="corr-1",
                  stock_lane_confirmation=StockLaneConfirmation.CONFIRMED)
    values.update(overrides)
    return StockRequest(**values)


def generic(**overrides):
    values = dict(asset_class=AssetClass.STOCK, validity="VALID", current=True,
                  contradictory=False, in_scope=True, context_reference="ctx-1")
    values.update(overrides)
    return GenericAssetClassContext(**values)


def authority(**overrides):
    values = dict(validity="VALID", current=True, revoked=False,
                  contradictory=False, in_scope=True, evidence_reference="auth-1")
    values.update(overrides)
    return AuthorityEvidence(**values)


class StockDeferralNoActionTests(unittest.TestCase):
    def test_vocabularies_and_decision_restrictions(self):
        self.assertEqual(len(Outcome), 2)
        self.assertEqual(len(ReasonCode), 22)
        self.assertEqual(len(EmittableReasonCode), 22)
        self.assertEqual(len(RequiredAction), 5)
        self.assertEqual(len({RequiredAction.NONE, RequiredAction.HUMAN_REVIEW, RequiredAction.GOVERNANCE_REVIEW}), 3)
        self.assertEqual(len(StockLaneConfirmation), 3)
        self.assertEqual(len(AssetClass), 3)
        with self.assertRaises(ValueError):
            Decision("s", Outcome.NO_ACTION, ReasonCode.NO_ACTION_REQUIRED, RequiredAction.RESET_REQUIRED, "c")
        with self.assertRaises(ValueError):
            Decision("s", Outcome.NO_ACTION, ReasonCode.NO_ACTION_REQUIRED, RequiredAction.FOUNDER_AUTHORITY_REQUIRED, "c")

    def test_all_twenty_branches(self):
        cases = [
            (dict(stock_evidence_contradictory=True), ReasonCode.STOCK_EVIDENCE_CONTRADICTORY),
            (dict(stock_deferral=True, stock_no_action=True), ReasonCode.STOCK_DEFERRAL_NO_ACTION_CONFLICT),
            (dict(stock_evidence_present=False, stock_evidence_current=True), ReasonCode.UNDEFINED_INPUT_COMBINATION),
            (dict(stock_evidence_present=False, stock_evidence_current=False, stock_evidence_sufficient=True), ReasonCode.UNDEFINED_INPUT_COMBINATION),
            (dict(stock_evidence_current=False, stock_evidence_sufficient=True), ReasonCode.UNDEFINED_INPUT_COMBINATION),
            (dict(stock_lane_confirmation=None), ReasonCode.STOCK_LANE_CONFIRMATION_MISSING),
            (dict(stock_lane_confirmation=StockLaneConfirmation.CONTRADICTORY), ReasonCode.STOCK_LANE_CONTRADICTORY),
            (dict(stock_lane_confirmation=StockLaneConfirmation.NOT_CONFIRMED), ReasonCode.STOCK_LANE_NOT_CONFIRMED),
            (dict(generic_asset_class_context=generic(contradictory=True)), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY),
            (dict(generic_asset_class_context=generic(validity="AMBIGUOUS")), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID),
            (dict(generic_asset_class_context=generic(validity="INVALID")), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID),
            (dict(generic_asset_class_context=generic(asset_class=AssetClass.OPTIONS)), ReasonCode.GENERIC_ASSET_CLASS_NOT_STOCK),
            (dict(generic_asset_class_context=generic(current=False)), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_STALE),
            (dict(generic_asset_class_context=generic(in_scope=False)), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE),
            (dict(stock_excluded=True), ReasonCode.STOCK_EXCLUDED),
            (dict(stock_restricted=True), ReasonCode.STOCK_RESTRICTED),
            (dict(authority_evidence=authority(validity="INVALID")), ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            (dict(stock_evidence_present=False, stock_evidence_current=False, stock_evidence_sufficient=False), ReasonCode.STOCK_EVIDENCE_MISSING),
            (dict(stock_evidence_current=False, stock_evidence_sufficient=False), ReasonCode.STOCK_EVIDENCE_STALE),
            (dict(stock_evidence_sufficient=False), ReasonCode.STOCK_EVIDENCE_INSUFFICIENT),
            (dict(stock_deferral=True), ReasonCode.STOCK_DEFERRAL_EXTERNALLY_REQUIRED),
            (dict(stock_no_action=True), ReasonCode.NO_ACTION_REQUIRED),
        ]
        for overrides, reason in cases:
            with self.subTest(reason=reason):
                self.assertEqual(evaluate(make(**overrides)).reason_code, reason)

    def test_precedence_collisions(self):
        lower = [dict(stock_deferral=True, stock_no_action=True), dict(stock_evidence_present=False, stock_evidence_current=True),
                 dict(stock_lane_confirmation=None), dict(stock_lane_confirmation=StockLaneConfirmation.NOT_CONFIRMED),
                 dict(generic_asset_class_context=generic(asset_class=AssetClass.OPTIONS)), dict(stock_excluded=True),
                 dict(stock_restricted=True), dict(authority_evidence=authority(validity="INVALID")),
                 dict(stock_evidence_present=False, stock_evidence_current=False), dict(stock_evidence_current=False, stock_evidence_sufficient=False),
                 dict(stock_evidence_sufficient=False), dict(stock_deferral=True), dict(stock_no_action=True), dict()]
        for overrides in lower:
            self.assertEqual(evaluate(make(stock_evidence_contradictory=True, **overrides)).reason_code, ReasonCode.STOCK_EVIDENCE_CONTRADICTORY)
        self.assertEqual(evaluate(make(stock_deferral=True, stock_no_action=True, stock_evidence_present=False, stock_evidence_current=True)).reason_code, ReasonCode.STOCK_DEFERRAL_NO_ACTION_CONFLICT)
        self.assertEqual(evaluate(make(stock_evidence_present=False, stock_evidence_current=True, stock_evidence_sufficient=False, stock_lane_confirmation=StockLaneConfirmation.NOT_CONFIRMED)).reason_code, ReasonCode.UNDEFINED_INPUT_COMBINATION)
        self.assertEqual(evaluate(make(stock_lane_confirmation=StockLaneConfirmation.NOT_CONFIRMED, generic_asset_class_context=generic(asset_class=AssetClass.OPTIONS), stock_excluded=True)).reason_code, ReasonCode.STOCK_LANE_NOT_CONFIRMED)
        self.assertEqual(evaluate(make(generic_asset_class_context=generic(asset_class=AssetClass.OPTIONS), stock_excluded=True, stock_restricted=True, stock_deferral=True)).reason_code, ReasonCode.GENERIC_ASSET_CLASS_NOT_STOCK)
        self.assertEqual(evaluate(make(stock_excluded=True, stock_restricted=True, authority_evidence=authority(validity="INVALID"))).reason_code, ReasonCode.STOCK_EXCLUDED)
        self.assertEqual(evaluate(make(authority_evidence=authority(validity="INVALID"), stock_deferral=True, stock_no_action=True)), evaluate(make(stock_deferral=True, stock_no_action=True)))

    def test_generic_and_authority_subprecedence(self):
        self.assertEqual(evaluate(make()).reason_code, ReasonCode.NO_ACTION_REQUIRED)
        self.assertEqual(evaluate(make(generic_asset_class_context=generic())).reason_code, ReasonCode.NO_ACTION_REQUIRED)
        self.assertEqual(evaluate(make(generic_asset_class_context=generic(asset_class=AssetClass.CRYPTO))).reason_code, ReasonCode.GENERIC_ASSET_CLASS_NOT_STOCK)
        for context, reason in [(generic(contradictory=True, validity="AMBIGUOUS"), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY),
                                 (generic(validity="AMBIGUOUS", asset_class=AssetClass.OPTIONS), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID),
                                 (generic(asset_class=AssetClass.OPTIONS, current=False, in_scope=False), ReasonCode.GENERIC_ASSET_CLASS_NOT_STOCK)]:
            self.assertEqual(evaluate(make(generic_asset_class_context=context)).reason_code, reason)
        for evidence, reason in [(authority(contradictory=True, validity="AMBIGUOUS", revoked=True), ReasonCode.AUTHORITY_EVIDENCE_INVALID),
                                 (authority(validity="AMBIGUOUS", revoked=True), ReasonCode.AUTHORITY_EVIDENCE_INVALID),
                                 (authority(validity="INVALID", revoked=True), ReasonCode.AUTHORITY_EVIDENCE_INVALID),
                                 (authority(revoked=True, current=False), ReasonCode.AUTHORITY_EVIDENCE_REVOKED),
                                 (authority(current=False, in_scope=False), ReasonCode.AUTHORITY_EVIDENCE_STALE),
                                 (authority(in_scope=False), ReasonCode.AUTHORITY_EVIDENCE_OUT_OF_SCOPE)]:
            self.assertEqual(evaluate(make(authority_evidence=evidence)).reason_code, reason)
        self.assertEqual(evaluate(make(authority_evidence=None)).reason_code, ReasonCode.NO_ACTION_REQUIRED)
        self.assertEqual(evaluate(make(authority_evidence=authority())).reason_code, ReasonCode.NO_ACTION_REQUIRED)

    def test_restriction_and_exclusion_are_descriptive_precedence(self):
        self.assertEqual(evaluate(make(stock_restricted=True)).reason_code, ReasonCode.STOCK_RESTRICTED)
        self.assertEqual(evaluate(make(stock_excluded=True)).reason_code, ReasonCode.STOCK_EXCLUDED)
        self.assertEqual(evaluate(make(stock_excluded=True, stock_restricted=True)).reason_code, ReasonCode.STOCK_EXCLUDED)
        self.assertEqual(evaluate(make(stock_excluded=True, authority_evidence=authority(validity="INVALID"))).reason_code, ReasonCode.STOCK_EXCLUDED)

    def test_undefined_and_evidence_ordering(self):
        for values in (dict(stock_evidence_present=False, stock_evidence_current=True, stock_evidence_sufficient=False),
                       dict(stock_evidence_present=False, stock_evidence_current=False, stock_evidence_sufficient=True),
                       dict(stock_evidence_present=False, stock_evidence_current=False, stock_evidence_sufficient=True)):
            self.assertEqual(evaluate(make(**values)).reason_code, ReasonCode.UNDEFINED_INPUT_COMBINATION)
        self.assertEqual(evaluate(make(stock_evidence_present=False, stock_evidence_current=False, stock_evidence_sufficient=False)).reason_code, ReasonCode.STOCK_EVIDENCE_MISSING)
        self.assertEqual(evaluate(make(stock_evidence_current=False, stock_evidence_sufficient=False)).reason_code, ReasonCode.STOCK_EVIDENCE_STALE)
        self.assertEqual(evaluate(make(stock_evidence_sufficient=False)).reason_code, ReasonCode.STOCK_EVIDENCE_INSUFFICIENT)

    def test_boundaries_raw_values_immutability_and_determinism(self):
        with self.assertRaises(ValueError):
            create_request(**{**make().__dict__, "stock_lane_confirmation": "UNKNOWN"})
        request = make()
        context = generic()
        evidence = authority()
        before = (asdict(request), asdict(context), asdict(evidence))
        first, second = evaluate(request), evaluate(request)
        self.assertEqual(first, second)
        self.assertIsNot(first, request)
        self.assertEqual(first.stock_reference, request.stock_reference)
        self.assertEqual(first.correlation_reference, request.correlation_reference)
        self.assertEqual((asdict(request), asdict(context), asdict(evidence)), before)
        with self.assertRaises(FrozenInstanceError):
            request.stock_reference = "changed"
        with self.assertRaises(FrozenInstanceError):
            context.asset_class = AssetClass.OPTIONS
        with self.assertRaises(FrozenInstanceError):
            evidence.validity = "INVALID"
        with self.assertRaises(FrozenInstanceError):
            first.reason_code = ReasonCode.NO_ACTION_REQUIRED

    def test_empty_references_and_supplied_object_nonmutation(self):
        with self.assertRaises(ValueError):
            make(stock_reference="")
        with self.assertRaises(ValueError):
            make(correlation_reference="")
        with self.assertRaises(ValueError):
            generic(context_reference="")
        with self.assertRaises(ValueError):
            authority(evidence_reference="")
        with self.assertRaises(ValueError):
            Decision("", Outcome.NO_ACTION, ReasonCode.NO_ACTION_REQUIRED, RequiredAction.NONE, "c")
        with self.assertRaises(ValueError):
            Decision("s", Outcome.NO_ACTION, ReasonCode.NO_ACTION_REQUIRED, RequiredAction.NONE, "")

        context = generic()
        evidence = authority()
        request = make(generic_asset_class_context=context, authority_evidence=evidence)
        before = (asdict(request), asdict(context), asdict(evidence))
        result = evaluate(request)
        self.assertIsNot(result, request)
        self.assertEqual((asdict(request), asdict(context), asdict(evidence)), before)
        self.assertEqual(result.stock_reference, request.stock_reference)
        self.assertEqual(result.correlation_reference, request.correlation_reference)

    def test_undefined_over_all_lower_categories(self):
        lower = [
            dict(stock_lane_confirmation=None),
            dict(stock_lane_confirmation=StockLaneConfirmation.CONTRADICTORY),
            dict(stock_lane_confirmation=StockLaneConfirmation.NOT_CONFIRMED),
            dict(generic_asset_class_context=generic(contradictory=True)),
            dict(generic_asset_class_context=generic(validity="AMBIGUOUS")),
            dict(generic_asset_class_context=generic(asset_class=AssetClass.OPTIONS)),
            dict(generic_asset_class_context=generic(current=False)),
            dict(generic_asset_class_context=generic(in_scope=False)),
            dict(stock_excluded=True), dict(stock_restricted=True),
            dict(authority_evidence=authority(validity="INVALID")),
            dict(stock_deferral=True), dict(stock_no_action=True),
        ]
        for overrides in lower:
            values = dict(stock_evidence_present=False, stock_evidence_current=True,
                          stock_evidence_sufficient=False)
            values.update(overrides)
            result = evaluate(make(**values))
            self.assertEqual((result.outcome, result.reason_code, result.required_action),
                             (Outcome.NO_ACTION, ReasonCode.UNDEFINED_INPUT_COMBINATION, RequiredAction.GOVERNANCE_REVIEW))
        for values in (
            dict(stock_evidence_present=False, stock_evidence_current=True, stock_evidence_sufficient=False),
            dict(stock_evidence_present=False, stock_evidence_current=False, stock_evidence_sufficient=True),
            dict(stock_evidence_present=False, stock_evidence_current=False, stock_evidence_sufficient=True),
        ):
            result = evaluate(make(**values))
            self.assertEqual(result.reason_code, ReasonCode.UNDEFINED_INPUT_COMBINATION)

    def test_each_lane_failure_over_all_lower_categories(self):
        lower = [dict(generic_asset_class_context=generic(asset_class=AssetClass.OPTIONS)),
                 dict(stock_excluded=True), dict(stock_restricted=True),
                 dict(authority_evidence=authority(validity="INVALID")),
                 dict(stock_evidence_present=False, stock_evidence_current=False, stock_evidence_sufficient=False),
                 dict(stock_evidence_current=False, stock_evidence_sufficient=False),
                 dict(stock_evidence_sufficient=False), dict(stock_deferral=True), dict(stock_no_action=True)]
        for lane, expected in ((None, ReasonCode.STOCK_LANE_CONFIRMATION_MISSING),
                               (StockLaneConfirmation.CONTRADICTORY, ReasonCode.STOCK_LANE_CONTRADICTORY),
                               (StockLaneConfirmation.NOT_CONFIRMED, ReasonCode.STOCK_LANE_NOT_CONFIRMED)):
            for overrides in lower:
                result = evaluate(make(stock_lane_confirmation=lane, **overrides))
                self.assertEqual((result.outcome, result.reason_code, result.required_action),
                                 (Outcome.NO_ACTION, expected, RequiredAction.GOVERNANCE_REVIEW))

    def test_each_generic_failure_over_all_lower_categories(self):
        lower = [dict(stock_excluded=True), dict(stock_restricted=True),
                 dict(authority_evidence=authority(validity="INVALID")),
                 dict(stock_evidence_present=False, stock_evidence_current=False, stock_evidence_sufficient=False),
                 dict(stock_evidence_current=False, stock_evidence_sufficient=False),
                 dict(stock_evidence_sufficient=False), dict(stock_deferral=True), dict(stock_no_action=True)]
        contexts = [
            (generic(contradictory=True), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY),
            (generic(validity="AMBIGUOUS"), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID),
            (generic(validity="INVALID"), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID),
            (generic(asset_class=AssetClass.OPTIONS), ReasonCode.GENERIC_ASSET_CLASS_NOT_STOCK),
            (generic(current=False), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_STALE),
            (generic(in_scope=False), ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE),
        ]
        for context, expected in contexts:
            for overrides in lower:
                result = evaluate(make(generic_asset_class_context=context, **overrides))
                self.assertEqual((result.outcome, result.reason_code, result.required_action),
                                 (Outcome.NO_ACTION, expected, RequiredAction.GOVERNANCE_REVIEW))

    def test_restriction_and_exclusion_over_all_lower_categories(self):
        lower = [dict(authority_evidence=authority(validity="INVALID")),
                 dict(stock_evidence_present=False, stock_evidence_current=False, stock_evidence_sufficient=False),
                 dict(stock_evidence_current=False, stock_evidence_sufficient=False),
                 dict(stock_evidence_sufficient=False), dict(stock_deferral=True), dict(stock_no_action=True)]
        for flag, expected in (("stock_excluded", ReasonCode.STOCK_EXCLUDED),
                               ("stock_restricted", ReasonCode.STOCK_RESTRICTED)):
            for overrides in lower:
                result = evaluate(make(**{flag: True}, **overrides))
                self.assertEqual((result.outcome, result.reason_code, result.required_action),
                                 (Outcome.NO_ACTION, expected, RequiredAction.NONE))

    def test_authority_over_all_lower_postures(self):
        lower = [dict(stock_evidence_present=False, stock_evidence_current=False, stock_evidence_sufficient=False),
                 dict(stock_evidence_current=False, stock_evidence_sufficient=False),
                 dict(stock_evidence_sufficient=False), dict(stock_deferral=True), dict(stock_no_action=True), dict()]
        for overrides in lower:
            result = evaluate(make(authority_evidence=authority(validity="INVALID"), **overrides))
            self.assertEqual((result.outcome, result.reason_code, result.required_action),
                             (Outcome.NO_ACTION, ReasonCode.AUTHORITY_EVIDENCE_INVALID, RequiredAction.GOVERNANCE_REVIEW))

    def test_explicit_no_action_and_fallback_have_same_safe_mapping(self):
        explicit = evaluate(make(stock_no_action=True))
        fallback = evaluate(make(stock_no_action=False))
        expected = (Outcome.NO_ACTION, ReasonCode.NO_ACTION_REQUIRED, RequiredAction.NONE)
        self.assertEqual((explicit.outcome, explicit.reason_code, explicit.required_action), expected)
        self.assertEqual((fallback.outcome, fallback.reason_code, fallback.required_action), expected)


if __name__ == "__main__":
    unittest.main()
