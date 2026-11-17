"""Review-only signed-envelope *shape* and binding negative-test classifier.

This is NOT signature verification. No keys, cryptographic library or trusted
source are present. All fixture envelopes must HOLD, even if structurally valid.
"""
from dataclasses import dataclass
from enum import Enum


class ReviewVerdict(str, Enum):
    HOLD = "HOLD"


@dataclass(frozen=True)
class SyntheticEnvelope:
    schema: str
    issuer: str
    key_id: str
    algorithm: str
    signed_payload_digest: str
    signature: str
    authority_id: str
    subject_id: str
    action: str
    resource: str
    target_digest: str
    mapping_digest: str
    checkpoint_sequence: int
    checkpoint_digest: str
    observed_epoch: int
    expires_epoch: int


@dataclass(frozen=True)
class ReviewResult:
    verdict: ReviewVerdict
    reason: str
    signature_verified: bool = False
    authority_granted: bool = False
    execution_authorized: bool = False


def inspect_fixture(envelope, *, expected_authority, expected_subject,
                    expected_action, expected_resource, expected_target,
                    expected_mapping, now, min_checkpoint):
    def hold(reason):
        return ReviewResult(ReviewVerdict.HOLD, reason)
    if not isinstance(envelope, SyntheticEnvelope):
        return hold("missing_or_invalid_envelope")
    if envelope.schema != "node-xnor.signed-revocation.v0.1":
        return hold("unsupported_schema")
    if not envelope.issuer or not envelope.key_id or not envelope.algorithm:
        return hold("missing_issuer_key_or_algorithm")
    if not envelope.signed_payload_digest or not envelope.signature:
        return hold("unsigned_or_incomplete_fixture")
    if envelope.authority_id != expected_authority:
        return hold("authority_mismatch")
    if envelope.subject_id != expected_subject:
        return hold("subject_mismatch")
    if envelope.action != expected_action or envelope.resource != expected_resource:
        return hold("scope_mismatch")
    if envelope.target_digest != expected_target:
        return hold("target_mismatch")
    if envelope.mapping_digest != expected_mapping:
        return hold("mapping_mismatch")
    if not isinstance(envelope.checkpoint_sequence, int) or isinstance(envelope.checkpoint_sequence, bool):
        return hold("invalid_checkpoint_sequence")
    if envelope.checkpoint_sequence < min_checkpoint:
        return hold("checkpoint_rollback")
    if not envelope.checkpoint_digest:
        return hold("missing_checkpoint_digest")
    if envelope.observed_epoch > now or envelope.expires_epoch <= now:
        return hold("stale_or_future_checkpoint")
    # A structurally plausible envelope still has no trusted verification.
    return hold("cryptographic_and_trust_verification_not_implemented")
