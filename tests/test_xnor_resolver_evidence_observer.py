"""Instrument real gate resolver without changing its authorization behavior."""
import unittest
from unittest.mock import patch

from test_authorization_gate import AuthorizationGateTests
from echoauth.auth import AuthorizationOutcome
from review_candidates.xnor_resolver_evidence_observer import (
    ClaimedEvidence, ObservationState, observe_resolver_binding,
)


class RealResolverObserverTests(unittest.TestCase):
    def setUp(self):
        self.fixture = AuthorizationGateTests(methodName="test_successful_authorization")
        self.fixture.setUp()
        self.fixture._register_policy()

    def run_observed(self, request, claimed):
        captured = []
        real_resolve = self.fixture.authority_service.resolve

        def spy(resolver_request):
            resolved = real_resolve(resolver_request)
            captured.append(observe_resolver_binding(resolver_request, resolved, claimed))
            return resolved

        with patch.object(self.fixture.authority_service, "resolve", side_effect=spy):
            decision = self.fixture.gate.authorize(request)
        self.assertEqual(len(captured), 1)
        self.assertFalse(captured[0].authority_granted)
        self.assertFalse(captured[0].execution_authorized)
        return decision, captured[0]

    def claim(self, **changes):
        fields = dict(authority_record_id="authority-1", grantor_id="parent-1",
                      subject_id="subject-1", action="read", resource="record-1")
        fields.update(changes)
        return ClaimedEvidence(**fields)

    def test_direct_matching_claim_observed_but_not_authorized_by_observer(self):
        decision, observed = self.run_observed(self.fixture._request(), self.claim())
        self.assertEqual(observed.state, ObservationState.MATCHED_FOR_REVIEW)
        self.assertEqual(decision.outcome, AuthorizationOutcome.AUTHORIZED)

    def test_caller_authority_substitution_holds_observer_only(self):
        decision, observed = self.run_observed(self.fixture._request(), self.claim(authority_record_id="authority-attacker"))
        self.assertEqual(observed.reason, "authority_record_id_mismatch")
        self.assertEqual(decision.outcome, AuthorizationOutcome.AUTHORIZED)

    def test_grantor_substitution_holds(self):
        _, observed = self.run_observed(self.fixture._request(), self.claim(grantor_id="teacher-1"))
        self.assertEqual(observed.reason, "grantor_id_mismatch")

    def test_subject_substitution_holds(self):
        _, observed = self.run_observed(self.fixture._request(), self.claim(subject_id="subject-2"))
        self.assertEqual(observed.reason, "subject_id_mismatch")

    def test_action_substitution_holds(self):
        _, observed = self.run_observed(self.fixture._request(), self.claim(action="write"))
        self.assertEqual(observed.reason, "action_mismatch")

    def test_resource_substitution_holds(self):
        _, observed = self.run_observed(self.fixture._request(), self.claim(resource="record-2"))
        self.assertEqual(observed.reason, "resource_mismatch")

    def test_delegated_grantor_from_real_resolver(self):
        self.fixture._create_delegation()
        request = self.fixture._request(requester_id="teacher-1", delegation_id="delegation-1")
        decision, observed = self.run_observed(request, self.claim())
        self.assertEqual(decision.outcome, AuthorizationOutcome.AUTHORIZED)
        self.assertEqual(observed.state, ObservationState.MATCHED_FOR_REVIEW)

    def test_delegated_caller_as_grantor_is_rejected(self):
        self.fixture._create_delegation()
        request = self.fixture._request(requester_id="teacher-1", delegation_id="delegation-1")
        _, observed = self.run_observed(request, self.claim(grantor_id="teacher-1"))
        self.assertEqual(observed.reason, "grantor_id_mismatch")

    def test_resolver_denial_stays_hold(self):
        decision, observed = self.run_observed(self.fixture._request(action="delete"),
                                                self.claim(action="delete"))
        self.assertEqual(decision.outcome, AuthorizationOutcome.INVALID_AUTHORITY)
        self.assertEqual(observed.state, ObservationState.HOLD)

    def test_policy_denial_not_upgraded_by_observer(self):
        # Register a higher priority deny and observe the real gate.
        from echoauth.policy import PolicyEffect
        self.fixture._register_policy(effect=PolicyEffect.DENY, rule_id="deny-2",
                                      policy_id="deny-policy", priority=20,
                                      audit_id="audit-deny-2")
        decision, observed = self.run_observed(self.fixture._request(), self.claim())
        self.assertEqual(observed.state, ObservationState.MATCHED_FOR_REVIEW)
        self.assertNotEqual(decision.outcome, AuthorizationOutcome.AUTHORIZED)


if __name__ == "__main__":
    unittest.main()
