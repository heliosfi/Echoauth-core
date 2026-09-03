"""Crossroad Execution Gate interface boundary.

Specification: governance/ceg.md

This module defines only the non-operational interface shape for CEG. CEG
sequences one already-authorized action inside a bounded runtime envelope. It
does not resolve authority, create permission, dispatch consequential work,
activate runtime behavior, or infer continuation authority.
"""

from __future__ import annotations

from typing import Protocol


class CrossroadExecutionGate(Protocol):
    """Non-operational interface for bounded authorized execution sequencing.

    Implementations must preserve a single-action boundary, reject replay,
    validate payload and channel integrity, respect execution locks, validate
    invariants, and emit execution audit evidence. This interface does not
    grant authority or permission and does not itself execute consequential
    actions.
    """

    def sequence_authorized_execution(
        self,
        *,
        authorization_result: object,
        execution_token: object,
        runtime_envelope: object,
    ) -> object:
        """Sequence one previously authorized action without dispatching it here."""
        ...

    def validate_single_action(self, *, execution_token: object) -> bool:
        """Validate that the token represents exactly one authorized action."""
        ...

    def validate_replay_protection(self, *, execution_token: object) -> bool:
        """Validate nonce/token freshness and reject replay or duplicate use."""
        ...

    def validate_payload_integrity(
        self, *, execution_token: object, payload: object
    ) -> bool:
        """Validate that the supplied payload matches the authorized payload."""
        ...

    def validate_channel_integrity(self, *, channel: object) -> bool:
        """Validate that the execution channel is available and acceptable."""
        ...

    def acquire_execution_lock(self, *, execution_token: object) -> object:
        """Describe the exclusive lock-acquisition boundary for one action."""
        ...

    def validate_invariants(
        self, *, execution_token: object, runtime_envelope: object
    ) -> bool:
        """Validate required invariants before any downstream execution crossing."""
        ...

    def emit_execution_audit(self, *, event: object) -> None:
        """Describe the audit-emission boundary for CEG sequencing evidence."""
        ...


__all__ = ["CrossroadExecutionGate"]
