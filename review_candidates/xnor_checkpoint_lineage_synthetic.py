"""Review-only synthetic checkpoint lineage consistency classifier.

No authenticated transparency log, signed roots, network provider or gate wiring.
"""
from dataclasses import dataclass
from enum import Enum


class LineageState(str, Enum):
    CONSISTENT_FOR_TEST = "CONSISTENT_FOR_TEST"
    HOLD = "HOLD"


@dataclass(frozen=True)
class Checkpoint:
    source_id: str
    epoch: int
    sequence: int
    digest: str
    parent_digest: str
    observed_at: int
    expires_at: int


@dataclass(frozen=True)
class LineageResult:
    state: LineageState
    reason: str
    authority_granted: bool = False
    execution_authorized: bool = False


def check_lineage(previous, candidate, *, expected_source, now, max_age):
    def hold(reason):
        return LineageResult(LineageState.HOLD, reason)
    if not isinstance(candidate, Checkpoint):
        return hold("missing_checkpoint")
    if candidate.source_id != expected_source or not candidate.source_id:
        return hold("source_mismatch")
    if any(type(v) is not int for v in (candidate.epoch, candidate.sequence,
                                       candidate.observed_at, candidate.expires_at)):
        return hold("invalid_numeric_fields")
    if candidate.epoch < 0 or candidate.sequence < 0:
        return hold("negative_epoch_or_sequence")
    if not candidate.digest:
        return hold("missing_digest")
    if candidate.observed_at > now or candidate.expires_at <= now or now - candidate.observed_at > max_age:
        return hold("stale_or_future_checkpoint")
    if previous is not None:
        if not isinstance(previous, Checkpoint):
            return hold("invalid_previous_checkpoint")
        if previous.source_id != candidate.source_id:
            return hold("source_changed")
        if candidate.epoch < previous.epoch:
            return hold("epoch_rollback")
        if candidate.epoch > previous.epoch:
            return hold("epoch_transition_requires_trust_review")
        if candidate.sequence < previous.sequence:
            return hold("sequence_rollback")
        if candidate.sequence == previous.sequence:
            if candidate.digest != previous.digest:
                return hold("same_sequence_equivocation")
            return LineageResult(LineageState.CONSISTENT_FOR_TEST, "same_checkpoint_for_test")
        if candidate.sequence != previous.sequence + 1:
            return hold("lineage_gap_requires_proof")
        if candidate.parent_digest != previous.digest:
            return hold("broken_parent_link")
    return LineageResult(LineageState.CONSISTENT_FOR_TEST, "synthetic_lineage_consistent")
