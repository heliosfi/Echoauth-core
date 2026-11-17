"""Test-only observation of the real EchoAuth resolver called by the real gate.

Does not inject trusted XNOR evidence or modify production authorization.
"""
import unittest
from unittest.mock import patch

from test_authorization_gate import AuthorizationGateTests
from echoauth.auth import AuthorizationOutcome


class RealResolverProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.fixture = AuthorizationGateTests(methodName="test_successful_authorization")
        self.fixture.setUp()
        self.fixture._register_policy()

    def observe(self, request):
        captured = []
        original = self.fixture.authority_service.resolve

        def recorder(resolution_request):
            result = original(resolution_request)
            captured.append((resolution_request, result))
            return result

        with patch.object(self.fixture.authority_service, "resolve", side_effect=recorder):
            decision = self.fixture.gate.authorize(request)
        self.assertEqual(len(captured), 1)
        return decision, captured[0][0], captured[0][1]

    def test_actual_gate_resolver_selects_authority_not_caller_hint(self):
        request = self.fixture._request(
            context={"location": "school", "xnor_claimed_authority": "authority-attacker"}
        )
        decision, resolver_request, resolved = self.observe(request)
        self.assertEqual(decision.outcome, AuthorizationOutcome.AUTHORIZED)
        self.assertEqual(resolved.authority_record_id, "authority-1")
        self.assertEqual(decision.evidence["authority"]["authority_record_id"], "authority-1")
        self.assertEqual(resolver_request.requester_id, "parent-1")
        self.assertNotEqual(resolved.authority_record_id, request.context["xnor_claimed_authority"])

    def test_real_gate_resolver_request_has_no_external_revocation_records(self):
        decision, resolver_request, resolved = self.observe(self.fixture._request())
        self.assertEqual(resolved.authority_record_id, "authority-1")
        self.assertEqual(tuple(resolver_request.revocation_records), ())
        self.assertNotIn("xnor_checkpoint", decision.evidence)
        self.assertNotIn("xnor_mapping_digest", decision.evidence)

    def test_delegated_gate_uses_grantor_for_authority_resolution(self):
        self.fixture._create_delegation()
        request = self.fixture._request(
            requester_id="teacher-1", delegation_id="delegation-1",
            context={"location": "school", "xnor_claimed_authority": "authority-attacker"},
        )
        decision, resolver_request, resolved = self.observe(request)
        self.assertEqual(decision.outcome, AuthorizationOutcome.AUTHORIZED)
        self.assertEqual(resolver_request.requester_id, "parent-1")
        self.assertEqual(resolved.authority_record_id, "authority-1")
        self.assertNotEqual(resolver_request.requester_id, request.requester_id)

    def test_caller_hint_does_not_create_missing_authority(self):
        request = self.fixture._request(
            action="delete",
            context={"location": "school", "xnor_claimed_authority": "authority-1"},
        )
        decision, _, resolved = self.observe(request)
        self.assertEqual(decision.outcome, AuthorizationOutcome.INVALID_AUTHORITY)
        self.assertNotEqual(resolved.outcome.value, "authorized")


if __name__ == "__main__":
    unittest.main()
