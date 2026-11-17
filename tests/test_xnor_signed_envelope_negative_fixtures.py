import unittest
from dataclasses import replace
from review_candidates.xnor_signed_envelope_fixture_review import (
    SyntheticEnvelope, ReviewVerdict, inspect_fixture,
)


class SignedEnvelopeNegativeFixtureTests(unittest.TestCase):
    def setUp(self):
        self.envelope = SyntheticEnvelope(
            schema="node-xnor.signed-revocation.v0.1", issuer="fixture-issuer",
            key_id="fixture-key", algorithm="fixture-alg",
            signed_payload_digest="fixture-payload", signature="NOT_A_REAL_SIGNATURE",
            authority_id="authority-a", subject_id="subject-a", action="read",
            resource="record-a", target_digest="target-a", mapping_digest="mapping-a",
            checkpoint_sequence=7, checkpoint_digest="checkpoint-7",
            observed_epoch=100, expires_epoch=200,
        )

    def inspect(self, envelope):
        result = inspect_fixture(
            envelope, expected_authority="authority-a", expected_subject="subject-a",
            expected_action="read", expected_resource="record-a",
            expected_target="target-a", expected_mapping="mapping-a",
            now=150, min_checkpoint=7,
        )
        self.assertEqual(result.verdict, ReviewVerdict.HOLD)
        self.assertFalse(result.signature_verified)
        self.assertFalse(result.authority_granted)
        self.assertFalse(result.execution_authorized)
        return result.reason

    def test_plausible_fixture_still_holds_without_crypto(self):
        self.assertEqual(self.inspect(self.envelope), "cryptographic_and_trust_verification_not_implemented")

    def test_missing_envelope(self):
        self.assertEqual(self.inspect(None), "missing_or_invalid_envelope")

    def test_wrong_schema(self):
        self.assertEqual(self.inspect(replace(self.envelope, schema="wrong")), "unsupported_schema")

    def test_missing_issuer(self):
        self.assertEqual(self.inspect(replace(self.envelope, issuer="")), "missing_issuer_key_or_algorithm")

    def test_missing_key_id(self):
        self.assertEqual(self.inspect(replace(self.envelope, key_id="")), "missing_issuer_key_or_algorithm")

    def test_missing_algorithm(self):
        self.assertEqual(self.inspect(replace(self.envelope, algorithm="")), "missing_issuer_key_or_algorithm")

    def test_unsigned_fixture(self):
        self.assertEqual(self.inspect(replace(self.envelope, signature="")), "unsigned_or_incomplete_fixture")

    def test_missing_payload_digest(self):
        self.assertEqual(self.inspect(replace(self.envelope, signed_payload_digest="")), "unsigned_or_incomplete_fixture")

    def test_authority_mismatch(self):
        self.assertEqual(self.inspect(replace(self.envelope, authority_id="authority-b")), "authority_mismatch")

    def test_subject_mismatch(self):
        self.assertEqual(self.inspect(replace(self.envelope, subject_id="subject-b")), "subject_mismatch")

    def test_action_mismatch(self):
        self.assertEqual(self.inspect(replace(self.envelope, action="write")), "scope_mismatch")

    def test_resource_mismatch(self):
        self.assertEqual(self.inspect(replace(self.envelope, resource="record-b")), "scope_mismatch")

    def test_target_mismatch(self):
        self.assertEqual(self.inspect(replace(self.envelope, target_digest="target-b")), "target_mismatch")

    def test_mapping_mismatch(self):
        self.assertEqual(self.inspect(replace(self.envelope, mapping_digest="mapping-b")), "mapping_mismatch")

    def test_checkpoint_rollback(self):
        self.assertEqual(self.inspect(replace(self.envelope, checkpoint_sequence=6)), "checkpoint_rollback")

    def test_boolean_checkpoint_rejected(self):
        self.assertEqual(self.inspect(replace(self.envelope, checkpoint_sequence=True)), "invalid_checkpoint_sequence")

    def test_missing_checkpoint_digest(self):
        self.assertEqual(self.inspect(replace(self.envelope, checkpoint_digest="")), "missing_checkpoint_digest")

    def test_expired_checkpoint(self):
        self.assertEqual(self.inspect(replace(self.envelope, expires_epoch=150)), "stale_or_future_checkpoint")

    def test_future_observation(self):
        self.assertEqual(self.inspect(replace(self.envelope, observed_epoch=151)), "stale_or_future_checkpoint")


if __name__ == "__main__":
    unittest.main()
