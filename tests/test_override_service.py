"""Sprint 2K deterministic Override Service tests."""

from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timezone

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth import AuthorizationDecision, AuthorizationOutcome
from echoauth.governance import (
    EscalationRequest,
    EscalationReviewType,
    EscalationService,
    OverrideAuthority,
    OverrideOutcome,
    OverrideRequest,
    OverrideService,
    OverrideValidationError,
    ReviewOutcome,
    ReviewRequest,
    ReviewerAssignment,
    ReviewService,
)
from echoauth.policy import RefusalService, refusal_request_from_decision


class OverrideServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.audit = InMemoryAuditLogRepository()
        clock = lambda: datetime(2026, 6, 19, 15, 0, tzinfo=timezone.utc)
        self.refusal_service = RefusalService(
            self.audit, audit_chain_id="runtime-audit", clock=clock
        )
        self.escalation_service = EscalationService(
            self.audit, audit_chain_id="runtime-audit", clock=clock
        )
        self.review_service = ReviewService(
            self.audit,
            audit_chain_id="runtime-audit",
            reviewer_assignments={
                EscalationReviewType.HUMAN: (
                    ReviewerAssignment(
                        "reviewer-human",
                        EscalationReviewType.HUMAN,
                        "authority-review-human",
                    ),
                )
            },
            clock=clock,
        )
        self.override_service = OverrideService(
            self.audit,
            audit_chain_id="runtime-audit",
            override_authorities=(
                OverrideAuthority("override-officer", "authority-override-1"),
            ),
            clock=clock,
        )

    def _inputs(
        self,
        review_outcome: ReviewOutcome,
        *,
        expires_at: str = "2026-06-19T15:05:00Z",
        override_authority_id: str = "override-officer",
        override_authority_reference: str = "authority-override-1",
        declared_by: str = "override-officer",
    ):
        authorization = AuthorizationDecision(
            authorization_decision_id="authorization-denied",
            request_id="request-1",
            outcome=AuthorizationOutcome.DENIED,
            reason="policy_denied",
            evidence_hash="authorization-evidence-denied",
            evidence={"policy": "denied"},
            decided_at="2026-06-19T12:00:00Z",
            policy_decision_id="policy-decision-1",
            audit_event_id="audit-authorization-denied",
        )
        refusal_request = refusal_request_from_decision(
            authorization,
            refusal_request_id="refusal-denied",
            evidence={"policy_decision_id": authorization.policy_decision_id},
        )
        refusal = self.refusal_service.refuse(refusal_request, authorization)
        escalation_request = EscalationRequest(
            escalation_id="escalation-human",
            request_id=authorization.request_id,
            subject_id="subject-1",
            trigger_state=authorization.outcome.value,
            trigger_reason=authorization.reason,
            required_authority_type=EscalationReviewType.HUMAN,
            evidence={"refusal_audit_event_id": refusal.audit_event_id},
            authorization_decision_id=authorization.authorization_decision_id,
            refusal_decision_id=refusal.refusal_decision_id,
            refusal_category=refusal.category,
        )
        escalation = self.escalation_service.escalate(
            escalation_request, authorization, refusal
        )
        review_request = ReviewRequest(
            review_request_id=f"review-{review_outcome.value}",
            request_id=authorization.request_id,
            escalation_decision_id=escalation.escalation_decision_id,
            reviewer_id="reviewer-human",
            requested_outcome=review_outcome,
            authority_references=("authority-review-human",),
            delegation_references=(),
            policy_evidence={"policy_decision_id": authorization.policy_decision_id},
            refusal_evidence={
                "refusal_decision_id": refusal.refusal_decision_id,
                "refusal_evidence_hash": refusal.evidence_hash,
            },
            audit_references=tuple(
                reference
                for reference in (
                    authorization.audit_event_id,
                    refusal.audit_event_id,
                    escalation.audit_event_id,
                )
                if reference
            ),
            evidence={"review": "submitted"},
        )
        review = self.review_service.review(review_request, escalation)
        audit_references = tuple(
            reference
            for reference in (
                authorization.audit_event_id,
                refusal.audit_event_id,
                escalation.audit_event_id,
                review.audit_event_id,
            )
            if reference
        )
        request = OverrideRequest(
            override_id=f"override-{review_outcome.value}",
            request_id=authorization.request_id,
            subject_id="subject-1",
            declared_by=declared_by,
            emergency_type="immediate_safety",
            requested_action="protect_subject",
            override_authority_id=override_authority_id,
            override_authority_reference=override_authority_reference,
            policy_version="policy-v1",
            expires_at=expires_at,
            effective_scope={"actions": ["protect_subject"]},
            evidence={"emergency_record": "record-1"},
            audit_references=audit_references,
        )
        return request, authorization, refusal, escalation, review

    def _decide(self, *args, **kwargs):
        inputs = self._inputs(*args, **kwargs)
        return self.override_service.decide(*inputs)

    def test_override_approval_classification(self) -> None:
        decision = self._decide(ReviewOutcome.APPROVED_FOR_OVERRIDE_REVIEW)
        self.assertEqual(decision.outcome, OverrideOutcome.APPROVED)
        self.assertEqual(decision.reason.code, "override_record_approved")
        self.assertTrue(decision.review_required)

    def test_override_denial_classification(self) -> None:
        decision = self._decide(ReviewOutcome.DENIED_AFTER_REVIEW)
        self.assertEqual(decision.outcome, OverrideOutcome.DENIED)
        self.assertEqual(decision.reason.code, "review_denied")

    def test_override_deferred_classification(self) -> None:
        decision = self._decide(ReviewOutcome.RETURNED_FOR_INFORMATION)
        self.assertEqual(decision.outcome, OverrideOutcome.DEFERRED)
        self.assertEqual(decision.reason.code, "additional_review_required")

    def test_override_expiration_classification(self) -> None:
        decision = self._decide(
            ReviewOutcome.APPROVED_FOR_OVERRIDE_REVIEW,
            expires_at="2026-06-19T14:59:59Z",
        )
        self.assertEqual(decision.outcome, OverrideOutcome.EXPIRED)

    def test_missing_explicit_override_authority_fails_closed(self) -> None:
        decision = self._decide(
            ReviewOutcome.APPROVED_FOR_OVERRIDE_REVIEW,
            override_authority_id="unknown-authority",
            override_authority_reference="unknown-reference",
            declared_by="unknown-authority",
        )
        self.assertEqual(decision.outcome, OverrideOutcome.DENIED)
        self.assertFalse(decision.reason.authority_valid)

    def test_inconsistent_evidence_chain_is_rejected(self) -> None:
        request, authorization, refusal, escalation, review = self._inputs(
            ReviewOutcome.APPROVED_FOR_OVERRIDE_REVIEW
        )
        invalid_review = replace(review, escalation_decision_id="wrong-escalation")
        with self.assertRaises(OverrideValidationError):
            self.override_service.decide(
                request, authorization, refusal, escalation, invalid_review
            )

    def test_override_evidence_is_immutable_and_audited(self) -> None:
        decision = self._decide(ReviewOutcome.APPROVED_FOR_OVERRIDE_REVIEW)
        chain = self.audit.chain("runtime-audit")

        self.assertEqual(len(chain), 4)
        self.assertEqual(chain[-1].record["event_type"], "authorization.override")
        self.assertEqual(
            chain[-1].record["details"]["evidence_hash"], decision.evidence_hash
        )
        with self.assertRaises(TypeError):
            decision.effective_scope["actions"] = ()
        with self.assertRaises(FrozenInstanceError):
            decision.evidence.policy_version = "changed"

    def test_override_processing_is_idempotent(self) -> None:
        inputs = self._inputs(ReviewOutcome.APPROVED_FOR_OVERRIDE_REVIEW)
        first = self.override_service.decide(*inputs)
        audit_count = len(self.audit.chain("runtime-audit"))
        second = self.override_service.decide(*inputs)

        self.assertEqual(first, second)
        self.assertEqual(len(self.audit.chain("runtime-audit")), audit_count)


if __name__ == "__main__":
    unittest.main()
