"""Review-only, synthetic NODE XNOR revocation evidence boundary.

This module does not authenticate signatures, trust anchors, checkpoints, or
external sources. It cannot authorize actions or modify authority records.
It fails closed when required externally verified facts are missing.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EvidenceDisposition(str, Enum):
    HOLD = "hold"
    REJECT = "reject"
    REVIEWABLE = "reviewable"  # Evidence only; NEVER authorization.


@dataclass(frozen=True)
class SyntheticRevocationEvidence:
    schema: str
    verdict: str
    target_authority_record_id: str
    target_fingerprint_digest: str
    checkpoint_digest: str
    record_digest: str
    signature_verified: bool
    checkpoint_trusted: bool
    freshness_verified: bool
    binding_verified: bool
    synthetic_only: bool = True


@dataclass(frozen=True)
class EvidenceReview:
    disposition: EvidenceDisposition
    reason: str
    permission_granted: bool = False
    registry_mutation_authorized: bool = False
    execution_authorized: bool = False


def review_synthetic_revocation(
    evidence: SyntheticRevocationEvidence | None,
    *,
    expected_authority_record_id: str,
) -> EvidenceReview:
    """Classify a synthetic evidence envelope without producing permission.

    This is deliberately not a runtime consumer. The caller MUST NOT map
    REVIEWABLE to an authorization or an authority-state transition.
    """
    if evidence is None:
        return EvidenceReview(EvidenceDisposition.HOLD, "missing_evidence")
    if not isinstance(evidence, SyntheticRevocationEvidence):
        return EvidenceReview(EvidenceDisposition.REJECT, "invalid_evidence_type")
    if not evidence.synthetic_only:
        return EvidenceReview(EvidenceDisposition.REJECT, "real_evidence_not_supported")
    if evidence.schema != "node-xnor.revocation-evidence.v0.1":
        return EvidenceReview(EvidenceDisposition.REJECT, "unsupported_schema")
    if evidence.verdict == "FAIL":
        return EvidenceReview(EvidenceDisposition.REJECT, "verifier_fail")
    if evidence.verdict != "PASS":
        return EvidenceReview(EvidenceDisposition.HOLD, "verifier_not_pass")
    if not expected_authority_record_id or evidence.target_authority_record_id != expected_authority_record_id:
        return EvidenceReview(EvidenceDisposition.REJECT, "target_mismatch")
    if not all((evidence.target_fingerprint_digest, evidence.record_digest, evidence.checkpoint_digest)):
        return EvidenceReview(EvidenceDisposition.HOLD, "missing_digest")
    if not evidence.signature_verified:
        return EvidenceReview(EvidenceDisposition.HOLD, "signature_unverified")
    if not evidence.checkpoint_trusted:
        return EvidenceReview(EvidenceDisposition.HOLD, "checkpoint_untrusted")
    if not evidence.freshness_verified:
        return EvidenceReview(EvidenceDisposition.HOLD, "freshness_unverified")
    if not evidence.binding_verified:
        return EvidenceReview(EvidenceDisposition.HOLD, "binding_unverified")
    return EvidenceReview(EvidenceDisposition.REVIEWABLE, "synthetic_evidence_reviewable")
