"""SAL-15 adversarial tests for execution-after-return authority separation."""

from __future__ import annotations

import unittest
from dataclasses import replace

from echoauth.execution import ExecutionOutcome
from echoauth.runtime import (
    RuntimeState,
    RuntimeTransition,
    RuntimeTransitionRequest,
)
from echoauth.runtime.halt_models import HaltOutcome
from echoauth.runtime.recovery import (
    RecoveryFailureCode,
    RecoveryOutcome,
    RecoverySourceState,
)
from tests.test_recovery_eligibility import RecoveryEligibilityTests
from tests.test_sal24_authorization_execution_handoff import (
    Sal24AuthorizationExecutionHandoffTests,
)


class Sal15ExecutionAfterReturnTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Sal24AuthorizationExecutionHandoffTests(methodName="runTest")
        self.fx.setUp()
        self.recovery_fx = RecoveryEligibilityTests(methodName="runTest")
        self.recovery_fx.setUp()

    def test_prior_execution_result_cannot_be_reused_as_fresh_permission(self):
        _, request, handoff, runtime = self.fx._accepted_handoff()
        completed = self.fx.execution_control.validate(request, runtime, handoff)
        self.assertEqual(completed.outcome, ExecutionOutcome.ELIGIBLE)

        follow_on = replace(
            request,
            execution_request_id="sal15-follow-on-from-execution-return",
        )
        decision = self.fx.execution_control.validate(
            follow_on,
            runtime,
            completed,  # type: ignore[arg-type]
        )

        self.assertEqual(decision.outcome, ExecutionOutcome.MISSING_AUTHORITY)
        self.assertEqual(decision.reason, "authorization_handoff_noncanonical")
        self.assertFalse(decision.eligible)

    def test_revalidation_required_recovery_result_is_not_reauthorization(self):
        recovery = self.recovery_fx.service.validate(
            self.recovery_fx.request,
            self.recovery_fx.authority,
            self.recovery_fx.halt,
        )
        self.assertIs(recovery.outcome, RecoveryOutcome.REVALIDATION_REQUIRED)

        _, request, _, runtime = self.fx._accepted_handoff()
        follow_on = replace(
            request,
            execution_request_id="sal15-follow-on-from-revalidation-required",
        )
        decision = self.fx.execution_control.validate(
            follow_on,
            runtime,
            recovery,  # type: ignore[arg-type]
        )

        self.assertEqual(decision.outcome, ExecutionOutcome.MISSING_AUTHORITY)
        self.assertEqual(decision.reason, "authorization_handoff_noncanonical")
        self.assertFalse(decision.eligible)

    def test_rejected_and_new_request_required_reassessment_cannot_continue(self):
        rejected_request = replace(
            self.recovery_fx.request,
            recovery_id="sal15-recovery-rejected",
            changed_evidence_hash="original-evidence",
        )
        rejected = self.recovery_fx.service.validate(
            rejected_request,
            self.recovery_fx.authority,
            self.recovery_fx.halt,
        )
        self.assertIs(rejected.outcome, RecoveryOutcome.REJECTED)

        new_request_input = replace(
            self.recovery_fx.request,
            recovery_id="sal15-recovery-new-request",
            source_state=RecoverySourceState.HALTED,
            failure_code=RecoveryFailureCode.INVALID_STATE,
            guard_evidence={
                "audit_chain_id": "chain-1",
                "original_failure_event_hash": self.recovery_fx.original_event_hash,
                "halt_audit_event_id": "audit-halt",
                "runtime_transition_decision_id": "transition-1",
                "runtime_transition_evidence_hash": "transition-hash",
            },
        )
        new_request = self.recovery_fx.service.validate(
            new_request_input,
            self.recovery_fx.authority,
            replace(self.recovery_fx.halt, runtime_state=HaltOutcome.HALTED),
        )
        self.assertIs(new_request.outcome, RecoveryOutcome.NEW_REQUEST_REQUIRED)

        _, request, _, runtime = self.fx._accepted_handoff()
        for index, returned in enumerate((rejected, new_request), start=1):
            with self.subTest(outcome=returned.outcome):
                follow_on = replace(
                    request,
                    execution_request_id=f"sal15-return-blocked-{index}",
                )
                decision = self.fx.execution_control.validate(
                    follow_on,
                    runtime,
                    returned,  # type: ignore[arg-type]
                )
                self.assertEqual(
                    decision.outcome,
                    ExecutionOutcome.MISSING_AUTHORITY,
                )
                self.assertEqual(
                    decision.reason,
                    "authorization_handoff_noncanonical",
                )
                self.assertFalse(decision.eligible)

    def test_completed_context_cannot_continue_after_runtime_becomes_blocked(self):
        auth_request = self.fx._authorization_request()
        ready = self.fx._runtime_decision()
        prior = self.fx.gate.authorize(auth_request)
        ready_request = self.fx._execution_request(auth_request, ready)
        handoff = self.fx.handoff_validator.validate(
            ready_request,
            auth_request,
            prior,
        )
        ready_bound = replace(
            ready_request,
            authority_evidence=self.fx._authority_evidence(handoff),
            audit_references=(
                ready.audit_event_id,
                handoff.fresh_authorization_audit_event_id,
                handoff.audit_event_id,
            ),
        )
        completed = self.fx.execution_control.validate(
            ready_bound,
            ready,
            handoff,
        )
        self.assertEqual(completed.outcome, ExecutionOutcome.ELIGIBLE)

        blocked = self.fx.state_machine.validate(
            RuntimeTransitionRequest(
                transition_request_id="sal15-runtime-blocked-after-return",
                request_id=auth_request.request_id,
                current_state=RuntimeState.READY,
                transition=RuntimeTransition.BLOCK_EXECUTION,
                requested_state=RuntimeState.EXECUTION_BLOCKED,
                actor_id="sal15-runtime-test",
                reason="sal15_return_requires_reassessment",
                evidence={"source": "sal15"},
                occurred_at="2026-06-19T12:59:30Z",
            )
        )
        blocked_request = self.fx._execution_request(
            auth_request,
            blocked,
            execution_request_id="sal15-blocked-follow-on",
        )
        blocked_bound = replace(
            blocked_request,
            authority_evidence=self.fx._authority_evidence(handoff),
            audit_references=(
                blocked.audit_event_id,
                handoff.fresh_authorization_audit_event_id,
                handoff.audit_event_id,
            ),
        )
        decision = self.fx.execution_control.validate(
            blocked_bound,
            blocked,
            handoff,
        )

        self.assertEqual(decision.outcome, ExecutionOutcome.BLOCKED)
        self.assertEqual(decision.reason, "execution_blocked")
        self.assertFalse(decision.eligible)

    def test_prior_action_handoff_cannot_authorize_follow_on_action(self):
        auth_request = self.fx._authorization_request()
        runtime = self.fx._runtime_decision()
        prior = self.fx.gate.authorize(auth_request)
        initial_request = self.fx._execution_request(auth_request, runtime)
        handoff = self.fx.handoff_validator.validate(
            initial_request,
            auth_request,
            prior,
        )
        self.assertTrue(handoff.accepted)

        follow_on_auth = self.fx._authorization_request(
            action="write",
            payload={"operation": "write"},
        )
        follow_on = self.fx._execution_request(
            follow_on_auth,
            runtime,
            execution_request_id="sal15-different-action-follow-on",
            authority_evidence=self.fx._authority_evidence(handoff),
            audit_references=(
                runtime.audit_event_id,
                handoff.fresh_authorization_audit_event_id,
                handoff.audit_event_id,
            ),
        )
        decision = self.fx.execution_control.validate(
            follow_on,
            runtime,
            handoff,
        )

        self.assertEqual(decision.outcome, ExecutionOutcome.MISSING_AUTHORITY)
        self.assertEqual(decision.reason, "authorization_handoff_binding_mismatch")
        self.assertFalse(decision.eligible)


if __name__ == "__main__":
    unittest.main()
