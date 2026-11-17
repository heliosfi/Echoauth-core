"""Negative tests: cryptographic test-vector PASS is not issuer enrollment."""
import unittest

from review_candidates.xnor_ed25519_test_vector_verifier import make_test_envelope
from review_candidates.xnor_test_key_trust_boundary import (
    TrustReviewState, review_test_key_trust,
)

PAYLOAD = {
    "authority_id": "authority-1",
    "target_digest": "target-1",
    "mapping_digest": "mapping-1",
    "checkpoint_sequence": 10,
    "observed_epoch": 100,
    "expires_epoch": 200,
    "revoked": False,
}


class TestKeyTrustBoundaryTests(unittest.TestCase):
    def review(self, envelope=None, **overrides):
        kwargs = dict(
            expected_authority="authority-1",
            expected_target="target-1",
            expected_mapping="mapping-1",
            now=150,
            min_checkpoint=10,
        )
        kwargs.update(overrides)
        return review_test_key_trust(envelope, **kwargs)

    def assert_not_authorized(self, result):
        self.assertEqual(result.state, TrustReviewState.HOLD)
        self.assertFalse(result.authority_granted)
        self.assertFalse(result.execution_authorized)

    def test_valid_signature_without_registry_holds(self):
        self.assert_not_authorized(self.review(make_test_envelope(PAYLOAD)))

    def test_valid_signature_with_empty_registry_holds(self):
        self.assert_not_authorized(self.review(make_test_envelope(PAYLOAD), approved_registry={}))

    def test_caller_claimed_trusted_does_not_enroll(self):
        self.assert_not_authorized(self.review(make_test_envelope(PAYLOAD), claimed_trusted=True))

    def test_caller_supplied_matching_registry_does_not_enroll(self):
        self.assert_not_authorized(self.review(
            make_test_envelope(PAYLOAD),
            approved_registry={"test-only-issuer": {"test-only-key-v1": "claimed"}},
        ))

    def test_matching_registry_plus_claim_still_holds(self):
        self.assert_not_authorized(self.review(
            make_test_envelope(PAYLOAD),
            approved_registry={"test-only-issuer": {"test-only-key-v1": "claimed"}},
            claimed_trusted=True,
        ))

    def test_unknown_registry_issuer_holds(self):
        self.assert_not_authorized(self.review(
            make_test_envelope(PAYLOAD), approved_registry={"other": {"key": "x"}},
        ))

    def test_invalid_signature_holds_even_with_registry(self):
        envelope = make_test_envelope(PAYLOAD)
        envelope["signature"] = bytes(64)
        self.assert_not_authorized(self.review(
            envelope, approved_registry={"test-only-issuer": {"test-only-key-v1": "claimed"}},
        ))

    def test_wrong_authority_holds_even_with_registry(self):
        self.assert_not_authorized(self.review(
            make_test_envelope(PAYLOAD), expected_authority="authority-2",
            approved_registry={"test-only-issuer": {"test-only-key-v1": "claimed"}},
        ))

    def test_rollback_holds_even_with_registry(self):
        self.assert_not_authorized(self.review(
            make_test_envelope(PAYLOAD), min_checkpoint=11,
            approved_registry={"test-only-issuer": {"test-only-key-v1": "claimed"}},
        ))

    def test_missing_envelope_holds(self):
        self.assert_not_authorized(self.review())


if __name__ == "__main__":
    unittest.main()
