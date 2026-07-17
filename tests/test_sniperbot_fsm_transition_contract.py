import json
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

from sniperbot.fsm.transition_contract import (
    AuthorityEvidence, ExternalFacts, ReasonCode, RequiredAction, State,
    TransitionDecision, TransitionRequest, TransitionRequestName,
    evaluate_transition,
)


def facts(**overrides):
    values = dict(readiness_preconditions_satisfied=False, confirmed_position_exists=False,
                  position_closed=False, cooldown_complete=False, lockout_required=False,
                  logging_failure_indicated=False, reset_facts_explicit=False)
    values.update(overrides)
    return ExternalFacts(**values)


def authority(**overrides):
    values = dict(presence="PRESENT", subject_scope="sniperbot-fsm",
                  currentness="CURRENT", revocation="NON_REVOKED",
                  validity_outcome="VALID", authority_reference="auth-1")
    values.update(overrides)
    return AuthorityEvidence(**values)


def request(current, requested, name, **kwargs):
    return TransitionRequest(current, requested, name, "corr-1", facts(**kwargs), authority())


class SniperbotFsmTransitionContractTests(unittest.TestCase):
    def test_closed_vocabularies(self):
        self.assertEqual(len(State), 6)
        self.assertEqual(len(ReasonCode), 17)
        self.assertEqual(len(RequiredAction), 5)

    def test_required_action_schema_parity(self):
        schema_path = (
            Path(__file__).resolve().parents[1]
            / "schemas"
            / "sniperbot-fsm-transition-decision.schema.json"
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        required_action = schema["$defs"]["RequiredAction"]

        self.assertEqual(required_action["type"], "string")
        self.assertEqual(
            required_action["enum"],
            [action.value for action in RequiredAction],
        )
        self.assertNotIn(None, required_action["enum"])

    def test_pause_ready(self):
        result = evaluate_transition(request(State.PAUSE, State.READY, TransitionRequestName.PAUSE_TO_READY, readiness_preconditions_satisfied=True))
        self.assertTrue(result.allowed)
        self.assertEqual(result.resulting_state, State.READY)
        self.assertEqual(result.required_next_human_or_governance_action, RequiredAction.NONE)

    def test_pause_ready_missing(self):
        result = evaluate_transition(request(State.PAUSE, State.READY, TransitionRequestName.PAUSE_TO_READY))
        self.assertFalse(result.allowed)
        self.assertEqual(result.reason_code, ReasonCode.READINESS_FACTS_MISSING)

    def test_manual_arming(self):
        ok = evaluate_transition(request(State.READY, State.ARMED_MANUAL, TransitionRequestName.READY_TO_ARMED_MANUAL))
        denied = evaluate_transition(TransitionRequest(State.READY, State.ARMED_MANUAL, TransitionRequestName.READY_TO_ARMED_MANUAL, "corr-1", facts(), None))
        self.assertTrue(ok.allowed)
        self.assertEqual(denied.reason_code, ReasonCode.AUTHORITY_MISSING)

    def test_auto_arming_denied(self):
        result = evaluate_transition(request(State.READY, State.ARMED_AUTO, TransitionRequestName.READY_TO_ARMED_AUTO))
        self.assertFalse(result.allowed)
        self.assertEqual(result.reason_code, ReasonCode.TRANSITION_FOUNDER_DENIED)
        self.assertEqual(result.required_next_human_or_governance_action, RequiredAction.FOUNDER_AUTHORITY_REQUIRED)

    def test_auto_trade(self):
        ok = evaluate_transition(request(State.ARMED_AUTO, State.IN_TRADE, TransitionRequestName.ARMED_AUTO_TO_IN_TRADE, confirmed_position_exists=True))
        no = evaluate_transition(request(State.ARMED_AUTO, State.IN_TRADE, TransitionRequestName.ARMED_AUTO_TO_IN_TRADE))
        self.assertTrue(ok.allowed)
        self.assertEqual(no.reason_code, ReasonCode.CONFIRMED_POSITION_FACT_MISSING)

    def test_excluded_transitions(self):
        for current, requested, name in ((State.ARMED_MANUAL, State.IN_TRADE, TransitionRequestName.ARMED_MANUAL_TO_IN_TRADE), (State.IN_TRADE, State.READY, TransitionRequestName.IN_TRADE_TO_READY)):
            result = evaluate_transition(request(current, requested, name))
            self.assertFalse(result.allowed)
            self.assertEqual(result.resulting_state, current)

    def test_trade_pause(self):
        ok = evaluate_transition(request(State.IN_TRADE, State.PAUSE, TransitionRequestName.IN_TRADE_TO_PAUSE, position_closed=True, cooldown_complete=True))
        no = evaluate_transition(request(State.IN_TRADE, State.PAUSE, TransitionRequestName.IN_TRADE_TO_PAUSE, position_closed=True))
        self.assertTrue(ok.allowed)
        self.assertEqual(no.reason_code, ReasonCode.COOLDOWN_FACT_MISSING)

    def test_lockout_precedence_and_logging_failure(self):
        result = evaluate_transition(request(State.READY, State.ARMED_MANUAL, TransitionRequestName.READY_TO_ARMED_MANUAL, lockout_required=True, logging_failure_indicated=True))
        self.assertTrue(result.allowed)
        self.assertEqual(result.resulting_state, State.LOCKOUT)
        self.assertEqual(result.reason_code, ReasonCode.LOCKOUT_REQUIRED)

    def test_reset(self):
        ok = evaluate_transition(request(State.LOCKOUT, State.PAUSE, TransitionRequestName.LOCKOUT_TO_PAUSE, reset_facts_explicit=True))
        no = evaluate_transition(TransitionRequest(State.LOCKOUT, State.PAUSE, TransitionRequestName.LOCKOUT_TO_PAUSE, "corr-1", facts(reset_facts_explicit=True), None))
        self.assertTrue(ok.allowed)
        self.assertEqual(no.reason_code, ReasonCode.RESET_EVIDENCE_MISSING)

    def test_contradiction_unknown_and_invariants(self):
        contradictory = evaluate_transition(request(State.PAUSE, State.READY, TransitionRequestName.PAUSE_TO_READY, confirmed_position_exists=True, position_closed=True))
        self.assertEqual(contradictory.reason_code, ReasonCode.AMBIGUOUS_OR_CONTRADICTORY_INPUT)
        undefined = evaluate_transition(request(State.PAUSE, State.LOCKOUT, TransitionRequestName.PAUSE_TO_READY))
        self.assertEqual(undefined.reason_code, ReasonCode.UNDEFINED_TRANSITION)
        self.assertEqual(undefined.resulting_state, State.PAUSE)

    def test_immutable_and_deterministic(self):
        req = request(State.PAUSE, State.READY, TransitionRequestName.PAUSE_TO_READY, readiness_preconditions_satisfied=True)
        with self.assertRaises(FrozenInstanceError):
            req.correlation_reference = "changed"
        first, second = evaluate_transition(req), evaluate_transition(req)
        self.assertEqual(first, second)
        self.assertIsInstance(first, TransitionDecision)
        self.assertEqual(first.correlation_reference, req.correlation_reference)


if __name__ == "__main__":
    unittest.main()
