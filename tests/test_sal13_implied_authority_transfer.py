"""SAL-13 adversarial tests for implied authority transfer.

This test lane is intentionally validation-only. It depends on the accepted,
unmerged SAL-24 authorization-to-execution handoff head and does not exercise
runtime envelopes, tokens, claims, dispatch, state mutation, or external action.
"""

from __future__ import annotations

import unittest
from dataclasses import asdict, replace

from echoauth.execution import ExecutionOutcome
from echoauth.runtime import RuntimeTransitionValidationError
from tests import test_sal24_authorization_execution_handoff as sal24


class Sal13ImpliedAuthorityTransferTests(unittest.TestCase):
    def setUp(self) -> None:
        # Reuse the established SAL-24 bounded fixture without inheriting its
        # TestCase class (which would duplicate its entire test suite here).
        self.fx = sal24.Sal24AuthorizationExecutionHandoffTests(
            methodName="test_fresh_authorization_and_ready_state_are_both_required_for_eligible"
        )
        self.fx.setUp()

    def test_ready_state_cannot_substitute_for_permission(self) -> None:
        auth_request = self.fx._authorization_request()
        runtime = self.fx._runtime_decision()
        request = self.fx._execution_request(auth_request, runtime)

        decision = self.fx.execution_control.validate(request, runtime, None)

        self.assertEqual(decision.outcome, ExecutionOutcome.MISSING_AUTHORITY)
        self.assertFalse(decision.eligible)
        self.assertEqual(decision.reason, "authorization_handoff_missing")

    def test_authorization_for_one_action_cannot_authorize_another_action(self) -> None:
        _, request, handoff, runtime = self.fx._accepted_handoff()
        changed = replace(request, action="write")

        decision = self.fx.execution_control.validate(changed, runtime, handoff)

        self.assertEqual(decision.outcome, ExecutionOutcome.MISSING_AUTHORITY)
        self.assertFalse(decision.eligible)
        self.assertEqual(decision.reason, "authorization_handoff_binding_mismatch")

    def test_authorization_for_one_resource_cannot_authorize_another_resource(self) -> None:
        _, request, handoff, runtime = self.fx._accepted_handoff()
        changed = replace(request, resource="record-2")

        decision = self.fx.execution_control.validate(changed, runtime, handoff)

        self.assertEqual(decision.outcome, ExecutionOutcome.MISSING_AUTHORITY)
        self.assertFalse(decision.eligible)
        self.assertEqual(decision.reason, "authorization_handoff_binding_mismatch")

    def test_authorization_decision_cannot_become_runtime_transition_request(self) -> None:
        authorization = self.fx.gate.authorize(self.fx._authorization_request())

        with self.assertRaises(RuntimeTransitionValidationError):
            self.fx.state_machine.validate(authorization)

    def test_execution_eligibility_result_cannot_become_runtime_transition_request(self) -> None:
        _, request, handoff, runtime = self.fx._accepted_handoff()
        execution_decision = self.fx.execution_control.validate(
            request, runtime, handoff
        )
        self.assertEqual(execution_decision.outcome, ExecutionOutcome.ELIGIBLE)

        with self.assertRaises(RuntimeTransitionValidationError):
            self.fx.state_machine.validate(execution_decision)

    def test_returned_execution_evidence_cannot_substitute_for_permission(self) -> None:
        _, request, handoff, runtime = self.fx._accepted_handoff()
        execution_decision = self.fx.execution_control.validate(
            request, runtime, handoff
        )
        self.assertEqual(execution_decision.outcome, ExecutionOutcome.ELIGIBLE)

        replay = replace(
            request,
            execution_request_id="sal13-return-replay",
            authority_evidence=asdict(execution_decision.evidence),
            audit_references=(runtime.audit_event_id, execution_decision.audit_event_id),
        )
        result = self.fx.execution_control.validate(replay, runtime, None)

        self.assertEqual(result.outcome, ExecutionOutcome.MISSING_AUTHORITY)
        self.assertFalse(result.eligible)
        self.assertEqual(result.reason, "authorization_handoff_missing")

    def test_planning_like_mapping_cannot_substitute_for_permission(self) -> None:
        auth_request = self.fx._authorization_request()
        runtime = self.fx._runtime_decision()
        request = self.fx._execution_request(
            auth_request,
            runtime,
            authority_evidence={
                "plan_id": "plan-1",
                "recommendation": "read record-1",
                "confidence": "high",
            },
        )

        decision = self.fx.execution_control.validate(request, runtime, None)

        self.assertEqual(decision.outcome, ExecutionOutcome.MISSING_AUTHORITY)
        self.assertFalse(decision.eligible)
        self.assertEqual(decision.reason, "authorization_handoff_missing")

    def test_permission_result_cannot_self_authorize_later_runtime_transition(self) -> None:
        prior, _, _, _ = self.fx._accepted_handoff()

        # A permission result is not a transition request. A later state change
        # still requires a separately formed RuntimeTransitionRequest.
        with self.assertRaises(RuntimeTransitionValidationError):
            self.fx.state_machine.validate(prior)


if __name__ == "__main__":
    unittest.main()
