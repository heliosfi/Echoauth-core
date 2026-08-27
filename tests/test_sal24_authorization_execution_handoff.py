"""SAL-24 adversarial tests for the validation-only authorization/execution seam."""

from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import datetime, timezone

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth import AuthorizationGateService, AuthorizationOutcome, AuthorizationRequest
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
from echoauth.canonical import canonical_sha256
from echoauth.execution import (
    AuthorizationExecutionHandoffValidator,
    ExecutionConstraint,
    ExecutionControl,
    ExecutionOutcome,
    ExecutionRequest,
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
from echoauth.models import ActorType, AssuranceLevel, AuthorityResolutionRequest
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
            verifier_component="sal24_test_verifier",
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


class Sal24AuthorizationExecutionHandoffTests(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime(2026, 6, 19, 13, 0, tzinfo=timezone.utc)
        clock = lambda: self.now
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
            self.identity_repository, Verifier(), clock=clock
        )

        self.authority_repository = InMemoryAuthorityRepository(
            self.audit, audit_chain_id="sal24-audit"
        )
        self.authority_repository.create(
            build_authority_record(
                authority_record_id="authority-1",
                authority_source_id="parent-1",
                subject_id="subject-1",
                authority_type=AuthorityType.PARENT,
                scope={
                    "actions": ["delegate", "read"],
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
            audit_chain_id="sal24-audit",
            clock=clock,
        )

        self.delegation_repository = InMemoryDelegationRepository(
            self.authority_repository,
            self.authority_matcher,
            self.audit,
            audit_chain_id="sal24-audit",
        )
        self.delegation_service = DelegationValidationService(
            self.delegation_repository,
            self.authority_repository,
            DelegationMatcher(),
            self.audit,
            audit_chain_id="sal24-audit",
            clock=clock,
        )

        self.policy_repository = InMemoryPolicyRepository(
            self.audit, audit_chain_id="sal24-audit"
        )
        self.policy_service = PolicyEvaluationService(
            self.policy_repository,
            PolicyMatcher(),
            self.audit,
            audit_chain_id="sal24-audit",
            clock=clock,
        )
        self._register_policy()

        self.gate = AuthorizationGateService(
            self.identity_service,
            self.authority_service,
            self.delegation_repository,
            self.delegation_service,
            self.policy_service,
            self.audit,
            audit_chain_id="sal24-audit",
            clock=clock,
        )
        self.handoff_validator = AuthorizationExecutionHandoffValidator(
            self.gate,
            self.audit,
            audit_chain_id="sal24-audit",
            clock=clock,
        )

        self.state_machine = RuntimeStateMachine(
            self.audit, audit_chain_id="sal24-audit", clock=clock
        )
        self.constraint = ExecutionConstraint(
            constraint_id="sal24-direct",
            required_state=RuntimeState.READY,
            expires_at="2026-07-19T13:00:00Z",
        )
        self.execution_control = ExecutionControl(
            self.audit,
            audit_chain_id="sal24-audit",
            constraints=(self.constraint,),
            clock=clock,
        )

    def _register_policy(self, *, expires_at="2026-07-19T12:00:00Z") -> None:
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
            audit_event_id="audit-policy-1",
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
            "delegation_id": None,
        }
        values.update(overrides)
        return AuthorizationRequest(**values)

    def _runtime_decision(self, *, ready=True):
        if ready:
            current, transition, target = (
                RuntimeState.AUTHORIZED,
                RuntimeTransition.MARK_READY,
                RuntimeState.READY,
            )
        else:
            current, transition, target = (
                RuntimeState.REQUESTED,
                RuntimeTransition.AUTHORIZE,
                RuntimeState.AUTHORIZED,
            )
        return self.state_machine.validate(
            RuntimeTransitionRequest(
                transition_request_id="sal24-runtime-transition",
                request_id="request-1",
                current_state=current,
                transition=transition,
                requested_state=target,
                actor_id="sal24-runtime-test",
                reason="sal24_runtime_validation",
                evidence={"source": "sal24"},
                occurred_at="2026-06-19T12:59:00Z",
            )
        )

    def _execution_request(self, auth_request, runtime, **overrides):
        values = {
            "execution_request_id": "sal24-execution-request",
            "request_id": auth_request.request_id,
            "runtime_transition_decision_id": runtime.transition_decision_id,
            "actor_id": auth_request.requester_id,
            "subject_id": auth_request.subject_id,
            "action": auth_request.action,
            "resource": auth_request.resource,
            "payload_hash": canonical_sha256(auth_request.payload),
            "context_hash": canonical_sha256(auth_request.context),
            "policy_version": auth_request.policy_version,
            "delegation_id": auth_request.delegation_id,
            "authority_evidence": {
                "authority_reference": "fabricated-authority",
                "authority_evidence_hash": "fabricated-hash",
            },
            "refusal_evidence": {},
            "escalation_evidence": {},
            "review_evidence": {},
            "override_evidence": {},
            "evidence": {"payload_hash": canonical_sha256(auth_request.payload)},
            "audit_references": (runtime.audit_event_id,),
            "requested_at": "2026-06-19T13:00:00Z",
            "constraint": self.constraint,
        }
        values.update(overrides)
        return ExecutionRequest(**values)

    @staticmethod
    def _authority_evidence(handoff):
        return {
            "authorization_decision_id": handoff.fresh_authorization_decision_id,
            "authorization_evidence_hash": handoff.fresh_authorization_evidence_hash,
            "authorization_audit_event_id": handoff.fresh_authorization_audit_event_id,
            "authority_resolution_id": handoff.authority_resolution_id,
            "handoff_validation_id": handoff.handoff_validation_id,
            "handoff_evidence_hash": handoff.evidence_hash,
        }

    def _accepted_handoff(self, auth_request=None, runtime=None):
        auth_request = auth_request or self._authorization_request()
        runtime = runtime or self._runtime_decision()
        prior = self.gate.authorize(auth_request)
        self.assertEqual(prior.outcome, AuthorizationOutcome.AUTHORIZED)
        request = self._execution_request(auth_request, runtime)
        handoff = self.handoff_validator.validate(request, auth_request, prior)
        self.assertTrue(handoff.accepted)
        bound = replace(
            request,
            authority_evidence=self._authority_evidence(handoff),
            audit_references=(
                runtime.audit_event_id,
                handoff.fresh_authorization_audit_event_id,
                handoff.audit_event_id,
            ),
        )
        return prior, bound, handoff, runtime

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

    def test_fresh_authorization_and_ready_state_are_both_required_for_eligible(self):
        _, request, handoff, runtime = self._accepted_handoff()
        decision = self.execution_control.validate(request, runtime, handoff)
        self.assertEqual(decision.outcome, ExecutionOutcome.ELIGIBLE)
        self.assertTrue(decision.eligible)
        self.assertEqual(
            decision.evidence.authorization_decision_id,
            handoff.fresh_authorization_decision_id,
        )

    def test_placeholder_authority_evidence_cannot_make_ready_state_eligible(self):
        auth_request = self._authorization_request()
        runtime = self._runtime_decision()
        prior = self.gate.authorize(auth_request)
        request = self._execution_request(auth_request, runtime)
        handoff = self.handoff_validator.validate(request, auth_request, prior)
        decision = self.execution_control.validate(request, runtime, handoff)
        self.assertEqual(decision.outcome, ExecutionOutcome.MISSING_AUTHORITY)
        self.assertEqual(decision.reason, "authorization_evidence_binding_mismatch")

    def test_non_authorized_prior_decision_fails_closed(self):
        auth_request = self._authorization_request()
        runtime = self._runtime_decision()
        self.authority_repository.revoke(
            "authority-1",
            actor_id="registry-admin",
            reason="authority_revoked",
            occurred_at="2026-06-19T12:30:00Z",
            audit_event_id="audit-authority-revoked",
        )
        prior = self.gate.authorize(auth_request)
        self.assertNotEqual(prior.outcome, AuthorizationOutcome.AUTHORIZED)
        handoff = self.handoff_validator.validate(
            self._execution_request(auth_request, runtime), auth_request, prior
        )
        self.assertFalse(handoff.accepted)
        self.assertEqual(handoff.reason, "prior_authorization_not_authorized")

    def test_stale_prior_authorization_after_authority_revocation_fails_closed(self):
        auth_request = self._authorization_request()
        runtime = self._runtime_decision()
        prior = self.gate.authorize(auth_request)
        self.authority_repository.revoke(
            "authority-1",
            actor_id="registry-admin",
            reason="authority_revoked",
            occurred_at="2026-06-19T12:30:00Z",
            audit_event_id="audit-authority-revoked",
        )
        handoff = self.handoff_validator.validate(
            self._execution_request(auth_request, runtime), auth_request, prior
        )
        self.assertFalse(handoff.accepted)
        self.assertEqual(handoff.reason, "fresh_authorization_not_authorized")

    def test_stale_prior_authorization_after_authority_expiry_fails_closed(self):
        auth_request = self._authorization_request()
        runtime = self._runtime_decision()
        prior = self.gate.authorize(auth_request)
        self.now = datetime(2026, 7, 19, 12, 0, tzinfo=timezone.utc)
        handoff = self.handoff_validator.validate(
            self._execution_request(auth_request, runtime), auth_request, prior
        )
        self.assertFalse(handoff.accepted)
        self.assertEqual(handoff.reason, "fresh_authorization_not_authorized")

    def test_stale_prior_authorization_after_policy_expiry_fails_closed(self):
        # A dedicated short-lived policy is used while authority remains current.
        self.policy_repository = InMemoryPolicyRepository(
            self.audit, audit_chain_id="sal24-policy-expiry"
        )
        self.policy_service = PolicyEvaluationService(
            self.policy_repository,
            PolicyMatcher(),
            self.audit,
            audit_chain_id="sal24-policy-expiry",
            clock=lambda: self.now,
        )
        self.policy_repository.register(
            build_policy_rule(
                rule_id="short-rule",
                policy_id="short-policy",
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
                expires_at="2026-06-19T13:30:00Z",
                status=PolicyStatus.ACTIVE,
            ),
            actor_id="policy-admin",
            reason="policy_registered",
            occurred_at="2026-06-19T12:02:00Z",
            audit_event_id="audit-short-policy",
        )
        self.gate = AuthorizationGateService(
            self.identity_service,
            self.authority_service,
            self.delegation_repository,
            self.delegation_service,
            self.policy_service,
            self.audit,
            audit_chain_id="sal24-policy-expiry",
            clock=lambda: self.now,
        )
        self.handoff_validator = AuthorizationExecutionHandoffValidator(
            self.gate,
            self.audit,
            audit_chain_id="sal24-policy-expiry",
            clock=lambda: self.now,
        )
        auth_request = self._authorization_request()
        runtime = self._runtime_decision()
        prior = self.gate.authorize(auth_request)
        self.assertEqual(prior.outcome, AuthorizationOutcome.AUTHORIZED)
        self.now = datetime(2026, 6, 19, 13, 30, tzinfo=timezone.utc)
        handoff = self.handoff_validator.validate(
            self._execution_request(auth_request, runtime), auth_request, prior
        )
        self.assertFalse(handoff.accepted)
        self.assertEqual(handoff.reason, "fresh_authorization_not_authorized")

    def test_stale_prior_authorization_after_identity_suspension_fails_closed(self):
        auth_request = self._authorization_request()
        runtime = self._runtime_decision()
        prior = self.gate.authorize(auth_request)
        self.identity_repository.transition(
            "identity-parent",
            IdentityStatus.SUSPENDED,
            updated_at="2026-06-19T13:01:00Z",
        )
        handoff = self.handoff_validator.validate(
            self._execution_request(auth_request, runtime), auth_request, prior
        )
        self.assertFalse(handoff.accepted)
        self.assertEqual(handoff.reason, "fresh_authorization_not_authorized")

    def test_stale_prior_delegated_authorization_after_delegation_revocation_fails_closed(self):
        self._create_delegation()
        auth_request = self._authorization_request(
            requester_id="teacher-1",
            delegation_id="delegation-1",
        )
        runtime = self._runtime_decision()
        prior = self.gate.authorize(auth_request)
        self.assertEqual(prior.outcome, AuthorizationOutcome.AUTHORIZED)
        self.delegation_repository.update_state(
            "delegation-1",
            DelegationState.REVOKED,
            actor_id="parent-1",
            reason="delegation_revoked",
            occurred_at="2026-06-19T13:01:00Z",
            audit_event_id="audit-delegation-revoked",
        )
        handoff = self.handoff_validator.validate(
            self._execution_request(auth_request, runtime), auth_request, prior
        )
        self.assertFalse(handoff.accepted)
        self.assertEqual(handoff.reason, "fresh_authorization_not_authorized")

    def test_request_id_action_and_resource_mismatches_fail_closed(self):
        auth_request = self._authorization_request()
        runtime = self._runtime_decision()
        prior = self.gate.authorize(auth_request)
        base = self._execution_request(auth_request, runtime)
        cases = (
            (replace(base, request_id="other-request"), "request_id_mismatch"),
            (replace(base, action="write"), "action_mismatch"),
            (replace(base, resource="record-2"), "resource_mismatch"),
        )
        for request, expected in cases:
            with self.subTest(expected=expected):
                handoff = self.handoff_validator.validate(request, auth_request, prior)
                self.assertFalse(handoff.accepted)
                self.assertEqual(handoff.reason, expected)

    def test_payload_context_policy_and_delegation_mismatches_fail_closed(self):
        auth_request = self._authorization_request()
        runtime = self._runtime_decision()
        prior = self.gate.authorize(auth_request)
        base = self._execution_request(auth_request, runtime)
        cases = (
            (replace(base, payload_hash="wrong"), "payload_mismatch"),
            (replace(base, context_hash="wrong"), "context_mismatch"),
            (replace(base, policy_version="policy-v2"), "policy_mismatch"),
            (replace(base, delegation_id="delegation-x"), "delegation_mismatch"),
        )
        for request, expected in cases:
            with self.subTest(expected=expected):
                handoff = self.handoff_validator.validate(request, auth_request, prior)
                self.assertFalse(handoff.accepted)
                self.assertEqual(handoff.reason, expected)

    def test_authorization_audit_lineage_mismatch_fails_closed(self):
        auth_request = self._authorization_request()
        runtime = self._runtime_decision()
        prior = self.gate.authorize(auth_request)
        tampered = replace(prior, audit_event_id="audit-missing")
        handoff = self.handoff_validator.validate(
            self._execution_request(auth_request, runtime), auth_request, tampered
        )
        self.assertFalse(handoff.accepted)
        self.assertEqual(handoff.reason, "prior_authorization_audit_mismatch")

    def test_valid_permission_does_not_replace_ready_state_requirement(self):
        auth_request = self._authorization_request()
        runtime = self._runtime_decision(ready=False)
        prior = self.gate.authorize(auth_request)
        request = self._execution_request(auth_request, runtime)
        handoff = self.handoff_validator.validate(request, auth_request, prior)
        self.assertTrue(handoff.accepted)
        bound = replace(
            request,
            authority_evidence=self._authority_evidence(handoff),
            audit_references=(
                runtime.audit_event_id,
                handoff.fresh_authorization_audit_event_id,
                handoff.audit_event_id,
            ),
        )
        decision = self.execution_control.validate(bound, runtime, handoff)
        self.assertEqual(decision.outcome, ExecutionOutcome.INVALID_STATE)
        self.assertFalse(decision.eligible)

    def test_ready_state_without_permission_handoff_fails_closed(self):
        auth_request = self._authorization_request()
        runtime = self._runtime_decision()
        request = self._execution_request(auth_request, runtime)
        decision = self.execution_control.validate(request, runtime)
        self.assertEqual(decision.outcome, ExecutionOutcome.MISSING_AUTHORITY)
        self.assertEqual(decision.reason, "authorization_handoff_missing")

    def test_legacy_authority_verdict_id_is_not_authorization_decision_mapping(self):
        _, request, handoff, runtime = self._accepted_handoff()
        legacy = replace(
            request,
            authority_evidence={
                "authority_verdict_id": handoff.authority_resolution_id,
                "authority_evidence_hash": handoff.fresh_authorization_evidence_hash,
            },
        )
        decision = self.execution_control.validate(legacy, runtime, handoff)
        self.assertEqual(decision.outcome, ExecutionOutcome.MISSING_AUTHORITY)
        self.assertEqual(decision.reason, "authorization_evidence_binding_mismatch")


if __name__ == "__main__":
    unittest.main()
