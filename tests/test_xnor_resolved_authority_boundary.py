"""Negative tests for synthetic exact resolved-authority binding."""
import unittest
from dataclasses import replace

from echoauth.auth import AuthorizationOutcome
from review_candidates.xnor_synthetic_fail_closed_provider import SyntheticFailClosedProvider, SyntheticSnapshot
from review_candidates.xnor_synthetic_gate_boundary import BoundaryState
from review_candidates.xnor_resolved_authority_boundary import (
    SyntheticResolvedAuthority, SyntheticResolvedAuthorityBoundary,
)
from test_authorization_gate import AuthorizationGateTests


class _Resolver:
    def __init__(self, binding):
        self.binding = binding
    def resolve_binding(self, request):
        return self.binding


class _Gate:
    def __init__(self, gate):
        self.gate = gate
        self.calls = 0
    def authorize(self, request):
        self.calls += 1
        return self.gate.authorize(request)


class ResolvedAuthorityBoundaryTests(unittest.TestCase):
    def setUp(self):
        f = AuthorizationGateTests(methodName="test_successful_authorization")
        f.setUp()
        f._register_policy()
        self.f = f
        self.gate = _Gate(f.gate)
        self.binding = SyntheticResolvedAuthority(
            "authority-1", "digest-a", "subject-1", "read", "record-1", True,
        )
        self.snapshot = SyntheticSnapshot(
            authority_record_id="authority-1", target_fingerprint_digest="digest-a",
            mapping_authority_record_id="authority-1", mapping_target_digest="digest-a",
            provider_identity="synthetic-provider", checkpoint_digest="synthetic-checkpoint",
            mapping_digest="synthetic-mapping", observed_at_epoch=100,
            expires_at_epoch=200, effective_revoked=False,
            source_attested_for_test=True, checkpoint_monotonic_for_test=True,
            mapping_attested_for_test=True,
        )

    def run_boundary(self, binding=None, snapshot=None):
        return SyntheticResolvedAuthorityBoundary(
            _Resolver(self.binding if binding is None else binding),
            SyntheticFailClosedProvider(self.snapshot if snapshot is None else snapshot),
            self.gate,
        ).evaluate(self.f._request(), now_epoch=150)

    def test_exact_binding_allows_independent_gate_evaluation(self):
        result = self.run_boundary()
        self.assertEqual(result.state, BoundaryState.GATE_EVALUATED)
        self.assertEqual(result.gate_decision.outcome, AuthorizationOutcome.AUTHORIZED)
        self.assertEqual(self.gate.calls, 1)

    def test_provider_clears_a_but_resolver_selects_b_blocks(self):
        result = self.run_boundary(binding=replace(
            self.binding, authority_record_id="authority-b", target_fingerprint_digest="digest-b"))
        self.assertEqual(result.state, BoundaryState.BLOCKED_HOLD)
        self.assertEqual(self.gate.calls, 0)

    def test_same_authority_wrong_digest_blocks(self):
        result = self.run_boundary(binding=replace(self.binding, target_fingerprint_digest="wrong"))
        self.assertEqual(result.state, BoundaryState.BLOCKED_HOLD)
        self.assertEqual(self.gate.calls, 0)

    def test_subject_mismatch_blocks(self):
        result = self.run_boundary(binding=replace(self.binding, subject_id="other"))
        self.assertEqual(result.state, BoundaryState.BLOCKED_HOLD)
        self.assertEqual(self.gate.calls, 0)

    def test_action_mismatch_blocks(self):
        result = self.run_boundary(binding=replace(self.binding, action="write"))
        self.assertEqual(result.state, BoundaryState.BLOCKED_HOLD)
        self.assertEqual(self.gate.calls, 0)

    def test_resource_mismatch_blocks(self):
        result = self.run_boundary(binding=replace(self.binding, resource="other"))
        self.assertEqual(result.state, BoundaryState.BLOCKED_HOLD)
        self.assertEqual(self.gate.calls, 0)

    def test_untrusted_resolver_blocks(self):
        result = self.run_boundary(binding=replace(self.binding, resolver_attested_for_test=False))
        self.assertEqual(result.state, BoundaryState.BLOCKED_HOLD)
        self.assertEqual(self.gate.calls, 0)

    def test_missing_binding_blocks(self):
        result = self.run_boundary(binding=False)
        self.assertEqual(result.state, BoundaryState.BLOCKED_HOLD)
        self.assertEqual(self.gate.calls, 0)

    def test_revoked_exact_binding_blocks(self):
        result = self.run_boundary(snapshot=replace(self.snapshot, effective_revoked=True))
        self.assertEqual(result.state, BoundaryState.BLOCKED_REVOKED)
        self.assertEqual(self.gate.calls, 0)


if __name__ == "__main__":
    unittest.main()
