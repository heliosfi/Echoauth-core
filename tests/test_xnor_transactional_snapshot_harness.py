"""Deterministic negative TOCTOU tests; no production authorization."""
import unittest
from dataclasses import replace

from review_candidates.xnor_transactional_snapshot_harness import (
    SyntheticCheckpoint, SyntheticTransactionHarness, TransactionState,
)


class _SequenceProvider:
    def __init__(self, *items):
        self.items = iter(items)
    def read_checkpoint(self):
        item = next(self.items)
        if isinstance(item, Exception):
            raise item
        return item


class TransactionalSnapshotHarnessTests(unittest.TestCase):
    def setUp(self):
        self.s = SyntheticCheckpoint(
            authority_id="authority-a", target_digest="digest-a",
            checkpoint_sequence=5, checkpoint_digest="checkpoint-5",
            mapping_digest="mapping-a", observed_epoch=100,
            expires_epoch=200, revoked=False, trusted_for_test=True,
        )

    def check(self, before=None, after=None, *, preflight=120, commit=130):
        result = SyntheticTransactionHarness(_SequenceProvider(
            self.s if before is None else before,
            self.s if after is None else after,
        )).evaluate(
            expected_authority="authority-a", expected_target="digest-a",
            preflight_epoch=preflight, commit_epoch=commit,
        )
        self.assertFalse(result.authority_granted)
        self.assertFalse(result.execution_authorized)
        self.assertFalse(result.continuation_authorized)
        return result.state

    def test_stable_snapshot_clear_for_gate_review_only(self):
        self.assertEqual(self.check(), TransactionState.CLEAR_FOR_GATE_REVIEW)

    def test_revoked_at_preflight(self):
        self.assertEqual(self.check(before=replace(self.s, revoked=True)), TransactionState.REVOKED)

    def test_revoked_between_preflight_and_commit(self):
        self.assertEqual(self.check(after=replace(self.s, revoked=True, checkpoint_sequence=6, checkpoint_digest="checkpoint-6")), TransactionState.REVOKED)

    def test_checkpoint_advance_requires_reassessment(self):
        self.assertEqual(self.check(after=replace(self.s, checkpoint_sequence=6, checkpoint_digest="checkpoint-6")), TransactionState.HOLD)

    def test_checkpoint_rollback_blocks(self):
        self.assertEqual(self.check(after=replace(self.s, checkpoint_sequence=4, checkpoint_digest="checkpoint-4")), TransactionState.HOLD)

    def test_same_sequence_different_digest_blocks(self):
        self.assertEqual(self.check(after=replace(self.s, checkpoint_digest="fork")), TransactionState.HOLD)

    def test_mapping_change_blocks(self):
        self.assertEqual(self.check(after=replace(self.s, mapping_digest="mapping-b")), TransactionState.HOLD)

    def test_authority_substitution_blocks(self):
        self.assertEqual(self.check(after=replace(self.s, authority_id="authority-b")), TransactionState.HOLD)

    def test_target_substitution_blocks(self):
        self.assertEqual(self.check(after=replace(self.s, target_digest="digest-b")), TransactionState.HOLD)

    def test_expired_before_commit_blocks(self):
        self.assertEqual(self.check(commit=200), TransactionState.HOLD)

    def test_untrusted_commit_snapshot_blocks(self):
        self.assertEqual(self.check(after=replace(self.s, trusted_for_test=False)), TransactionState.HOLD)

    def test_commit_provider_outage_blocks(self):
        self.assertEqual(self.check(after=RuntimeError("synthetic outage")), TransactionState.HOLD)

    def test_preflight_provider_outage_blocks(self):
        self.assertEqual(self.check(before=RuntimeError("synthetic outage")), TransactionState.HOLD)

    def test_wrong_authority_at_preflight_blocks(self):
        self.assertEqual(self.check(before=replace(self.s, authority_id="authority-b")), TransactionState.HOLD)


if __name__ == "__main__":
    unittest.main()
