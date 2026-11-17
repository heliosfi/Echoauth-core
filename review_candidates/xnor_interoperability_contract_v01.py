"""Synthetic-only interoperable XNOR evidence and authority mapping contract.

This module does NOT verify signatures, authenticate a mapping, read real keys,
or integrate with AuthorizationGateService. It tests structural correspondence.
"""

from dataclasses import dataclass
from enum import Enum


SCHEMA = "node-xnor.revocation-evidence.v0.1"
MAPPING_SCHEMA = "echoauth.xnor-authority-mapping.v0.1"


class ReviewState(str, Enum):
    HOLD = "HOLD"
    REJECT = "REJECT"
    MATCHED_FOR_REVIEW = "MATCHED_FOR_REVIEW"


@dataclass(frozen=True)
class XnorEvidenceEnvelopeV01:
    schema: str
    verifier_version: str
    verdict: str
    reason_codes: tuple[str, ...]
    target_fingerprint_digest: str
    revocation_record_digest: str
    trusted_checkpoint_digest: str | None
    observed_at: str
    evidence_source: str
    authority_granted: bool = False
    registry_mutation_authorized: bool = False
    execution_authorized: bool = False
    continuation_authorized: bool = False


@dataclass(frozen=True)
class AuthorityMappingV01:
    schema: str
    xnor_namespace: str
    target_fingerprint_digest: str
    target_role: str
    target_tier: str
    target_scope: str
    source_identity: str
    authority_record_id: str
    authority_source_id: str
    subject_id: str
    mapping_version: str
    mapping_digest: str
    approval_provenance_digest: str


@dataclass(frozen=True)
class InteropReview:
    state: ReviewState
    reason: str
    authority_granted: bool = False
    registry_mutation_authorized: bool = False
    execution_authorized: bool = False
    continuation_authorized: bool = False


def review_synthetic_interoperability(
    evidence: XnorEvidenceEnvelopeV01 | None,
    mapping: AuthorityMappingV01 | None,
    *,
    expected_authority_record_id: str,
    expected_target_digest: str,
) -> InteropReview:
    """Structural review only: MATCHED_FOR_REVIEW is never authorization."""
    if evidence is None or mapping is None:
        return InteropReview(ReviewState.HOLD, "missing_evidence_or_mapping")
    if not isinstance(evidence, XnorEvidenceEnvelopeV01) or not isinstance(mapping, AuthorityMappingV01):
        return InteropReview(ReviewState.REJECT, "invalid_type")
    if evidence.schema != SCHEMA or mapping.schema != MAPPING_SCHEMA:
        return InteropReview(ReviewState.REJECT, "schema_mismatch")
    if any((evidence.authority_granted, evidence.registry_mutation_authorized,
            evidence.execution_authorized, evidence.continuation_authorized)):
        return InteropReview(ReviewState.REJECT, "authorization_flag_true")
    if evidence.evidence_source != "synthetic-review":
        return InteropReview(ReviewState.REJECT, "non_synthetic_source")
    if evidence.verdict == "FAIL":
        return InteropReview(ReviewState.REJECT, "verifier_fail")
    if evidence.verdict != "PASS":
        return InteropReview(ReviewState.HOLD, "verifier_not_pass")
    if (mapping.target_fingerprint_digest != evidence.target_fingerprint_digest
            or mapping.target_fingerprint_digest != expected_target_digest
            or mapping.authority_record_id != expected_authority_record_id):
        return InteropReview(ReviewState.REJECT, "target_or_authority_mismatch")
    required = (
        evidence.verifier_version, evidence.revocation_record_digest,
        evidence.trusted_checkpoint_digest, evidence.observed_at,
        mapping.xnor_namespace, mapping.target_role, mapping.target_tier,
        mapping.target_scope, mapping.source_identity, mapping.authority_source_id,
        mapping.subject_id, mapping.mapping_version, mapping.mapping_digest,
        mapping.approval_provenance_digest,
    )
    if not all(required):
        return InteropReview(ReviewState.HOLD, "missing_required_provenance")
    # These are untrusted synthetic strings, not verified cryptographic facts.
    return InteropReview(ReviewState.MATCHED_FOR_REVIEW, "structural_match_only")
