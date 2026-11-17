"""Review-only trust gate: valid public test signatures never establish enrollment.

No production trust registry, source verification, authority, or execution.
"""
from dataclasses import dataclass
from enum import Enum

from review_candidates.xnor_ed25519_test_vector_verifier import (
    Verdict, verify_test_envelope,
)


class TrustReviewState(str, Enum):
    HOLD = "HOLD"


@dataclass(frozen=True)
class TrustReviewResult:
    state: TrustReviewState
    reason: str
    authority_granted: bool = False
    execution_authorized: bool = False


def review_test_key_trust(envelope, *, expected_authority, expected_target,
                          expected_mapping, now, min_checkpoint,
                          approved_registry=None, claimed_trusted=False):
    """A test vector and caller assertion cannot be a production trust anchor.

    The optional registry is only an illustrative input; this review function
    intentionally never converts it into real issuer enrollment.
    """
    verification = verify_test_envelope(
        envelope, expected_authority=expected_authority,
        expected_target=expected_target, expected_mapping=expected_mapping,
        now=now, min_checkpoint=min_checkpoint,
    )
    if verification.verdict is not Verdict.VERIFIED_FOR_TEST:
        return TrustReviewResult(TrustReviewState.HOLD,
                                 "test_vector_invalid:" + verification.reason)
    if not isinstance(approved_registry, dict) or not approved_registry:
        return TrustReviewResult(TrustReviewState.HOLD, "no_approved_trust_registry")
    # Even a matching caller-supplied registry or claimed_trusted=True cannot
    # enroll keys, verify registry provenance, or authorize production use.
    return TrustReviewResult(TrustReviewState.HOLD,
                             "registry_provenance_and_enrollment_unverified")
