"""SAL-14 adversarial tests for repeated processing and replay."""

from __future__ import annotations

import unittest
from dataclasses import replace

from echoauth.auth import AuthorizationOutcome
from echoauth.execution import ExecutionOutcome
from echoauth.runtime import (
    RuntimeState,
    RuntimeTransition,
    RuntimeTransitionRequest,
)
from tests.test_sal24_authorization_execution_handoff import (
    Sal24AuthorizationExecutionHandoffTests,
)


class Sal14RepeatedProcessingReplayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Sal24AuthorizationExecutionHandoffTests(methodName="runTest")
        self.fx.setUp()

    def test_exact_handoff_retry_returns_same_evidence_without_duplicate_audit(self):
        auth_request = self.fx._authorization_request()
        runtime = self.fx._runtime_decision()
        prior = self.fx.gate.authorize(auth_request)
        request = self.fx._execution_request(auth_request, runtime)

        first = self.fx.handoff_validator.validate(request, auth_request, prior)
        audit_count = len(self.fx.audit.chain("sal24-audit"))
        second = self.fx.handoff_validator.validate(request, auth_request, prior)

        self.assertTrue(first.accepted)
        self.assertEqual(first, second)
        self.assertEqual(len(self.fx.audit.chain("sal24-audit")), audit_count)

    def test_lost_response_retry_does_not_duplicate_execution_eligibility_evidence(self):
        _, request, handoff, runtime = self.fx._accepted_handoff()

        first = self.fx.execution_control.validate(request, runtime, handoff)
        audit_count = len(self.fx.audit.chain("sal24-audit"))
        # Simulate a client retry after the first response was lost.
        second = self.fx.execution_control.validate(request, runtime, handoff)

        self.assertEqual(first.outcome, ExecutionOutcome.ELIGIBLE)
        self.assertEqual(first, second)
        self.assertEqual(len(self.fx.audit.chain("sal24-audit")), audit_count)

    def test_permission_change_between_retries_bypasses_replay_cache_and_fails_closed(self):
        auth_request = self.fx._authorization_request()
        runtime = self.fx._runtime_decision()
        prior = self.fx.gate.authorize(auth_request)
        request = self.fx._execution_request(auth_request, runtime)

        first = self.fx.handoff_validator.validate(request, auth_request, prior)
        self.assertTrue(first.accepted)

        self.fx.authority_repository.revoke(
            "authority-1",
            actor_id="registry-admin",
            reason="authority_revoked",
            occurred_at="2026-06-19T12:30:00Z",
            audit_event_id="audit-authority-revoked-sal14",
        )

        second = self.fx.handoff_validator.validate(request, auth_request, prior)
        self.assertFalse(second.accepted)
        self.assertEqual(second.reason, "fresh_authorization_not_authorized")
        self.assertNotEqual(first.handoff_validation_id, second.handoff_validation_id)

        audit_count = len(self.fx.audit.chain("sal24-audit"))
        third = self.fx.handoff_validator.validate(request, auth_request, prior)
        self.assertEqual(second, third)
        self.assertEqual(len(self.fx.audit.chain("sal24-audit")), audit_count)

    def test_transport_metadata_change_is_distinct_attributable_evaluation_not_authority_grant(self):
        runtime = self.fx._runtime_decision()
        first_request = self.fx._authorization_request()
        first_prior = self.fx.gate.authorize(first_request)
        first_handoff = self.fx.handoff_validator.validate(
            self.fx._execution_request(first_request, runtime),
            first_request,
            first_prior,
        )

        second_request = self.fx._authorization_request(
            correlation_id="correlation-transport-retry",
            idempotency_key="idempotency-transport-retry",
        )
        second_prior = self.fx.gate.authorize(second_request)
        second_handoff = self.fx.handoff_validator.validate(
            self.fx._execution_request(second_request, runtime),
            second_request,
            second_prior,
        )

        self.assertEqual(first_prior.outcome, AuthorizationOutcome.AUTHORIZED)
        self.assertEqual(second_prior.outcome, AuthorizationOutcome.AUTHORIZED)
        self.assertTrue(first_handoff.accepted)
        self.assertTrue(second_handoff.accepted)
        self.assertNotEqual(
            first_prior.authorization_decision_id,
            second_prior.authorization_decision_id,
        )
        self.assertNotEqual(
            first_handoff.handoff_validation_id,
            second_handoff.handoff_validation_id,
        )
        # Both outputs remain validation evidence only; neither executes an action.

    def test_changed_runtime_evidence_blocks_reordered_duplicate_even_with_fresh_permission(self):
        auth_request = self.fx._authorization_request()
        ready = self.fx._runtime_decision()
        prior = self.fx.gate.authorize(auth_request)
        ready_request = self.fx._execution_request(auth_request, ready)
        ready_handoff = self.fx.handoff_validator.validate(
            ready_request, auth_request, prior
        )
        ready_bound = replace(
            ready_request,
            authority_evidence=self.fx._authority_evidence(ready_handoff),
            audit_references=(
                ready.audit_event_id,
                ready_handoff.fresh_authorization_audit_event_id,
                ready_handoff.audit_event_id,
            ),
        )
        first = self.fx.execution_control.validate(
            ready_bound, ready, ready_handoff
        )
        self.assertEqual(first.outcome, ExecutionOutcome.ELIGIBLE)

        blocked = self.fx.state_machine.validate(
            RuntimeTransitionRequest(
                transition_request_id="sal14-block-runtime-transition",
                request_id=auth_request.request_id,
                current_state=RuntimeState.READY,
                transition=RuntimeTransition.BLOCK_EXECUTION,
                requested_state=RuntimeState.EXECUTION_BLOCKED,
                actor_id="sal14-runtime-test",
                reason="sal14_reordered_duplicate_after_block",
                evidence={"source": "sal14"},
                occurred_at="2026-06-19T12:59:30Z",
            )
        )
        blocked_request = self.fx._execution_request(auth_request, blocked)
        blocked_handoff = self.fx.handoff_validator.validate(
            blocked_request, auth_request, prior
        )
        blocked_bound = replace(
            blocked_request,
            authority_evidence=self.fx._authority_evidence(blocked_handoff),
            audit_references=(
                blocked.audit_event_id,
                blocked_handoff.fresh_authorization_audit_event_id,
                blocked_handoff.audit_event_id,
            ),
        )
        second = self.fx.execution_control.validate(
            blocked_bound, blocked, blocked_handoff
        )

        self.assertEqual(second.outcome, ExecutionOutcome.BLOCKED)
        self.assertFalse(second.eligible)
        self.assertNotEqual(first.execution_decision_id, second.execution_decision_id)


if __name__ == "__main__":
    unittest.main()
