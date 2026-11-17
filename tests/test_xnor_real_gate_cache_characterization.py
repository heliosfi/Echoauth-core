"""Review-only characterization of the *actual* EchoAuth gate cache.

No production changes and no assertion that external XNOR revocations are wired.
"""
from test_authorization_gate import AuthorizationGateTests
from echoauth.auth import AuthorizationOutcome


class ActualGateCacheCharacterizationTests(AuthorizationGateTests):
    def test_identical_positive_evidence_reuses_cached_decision(self):
        self._register_policy()
        request = self._request()
        first = self.gate.authorize(request)
        self.assertEqual(first.outcome, AuthorizationOutcome.AUTHORIZED)
        count = len(self.audit.chain("gate-audit"))
        second = self.gate.authorize(request)
        self.assertIs(first, second)
        self.assertEqual(len(self.audit.chain("gate-audit")), count)
        self.assertEqual(len(self.gate._cache), 1)

    def test_persisted_revocation_changes_decision_and_does_not_replay_positive(self):
        self._register_policy()
        request = self._request()
        first = self.gate.authorize(request)
        self.assertEqual(first.outcome, AuthorizationOutcome.AUTHORIZED)
        self.authority_repository.revoke(
            "authority-1",
            actor_id="registry-admin",
            reason="authority_revoked",
            occurred_at="2026-06-19T12:30:00Z",
            audit_event_id="audit-authority-revoked",
        )
        second = self.gate.authorize(request)
        self.assertEqual(second.outcome, AuthorizationOutcome.REVOKED)
        self.assertIsNot(first, second)
        self.assertNotEqual(first.evidence_hash, second.evidence_hash)

    def test_positive_evidence_has_no_external_xnor_checkpoint_binding(self):
        self._register_policy()
        decision = self.gate.authorize(self._request())
        self.assertEqual(decision.outcome, AuthorizationOutcome.AUTHORIZED)
        self.assertNotIn("xnor_checkpoint_digest", decision.evidence)
        self.assertNotIn("xnor_revocation_coverage", decision.evidence)
        self.assertNotIn("xnor_mapping_digest", decision.evidence)

    def test_same_evidence_hash_cannot_prove_external_revocation_freshness(self):
        self._register_policy()
        request = self._request()
        first = self.gate.authorize(request)
        # Simulate an external revocation event *not delivered* to the gate.
        # This test deliberately does not mutate the authority repository.
        external_event = {"target": "authority-1", "revoked": True, "checkpoint": 6}
        self.assertTrue(external_event["revoked"])
        second = self.gate.authorize(request)
        self.assertEqual(first.outcome, AuthorizationOutcome.AUTHORIZED)
        self.assertIs(first, second)
        self.assertEqual(first.evidence_hash, second.evidence_hash)
        # Observed gap: a disconnected external event cannot affect the gate.
        # This is NOT a desired security result.
