import unittest
from dataclasses import replace
from review_candidates.xnor_resolved_authority_binding_adapter import (
    ResolvedAuthority, SignedCoverage, ReviewState, bind_resolved_authority,
)


class ResolvedAuthorityBindingAdapterTests(unittest.TestCase):
    def setUp(self):
        fields = dict(authority_id="authority-B", grantor_id="grantor-G",
                      subject_id="subject-S", action="read", resource="resource-R",
                      target_digest="target-T", mapping_digest="mapping-M")
        self.resolved = ResolvedAuthority(**fields)
        self.coverage = SignedCoverage(**fields, checkpoint_digest="checkpoint-8",
                                       checkpoint_sequence=8,
                                       signed_lineage_verified_for_test=True, revoked=False)

    def check(self, coverage=None, resolved=None, commit_digest="checkpoint-8", commit_seq=8):
        result = bind_resolved_authority(
            self.resolved if resolved is None else resolved,
            self.coverage if coverage is None else coverage,
            commit_checkpoint_digest=commit_digest,
            commit_checkpoint_sequence=commit_seq,
        )
        self.assertFalse(result.authority_granted)
        self.assertFalse(result.execution_authorized)
        return result

    def test_matching_synthetic_evidence_never_authorizes(self):
        self.assertEqual(self.check().state, ReviewState.MATCHED_FOR_TEST)

    def test_caller_selected_a_gate_resolves_b(self):
        self.assertEqual(self.check(replace(self.coverage, authority_id="authority-A")).reason,
                         "authority_id_mismatch")

    def test_grantor_substitution(self):
        self.assertEqual(self.check(replace(self.coverage, grantor_id="other")).reason,
                         "grantor_id_mismatch")

    def test_subject_substitution(self):
        self.assertEqual(self.check(replace(self.coverage, subject_id="other")).reason,
                         "subject_id_mismatch")

    def test_action_substitution(self):
        self.assertEqual(self.check(replace(self.coverage, action="write")).reason,
                         "action_mismatch")

    def test_resource_substitution(self):
        self.assertEqual(self.check(replace(self.coverage, resource="other")).reason,
                         "resource_mismatch")

    def test_target_substitution(self):
        self.assertEqual(self.check(replace(self.coverage, target_digest="other")).reason,
                         "target_digest_mismatch")

    def test_mapping_substitution(self):
        self.assertEqual(self.check(replace(self.coverage, mapping_digest="other")).reason,
                         "mapping_digest_mismatch")

    def test_unverified_signed_lineage(self):
        self.assertEqual(self.check(replace(self.coverage, signed_lineage_verified_for_test=False)).state,
                         ReviewState.HOLD)

    def test_revoked(self):
        self.assertEqual(self.check(replace(self.coverage, revoked=True)).reason,
                         "revoked_or_unknown")

    def test_checkpoint_digest_changes_at_commit(self):
        self.assertEqual(self.check(commit_digest="checkpoint-9").reason,
                         "checkpoint_changed_before_commit")

    def test_checkpoint_sequence_changes_at_commit(self):
        self.assertEqual(self.check(commit_seq=9).reason, "checkpoint_changed_before_commit")

    def test_missing_checkpoint_digest(self):
        self.assertEqual(self.check(replace(self.coverage, checkpoint_digest="")).state,
                         ReviewState.HOLD)

    def test_boolean_checkpoint_sequence(self):
        self.assertEqual(self.check(replace(self.coverage, checkpoint_sequence=True)).state,
                         ReviewState.HOLD)

    def test_missing_coverage(self):
        result = bind_resolved_authority(self.resolved, None,
                                         commit_checkpoint_digest="checkpoint-8",
                                         commit_checkpoint_sequence=8)
        self.assertEqual(result.state, ReviewState.HOLD)

    def test_missing_authority_field(self):
        self.assertEqual(self.check(replace(self.coverage, authority_id="")).state,
                         ReviewState.HOLD)


if __name__ == "__main__":
    unittest.main()
