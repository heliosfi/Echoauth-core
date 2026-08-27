"""Focused SAL-22 compact runtime-state currentness tests."""

from __future__ import annotations

import unittest
from datetime import datetime, timezone

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.runtime import (
    InMemoryRuntimeCurrentStateRepository,
    RuntimeDecisionCurrentnessService,
    RuntimeState,
    RuntimeStateCurrentnessError,
    RuntimeStateMachine,
    RuntimeTransition,
    RuntimeTransitionRequest,
)


class RuntimeStateCurrentnessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime(2026, 6, 19, 13, 0, tzinfo=timezone.utc)
        self.clock = lambda: self.now
        self.audit = InMemoryAuditLogRepository()
        self.machine = RuntimeStateMachine(
            self.audit,
            audit_chain_id="sal22-audit",
            clock=self.clock,
        )
        self.repository = InMemoryRuntimeCurrentStateRepository(
            self.audit,
            audit_chain_id="sal22-audit",
            clock=self.clock,
        )
        self.repository.register_initial(
            request_id="request-1",
            state=RuntimeState.AUTHORIZED,
            actor_id="sal22-test",
            occurred_at="2026-06-19T12:58:00Z",
        )
        self.currentness = RuntimeDecisionCurrentnessService(
            self.repository,
            self.audit,
            audit_chain_id="sal22-audit",
            clock=self.clock,
        )

    def _decision(self, current, transition, target, suffix):
        return self.machine.validate(
            RuntimeTransitionRequest(
                transition_request_id=f"sal22-{suffix}",
                request_id="request-1",
                current_state=current,
                transition=transition,
                requested_state=target,
                actor_id="sal22-test",
                reason=f"sal22_{suffix}",
                evidence={"source": suffix},
                occurred_at="2026-06-19T12:59:00Z",
            )
        )

    def _apply(self, decision):
        current = self.repository.get("request-1")
        return self.repository.apply(
            decision,
            expected_revision=current.state_revision,
            actor_id="sal22-test",
            applied_at="2026-06-19T12:59:30Z",
        )

    def test_explicit_initial_state_is_revision_zero(self) -> None:
        record = self.repository.get("request-1")
        self.assertEqual(record.current_state, RuntimeState.AUTHORIZED)
        self.assertEqual(record.state_revision, 0)
        self.assertIsNone(record.last_applied_transition_decision_id)
        self.assertEqual(self.repository.history("request-1"), ())

    def test_applied_ready_is_current_at_exact_revision(self) -> None:
        ready = self._decision(
            RuntimeState.AUTHORIZED,
            RuntimeTransition.MARK_READY,
            RuntimeState.READY,
            "ready-1",
        )
        application = self._apply(ready)
        result = self.currentness.validate(ready)

        self.assertEqual(application.resulting_revision, 1)
        self.assertTrue(result.current)
        self.assertEqual(result.current_state, RuntimeState.READY)
        self.assertEqual(result.current_revision, 1)
        self.assertEqual(result.reason, "runtime_transition_decision_current")

    def test_graph_valid_but_never_applied_decision_is_not_current(self) -> None:
        ready = self._decision(
            RuntimeState.AUTHORIZED,
            RuntimeTransition.MARK_READY,
            RuntimeState.READY,
            "never-applied",
        )
        result = self.currentness.validate(ready)
        self.assertFalse(result.current)
        self.assertEqual(result.reason, "transition_decision_never_applied")
        self.assertEqual(self.repository.get("request-1").state_revision, 0)

    def test_stale_expected_revision_fails_without_overwrite(self) -> None:
        ready = self._decision(
            RuntimeState.AUTHORIZED,
            RuntimeTransition.MARK_READY,
            RuntimeState.READY,
            "ready-1",
        )
        self._apply(ready)
        block = self._decision(
            RuntimeState.READY,
            RuntimeTransition.BLOCK_EXECUTION,
            RuntimeState.EXECUTION_BLOCKED,
            "block-2",
        )
        with self.assertRaisesRegex(
            RuntimeStateCurrentnessError,
            "expected_revision_mismatch",
        ):
            self.repository.apply(
                block,
                expected_revision=0,
                actor_id="sal22-test",
                applied_at="2026-06-19T13:00:00Z",
            )
        record = self.repository.get("request-1")
        self.assertEqual(record.current_state, RuntimeState.READY)
        self.assertEqual(record.state_revision, 1)

    def test_same_application_is_idempotent_only_while_still_current(self) -> None:
        ready = self._decision(
            RuntimeState.AUTHORIZED,
            RuntimeTransition.MARK_READY,
            RuntimeState.READY,
            "ready-1",
        )
        first = self._apply(ready)
        history_count = len(self.repository.history("request-1"))
        audit_count = len(self.audit.chain("sal22-audit"))
        second = self.repository.apply(
            ready,
            expected_revision=1,
            actor_id="sal22-test",
            applied_at="2026-06-19T13:01:00Z",
        )
        self.assertEqual(first, second)
        self.assertEqual(len(self.repository.history("request-1")), history_count)
        self.assertEqual(len(self.audit.chain("sal22-audit")), audit_count)

        block = self._decision(
            RuntimeState.READY,
            RuntimeTransition.BLOCK_EXECUTION,
            RuntimeState.EXECUTION_BLOCKED,
            "block-2",
        )
        self._apply(block)
        with self.assertRaisesRegex(
            RuntimeStateCurrentnessError,
            "transition_decision_superseded",
        ):
            self.repository.apply(
                ready,
                expected_revision=2,
                actor_id="sal22-test",
            )

    def test_old_ready_stays_stale_after_state_returns_to_ready(self) -> None:
        ready_one = self._decision(
            RuntimeState.AUTHORIZED,
            RuntimeTransition.MARK_READY,
            RuntimeState.READY,
            "ready-1",
        )
        self._apply(ready_one)
        self.assertTrue(self.currentness.validate(ready_one).current)

        block = self._decision(
            RuntimeState.READY,
            RuntimeTransition.BLOCK_EXECUTION,
            RuntimeState.EXECUTION_BLOCKED,
            "block-2",
        )
        self._apply(block)
        stale_after_block = self.currentness.validate(ready_one)
        self.assertFalse(stale_after_block.current)
        self.assertEqual(
            stale_after_block.reason,
            "transition_decision_superseded",
        )
        self.assertEqual(stale_after_block.current_revision, 2)

        ready_two = self._decision(
            RuntimeState.EXECUTION_BLOCKED,
            RuntimeTransition.RELEASE_BLOCK,
            RuntimeState.READY,
            "ready-3",
        )
        self._apply(ready_two)
        stale_after_return = self.currentness.validate(ready_one)
        current_after_return = self.currentness.validate(ready_two)

        self.assertFalse(stale_after_return.current)
        self.assertEqual(stale_after_return.current_state, RuntimeState.READY)
        self.assertEqual(stale_after_return.current_revision, 3)
        self.assertEqual(
            stale_after_return.reason,
            "transition_decision_superseded",
        )
        self.assertTrue(current_after_return.current)
        self.assertEqual(current_after_return.current_revision, 3)
        self.assertNotEqual(
            ready_one.transition_decision_id,
            ready_two.transition_decision_id,
        )

    def test_application_history_is_append_only_and_revisioned(self) -> None:
        ready = self._decision(
            RuntimeState.AUTHORIZED,
            RuntimeTransition.MARK_READY,
            RuntimeState.READY,
            "ready-1",
        )
        self._apply(ready)
        block = self._decision(
            RuntimeState.READY,
            RuntimeTransition.BLOCK_EXECUTION,
            RuntimeState.EXECUTION_BLOCKED,
            "block-2",
        )
        self._apply(block)
        history = self.repository.history("request-1")
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0].prior_revision, 0)
        self.assertEqual(history[0].resulting_revision, 1)
        self.assertEqual(history[1].prior_revision, 1)
        self.assertEqual(history[1].resulting_revision, 2)
        self.assertEqual(
            history[1].prior_state_record_hash,
            history[0].resulting_state_record_hash,
        )


if __name__ == "__main__":
    unittest.main()
