"""Isolated synthetic revocation-aware positive-cache replay harness.

Not wired to EchoAuth's real decision cache or gate. Synthetic checkpoints
do not establish cryptographic authenticity or real-world revocation coverage.
"""
from dataclasses import dataclass
from enum import Enum


class ReplayState(str, Enum):
    REVIEW_CANDIDATE = "REVIEW_CANDIDATE"
    HOLD = "HOLD"
    REVOKED = "REVOKED"


@dataclass(frozen=True)
class Snapshot:
    authority_id: str
    target_digest: str
    checkpoint_sequence: int
    checkpoint_digest: str
    mapping_digest: str
    valid_until: int
    revoked: bool
    attested_for_test: bool = False


@dataclass(frozen=True)
class ReplayResult:
    state: ReplayState
    reason: str
    reused_positive: bool = False
    authority_granted: bool = False
    execution_authorized: bool = False


class SyntheticPositiveCache:
    """Cache candidates only, never real AuthorizationDecision objects."""
    def __init__(self):
        self._candidate = None

    def store(self, snapshot: Snapshot):
        if snapshot.attested_for_test and not snapshot.revoked:
            self._candidate = snapshot

    def evaluate(self, provider, *, authority_id: str, target_digest: str, now: int):
        hold = lambda reason: ReplayResult(ReplayState.HOLD, reason)
        try:
            current = provider.read()
        except Exception:
            return hold("provider_unavailable")
        if not isinstance(current, Snapshot) or not current.attested_for_test:
            return hold("untrusted_or_missing_snapshot")
        if current.authority_id != authority_id or current.target_digest != target_digest:
            return hold("authority_or_target_mismatch")
        if (not current.checkpoint_digest or not current.mapping_digest or
                current.checkpoint_sequence < 0 or current.valid_until <= now):
            return hold("invalid_or_stale_checkpoint")
        if current.revoked:
            return ReplayResult(ReplayState.REVOKED, "revoked_current_checkpoint")
        previous = self._candidate
        if previous is None:
            return ReplayResult(ReplayState.REVIEW_CANDIDATE, "fresh_review_required")
        if (previous.authority_id != current.authority_id or
                previous.target_digest != current.target_digest or
                previous.mapping_digest != current.mapping_digest):
            return hold("cached_binding_mismatch")
        if current.checkpoint_sequence < previous.checkpoint_sequence:
            return hold("checkpoint_rollback")
        if (current.checkpoint_sequence != previous.checkpoint_sequence or
                current.checkpoint_digest != previous.checkpoint_digest):
            return ReplayResult(ReplayState.REVIEW_CANDIDATE, "checkpoint_changed_reassess")
        # Even an unchanged checkpoint cannot prove freshness or atomic commit.
        # Never reuse a cached positive authorization in this review harness.
        return ReplayResult(ReplayState.REVIEW_CANDIDATE, "same_checkpoint_reassess")
