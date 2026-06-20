"""Sprint 2D Authority Resolution foundation tests."""

from __future__ import annotations

import unittest
from datetime import datetime, timezone

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth.authority import (
    AuthorityResolutionOutcome,
    AuthorityResolutionService,
    AuthorityScopeMatcher,
    AuthorityStatus,
    AuthorityType,
    InMemoryAuthorityRepository,
    ScopeMatchResult,
    build_authority_record,
)
from echoauth.models import AuthorityResolutionRequest, CanonicalJsonObject


class ExactScopeMatcher(AuthorityScopeMatcher):
    """Test-only matcher for explicit action and resource lists."""

    def match(
        self,
        scope: CanonicalJsonObject,
        *,
        action: str,
        resource: str,
        context: CanonicalJsonObject,
    ) -> ScopeMatchResult:
        if scope.get("ambiguous"):
            return ScopeMatchResult.AMBIGUOUS
        actions = scope.get("actions", ())
        resources = scope.get("resources", ())
        if action in actions and resource in resources:
            return ScopeMatchResult.MATCH
        return ScopeMatchResult.MISMATCH


def _request(**overrides: object) -> AuthorityResolutionRequest:
    values: dict[str, object] = {
        "request_id": "request-1",
        "subject_id": "subject-1",
        "requester_id": "source-1",
        "action": "read",
        "resource": "record-1",
        "context": {"channel": "test"},
        "identity_verdict_id": "identity-verdict-1",
        "authority_records": (),
        "policy_version": "policy-v1",
        "delegation_records": (),
        "revocation_records": (),
    }
    values.update(overrides)
    return AuthorityResolutionRequest(**values)  # type: ignore[arg-type]


class AuthorityResolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.audit = InMemoryAuditLogRepository()
        self.repository = InMemoryAuthorityRepository(
            self.audit, audit_chain_id="authority-audit"
        )
        self.clock = lambda: datetime(2026, 6, 19, 13, 0, tzinfo=timezone.utc)
        self.service = AuthorityResolutionService(
            self.repository,
            ExactScopeMatcher(),
            self.audit,
            audit_chain_id="authority-audit",
            clock=self.clock,
        )

    def _register(
        self,
        *,
        record_id: str = "authority-1",
        priority: int = 10,
        expires_at: str | None = "2026-07-19T12:00:00Z",
        authority_type: AuthorityType = AuthorityType.PARENT,
        scope: CanonicalJsonObject | None = None,
    ):
        record = build_authority_record(
            authority_record_id=record_id,
            authority_source_id="source-1",
            subject_id="subject-1",
            authority_type=authority_type,
            scope=scope or {"actions": ["read"], "resources": ["record-1"]},
            priority=priority,
            issued_at="2026-06-19T12:00:00Z",
            expires_at=expires_at,
            status=AuthorityStatus.ACTIVE,
        )
        return self.repository.create(
            record,
            actor_id="registry-admin",
            reason="authority_registered",
            occurred_at="2026-06-19T12:01:00Z",
            audit_event_id=f"audit-create-{record_id}",
        )

    def test_valid_authority_resolution(self) -> None:
        self._register()

        result = self.service.resolve(_request())

        self.assertEqual(result.outcome, AuthorityResolutionOutcome.AUTHORIZED)
        self.assertEqual(result.authority_record_id, "authority-1")
        self.assertEqual(result.authority_source_id, "source-1")
        self.assertEqual(len(self.audit.chain("authority-audit")), 2)

    def test_revoked_authority(self) -> None:
        self._register()
        self.repository.revoke(
            "authority-1",
            actor_id="registry-admin",
            reason="authority_revoked",
            occurred_at="2026-06-19T12:30:00Z",
            audit_event_id="audit-revoke-authority-1",
        )

        result = self.service.resolve(_request())

        self.assertEqual(result.outcome, AuthorityResolutionOutcome.REVOKED)

    def test_effective_revocation_record_revokes_active_authority(self) -> None:
        self._register()
        request = _request(
            revocation_records=(
                {
                    "revocation_id": "revocation-1",
                    "target_type": "authority",
                    "target_id": "authority-1",
                    "effective_at": "2026-06-19T12:30:00Z",
                },
            )
        )

        result = self.service.resolve(request)

        self.assertEqual(result.outcome, AuthorityResolutionOutcome.REVOKED)

    def test_expired_authority(self) -> None:
        self._register(expires_at="2026-06-19T12:30:00Z")

        result = self.service.resolve(_request())

        self.assertEqual(result.outcome, AuthorityResolutionOutcome.EXPIRED)

    def test_conflicting_authority(self) -> None:
        self._register(record_id="authority-1", priority=10)
        self._register(record_id="authority-2", priority=20)

        result = self.service.resolve(_request())

        self.assertEqual(result.outcome, AuthorityResolutionOutcome.CONFLICT)
        self.assertEqual(
            result.evaluated_authority_record_ids,
            ("authority-1", "authority-2"),
        )

    def test_insufficient_authority(self) -> None:
        result = self.service.resolve(_request())

        self.assertEqual(
            result.outcome, AuthorityResolutionOutcome.INSUFFICIENT_AUTHORITY
        )
        self.assertEqual(result.reason, "no_explicit_authority_record")

    def test_scope_mismatch_is_denied(self) -> None:
        self._register()

        result = self.service.resolve(_request(action="write"))

        self.assertEqual(result.outcome, AuthorityResolutionOutcome.DENIED)
        self.assertEqual(result.reason, "authority_scope_mismatch")

    def test_resolution_is_deterministic_and_audit_idempotent(self) -> None:
        self._register()
        request = _request()

        first = self.service.resolve(request)
        audit_count = len(self.audit.chain("authority-audit"))
        second = self.service.resolve(request)

        self.assertEqual(first, second)
        self.assertEqual(len(self.audit.chain("authority-audit")), audit_count)

    def test_invalid_revocation_evidence_is_denied(self) -> None:
        self._register()

        result = self.service.resolve(
            _request(revocation_records=({"target_type": "authority"},))
        )

        self.assertEqual(result.outcome, AuthorityResolutionOutcome.DENIED)
        self.assertEqual(result.reason, "invalid_authority_resolution_request")


if __name__ == "__main__":
    unittest.main()
