"""Sprint 2H deterministic Refusal Service tests."""

from __future__ import annotations

import unittest
from datetime import datetime, timezone

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth import AuthorizationDecision, AuthorizationOutcome
from echoauth.policy import (
    RefusalCategory,
    RefusalService,
    refusal_request_from_decision,
)


def _authorization_decision(
    outcome: AuthorizationOutcome,
    reason: str,
) -> AuthorizationDecision:
    return AuthorizationDecision(
        authorization_decision_id=f"authorization-{outcome.value}",
        request_id="request-1",
        outcome=outcome,
        reason=reason,
        evidence_hash=f"evidence-{outcome.value}",
        evidence={"dependency": reason},
        decided_at="2026-06-19T12:00:00Z",
        audit_event_id=f"audit-authorization-{outcome.value}",
    )


class RefusalServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.audit = InMemoryAuditLogRepository()
        self.service = RefusalService(
            self.audit,
            audit_chain_id="refusal-audit",
            clock=lambda: datetime(2026, 6, 19, 13, 0, tzinfo=timezone.utc),
        )

    def _refuse(self, decision: AuthorizationDecision):
        request = refusal_request_from_decision(
            decision,
            refusal_request_id=f"refusal-{decision.outcome.value}",
            evidence={"source_event": decision.audit_event_id},
        )
        return self.service.refuse(request, decision)

    def test_identity_refusal(self) -> None:
        refusal = self._refuse(
            _authorization_decision(
                AuthorizationOutcome.INVALID_IDENTITY, "identity_not_verified"
            )
        )
        self.assertEqual(refusal.category, RefusalCategory.INVALID_IDENTITY)

    def test_authority_refusal(self) -> None:
        refusal = self._refuse(
            _authorization_decision(
                AuthorizationOutcome.INVALID_AUTHORITY, "authority_not_valid"
            )
        )
        self.assertEqual(refusal.category, RefusalCategory.INVALID_AUTHORITY)

    def test_delegation_refusal(self) -> None:
        refusal = self._refuse(
            _authorization_decision(
                AuthorizationOutcome.INVALID_DELEGATION, "delegation_not_valid"
            )
        )
        self.assertEqual(refusal.category, RefusalCategory.INVALID_DELEGATION)

    def test_policy_denial_refusal(self) -> None:
        refusal = self._refuse(
            _authorization_decision(AuthorizationOutcome.DENIED, "policy_denied")
        )
        self.assertEqual(refusal.category, RefusalCategory.POLICY_DENIED)

    def test_revoked_refusal(self) -> None:
        refusal = self._refuse(
            _authorization_decision(AuthorizationOutcome.REVOKED, "authority_revoked")
        )
        self.assertEqual(refusal.category, RefusalCategory.REVOKED)

    def test_expired_refusal(self) -> None:
        refusal = self._refuse(
            _authorization_decision(AuthorizationOutcome.EXPIRED, "policy_expired")
        )
        self.assertEqual(refusal.category, RefusalCategory.EXPIRED)

    def test_conflict_refusal(self) -> None:
        refusal = self._refuse(
            _authorization_decision(AuthorizationOutcome.CONFLICT, "policy_conflict")
        )
        self.assertEqual(refusal.category, RefusalCategory.CONFLICT)

    def test_malformed_request_refusal(self) -> None:
        refusal = self._refuse(
            _authorization_decision(
                AuthorizationOutcome.DENIED, "invalid_authorization_request"
            )
        )
        self.assertEqual(refusal.category, RefusalCategory.MALFORMED_REQUEST)

    def test_deterministic_refusal_generation(self) -> None:
        decision = _authorization_decision(
            AuthorizationOutcome.INVALID_AUTHORITY, "authority_not_valid"
        )
        request = refusal_request_from_decision(
            decision,
            refusal_request_id="refusal-deterministic",
            evidence={"record": "authority-1"},
        )

        first = self.service.refuse(request, decision)
        audit_count = len(self.audit.chain("refusal-audit"))
        second = self.service.refuse(request, decision)

        self.assertEqual(first, second)
        self.assertEqual(len(self.audit.chain("refusal-audit")), audit_count)
        self.assertEqual(first.evidence["authorization_evidence_hash"], decision.evidence_hash)


if __name__ == "__main__":
    unittest.main()
