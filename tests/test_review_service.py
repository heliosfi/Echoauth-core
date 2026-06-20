"""Sprint 2J deterministic Review Service tests."""

from __future__ import annotations

import unittest
from datetime import datetime, timezone

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth import AuthorizationDecision, AuthorizationOutcome
from echoauth.governance import (
    EscalationRequest,
    EscalationReviewType,
    EscalationService,
    ReviewOutcome,
    ReviewRequest,
    ReviewerAssignment,
    ReviewService,
)
from echoauth.policy import RefusalService, refusal_request_from_decision


class ReviewServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.audit = InMemoryAuditLogRepository()
        clock = lambda: datetime(2026, 6, 19, 14, 0, tzinfo=timezone.utc)
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
                        "reviewer-human-primary",
                        EscalationReviewType.HUMAN,
                        "authority-human-primary",
                    ),
                    ReviewerAssignment(
                        "reviewer-human-secondary",
                        EscalationReviewType.HUMAN,
                        "authority-human-secondary",
                    ),
                ),
                EscalationReviewType.GUARDIAN: (
                    ReviewerAssignment(
                        "reviewer-guardian",
                        EscalationReviewType.GUARDIAN,
                        "authority-guardian",
                    ),
                ),
                EscalationReviewType.PARENT: (
                    ReviewerAssignment(
                        "reviewer-parent",
                        EscalationReviewType.PARENT,
                        "authority-parent",
                    ),
                ),
                EscalationReviewType.ADMIN: (
                    ReviewerAssignment(
                        "reviewer-admin",
                        EscalationReviewType.ADMIN,
                        "authority-admin",
                    ),
                ),
                EscalationReviewType.CLINICAL: (
                    ReviewerAssignment(
                        "reviewer-clinical",
                        EscalationReviewType.CLINICAL,
                        "authority-clinical",
                    ),
                ),
            },
            clock=clock,
        )

    def _review_inputs(
        self,
        outcome: ReviewOutcome,
        review_type: EscalationReviewType = EscalationReviewType.HUMAN,
        *,
        authority_references: tuple[str, ...] | None = None,
        reviewer_id: str | None = None,
    ):
        authorization = AuthorizationDecision(
            authorization_decision_id=f"authorization-{review_type.value}",
            request_id="request-1",
            outcome=AuthorizationOutcome.DENIED,
            reason="policy_denied",
            evidence_hash=f"authorization-evidence-{review_type.value}",
            evidence={"policy": "denied"},
            decided_at="2026-06-19T12:00:00Z",
            policy_decision_id="policy-decision-1",
            audit_event_id=f"audit-authorization-{review_type.value}",
        )
        refusal_request = refusal_request_from_decision(
            authorization,
            refusal_request_id=f"refusal-{review_type.value}",
            evidence={"policy_decision_id": authorization.policy_decision_id},
        )
        refusal = self.refusal_service.refuse(refusal_request, authorization)
        escalation_request = EscalationRequest(
            escalation_id=f"escalation-{review_type.value}",
            request_id=authorization.request_id,
            subject_id="subject-1",
            trigger_state=authorization.outcome.value,
            trigger_reason=authorization.reason,
            required_authority_type=review_type,
            evidence={"refusal_audit_event_id": refusal.audit_event_id},
            authorization_decision_id=authorization.authorization_decision_id,
            refusal_decision_id=refusal.refusal_decision_id,
            refusal_category=refusal.category,
        )
        escalation = self.escalation_service.escalate(
            escalation_request, authorization, refusal
        )
        default_authority = {
            EscalationReviewType.HUMAN: "authority-human-primary",
            EscalationReviewType.GUARDIAN: "authority-guardian",
            EscalationReviewType.PARENT: "authority-parent",
            EscalationReviewType.ADMIN: "authority-admin",
            EscalationReviewType.CLINICAL: "authority-clinical",
        }[review_type]
        audit_references = tuple(
            reference
            for reference in (
                authorization.audit_event_id,
                refusal.audit_event_id,
                escalation.audit_event_id,
            )
            if reference
        )
        request = ReviewRequest(
            review_request_id=f"review-{review_type.value}-{outcome.value}",
            request_id=authorization.request_id,
            escalation_decision_id=escalation.escalation_decision_id,
            reviewer_id=reviewer_id or {
                EscalationReviewType.HUMAN: "reviewer-human-primary",
                EscalationReviewType.GUARDIAN: "reviewer-guardian",
                EscalationReviewType.PARENT: "reviewer-parent",
                EscalationReviewType.ADMIN: "reviewer-admin",
                EscalationReviewType.CLINICAL: "reviewer-clinical",
            }[review_type],
            requested_outcome=outcome,
            authority_references=(
                (default_authority,)
                if authority_references is None
                else authority_references
            ),
            delegation_references=("delegation-evidence-1",),
            policy_evidence={"policy_decision_id": authorization.policy_decision_id},
            refusal_evidence={
                "refusal_decision_id": refusal.refusal_decision_id,
                "refusal_evidence_hash": refusal.evidence_hash,
            },
            audit_references=audit_references,
            evidence={"review_record": "submitted"},
        )
        return request, escalation

    def _review(self, *args, **kwargs):
        request, escalation = self._review_inputs(*args, **kwargs)
        return self.review_service.review(request, escalation)

    def test_review_from_escalation(self) -> None:
        decision = self._review(
            ReviewOutcome.GUARDIAN_REVIEW_REQUIRED,
            EscalationReviewType.GUARDIAN,
        )
        self.assertEqual(decision.outcome, ReviewOutcome.GUARDIAN_REVIEW_REQUIRED)
        self.assertEqual(decision.reviewer_id, "reviewer-guardian")

    def test_review_approval_path(self) -> None:
        decision = self._review(ReviewOutcome.APPROVED_FOR_OVERRIDE_REVIEW)
        self.assertEqual(
            decision.outcome, ReviewOutcome.APPROVED_FOR_OVERRIDE_REVIEW
        )
        self.assertEqual(decision.reason, "review_recorded")

    def test_review_denial_path(self) -> None:
        decision = self._review(ReviewOutcome.DENIED_AFTER_REVIEW)
        self.assertEqual(decision.outcome, ReviewOutcome.DENIED_AFTER_REVIEW)

    def test_returned_for_information_path(self) -> None:
        decision = self._review(ReviewOutcome.RETURNED_FOR_INFORMATION)
        self.assertEqual(decision.outcome, ReviewOutcome.RETURNED_FOR_INFORMATION)

    def test_delegated_review_path(self) -> None:
        decision = self._review(ReviewOutcome.DELEGATED_REVIEW_REQUIRED)
        self.assertEqual(decision.outcome, ReviewOutcome.DELEGATED_REVIEW_REQUIRED)
        self.assertEqual(
            decision.evidence["delegation_references"],
            ("delegation-evidence-1",),
        )

    def test_unresolved_review_path(self) -> None:
        decision = self._review(
            ReviewOutcome.APPROVED_FOR_OVERRIDE_REVIEW,
            authority_references=(),
        )
        self.assertEqual(decision.outcome, ReviewOutcome.UNRESOLVED)
        self.assertIsNone(decision.reviewer_id)

    def test_non_assigned_reviewer_fails_closed(self) -> None:
        decision = self._review(
            ReviewOutcome.APPROVED_FOR_OVERRIDE_REVIEW,
            reviewer_id="reviewer-human-secondary",
            authority_references=(
                "authority-human-primary",
                "authority-human-secondary",
            ),
        )
        self.assertEqual(decision.outcome, ReviewOutcome.UNRESOLVED)
        self.assertIsNone(decision.reviewer_id)

    def test_deterministic_reviewer_assignment_uses_configured_order(self) -> None:
        decision = self._review(
            ReviewOutcome.ADMINISTRATIVE_REVIEW_REQUIRED,
            authority_references=(
                "authority-human-secondary",
                "authority-human-primary",
            ),
        )
        self.assertEqual(decision.reviewer_id, "reviewer-human-primary")
        self.assertEqual(
            decision.reviewer_authority_reference, "authority-human-primary"
        )

    def test_audit_evidence_packaging(self) -> None:
        request, escalation = self._review_inputs(
            ReviewOutcome.CLINICAL_REVIEW_REQUIRED,
            EscalationReviewType.CLINICAL,
        )
        decision = self.review_service.review(request, escalation)
        chain = self.audit.chain("runtime-audit")

        self.assertEqual(len(chain), 3)
        self.assertEqual(chain[-1].record["event_type"], "authorization.review")
        self.assertEqual(
            decision.evidence["escalation_decision_id"],
            escalation.escalation_decision_id,
        )
        self.assertEqual(
            decision.evidence["escalation_evidence_hash"], escalation.evidence_hash
        )
        self.assertEqual(chain[-1].record["details"]["evidence_hash"], decision.evidence_hash)

    def test_idempotent_review_processing(self) -> None:
        request, escalation = self._review_inputs(
            ReviewOutcome.PARENT_REVIEW_REQUIRED,
            EscalationReviewType.PARENT,
        )
        first = self.review_service.review(request, escalation)
        audit_count = len(self.audit.chain("runtime-audit"))
        second = self.review_service.review(request, escalation)

        self.assertEqual(first, second)
        self.assertEqual(len(self.audit.chain("runtime-audit")), audit_count)


if __name__ == "__main__":
    unittest.main()
