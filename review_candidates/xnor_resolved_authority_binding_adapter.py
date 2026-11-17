"""Isolated synthetic authority-binding adapter. Not production gate integration.

ResolvedAuthority must be provided by independent gate resolver, not by caller.
This module cannot authenticate that provenance and never grants authorization.
"""
from dataclasses import dataclass
from enum import Enum


class ReviewState(str, Enum):
    MATCHED_FOR_TEST = "MATCHED_FOR_TEST"
    HOLD = "HOLD"


@dataclass(frozen=True)
class ResolvedAuthority:
    authority_id: str
    grantor_id: str
    subject_id: str
    action: str
    resource: str
    target_digest: str
    mapping_digest: str


@dataclass(frozen=True)
class SignedCoverage:
    authority_id: str
    grantor_id: str
    subject_id: str
    action: str
    resource: str
    target_digest: str
    mapping_digest: str
    checkpoint_digest: str
    checkpoint_sequence: int
    signed_lineage_verified_for_test: bool
    revoked: bool


@dataclass(frozen=True)
class ReviewResult:
    state: ReviewState
    reason: str
    authority_granted: bool = False
    execution_authorized: bool = False


def bind_resolved_authority(resolved, coverage, *, commit_checkpoint_digest,
                            commit_checkpoint_sequence):
    def hold(reason):
        return ReviewResult(ReviewState.HOLD, reason)
    if not isinstance(resolved, ResolvedAuthority) or not isinstance(coverage, SignedCoverage):
        return hold("missing_resolved_authority_or_coverage")
    if coverage.signed_lineage_verified_for_test is not True:
        return hold("signed_lineage_not_verified")
    if coverage.revoked is not False:
        return hold("revoked_or_unknown")
    for field in ("authority_id", "grantor_id", "subject_id", "action", "resource",
                  "target_digest", "mapping_digest"):
        a, b = getattr(resolved, field), getattr(coverage, field)
        if not isinstance(a, str) or not a or a != b:
            return hold(field + "_mismatch")
    if not isinstance(coverage.checkpoint_digest, str) or not coverage.checkpoint_digest:
        return hold("missing_checkpoint_digest")
    if type(coverage.checkpoint_sequence) is not int or coverage.checkpoint_sequence < 0:
        return hold("invalid_checkpoint_sequence")
    if (coverage.checkpoint_digest != commit_checkpoint_digest
            or coverage.checkpoint_sequence != commit_checkpoint_sequence):
        return hold("checkpoint_changed_before_commit")
    return ReviewResult(ReviewState.MATCHED_FOR_TEST, "synthetic_binding_matched")
