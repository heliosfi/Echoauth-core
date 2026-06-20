"""Sprint 2M deterministic Execution Control tests."""

from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.execution import (
    ExecutionConstraint,
    ExecutionControl,
    ExecutionControlValidationError,
    ExecutionOutcome,
    ExecutionRequest,
)
from echoauth.runtime import (
    RuntimeState,
    RuntimeStateMachine,
    RuntimeTransition,
    RuntimeTransitionRequest,
)


class ExecutionControlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.audit = InMemoryAuditLogRepository()
        clock = lambda: datetime(2026, 6, 19, 17, 0, tzinfo=timezone.utc)
        self.state_machine = RuntimeStateMachine(
            self.audit, audit_chain_id="execution-audit", clock=clock
        )
        self.direct_constraint = ExecutionConstraint(
            constraint_id="execution-constraint-direct",
            required_state=RuntimeState.READY,
            expires_at="2026-06-19T17:05:00Z",
        )
        self.override_constraint = ExecutionConstraint(
            constraint_id="execution-constraint-override",
            required_state=RuntimeState.READY,
            expires_at="2026-06-19T17:05:00Z",
            require_refusal_evidence=True,
            require_escalation_evidence=True,
            require_review_evidence=True,
            require_override_evidence=True,
        )
        self.disabled_constraint = ExecutionConstraint(
            constraint_id="execution-constraint-disabled",
            required_state=RuntimeState.READY,
            expires_at="2026-06-19T17:05:00Z",
            execution_enabled=False,
        )
        self.expired_constraint = ExecutionConstraint(
            constraint_id="execution-constraint-expired",
            required_state=RuntimeState.READY,
            expires_at="2026-06-19T16:59:59Z",
        )
        self.control = ExecutionControl(
            self.audit,
            audit_chain_id="execution-audit",
            constraints=(
                self.direct_constraint,
                self.override_constraint,
                self.disabled_constraint,
                self.expired_constraint,
            ),
            clock=clock,
        )

    def _runtime_decision(
        self,
        current: RuntimeState,
        transition: RuntimeTransition,
        target: RuntimeState,
    ):
        return self.state_machine.validate(
            RuntimeTransitionRequest(
                transition_request_id="runtime-transition-1",
                request_id="request-1",
                current_state=current,
                transition=transition,
                requested_state=target,
                actor_id="execution-test",
                reason="execution_eligibility_test",
                evidence={"state_source": "test"},
                occurred_at="2026-06-19T16:59:00Z",
            )
        )

    def _request(
        self,
        runtime_decision,
        *,
        constraint: ExecutionConstraint | None = None,
        authority_evidence=None,
        require_all_path_evidence: bool = False,
        refusal_evidence=None,
        escalation_evidence=None,
        review_evidence=None,
        override_evidence=None,
    ) -> ExecutionRequest:
        return ExecutionRequest(
            execution_request_id="execution-request-1",
            request_id=runtime_decision.request_id,
            runtime_transition_decision_id=runtime_decision.transition_decision_id,
            actor_id="execution-control-client",
            action="protect_subject",
            resource="subject-1",
            authority_evidence=(
                {
                    "authority_reference": "authority-1",
                    "authority_evidence_hash": "authority-hash-1",
                }
                if authority_evidence is None
                else authority_evidence
            ),
            refusal_evidence=refusal_evidence or {},
            escalation_evidence=escalation_evidence or {},
            review_evidence=review_evidence or {},
            override_evidence=override_evidence or {},
            evidence={"payload_hash": "payload-hash-1"},
            audit_references=(runtime_decision.audit_event_id,),
            requested_at="2026-06-19T17:00:00Z",
            constraint=(
                constraint
                or (
                    self.override_constraint
                    if require_all_path_evidence
                    else self.direct_constraint
                )
            ),
        )

    def _ready_decision(self):
        return self._runtime_decision(
            RuntimeState.AUTHORIZED,
            RuntimeTransition.MARK_READY,
            RuntimeState.READY,
        )

    def test_execution_is_eligible_from_ready_state(self) -> None:
        runtime = self._ready_decision()
        decision = self.control.validate(self._request(runtime), runtime)

        self.assertEqual(decision.outcome, ExecutionOutcome.ELIGIBLE)
        self.assertTrue(decision.eligible)

    def test_complete_override_path_evidence_is_validated(self) -> None:
        runtime = self._runtime_decision(
            RuntimeState.OVERRIDDEN,
            RuntimeTransition.MARK_READY,
            RuntimeState.READY,
        )
        request = self._request(
            runtime,
            require_all_path_evidence=True,
            refusal_evidence={
                "refusal_decision_id": "refusal-1",
                "refusal_evidence_hash": "refusal-hash-1",
            },
            escalation_evidence={
                "escalation_decision_id": "escalation-1",
                "escalation_evidence_hash": "escalation-hash-1",
            },
            review_evidence={
                "review_decision_id": "review-1",
                "review_evidence_hash": "review-hash-1",
            },
            override_evidence={
                "override_decision_id": "override-1",
                "override_evidence_hash": "override-hash-1",
            },
        )
        decision = self.control.validate(request, runtime)

        self.assertEqual(decision.outcome, ExecutionOutcome.ELIGIBLE)
        self.assertIsNotNone(decision.evidence.override_evidence_hash)

    def test_rejected_runtime_transition_blocks_execution(self) -> None:
        runtime = self._runtime_decision(
            RuntimeState.READY,
            RuntimeTransition.AUTHORIZE,
            RuntimeState.AUTHORIZED,
        )
        decision = self.control.validate(self._request(runtime), runtime)

        self.assertEqual(decision.outcome, ExecutionOutcome.BLOCKED)
        self.assertFalse(decision.eligible)

    def test_execution_blocked_state_blocks_execution(self) -> None:
        runtime = self._runtime_decision(
            RuntimeState.READY,
            RuntimeTransition.BLOCK_EXECUTION,
            RuntimeState.EXECUTION_BLOCKED,
        )
        decision = self.control.validate(self._request(runtime), runtime)
        self.assertEqual(decision.outcome, ExecutionOutcome.BLOCKED)

    def test_configured_disabled_constraint_blocks_execution(self) -> None:
        runtime = self._ready_decision()
        request = self._request(runtime, constraint=self.disabled_constraint)
        decision = self.control.validate(request, runtime)
        self.assertEqual(decision.outcome, ExecutionOutcome.BLOCKED)

    def test_unconfigured_constraint_is_rejected(self) -> None:
        runtime = self._ready_decision()
        unconfigured = ExecutionConstraint(
            constraint_id="unconfigured",
            required_state=RuntimeState.READY,
            expires_at="2026-06-19T17:05:00Z",
        )
        with self.assertRaises(ExecutionControlValidationError):
            self.control.validate(
                self._request(runtime, constraint=unconfigured), runtime
            )

    def test_non_ready_state_is_invalid(self) -> None:
        runtime = self._runtime_decision(
            RuntimeState.REQUESTED,
            RuntimeTransition.AUTHORIZE,
            RuntimeState.AUTHORIZED,
        )
        decision = self.control.validate(self._request(runtime), runtime)
        self.assertEqual(decision.outcome, ExecutionOutcome.INVALID_STATE)

    def test_missing_authority_fails_closed(self) -> None:
        runtime = self._ready_decision()
        request = self._request(runtime, authority_evidence={})
        decision = self.control.validate(request, runtime)
        self.assertEqual(decision.outcome, ExecutionOutcome.MISSING_AUTHORITY)

    def test_missing_required_path_evidence_fails_closed(self) -> None:
        runtime = self._ready_decision()
        request = self._request(runtime, require_all_path_evidence=True)
        decision = self.control.validate(request, runtime)
        self.assertEqual(decision.outcome, ExecutionOutcome.MISSING_EVIDENCE)

    def test_expired_constraint_fails_closed(self) -> None:
        runtime = self._ready_decision()
        request = self._request(runtime, constraint=self.expired_constraint)
        decision = self.control.validate(request, runtime)
        self.assertEqual(decision.outcome, ExecutionOutcome.EXPIRED)

    def test_halted_runtime_fails_closed(self) -> None:
        runtime = self._runtime_decision(
            RuntimeState.REQUESTED,
            RuntimeTransition.HALT,
            RuntimeState.HALTED,
        )
        decision = self.control.validate(self._request(runtime), runtime)
        self.assertEqual(decision.outcome, ExecutionOutcome.HALTED)

    def test_execution_evidence_is_immutable_and_audited(self) -> None:
        runtime = self._ready_decision()
        decision = self.control.validate(self._request(runtime), runtime)
        event = self.audit.chain("execution-audit")[-1]

        self.assertEqual(event.record["event_type"], "execution.eligibility.validation")
        self.assertEqual(event.record["details"]["evidence_hash"], decision.evidence_hash)
        self.assertEqual(
            decision.evidence.runtime_transition_evidence_hash,
            runtime.evidence_hash,
        )
        self.assertEqual(decision.evidence.action, "protect_subject")
        self.assertEqual(decision.evidence.resource, "subject-1")
        with self.assertRaises(FrozenInstanceError):
            decision.evidence.runtime_state = RuntimeState.HALTED

    def test_execution_validation_is_idempotent(self) -> None:
        runtime = self._ready_decision()
        request = self._request(runtime)
        first = self.control.validate(request, runtime)
        audit_count = len(self.audit.chain("execution-audit"))
        second = self.control.validate(request, runtime)

        self.assertEqual(first, second)
        self.assertEqual(len(self.audit.chain("execution-audit")), audit_count)


if __name__ == "__main__":
    unittest.main()
