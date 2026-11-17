"""Synthetic-only fail-closed revocation provider contract.

This module has no production gate wiring, cryptography, network, registry
access, or authorization side effects. Attested below means a test fixture
assertion, NEVER an independently authenticated fact.
"""
from dataclasses import dataclass
from enum import Enum


class CoverageState(str, Enum):
    CLEAR_FOR_REVIEW = "CLEAR_FOR_REVIEW"
    REVOKED = "REVOKED"
    HOLD = "HOLD"


@dataclass(frozen=True)
class SyntheticSnapshot:
    authority_record_id: str
    target_fingerprint_digest: str
    mapping_authority_record_id: str
    mapping_target_digest: str
    provider_identity: str
    checkpoint_digest: str
    mapping_digest: str
    observed_at_epoch: int
    expires_at_epoch: int
    effective_revoked: bool
    synthetic_only: bool = True
    source_attested_for_test: bool = False
    checkpoint_monotonic_for_test: bool = False
    mapping_attested_for_test: bool = False


@dataclass(frozen=True)
class CoverageDecision:
    state: CoverageState
    reason: str
    authority_granted: bool = False
    execution_authorized: bool = False
    continuation_authorized: bool = False
    registry_mutation_authorized: bool = False


class SyntheticFailClosedProvider:
    """Fixture-backed decision: no real trust anchor or authorization capability."""

    def __init__(self, snapshot: SyntheticSnapshot | None, *, unavailable=False):
        self.snapshot = snapshot
        self.unavailable = unavailable

    def check(self, *, authority_record_id: str, target_digest: str,
              now_epoch: int) -> CoverageDecision:
        hold = lambda reason: CoverageDecision(CoverageState.HOLD, reason)
        if self.unavailable:
            return hold("provider_unavailable")
        s = self.snapshot
        if s is None:
            return hold("missing_snapshot")
        if not isinstance(s, SyntheticSnapshot) or not s.synthetic_only:
            return hold("invalid_or_non_synthetic_snapshot")
        if (not s.provider_identity or not s.checkpoint_digest or not s.mapping_digest):
            return hold("missing_provenance")
        if not all((s.source_attested_for_test, s.checkpoint_monotonic_for_test,
                    s.mapping_attested_for_test)):
            return hold("untrusted_synthetic_assertion")
        if (s.authority_record_id != authority_record_id
                or s.mapping_authority_record_id != authority_record_id
                or s.target_fingerprint_digest != target_digest
                or s.mapping_target_digest != target_digest):
            return hold("authority_or_mapping_mismatch")
        if (s.observed_at_epoch > now_epoch or s.expires_at_epoch <= now_epoch
                or s.expires_at_epoch <= s.observed_at_epoch):
            return hold("stale_or_invalid_time")
        if s.effective_revoked:
            return CoverageDecision(CoverageState.REVOKED, "synthetic_effective_revocation")
        return CoverageDecision(CoverageState.CLEAR_FOR_REVIEW, "synthetic_coverage_only")
