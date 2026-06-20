"""Sprint 2L validation-only Runtime State Machine tests."""

from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.runtime import (
    RUNTIME_STATE_GRAPH,
    RuntimeState,
    RuntimeStateMachine,
    RuntimeTransition,
    RuntimeTransitionRequest,
)


class RuntimeStateMachineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.audit = InMemoryAuditLogRepository()
        self.machine = RuntimeStateMachine(
            self.audit,
            audit_chain_id="runtime-state-audit",
            clock=lambda: datetime(2026, 6, 19, 16, 0, tzinfo=timezone.utc),
        )

    def _request(
        self,
        current: RuntimeState,
        transition: RuntimeTransition,
        requested: RuntimeState,
        *,
        suffix: str = "1",
    ) -> RuntimeTransitionRequest:
        return RuntimeTransitionRequest(
            transition_request_id=f"transition-{suffix}",
            request_id="request-1",
            current_state=current,
            transition=transition,
            requested_state=requested,
            actor_id="runtime-validator-test",
            reason=f"test_{transition.value}",
            evidence={"source": suffix},
            occurred_at="2026-06-19T15:59:00Z",
        )

    def test_canonical_state_vocabulary(self) -> None:
        self.assertEqual(
            {state.name for state in RuntimeState},
            {
                "REQUESTED",
                "AUTHORIZED",
                "REFUSED",
                "ESCALATED",
                "UNDER_REVIEW",
                "OVERRIDDEN",
                "READY",
                "EXECUTION_BLOCKED",
                "EXPIRED",
                "HALTED",
            },
        )

    def test_every_enumerated_graph_edge_is_valid(self) -> None:
        self.assertEqual(len(RUNTIME_STATE_GRAPH), 33)
        for index, ((current, transition), target) in enumerate(
            RUNTIME_STATE_GRAPH.items()
        ):
            with self.subTest(current=current, transition=transition, target=target):
                decision = self.machine.validate(
                    self._request(current, transition, target, suffix=str(index))
                )
                self.assertTrue(decision.allowed)
                self.assertEqual(decision.next_state, target)

    def test_requested_to_authorized_validation(self) -> None:
        decision = self.machine.validate(
            self._request(
                RuntimeState.REQUESTED,
                RuntimeTransition.AUTHORIZE,
                RuntimeState.AUTHORIZED,
            )
        )
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.reason, "transition_valid")

    def test_escalation_review_override_ready_path_is_validation_only(self) -> None:
        path = (
            (
                RuntimeState.REQUESTED,
                RuntimeTransition.ESCALATE,
                RuntimeState.ESCALATED,
            ),
            (
                RuntimeState.ESCALATED,
                RuntimeTransition.BEGIN_REVIEW,
                RuntimeState.UNDER_REVIEW,
            ),
            (
                RuntimeState.UNDER_REVIEW,
                RuntimeTransition.OVERRIDE,
                RuntimeState.OVERRIDDEN,
            ),
            (
                RuntimeState.OVERRIDDEN,
                RuntimeTransition.MARK_READY,
                RuntimeState.READY,
            ),
        )
        for index, (current, transition, target) in enumerate(path):
            decision = self.machine.validate(
                self._request(current, transition, target, suffix=f"path-{index}")
            )
            self.assertTrue(decision.allowed)
            self.assertEqual(decision.current_state, current)
            self.assertEqual(decision.next_state, target)

    def test_refused_and_halted_states_may_only_follow_explicit_edges(self) -> None:
        refused = self.machine.validate(
            self._request(
                RuntimeState.REFUSED,
                RuntimeTransition.ESCALATE,
                RuntimeState.ESCALATED,
                suffix="refused",
            )
        )
        halted = self.machine.validate(
            self._request(
                RuntimeState.HALTED,
                RuntimeTransition.ESCALATE,
                RuntimeState.ESCALATED,
                suffix="halted",
            )
        )
        self.assertTrue(refused.allowed)
        self.assertTrue(halted.allowed)

    def test_execution_block_release_validation(self) -> None:
        decision = self.machine.validate(
            self._request(
                RuntimeState.EXECUTION_BLOCKED,
                RuntimeTransition.RELEASE_BLOCK,
                RuntimeState.READY,
            )
        )
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.next_state, RuntimeState.READY)

    def test_undefined_transition_fails_closed(self) -> None:
        decision = self.machine.validate(
            self._request(
                RuntimeState.READY,
                RuntimeTransition.AUTHORIZE,
                RuntimeState.AUTHORIZED,
            )
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.next_state, RuntimeState.READY)
        self.assertEqual(decision.reason, "undefined_transition")

    def test_requested_state_mismatch_fails_closed(self) -> None:
        decision = self.machine.validate(
            self._request(
                RuntimeState.REQUESTED,
                RuntimeTransition.AUTHORIZE,
                RuntimeState.READY,
            )
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.next_state, RuntimeState.REQUESTED)
        self.assertEqual(decision.reason, "requested_state_mismatch")

    def test_expired_state_rejects_every_transition(self) -> None:
        for index, transition in enumerate(RuntimeTransition):
            decision = self.machine.validate(
                self._request(
                    RuntimeState.EXPIRED,
                    transition,
                    RuntimeState.REQUESTED,
                    suffix=f"expired-{index}",
                )
            )
            self.assertFalse(decision.allowed)
            self.assertEqual(decision.next_state, RuntimeState.EXPIRED)

    def test_transition_evidence_is_immutable_and_audited(self) -> None:
        decision = self.machine.validate(
            self._request(
                RuntimeState.AUTHORIZED,
                RuntimeTransition.MARK_READY,
                RuntimeState.READY,
            )
        )
        event = self.audit.chain("runtime-state-audit")[-1]

        self.assertEqual(event.record["event_type"], "runtime.transition.validation")
        self.assertEqual(event.record["state_before"], "authorized")
        self.assertEqual(event.record["state_after"], "ready")
        self.assertEqual(event.record["details"]["evidence_hash"], decision.evidence_hash)
        with self.assertRaises(FrozenInstanceError):
            decision.evidence.validated_state = RuntimeState.HALTED

    def test_transition_validation_is_idempotent(self) -> None:
        request = self._request(
            RuntimeState.REQUESTED,
            RuntimeTransition.REFUSE,
            RuntimeState.REFUSED,
        )
        first = self.machine.validate(request)
        audit_count = len(self.audit.chain("runtime-state-audit"))
        second = self.machine.validate(request)

        self.assertEqual(first, second)
        self.assertEqual(len(self.audit.chain("runtime-state-audit")), audit_count)


if __name__ == "__main__":
    unittest.main()
