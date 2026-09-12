"""Focused SAL-12 currentness tests for the Runtime Authorization Gate.

These tests intentionally distinguish fresh reevaluation of the same
AuthorizationRequest from consumer-side replay of a previously issued
AuthorizationDecision. The latter remains outside the currently established
interface and is not claimed here.
"""

from __future__ import annotations

import unittest
from datetime import datetime, timezone

from echoauth.auth import AuthorizationOutcome
from echoauth.auth.permissions import DelegationState
from echoauth.identity import IdentityStatus
from tests import test_authorization_gate as gate_tests


class AuthorizationCurrentnessAdversarialTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = gate_tests.AuthorizationGateTests(
            methodName="test_successful_authorization"
        )
        self.fixture.setUp()

    def _assert_replaced_authorization(
        self,
        first,
        second,
        *,
        expected_outcome: AuthorizationOutcome,
        expected_reason: str,
    ) -> None:
        self.assertEqual(first.outcome, AuthorizationOutcome.AUTHORIZED)
        self.assertEqual(second.outcome, expected_outcome)
        self.assertEqual(second.reason, expected_reason)
        self.assertNotEqual(
            first.authorization_decision_id,
            second.authorization_decision_id,
        )
        self.assertNotEqual(first.evidence_hash, second.evidence_hash)

    def test_same_request_rechecks_authority_after_revocation(self) -> None:
        fixture = self.fixture
        fixture._register_policy()
        request = fixture._request()
        first = fixture.gate.authorize(request)

        fixture.now = datetime(2026, 6, 19, 13, 5, tzinfo=timezone.utc)
        fixture.authority_repository.revoke(
            "authority-1",
            actor_id="registry-admin",
            reason="authority_revoked_after_authorization",
            occurred_at="2026-06-19T13:05:00Z",
            audit_event_id="audit-authority-revoked-after-authorization",
        )
        second = fixture.gate.authorize(request)

        self._assert_replaced_authorization(
            first,
            second,
            expected_outcome=AuthorizationOutcome.REVOKED,
            expected_reason="authority_revoked",
        )

    def test_same_request_rechecks_authority_after_expiry(self) -> None:
        fixture = self.fixture
        fixture._register_policy()
        request = fixture._request()
        first = fixture.gate.authorize(request)

        fixture.now = datetime(2026, 7, 19, 12, 0, tzinfo=timezone.utc)
        second = fixture.gate.authorize(request)

        self._assert_replaced_authorization(
            first,
            second,
            expected_outcome=AuthorizationOutcome.EXPIRED,
            expected_reason="authority_expired",
        )
        self.assertNotEqual(first.decided_at, second.decided_at)

    def test_same_request_rechecks_policy_after_expiry(self) -> None:
        fixture = self.fixture
        fixture._register_policy(expires_at="2026-06-19T13:30:00Z")
        request = fixture._request()
        first = fixture.gate.authorize(request)

        fixture.now = datetime(2026, 6, 19, 13, 30, tzinfo=timezone.utc)
        second = fixture.gate.authorize(request)

        self._assert_replaced_authorization(
            first,
            second,
            expected_outcome=AuthorizationOutcome.EXPIRED,
            expected_reason="policy_expired",
        )
        self.assertNotEqual(first.decided_at, second.decided_at)

    def test_same_request_rechecks_identity_after_suspension(self) -> None:
        fixture = self.fixture
        fixture._register_policy()
        request = fixture._request()
        first = fixture.gate.authorize(request)

        fixture.now = datetime(2026, 6, 19, 13, 5, tzinfo=timezone.utc)
        fixture.identity_repository.transition(
            "identity-parent",
            IdentityStatus.SUSPENDED,
            updated_at="2026-06-19T13:05:00Z",
        )
        second = fixture.gate.authorize(request)

        self._assert_replaced_authorization(
            first,
            second,
            expected_outcome=AuthorizationOutcome.INVALID_IDENTITY,
            expected_reason="identity_not_verified",
        )

    def test_same_request_rechecks_delegation_after_revocation(self) -> None:
        fixture = self.fixture
        fixture._create_delegation()
        fixture._register_policy()
        request = fixture._request(
            requester_id="teacher-1",
            delegation_id="delegation-1",
        )
        first = fixture.gate.authorize(request)

        fixture.now = datetime(2026, 6, 19, 13, 5, tzinfo=timezone.utc)
        fixture.delegation_repository.update_state(
            "delegation-1",
            DelegationState.REVOKED,
            actor_id="parent-1",
            reason="delegation_revoked_after_authorization",
            occurred_at="2026-06-19T13:05:00Z",
            audit_event_id="audit-delegation-revoked-after-authorization",
        )
        second = fixture.gate.authorize(request)

        self._assert_replaced_authorization(
            first,
            second,
            expected_outcome=AuthorizationOutcome.REVOKED,
            expected_reason="delegation_revoked",
        )


if __name__ == "__main__":
    unittest.main()
