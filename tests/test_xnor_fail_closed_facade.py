import unittest
from unittest.mock import Mock

from test_authorization_gate import AuthorizationGateTests
from echoauth.auth import AuthorizationOutcome
from echoauth.policy import PolicyEffect
from review_candidates.xnor_fail_closed_facade import (
    FacadeState, evaluate_facade,
)


class Observation:
    def __init__(self, value):
        self.state = type("State", (), {"value": value})()


class FailClosedFacadeTests(unittest.TestCase):
    def setUp(self):
        self.fixture = AuthorizationGateTests(methodName="test_successful_authorization")
        self.fixture.setUp()
        self.fixture._register_policy()

    def test_missing_observation_never_calls_gate(self):
        gate = Mock()
        result = evaluate_facade(observation=None, gate=gate, request=self.fixture._request())
        self.assertEqual(result.state, FacadeState.BLOCKED_FOR_REVIEW)
        gate.authorize.assert_not_called()

    def test_mismatch_never_calls_gate(self):
        gate = Mock()
        result = evaluate_facade(observation=Observation("HOLD"), gate=gate,
                                 request=self.fixture._request())
        self.assertEqual(result.state, FacadeState.BLOCKED_FOR_REVIEW)
        gate.authorize.assert_not_called()

    def test_unrecognized_observation_never_calls_gate(self):
        gate = Mock()
        result = evaluate_facade(observation=Observation("CLEAR"), gate=gate,
                                 request=self.fixture._request())
        self.assertEqual(result.state, FacadeState.BLOCKED_FOR_REVIEW)
        gate.authorize.assert_not_called()

    def test_matching_synthetic_observation_forwards_to_real_gate(self):
        result = evaluate_facade(observation=Observation("MATCHED_FOR_REVIEW"),
                                 gate=self.fixture.gate, request=self.fixture._request())
        self.assertEqual(result.state, FacadeState.FORWARDED_FOR_REVIEW)
        self.assertEqual(result.gate_decision.outcome, AuthorizationOutcome.AUTHORIZED)
        self.assertFalse(result.authority_granted)
        self.assertFalse(result.execution_authorized)

    def test_matching_synthetic_observation_cannot_override_policy_denial(self):
        self.fixture._register_policy(effect=PolicyEffect.DENY, rule_id="deny-2",
                                      policy_id="deny-policy", priority=20,
                                      audit_id="audit-deny-2")
        result = evaluate_facade(observation=Observation("MATCHED_FOR_REVIEW"),
                                 gate=self.fixture.gate, request=self.fixture._request())
        self.assertEqual(result.state, FacadeState.FORWARDED_FOR_REVIEW)
        self.assertNotEqual(result.gate_decision.outcome, AuthorizationOutcome.AUTHORIZED)
        self.assertFalse(result.authority_granted)

    def test_matching_synthetic_observation_cannot_override_authority_denial(self):
        result = evaluate_facade(observation=Observation("MATCHED_FOR_REVIEW"),
                                 gate=self.fixture.gate, request=self.fixture._request(action="delete"))
        self.assertEqual(result.gate_decision.outcome, AuthorizationOutcome.INVALID_AUTHORITY)
        self.assertFalse(result.authority_granted)

    def test_gate_exception_blocks_facade(self):
        gate = Mock()
        gate.authorize.side_effect = RuntimeError("dependency down")
        result = evaluate_facade(observation=Observation("MATCHED_FOR_REVIEW"),
                                 gate=gate, request=self.fixture._request())
        self.assertEqual(result.state, FacadeState.BLOCKED_FOR_REVIEW)
        self.assertIsNone(result.gate_decision)


if __name__ == "__main__":
    unittest.main()
