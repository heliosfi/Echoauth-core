"""Focused SAL-19 authorization-to-execution binding adversarial tests."""

from __future__ import annotations

import unittest
from datetime import datetime, timezone

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth import (
    AuthorizationGateService,
    AuthorizationRequest,
    AuthorityResolutionService,
    AuthorityScopeMatcher,
    AuthorityStatus,
    AuthorityType,
    DelegationContextMatch,
    DelegationContextMatcher,
    DelegationValidationService,
    InMemoryAuthorityRepository,
    InMemoryDelegationRepository,
    ScopeMatchResult,
    build_authority_record,
)
from echoauth.execution import (
    AuthorizationExecutionBinder,
    AuthorizationExecutionBindingError,
    ExecutionConstraint,
    ExecutionControl,
    ExecutionOutcome,
    ExecutionRequest,
    authorization_execution_evidence_mapping,
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
from echoauth.models import ActorType, AssuranceLevel
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
from echoauth.runtime import (
    RuntimeState,
    RuntimeStateMachine,
    RuntimeTransition,
    RuntimeTransitionRequest,
)


class Verifier(CredentialVerifier):
    def verify(self, record, credential_set, context, session_id):
        return CredentialVerification(
            state=IdentityVerdictState.VERIFIED,
            assurance_level=AssuranceLevel.STANDARD,
            reason="credentials_verified",
            verifier_component="sal19_verifier",
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


class AuthorizationExecutionBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime(2026, 6, 19, 13, 0, tzinfo=timezone.utc)
        self.clock = lambda: self.now
        self.audit = InMemoryAuditLogRepository()

        self.identity_repository = InMemoryIdentityRepository()
        self.identity_repository.register(
            IdentityRecord(
                identity_record_id="identity-parent",
                actor_id="parent-1",
                actor_type=ActorType.HUMAN,
                status=IdentityStatus.ACTIVE,
                credential_refs=("credential-parent-1",),
                created_at="2026-06-19T12:00:00Z",
                updated_at="2026-06-19T12:00:00Z",
            )
        )
        identity_service = RegistryIdentityService(
            self.identity_repository,
            Verifier(),
            clock=self.clock,
        )

        self.authority_repository = InMemoryAuthorityRepository(
            self.audit, audit_chain_id="sal19-audit"
        )
        self.authority_repository.create(
            build_authority_record(
                authority_record_id="authority-1",
                authority_source_id="parent-1",
                subject_id="subject-1",
                authority_type=AuthorityType.PARENT,
                scope={"actions": ["read"], "resources": ["record-1"]},
                priority=10,
                issued_at="2026-06-19T12:00:00Z",
                expires_at="2026-06-19T14:00:00Z",
                status=AuthorityStatus.ACTIVE,
            ),
            actor_id="registry-admin",
            reason="authority_registered",
            occurred_at="2026-06-19T12:01:00Z",
            audit_event_id="audit-sal19-authority-create",
        )
        authority_matcher = AuthorityMatcher()
        authority_service = AuthorityResolutionService(
            self.authority_repository,
            authority_matcher,
            self.audit,
            audit_chain_id="sal19-audit",
            clock=self.clock,
        )

        delegation_repository = InMemoryDelegationRepository(
            self.authority_repository,
            authority_matcher,
            self.audit,
            audit_chain_id="sal19-audit",
        )
        delegation_service = DelegationValidationService(
            delegation_repository,
            self.authority_repository,
            DelegationMatcher(),
            self.audit,
            audit_chain_id="sal19-audit",
            clock=self.clock,
        )

        self.policy_repository = InMemoryPolicyRepository(
            self.audit, audit_chain_id="sal19-audit"
        )
        policy_service = PolicyEvaluationService(
            self.policy_repository,
            PolicyMatcher(),
            self.audit,
            audit_chain_id="sal19-audit",
            clock=self.clock,
        )

        gate = AuthorizationGateService(
            identity_service,
            authority_service,
            delegation_repository,
            delegation_service,
            policy_service,
            self.audit,
            audit_chain_id="sal19-audit",
            clock=self.clock,
        )
        self.binder = AuthorizationExecutionBinder(
            gate,
            self.audit,
            audit_chain_id="sal19-audit",
            clock=self.clock,
        )

        self.state_machine = RuntimeStateMachine(
            self.audit,
            audit_chain_id="sal19-audit",
            clock=self.clock,
        )
        self.constraint = ExecutionConstraint(
            constraint_id="sal19-execution-constraint",
            required_state=RuntimeState.READY,
            expires_at="2026-06-19T15:00:00Z",
        )
        self.control = ExecutionControl(
            self.audit,
            audit_chain_id="sal19-audit",
            constraints=(self.constraint,),
            authorization_binder=self.binder,
            clock=self.clock,
        )

    def _register_policy(self, *, expires_at="2026-06-19T14:00:00Z") -> None:
        self.policy_repository.register(
            build_policy_rule(
                rule_id="rule-1",
                policy_id="policy-1",
                policy_version="policy-v1",
                policy_type=PolicyType.AUTHORITY,
                effect=PolicyEffect.AUTHORIZE,
                actions=("read",),
                resources=("record-1",),
                scope={"location": "school"},
                priority=10,
                reason="policy_authorized",
                created_by="policy-admin",
                effective_at="2026-06-19T12:00:00Z",
                expires_at=expires_at,
                status=PolicyStatus.ACTIVE,
            ),
            actor_id="policy-admin",
            reason="policy_registered",
            occurred_at="2026-06-19T12:02:00Z",
            audit_event_id="audit-sal19-policy",
        )

    def _authorization_request(self, **overrides) -> AuthorizationRequest:
        values = {
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
        return AuthorizationRequest(**values)

    def _runtime_decision(self):
        return self.state_machine.validate(
            RuntimeTransitionRequest(
                transition_request_id="sal19-runtime-transition",
                request_id="request-1",
                current_state=RuntimeState.AUTHORIZED,
                transition=RuntimeTransition.MARK_READY,
                requested_state=RuntimeState.READY,
                actor_id="sal19-test",
                reason="sal19_execution_readiness",
                evidence={"source": "sal19"},
                occurred_at="2026-06-19T12:59:00Z",
            )
        )

    def _execution_request(self, runtime, *, authority_evidence=None, action="read"):
        return ExecutionRequest(
            execution_request_id="execution-request-1",
            request_id="request-1",
            runtime_transition_decision_id=runtime.transition_decision_id,
            actor_id="parent-1",
            action=action,
            resource="record-1",
            authority_evidence=authority_evidence or {},
            refusal_evidence={},
            escalation_evidence={},
            review_evidence={},
            override_evidence={},
            evidence={"payload_hash": "sal19-request-evidence"},
            audit_references=(runtime.audit_event_id,),
            requested_at="2026-06-19T13:00:00Z",
            constraint=self.constraint,
        )

    def test_fresh_authorization_binding_allows_eligibility_assessment(self) -> None:
        self._register_policy()
        runtime = self._runtime_decision()
        decision = self.control.validate_authorized(
            self._execution_request(runtime),
            runtime,
            self._authorization_request(),
        )
        self.assertEqual(decision.outcome, ExecutionOutcome.ELIGIBLE)
        self.assertTrue(decision.eligible)
        self.assertIsNotNone(decision.evidence.authority_evidence_hash)

    def test_loose_placeholder_authority_evidence_cannot_be_eligible(self) -> None:
        self._register_policy()
        runtime = self._runtime_decision()
        request = self._execution_request(
            runtime,
            authority_evidence={
                "authority_reference": "fabricated-authority",
                "authority_evidence_hash": "fabricated-hash",
            },
        )
        decision = self.control.validate(request, runtime)
        self.assertEqual(decision.outcome, ExecutionOutcome.MISSING_AUTHORITY)
        self.assertFalse(decision.eligible)
        self.assertEqual(decision.reason, "authorization_binding_required")

    def test_old_binding_cannot_bypass_fresh_authorization_after_revocation(self) -> None:
        self._register_policy()
        runtime = self._runtime_decision()
        authorization_request = self._authorization_request()
        old_binding = self.binder.bind(
            authorization_request,
            execution_request_id="execution-request-1",
            actor_id="parent-1",
            action="read",
            resource="record-1",
        )
        self.authority_repository.revoke(
            "authority-1",
            actor_id="registry-admin",
            reason="authority_revoked",
            occurred_at="2026-06-19T13:05:00Z",
            audit_event_id="audit-sal19-authority-revoked",
        )

        replay = self.control.validate(
            self._execution_request(
                runtime,
                authority_evidence=authorization_execution_evidence_mapping(old_binding),
            ),
            runtime,
        )
        self.assertEqual(replay.outcome, ExecutionOutcome.MISSING_AUTHORITY)
        self.assertFalse(replay.eligible)

        with self.assertRaisesRegex(
            AuthorizationExecutionBindingError,
            "authorization_not_authorized:authority_revoked",
        ):
            self.control.validate_authorized(
                self._execution_request(runtime),
                runtime,
                authorization_request,
            )

    def test_policy_expiry_requires_fresh_authorization_and_fails_closed(self) -> None:
        self._register_policy(expires_at="2026-06-19T13:10:00Z")
        runtime = self._runtime_decision()
        authorization_request = self._authorization_request()
        first = self.control.validate_authorized(
            self._execution_request(runtime), runtime, authorization_request
        )
        self.assertEqual(first.outcome, ExecutionOutcome.ELIGIBLE)

        self.now = datetime(2026, 6, 19, 13, 11, tzinfo=timezone.utc)
        with self.assertRaisesRegex(
            AuthorizationExecutionBindingError,
            "authorization_not_authorized:policy_expired",
        ):
            self.control.validate_authorized(
                self._execution_request(runtime), runtime, authorization_request
            )

    def test_identity_suspension_requires_fresh_authorization_and_fails_closed(self) -> None:
        self._register_policy()
        runtime = self._runtime_decision()
        authorization_request = self._authorization_request()
        first = self.control.validate_authorized(
            self._execution_request(runtime), runtime, authorization_request
        )
        self.assertEqual(first.outcome, ExecutionOutcome.ELIGIBLE)

        self.identity_repository.transition(
            "identity-parent",
            IdentityStatus.SUSPENDED,
            updated_at="2026-06-19T13:05:00Z",
        )
        with self.assertRaisesRegex(
            AuthorizationExecutionBindingError,
            "authorization_not_authorized:identity_not_verified",
        ):
            self.control.validate_authorized(
                self._execution_request(runtime), runtime, authorization_request
            )

    def test_action_mismatch_is_rejected_before_eligibility(self) -> None:
        self._register_policy()
        runtime = self._runtime_decision()
        with self.assertRaisesRegex(
            AuthorizationExecutionBindingError,
            "authorization_action_mismatch",
        ):
            self.control.validate_authorized(
                self._execution_request(runtime, action="write"),
                runtime,
                self._authorization_request(),
            )


if __name__ == "__main__":
    unittest.main()
