"""Isolated Ed25519 test-vector verifier, NOT a production trust provider.

Test-only deterministic seed; never use this seed/key for real signatures.
A valid test signature is only VERIFIED_FOR_TEST, never authorization.
"""
import json
from dataclasses import dataclass
from enum import Enum
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

DOMAIN = b"NODE-XNOR-REVOCATION-TEST-V0.1\\x00".replace(b"\\x00", b"\x00")
TEST_SEED = bytes(range(32))
TEST_ISSUER = "test-only-issuer"
TEST_KEY_ID = "test-only-key-v1"


class Verdict(str, Enum):
    VERIFIED_FOR_TEST = "VERIFIED_FOR_TEST"
    HOLD = "HOLD"


@dataclass(frozen=True)
class Result:
    verdict: Verdict
    reason: str
    authority_granted: bool = False
    execution_authorized: bool = False


def canonical_bytes(payload):
    if not isinstance(payload, dict):
        raise ValueError("payload_not_object")
    if any(not isinstance(k, str) for k in payload):
        raise ValueError("nonstring_key")
    return json.dumps(payload, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def make_test_envelope(payload):
    key = Ed25519PrivateKey.from_private_bytes(TEST_SEED)
    body = canonical_bytes(payload)
    return {"issuer": TEST_ISSUER, "key_id": TEST_KEY_ID,
            "algorithm": "Ed25519", "payload": body,
            "signature": key.sign(DOMAIN + body)}


def verify_test_envelope(envelope, *, expected_authority, expected_target,
                         expected_mapping, now, min_checkpoint):
    def hold(reason):
        return Result(Verdict.HOLD, reason)
    if not isinstance(envelope, dict):
        return hold("missing_envelope")
    if (envelope.get("issuer"), envelope.get("key_id"),
        envelope.get("algorithm")) != (TEST_ISSUER, TEST_KEY_ID, "Ed25519"):
        return hold("untrusted_test_issuer_key_or_algorithm")
    body, signature = envelope.get("payload"), envelope.get("signature")
    if not isinstance(body, bytes) or not isinstance(signature, bytes):
        return hold("invalid_wire_types")
    if len(body) > 8192 or len(signature) != 64:
        return hold("invalid_wire_size")
    try:
        def reject_duplicates(pairs):
            obj = {}
            for k, v in pairs:
                if k in obj:
                    raise ValueError("duplicate_key")
                obj[k] = v
            return obj
        payload = json.loads(body.decode("utf-8"), object_pairs_hook=reject_duplicates,
                             parse_constant=lambda x: (_ for _ in ()).throw(ValueError("nonfinite")))
        if canonical_bytes(payload) != body:
            return hold("noncanonical_payload")
    except (ValueError, UnicodeError, TypeError):
        return hold("invalid_payload")
    try:
        public = Ed25519PrivateKey.from_private_bytes(TEST_SEED).public_key()
        public.verify(signature, DOMAIN + body)
    except InvalidSignature:
        return hold("invalid_signature")
    if payload.get("authority_id") != expected_authority:
        return hold("authority_mismatch")
    if payload.get("target_digest") != expected_target:
        return hold("target_mismatch")
    if payload.get("mapping_digest") != expected_mapping:
        return hold("mapping_mismatch")
    seq = payload.get("checkpoint_sequence")
    if type(seq) is not int or seq < min_checkpoint:
        return hold("invalid_or_rollback_checkpoint")
    observed, expiry = payload.get("observed_epoch"), payload.get("expires_epoch")
    if type(observed) is not int or type(expiry) is not int or observed > now or expiry <= now:
        return hold("invalid_or_stale_time")
    if payload.get("revoked") is not False:
        return hold("revoked_or_missing_coverage")
    return Result(Verdict.VERIFIED_FOR_TEST, "test_signature_and_binding_valid")
