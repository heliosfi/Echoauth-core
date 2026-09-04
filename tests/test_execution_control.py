"""Sprint 2M execution control tests with SAL-24 permission handoff binding."""

from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timezone

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.execution import (
    AuthorizationExecutionHandoffDecision,
    ExecutionConstraint,
    ExecutionControl,
    ExecutionControlValidationError,
    ExecutionOutcome,
    ExecutionRequest,
)
from echoauth.models import AuditRecord
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
            subject_id="subject-1",
            action="protect_subject",
            resource="subject-1",
            payload_hash="payload-hash-1",
            context_hash="context-hash-1",
            policy_version="policy-v1",
            delegation_id=None,
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

    def _bind_handoff(self, request, runtime):
        handoff = AuthorizationExecutionHandoffDecision(
            handoff_validation_id="aeh-test",
            request_id=request.request_id,
            requester_id=request.actor_id,
            subject_id=request.subject_id,
            action=request.action,
            resource=request.resource,
            payload_hash=request.payload_hash,
            context_hash=request.context_hash,
            policy_version=request.policy_version,
            delegation_id=request.delegation_id,
            prior_authorization_decision_id="adec-prior",
            fresh_authorization_decision_id="adec-fresh",
            fresh_authorization_evidence_hash="auth-evidence-fresh",
            fresh_authorization_audit_event_id="audit-adec-fresh",
            identity_verdict_id="idv-1",
            authority_resolution_id="ares-1",
            delegation_validation_id=None,
            policy_decision_id="pdec-1",
            accepted=True,
            reason="authorization_current_and_bound",
            validated_at="2026-06-19T17:00:00Z",
            evidence_hash="handoff-evidence-hash",
            audit_event_id="audit-aeh-test",
        )
        self.audit.append(
            AuditRecord(
                event_type="authorization.execution_handoff.validation",
                actor_id="authorization_execution_handoff_validator",
                request_id=request.request_id,
                authority_verdict_id="ares-1",
                reason=handoff.reason,
                details={
                    "accepted": True,
                    "evidence_hash": handoff.evidence_hash,
                    "fresh_authorization_decision_id": handoff.fresh_authorization_decision_id,
                    "handoff_validation_id": handoff.handoff_validation_id,
                    "prior_authorization_decision_id": handoff.prior_authorization_decision_id,
                },
                occurred_at="2026-06-19T17:00:00Z",
            ),
            audit_event_id=handoff.audit_event_id,
            chain_id="execution-audit",
        )
        authority_evidence = {
            "authorization_decision_id": handoff.fresh_authorization_decision_id,
            "authorization_evidence_hash": handoff.fresh_authorization_evidence_hash,
            "authorization_audit_event_id": handoff.fresh_authorization_audit_event_id,
            "authority_resolution_id": handoff.authority_resolution_id,
            "handoff_validation_id": handoff.handoff_validation_id,
            "handoff_evidence_hash": handoff.evidence_hash,
        }
        bound = replace(
            request,
            authority_evidence=authority_evidence,
            audit_references=(
                runtime.audit_event_id,
                handoff.fresh_authorization_audit_event_id,
                handoff.audit_event_id,
            ),
        )
        return bound, handoff

    def test_execution_is_eligible_from_ready_state_with_bound_permission(self) -> None:
        runtime = self._ready_decision()
        request, handoff = self._bind_handoff(self._request(runtime), runtime)
        decision = self.control.validate(request, runtime, handoff)
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
            refusal_evidence={"refusal_decision_id": "refusal-1", "refusal_evidence_hash": "refusal-hash-1"},
            escalation_evidence={"escalation_decision_id": "escalation-1", "escalation_evidence_hash": "escalation-hash-1"},
            review_evidence={"review_decision_id": "review-1", "review_evidence_hash": "review-hash-1"},
            override_evidence={"override_decision_id": "override-1", "override_evidence_hash": "override-hash-1"},
        )
        request, handoff = self._bind_handoff(request, runtime)
        decision = self.control.validate(request, runtime, handoff)
        self.assertEqual(decision.outcome, ExecutionOutcome.ELIGIBLE)
        self.assertIsNotNone(decision.evidence.override_evidence_hash)

    def test_rejected_runtime_transition_blocks_execution(self) -> None:
        runtime = self._runtime_decision(RuntimeState.READY, RuntimeTransition.AUTHORIZE, RuntimeState.AUTHORIZED)
        decision = self.control.validate(self._request(runtime), runtime)
        self.assertEqual(decision.outcome, ExecutionOutcome.BLOCKED)
        self.assertFalse(decision.eligible)

    def test_execution_blocked_state_blocks_execution(self) -> None:
        runtime = self._runtime_decision(RuntimeState.READY, RuntimeTransition.BLOCK_EXECUTION, RuntimeState.EXECUTION_BLOCKED)
        decision = self.control.validate(self._request(runtime), runtime)
        self.assertEqual(decision.outcome, ExecutionOutcome.BLOCKED)

    def test_configured_disabled_constraint_blocks_execution(self) -> None:
        runtime = self._ready_decision()
        decision = self.control.validate(self._request(runtime, constraint=self.disabled_constraint), runtime)
        self.assertEqual(decision.outcome, ExecutionOutcome.BLOCKED)

    def test_unconfigured_constraint_is_rejected(self) -> None:
        runtime = self._ready_decision()
        unconfigured = ExecutionConstraint(
            constraint_id="unconfigured",
            required_state=RuntimeState.READY,
            expires_at="2026-06-19T17:05:00Z",
        )
        with self.assertRaises(ExecutionControlValidationError):
            self.control.validate(self._request(runtime, constraint=unconfigured), runtime)

    def test_non_ready_state_is_invalid(self) -> None:
        runtime = self._runtime_decision(RuntimeState.REQUESTED, RuntimeTransition.AUTHORIZE, RuntimeState.AUTHORIZED)
        decision = self.control.validate(self._request(runtime), runtime)
        self.assertEqual(decision.outcome, ExecutionOutcome.INVALID_STATE)

    def test_missing_authority_handoff_fails_closed(self) -> None:
        runtime = self._ready_decision()
        decision = self.control.validate(self._request(runtime), runtime)
        self.assertEqual(decision.outcome, ExecutionOutcome.MISSING_AUTHORITY)

    def test_missing_required_path_evidence_fails_closed(self) -> None:
        runtime = self._ready_decision()
        request, handoff = self._bind_handoff(self._request(runtime, require_all_path_evidence=True), runtime)
        decision = self.control.validate(request, runtime, handoff)
        self.assertEqual(decision.outcome, ExecutionOutcome.MISSING_EVIDENCE)

    def test_expired_constraint_fails_closed(self) -> None:
        runtime = self._ready_decision()
        decision = self.control.validate(self._request(runtime, constraint=self.expired_constraint), runtime)
        self.assertEqual(decision.outcome, ExecutionOutcome.EXPIRED)

    def test_halted_runtime_fails_closed(self) -> None:
        runtime = self._runtime_decision(RuntimeState.REQUESTED, RuntimeTransition.HALT, RuntimeState.HALTED)
        decision = self.control.validate(self._request(runtime), runtime)
        self.assertEqual(decision.outcome, ExecutionOutcome.HALTED)

    def test_execution_evidence_is_immutable_and_audited(self) -> None:
        runtime = self._ready_decision()
        request, handoff = self._bind_handoff(self._request(runtime), runtime)
        decision = self.control.validate(request, runtime, handoff)
        event = self.audit.chain("execution-audit")[-1]
        self.assertEqual(event.record["event_type"], "execution.eligibility.validation")
        self.assertEqual(event.record["details"]["evidence_hash"], decision.evidence_hash)
        self.assertEqual(decision.evidence.runtime_transition_evidence_hash, runtime.evidence_hash)
        self.assertEqual(decision.evidence.authorization_handoff_validation_id, handoff.handoff_validation_id)
        with self.assertRaises(FrozenInstanceError):
            decision.evidence.runtime_state = RuntimeState.HALTED

    def test_execution_validation_is_idempotent(self) -> None:
        runtime = self._ready_decision()
        request, handoff = self._bind_handoff(self._request(runtime), runtime)
        first = self.control.validate(request, runtime, handoff)
        audit_count = len(self.audit.chain("execution-audit"))
        second = self.control.validate(request, runtime, handoff)
        self.assertEqual(first, second)
        self.assertEqual(len(self.audit.chain("execution-audit")), audit_count)


if __name__ == "__main__":
    unittest.main()
