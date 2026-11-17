"""Synthetic-only exact-authority binding boundary.

This review fixture requires a resolver-derived binding independent of caller
supplied provider keys. It is NOT a production trusted resolver, and no real
cryptographic or gate enforcement is claimed.
"""
from dataclasses import dataclass
from review_candidates.xnor_synthetic_fail_closed_provider import CoverageState
from review_candidates.xnor_synthetic_gate_boundary import BoundaryResult, BoundaryState


@dataclass(frozen=True)
class SyntheticResolvedAuthority:
    authority_record_id: str
    target_fingerprint_digest: str
    subject_id: str
    action: str
    resource: str
    resolver_attested_for_test: bool = False


class SyntheticResolvedAuthorityBoundary:
    def __init__(self, resolver, provider, gate):
        self.resolver = resolver
        self.provider = provider
        self.gate = gate

    def evaluate(self, request, *, now_epoch: int):
        blocked = lambda reason: BoundaryResult(BoundaryState.BLOCKED_HOLD, reason)
        try:
            binding = self.resolver.resolve_binding(request)
        except Exception:
            return blocked("resolver_unavailable")
        if not isinstance(binding, SyntheticResolvedAuthority):
            return blocked("missing_or_ambiguous_resolved_authority")
        if not binding.resolver_attested_for_test:
            return blocked("untrusted_synthetic_resolver")
        if not all((binding.authority_record_id, binding.target_fingerprint_digest)):
            return blocked("missing_resolved_binding")
        if (binding.subject_id != request.subject_id or
                binding.action != request.action or
                binding.resource != request.resource):
            return blocked("resolved_request_scope_mismatch")
        try:
            coverage = self.provider.check(
                authority_record_id=binding.authority_record_id,
                target_digest=binding.target_fingerprint_digest,
                now_epoch=now_epoch,
            )
        except Exception:
            return blocked("provider_unavailable")
        if coverage.state == CoverageState.REVOKED:
            return BoundaryResult(BoundaryState.BLOCKED_REVOKED, coverage.reason)
        if coverage.state != CoverageState.CLEAR_FOR_REVIEW:
            return blocked(coverage.reason)
        # Still only a test-only boundary. Production must bind the actual gate
        # resolution to the SAME trusted snapshot, atomically.
        return BoundaryResult(
            BoundaryState.GATE_EVALUATED, "synthetic_resolved_binding_checked",
            gate_decision=self.gate.authorize(request),
        )
