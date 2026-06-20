"""Sprint 2I deterministic Escalation Service tests."""

from __future__ import annotations

import unittest
from datetime import datetime, timezone

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth import AuthorizationDecision, AuthorizationOutcome
from echoauth.governance import (
    EscalationCategory,
    EscalationRequest,
    EscalationReviewType,
    EscalationService,
    EscalationState,
    EscalationValidationError,
)
from echoauth.policy import RefusalService, refusal_request_from_decision


def _authorization_decision(
    outcome: AuthorizationOutcome,
    reason: str,
) -> AuthorizationDecision:
    return AuthorizationDecision(
        authorization_decision_id=f"authorization-{outcome.value}-{reason}",
        request_id="request-1",
        outcome=outcome,
        reason=reason,
        evidence_hash=f"evidence-{outcome.value}-{reason}",
        evidence={"dependency": reason},
        decided_at="2026-06-19T12:00:00Z",
        audit_event_id=f"audit-authorization-{outcome.value}-{reason}",
    )


class EscalationServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.audit = InMemoryAuditLogRepository()
        clock = lambda: datetime(2026, 6, 19, 13, 0, tzinfo=timezone.utc)
        self.refusal_service = RefusalService(
            self.audit,
            audit_chain_id="runtime-audit",
            clock=clock,
        )
        self.escalation_service = EscalationService(
            self.audit,
            audit_chain_id="runtime-audit",
            clock=clock,
        )

    def _inputs(
        self,
        outcome: AuthorizationOutcome,
        reason: str,
        review_type: EscalationReviewType,
        *,
        recoverable: bool = False,
    ):
        authorization = _authorization_decision(outcome, reason)
        refusal_request = refusal_request_from_decision(
            authorization,
            refusal_request_id=f"refusal-{outcome.value}-{reason}",
            recoverable=recoverable,
            evidence={"source_event": authorization.audit_event_id},
        )
        refusal = self.refusal_service.refuse(refusal_request, authorization)
        escalation = EscalationRequest(
            escalation_id=f"escalation-{outcome.value}-{review_type.value}",
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
        return escalation, authorization, refusal

    def _escalate(self, *args, **kwargs):
        request, authorization, refusal = self._inputs(*args, **kwargs)
        return self.escalation_service.escalate(request, authorization, refusal)

    def test_escalation_from_refusal(self) -> None:
        decision = self._escalate(
            AuthorizationOutcome.DENIED,
            "policy_denied",
            EscalationReviewType.HUMAN,
        )
        self.assertEqual(decision.category, EscalationCategory.HUMAN_REVIEW_REQUIRED)
        self.assertEqual(decision.escalation_state, EscalationState.OPENED)
        self.assertEqual(decision.resolution, "none")

    def test_escalation_from_conflict(self) -> None:
        decision = self._escalate(
            AuthorizationOutcome.CONFLICT,
            "policy_conflict",
            EscalationReviewType.ADMIN,
        )
        self.assertEqual(decision.category, EscalationCategory.ADMIN_REVIEW_REQUIRED)

    def test_escalation_from_revoked_outcome(self) -> None:
        decision = self._escalate(
            AuthorizationOutcome.REVOKED,
            "authority_revoked",
            EscalationReviewType.PARENT,
        )
        self.assertEqual(decision.category, EscalationCategory.PARENT_REVIEW_REQUIRED)

    def test_escalation_from_expired_outcome(self) -> None:
        decision = self._escalate(
            AuthorizationOutcome.EXPIRED,
            "authority_expired",
            EscalationReviewType.GUARDIAN,
        )
        self.assertEqual(decision.category, EscalationCategory.GUARDIAN_REVIEW_REQUIRED)

    def test_escalation_from_unavailable_dependency(self) -> None:
        decision = self._escalate(
            AuthorizationOutcome.INVALID_POLICY,
            "policy_dependency_failed",
            EscalationReviewType.CLINICAL,
            recoverable=True,
        )
        self.assertEqual(decision.category, EscalationCategory.SYSTEM_HOLD)

    def test_no_escalation_available(self) -> None:
        decision = self._escalate(
            AuthorizationOutcome.DENIED,
            "invalid_authorization_request",
            EscalationReviewType.NONE,
        )
        self.assertEqual(
            decision.category, EscalationCategory.NO_ESCALATION_AVAILABLE
        )
        self.assertEqual(decision.resolution, "none")

    def test_all_explicit_review_routes_are_deterministic(self) -> None:
        expected = {
            EscalationReviewType.HUMAN: EscalationCategory.HUMAN_REVIEW_REQUIRED,
            EscalationReviewType.GUARDIAN: EscalationCategory.GUARDIAN_REVIEW_REQUIRED,
            EscalationReviewType.PARENT: EscalationCategory.PARENT_REVIEW_REQUIRED,
            EscalationReviewType.ADMIN: EscalationCategory.ADMIN_REVIEW_REQUIRED,
            EscalationReviewType.CLINICAL: EscalationCategory.CLINICAL_REVIEW_REQUIRED,
        }
        for review_type, category in expected.items():
            with self.subTest(review_type=review_type):
                decision = self._escalate(
                    AuthorizationOutcome.DENIED, "policy_denied", review_type
                )
                self.assertEqual(decision.category, category)

    def test_deterministic_escalation_classification(self) -> None:
        request, authorization, refusal = self._inputs(
            AuthorizationOutcome.CONFLICT,
            "authority_conflict",
            EscalationReviewType.HUMAN,
        )
        first = self.escalation_service.escalate(request, authorization, refusal)
        audit_count = len(self.audit.chain("runtime-audit"))
        second = self.escalation_service.escalate(request, authorization, refusal)

        self.assertEqual(first, second)
        self.assertEqual(len(self.audit.chain("runtime-audit")), audit_count)

    def test_audit_evidence_packaging(self) -> None:
        request, authorization, refusal = self._inputs(
            AuthorizationOutcome.REVOKED,
            "delegation_revoked",
            EscalationReviewType.CLINICAL,
        )
        decision = self.escalation_service.escalate(request, authorization, refusal)
        chain = self.audit.chain("runtime-audit")

        self.assertEqual(len(chain), 2)
        self.assertEqual(chain[-1].record["event_type"], "authorization.escalation")
        self.assertEqual(
            decision.evidence["authorization_decision_id"],
            authorization.authorization_decision_id,
        )
        self.assertEqual(
            decision.evidence["refusal_decision_id"], refusal.refusal_decision_id
        )
        self.assertEqual(
            decision.evidence["refusal_audit_event_id"], refusal.audit_event_id
        )
        self.assertEqual(chain[-1].record["details"]["evidence_hash"], decision.evidence_hash)

    def test_authorized_decision_cannot_be_escalated(self) -> None:
        request, _, refusal = self._inputs(
            AuthorizationOutcome.DENIED,
            "policy_denied",
            EscalationReviewType.HUMAN,
        )
        authorized = _authorization_decision(
            AuthorizationOutcome.AUTHORIZED, "authorization_dependencies_satisfied"
        )
        with self.assertRaises(EscalationValidationError):
            self.escalation_service.escalate(request, authorized, refusal)

    def test_mismatched_refusal_evidence_fails_closed(self) -> None:
        request, authorization, refusal = self._inputs(
            AuthorizationOutcome.DENIED,
            "policy_denied",
            EscalationReviewType.HUMAN,
        )
        other_authorization = _authorization_decision(
            AuthorizationOutcome.CONFLICT, "policy_conflict"
        )
        with self.assertRaises(EscalationValidationError):
            self.escalation_service.escalate(
                request, other_authorization, refusal
            )


if __name__ == "__main__":
    unittest.main()
