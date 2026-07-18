import inspect
import itertools
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

    def test_lockout_schema_semantic_parity(self):
        schema_path = (
            Path(__file__).resolve().parents[1]
            / "schemas"
            / "sniperbot-fsm-transition-decision.schema.json"
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        forced_lockout = schema["allOf"][0]["then"]["properties"]["decision"][
            "properties"
        ]
        locked_state = schema["allOf"][1]
        locked_decision = locked_state["then"]["properties"]["decision"][
            "properties"
        ]

        expected = {
            "allowed": {"const": False},
            "resulting_state": {"const": "LOCKOUT"},
            "reason_code": {"const": "LOCKOUT_REQUIRED"},
            "required_next_human_or_governance_action": {
                "const": "RESET_REQUIRED"
            },
        }
        self.assertEqual(forced_lockout, expected)
        self.assertEqual(
            {key: locked_decision[key] for key in expected},
            expected,
        )
        self.assertEqual(locked_decision["current_state"], {"const": "LOCKOUT"})
        locked_request = locked_state["if"]["properties"]["request"]
        self.assertEqual(
            locked_request["properties"]["current_state"],
            {"const": "LOCKOUT"},
        )
        self.assertEqual(
            locked_request["not"]["properties"],
            {
                "requested_state": {"const": "PAUSE"},
                "transition_request": {"const": "LOCKOUT_TO_PAUSE"},
            },
        )
        lower_reason_codes = {
            "TRANSITION_FOUNDER_DENIED",
            "UNDEFINED_TRANSITION",
        }
        guarded_lower_rules = 0
        for rule in schema["allOf"][2:]:
            decision = (
                rule.get("then", {})
                .get("properties", {})
                .get("decision", {})
                .get("properties", {})
            )
            reason = decision.get("reason_code", {}).get("const")
            if reason not in lower_reason_codes:
                continue
            guarded_lower_rules += 1
            request = rule["if"]["properties"]["request"]
            self.assertEqual(
                request["properties"]["external_facts"]["properties"][
                    "lockout_required"
                ],
                {"const": False},
            )
        self.assertEqual(guarded_lower_rules, 5)

    def test_transition_request_coherence_schema_parity(self):
        schema_path = (
            Path(__file__).resolve().parents[1]
            / "schemas"
            / "sniperbot-fsm-transition-decision.schema.json"
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        subject_rules = schema["$defs"]["CanonicalTransitionSubject"]["oneOf"]
        actual = {}
        for rule in subject_rules:
            properties = rule["properties"]
            name = properties["transition_request"]["const"]
            current = properties.get("current_state", {}).get("const")
            requested = properties["requested_state"]["const"]
            actual[name] = (current, requested)

        self.assertEqual(
            actual,
            {
                "PAUSE_TO_READY": ("PAUSE", "READY"),
                "READY_TO_ARMED_MANUAL": ("READY", "ARMED_MANUAL"),
                "READY_TO_ARMED_AUTO": ("READY", "ARMED_AUTO"),
                "ARMED_AUTO_TO_IN_TRADE": ("ARMED_AUTO", "IN_TRADE"),
                "ARMED_MANUAL_TO_IN_TRADE": ("ARMED_MANUAL", "IN_TRADE"),
                "IN_TRADE_TO_READY": ("IN_TRADE", "READY"),
                "IN_TRADE_TO_PAUSE": ("IN_TRADE", "PAUSE"),
                "ANY_TO_LOCKOUT": (None, "LOCKOUT"),
                "LOCKOUT_TO_PAUSE": ("LOCKOUT", "PAUSE"),
            },
        )

        rules_by_description = {
            rule.get("description"): rule for rule in schema["allOf"]
        }
        mismatch = rules_by_description[
            "Closed transition request identifiers with non-canonical state "
            "pairs are governed undefined transitions after higher-priority "
            "branches."
        ]
        mismatch_request = mismatch["if"]["properties"]["request"]
        self.assertEqual(
            mismatch_request["not"],
            {"$ref": "#/$defs/CanonicalTransitionSubject"},
        )
        self.assertEqual(
            mismatch_request["properties"]["current_state"],
            {"not": {"const": "LOCKOUT"}},
        )
        self.assertEqual(
            mismatch_request["properties"]["external_facts"]["properties"][
                "lockout_required"
            ],
            {"const": False},
        )
        expected_decision = {
            "allowed": {"const": False},
            "reason_code": {"const": "UNDEFINED_TRANSITION"},
            "required_next_human_or_governance_action": {
                "const": "GOVERNANCE_REVIEW"
            },
        }
        self.assertEqual(
            mismatch["then"]["properties"]["decision"]["properties"],
            expected_decision,
        )

        any_without_lockout = rules_by_description[
            "ANY_TO_LOCKOUT without an active lockout fact is a governed "
            "undefined transition outside the current lockout gate."
        ]
        any_request = any_without_lockout["if"]["properties"]["request"]
        self.assertEqual(
            any_request["properties"]["transition_request"],
            {"const": "ANY_TO_LOCKOUT"},
        )
        self.assertEqual(
            any_without_lockout["then"]["properties"]["decision"]["properties"],
            expected_decision,
        )

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
        conditional_effects = json.dumps(
            [rule.get("then", {}) for rule in schema["allOf"]],
            sort_keys=True,
        )
        for affirmative_input_constraint in (
            '"readiness_preconditions_satisfied": {"const": true}',
            '"confirmed_position_exists": {"const": true}',
            '"cooldown_complete": {"const": true}',
        ):
            self.assertNotIn(affirmative_input_constraint, conditional_effects)

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

    def test_all_25_authority_collisions_for_arming_and_reset(self):
        collisions = []
        group_counts = {"absent": 0, "stale": 0, "revoked": 0}
        for presence, currentness, revocation, validity_outcome in itertools.product(
            ("PRESENT", "ABSENT"),
            ("CURRENT", "STALE"),
            ("NON_REVOKED", "REVOKED"),
            ("VALID", "INVALID", "AMBIGUOUS", "OUT_OF_SCOPE"),
        ):
            failure_count = sum(
                (
                    presence == "ABSENT",
                    currentness == "STALE",
                    revocation == "REVOKED",
                    validity_outcome != "VALID",
                )
            )
            if failure_count < 2:
                continue

            values = {
                "presence": presence,
                "subject_scope": "sniperbot-fsm",
                "currentness": currentness,
                "revocation": revocation,
                "validity_outcome": validity_outcome,
                "authority_reference": "collision-auth-ref",
            }
            collisions.append(values)

            if presence == "ABSENT":
                group_counts["absent"] += 1
                arming_reason = ReasonCode.AUTHORITY_MISSING
                reset_reason = ReasonCode.RESET_EVIDENCE_MISSING
                arming_action = RequiredAction.FOUNDER_AUTHORITY_REQUIRED
            elif currentness == "STALE":
                group_counts["stale"] += 1
                arming_reason = reset_reason = ReasonCode.AUTHORITY_STALE
                arming_action = RequiredAction.FOUNDER_AUTHORITY_REQUIRED
            elif revocation == "REVOKED":
                group_counts["revoked"] += 1
                arming_reason = reset_reason = ReasonCode.AUTHORITY_REVOKED
                arming_action = RequiredAction.FOUNDER_AUTHORITY_REQUIRED
            elif validity_outcome == "OUT_OF_SCOPE":
                arming_reason = reset_reason = ReasonCode.AUTHORITY_OUT_OF_SCOPE
                arming_action = RequiredAction.GOVERNANCE_REVIEW
            else:
                arming_reason = reset_reason = ReasonCode.AUTHORITY_INVALID
                arming_action = RequiredAction.FOUNDER_AUTHORITY_REQUIRED

            forward_evidence = AuthorityEvidence(**values)
            reverse_evidence = AuthorityEvidence(
                **dict(reversed(tuple(values.items())))
            )
            arming = TransitionRequest(
                State.READY,
                State.ARMED_MANUAL,
                TransitionRequestName.READY_TO_ARMED_MANUAL,
                "arming-collision-ref",
                facts(),
                forward_evidence,
            )
            arming_reordered = replace(arming, authority_evidence=reverse_evidence)
            reset = TransitionRequest(
                State.LOCKOUT,
                State.PAUSE,
                TransitionRequestName.LOCKOUT_TO_PAUSE,
                "reset-collision-ref",
                facts(reset_facts_explicit=False),
                forward_evidence,
            )
            reset_reordered = replace(reset, authority_evidence=reverse_evidence)

            with self.subTest(context="arming", values=values):
                first = evaluate_transition(arming)
                second = evaluate_transition(arming)
                reordered = evaluate_transition(arming_reordered)
                self.assertFalse(first.allowed)
                self.assertEqual(first.resulting_state, State.READY)
                self.assertEqual(first.reason_code, arming_reason)
                self.assertEqual(
                    first.required_next_human_or_governance_action,
                    arming_action,
                )
                self.assertEqual(first.correlation_reference, "arming-collision-ref")
                self.assertEqual(first, second)
                self.assertIsNot(first, second)
                self.assertEqual(first, reordered)
                self.assertEqual(arming.authority_evidence, forward_evidence)

            with self.subTest(context="reset", values=values):
                first = evaluate_transition(reset)
                second = evaluate_transition(reset)
                reordered = evaluate_transition(reset_reordered)
                self.assertFalse(first.allowed)
                self.assertEqual(first.resulting_state, State.LOCKOUT)
                self.assertEqual(first.reason_code, reset_reason)
                self.assertEqual(
                    first.required_next_human_or_governance_action,
                    RequiredAction.RESET_REQUIRED,
                )
                self.assertEqual(first.correlation_reference, "reset-collision-ref")
                self.assertEqual(first, second)
                self.assertIsNot(first, second)
                self.assertEqual(first, reordered)
                self.assertEqual(reset.authority_evidence, forward_evidence)

        self.assertEqual(len(collisions), 25)
        self.assertEqual(group_counts, {"absent": 15, "stale": 7, "revoked": 3})

    def test_authority_collision_outer_precedence_is_preserved(self):
        collision = authority(presence="ABSENT", currentness="STALE")
        lockout = evaluate_transition(
            TransitionRequest(
                State.READY,
                State.ARMED_MANUAL,
                TransitionRequestName.READY_TO_ARMED_MANUAL,
                "lockout-collision-ref",
                facts(lockout_required=True),
                collision,
            )
        )
        contradiction = evaluate_transition(
            TransitionRequest(
                State.READY,
                State.ARMED_MANUAL,
                TransitionRequestName.READY_TO_ARMED_MANUAL,
                "contradiction-collision-ref",
                facts(confirmed_position_exists=True, position_closed=True),
                collision,
            )
        )

        self.assertEqual(lockout.resulting_state, State.LOCKOUT)
        self.assertEqual(lockout.reason_code, ReasonCode.LOCKOUT_REQUIRED)
        self.assertEqual(
            contradiction.reason_code,
            ReasonCode.AMBIGUOUS_OR_CONTRADICTORY_INPUT,
        )
        self.assertEqual(
            contradiction.required_next_human_or_governance_action,
            RequiredAction.HUMAN_REVIEW,
        )

    def test_all_closed_transition_request_state_pair_combinations(self):
        canonical_pairs = {
            TransitionRequestName.PAUSE_TO_READY: {(State.PAUSE, State.READY)},
            TransitionRequestName.READY_TO_ARMED_MANUAL: {
                (State.READY, State.ARMED_MANUAL)
            },
            TransitionRequestName.READY_TO_ARMED_AUTO: {
                (State.READY, State.ARMED_AUTO)
            },
            TransitionRequestName.ARMED_AUTO_TO_IN_TRADE: {
                (State.ARMED_AUTO, State.IN_TRADE)
            },
            TransitionRequestName.ARMED_MANUAL_TO_IN_TRADE: {
                (State.ARMED_MANUAL, State.IN_TRADE)
            },
            TransitionRequestName.IN_TRADE_TO_READY: {
                (State.IN_TRADE, State.READY)
            },
            TransitionRequestName.IN_TRADE_TO_PAUSE: {
                (State.IN_TRADE, State.PAUSE)
            },
            TransitionRequestName.ANY_TO_LOCKOUT: {
                (state, State.LOCKOUT) for state in State
            },
            TransitionRequestName.LOCKOUT_TO_PAUSE: {
                (State.LOCKOUT, State.PAUSE)
            },
        }
        exact_outcomes = {
            TransitionRequestName.PAUSE_TO_READY: (
                True,
                State.READY,
                ReasonCode.ALLOWED,
                RequiredAction.NONE,
            ),
            TransitionRequestName.READY_TO_ARMED_MANUAL: (
                True,
                State.ARMED_MANUAL,
                ReasonCode.ALLOWED,
                RequiredAction.NONE,
            ),
            TransitionRequestName.READY_TO_ARMED_AUTO: (
                False,
                State.READY,
                ReasonCode.TRANSITION_FOUNDER_DENIED,
                RequiredAction.FOUNDER_AUTHORITY_REQUIRED,
            ),
            TransitionRequestName.ARMED_AUTO_TO_IN_TRADE: (
                True,
                State.IN_TRADE,
                ReasonCode.ALLOWED,
                RequiredAction.NONE,
            ),
            TransitionRequestName.ARMED_MANUAL_TO_IN_TRADE: (
                False,
                State.ARMED_MANUAL,
                ReasonCode.UNDEFINED_TRANSITION,
                RequiredAction.GOVERNANCE_REVIEW,
            ),
            TransitionRequestName.IN_TRADE_TO_READY: (
                False,
                State.IN_TRADE,
                ReasonCode.UNDEFINED_TRANSITION,
                RequiredAction.GOVERNANCE_REVIEW,
            ),
            TransitionRequestName.IN_TRADE_TO_PAUSE: (
                True,
                State.PAUSE,
                ReasonCode.ALLOWED,
                RequiredAction.NONE,
            ),
            TransitionRequestName.LOCKOUT_TO_PAUSE: (
                True,
                State.PAUSE,
                ReasonCode.ALLOWED,
                RequiredAction.NONE,
            ),
        }
        exact_fact_overrides = {
            TransitionRequestName.PAUSE_TO_READY: {
                "readiness_preconditions_satisfied": True
            },
            TransitionRequestName.ARMED_AUTO_TO_IN_TRADE: {
                "confirmed_position_exists": True
            },
            TransitionRequestName.IN_TRADE_TO_PAUSE: {
                "position_closed": True,
                "cooldown_complete": True,
            },
            TransitionRequestName.LOCKOUT_TO_PAUSE: {
                "reset_facts_explicit": True
            },
        }
        counts = {
            "canonical": 0,
            "mismatched": 0,
            "undefined_mismatch": 0,
            "locked_mismatch": 0,
        }

        for current, requested, transition_name in itertools.product(
            tuple(State), tuple(State), tuple(TransitionRequestName)
        ):
            canonical = (current, requested) in canonical_pairs[transition_name]
            counts["canonical" if canonical else "mismatched"] += 1
            evidence = (
                authority()
                if canonical
                else authority(presence="ABSENT", currentness="STALE")
            )
            value = TransitionRequest(
                current,
                requested,
                transition_name,
                "coherence-matrix-ref",
                facts(**(exact_fact_overrides.get(transition_name, {}) if canonical else {})),
                evidence,
            )
            facts_before = value.external_facts
            evidence_before = value.authority_evidence
            first = evaluate_transition(value)
            second = evaluate_transition(value)

            if current is State.LOCKOUT:
                if (
                    requested is State.PAUSE
                    and transition_name is TransitionRequestName.LOCKOUT_TO_PAUSE
                ):
                    expected = exact_outcomes[transition_name]
                else:
                    expected = (
                        False,
                        State.LOCKOUT,
                        ReasonCode.LOCKOUT_REQUIRED,
                        RequiredAction.RESET_REQUIRED,
                    )
                    if not canonical:
                        counts["locked_mismatch"] += 1
            elif not canonical:
                expected = (
                    False,
                    current,
                    ReasonCode.UNDEFINED_TRANSITION,
                    RequiredAction.GOVERNANCE_REVIEW,
                )
                counts["undefined_mismatch"] += 1
            elif transition_name is TransitionRequestName.ANY_TO_LOCKOUT:
                expected = (
                    False,
                    current,
                    ReasonCode.UNDEFINED_TRANSITION,
                    RequiredAction.GOVERNANCE_REVIEW,
                )
            else:
                expected = exact_outcomes[transition_name]

            with self.subTest(
                current=current,
                requested=requested,
                transition_name=transition_name,
            ):
                self.assertEqual(
                    (
                        first.allowed,
                        first.resulting_state,
                        first.reason_code,
                        first.required_next_human_or_governance_action,
                    ),
                    expected,
                )
                self.assertEqual(first.current_state, current)
                self.assertEqual(first.requested_state, requested)
                self.assertEqual(
                    first.correlation_reference,
                    "coherence-matrix-ref",
                )
                self.assertEqual(first, second)
                self.assertIsNot(first, second)
                self.assertIs(value.external_facts, facts_before)
                self.assertIs(value.authority_evidence, evidence_before)

        self.assertEqual(
            counts,
            {
                "canonical": 14,
                "mismatched": 310,
                "undefined_mismatch": 258,
                "locked_mismatch": 52,
            },
        )

    def test_all_32_formerly_allowed_mismatches_are_governed_denials(self):
        formerly_allowed = (
            (
                State.PAUSE,
                State.READY,
                TransitionRequestName.PAUSE_TO_READY,
                {"readiness_preconditions_satisfied": True},
            ),
            (
                State.READY,
                State.ARMED_MANUAL,
                TransitionRequestName.READY_TO_ARMED_MANUAL,
                {},
            ),
            (
                State.ARMED_AUTO,
                State.IN_TRADE,
                TransitionRequestName.ARMED_AUTO_TO_IN_TRADE,
                {"confirmed_position_exists": True},
            ),
            (
                State.IN_TRADE,
                State.PAUSE,
                TransitionRequestName.IN_TRADE_TO_PAUSE,
                {"position_closed": True, "cooldown_complete": True},
            ),
        )
        checked = 0
        for current, requested, canonical_name, fact_values in formerly_allowed:
            for supplied_name in TransitionRequestName:
                if supplied_name is canonical_name:
                    continue
                value = TransitionRequest(
                    current,
                    requested,
                    supplied_name,
                    "formerly-allowed-ref",
                    facts(**fact_values),
                    authority(),
                )
                decision = evaluate_transition(value)
                with self.subTest(
                    current=current,
                    requested=requested,
                    supplied_name=supplied_name,
                ):
                    self.assertFalse(decision.allowed)
                    self.assertEqual(decision.resulting_state, current)
                    self.assertEqual(
                        decision.reason_code,
                        ReasonCode.UNDEFINED_TRANSITION,
                    )
                    self.assertEqual(
                        decision.required_next_human_or_governance_action,
                        RequiredAction.GOVERNANCE_REVIEW,
                    )
                    self.assertEqual(
                        decision.correlation_reference,
                        "formerly-allowed-ref",
                    )
                checked += 1
        self.assertEqual(checked, 32)

    def test_transition_request_coherence_precedence(self):
        mismatch_with_failed_prerequisite = TransitionRequest(
            State.PAUSE,
            State.READY,
            TransitionRequestName.READY_TO_ARMED_MANUAL,
            "prerequisite-ref",
            facts(readiness_preconditions_satisfied=False),
            authority(),
        )
        mismatch_with_authority_collision = TransitionRequest(
            State.READY,
            State.ARMED_MANUAL,
            TransitionRequestName.PAUSE_TO_READY,
            "authority-ref",
            facts(),
            authority(presence="ABSENT", currentness="STALE"),
        )
        mismatch_with_contradiction = replace(
            mismatch_with_failed_prerequisite,
            correlation_reference="contradiction-ref",
            external_facts=facts(
                confirmed_position_exists=True,
                position_closed=True,
            ),
        )
        mismatch_with_forced_lockout = replace(
            mismatch_with_failed_prerequisite,
            correlation_reference="forced-ref",
            external_facts=facts(lockout_required=True),
        )

        for value in (
            mismatch_with_failed_prerequisite,
            mismatch_with_authority_collision,
        ):
            decision = evaluate_transition(value)
            self.assertEqual(decision.reason_code, ReasonCode.UNDEFINED_TRANSITION)
            self.assertEqual(
                decision.required_next_human_or_governance_action,
                RequiredAction.GOVERNANCE_REVIEW,
            )
        contradiction = evaluate_transition(mismatch_with_contradiction)
        self.assertEqual(
            contradiction.reason_code,
            ReasonCode.AMBIGUOUS_OR_CONTRADICTORY_INPUT,
        )
        forced = evaluate_transition(mismatch_with_forced_lockout)
        self.assertEqual(forced.reason_code, ReasonCode.LOCKOUT_REQUIRED)
        self.assertEqual(forced.resulting_state, State.LOCKOUT)

        with self.assertRaises(TypeError):
            evaluate_transition(
                replace(
                    mismatch_with_forced_lockout,
                    transition_request="READY_TO_ARMED_MANUAL",
                )
            )

    def test_forced_lockout_is_absolute_across_closed_request_identifiers(self):
        for current, requested, transition_name in itertools.product(
            tuple(State), tuple(State), tuple(TransitionRequestName)
        ):
            value = TransitionRequest(
                current,
                requested,
                transition_name,
                "forced-lockout-ref",
                facts(lockout_required=True),
                authority(),
            )
            with self.subTest(
                current=current,
                requested=requested,
                transition_name=transition_name,
            ):
                first = evaluate_transition(value)
                second = evaluate_transition(value)
                self.assertEqual(first.current_state, current)
                self.assertEqual(first.requested_state, requested)
                self.assertFalse(first.allowed)
                self.assertEqual(first.resulting_state, State.LOCKOUT)
                self.assertEqual(first.reason_code, ReasonCode.LOCKOUT_REQUIRED)
                self.assertEqual(
                    first.required_next_human_or_governance_action,
                    RequiredAction.RESET_REQUIRED,
                )
                self.assertEqual(first.correlation_reference, "forced-lockout-ref")
                self.assertEqual(first, second)
                self.assertIsNot(first, second)
                self.assertEqual(value.external_facts, facts(lockout_required=True))

        contradiction = evaluate_transition(
            TransitionRequest(
                State.READY,
                State.ARMED_MANUAL,
                TransitionRequestName.READY_TO_ARMED_MANUAL,
                "forced-contradiction-ref",
                facts(
                    lockout_required=True,
                    confirmed_position_exists=True,
                    position_closed=True,
                ),
                authority(presence="ABSENT", currentness="STALE"),
            )
        )
        self.assertEqual(contradiction.reason_code, ReasonCode.LOCKOUT_REQUIRED)
        self.assertEqual(contradiction.resulting_state, State.LOCKOUT)

    def test_only_exact_governed_reset_path_can_exit_lockout(self):
        for requested, transition_name in itertools.product(
            tuple(State), tuple(TransitionRequestName)
        ):
            if (
                requested is State.PAUSE
                and transition_name is TransitionRequestName.LOCKOUT_TO_PAUSE
            ):
                continue
            value = TransitionRequest(
                State.LOCKOUT,
                requested,
                transition_name,
                "locked-denial-ref",
                facts(reset_facts_explicit=True),
                authority(),
            )
            with self.subTest(requested=requested, transition_name=transition_name):
                decision = evaluate_transition(value)
                self.assertFalse(decision.allowed)
                self.assertEqual(decision.resulting_state, State.LOCKOUT)
                self.assertEqual(decision.reason_code, ReasonCode.LOCKOUT_REQUIRED)
                self.assertEqual(
                    decision.required_next_human_or_governance_action,
                    RequiredAction.RESET_REQUIRED,
                )
                self.assertEqual(decision.correlation_reference, "locked-denial-ref")

        wrong_name_with_collision = evaluate_transition(
            TransitionRequest(
                State.LOCKOUT,
                State.PAUSE,
                TransitionRequestName.PAUSE_TO_READY,
                "locked-collision-ref",
                facts(reset_facts_explicit=True),
                authority(presence="ABSENT", currentness="STALE"),
            )
        )
        self.assertEqual(
            wrong_name_with_collision.reason_code,
            ReasonCode.LOCKOUT_REQUIRED,
        )

    def test_lockout_reset_requirements_and_contradiction_precedence(self):
        evidence_free_entry = evaluate_transition(
            TransitionRequest(
                State.PAUSE,
                State.LOCKOUT,
                TransitionRequestName.ANY_TO_LOCKOUT,
                "evidence-free-lockout-ref",
                facts(lockout_required=False),
                authority(),
            )
        )
        valid_reset = evaluate_transition(
            TransitionRequest(
                State.LOCKOUT,
                State.PAUSE,
                TransitionRequestName.LOCKOUT_TO_PAUSE,
                "valid-reset-ref",
                facts(reset_facts_explicit=True),
                authority(),
            )
        )
        missing_facts = evaluate_transition(
            TransitionRequest(
                State.LOCKOUT,
                State.PAUSE,
                TransitionRequestName.LOCKOUT_TO_PAUSE,
                "missing-reset-facts-ref",
                facts(reset_facts_explicit=False),
                authority(),
            )
        )
        contradiction = evaluate_transition(
            TransitionRequest(
                State.LOCKOUT,
                State.READY,
                TransitionRequestName.PAUSE_TO_READY,
                "locked-contradiction-ref",
                facts(confirmed_position_exists=True, position_closed=True),
                authority(),
            )
        )

        self.assertFalse(evidence_free_entry.allowed)
        self.assertEqual(evidence_free_entry.resulting_state, State.PAUSE)
        self.assertEqual(
            evidence_free_entry.reason_code,
            ReasonCode.UNDEFINED_TRANSITION,
        )
        self.assertEqual(
            evidence_free_entry.required_next_human_or_governance_action,
            RequiredAction.GOVERNANCE_REVIEW,
        )
        self.assertTrue(valid_reset.allowed)
        self.assertEqual(valid_reset.resulting_state, State.PAUSE)
        self.assertEqual(valid_reset.reason_code, ReasonCode.ALLOWED)
        self.assertEqual(
            valid_reset.required_next_human_or_governance_action,
            RequiredAction.NONE,
        )
        self.assertFalse(missing_facts.allowed)
        self.assertEqual(missing_facts.resulting_state, State.LOCKOUT)
        self.assertEqual(missing_facts.reason_code, ReasonCode.RESET_FACTS_MISSING)
        self.assertEqual(
            missing_facts.required_next_human_or_governance_action,
            RequiredAction.RESET_REQUIRED,
        )
        self.assertEqual(
            contradiction.reason_code,
            ReasonCode.AMBIGUOUS_OR_CONTRADICTORY_INPUT,
        )
        self.assertEqual(contradiction.resulting_state, State.LOCKOUT)
        self.assertEqual(
            contradiction.required_next_human_or_governance_action,
            RequiredAction.HUMAN_REVIEW,
        )

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
        self.assertFalse(result.allowed)
        self.assertEqual(result.resulting_state, State.LOCKOUT)
        self.assertEqual(result.reason_code, ReasonCode.LOCKOUT_REQUIRED)
        self.assertEqual(result.required_next_human_or_governance_action, RequiredAction.RESET_REQUIRED)

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
