"""Review-only transactional revocation checkpoint harness.

This is an isolated deterministic simulator, not an EchoAuth production gate,
authenticated source, cryptographic verifier or authorization implementation.
"""
from dataclasses import dataclass
from enum import Enum


class TransactionState(str, Enum):
    HOLD = "HOLD"
    REVOKED = "REVOKED"
    CLEAR_FOR_GATE_REVIEW = "CLEAR_FOR_GATE_REVIEW"


@dataclass(frozen=True)
class SyntheticCheckpoint:
    authority_id: str
    target_digest: str
    checkpoint_sequence: int
    checkpoint_digest: str
    mapping_digest: str
    observed_epoch: int
    expires_epoch: int
    revoked: bool
    trusted_for_test: bool = False


@dataclass(frozen=True)
class TransactionResult:
    state: TransactionState
    reason: str
    authority_granted: bool = False
    execution_authorized: bool = False
    continuation_authorized: bool = False


class SyntheticTransactionHarness:
    def __init__(self, provider):
        self.provider = provider

    def evaluate(self, *, expected_authority: str, expected_target: str,
                 preflight_epoch: int, commit_epoch: int):
        hold = lambda reason: TransactionResult(TransactionState.HOLD, reason)
        try:
            before = self.provider.read_checkpoint()
        except Exception:
            return hold("preflight_provider_error")
        if not self._valid(before, expected_authority, expected_target, preflight_epoch):
            return hold("invalid_preflight_coverage")
        if before.revoked:
            return TransactionResult(TransactionState.REVOKED, "preflight_revoked")
        # Simulates the independent final-commit recheck. No actual gate call.
        try:
            after = self.provider.read_checkpoint()
        except Exception:
            return hold("commit_provider_error")
        if not self._valid(after, expected_authority, expected_target, commit_epoch):
            return hold("invalid_commit_coverage")
        if after.revoked:
            return TransactionResult(TransactionState.REVOKED, "revoked_before_commit")
        if after.checkpoint_sequence < before.checkpoint_sequence:
            return hold("checkpoint_rollback")
        if (after.checkpoint_sequence != before.checkpoint_sequence or
                after.checkpoint_digest != before.checkpoint_digest or
                after.mapping_digest != before.mapping_digest or
                after.authority_id != before.authority_id or
                after.target_digest != before.target_digest):
            return hold("snapshot_changed_requires_reassessment")
        return TransactionResult(TransactionState.CLEAR_FOR_GATE_REVIEW, "stable_synthetic_snapshot")

    @staticmethod
    def _valid(s, authority, target, at):
        return (
            isinstance(s, SyntheticCheckpoint)
            and s.trusted_for_test
            and s.authority_id == authority
            and s.target_digest == target
            and bool(s.checkpoint_digest)
            and bool(s.mapping_digest)
            and isinstance(s.checkpoint_sequence, int)
            and not isinstance(s.checkpoint_sequence, bool)
            and s.checkpoint_sequence >= 0
            and s.observed_epoch <= at < s.expires_epoch
        )
