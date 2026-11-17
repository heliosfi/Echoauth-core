"""Characterize direct gate bypass of an optional review-only XNOR facade.

The current gate is not XNOR-aware. These tests demonstrate the gap, not a fix.
"""
import unittest
from unittest.mock import Mock

from test_authorization_gate import AuthorizationGateTests
from echoauth.auth import AuthorizationOutcome


class DirectGateBypassTests(unittest.TestCase):
    def setUp(self):
        self.fixture = AuthorizationGateTests(methodName="test_successful_authorization")
        self.fixture.setUp()
        self.fixture._register_policy()

    def test_direct_gate_can_authorize_without_xnor_observer(self):
        decision = self.fixture.gate.authorize(self.fixture._request())
        self.assertEqual(decision.outcome, AuthorizationOutcome.AUTHORIZED)
        self.assertNotIn("xnor_checkpoint", decision.evidence)

    def test_direct_gate_ignores_untrusted_xnor_revocation_hint(self):
        decision = self.fixture.gate.authorize(self.fixture._request(
            context={"location": "school", "xnor_revoked": True}
        ))
        self.assertEqual(decision.outcome, AuthorizationOutcome.AUTHORIZED)
        self.assertNotIn("xnor_checkpoint", decision.evidence)

    def test_optional_provider_not_invoked_by_direct_gate(self):
        optional_provider = Mock()
        decision = self.fixture.gate.authorize(self.fixture._request())
        self.assertEqual(decision.outcome, AuthorizationOutcome.AUTHORIZED)
        optional_provider.assert_not_called()

    def test_independent_policy_denial_still_enforced(self):
        from echoauth.policy import PolicyEffect
        self.fixture._register_policy(effect=PolicyEffect.DENY, rule_id="deny-2",
                                      policy_id="deny-policy", priority=20,
                                      audit_id="audit-deny-2")
        decision = self.fixture.gate.authorize(self.fixture._request())
        self.assertNotEqual(decision.outcome, AuthorizationOutcome.AUTHORIZED)

    def test_internal_authority_revocation_still_enforced(self):
        self.fixture.authority_repository.revoke(
            "authority-1", actor_id="registry-admin",
            reason="authority_revoked", occurred_at="2026-06-19T12:30:00Z",
            audit_event_id="audit-authority-revoked")
        decision = self.fixture.gate.authorize(self.fixture._request())
        self.assertEqual(decision.outcome, AuthorizationOutcome.REVOKED)


if __name__ == "__main__":
    unittest.main()
