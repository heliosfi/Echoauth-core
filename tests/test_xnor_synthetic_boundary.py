"""Synthetic-only negative tests for non-authorizing XNOR review classifier."""

import unittest
from dataclasses import replace

from review_candidates.xnor_revocation_synthetic_boundary import (
    EvidenceDisposition,
    SyntheticRevocationEvidence,
    review_synthetic_revocation,
)


class SyntheticBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.evidence = SyntheticRevocationEvidence(
            schema="node-xnor.revocation-evidence.v0.1",
            verdict="PASS",
            target_authority_record_id="synthetic-authority-1",
            target_fingerprint_digest="synthetic-fingerprint-digest",
            checkpoint_digest="synthetic-checkpoint-digest",
            record_digest="synthetic-record-digest",
            signature_verified=True,
            checkpoint_trusted=True,
            freshness_verified=True,
            binding_verified=True,
        )

    def review(self, evidence):
        result = review_synthetic_revocation(
            evidence, expected_authority_record_id="synthetic-authority-1"
        )
        self.assertFalse(result.permission_granted)
        self.assertFalse(result.registry_mutation_authorized)
        self.assertFalse(result.execution_authorized)
        return result

    def test_pass_is_reviewable_but_never_permission(self):
        self.assertEqual(self.review(self.evidence).disposition, EvidenceDisposition.REVIEWABLE)

    def test_fail_is_rejected(self):
        self.assertEqual(self.review(replace(self.evidence, verdict="FAIL")).disposition, EvidenceDisposition.REJECT)

    def test_hold_stays_hold(self):
        self.assertEqual(self.review(replace(self.evidence, verdict="HOLD")).disposition, EvidenceDisposition.HOLD)

    def test_missing_evidence_stays_hold(self):
        self.assertEqual(self.review(None).disposition, EvidenceDisposition.HOLD)

    def test_wrong_target_is_rejected(self):
        self.assertEqual(self.review(replace(self.evidence, target_authority_record_id="other")).disposition, EvidenceDisposition.REJECT)

    def test_untrusted_checkpoint_stays_hold(self):
        self.assertEqual(self.review(replace(self.evidence, checkpoint_trusted=False)).disposition, EvidenceDisposition.HOLD)

    def test_unverified_signature_stays_hold(self):
        self.assertEqual(self.review(replace(self.evidence, signature_verified=False)).disposition, EvidenceDisposition.HOLD)

    def test_stale_evidence_stays_hold(self):
        self.assertEqual(self.review(replace(self.evidence, freshness_verified=False)).disposition, EvidenceDisposition.HOLD)

    def test_unverified_binding_stays_hold(self):
        self.assertEqual(self.review(replace(self.evidence, binding_verified=False)).disposition, EvidenceDisposition.HOLD)

    def test_missing_checkpoint_digest_stays_hold(self):
        self.assertEqual(self.review(replace(self.evidence, checkpoint_digest="")).disposition, EvidenceDisposition.HOLD)

    def test_real_evidence_is_not_accepted(self):
        self.assertEqual(self.review(replace(self.evidence, synthetic_only=False)).disposition, EvidenceDisposition.REJECT)

    def test_unsupported_schema_is_rejected(self):
        self.assertEqual(self.review(replace(self.evidence, schema="unknown")).disposition, EvidenceDisposition.REJECT)


if __name__ == "__main__":
    unittest.main()
