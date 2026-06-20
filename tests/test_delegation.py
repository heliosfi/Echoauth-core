"""Sprint 2E canonical Delegation foundation tests."""

from __future__ import annotations

import unittest
from datetime import datetime, timezone

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth.authority import (
    AuthorityResolutionService,
    AuthorityScopeMatcher,
    AuthorityStatus,
    AuthorityType,
    InMemoryAuthorityRepository,
    ScopeMatchResult,
    build_authority_record,
)
from echoauth.auth.permissions import (
    DelegationContextMatch,
    DelegationContextMatcher,
    DelegationState,
    DelegationValidationError,
    DelegationValidationOutcome,
    DelegationValidationRequest,
    DelegationValidationService,
    InMemoryDelegationRepository,
    build_delegation_grant,
)
from echoauth.models import AuthorityResolutionRequest, CanonicalJsonObject


class ExactAuthorityScopeMatcher(AuthorityScopeMatcher):
    def match(
        self,
        scope: CanonicalJsonObject,
        *,
        action: str,
        resource: str,
        context: CanonicalJsonObject,
    ) -> ScopeMatchResult:
        if action in scope.get("actions", ()) and resource in scope.get("resources", ()):
            return ScopeMatchResult.MATCH
        return ScopeMatchResult.MISMATCH


class ExactContextMatcher(DelegationContextMatcher):
    def match(
        self,
        constraints: CanonicalJsonObject,
        context: CanonicalJsonObject,
    ) -> DelegationContextMatch:
        if all(context.get(key) == value for key, value in constraints.items()):
            return DelegationContextMatch.MATCH
        return DelegationContextMatch.MISMATCH


class DelegationFoundationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.audit = InMemoryAuditLogRepository()
        self.authority_repository = InMemoryAuthorityRepository(
            self.audit, audit_chain_id="governance-audit"
        )
        self.authority_scope_matcher = ExactAuthorityScopeMatcher()
        authority = build_authority_record(
            authority_record_id="authority-1",
            authority_source_id="parent-1",
            subject_id="subject-1",
            authority_type=AuthorityType.PARENT,
            scope={
                "actions": ["delegate", "read", "support"],
                "resources": ["record-1"],
            },
            priority=10,
            issued_at="2026-06-19T12:00:00Z",
            expires_at="2026-07-19T12:00:00Z",
            status=AuthorityStatus.ACTIVE,
        )
        self.authority_repository.create(
            authority,
            actor_id="registry-admin",
            reason="authority_registered",
            occurred_at="2026-06-19T12:01:00Z",
            audit_event_id="audit-authority-create",
        )
        authority_service = AuthorityResolutionService(
            self.authority_repository,
            self.authority_scope_matcher,
            self.audit,
            audit_chain_id="governance-audit",
            clock=lambda: datetime(2026, 6, 19, 12, 2, tzinfo=timezone.utc),
        )
        self.authority_result = authority_service.resolve(
            AuthorityResolutionRequest(
                request_id="authority-request-1",
                subject_id="subject-1",
                requester_id="parent-1",
                action="delegate",
                resource="record-1",
                context={"location": "school"},
                identity_verdict_id="identity-verdict-parent",
                authority_records=(),
                policy_version="policy-v1",
            )
        )
        self.repository = InMemoryDelegationRepository(
            self.authority_repository,
            self.authority_scope_matcher,
            self.audit,
            audit_chain_id="governance-audit",
        )

    def _create_and_activate(
        self,
        *,
        expires_at: str = "2026-07-19T12:00:00Z",
        chain_metadata: CanonicalJsonObject | None = None,
        allowed_actions: tuple[str, ...] = ("read",),
    ):
        grant = build_delegation_grant(
            delegation_id="delegation-1",
            grantor_id="parent-1",
            delegate_id="teacher-1",
            subject_id="subject-1",
            role="teacher",
            allowed_actions=allowed_actions,
            allowed_resources=("record-1",),
            context_constraints={"location": "school"},
            issued_at="2026-06-19T12:03:00Z",
            expires_at=expires_at,
            source_authority_reference="authority-1",
            authority_resolution_id=self.authority_result.authority_resolution_id,
            chain_metadata=chain_metadata,
        )
        self.repository.create(
            grant,
            self.authority_result,
            actor_id="parent-1",
            reason="delegation_created",
            occurred_at="2026-06-19T12:04:00Z",
            audit_event_id="audit-delegation-create",
        )
        return self.repository.update_state(
            "delegation-1",
            DelegationState.ACTIVE,
            actor_id="parent-1",
            reason="delegation_activated",
            occurred_at="2026-06-19T12:05:00Z",
            audit_event_id="audit-delegation-activate",
        )

    def _service(self, hour: int = 12, minute: int = 10) -> DelegationValidationService:
        return DelegationValidationService(
            self.repository,
            self.authority_repository,
            ExactContextMatcher(),
            self.audit,
            audit_chain_id="governance-audit",
            clock=lambda: datetime(2026, 6, 19, hour, minute, tzinfo=timezone.utc),
        )

    def _request(self, **overrides: object) -> DelegationValidationRequest:
        values: dict[str, object] = {
            "validation_id": "delegation-validation-1",
            "delegation_id": "delegation-1",
            "requester_id": "teacher-1",
            "subject_id": "subject-1",
            "action": "read",
            "resource": "record-1",
            "context": {"location": "school"},
            "authority_verdict_id": self.authority_result.authority_resolution_id,
        }
        values.update(overrides)
        return DelegationValidationRequest(**values)  # type: ignore[arg-type]

    def test_valid_delegation(self) -> None:
        self._create_and_activate()

        result = self._service().validate(self._request())

        self.assertEqual(result.outcome, DelegationValidationOutcome.VALID)
        self.assertEqual(result.effective_scope["actions"], ("read",))

    def test_revoked_delegation(self) -> None:
        self._create_and_activate()
        self.repository.revoke(
            "delegation-1",
            actor_id="parent-1",
            reason="delegation_revoked",
            occurred_at="2026-06-19T12:06:00Z",
            audit_event_id="audit-delegation-revoke",
        )

        result = self._service().validate(self._request())

        self.assertEqual(result.outcome, DelegationValidationOutcome.REVOKED)

    def test_expired_delegation(self) -> None:
        self._create_and_activate(expires_at="2026-06-19T12:30:00Z")

        result = self._service(hour=13).validate(self._request())

        self.assertEqual(result.outcome, DelegationValidationOutcome.EXPIRED)

    def test_invalid_grantor_after_authority_revocation(self) -> None:
        self._create_and_activate()
        self.authority_repository.revoke(
            "authority-1",
            actor_id="registry-admin",
            reason="authority_revoked",
            occurred_at="2026-06-19T12:06:00Z",
            audit_event_id="audit-authority-revoke",
        )

        result = self._service().validate(self._request())

        self.assertEqual(result.outcome, DelegationValidationOutcome.INVALID_GRANTOR)

    def test_invalid_scope(self) -> None:
        self._create_and_activate()

        result = self._service().validate(self._request(action="write"))

        self.assertEqual(result.outcome, DelegationValidationOutcome.INVALID_SCOPE)

    def test_invalid_subject(self) -> None:
        self._create_and_activate()

        result = self._service().validate(self._request(subject_id="subject-2"))

        self.assertEqual(result.outcome, DelegationValidationOutcome.INVALID_SUBJECT)

    def test_deterministic_validation_outcomes_and_audit(self) -> None:
        self._create_and_activate()
        service = self._service()
        request = self._request()

        first = service.validate(request)
        audit_count = len(self.audit.chain("governance-audit"))
        second = service.validate(request)

        self.assertEqual(first, second)
        self.assertEqual(len(self.audit.chain("governance-audit")), audit_count)
        history = self.repository.history("delegation-1")
        self.assertEqual(history[1].previous_audit_hash, history[0].audit_event_hash)

    def test_grant_creation_rejects_scope_beyond_authority(self) -> None:
        grant = build_delegation_grant(
            delegation_id="delegation-1",
            grantor_id="parent-1",
            delegate_id="teacher-1",
            subject_id="subject-1",
            role="teacher",
            allowed_actions=("delete",),
            allowed_resources=("record-1",),
            context_constraints={"location": "school"},
            issued_at="2026-06-19T12:03:00Z",
            expires_at="2026-07-19T12:00:00Z",
            source_authority_reference="authority-1",
            authority_resolution_id=self.authority_result.authority_resolution_id,
        )

        with self.assertRaises(DelegationValidationError):
            self.repository.create(
                grant,
                self.authority_result,
                actor_id="parent-1",
                reason="delegation_created",
                occurred_at="2026-06-19T12:04:00Z",
                audit_event_id="audit-delegation-create",
            )

    def test_chain_metadata_is_preserved_but_validation_conflicts(self) -> None:
        stored = self._create_and_activate(
            chain_metadata={"parent_delegation_id": "delegation-parent"}
        )

        result = self._service().validate(self._request())

        self.assertEqual(stored.delegation_grant.chain_metadata["parent_delegation_id"], "delegation-parent")
        self.assertEqual(result.outcome, DelegationValidationOutcome.CONFLICT)
        self.assertEqual(result.reason, "delegation_chain_validation_deferred")


if __name__ == "__main__":
    unittest.main()
