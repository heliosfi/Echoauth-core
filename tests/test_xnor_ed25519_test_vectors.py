import unittest
from copy import deepcopy
from review_candidates.xnor_ed25519_test_vector_verifier import (
    DOMAIN, TEST_SEED, Verdict, canonical_bytes, make_test_envelope, verify_test_envelope,
)
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


class Ed25519VectorTests(unittest.TestCase):
    def setUp(self):
        self.payload = dict(authority_id="authority-a", target_digest="target-a",
                            mapping_digest="mapping-a", checkpoint_sequence=7,
                            observed_epoch=100, expires_epoch=200, revoked=False)

    def check(self, envelope):
        return verify_test_envelope(envelope, expected_authority="authority-a",
                                    expected_target="target-a", expected_mapping="mapping-a",
                                    now=150, min_checkpoint=7)

    def test_valid_signature_is_test_only_not_authority(self):
        result = self.check(make_test_envelope(self.payload))
        self.assertEqual(result.verdict, Verdict.VERIFIED_FOR_TEST)
        self.assertFalse(result.authority_granted)
        self.assertFalse(result.execution_authorized)

    def test_signature_mutation_holds(self):
        e = make_test_envelope(self.payload)
        e["signature"] = bytes([e["signature"][0] ^ 1]) + e["signature"][1:]
        self.assertEqual(self.check(e).reason, "invalid_signature")

    def test_payload_mutation_holds(self):
        e = make_test_envelope(self.payload)
        e["payload"] = e["payload"].replace(b"target-a", b"target-b")
        self.assertEqual(self.check(e).reason, "invalid_signature")

    def test_wrong_issuer_holds(self):
        e = make_test_envelope(self.payload); e["issuer"] = "other"
        self.assertEqual(self.check(e).verdict, Verdict.HOLD)

    def test_wrong_key_id_holds(self):
        e = make_test_envelope(self.payload); e["key_id"] = "other"
        self.assertEqual(self.check(e).verdict, Verdict.HOLD)

    def test_algorithm_substitution_holds(self):
        e = make_test_envelope(self.payload); e["algorithm"] = "none"
        self.assertEqual(self.check(e).verdict, Verdict.HOLD)

    def test_wrong_domain_signature_holds(self):
        e = make_test_envelope(self.payload)
        e["signature"] = Ed25519PrivateKey.from_private_bytes(TEST_SEED).sign(b"OTHER" + e["payload"])
        self.assertEqual(self.check(e).reason, "invalid_signature")

    def test_noncanonical_json_holds(self):
        e = make_test_envelope(self.payload)
        e["payload"] = b'{ "authority_id": "authority-a" }'
        e["signature"] = Ed25519PrivateKey.from_private_bytes(TEST_SEED).sign(DOMAIN + e["payload"])
        self.assertEqual(self.check(e).reason, "noncanonical_payload")

    def test_duplicate_key_holds(self):
        e = make_test_envelope(self.payload)
        e["payload"] = b'{"authority_id":"a","authority_id":"b"}'
        e["signature"] = Ed25519PrivateKey.from_private_bytes(TEST_SEED).sign(DOMAIN + e["payload"])
        self.assertEqual(self.check(e).reason, "invalid_payload")

    def test_wrong_authority_holds(self):
        p = dict(self.payload, authority_id="authority-b")
        self.assertEqual(self.check(make_test_envelope(p)).reason, "authority_mismatch")

    def test_wrong_target_holds(self):
        p = dict(self.payload, target_digest="target-b")
        self.assertEqual(self.check(make_test_envelope(p)).reason, "target_mismatch")

    def test_wrong_mapping_holds(self):
        p = dict(self.payload, mapping_digest="mapping-b")
        self.assertEqual(self.check(make_test_envelope(p)).reason, "mapping_mismatch")

    def test_checkpoint_rollback_holds(self):
        p = dict(self.payload, checkpoint_sequence=6)
        self.assertEqual(self.check(make_test_envelope(p)).reason, "invalid_or_rollback_checkpoint")

    def test_boolean_checkpoint_holds(self):
        p = dict(self.payload, checkpoint_sequence=True)
        self.assertEqual(self.check(make_test_envelope(p)).verdict, Verdict.HOLD)

    def test_expired_holds(self):
        p = dict(self.payload, expires_epoch=150)
        self.assertEqual(self.check(make_test_envelope(p)).reason, "invalid_or_stale_time")

    def test_future_observation_holds(self):
        p = dict(self.payload, observed_epoch=151)
        self.assertEqual(self.check(make_test_envelope(p)).verdict, Verdict.HOLD)

    def test_revoked_holds(self):
        p = dict(self.payload, revoked=True)
        self.assertEqual(self.check(make_test_envelope(p)).reason, "revoked_or_missing_coverage")

    def test_missing_coverage_holds(self):
        p = dict(self.payload); del p["revoked"]
        self.assertEqual(self.check(make_test_envelope(p)).verdict, Verdict.HOLD)

    def test_missing_signature_holds(self):
        e = make_test_envelope(self.payload); del e["signature"]
        self.assertEqual(self.check(e).verdict, Verdict.HOLD)

    def test_oversized_payload_holds(self):
        e = make_test_envelope(self.payload); e["payload"] = b"x" * 8193
        self.assertEqual(self.check(e).reason, "invalid_wire_size")


if __name__ == "__main__":
    unittest.main()
