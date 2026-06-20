"""Sprint 2F canonical Policy Evaluation foundation tests."""

from __future__ import annotations

import unittest
from datetime import datetime, timezone

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth.authority import (
    AuthorityResolutionOutcome,
    AuthorityResolutionResult,
    AuthorityType,
)
from echoauth.auth.permissions import (
    DelegationValidationOutcome,
    DelegationValidationResult,
)
from echoauth.policy import (
    InMemoryPolicyRepository,
    PolicyEffect,
    PolicyEvaluationOutcome,
    PolicyEvaluationRequest,
    PolicyEvaluationService,
    PolicyScopeMatch,
    PolicyScopeMatcher,
    PolicyStatus,
    PolicyType,
    build_policy_rule,
)


class ExactPolicyScopeMatcher(PolicyScopeMatcher):
    def match(self, scope, context):
        if scope.get("ambiguous"):
            return PolicyScopeMatch.AMBIGUOUS
        if all(context.get(key) == value for key, value in scope.items()):
            return PolicyScopeMatch.MATCH
        return PolicyScopeMatch.MISMATCH


class PolicyEvaluationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.audit = InMemoryAuditLogRepository()
        self.repository = InMemoryPolicyRepository(
            self.audit, audit_chain_id="governance-audit"
        )
        self.service = PolicyEvaluationService(
            self.repository,
            ExactPolicyScopeMatcher(),
            self.audit,
            audit_chain_id="governance-audit",
            clock=lambda: datetime(2026, 6, 19, 13, 0, tzinfo=timezone.utc),
        )
        self.authority = AuthorityResolutionResult(
            authority_resolution_id="authority-resolution-1",
            request_id="request-1",
            outcome=AuthorityResolutionOutcome.AUTHORIZED,
            reason="explicit_authority_record_matched",
            evidence_hash="authority-evidence-1",
            resolved_at="2026-06-19T12:00:00Z",
            evaluated_authority_record_ids=("authority-1",),
            authority_record_id="authority-1",
            authority_source_id="requester-1",
            authority_type=AuthorityType.PARENT,
            scope={"actions": ("read",), "resources": ("record-1",)},
            audit_event_id="audit-authority-resolution",
        )

    def _rule(
        self,
        *,
        rule_id: str = "rule-1",
        policy_id: str = "policy-1",
        effect: PolicyEffect = PolicyEffect.AUTHORIZE,
        priority: int = 10,
        expires_at: str | None = "2026-07-19T12:00:00Z",
    ):
        return build_policy_rule(
            rule_id=rule_id,
            policy_id=policy_id,
            policy_version="policy-v1",
            policy_type=PolicyType.AUTHORITY,
            effect=effect,
            actions=("read",),
            resources=("record-1",),
            scope={"location": "school"},
            priority=priority,
            reason="policy_authorized" if effect is PolicyEffect.AUTHORIZE else "policy_denied",
            created_by="policy-admin",
            effective_at="2026-06-19T12:00:00Z",
            expires_at=expires_at,
            status=PolicyStatus.ACTIVE,
        )

    def _register(self, rule=None, index: int = 1):
        return self.repository.register(
            rule or self._rule(),
            actor_id="policy-admin",
            reason="policy_registered",
            occurred_at="2026-06-19T12:01:00Z",
            audit_event_id=f"audit-policy-{index}",
        )

    def _request(self, **overrides: object) -> PolicyEvaluationRequest:
        values: dict[str, object] = {
            "policy_evaluation_id": "policy-evaluation-1",
            "request_id": "request-1",
            "subject_id": "subject-1",
            "requester_id": "requester-1",
            "authority_verdict_id": "authority-resolution-1",
            "action": "read",
            "resource": "record-1",
            "context": {"location": "school"},
            "policy_version": "policy-v1",
        }
        values.update(overrides)
        return PolicyEvaluationRequest(**values)  # type: ignore[arg-type]

    def test_authorized_request(self) -> None:
        self._register()

        result = self.service.evaluate(self._request(), self.authority)

        self.assertEqual(result.outcome, PolicyEvaluationOutcome.AUTHORIZED)
        self.assertEqual(result.matched_rules, ("rule-1",))

    def test_denied_request(self) -> None:
        self._register(self._rule(effect=PolicyEffect.DENY))

        result = self.service.evaluate(self._request(), self.authority)

        self.assertEqual(result.outcome, PolicyEvaluationOutcome.DENIED)
        self.assertEqual(result.failed_rules, ("rule-1",))

    def test_conflicting_rules(self) -> None:
        self._register(self._rule(), index=1)
        self._register(
            self._rule(
                rule_id="rule-2",
                policy_id="policy-2",
                effect=PolicyEffect.DENY,
            ),
            index=2,
        )

        result = self.service.evaluate(self._request(), self.authority)

        self.assertEqual(result.outcome, PolicyEvaluationOutcome.CONFLICT)

    def test_expired_policy(self) -> None:
        self._register(self._rule(expires_at="2026-06-19T12:30:00Z"))

        result = self.service.evaluate(self._request(), self.authority)

        self.assertEqual(result.outcome, PolicyEvaluationOutcome.EXPIRED)

    def test_revoked_policy(self) -> None:
        self._register()
        self.repository.update_status(
            "rule-1",
            PolicyStatus.REVOKED,
            actor_id="policy-admin",
            reason="policy_revoked",
            occurred_at="2026-06-19T12:30:00Z",
            audit_event_id="audit-policy-revoked",
        )

        result = self.service.evaluate(self._request(), self.authority)

        self.assertEqual(result.outcome, PolicyEvaluationOutcome.REVOKED)

    def test_invalid_policy(self) -> None:
        result = self.service.evaluate(
            self._request(policy_version="missing-version"), self.authority
        )

        self.assertEqual(result.outcome, PolicyEvaluationOutcome.INVALID_POLICY)

    def test_deterministic_evaluation(self) -> None:
        self._register()
        request = self._request()

        first = self.service.evaluate(request, self.authority)
        audit_count = len(self.audit.chain("governance-audit"))
        second = self.service.evaluate(request, self.authority)

        self.assertEqual(first, second)
        self.assertEqual(len(self.audit.chain("governance-audit")), audit_count)

    def test_higher_priority_rule_controls_evaluation(self) -> None:
        self._register(
            self._rule(effect=PolicyEffect.DENY, priority=10), index=1
        )
        self._register(
            self._rule(
                rule_id="rule-2",
                policy_id="policy-2",
                effect=PolicyEffect.AUTHORIZE,
                priority=20,
            ),
            index=2,
        )

        result = self.service.evaluate(self._request(), self.authority)

        self.assertEqual(result.outcome, PolicyEvaluationOutcome.AUTHORIZED)
        self.assertEqual(result.matched_rules, ("rule-2",))

    def test_valid_delegation_is_accepted_as_upstream_evidence(self) -> None:
        self._register()
        delegation = DelegationValidationResult(
            validation_id="delegation-validation-1",
            delegation_id="delegation-1",
            outcome=DelegationValidationOutcome.VALID,
            reason="delegation_valid",
            evidence_hash="delegation-evidence-1",
            validated_at="2026-06-19T12:30:00Z",
        )

        result = self.service.evaluate(
            self._request(
                requester_id="delegate-1",
                delegation_id="delegation-1",
            ),
            self.authority,
            delegation,
        )

        self.assertEqual(result.outcome, PolicyEvaluationOutcome.AUTHORIZED)


if __name__ == "__main__":
    unittest.main()
