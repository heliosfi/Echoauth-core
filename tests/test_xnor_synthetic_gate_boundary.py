"""Synthetic gate boundary: blocked cases never invoke the ordinary gate."""
import unittest
from dataclasses import replace

from echoauth.auth import AuthorizationOutcome
from review_candidates.xnor_synthetic_fail_closed_provider import (
    SyntheticFailClosedProvider, SyntheticSnapshot,
)
from review_candidates.xnor_synthetic_gate_boundary import (
    BoundaryState, SyntheticGateBoundary,
)
from test_authorization_gate import AuthorizationGateTests


class _CountingGate:
    def __init__(self, gate):
        self.gate = gate
        self.calls = 0

    def authorize(self, request):
        self.calls += 1
        return self.gate.authorize(request)


class _FailingProvider:
    def check(self, **kwargs):
        raise RuntimeError("synthetic outage")


class SyntheticGateBoundaryTests(unittest.TestCase):
    def setUp(self):
        f = AuthorizationGateTests(methodName="test_successful_authorization")
        f.setUp()
        f._register_policy()
        self.fixture = f
        self.gate = _CountingGate(f.gate)
        self.snapshot = SyntheticSnapshot(
            authority_record_id="authority-1",
            target_fingerprint_digest="synthetic-target",
            mapping_authority_record_id="authority-1",
            mapping_target_digest="synthetic-target",
            provider_identity="synthetic-provider",
            checkpoint_digest="synthetic-checkpoint",
            mapping_digest="synthetic-mapping",
            observed_at_epoch=100,
            expires_at_epoch=200,
            effective_revoked=False,
            source_attested_for_test=True,
            checkpoint_monotonic_for_test=True,
            mapping_attested_for_test=True,
        )

    def evaluate(self, snapshot=None, *, unavailable=False, provider=None):
        p = provider if provider is not None else SyntheticFailClosedProvider(
            self.snapshot if snapshot is None else snapshot, unavailable=unavailable
        )
        return SyntheticGateBoundary(p, self.gate).evaluate(
            self.fixture._request(),
            authority_record_id="authority-1",
            target_digest="synthetic-target", now_epoch=150,
        )

    def test_clear_runs_independent_gate(self):
        r = self.evaluate()
        self.assertEqual(r.state, BoundaryState.GATE_EVALUATED)
        self.assertEqual(self.gate.calls, 1)
        self.assertEqual(r.gate_decision.outcome, AuthorizationOutcome.AUTHORIZED)
        self.assertFalse(r.authority_granted_by_evidence)

    def test_revoked_blocks_gate(self):
        r = self.evaluate(replace(self.snapshot, effective_revoked=True))
        self.assertEqual(r.state, BoundaryState.BLOCKED_REVOKED)
        self.assertEqual(self.gate.calls, 0)
        self.assertIsNone(r.gate_decision)

    def test_stale_blocks_gate(self):
        r = self.evaluate(replace(self.snapshot, expires_at_epoch=149))
        self.assertEqual(r.state, BoundaryState.BLOCKED_HOLD)
        self.assertEqual(self.gate.calls, 0)

    def test_mapping_mismatch_blocks_gate(self):
        r = self.evaluate(replace(self.snapshot, mapping_authority_record_id="other"))
        self.assertEqual(r.state, BoundaryState.BLOCKED_HOLD)
        self.assertEqual(self.gate.calls, 0)

    def test_provider_outage_blocks_gate(self):
        r = self.evaluate(unavailable=True)
        self.assertEqual(r.state, BoundaryState.BLOCKED_HOLD)
        self.assertEqual(self.gate.calls, 0)

    def test_provider_exception_blocks_gate(self):
        r = self.evaluate(provider=_FailingProvider())
        self.assertEqual(r.state, BoundaryState.BLOCKED_HOLD)
        self.assertEqual(self.gate.calls, 0)

    def test_clear_does_not_override_policy_denial(self):
        self.fixture._register_policy(
            effect=__import__("echoauth.policy", fromlist=["PolicyEffect"]).PolicyEffect.DENY,
            rule_id="deny-rule", policy_id="deny-policy", audit_id="audit-deny",
        )
        r = self.evaluate()
        self.assertEqual(r.state, BoundaryState.GATE_EVALUATED)
        self.assertNotEqual(r.gate_decision.outcome, AuthorizationOutcome.AUTHORIZED)
        self.assertEqual(self.gate.calls, 1)


if __name__ == "__main__":
    unittest.main()
