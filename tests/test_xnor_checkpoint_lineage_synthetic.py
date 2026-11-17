import unittest
from dataclasses import replace
from review_candidates.xnor_checkpoint_lineage_synthetic import (
    Checkpoint, LineageState, check_lineage,
)


class CheckpointLineageTests(unittest.TestCase):
    def setUp(self):
        self.previous = Checkpoint("source-a", 1, 7, "digest-7", "digest-6", 100, 200)
        self.next = Checkpoint("source-a", 1, 8, "digest-8", "digest-7", 110, 200)

    def check(self, candidate, previous=None):
        result = check_lineage(self.previous if previous is None else previous, candidate,
                               expected_source="source-a", now=150, max_age=60)
        self.assertFalse(result.authority_granted)
        self.assertFalse(result.execution_authorized)
        return result

    def test_valid_synthetic_next_checkpoint(self):
        self.assertEqual(self.check(self.next).state, LineageState.CONSISTENT_FOR_TEST)

    def test_same_checkpoint_is_consistent_not_authority(self):
        self.assertEqual(self.check(self.previous).state, LineageState.CONSISTENT_FOR_TEST)

    def test_missing_checkpoint(self):
        self.assertEqual(self.check(None).state, LineageState.HOLD)

    def test_wrong_source(self):
        self.assertEqual(self.check(replace(self.next, source_id="source-b")).state, LineageState.HOLD)

    def test_missing_digest(self):
        self.assertEqual(self.check(replace(self.next, digest="")).state, LineageState.HOLD)

    def test_sequence_rollback(self):
        self.assertEqual(self.check(replace(self.next, sequence=6)).reason, "sequence_rollback")

    def test_same_sequence_fork(self):
        self.assertEqual(self.check(replace(self.next, sequence=7)).reason, "same_sequence_equivocation")

    def test_parent_mismatch(self):
        self.assertEqual(self.check(replace(self.next, parent_digest="wrong")).reason, "broken_parent_link")

    def test_sequence_gap(self):
        self.assertEqual(self.check(replace(self.next, sequence=9)).reason, "lineage_gap_requires_proof")

    def test_epoch_rollback(self):
        self.assertEqual(self.check(replace(self.next, epoch=0)).reason, "epoch_rollback")

    def test_epoch_transition(self):
        self.assertEqual(self.check(replace(self.next, epoch=2)).reason, "epoch_transition_requires_trust_review")

    def test_expired(self):
        self.assertEqual(self.check(replace(self.next, expires_at=150)).state, LineageState.HOLD)

    def test_future_observation(self):
        self.assertEqual(self.check(replace(self.next, observed_at=151)).state, LineageState.HOLD)

    def test_stale_observation(self):
        self.assertEqual(self.check(replace(self.next, observed_at=80)).state, LineageState.HOLD)

    def test_boolean_sequence(self):
        self.assertEqual(self.check(replace(self.next, sequence=True)).reason, "invalid_numeric_fields")

    def test_negative_sequence(self):
        self.assertEqual(self.check(replace(self.next, sequence=-1)).state, LineageState.HOLD)

    def test_negative_epoch(self):
        self.assertEqual(self.check(replace(self.next, epoch=-1)).state, LineageState.HOLD)

    def test_initial_checkpoint_remains_synthetic(self):
        result = self.check(self.next, previous=False)
        self.assertEqual(result.state, LineageState.HOLD)

    def test_wrong_prior_source(self):
        previous = replace(self.previous, source_id="source-b")
        self.assertEqual(self.check(self.next, previous=previous).reason, "source_changed")


if __name__ == "__main__":
    unittest.main()
