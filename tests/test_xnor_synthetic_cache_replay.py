import unittest
from dataclasses import replace
from review_candidates.xnor_synthetic_cache_replay import (
    ReplayState, Snapshot, SyntheticPositiveCache,
)


class _Provider:
    def __init__(self, value):
        self.value = value
    def read(self):
        if isinstance(self.value, Exception):
            raise self.value
        return self.value


class SyntheticCacheReplayTests(unittest.TestCase):
    def setUp(self):
        self.s = Snapshot(
            authority_id="authority-a", target_digest="digest-a",
            checkpoint_sequence=5, checkpoint_digest="checkpoint-5",
            mapping_digest="mapping-a", valid_until=200, revoked=False,
            attested_for_test=True,
        )
        self.cache = SyntheticPositiveCache()
        self.cache.store(self.s)

    def check(self, current, *, now=150, authority="authority-a", target="digest-a"):
        result = self.cache.evaluate(_Provider(current), authority_id=authority,
                                     target_digest=target, now=now)
        self.assertFalse(result.reused_positive)
        self.assertFalse(result.authority_granted)
        self.assertFalse(result.execution_authorized)
        return result.state

    def test_same_checkpoint_does_not_reuse_positive(self):
        self.assertEqual(self.check(self.s), ReplayState.REVIEW_CANDIDATE)

    def test_revocation_at_new_checkpoint_blocks(self):
        self.assertEqual(self.check(replace(self.s, checkpoint_sequence=6,
            checkpoint_digest="checkpoint-6", revoked=True)), ReplayState.REVOKED)

    def test_revocation_at_same_checkpoint_blocks(self):
        self.assertEqual(self.check(replace(self.s, revoked=True)), ReplayState.REVOKED)

    def test_checkpoint_advance_requires_reassessment(self):
        self.assertEqual(self.check(replace(self.s, checkpoint_sequence=6,
            checkpoint_digest="checkpoint-6")), ReplayState.REVIEW_CANDIDATE)

    def test_rollback_blocks(self):
        self.assertEqual(self.check(replace(self.s, checkpoint_sequence=4,
            checkpoint_digest="checkpoint-4")), ReplayState.HOLD)

    def test_checkpoint_fork_reassesses(self):
        self.assertEqual(self.check(replace(self.s, checkpoint_digest="fork")),
                         ReplayState.REVIEW_CANDIDATE)

    def test_provider_outage_blocks(self):
        self.assertEqual(self.check(RuntimeError("outage")), ReplayState.HOLD)

    def test_missing_snapshot_blocks(self):
        self.assertEqual(self.check(None), ReplayState.HOLD)

    def test_untrusted_snapshot_blocks(self):
        self.assertEqual(self.check(replace(self.s, attested_for_test=False)), ReplayState.HOLD)

    def test_stale_snapshot_blocks(self):
        self.assertEqual(self.check(self.s, now=200), ReplayState.HOLD)

    def test_authority_substitution_blocks(self):
        self.assertEqual(self.check(replace(self.s, authority_id="authority-b")), ReplayState.HOLD)

    def test_target_substitution_blocks(self):
        self.assertEqual(self.check(replace(self.s, target_digest="digest-b")), ReplayState.HOLD)

    def test_mapping_change_blocks(self):
        self.assertEqual(self.check(replace(self.s, mapping_digest="mapping-b")), ReplayState.HOLD)

    def test_missing_checkpoint_blocks(self):
        self.assertEqual(self.check(replace(self.s, checkpoint_digest="")), ReplayState.HOLD)

    def test_no_cached_candidate_requires_fresh_review(self):
        self.cache = SyntheticPositiveCache()
        self.assertEqual(self.check(self.s), ReplayState.REVIEW_CANDIDATE)


if __name__ == "__main__":
    unittest.main()
