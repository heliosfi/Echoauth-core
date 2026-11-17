"""Isolated review-only facade. Caller must NOT use this as a production gate.

This facade consumes a pre-captured real resolver observation. It does not prove
atomicity, trust, bypass prevention, or authoritative resolver provenance.
"""
from dataclasses import dataclass
from enum import Enum


class FacadeState(str, Enum):
    BLOCKED_FOR_REVIEW = "BLOCKED_FOR_REVIEW"
    FORWARDED_FOR_REVIEW = "FORWARDED_FOR_REVIEW"


@dataclass(frozen=True)
class FacadeResult:
    state: FacadeState
    reason: str
    gate_decision: object = None
    authority_granted: bool = False
    execution_authorized: bool = False


def evaluate_facade(*, observation, gate, request):
    """Only a matching isolated observation permits invoking the real gate.

    The result does not assert authorization, even when the underlying gate
    returns AUTHORIZED. Real integration requires mandatory internal wiring.
    """
    if (observation is None or getattr(observation, "state", None) is None
            or getattr(observation.state, "value", None) != "MATCHED_FOR_REVIEW"):
        return FacadeResult(FacadeState.BLOCKED_FOR_REVIEW, "coverage_hold")
    try:
        decision = gate.authorize(request)
    except Exception:
        return FacadeResult(FacadeState.BLOCKED_FOR_REVIEW, "gate_dependency_failed")
    return FacadeResult(FacadeState.FORWARDED_FOR_REVIEW,
                        "synthetic_coverage_forwarded_to_independent_gate",
                        gate_decision=decision)
