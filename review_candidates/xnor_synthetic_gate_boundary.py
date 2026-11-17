"""Review-only fail-closed boundary in front of existing EchoAuth gate.

This wrapper is NOT installed in production. Synthetic provider decisions never
authorize. A trusted CLEAR_FOR_REVIEW fixture merely allows ordinary gate checks.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any

from review_candidates.xnor_synthetic_fail_closed_provider import CoverageState


class BoundaryState(str, Enum):
    BLOCKED_HOLD = "BLOCKED_HOLD"
    BLOCKED_REVOKED = "BLOCKED_REVOKED"
    GATE_EVALUATED = "GATE_EVALUATED"


@dataclass(frozen=True)
class BoundaryResult:
    state: BoundaryState
    reason: str
    gate_decision: Any = None
    authority_granted_by_evidence: bool = False
    execution_authorized: bool = False
    continuation_authorized: bool = False


class SyntheticGateBoundary:
    def __init__(self, provider, gate):
        self.provider = provider
        self.gate = gate

    def evaluate(self, request, *, authority_record_id: str,
                 target_digest: str, now_epoch: int) -> BoundaryResult:
        try:
            coverage = self.provider.check(
                authority_record_id=authority_record_id,
                target_digest=target_digest,
                now_epoch=now_epoch,
            )
        except Exception:
            return BoundaryResult(BoundaryState.BLOCKED_HOLD, "provider_error")
        if coverage.state == CoverageState.REVOKED:
            return BoundaryResult(BoundaryState.BLOCKED_REVOKED, coverage.reason)
        if coverage.state != CoverageState.CLEAR_FOR_REVIEW:
            return BoundaryResult(BoundaryState.BLOCKED_HOLD, coverage.reason)
        # A structural fixture match never substitutes for independent gate checks.
        return BoundaryResult(
            BoundaryState.GATE_EVALUATED, "gate_evaluated",
            gate_decision=self.gate.authorize(request),
        )
