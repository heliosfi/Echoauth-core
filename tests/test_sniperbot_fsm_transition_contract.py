import inspect
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

    def test_denial_input_schema_boundary_parity(self):
        schema_path = (
            Path(__file__).resolve().parents[1]
            / "schemas"
            / "sniperbot-fsm-transition-decision.schema.json"
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        definitions = schema["$defs"]
        request_schema = definitions["TransitionRequest"]
        facts_schema = definitions["ExternalFacts"]
        authority_schema = definitions["AuthorityEvidence"]

        self.assertIn("authority_evidence", request_schema["required"])
        self.assertFalse(request_schema["additionalProperties"])
        self.assertFalse(facts_schema["additionalProperties"])
        self.assertFalse(authority_schema["additionalProperties"])
        self.assertTrue(
            all(
                facts_schema["properties"][field]["type"] == "boolean"
                for field in facts_schema["required"]
            )
        )
        self.assertEqual(
            request_schema["properties"]["correlation_reference"]["minLength"],
            1,
        )
        self.assertEqual(
            authority_schema["properties"]["authority_reference"]["minLength"],
            1,
        )

        conditional_text = json.dumps(schema["allOf"], sort_keys=True)
        self.assertNotIn("#/$defs/ValidAuthorityEvidence", conditional_text)
        self.assertEqual(conditional_text.count("#/$defs/AuthorityEvidence"), 2)
        for affirmative_input_constraint in (
            '"readiness_preconditions_satisfied": {"const": true}',
            '"confirmed_position_exists": {"const": true}',
            '"cooldown_complete": {"const": true}',
        ):
            self.assertNotIn(affirmative_input_constraint, conditional_text)

    def test_null_authority_schema_parity(self):
        schema_path = (
            Path(__file__).resolve().parents[1]
            / "schemas"
            / "sniperbot-fsm-transition-decision.schema.json"
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        request_schema = schema["$defs"]["TransitionRequest"]
        authority_property = request_schema["properties"]["authority_evidence"]

        self.assertIn("authority_evidence", request_schema["required"])
        self.assertEqual(
            authority_property["oneOf"],
            [
                {"$ref": "#/$defs/AuthorityEvidence"},
                {"type": "null"},
            ],
        )
        conditional_text = json.dumps(schema["allOf"], sort_keys=True)
        self.assertEqual(conditional_text.count("#/$defs/AuthorityEvidence"), 2)

    def test_authority_omission_and_explicit_none_are_distinct(self):
        parameter = inspect.signature(TransitionRequest).parameters[
            "authority_evidence"
        ]
        self.assertIs(parameter.default, inspect.Parameter.empty)

        with self.assertRaises(TypeError):
            TransitionRequest(
                State.PAUSE,
                State.READY,
                TransitionRequestName.PAUSE_TO_READY,
                "corr-1",
                facts(readiness_preconditions_satisfied=True),
            )

        allowed = evaluate_transition(
            TransitionRequest(
                State.PAUSE,
                State.READY,
                TransitionRequestName.PAUSE_TO_READY,
                "allowed-null-ref",
                facts(readiness_preconditions_satisfied=True),
                None,
            )
        )
        denied = evaluate_transition(
            TransitionRequest(
                State.PAUSE,
                State.READY,
                TransitionRequestName.PAUSE_TO_READY,
                "denied-null-ref",
                facts(readiness_preconditions_satisfied=False),
                None,
            )
        )
        self.assertTrue(allowed.allowed)
        self.assertEqual(allowed.reason_code, ReasonCode.ALLOWED)
        self.assertEqual(allowed.correlation_reference, "allowed-null-ref")
        self.assertFalse(denied.allowed)
        self.assertEqual(denied.reason_code, ReasonCode.READINESS_FACTS_MISSING)
        self.assertEqual(
            denied.required_next_human_or_governance_action,
            RequiredAction.GOVERNANCE_REVIEW,
        )
        self.assertEqual(denied.correlation_reference, "denied-null-ref")

    def test_explicit_none_rejected_before_authority_required_evaluation(self):
        cases = (
            TransitionRequest(
                State.READY,
                State.ARMED_MANUAL,
                TransitionRequestName.READY_TO_ARMED_MANUAL,
                "arming-null-ref",
                facts(),
                None,
            ),
            TransitionRequest(
                State.LOCKOUT,
                State.PAUSE,
                TransitionRequestName.LOCKOUT_TO_PAUSE,
                "reset-null-ref",
                facts(reset_facts_explicit=True),
                None,
            ),
            TransitionRequest(
                State.READY,
                State.ARMED_MANUAL,
                TransitionRequestName.READY_TO_ARMED_MANUAL,
                "lockout-null-ref",
                facts(lockout_required=True),
                None,
            ),
        )
        for value in cases:
            with self.subTest(reference=value.correlation_reference):
                with self.assertRaises(ValueError):
                    evaluate_transition(value)

    def assert_denial(self, value, reason, action):
        first = evaluate_transition(value)
        second = evaluate_transition(value)
        self.assertIsInstance(first, TransitionDecision)
        self.assertFalse(first.allowed)
        self.assertEqual(first.resulting_state, value.current_state)
        self.assertEqual(first.reason_code, reason)
        self.assertEqual(first.required_next_human_or_governance_action, action)
        self.assertEqual(first.correlation_reference, value.correlation_reference)
        self.assertEqual(first, second)

    def test_governed_prerequisite_negative_conditions(self):
        cases = (
            (
                request(
                    State.PAUSE,
                    State.READY,
                    TransitionRequestName.PAUSE_TO_READY,
                    readiness_preconditions_satisfied=False,
                ),
                ReasonCode.READINESS_FACTS_MISSING,
            ),
            (
                request(
                    State.ARMED_AUTO,
                    State.IN_TRADE,
                    TransitionRequestName.ARMED_AUTO_TO_IN_TRADE,
                    confirmed_position_exists=False,
                ),
                ReasonCode.CONFIRMED_POSITION_FACT_MISSING,
            ),
            (
                request(
                    State.IN_TRADE,
                    State.PAUSE,
                    TransitionRequestName.IN_TRADE_TO_PAUSE,
                    position_closed=False,
                    cooldown_complete=True,
                ),
                ReasonCode.POSITION_CLOSED_FACT_MISSING,
            ),
            (
                request(
                    State.IN_TRADE,
                    State.PAUSE,
                    TransitionRequestName.IN_TRADE_TO_PAUSE,
                    position_closed=True,
                    cooldown_complete=False,
                ),
                ReasonCode.COOLDOWN_FACT_MISSING,
            ),
        )
        for value, reason in cases:
            with self.subTest(reason=reason):
                self.assert_denial(value, reason, RequiredAction.GOVERNANCE_REVIEW)

    def test_governed_individual_authority_failure_conditions(self):
        authority_cases = (
            ({"presence": "ABSENT"}, ReasonCode.AUTHORITY_MISSING),
            ({"currentness": "STALE"}, ReasonCode.AUTHORITY_STALE),
            ({"revocation": "REVOKED"}, ReasonCode.AUTHORITY_REVOKED),
            ({"validity_outcome": "OUT_OF_SCOPE"}, ReasonCode.AUTHORITY_OUT_OF_SCOPE),
            ({"validity_outcome": "INVALID"}, ReasonCode.AUTHORITY_INVALID),
            ({"validity_outcome": "AMBIGUOUS"}, ReasonCode.AUTHORITY_INVALID),
        )
        for overrides, reason in authority_cases:
            evidence = authority(**overrides)
            arming = TransitionRequest(
                State.READY,
                State.ARMED_MANUAL,
                TransitionRequestName.READY_TO_ARMED_MANUAL,
                "arming-ref",
                facts(),
                evidence,
            )
            reset = TransitionRequest(
                State.LOCKOUT,
                State.PAUSE,
                TransitionRequestName.LOCKOUT_TO_PAUSE,
                "reset-ref",
                facts(reset_facts_explicit=True),
                evidence,
            )
            arming_reason = reason
            reset_reason = (
                ReasonCode.RESET_EVIDENCE_MISSING
                if reason is ReasonCode.AUTHORITY_MISSING
                else reason
            )
            arming_action = (
                RequiredAction.GOVERNANCE_REVIEW
                if reason is ReasonCode.AUTHORITY_OUT_OF_SCOPE
                else RequiredAction.FOUNDER_AUTHORITY_REQUIRED
            )
            with self.subTest(context="arming", overrides=overrides):
                self.assert_denial(arming, arming_reason, arming_action)
            with self.subTest(context="reset", overrides=overrides):
                self.assert_denial(reset, reset_reason, RequiredAction.RESET_REQUIRED)

    def test_wrong_runtime_types_and_unsupported_shapes_are_rejected(self):
        valid = request(
            State.PAUSE,
            State.READY,
            TransitionRequestName.PAUSE_TO_READY,
            readiness_preconditions_satisfied=True,
        )
        with self.assertRaises(TypeError):
            evaluate_transition(object())
        with self.assertRaises(TypeError):
            evaluate_transition(replace(valid, current_state="PAUSE"))
        with self.assertRaises(TypeError):
            evaluate_transition(replace(valid, requested_state="READY"))
        with self.assertRaises(TypeError):
            evaluate_transition(replace(valid, transition_request="PAUSE_TO_READY"))
        with self.assertRaises(TypeError):
            evaluate_transition(replace(valid, external_facts={}))
        with self.assertRaises(TypeError):
            evaluate_transition(replace(valid, authority_evidence={}))

    def test_external_fact_types_are_strict_booleans(self):
        field_names = (
            "readiness_preconditions_satisfied",
            "confirmed_position_exists",
            "position_closed",
            "cooldown_complete",
            "lockout_required",
            "logging_failure_indicated",
            "reset_facts_explicit",
        )
        for field_name in field_names:
            invalid_facts = replace(facts(), **{field_name: 1})
            value = TransitionRequest(
                State.PAUSE,
                State.READY,
                TransitionRequestName.PAUSE_TO_READY,
                "corr-1",
                invalid_facts,
                authority(),
            )
            with self.subTest(field=field_name), self.assertRaises(TypeError):
                evaluate_transition(value)

    def test_unknown_authority_vocabulary_values_are_rejected(self):
        fields = (
            "presence",
            "currentness",
            "revocation",
            "validity_outcome",
        )
        for field_name in fields:
            evidence = authority(**{field_name: "UNKNOWN"})
            value = TransitionRequest(
                State.READY,
                State.ARMED_MANUAL,
                TransitionRequestName.READY_TO_ARMED_MANUAL,
                "corr-1",
                facts(),
                evidence,
            )
            with self.subTest(field=field_name), self.assertRaises(ValueError):
                evaluate_transition(value)
        with self.assertRaises(ValueError):
            State("UNKNOWN")
        with self.assertRaises(ValueError):
            TransitionRequestName("UNKNOWN")

    def test_invalid_references_and_authority_field_types_are_rejected(self):
        valid = request(
            State.PAUSE,
            State.READY,
            TransitionRequestName.PAUSE_TO_READY,
            readiness_preconditions_satisfied=True,
        )
        with self.assertRaises(ValueError):
            evaluate_transition(replace(valid, correlation_reference=""))
        with self.assertRaises(TypeError):
            evaluate_transition(replace(valid, correlation_reference=1))
        for field_name in (
            "presence",
            "subject_scope",
            "currentness",
            "revocation",
            "validity_outcome",
            "authority_reference",
        ):
            evidence = authority(**{field_name: 1})
            with self.subTest(field=field_name), self.assertRaises(TypeError):
                evaluate_transition(replace(valid, authority_evidence=evidence))
        for field_name in ("subject_scope", "authority_reference"):
            evidence = authority(**{field_name: ""})
            with self.subTest(field=field_name), self.assertRaises(ValueError):
                evaluate_transition(replace(valid, authority_evidence=evidence))

    def test_prohibited_constructor_fields_are_rejected(self):
        with self.assertRaises(TypeError):
            TransitionRequest(
                State.PAUSE,
                State.READY,
                TransitionRequestName.PAUSE_TO_READY,
                "corr-1",
                facts(),
                authority(),
                prohibited=True,
            )
        with self.assertRaises(TypeError):
            ExternalFacts(
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                prohibited=True,
            )
        with self.assertRaises(TypeError):
            AuthorityEvidence(
                "PRESENT",
                "sniperbot-fsm",
                "CURRENT",
                "NON_REVOKED",
                "VALID",
                "auth-1",
                prohibited=True,
            )
        with self.assertRaises(TypeError):
            ExternalFacts()
        with self.assertRaises(TypeError):
            AuthorityEvidence()

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
        denied = evaluate_transition(TransitionRequest(State.READY, State.ARMED_MANUAL, TransitionRequestName.READY_TO_ARMED_MANUAL, "corr-1", facts(), authority(presence="ABSENT")))
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
        no = evaluate_transition(TransitionRequest(State.LOCKOUT, State.PAUSE, TransitionRequestName.LOCKOUT_TO_PAUSE, "corr-1", facts(reset_facts_explicit=True), authority(presence="ABSENT")))
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
