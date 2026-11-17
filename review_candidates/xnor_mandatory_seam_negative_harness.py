"""Synthetic-only mandatory revocation seam contract.

No production import, crypto verification, trusted keys, actual gate integration,
or authorization. All results are review classifications, never permission.
"""
from dataclasses import dataclass
from enum import Enum


class ReviewDisposition(str, Enum):
    HOLD = "HOLD"
    CONTINUE_REVIEW = "CONTINUE_REVIEW"


@dataclass(frozen=True)
class SyntheticCheckpoint:
    issuer_known: bool = False
    signature_valid: bool = False
    lineage_valid: bool = False
    fresh: bool = False
    mapping_valid: bool = False
    authority_id: str = ""
    revoked: bool = False
    source_available: bool = False
    snapshot_stable: bool = False


@dataclass(frozen=True)
class ReviewResult:
    disposition: ReviewDisposition
    reason: str
    authority_granted: bool = False
    execution_authorized: bool = False


def review_mandatory_seam(*, resolved_authority_id, checkpoint, independent_gate_allows):
    """Classify synthetic evidence; CONTINUE_REVIEW never means AUTHORIZED.

    resolved_authority_id must originate from an independently selected
    authority resolver in a future implementation, never request context.
    """
    if not resolved_authority_id:
        return ReviewResult(ReviewDisposition.HOLD, "missing_resolver_authority")
    if checkpoint is None:
        return ReviewResult(ReviewDisposition.HOLD, "missing_checkpoint")
    for field, reason in (
        ("source_available", "source_unavailable"),
        ("issuer_known", "unknown_issuer"),
        ("signature_valid", "invalid_signature"),
        ("lineage_valid", "invalid_lineage"),
        ("fresh", "stale_checkpoint"),
        ("mapping_valid", "invalid_mapping"),
        ("snapshot_stable", "unstable_snapshot"),
    ):
        if getattr(checkpoint, field, None) is not True:
            return ReviewResult(ReviewDisposition.HOLD, reason)
    if checkpoint.authority_id != resolved_authority_id:
        return ReviewResult(ReviewDisposition.HOLD, "authority_mismatch")
    if checkpoint.revoked is True:
        return ReviewResult(ReviewDisposition.HOLD, "effective_revocation")
    if checkpoint.revoked is not False:
        return ReviewResult(ReviewDisposition.HOLD, "unknown_revocation_state")
    if independent_gate_allows is not True:
        return ReviewResult(ReviewDisposition.HOLD, "independent_gate_denial")
    return ReviewResult(ReviewDisposition.CONTINUE_REVIEW, "synthetic_clear_not_permission")
