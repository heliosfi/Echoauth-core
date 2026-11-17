"""Negative contract tests; no production gate integration or real signatures."""
import unittest
from dataclasses import replace

from review_candidates.xnor_mandatory_seam_negative_harness import (
    ReviewDisposition, SyntheticCheckpoint, review_mandatory_seam,
)


def valid_checkpoint():
    return SyntheticCheckpoint(
        issuer_known=True, signature_valid=True, lineage_valid=True,
        fresh=True, mapping_valid=True, authority_id="authority-1",
        revoked=False, source_available=True, snapshot_stable=True,
    )


class MandatorySeamNegativeHarnessTests(unittest.TestCase):
    def classify(self, checkpoint=None, *, authority="authority-1", allows=True):
        return review_mandatory_seam(
            resolved_authority_id=authority,
            checkpoint=checkpoint,
            independent_gate_allows=allows,
        )

    def assert_hold(self, result):
        self.assertEqual(result.disposition, ReviewDisposition.HOLD)
        self.assertFalse(result.authority_granted)
        self.assertFalse(result.execution_authorized)

    def test_synthetic_clear_is_not_permission(self):
        result = self.classify(valid_checkpoint())
        self.assertEqual(result.disposition, ReviewDisposition.CONTINUE_REVIEW)
        self.assertFalse(result.authority_granted)
        self.assertFalse(result.execution_authorized)

    def test_missing_checkpoint(self):
        self.assert_hold(self.classify())

    def test_missing_resolver_authority(self):
        self.assert_hold(self.classify(valid_checkpoint(), authority=""))

    def test_unknown_issuer(self):
        self.assert_hold(self.classify(replace(valid_checkpoint(), issuer_known=False)))

    def test_invalid_signature(self):
        self.assert_hold(self.classify(replace(valid_checkpoint(), signature_valid=False)))

    def test_invalid_lineage(self):
        self.assert_hold(self.classify(replace(valid_checkpoint(), lineage_valid=False)))

    def test_stale_checkpoint(self):
        self.assert_hold(self.classify(replace(valid_checkpoint(), fresh=False)))

    def test_invalid_mapping(self):
        self.assert_hold(self.classify(replace(valid_checkpoint(), mapping_valid=False)))

    def test_authority_mismatch(self):
        self.assert_hold(self.classify(replace(valid_checkpoint(), authority_id="other")))

    def test_effective_revocation(self):
        self.assert_hold(self.classify(replace(valid_checkpoint(), revoked=True)))

    def test_unknown_revocation(self):
        self.assert_hold(self.classify(replace(valid_checkpoint(), revoked=None)))

    def test_provider_outage(self):
        self.assert_hold(self.classify(replace(valid_checkpoint(), source_available=False)))

    def test_snapshot_changed_before_commit(self):
        self.assert_hold(self.classify(replace(valid_checkpoint(), snapshot_stable=False)))

    def test_independent_gate_denial_not_upgraded(self):
        self.assert_hold(self.classify(valid_checkpoint(), allows=False))

    def test_missing_gate_result_not_upgraded(self):
        self.assert_hold(self.classify(valid_checkpoint(), allows=None))

    def test_unrecognized_checkpoint_object_fails_closed(self):
        self.assert_hold(self.classify(object()))

    def test_untrusted_truthy_string_does_not_pass(self):
        self.assert_hold(self.classify(replace(valid_checkpoint(), signature_valid="yes")))


if __name__ == "__main__":
    unittest.main()
