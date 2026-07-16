"""Direct evidence for the Options Eligibility / Exclusion evaluator."""

from __future__ import annotations

import ast
import dataclasses
import inspect
import unittest
from pathlib import Path

from sniperbot.options import eligibility_decision as subject
from sniperbot.options.eligibility_decision import (
    AuthorityEvidence,
    Decision,
    OptionsEligibilityRequest,
    Outcome,
    ReasonCode,
    RequiredAction,
    Validity,
    create_request,
    evaluate,
)


class OptionsEligibilityExclusionTests(unittest.TestCase):
    def request(self, **changes: object) -> OptionsEligibilityRequest:
        values: dict[str, object] = {
            "options_reference": "options-ref",
            "eligibility_evidence_present": True,
            "eligibility_evidence_current": True,
            "eligibility_evidence_sufficient": True,
            "eligibility_evidence_contradictory": False,
            "options_eligible": True,
            "options_excluded": False,
            "options_restricted": False,
            "eligibility_evidence_reference": "evidence-ref",
            "correlation_reference": "correlation-ref",
        }
        values.update(changes)
        return create_request(**values)

    @staticmethod
    def authority(**changes: object) -> AuthorityEvidence:
        values: dict[str, object] = {
            "validity": Validity.VALID,
            "current": True,
            "revoked": False,
            "contradictory": False,
            "in_scope": True,
            "evidence_reference": "authority-ref",
        }
        values.update(changes)
        return AuthorityEvidence(**values)

    def assert_decision(
        self,
        request: OptionsEligibilityRequest,
        outcome: Outcome,
        reason: ReasonCode,
        action: RequiredAction,
    ) -> None:
        result = evaluate(request)
        self.assertEqual((result.outcome, result.reason_code, result.required_action), (outcome, reason, action))
        self.assertEqual(result.options_reference, request.options_reference)
        self.assertEqual(result.eligibility_evidence_reference, request.eligibility_evidence_reference)
        self.assertEqual(result.correlation_reference, request.correlation_reference)

    def test_exact_public_api_and_enum_vocabularies(self) -> None:
        self.assertEqual(subject.__all__, [
            "Outcome", "ReasonCode", "RequiredAction", "Validity",
            "AuthorityEvidence", "OptionsEligibilityRequest", "Decision",
            "create_request", "evaluate",
        ])
        self.assertEqual([member.value for member in Outcome], ["ELIGIBLE", "EXCLUDED", "RESTRICTED", "REVIEW_REQUIRED"])
        self.assertEqual([member.value for member in ReasonCode], [
            "OPTIONS_ELIGIBLE", "OPTIONS_EXCLUDED", "OPTIONS_RESTRICTED",
            "OPTIONS_ELIGIBILITY_EVIDENCE_MISSING", "OPTIONS_ELIGIBILITY_EVIDENCE_STALE",
            "OPTIONS_ELIGIBILITY_EVIDENCE_INSUFFICIENT", "OPTIONS_ELIGIBILITY_EVIDENCE_CONTRADICTORY",
            "OPTIONS_ELIGIBLE_EXCLUDED_CONFLICT", "OPTIONS_ELIGIBLE_RESTRICTED_CONFLICT",
            "AUTHORITY_EVIDENCE_INVALID", "AUTHORITY_EVIDENCE_STALE", "AUTHORITY_EVIDENCE_REVOKED",
            "AUTHORITY_EVIDENCE_OUT_OF_SCOPE", "UNDEFINED_INPUT_COMBINATION",
            "OPTIONS_ELIGIBILITY_UNRESOLVED",
        ])
        self.assertEqual([member.value for member in RequiredAction], [
            "NONE", "HUMAN_REVIEW", "GOVERNANCE_REVIEW",
            "FOUNDER_AUTHORITY_REQUIRED", "RESET_REQUIRED",
        ])
        self.assertEqual([member.value for member in Validity], ["VALID", "INVALID", "AMBIGUOUS"])
        for enum_type in (Outcome, ReasonCode, RequiredAction, Validity):
            self.assertEqual(len(enum_type.__members__), len(list(enum_type)))
        self.assertFalse(hasattr(subject, "EmittableAction"))
        self.assertFalse(hasattr(subject, "AssetClass"))

    def test_exact_frozen_dataclass_contracts(self) -> None:
        self.assertEqual([field.name for field in dataclasses.fields(AuthorityEvidence)], [
            "validity", "current", "revoked", "contradictory", "in_scope", "evidence_reference",
        ])
        self.assertEqual([field.name for field in dataclasses.fields(OptionsEligibilityRequest)], [
            "options_reference", "eligibility_evidence_present", "eligibility_evidence_current",
            "eligibility_evidence_sufficient", "eligibility_evidence_contradictory",
            "options_eligible", "options_excluded", "options_restricted",
            "eligibility_evidence_reference", "correlation_reference", "authority_evidence",
        ])
        self.assertEqual([field.name for field in dataclasses.fields(Decision)], [
            "outcome", "reason_code", "required_action", "options_reference",
            "eligibility_evidence_reference", "correlation_reference",
        ])
        request_fields = dataclasses.fields(OptionsEligibilityRequest)
        self.assertTrue(all(field.default is dataclasses.MISSING for field in request_fields[:10]))
        self.assertIsNone(request_fields[10].default)
        for cls in (AuthorityEvidence, OptionsEligibilityRequest, Decision):
            self.assertTrue(cls.__dataclass_params__.frozen)

    def test_exact_function_signatures(self) -> None:
        self.assertEqual(str(inspect.signature(create_request)), "(**values: 'object') -> 'OptionsEligibilityRequest'")
        self.assertEqual(str(inspect.signature(evaluate)), "(request: 'OptionsEligibilityRequest') -> 'Decision'")

    def test_omission_accepted_and_explicit_none_rejected(self) -> None:
        self.assertIsNone(self.request().authority_evidence)
        with self.assertRaises(TypeError):
            self.request(authority_evidence=None)
        direct = OptionsEligibilityRequest(
            "options-ref", True, True, True, False, True, False, False,
            "evidence-ref", "correlation-ref",
        )
        self.assertIsNone(direct.authority_evidence)

    def test_strict_request_and_authority_boundaries(self) -> None:
        for field in (
            "eligibility_evidence_present", "eligibility_evidence_current",
            "eligibility_evidence_sufficient", "eligibility_evidence_contradictory",
            "options_eligible", "options_excluded", "options_restricted",
        ):
            with self.subTest(field=field), self.assertRaises(TypeError):
                self.request(**{field: 1})
        for field in ("options_reference", "eligibility_evidence_reference", "correlation_reference"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.request(**{field: ""})
            with self.subTest(field=field), self.assertRaises(TypeError):
                self.request(**{field: 1})
        with self.assertRaises(TypeError):
            self.request(authority_evidence={})
        with self.assertRaises(TypeError):
            create_request(unexpected=True)
        with self.assertRaises(TypeError):
            AuthorityEvidence("VALID", True, False, False, True, "ref")
        with self.assertRaises(TypeError):
            AuthorityEvidence(Validity.VALID, 1, False, False, True, "ref")
        with self.assertRaises(ValueError):
            AuthorityEvidence(Validity.VALID, True, False, False, True, "")

    def test_decision_typed_and_emittable_boundaries(self) -> None:
        valid = (Outcome.ELIGIBLE, ReasonCode.OPTIONS_ELIGIBLE, RequiredAction.NONE, "o", "e", "c")
        Decision(*valid)
        with self.assertRaises(TypeError):
            Decision("ELIGIBLE", ReasonCode.OPTIONS_ELIGIBLE, RequiredAction.NONE, "o", "e", "c")
        with self.assertRaises(TypeError):
            Decision(Outcome.ELIGIBLE, "OPTIONS_ELIGIBLE", RequiredAction.NONE, "o", "e", "c")
        for action in (RequiredAction.FOUNDER_AUTHORITY_REQUIRED, RequiredAction.RESET_REQUIRED):
            with self.subTest(action=action), self.assertRaises(ValueError):
                Decision(Outcome.REVIEW_REQUIRED, ReasonCode.OPTIONS_ELIGIBILITY_UNRESOLVED, action, "o", "e", "c")
        for index in (3, 4, 5):
            values = list(valid)
            values[index] = ""
            with self.subTest(index=index), self.assertRaises(ValueError):
                Decision(*values)

    def test_non_request_evaluation_rejected(self) -> None:
        for value in (None, {}, object()):
            with self.subTest(value=value), self.assertRaises(TypeError):
                evaluate(value)

    def test_all_twelve_branches_and_exact_mappings(self) -> None:
        cases = [
            ({"eligibility_evidence_contradictory": True}, Outcome.REVIEW_REQUIRED, ReasonCode.OPTIONS_ELIGIBILITY_EVIDENCE_CONTRADICTORY, RequiredAction.HUMAN_REVIEW),
            ({"options_excluded": True}, Outcome.REVIEW_REQUIRED, ReasonCode.OPTIONS_ELIGIBLE_EXCLUDED_CONFLICT, RequiredAction.GOVERNANCE_REVIEW),
            ({"options_restricted": True}, Outcome.RESTRICTED, ReasonCode.OPTIONS_ELIGIBLE_RESTRICTED_CONFLICT, RequiredAction.HUMAN_REVIEW),
            ({"options_eligible": False, "eligibility_evidence_present": False, "eligibility_evidence_current": True, "eligibility_evidence_sufficient": False}, Outcome.REVIEW_REQUIRED, ReasonCode.UNDEFINED_INPUT_COMBINATION, RequiredAction.GOVERNANCE_REVIEW),
            ({"options_eligible": False, "options_excluded": True}, Outcome.EXCLUDED, ReasonCode.OPTIONS_EXCLUDED, RequiredAction.NONE),
            ({"options_eligible": False, "options_restricted": True}, Outcome.RESTRICTED, ReasonCode.OPTIONS_RESTRICTED, RequiredAction.HUMAN_REVIEW),
            ({"options_eligible": False, "authority_evidence": self.authority(validity=Validity.INVALID)}, Outcome.REVIEW_REQUIRED, ReasonCode.AUTHORITY_EVIDENCE_INVALID, RequiredAction.GOVERNANCE_REVIEW),
            ({"options_eligible": False, "eligibility_evidence_present": False, "eligibility_evidence_current": False, "eligibility_evidence_sufficient": False}, Outcome.REVIEW_REQUIRED, ReasonCode.OPTIONS_ELIGIBILITY_EVIDENCE_MISSING, RequiredAction.HUMAN_REVIEW),
            ({"options_eligible": False, "eligibility_evidence_current": False, "eligibility_evidence_sufficient": False}, Outcome.REVIEW_REQUIRED, ReasonCode.OPTIONS_ELIGIBILITY_EVIDENCE_STALE, RequiredAction.HUMAN_REVIEW),
            ({"options_eligible": False, "eligibility_evidence_sufficient": False}, Outcome.REVIEW_REQUIRED, ReasonCode.OPTIONS_ELIGIBILITY_EVIDENCE_INSUFFICIENT, RequiredAction.HUMAN_REVIEW),
            ({}, Outcome.ELIGIBLE, ReasonCode.OPTIONS_ELIGIBLE, RequiredAction.NONE),
            ({"options_eligible": False}, Outcome.REVIEW_REQUIRED, ReasonCode.OPTIONS_ELIGIBILITY_UNRESOLVED, RequiredAction.GOVERNANCE_REVIEW),
        ]
        for changes, outcome, reason, action in cases:
            with self.subTest(reason=reason):
                self.assert_decision(self.request(**changes), outcome, reason, action)

    def test_posture_and_undefined_precedence(self) -> None:
        self.assert_decision(self.request(options_excluded=True, options_restricted=True), Outcome.REVIEW_REQUIRED, ReasonCode.OPTIONS_ELIGIBLE_EXCLUDED_CONFLICT, RequiredAction.GOVERNANCE_REVIEW)
        self.assert_decision(self.request(options_eligible=False, options_excluded=True, options_restricted=True), Outcome.EXCLUDED, ReasonCode.OPTIONS_EXCLUDED, RequiredAction.NONE)
        witnesses = [
            {"eligibility_evidence_present": False, "eligibility_evidence_current": True, "eligibility_evidence_sufficient": False},
            {"eligibility_evidence_present": False, "eligibility_evidence_current": False, "eligibility_evidence_sufficient": True},
            {"eligibility_evidence_present": True, "eligibility_evidence_current": False, "eligibility_evidence_sufficient": True},
        ]
        for witness in witnesses:
            with self.subTest(witness=witness):
                self.assert_decision(self.request(options_eligible=False, **witness), Outcome.REVIEW_REQUIRED, ReasonCode.UNDEFINED_INPUT_COMBINATION, RequiredAction.GOVERNANCE_REVIEW)

    def test_exclusion_and_restriction_precede_lower_branches(self) -> None:
        lower = {
            "authority_evidence": self.authority(validity=Validity.INVALID),
            "eligibility_evidence_present": False,
            "eligibility_evidence_current": False,
            "eligibility_evidence_sufficient": False,
            "options_eligible": False,
        }
        self.assert_decision(self.request(options_excluded=True, **lower), Outcome.EXCLUDED, ReasonCode.OPTIONS_EXCLUDED, RequiredAction.NONE)
        self.assert_decision(self.request(options_restricted=True, **lower), Outcome.RESTRICTED, ReasonCode.OPTIONS_RESTRICTED, RequiredAction.HUMAN_REVIEW)

    def test_all_fourteen_authority_subprecedence_collisions(self) -> None:
        cases = [
            ({"contradictory": True, "validity": Validity.AMBIGUOUS}, ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            ({"contradictory": True, "validity": Validity.INVALID}, ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            ({"contradictory": True, "revoked": True}, ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            ({"contradictory": True, "current": False}, ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            ({"contradictory": True, "in_scope": False}, ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            ({"validity": Validity.AMBIGUOUS, "revoked": True}, ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            ({"validity": Validity.AMBIGUOUS, "current": False}, ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            ({"validity": Validity.AMBIGUOUS, "in_scope": False}, ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            ({"validity": Validity.INVALID, "revoked": True}, ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            ({"validity": Validity.INVALID, "current": False}, ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            ({"validity": Validity.INVALID, "in_scope": False}, ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            ({"revoked": True, "current": False}, ReasonCode.AUTHORITY_EVIDENCE_REVOKED),
            ({"revoked": True, "in_scope": False}, ReasonCode.AUTHORITY_EVIDENCE_REVOKED),
            ({"current": False, "in_scope": False}, ReasonCode.AUTHORITY_EVIDENCE_STALE),
        ]
        for facts, reason in cases:
            with self.subTest(facts=facts):
                self.assert_decision(self.request(options_eligible=False, authority_evidence=self.authority(**facts)), Outcome.REVIEW_REQUIRED, reason, RequiredAction.GOVERNANCE_REVIEW)

    def test_absent_and_valid_authority_continue(self) -> None:
        self.assert_decision(self.request(), Outcome.ELIGIBLE, ReasonCode.OPTIONS_ELIGIBLE, RequiredAction.NONE)
        self.assert_decision(self.request(authority_evidence=self.authority()), Outcome.ELIGIBLE, ReasonCode.OPTIONS_ELIGIBLE, RequiredAction.NONE)

    def test_reference_preservation_non_mutation_and_repetition(self) -> None:
        authority = self.authority()
        request = self.request(authority_evidence=authority)
        request_before = dataclasses.asdict(request)
        authority_before = dataclasses.asdict(authority)
        first = evaluate(request)
        second = evaluate(request)
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        self.assertEqual(dataclasses.asdict(request), request_before)
        self.assertEqual(dataclasses.asdict(authority), authority_before)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            request.options_eligible = False

    def test_production_import_and_capability_boundary(self) -> None:
        path = Path("src/sniperbot/options/eligibility_decision.py")
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                imports.append((node.module, tuple(alias.name for alias in node.names)))
            elif isinstance(node, ast.Import):
                self.fail("plain imports are prohibited")
        self.assertEqual(imports, [
            ("__future__", ("annotations",)),
            ("dataclasses", ("dataclass",)),
            ("enum", ("Enum",)),
        ])
        source = path.read_text(encoding="utf-8").lower()
        for token in ("open(", "getenv", "subprocess", "socket", "requests", "logging", "random", "datetime", "time.", "broker", "create_order", "submit_order", "wallet", "option_chain"):
            with self.subTest(token=token):
                self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
