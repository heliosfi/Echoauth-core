import unittest
from dataclasses import FrozenInstanceError, asdict

from sniperbot.rollback.fallback_decision import (
    AuthorityEvidence, Context, Decision, EmittableReasonCode, Outcome,
    ReasonCode, RequiredAction, RollbackRequest, State, create_request, evaluate,
)


def make(**overrides):
    values = dict(current_condition_reference="condition-1", rollback_required=False,
                  rollback_available=False, rollback_evidence_present=True,
                  rollback_evidence_current=True, rollback_evidence_sufficient=True,
                  rollback_evidence_contradictory=False, no_action=False,
                  correlation_reference="corr-1")
    values.update(overrides)
    return RollbackRequest(**values)


def authority(**overrides):
    values = dict(validity="VALID", currentness="CURRENT",
                  revocation="NON_REVOKED", scope="IN_SCOPE",
                  evidence_reference="auth-1")
    values.update(overrides)
    return AuthorityEvidence(**values)


class RollbackNoActionFallbackTests(unittest.TestCase):
    def test_closed_vocabularies_and_schema_boundary(self):
        self.assertEqual(len(Outcome), 2)
        self.assertEqual(len(ReasonCode), 14)
        self.assertEqual(len(EmittableReasonCode), 13)
        self.assertIn(ReasonCode.UNKNOWN_CONDITION, ReasonCode)
        self.assertNotIn(ReasonCode.UNKNOWN_CONDITION, EmittableReasonCode)
        self.assertEqual(len(RequiredAction), 5)
        self.assertEqual(len({RequiredAction.NONE, RequiredAction.HUMAN_REVIEW, RequiredAction.GOVERNANCE_REVIEW}), 3)
        self.assertEqual(len(State), 6)
        with self.assertRaises(ValueError):
            Decision(Outcome.NO_ACTION, ReasonCode.UNKNOWN_CONDITION, RequiredAction.NONE, "c")
        for action in (RequiredAction.FOUNDER_AUTHORITY_REQUIRED, RequiredAction.RESET_REQUIRED):
            with self.assertRaises(ValueError):
                Decision(Outcome.NO_ACTION, ReasonCode.NO_ACTION_REQUIRED, action, "c")

    def test_all_first_match_branches(self):
        cases = [
            (dict(rollback_evidence_contradictory=True), Outcome.NO_ACTION, ReasonCode.ROLLBACK_EVIDENCE_CONTRADICTORY, RequiredAction.HUMAN_REVIEW),
            (dict(rollback_required=True, no_action=True), Outcome.NO_ACTION, ReasonCode.ROLLBACK_AND_NO_ACTION_CONFLICT, RequiredAction.GOVERNANCE_REVIEW),
            (dict(rollback_evidence_present=False, rollback_evidence_current=True), Outcome.NO_ACTION, ReasonCode.UNDEFINED_INPUT_COMBINATION, RequiredAction.GOVERNANCE_REVIEW),
            (dict(rollback_evidence_present=False, rollback_evidence_sufficient=True), Outcome.NO_ACTION, ReasonCode.UNDEFINED_INPUT_COMBINATION, RequiredAction.GOVERNANCE_REVIEW),
            (dict(rollback_evidence_current=False, rollback_evidence_sufficient=True), Outcome.NO_ACTION, ReasonCode.UNDEFINED_INPUT_COMBINATION, RequiredAction.GOVERNANCE_REVIEW),
            (dict(authority_evidence=authority(validity="INVALID")), Outcome.NO_ACTION, ReasonCode.AUTHORITY_EVIDENCE_INVALID, RequiredAction.GOVERNANCE_REVIEW),
            (dict(rollback_evidence_present=False, rollback_evidence_current=False, rollback_evidence_sufficient=False), Outcome.DEFER, ReasonCode.ROLLBACK_EVIDENCE_MISSING, RequiredAction.HUMAN_REVIEW),
            (dict(rollback_evidence_current=False, rollback_evidence_sufficient=True), Outcome.NO_ACTION, ReasonCode.UNDEFINED_INPUT_COMBINATION, RequiredAction.GOVERNANCE_REVIEW),
            (dict(rollback_evidence_current=False, rollback_evidence_sufficient=False), Outcome.DEFER, ReasonCode.ROLLBACK_EVIDENCE_STALE, RequiredAction.HUMAN_REVIEW),
            (dict(rollback_evidence_sufficient=False), Outcome.DEFER, ReasonCode.ROLLBACK_EVIDENCE_INSUFFICIENT, RequiredAction.HUMAN_REVIEW),
            (dict(rollback_required=True, rollback_available=False), Outcome.DEFER, ReasonCode.ROLLBACK_UNAVAILABLE, RequiredAction.HUMAN_REVIEW),
            (dict(rollback_required=True, rollback_available=True), Outcome.DEFER, ReasonCode.ROLLBACK_EXTERNALLY_REQUIRED, RequiredAction.HUMAN_REVIEW),
            (dict(no_action=True), Outcome.NO_ACTION, ReasonCode.NO_ACTION_REQUIRED, RequiredAction.NONE),
            (dict(), Outcome.NO_ACTION, ReasonCode.NO_ACTION_REQUIRED, RequiredAction.NONE),
        ]
        for overrides, outcome, reason, action in cases:
            result = evaluate(make(**overrides))
            self.assertEqual((result.outcome, result.reason_code, result.required_action), (outcome, reason, action))

    def test_precedence_collisions(self):
        lower_precedence = [
            dict(rollback_required=True, no_action=True),
            dict(rollback_evidence_present=False, rollback_evidence_current=True),
            dict(rollback_evidence_present=False, rollback_evidence_sufficient=True),
            dict(rollback_evidence_current=False, rollback_evidence_sufficient=True),
            dict(authority_evidence=authority(validity="INVALID")),
            dict(rollback_evidence_present=False, rollback_evidence_current=False, rollback_evidence_sufficient=False),
            dict(rollback_evidence_current=False, rollback_evidence_sufficient=False),
            dict(rollback_evidence_sufficient=False),
            dict(rollback_required=True, rollback_available=False),
            dict(rollback_required=True, rollback_available=True),
            dict(no_action=True),
            dict(),
        ]
        for overrides in lower_precedence:
            with self.subTest(overrides=overrides):
                result = evaluate(make(rollback_evidence_contradictory=True, **overrides))
                self.assertEqual((result.outcome, result.reason_code, result.required_action),
                                 (Outcome.NO_ACTION, ReasonCode.ROLLBACK_EVIDENCE_CONTRADICTORY,
                                  RequiredAction.HUMAN_REVIEW))

        result = evaluate(make(rollback_required=True, no_action=True,
                               rollback_evidence_present=False,
                               rollback_evidence_current=True,
                               rollback_evidence_sufficient=False))
        self.assertEqual((result.outcome, result.reason_code, result.required_action),
                         (Outcome.NO_ACTION, ReasonCode.ROLLBACK_AND_NO_ACTION_CONFLICT,
                          RequiredAction.GOVERNANCE_REVIEW))

        undefined = dict(rollback_evidence_present=False,
                         rollback_evidence_current=True,
                         rollback_evidence_sufficient=False)
        for extra in (dict(authority_evidence=authority(validity="INVALID")),
                      dict(),):
            with self.subTest(undefined_extra=extra):
                result = evaluate(make(**undefined, **extra))
                self.assertEqual((result.outcome, result.reason_code, result.required_action),
                                 (Outcome.NO_ACTION, ReasonCode.UNDEFINED_INPUT_COMBINATION,
                                  RequiredAction.GOVERNANCE_REVIEW))
        for evidence in (
            dict(rollback_evidence_present=False, rollback_evidence_current=True, rollback_evidence_sufficient=False),
            dict(rollback_evidence_present=False, rollback_evidence_current=True, rollback_evidence_sufficient=False),
            dict(rollback_evidence_present=False, rollback_evidence_current=False, rollback_evidence_sufficient=True),
        ):
            result = evaluate(make(authority_evidence=authority(validity="INVALID"), **evidence))
            self.assertEqual(result.reason_code, ReasonCode.UNDEFINED_INPUT_COMBINATION)

        authority_over = [
            dict(rollback_evidence_present=False, rollback_evidence_current=False, rollback_evidence_sufficient=False),
            dict(rollback_evidence_present=True, rollback_evidence_current=False, rollback_evidence_sufficient=False),
            dict(rollback_evidence_present=True, rollback_evidence_current=True, rollback_evidence_sufficient=False),
            dict(rollback_required=True, rollback_available=False),
            dict(rollback_required=True, rollback_available=True),
            dict(no_action=True),
        ]
        for overrides in authority_over:
            with self.subTest(authority_over=overrides):
                result = evaluate(make(authority_evidence=authority(validity="INVALID"), **overrides))
                self.assertEqual((result.outcome, result.reason_code, result.required_action),
                                 (Outcome.NO_ACTION, ReasonCode.AUTHORITY_EVIDENCE_INVALID,
                                  RequiredAction.GOVERNANCE_REVIEW))

        for overrides in (
            dict(rollback_evidence_present=False, rollback_evidence_current=False, rollback_evidence_sufficient=False),
            dict(rollback_evidence_present=True, rollback_evidence_current=False, rollback_evidence_sufficient=False),
        ):
            result = evaluate(make(**overrides))
            self.assertEqual((result.outcome, result.reason_code, result.required_action),
                             (Outcome.DEFER, ReasonCode.ROLLBACK_EVIDENCE_MISSING if not overrides["rollback_evidence_present"] else ReasonCode.ROLLBACK_EVIDENCE_STALE, RequiredAction.HUMAN_REVIEW))

        for overrides, reason in (
            (dict(rollback_evidence_present=False, rollback_evidence_current=False, rollback_evidence_sufficient=False), ReasonCode.ROLLBACK_EVIDENCE_MISSING),
            (dict(rollback_evidence_present=True, rollback_evidence_current=False, rollback_evidence_sufficient=False), ReasonCode.ROLLBACK_EVIDENCE_STALE),
        ):
            result = evaluate(make(**overrides))
            self.assertEqual((result.outcome, result.reason_code, result.required_action),
                             (Outcome.DEFER, reason, RequiredAction.HUMAN_REVIEW))

        result = evaluate(make(rollback_evidence_present=True, rollback_evidence_current=True,
                               rollback_evidence_sufficient=False))
        self.assertEqual((result.outcome, result.reason_code, result.required_action),
                         (Outcome.DEFER, ReasonCode.ROLLBACK_EVIDENCE_INSUFFICIENT,
                          RequiredAction.HUMAN_REVIEW))

        result = evaluate(make(rollback_required=True, rollback_available=False))
        self.assertEqual((result.outcome, result.reason_code, result.required_action),
                         (Outcome.DEFER, ReasonCode.ROLLBACK_UNAVAILABLE,
                          RequiredAction.HUMAN_REVIEW))

    def test_missing_stale_insufficient_ordering(self):
        for overrides in (
            dict(rollback_evidence_present=False, rollback_evidence_current=False, rollback_evidence_sufficient=False),
            dict(rollback_evidence_present=False, rollback_evidence_current=False, rollback_evidence_sufficient=False),
            dict(rollback_evidence_present=False, rollback_evidence_current=False, rollback_evidence_sufficient=False),
        ):
            result = evaluate(make(**overrides))
            self.assertEqual((result.outcome, result.reason_code, result.required_action),
                             (Outcome.DEFER, ReasonCode.ROLLBACK_EVIDENCE_MISSING, RequiredAction.HUMAN_REVIEW))
        result = evaluate(make(rollback_evidence_present=True, rollback_evidence_current=False,
                               rollback_evidence_sufficient=False))
        self.assertEqual((result.outcome, result.reason_code, result.required_action),
                         (Outcome.DEFER, ReasonCode.ROLLBACK_EVIDENCE_STALE, RequiredAction.HUMAN_REVIEW))

    def test_authority_subprecedence(self):
        for overrides, reason in [
            (dict(validity="AMBIGUOUS", revocation="REVOKED", currentness="STALE", scope="OUT_OF_SCOPE"), ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            (dict(validity="INVALID", revocation="REVOKED", currentness="STALE", scope="OUT_OF_SCOPE"), ReasonCode.AUTHORITY_EVIDENCE_INVALID),
            (dict(revocation="REVOKED", currentness="STALE", scope="OUT_OF_SCOPE"), ReasonCode.AUTHORITY_EVIDENCE_REVOKED),
            (dict(currentness="STALE", scope="OUT_OF_SCOPE"), ReasonCode.AUTHORITY_EVIDENCE_STALE),
            (dict(scope="OUT_OF_SCOPE"), ReasonCode.AUTHORITY_EVIDENCE_OUT_OF_SCOPE),
        ]:
            self.assertEqual(evaluate(make(authority_evidence=authority(**overrides))).reason_code, reason)

    def test_context_is_opaque_and_all_states_are_non_decisional(self):
        baseline = evaluate(make())
        for state in State:
            result = evaluate(make(fsm_state_reference=state, halt_context=True, failure_context=True, recovery_context=True, reset_context=True))
            self.assertEqual(result, baseline)
        self.assertEqual(Context(State.PAUSE).fsm_state_reference, State.PAUSE)

    def test_raw_boundary_correlation_immutability_and_determinism(self):
        with self.assertRaises(ValueError):
            create_request(**{**make().__dict__, "fsm_state_reference": "UNKNOWN"})
        request = make(fsm_state_reference=State.READY)
        first, second = evaluate(request), evaluate(request)
        self.assertEqual(first, second)
        self.assertEqual(first.correlation_reference, request.correlation_reference)
        with self.assertRaises(FrozenInstanceError):
            request.correlation_reference = "changed"
        with self.assertRaises(FrozenInstanceError):
            first.reason_code = ReasonCode.NO_ACTION_REQUIRED

    def test_evaluation_does_not_mutate_supplied_objects(self):
        context = Context(State.IN_TRADE, True, False, True, False)
        evidence = authority()
        request = make(authority_evidence=evidence,
                       fsm_state_reference=context.fsm_state_reference,
                       halt_context=context.halt_context,
                       failure_context=context.failure_context,
                       recovery_context=context.recovery_context,
                       reset_context=context.reset_context)
        request_before = asdict(request)
        evidence_before = asdict(evidence)
        context_before = asdict(context)
        result = evaluate(request)
        self.assertIsNot(result, request)
        self.assertEqual(asdict(request), request_before)
        self.assertEqual(asdict(evidence), evidence_before)
        self.assertEqual(asdict(context), context_before)
        self.assertEqual(result.correlation_reference, request.correlation_reference)

    def test_authority_absent_valid_and_unknown_condition_never_emitted(self):
        self.assertEqual(evaluate(make(authority_evidence=None)).reason_code, ReasonCode.NO_ACTION_REQUIRED)
        self.assertEqual(evaluate(make(authority_evidence=authority())).reason_code, ReasonCode.NO_ACTION_REQUIRED)
        for request in (make(), make(rollback_required=True, rollback_available=False)):
            self.assertNotEqual(evaluate(request).reason_code, ReasonCode.UNKNOWN_CONDITION)


if __name__ == "__main__":
    unittest.main()
