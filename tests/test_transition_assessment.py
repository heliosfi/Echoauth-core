"""Focused tests for the bounded upstream transition-assessment surface."""

from __future__ import annotations

import unittest
from datetime import datetime, timezone

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.runtime.state_machine import (
    RUNTIME_STATE_GRAPH,
    RuntimeStateMachine,
    RuntimeTransitionValidationError,
)
from echoauth.runtime.state_models import RuntimeState, RuntimeTransition, RuntimeTransitionRequest
from echoauth.runtime.transition_assessment import assess_transition


class TransitionAssessmentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.audit = InMemoryAuditLogRepository()
        self.machine = RuntimeStateMachine(
            self.audit,
            audit_chain_id="transition-assessment-audit",
            clock=lambda: datetime(2026, 8, 25, 12, 0, tzinfo=timezone.utc),
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
            transition_request_id=f"assessment-{suffix}",
            request_id="request-1",
            current_state=current,
            transition=transition,
            requested_state=requested,
            actor_id="transition-assessment-test",
            reason=f"test_{transition.value}",
            evidence={"source": suffix},
            occurred_at="2026-08-25T11:59:00Z",
        )

    def test_valid_transition_returns_canonical_decision(self) -> None:
        decision = assess_transition(
            self.machine,
            self._request(
                RuntimeState.REQUESTED,
                RuntimeTransition.AUTHORIZE,
                RuntimeState.AUTHORIZED,
            ),
        )
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.current_state, RuntimeState.REQUESTED)
        self.assertEqual(decision.next_state, RuntimeState.AUTHORIZED)
        self.assertEqual(decision.reason, "transition_valid")

    def test_undefined_transition_remains_fail_closed(self) -> None:
        decision = assess_transition(
            self.machine,
            self._request(
                RuntimeState.READY,
                RuntimeTransition.AUTHORIZE,
                RuntimeState.AUTHORIZED,
            ),
        )
        event = self.audit.chain("transition-assessment-audit")[-1]

        self.assertFalse(decision.allowed)
        self.assertEqual(decision.current_state, RuntimeState.READY)
        self.assertEqual(decision.next_state, RuntimeState.READY)
        self.assertEqual(decision.reason, "undefined_transition")
        self.assertEqual(event.record["state_before"], "ready")
        self.assertEqual(event.record["state_after"], "ready")
        self.assertEqual(event.record["reason"], "undefined_transition")

    def test_requested_state_mismatch_remains_fail_closed(self) -> None:
        decision = assess_transition(
            self.machine,
            self._request(
                RuntimeState.REQUESTED,
                RuntimeTransition.AUTHORIZE,
                RuntimeState.READY,
            ),
        )
        event = self.audit.chain("transition-assessment-audit")[-1]

        self.assertFalse(decision.allowed)
        self.assertEqual(decision.current_state, RuntimeState.REQUESTED)
        self.assertEqual(decision.next_state, RuntimeState.REQUESTED)
        self.assertEqual(decision.reason, "requested_state_mismatch")
        self.assertEqual(event.record["state_before"], "requested")
        self.assertEqual(event.record["state_after"], "requested")
        self.assertEqual(event.record["reason"], "requested_state_mismatch")

    def test_empty_transition_evidence_is_rejected_before_audit(self) -> None:
        request = RuntimeTransitionRequest(
            transition_request_id="assessment-empty-evidence",
            request_id="request-1",
            current_state=RuntimeState.REQUESTED,
            transition=RuntimeTransition.AUTHORIZE,
            requested_state=RuntimeState.AUTHORIZED,
            actor_id="transition-assessment-test",
            reason="empty_evidence",
            evidence={},
            occurred_at="2026-08-25T11:59:00Z",
        )

        with self.assertRaisesRegex(
            RuntimeTransitionValidationError,
            "evidence must be a non-empty canonical JSON object",
        ):
            assess_transition(self.machine, request)

        self.assertEqual(len(self.audit.chain("transition-assessment-audit")), 0)

    def test_non_mapping_transition_evidence_is_rejected_before_audit(self) -> None:
        request = RuntimeTransitionRequest(
            transition_request_id="assessment-non-mapping-evidence",
            request_id="request-1",
            current_state=RuntimeState.REQUESTED,
            transition=RuntimeTransition.AUTHORIZE,
            requested_state=RuntimeState.AUTHORIZED,
            actor_id="transition-assessment-test",
            reason="non_mapping_evidence",
            evidence=[],  # type: ignore[arg-type]
            occurred_at="2026-08-25T11:59:00Z",
        )

        with self.assertRaisesRegex(
            RuntimeTransitionValidationError,
            "evidence must be a non-empty canonical JSON object",
        ):
            assess_transition(self.machine, request)

        self.assertEqual(len(self.audit.chain("transition-assessment-audit")), 0)

    def test_non_canonical_transition_evidence_is_rejected_before_audit(self) -> None:
        request = RuntimeTransitionRequest(
            transition_request_id="assessment-non-canonical-evidence",
            request_id="request-1",
            current_state=RuntimeState.REQUESTED,
            transition=RuntimeTransition.AUTHORIZE,
            requested_state=RuntimeState.AUTHORIZED,
            actor_id="transition-assessment-test",
            reason="non_canonical_evidence",
            evidence={"unsupported": object()},
            occurred_at="2026-08-25T11:59:00Z",
        )

        with self.assertRaisesRegex(
            RuntimeTransitionValidationError,
            "evidence is not canonical JSON",
        ):
            assess_transition(self.machine, request)

        self.assertEqual(len(self.audit.chain("transition-assessment-audit")), 0)

    def test_malformed_transition_request_type_is_rejected_before_audit(self) -> None:
        with self.assertRaisesRegex(
            RuntimeTransitionValidationError,
            "request must be a RuntimeTransitionRequest",
        ):
            assess_transition(self.machine, object())  # type: ignore[arg-type]

        self.assertEqual(len(self.audit.chain("transition-assessment-audit")), 0)

    def test_non_canonical_current_state_is_rejected_before_audit(self) -> None:
        request = RuntimeTransitionRequest(
            transition_request_id="assessment-fabricated-current-state",
            request_id="request-1",
            current_state="fabricated",  # type: ignore[arg-type]
            transition=RuntimeTransition.AUTHORIZE,
            requested_state=RuntimeState.AUTHORIZED,
            actor_id="transition-assessment-test",
            reason="fabricated_current_state",
            evidence={"source": "fabricated-current-state"},
            occurred_at="2026-08-25T11:59:00Z",
        )

        with self.assertRaisesRegex(
            RuntimeTransitionValidationError,
            "current_state must be canonical",
        ):
            assess_transition(self.machine, request)

        self.assertEqual(len(self.audit.chain("transition-assessment-audit")), 0)

    def test_adapter_does_not_apply_state_and_preserves_audit_and_hash(self) -> None:
        request = self._request(
            RuntimeState.AUTHORIZED,
            RuntimeTransition.MARK_READY,
            RuntimeState.READY,
        )
        decision = assess_transition(self.machine, request)
        event = self.audit.chain("transition-assessment-audit")[-1]

        self.assertEqual(request.current_state, RuntimeState.AUTHORIZED)
        self.assertEqual(request.requested_state, RuntimeState.READY)
        self.assertEqual(decision.current_state, RuntimeState.AUTHORIZED)
        self.assertEqual(decision.next_state, RuntimeState.READY)
        self.assertEqual(event.record["details"]["evidence_hash"], decision.evidence_hash)
        self.assertEqual(decision.validated_at, "2026-08-25T12:00:00Z")

    def test_adapter_preserves_idempotent_validation(self) -> None:
        request = self._request(
            RuntimeState.REQUESTED,
            RuntimeTransition.REFUSE,
            RuntimeState.REFUSED,
        )
        first = assess_transition(self.machine, request)
        audit_count = len(self.audit.chain("transition-assessment-audit"))
        second = assess_transition(self.machine, request)
        self.assertEqual(first, second)
        self.assertEqual(len(self.audit.chain("transition-assessment-audit")), audit_count)

    def test_canonical_vocabularies_and_graph_are_not_extended(self) -> None:
        self.assertEqual(len(RUNTIME_STATE_GRAPH), 33)
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
        self.assertNotIn("S0", {state.name for state in RuntimeState})

    def test_non_runtime_machine_is_rejected(self) -> None:
        request = self._request(
            RuntimeState.REQUESTED,
            RuntimeTransition.AUTHORIZE,
            RuntimeState.AUTHORIZED,
        )
        with self.assertRaises(TypeError):
            assess_transition(object(), request)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
