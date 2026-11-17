import unittest
from dataclasses import replace
from review_candidates.xnor_ed25519_test_vector_verifier import make_test_envelope
from review_candidates.xnor_checkpoint_lineage_synthetic import Checkpoint
from review_candidates.xnor_signed_lineage_composition import (
    CombinedState, verify_composed_fixture,
)


class SignedLineageCompositionTests(unittest.TestCase):
    def setUp(self):
        self.previous = Checkpoint("source-a", 1, 7, "digest-7", "digest-6", 100, 200)
        self.candidate = Checkpoint("source-a", 1, 8, "digest-8", "digest-7", 110, 200)
        self.payload = dict(authority_id="authority-a", target_digest="target-a",
                            mapping_digest="mapping-a", checkpoint_sequence=8,
                            checkpoint_digest="digest-8", checkpoint_source="source-a",
                            checkpoint_epoch=1, observed_epoch=110,
                            expires_epoch=200, revoked=False)

    def check(self, payload=None, candidate=None, previous=None):
        result = verify_composed_fixture(
            make_test_envelope(self.payload if payload is None else payload),
            self.previous if previous is None else previous,
            self.candidate if candidate is None else candidate,
            expected_authority="authority-a", expected_target="target-a",
            expected_mapping="mapping-a", expected_source="source-a",
            now=150, max_age=60, min_checkpoint=7,
        )
        self.assertFalse(result.authority_granted)
        self.assertFalse(result.execution_authorized)
        return result

    def test_signed_consistent_fixture_is_test_only(self):
        self.assertEqual(self.check().state, CombinedState.CONSISTENT_FOR_TEST)

    def test_signed_checkpoint_digest_mismatch(self):
        self.assertEqual(self.check(payload=dict(self.payload, checkpoint_digest="other")).reason,
                         "signed_lineage_binding_mismatch")

    def test_signed_checkpoint_source_mismatch(self):
        self.assertEqual(self.check(payload=dict(self.payload, checkpoint_source="source-b")).reason,
                         "signed_lineage_binding_mismatch")

    def test_signed_checkpoint_epoch_mismatch(self):
        self.assertEqual(self.check(payload=dict(self.payload, checkpoint_epoch=2)).reason,
                         "signed_lineage_binding_mismatch")

    def test_signed_checkpoint_sequence_mismatch(self):
        self.assertEqual(self.check(payload=dict(self.payload, checkpoint_sequence=9)).reason,
                         "signed_lineage_binding_mismatch")

    def test_parent_link_mismatch(self):
        self.assertEqual(self.check(candidate=replace(self.candidate, parent_digest="other")).state,
                         CombinedState.HOLD)

    def test_same_sequence_fork(self):
        self.assertEqual(self.check(candidate=replace(self.candidate, sequence=7)).state,
                         CombinedState.HOLD)

    def test_epoch_transition(self):
        self.assertEqual(self.check(candidate=replace(self.candidate, epoch=2)).state,
                         CombinedState.HOLD)

    def test_revoked_signed_payload(self):
        self.assertEqual(self.check(payload=dict(self.payload, revoked=True)).state,
                         CombinedState.HOLD)

    def test_authority_substitution(self):
        self.assertEqual(self.check(payload=dict(self.payload, authority_id="authority-b")).state,
                         CombinedState.HOLD)

    def test_mapping_substitution(self):
        self.assertEqual(self.check(payload=dict(self.payload, mapping_digest="other")).state,
                         CombinedState.HOLD)

    def test_expired_lineage(self):
        self.assertEqual(self.check(candidate=replace(self.candidate, expires_at=150)).state,
                         CombinedState.HOLD)


if __name__ == "__main__":
    unittest.main()
