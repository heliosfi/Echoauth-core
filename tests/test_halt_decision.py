"""Sprint 2O deterministic, evidence-only Halt Decision tests."""

from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.runtime import (
    HaltCause,
    HaltDecisionService,
    HaltOutcome,
    HaltRequest,
    HaltSeverity,
    HaltValidationError,
)


class HaltDecisionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.audit = InMemoryAuditLogRepository()
        self.service = HaltDecisionService(
            self.audit,
            audit_chain_id="halt-audit",
            clock=lambda: datetime(2026, 6, 19, 19, 0, tzinfo=timezone.utc),
        )

    def _request(
        self,
        cause: HaltCause,
        evidence,
        *,
        severity: HaltSeverity = HaltSeverity.HIGH,
        event_id: str = "halt-event-1",
    ) -> HaltRequest:
        return HaltRequest(
            halt_event_id=event_id,
            request_id="request-1",
            detected_by="halt-test",
            failure_type=cause,
            severity=severity,
            state_before="ready",
            evidence=evidence,
            occurred_at="2026-06-19T18:59:00Z",
        )

    def test_missing_authority_is_refused(self) -> None:
        decision = self.service.decide(
            self._request(
                HaltCause.MISSING_AUTHORITY,
                {
                    "authority_check_id": "authority-check-1",
                    "authority_evidence_hash": "authority-hash-1",
                    "authority_status": "missing",
                },
            )
        )
        self.assertEqual(decision.runtime_state, HaltOutcome.REFUSED)
        self.assertFalse(decision.recovery_allowed)

    def test_missing_evidence_is_held(self) -> None:
        decision = self.service.decide(
            self._request(
                HaltCause.MISSING_EVIDENCE,
                {
                    "missing_evidence": ["policy_evidence"],
                    "source_evidence_hash": "source-hash-1",
                },
            )
        )
        self.assertEqual(decision.runtime_state, HaltOutcome.HOLD)
        self.assertTrue(decision.recovery_allowed)

    def test_invalid_state_is_halted(self) -> None:
        decision = self.service.decide(
            self._request(
                HaltCause.INVALID_STATE,
                {
                    "runtime_transition_decision_id": "transition-1",
                    "runtime_transition_evidence_hash": "transition-hash-1",
                },
            )
        )
        self.assertEqual(decision.runtime_state, HaltOutcome.HALTED)

    def test_invalid_invariant_is_refused(self) -> None:
        decision = self.service.decide(
            self._request(
                HaltCause.FAILED_INVARIANT,
                {
                    "facts_hash": "facts-hash-1",
                    "invariant_result_id": "invariant-1",
                    "invariant_state": "invalid",
                },
            )
        )
        self.assertEqual(decision.runtime_state, HaltOutcome.REFUSED)

    def test_incomplete_invariant_is_held(self) -> None:
        decision = self.service.decide(
            self._request(
                HaltCause.FAILED_INVARIANT,
                {
                    "facts_hash": "facts-hash-1",
                    "invariant_result_id": "invariant-1",
                    "invariant_state": "hold",
                },
            )
        )
        self.assertEqual(decision.runtime_state, HaltOutcome.HOLD)

    def test_critical_invariant_is_halted(self) -> None:
        decision = self.service.decide(
            self._request(
                HaltCause.FAILED_INVARIANT,
                {
                    "facts_hash": "facts-hash-1",
                    "invariant_result_id": "invariant-1",
                    "invariant_state": "halt",
                },
            )
        )
        self.assertEqual(decision.runtime_state, HaltOutcome.HALTED)

    def test_expired_dependency_is_refused(self) -> None:
        decision = self.service.decide(
            self._request(
                HaltCause.EXPIRED_DEPENDENCY,
                {
                    "dependency_evidence_hash": "dependency-hash-1",
                    "dependency_id": "dependency-1",
                    "dependency_status": "expired",
                },
            )
        )
        self.assertEqual(decision.runtime_state, HaltOutcome.REFUSED)

    def test_invalid_dependency_is_refused(self) -> None:
        decision = self.service.decide(
            self._request(
                HaltCause.INVALID_DEPENDENCY,
                {
                    "dependency_evidence_hash": "dependency-hash-1",
                    "dependency_id": "dependency-1",
                    "dependency_status": "revoked",
                },
            )
        )
        self.assertEqual(decision.runtime_state, HaltOutcome.REFUSED)

    def test_unresolved_override_is_escalated(self) -> None:
        decision = self.service.decide(
            self._request(
                HaltCause.UNRESOLVED_OVERRIDE,
                {
                    "override_decision_id": "override-1",
                    "override_evidence_hash": "override-hash-1",
                    "override_outcome": "deferred",
                    "required_reviewer": "guardian-reviewer",
                },
            )
        )
        self.assertEqual(decision.runtime_state, HaltOutcome.ESCALATED)
        self.assertTrue(decision.recovery_allowed)
        self.assertEqual(decision.required_reviewer, "guardian-reviewer")

    def test_unsafe_execution_is_halted(self) -> None:
        decision = self.service.decide(
            self._request(
                HaltCause.UNSAFE_EXECUTION,
                {
                    "execution_decision_id": "execution-1",
                    "execution_evidence_hash": "execution-hash-1",
                    "execution_outcome": "blocked",
                },
            )
        )
        self.assertEqual(decision.runtime_state, HaltOutcome.HALTED)

    def test_critical_severity_always_halts(self) -> None:
        decision = self.service.decide(
            self._request(
                HaltCause.MISSING_EVIDENCE,
                {
                    "missing_evidence": ["authority_evidence"],
                    "source_evidence_hash": "source-hash-1",
                },
                severity=HaltSeverity.CRITICAL,
            )
        )
        self.assertEqual(decision.runtime_state, HaltOutcome.HALTED)
        self.assertEqual(decision.reason, "critical_failure")

    def test_invalid_cause_evidence_is_rejected(self) -> None:
        with self.assertRaises(HaltValidationError):
            self.service.decide(
                self._request(
                    HaltCause.UNSAFE_EXECUTION,
                    {
                        "execution_decision_id": "execution-1",
                        "execution_evidence_hash": "execution-hash-1",
                        "execution_outcome": "eligible",
                    },
                )
            )

    def test_decision_evidence_is_immutable_and_audited(self) -> None:
        decision = self.service.decide(
            self._request(
                HaltCause.INVALID_STATE,
                {
                    "runtime_transition_decision_id": "transition-1",
                    "runtime_transition_evidence_hash": "transition-hash-1",
                },
            )
        )
        event = self.audit.chain("halt-audit")[-1]

        self.assertEqual(event.record["event_type"], "runtime.halt.decision")
        self.assertEqual(event.record["details"]["evidence_hash"], decision.evidence_hash)
        self.assertEqual(
            decision.evidence.source_references,
            ("transition-1",),
        )
        with self.assertRaises(FrozenInstanceError):
            decision.evidence.state_before = "halted"

    def test_equivalent_evidence_is_deterministic_and_idempotent(self) -> None:
        first_request = self._request(
            HaltCause.MISSING_AUTHORITY,
            {
                "authority_status": "missing",
                "authority_check_id": "authority-check-1",
                "authority_evidence_hash": "authority-hash-1",
            },
        )
        second_request = self._request(
            HaltCause.MISSING_AUTHORITY,
            {
                "authority_evidence_hash": "authority-hash-1",
                "authority_check_id": "authority-check-1",
                "authority_status": "missing",
            },
        )
        first = self.service.decide(first_request)
        audit_count = len(self.audit.chain("halt-audit"))
        second = self.service.decide(second_request)

        self.assertEqual(first, second)
        self.assertEqual(len(self.audit.chain("halt-audit")), audit_count)


if __name__ == "__main__":
    unittest.main()
