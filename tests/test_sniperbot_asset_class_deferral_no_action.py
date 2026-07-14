import unittest
from dataclasses import FrozenInstanceError

from sniperbot.deferral.asset_class_decision import (
    AssetClass, AuthorityEvidence, Decision, DeferralRequest, Outcome,
    ReasonCode, RequiredAction, create_request, evaluate,
)


def make(**overrides):
    values = dict(asset_class=AssetClass.STOCK, evidence_present=True,
                  evidence_current=True, evidence_sufficient=True,
                  evidence_contradictory=False, eligibility_status=None,
                  exclusion_status=None, explicit_deferral_required=False,
                  authority_evidence=None, correlation_reference="corr-1")
    values.update(overrides)
    return DeferralRequest(**values)


def authority(**overrides):
    values = dict(validity="VALID", currentness="CURRENT",
                  revocation="NON_REVOKED", scope="IN_SCOPE",
                  evidence_reference="auth-1")
    values.update(overrides)
    return AuthorityEvidence(**values)


class AssetClassDeferralNoActionTests(unittest.TestCase):
    def test_closed_vocabularies(self):
        self.assertEqual(len(AssetClass), 3)
        self.assertEqual(len(Outcome), 2)
        self.assertEqual(len(ReasonCode), 13)
        self.assertEqual(len(RequiredAction), 5)

    def test_each_asset_class_and_fallback(self):
        for asset in AssetClass:
            self.assertEqual(evaluate(make(asset_class=asset)).asset_class, asset)
        result = evaluate(make())
        self.assertEqual((result.outcome, result.reason_code, result.required_action), (Outcome.NO_ACTION, ReasonCode.NO_ACTION_REQUIRED, RequiredAction.NONE))

    def test_precedence_and_undefined_combinations(self):
        cases = [
            (dict(evidence_contradictory=True, explicit_deferral_required=True), ReasonCode.EVIDENCE_CONTRADICTORY),
            (dict(evidence_present=False, evidence_current=True), ReasonCode.UNDEFINED_INPUT_COMBINATION),
            (dict(evidence_present=False, evidence_sufficient=True), ReasonCode.UNDEFINED_INPUT_COMBINATION),
            (dict(evidence_current=False, evidence_sufficient=True), ReasonCode.UNDEFINED_INPUT_COMBINATION),
            (dict(eligibility_status=True, exclusion_status=True), ReasonCode.UNDEFINED_INPUT_COMBINATION),
            (dict(exclusion_status=True), ReasonCode.EXTERNALLY_EXCLUDED),
            (dict(evidence_present=False, evidence_current=False, evidence_sufficient=False), ReasonCode.EVIDENCE_MISSING),
            (dict(evidence_current=False, evidence_sufficient=False), ReasonCode.EVIDENCE_STALE),
            (dict(evidence_sufficient=False), ReasonCode.EVIDENCE_INSUFFICIENT),
            (dict(explicit_deferral_required=True), ReasonCode.EXTERNAL_DEFERRAL_REQUIRED),
        ]
        for overrides, reason in cases:
            self.assertEqual(evaluate(make(**overrides)).reason_code, reason)

    def test_authority_subprecedence(self):
        for overrides, reason in [
            (dict(validity="AMBIGUOUS", revocation="REVOKED", currentness="STALE", scope="OUT_OF_SCOPE"), ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            (dict(validity="INVALID", revocation="REVOKED", currentness="STALE", scope="OUT_OF_SCOPE"), ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            (dict(revocation="REVOKED", currentness="STALE", scope="OUT_OF_SCOPE"), ReasonCode.AUTHORITY_EVIDENCE_REVOKED),
            (dict(currentness="STALE", scope="OUT_OF_SCOPE"), ReasonCode.AUTHORITY_EVIDENCE_STALE),
            (dict(scope="OUT_OF_SCOPE"), ReasonCode.AUTHORITY_EVIDENCE_OUT_OF_SCOPE),
        ]:
            result = evaluate(make(authority_evidence=authority(**overrides)))
            self.assertEqual(result.reason_code, reason)
            self.assertEqual(result.outcome, Outcome.NO_ACTION)
            self.assertEqual(result.required_action, RequiredAction.GOVERNANCE_REVIEW)

    def test_authority_absent_valid_and_eligibility_context(self):
        self.assertEqual(evaluate(make(authority_evidence=None)).reason_code, ReasonCode.NO_ACTION_REQUIRED)
        self.assertEqual(evaluate(make(authority_evidence=authority())).reason_code, ReasonCode.NO_ACTION_REQUIRED)
        self.assertEqual(evaluate(make(eligibility_status=False)).reason_code, ReasonCode.NO_ACTION_REQUIRED)

    def test_unknown_raw_asset_class_rejected(self):
        with self.assertRaises(ValueError):
            create_request("UNKNOWN", evidence_present=True, evidence_current=True,
                           evidence_sufficient=True, evidence_contradictory=False,
                           eligibility_status=None, exclusion_status=None,
                           explicit_deferral_required=False, authority_evidence=None,
                           correlation_reference="corr-1")

    def test_immutability_correlation_and_determinism(self):
        request = make()
        with self.assertRaises(FrozenInstanceError):
            request.correlation_reference = "changed"
        first, second = evaluate(request), evaluate(request)
        self.assertEqual(first, second)
        self.assertIsInstance(first, Decision)
        self.assertEqual(first.correlation_reference, request.correlation_reference)


if __name__ == "__main__":
    unittest.main()
