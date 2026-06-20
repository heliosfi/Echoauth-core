"""Sprint 2G Runtime Authorization Gate foundation tests."""

from __future__ import annotations

import unittest
from datetime import datetime, timezone

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth import (
    AuthorizationGateService,
    AuthorizationOutcome,
    AuthorizationRequest,
)
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
    DelegationValidationService,
    InMemoryDelegationRepository,
    build_delegation_grant,
)
from echoauth.identity import (
    CredentialVerification,
    CredentialVerifier,
    IdentityRecord,
    IdentityStatus,
    IdentityVerdictState,
    InMemoryIdentityRepository,
    RegistryIdentityService,
)
from echoauth.models import (
    ActorType,
    AssuranceLevel,
    AuthorityResolutionRequest,
    CanonicalJsonObject,
)
from echoauth.policy import (
    InMemoryPolicyRepository,
    PolicyEffect,
    PolicyEvaluationService,
    PolicyScopeMatch,
    PolicyScopeMatcher,
    PolicyStatus,
    PolicyType,
    build_policy_rule,
)


class Verifier(CredentialVerifier):
    def verify(self, record, credential_set, context, session_id):
        return CredentialVerification(
            state=IdentityVerdictState.VERIFIED,
            assurance_level=AssuranceLevel.STANDARD,
            reason="credentials_verified",
            verifier_component="test_verifier",
            evidence={"credential_class": "test"},
        )


class AuthorityMatcher(AuthorityScopeMatcher):
    def match(self, scope, *, action, resource, context):
        if action in scope.get("actions", ()) and resource in scope.get("resources", ()):
            return ScopeMatchResult.MATCH
        return ScopeMatchResult.MISMATCH


class DelegationMatcher(DelegationContextMatcher):
    def match(self, constraints, context):
        if all(context.get(key) == value for key, value in constraints.items()):
            return DelegationContextMatch.MATCH
        return DelegationContextMatch.MISMATCH


class PolicyMatcher(PolicyScopeMatcher):
    def match(self, scope, context):
        if all(context.get(key) == value for key, value in scope.items()):
            return PolicyScopeMatch.MATCH
        return PolicyScopeMatch.MISMATCH


class AuthorizationGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime(2026, 6, 19, 13, 0, tzinfo=timezone.utc)
        self.audit = InMemoryAuditLogRepository()
        self.identity_repository = InMemoryIdentityRepository()
        for identity_id, actor_id in (
            ("identity-parent", "parent-1"),
            ("identity-delegate", "teacher-1"),
        ):
            self.identity_repository.register(
                IdentityRecord(
                    identity_record_id=identity_id,
                    actor_id=actor_id,
                    actor_type=ActorType.HUMAN,
                    status=IdentityStatus.ACTIVE,
                    credential_refs=(f"credential-{actor_id}",),
                    created_at="2026-06-19T12:00:00Z",
                    updated_at="2026-06-19T12:00:00Z",
                )
            )
        self.identity_service = RegistryIdentityService(
            self.identity_repository, Verifier(), clock=lambda: self.now
        )
        self.authority_repository = InMemoryAuthorityRepository(
            self.audit, audit_chain_id="gate-audit"
        )
        self.authority_repository.create(
            build_authority_record(
                authority_record_id="authority-1",
                authority_source_id="parent-1",
                subject_id="subject-1",
                authority_type=AuthorityType.PARENT,
                scope={
                    "actions": ["delegate", "read", "write"],
                    "resources": ["record-1"],
                },
                priority=10,
                issued_at="2026-06-19T12:00:00Z",
                expires_at="2026-07-19T12:00:00Z",
                status=AuthorityStatus.ACTIVE,
            ),
            actor_id="registry-admin",
            reason="authority_registered",
            occurred_at="2026-06-19T12:01:00Z",
            audit_event_id="audit-authority-create",
        )
        self.authority_matcher = AuthorityMatcher()
        self.authority_service = AuthorityResolutionService(
            self.authority_repository,
            self.authority_matcher,
            self.audit,
            audit_chain_id="gate-audit",
            clock=lambda: self.now,
        )
        self.delegation_repository = InMemoryDelegationRepository(
            self.authority_repository,
            self.authority_matcher,
            self.audit,
            audit_chain_id="gate-audit",
        )
        self.delegation_service = DelegationValidationService(
            self.delegation_repository,
            self.authority_repository,
            DelegationMatcher(),
            self.audit,
            audit_chain_id="gate-audit",
            clock=lambda: self.now,
        )
        self.policy_repository = InMemoryPolicyRepository(
            self.audit, audit_chain_id="gate-audit"
        )
        self.policy_service = PolicyEvaluationService(
            self.policy_repository,
            PolicyMatcher(),
            self.audit,
            audit_chain_id="gate-audit",
            clock=lambda: self.now,
        )
        self.gate = AuthorizationGateService(
            self.identity_service,
            self.authority_service,
            self.delegation_repository,
            self.delegation_service,
            self.policy_service,
            self.audit,
            audit_chain_id="gate-audit",
            clock=lambda: self.now,
        )

    def _register_policy(
        self,
        *,
        effect=PolicyEffect.AUTHORIZE,
        rule_id="rule-1",
        policy_id="policy-1",
        priority=10,
        action="read",
        expires_at="2026-07-19T12:00:00Z",
        audit_id="audit-policy-1",
    ):
        self.policy_repository.register(
            build_policy_rule(
                rule_id=rule_id,
                policy_id=policy_id,
                policy_version="policy-v1",
                policy_type=PolicyType.AUTHORITY,
                effect=effect,
                actions=(action,),
                resources=("record-1",),
                scope={"location": "school"},
                priority=priority,
                reason="policy_authorized" if effect is PolicyEffect.AUTHORIZE else "policy_denied",
                created_by="policy-admin",
                effective_at="2026-06-19T12:00:00Z",
                expires_at=expires_at,
                status=PolicyStatus.ACTIVE,
            ),
            actor_id="policy-admin",
            reason="policy_registered",
            occurred_at="2026-06-19T12:02:00Z",
            audit_event_id=audit_id,
        )

    def _request(self, **overrides: object) -> AuthorizationRequest:
        values: dict[str, object] = {
            "request_id": "request-1",
            "requester_id": "parent-1",
            "requester_type": ActorType.HUMAN,
            "subject_id": "subject-1",
            "action": "read",
            "resource": "record-1",
            "credential_set": {"credential": "proof"},
            "required_assurance": AssuranceLevel.STANDARD,
            "payload": {"operation": "read"},
            "context": {"location": "school"},
            "policy_version": "policy-v1",
            "correlation_id": "correlation-1",
            "idempotency_key": "idempotency-1",
        }
        values.update(overrides)
        return AuthorizationRequest(**values)  # type: ignore[arg-type]

    def _create_delegation(self) -> None:
        authority = self.authority_service.resolve(
            AuthorityResolutionRequest(
                request_id="grant-request",
                subject_id="subject-1",
                requester_id="parent-1",
                action="delegate",
                resource="record-1",
                context={"location": "school"},
                identity_verdict_id="identity-parent",
                authority_records=(),
                policy_version="policy-v1",
            )
        )
        grant = build_delegation_grant(
            delegation_id="delegation-1",
            grantor_id="parent-1",
            delegate_id="teacher-1",
            subject_id="subject-1",
            role="teacher",
            allowed_actions=("read",),
            allowed_resources=("record-1",),
            context_constraints={"location": "school"},
            issued_at="2026-06-19T12:03:00Z",
            expires_at="2026-07-19T12:00:00Z",
            source_authority_reference="authority-1",
            authority_resolution_id=authority.authority_resolution_id,
        )
        self.delegation_repository.create(
            grant,
            authority,
            actor_id="parent-1",
            reason="delegation_created",
            occurred_at="2026-06-19T12:04:00Z",
            audit_event_id="audit-delegation-create",
        )
        self.delegation_repository.update_state(
            "delegation-1",
            DelegationState.ACTIVE,
            actor_id="parent-1",
            reason="delegation_activated",
            occurred_at="2026-06-19T12:05:00Z",
            audit_event_id="audit-delegation-active",
        )

    def test_successful_authorization(self) -> None:
        self._register_policy()
        decision = self.gate.authorize(self._request())
        self.assertEqual(decision.outcome, AuthorizationOutcome.AUTHORIZED)
        self.assertEqual(
            decision.evidence["evaluation_order"],
            ("identity", "authority", "delegation", "policy"),
        )

    def test_successful_delegated_authorization_runs_all_dependencies(self) -> None:
        self._create_delegation()
        self._register_policy()

        decision = self.gate.authorize(
            self._request(
                requester_id="teacher-1",
                delegation_id="delegation-1",
            )
        )

        self.assertEqual(decision.outcome, AuthorizationOutcome.AUTHORIZED)
        self.assertIsNotNone(decision.identity_verdict_id)
        self.assertIsNotNone(decision.authority_resolution_id)
        self.assertIsNotNone(decision.delegation_validation_id)
        self.assertIsNotNone(decision.policy_decision_id)

    def test_identity_failure(self) -> None:
        self._register_policy()
        self.identity_repository.transition(
            "identity-parent",
            IdentityStatus.SUSPENDED,
            updated_at="2026-06-19T12:30:00Z",
        )
        decision = self.gate.authorize(self._request())
        self.assertEqual(decision.outcome, AuthorizationOutcome.INVALID_IDENTITY)

    def test_authority_failure(self) -> None:
        self._register_policy(action="delete")
        decision = self.gate.authorize(self._request(action="delete"))
        self.assertEqual(decision.outcome, AuthorizationOutcome.INVALID_AUTHORITY)

    def test_delegation_failure(self) -> None:
        self._create_delegation()
        self._register_policy(action="write")
        decision = self.gate.authorize(
            self._request(
                requester_id="teacher-1",
                action="write",
                delegation_id="delegation-1",
            )
        )
        self.assertEqual(decision.outcome, AuthorizationOutcome.INVALID_DELEGATION)

    def test_policy_denial(self) -> None:
        self._register_policy(effect=PolicyEffect.DENY)
        decision = self.gate.authorize(self._request())
        self.assertEqual(decision.outcome, AuthorizationOutcome.DENIED)

    def test_conflict_outcome(self) -> None:
        self._register_policy()
        self._register_policy(
            effect=PolicyEffect.DENY,
            rule_id="rule-2",
            policy_id="policy-2",
            audit_id="audit-policy-2",
        )
        decision = self.gate.authorize(self._request())
        self.assertEqual(decision.outcome, AuthorizationOutcome.CONFLICT)

    def test_revoked_outcome(self) -> None:
        self._register_policy()
        self.authority_repository.revoke(
            "authority-1",
            actor_id="registry-admin",
            reason="authority_revoked",
            occurred_at="2026-06-19T12:30:00Z",
            audit_event_id="audit-authority-revoked",
        )
        decision = self.gate.authorize(self._request())
        self.assertEqual(decision.outcome, AuthorizationOutcome.REVOKED)

    def test_expired_outcome(self) -> None:
        self._register_policy(expires_at="2026-06-19T12:30:00Z")
        decision = self.gate.authorize(self._request())
        self.assertEqual(decision.outcome, AuthorizationOutcome.EXPIRED)

    def test_deterministic_decision_generation(self) -> None:
        self._register_policy()
        request = self._request()
        first = self.gate.authorize(request)
        audit_count = len(self.audit.chain("gate-audit"))
        second = self.gate.authorize(request)
        self.assertEqual(first, second)
        self.assertEqual(len(self.audit.chain("gate-audit")), audit_count)


if __name__ == "__main__":
    unittest.main()
