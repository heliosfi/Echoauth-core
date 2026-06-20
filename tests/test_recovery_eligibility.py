"""Sprint 2P Recovery Eligibility validation tests."""

from __future__ import annotations

import unittest
from dataclasses import asdict, replace
from datetime import datetime, timezone

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth.authority_resolution import (
    AuthorityResolutionOutcome,
    AuthorityResolutionResult,
)
from echoauth.governance.review_models import ReviewDecision, ReviewOutcome
from echoauth.models import AuditAppendState, AuditRecord
from echoauth.runtime.halt_models import (
    HaltCause,
    HaltDecision,
    HaltDecisionEvidence,
    HaltOutcome,
    HaltSeverity,
)
from echoauth.runtime.recovery import (
    RecoveryEligibilityRequest,
    RecoveryEligibilityService,
    RecoveryEligibilityValidationError,
    RecoveryFailureCode,
    RecoveryOutcome,
    RecoveryPath,
    RecoveryProtocolStatus,
    RecoveryReviewProtocol,
    RecoverySourceState,
    recovery_review_protocol_hash,
)

NOW = datetime(2026, 6, 19, 16, 0, tzinfo=timezone.utc)
NOW_TEXT = "2026-06-19T16:00:00Z"


class RecoveryEligibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.audit = InMemoryAuditLogRepository()
        original = self.audit.append(
            AuditRecord(
                event_type="execution.eligibility.validation",
                actor_id="execution_control",
                request_id="request-1",
                reason="execution_blocked",
                details={"evidence_hash": "original-evidence"},
                occurred_at="2026-06-19T15:00:00Z",
            ),
            audit_event_id="audit-original",
            chain_id="chain-1",
        )
        self.assertIs(original.append_state, AuditAppendState.ACCEPTED)
        halt_audit = self.audit.append(
            AuditRecord(
                event_type="runtime.halt.decision",
                actor_id="halt_decision_service",
                request_id="request-1",
                reason="evidence_missing",
                details={
                    "evidence_hash": "halt-evidence",
                    "halt_decision_id": "haltdec-1",
                    "outcome": "hold",
                },
                occurred_at="2026-06-19T15:01:00Z",
            ),
            audit_event_id="audit-halt",
            chain_id="chain-1",
        )
        self.assertIs(halt_audit.append_state, AuditAppendState.ACCEPTED)
        self.original_event_hash = str(original.event_hash)
        self.service = RecoveryEligibilityService(
            self.audit,
            audit_chain_id="chain-1",
            clock=lambda: NOW,
        )
        self.authority = AuthorityResolutionResult(
            authority_resolution_id="ares-1",
            request_id="request-1",
            outcome=AuthorityResolutionOutcome.AUTHORIZED,
            reason="explicit_authority_record_matched",
            evidence_hash="authority-evidence",
            resolved_at="2026-06-19T14:59:00Z",
            evaluated_authority_record_ids=("authority-record-1",),
            authority_record_id="authority-record-1",
            authority_source_id="recovery-authority",
            audit_event_id="audit-authority",
        )
        halt_evidence = HaltDecisionEvidence(
            classifier_version="echoauth.halt-decision.v1",
            halt_event_id="halt-event-1",
            failure_type=HaltCause.MISSING_EVIDENCE,
            severity=HaltSeverity.MEDIUM,
            state_before="ready",
            source_evidence_hash="halt-source-evidence",
            source_references=("original-evidence",),
            occurred_at="2026-06-19T15:01:00Z",
        )
        self.halt = HaltDecision(
            halt_decision_id="haltdec-1",
            halt_event_id="halt-event-1",
            request_id="request-1",
            runtime_state=HaltOutcome.HOLD,
            reason="evidence_missing",
            recovery_allowed=True,
            required_reviewer=None,
            evidence=halt_evidence,
            evidence_hash="halt-evidence",
            decided_at="2026-06-19T15:01:00Z",
            audit_event_id="audit-halt",
        )
        self.request = RecoveryEligibilityRequest(
            recovery_id="recovery-1",
            request_id="request-1",
            source_state=RecoverySourceState.EXECUTION_BLOCKED,
            failure_code=RecoveryFailureCode.MISSING_EVIDENCE,
            requested_recovery_path=RecoveryPath.REVALIDATE_REQUEST,
            recovery_actor_id="actor-1",
            recovery_authority_reference="recovery-authority",
            authority_resolution_id="ares-1",
            authority_evidence_hash="authority-evidence",
            halt_decision_id="haltdec-1",
            halt_decision_evidence_hash="halt-evidence",
            original_failure_evidence_hash="original-evidence",
            original_failure_audit_event_id="audit-original",
            changed_evidence_reference="evidence/new-1",
            changed_evidence_hash="changed-evidence",
            recovery_policy_version="recovery.v1",
            guard_evidence={
                "audit_chain_id": "chain-1",
                "original_failure_event_hash": self.original_event_hash,
                "halt_audit_event_id": "audit-halt",
                "missing_evidence_refs": ["authority_record"],
            },
            invalidated_token_refs=(),
            requested_at=NOW_TEXT,
        )

    def test_execution_blocked_request_requires_revalidation(self) -> None:
        result = self.service.validate(self.request, self.authority, self.halt)

        self.assertIs(result.outcome, RecoveryOutcome.REVALIDATION_REQUIRED)
        self.assertEqual(
            result.required_validations,
            (
                "identity",
                "authority",
                "delegation_if_applicable",
                "policy",
                "invariants",
                "audit_path",
            ),
        )
        self.assertFalse(hasattr(result, "recovery_allowed"))

    def test_all_execution_blocked_failure_policies_are_enforced(self) -> None:
        cases = (
            (
                RecoveryFailureCode.DEPENDENCY_UNAVAILABLE,
                {
                    "dependency_id": "dependency-1",
                    "dependency_status": "available",
                    "dependency_evidence_hash": "dependency-hash",
                },
            ),
            (
                RecoveryFailureCode.AUDIT_PATH_DEGRADED,
                {
                    "audit_path_status": "restored",
                    "audit_path_evidence_hash": "audit-path-hash",
                },
            ),
            (
                RecoveryFailureCode.COORDINATION_INTERRUPTED,
                {"coordination_context_hash": "coordination-hash"},
            ),
        )
        base = {
            "audit_chain_id": "chain-1",
            "original_failure_event_hash": self.original_event_hash,
            "halt_audit_event_id": "audit-halt",
        }
        for index, (failure_code, extra) in enumerate(cases, start=2):
            with self.subTest(failure_code=failure_code):
                request = replace(
                    self.request,
                    recovery_id=f"recovery-{index}",
                    failure_code=failure_code,
                    guard_evidence={**base, **extra},
                )
                result = self.service.validate(request, self.authority, self.halt)
                self.assertIs(
                    result.outcome, RecoveryOutcome.REVALIDATION_REQUIRED
                )

    def test_unresolved_guard_fails_closed(self) -> None:
        request = replace(
            self.request,
            failure_code=RecoveryFailureCode.DEPENDENCY_UNAVAILABLE,
            guard_evidence={
                "audit_chain_id": "chain-1",
                "original_failure_event_hash": self.original_event_hash,
                "halt_audit_event_id": "audit-halt",
                "dependency_id": "dependency-1",
                "dependency_status": "unavailable",
                "dependency_evidence_hash": "dependency-hash",
            },
        )

        result = self.service.validate(request, self.authority, self.halt)

        self.assertIs(result.outcome, RecoveryOutcome.REJECTED)
        self.assertEqual(result.reason, "recovery_guard_not_satisfied")

    def test_halted_request_requires_new_request(self) -> None:
        request = replace(
            self.request,
            source_state=RecoverySourceState.HALTED,
            failure_code=RecoveryFailureCode.INVALID_STATE,
            guard_evidence={
                "audit_chain_id": "chain-1",
                "original_failure_event_hash": self.original_event_hash,
                "halt_audit_event_id": "audit-halt",
                "runtime_transition_decision_id": "transition-1",
                "runtime_transition_evidence_hash": "transition-hash",
            },
        )
        halt = replace(self.halt, runtime_state=HaltOutcome.HALTED)

        result = self.service.validate(request, self.authority, halt)

        self.assertIs(result.outcome, RecoveryOutcome.NEW_REQUEST_REQUIRED)
        self.assertEqual(result.required_validations, ())

    def test_authority_and_changed_evidence_fail_closed(self) -> None:
        invalid_authority = replace(
            self.authority,
            outcome=AuthorityResolutionOutcome.REVOKED,
        )
        authority_result = self.service.validate(
            self.request, invalid_authority, self.halt
        )
        changed_result = self.service.validate(
            replace(
                self.request,
                recovery_id="recovery-changed",
                changed_evidence_hash="original-evidence",
            ),
            self.authority,
            self.halt,
        )

        self.assertIs(authority_result.outcome, RecoveryOutcome.REJECTED)
        self.assertIs(changed_result.outcome, RecoveryOutcome.REJECTED)

    def test_missing_or_mismatched_audit_links_are_rejected(self) -> None:
        request = replace(
            self.request,
            guard_evidence={
                **self.request.guard_evidence,
                "original_failure_event_hash": "wrong-event-hash",
            },
        )

        result = self.service.validate(request, self.authority, self.halt)

        self.assertIs(result.outcome, RecoveryOutcome.REJECTED)
        self.assertEqual(result.reason, "original_failure_audit_mismatch")

    def test_critical_halt_requires_bound_recovery_review_protocol(self) -> None:
        halt = replace(self.halt, runtime_state=HaltOutcome.HALTED)
        review = ReviewDecision(
            review_decision_id="review-1",
            review_request_id="review-request-1",
            request_id="request-1",
            escalation_decision_id="escalation-1",
            outcome=ReviewOutcome.UNRESOLVED,
            reviewer_id="reviewer-1",
            reviewer_authority_reference="review-authority",
            reason="recovery_protocol_reviewed",
            evidence_hash="review-evidence",
            evidence={},
            created_at="2026-06-19T15:30:00Z",
            audit_event_id="audit-review",
        )
        review_authority = replace(
            self.authority,
            authority_resolution_id="ares-review",
            authority_source_id="review-authority",
            evidence_hash="review-authority-evidence",
        )
        protocol = RecoveryReviewProtocol(
            protocol_id="recovery-review-1",
            protocol_version="1",
            protocol_status=RecoveryProtocolStatus.ACTIVE,
            request_id="request-1",
            halt_decision_id="haltdec-1",
            halt_decision_evidence_hash="halt-evidence",
            review_decision_id="review-1",
            review_decision_evidence_hash="review-evidence",
            reviewer_id="reviewer-1",
            reviewer_authority_reference="review-authority",
            reviewer_authority_resolution_id="ares-review",
            reviewer_authority_evidence_hash="review-authority-evidence",
            permitted_recovery_path=RecoveryPath.REVALIDATE_REQUEST,
            scope={"recovery": "request-1"},
            expires_at="2026-06-20T16:00:00Z",
            evidence_hash="pending",
        )
        protocol = replace(
            protocol, evidence_hash=recovery_review_protocol_hash(protocol)
        )
        request = replace(
            self.request,
            source_state=RecoverySourceState.HALTED,
            failure_code=RecoveryFailureCode.CRITICAL_INVARIANT_FAILURE,
            guard_evidence={
                "audit_chain_id": "chain-1",
                "original_failure_event_hash": self.original_event_hash,
                "halt_audit_event_id": "audit-halt",
                "invariant_result_id": "invariant-1",
                "invariant_state": "valid",
                "invariant_facts_hash": "invariant-facts",
            },
            recovery_review_protocol=protocol,
        )

        result = self.service.validate(
            request,
            self.authority,
            halt,
            review_decision=review,
            review_authority_resolution=review_authority,
        )

        self.assertIs(result.outcome, RecoveryOutcome.REVALIDATION_REQUIRED)

    def test_critical_halt_without_protocol_requires_new_request(self) -> None:
        request = replace(
            self.request,
            source_state=RecoverySourceState.HALTED,
            failure_code=RecoveryFailureCode.CRITICAL_INVARIANT_FAILURE,
            guard_evidence={
                "audit_chain_id": "chain-1",
                "original_failure_event_hash": self.original_event_hash,
                "halt_audit_event_id": "audit-halt",
                "invariant_result_id": "invariant-1",
                "invariant_state": "valid",
                "invariant_facts_hash": "invariant-facts",
            },
        )

        result = self.service.validate(
            request,
            self.authority,
            replace(self.halt, runtime_state=HaltOutcome.HALTED),
        )

        self.assertIs(result.outcome, RecoveryOutcome.NEW_REQUEST_REQUIRED)

    def test_audit_events_are_eligibility_only_and_preserve_sources(self) -> None:
        original_before = self.audit.get("audit-original").canonical_text
        halt_before = self.audit.get("audit-halt").canonical_text

        result = self.service.validate(self.request, self.authority, self.halt)

        events = self.audit.chain("chain-1")
        event_types = [event.record["event_type"] for event in events]
        self.assertEqual(
            event_types[-2:],
            ["recovery.eligibility.requested", "recovery.eligibility.decided"],
        )
        self.assertNotIn("runtime.recovered", event_types)
        self.assertEqual(
            self.audit.get("audit-original").canonical_text, original_before
        )
        self.assertEqual(self.audit.get("audit-halt").canonical_text, halt_before)
        self.assertEqual(result.audit_event_id, events[-1].audit_event_id)

    def test_results_are_deterministic_and_idempotent(self) -> None:
        first = self.service.validate(self.request, self.authority, self.halt)
        event_count = len(self.audit.chain("chain-1"))
        second = self.service.validate(self.request, self.authority, self.halt)

        self.assertEqual(first, second)
        self.assertEqual(len(self.audit.chain("chain-1")), event_count)

    def test_invalid_state_failure_pair_is_rejected_before_audit(self) -> None:
        request = replace(
            self.request,
            source_state=RecoverySourceState.HALTED,
            failure_code=RecoveryFailureCode.MISSING_EVIDENCE,
        )

        with self.assertRaises(RecoveryEligibilityValidationError):
            self.service.validate(request, self.authority, self.halt)

        self.assertEqual(len(self.audit.chain("chain-1")), 2)


if __name__ == "__main__":
    unittest.main()
