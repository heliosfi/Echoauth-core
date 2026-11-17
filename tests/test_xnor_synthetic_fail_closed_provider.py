"""Fail-closed synthetic provider tests; no runtime authorization integration."""
import unittest
from dataclasses import replace

from review_candidates.xnor_synthetic_fail_closed_provider import (
    CoverageState, SyntheticFailClosedProvider, SyntheticSnapshot,
)


class SyntheticFailClosedProviderTests(unittest.TestCase):
    def setUp(self):
        self.s = SyntheticSnapshot(
            authority_record_id="authority-1",
            target_fingerprint_digest="synthetic-digest-1",
            mapping_authority_record_id="authority-1",
            mapping_target_digest="synthetic-digest-1",
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

    def check(self, snapshot=None, unavailable=False):
        provider = SyntheticFailClosedProvider(
            self.s if snapshot is None else snapshot, unavailable=unavailable
        )
        decision = provider.check(
            authority_record_id="authority-1",
            target_digest="synthetic-digest-1", now_epoch=150,
        )
        self.assertFalse(decision.authority_granted)
        self.assertFalse(decision.execution_authorized)
        self.assertFalse(decision.continuation_authorized)
        self.assertFalse(decision.registry_mutation_authorized)
        return decision.state

    def test_covered_clear_only_for_review(self):
        self.assertEqual(self.check(), CoverageState.CLEAR_FOR_REVIEW)

    def test_effective_revocation(self):
        self.assertEqual(self.check(replace(self.s, effective_revoked=True)), CoverageState.REVOKED)

    def test_source_outage(self):
        self.assertEqual(self.check(unavailable=True), CoverageState.HOLD)

    def test_missing_snapshot(self):
        d = SyntheticFailClosedProvider(None).check(
            authority_record_id="authority-1", target_digest="synthetic-digest-1", now_epoch=150)
        self.assertEqual(d.state, CoverageState.HOLD)

    def test_stale(self):
        self.assertEqual(self.check(replace(self.s, expires_at_epoch=149)), CoverageState.HOLD)

    def test_future_observation(self):
        self.assertEqual(self.check(replace(self.s, observed_at_epoch=151)), CoverageState.HOLD)

    def test_mapping_authority_mismatch(self):
        self.assertEqual(self.check(replace(self.s, mapping_authority_record_id="other")), CoverageState.HOLD)

    def test_mapping_target_mismatch(self):
        self.assertEqual(self.check(replace(self.s, mapping_target_digest="other")), CoverageState.HOLD)

    def test_source_not_attested(self):
        self.assertEqual(self.check(replace(self.s, source_attested_for_test=False)), CoverageState.HOLD)

    def test_checkpoint_rollback(self):
        self.assertEqual(self.check(replace(self.s, checkpoint_monotonic_for_test=False)), CoverageState.HOLD)

    def test_mapping_not_attested(self):
        self.assertEqual(self.check(replace(self.s, mapping_attested_for_test=False)), CoverageState.HOLD)

    def test_missing_checkpoint(self):
        self.assertEqual(self.check(replace(self.s, checkpoint_digest="")), CoverageState.HOLD)

    def test_non_synthetic_source(self):
        self.assertEqual(self.check(replace(self.s, synthetic_only=False)), CoverageState.HOLD)


if __name__ == "__main__":
    unittest.main()
