"""Synthetic-only interoperability contract negative tests."""
import unittest
from dataclasses import replace

from review_candidates.xnor_interoperability_contract_v01 import (
    AuthorityMappingV01, XnorEvidenceEnvelopeV01, ReviewState,
    review_synthetic_interoperability,
)


class InteroperabilityContractTests(unittest.TestCase):
    def setUp(self):
        self.e = XnorEvidenceEnvelopeV01(
            schema="node-xnor.revocation-evidence.v0.1",
            verifier_version="synthetic-v1", verdict="PASS", reason_codes=(),
            target_fingerprint_digest="synthetic-target",
            revocation_record_digest="synthetic-record",
            trusted_checkpoint_digest="synthetic-checkpoint",
            observed_at="2026-11-17T12:00:00Z",
            evidence_source="synthetic-review",
        )
        self.m = AuthorityMappingV01(
            schema="echoauth.xnor-authority-mapping.v0.1",
            xnor_namespace="synthetic-xnor", target_fingerprint_digest="synthetic-target",
            target_role="NODE_XNOR_REFERENCE_ISSUER", target_tier="NODE_XNOR_TIER2",
            target_scope="node-xnor:reference:issue", source_identity="synthetic-source",
            authority_record_id="authority-1", authority_source_id="source-1",
            subject_id="subject-1", mapping_version="synthetic-v1",
            mapping_digest="synthetic-mapping", approval_provenance_digest="synthetic-approval",
        )

    def check(self, e=None, m=None):
        r = review_synthetic_interoperability(
            self.e if e is None else e, self.m if m is None else m,
            expected_authority_record_id="authority-1",
            expected_target_digest="synthetic-target",
        )
        self.assertFalse(r.authority_granted)
        self.assertFalse(r.registry_mutation_authorized)
        self.assertFalse(r.execution_authorized)
        self.assertFalse(r.continuation_authorized)
        return r.state

    def test_structural_match_not_authorization(self):
        self.assertEqual(self.check(), ReviewState.MATCHED_FOR_REVIEW)

    def test_verifier_fail(self):
        self.assertEqual(self.check(e=replace(self.e, verdict="FAIL")), ReviewState.REJECT)

    def test_verifier_hold(self):
        self.assertEqual(self.check(e=replace(self.e, verdict="HOLD")), ReviewState.HOLD)

    def test_wrong_target(self):
        self.assertEqual(self.check(e=replace(self.e, target_fingerprint_digest="wrong")), ReviewState.REJECT)

    def test_wrong_authority_id(self):
        self.assertEqual(self.check(m=replace(self.m, authority_record_id="wrong")), ReviewState.REJECT)

    def test_missing_checkpoint(self):
        self.assertEqual(self.check(e=replace(self.e, trusted_checkpoint_digest=None)), ReviewState.HOLD)

    def test_missing_mapping_approval(self):
        self.assertEqual(self.check(m=replace(self.m, approval_provenance_digest="")), ReviewState.HOLD)

    def test_non_synthetic_source(self):
        self.assertEqual(self.check(e=replace(self.e, evidence_source="production")), ReviewState.REJECT)

    def test_schema_mismatch(self):
        self.assertEqual(self.check(e=replace(self.e, schema="other")), ReviewState.REJECT)

    def test_authority_flag_true(self):
        self.assertEqual(self.check(e=replace(self.e, authority_granted=True)), ReviewState.REJECT)

    def test_continuation_flag_true(self):
        self.assertEqual(self.check(e=replace(self.e, continuation_authorized=True)), ReviewState.REJECT)

    def test_missing_evidence(self):
        r = review_synthetic_interoperability(None, self.m,
            expected_authority_record_id="authority-1", expected_target_digest="synthetic-target")
        self.assertEqual(r.state, ReviewState.HOLD)

    def test_missing_mapping(self):
        r = review_synthetic_interoperability(self.e, None,
            expected_authority_record_id="authority-1", expected_target_digest="synthetic-target")
        self.assertEqual(r.state, ReviewState.HOLD)


if __name__ == "__main__":
    unittest.main()
