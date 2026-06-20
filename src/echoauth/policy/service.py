"""Deterministic authority/delegation-aware Policy Evaluation service."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime, timezone
from threading import RLock

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth.authority_models import freeze_authority_value
from echoauth.auth.authority_resolution import (
    AuthorityResolutionOutcome,
    AuthorityResolutionResult,
)
from echoauth.auth.authority_validation import parse_authority_timestamp
from echoauth.auth.delegation_models import (
    DelegationValidationOutcome,
    DelegationValidationResult,
)
from echoauth.canonical import canonical_sha256
from echoauth.models import AuditAppendState, AuditRecord, CanonicalJsonObject
from echoauth.policy.models import (
    PolicyEffect,
    PolicyEvaluationOutcome,
    PolicyEvaluationRequest,
    PolicyEvaluationResult,
    PolicyRule,
    PolicyScopeMatch,
    PolicyStatus,
)
from echoauth.policy.repository import PolicyRepository
from echoauth.policy.validation import PolicyValidationError, validate_policy_request


class PolicyEvaluationAuditError(RuntimeError):
    pass


class PolicyScopeMatcher(ABC):
    @abstractmethod
    def match(
        self,
        scope: CanonicalJsonObject,
        context: CanonicalJsonObject,
    ) -> PolicyScopeMatch:
        """Match canonical policy scope without expanding it."""


class PolicyEvaluationService:
    """Evaluate declarative rules after authority and optional delegation."""

    def __init__(
        self,
        repository: PolicyRepository,
        scope_matcher: PolicyScopeMatcher,
        audit_repository: InMemoryAuditLogRepository,
        *,
        audit_chain_id: str,
        component_id: str = "policy_evaluation_service",
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if not audit_chain_id:
            raise ValueError("audit_chain_id must not be empty")
        self._repository = repository
        self._scope_matcher = scope_matcher
        self._audit_repository = audit_repository
        self._audit_chain_id = audit_chain_id
        self._component_id = component_id
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._cache: dict[str, PolicyEvaluationResult] = {}
        self._lock = RLock()

    def evaluate(
        self,
        request: PolicyEvaluationRequest,
        authority_result: AuthorityResolutionResult,
        delegation_result: DelegationValidationResult | None = None,
    ) -> PolicyEvaluationResult:
        now = self._utc_now()
        try:
            validate_policy_request(request)
        except PolicyValidationError:
            return self._complete(
                request,
                authority_result,
                delegation_result,
                rules=(),
                outcome=PolicyEvaluationOutcome.INVALID_POLICY,
                reason="invalid_policy_evaluation_request",
                now=now,
            )

        dependency_outcome = self._validate_dependencies(
            request, authority_result, delegation_result
        )
        if dependency_outcome is not None:
            outcome, reason = dependency_outcome
            return self._complete(
                request,
                authority_result,
                delegation_result,
                rules=(),
                outcome=outcome,
                reason=reason,
                now=now,
            )

        rules = tuple(
            stored.policy_rule
            for stored in self._repository.rules_for_version(request.policy_version)
        )
        if not rules:
            return self._complete(
                request,
                authority_result,
                delegation_result,
                rules=(),
                outcome=PolicyEvaluationOutcome.INVALID_POLICY,
                reason="policy_version_not_found",
                now=now,
            )

        active: list[PolicyRule] = []
        revoked: list[PolicyRule] = []
        expired: list[PolicyRule] = []
        scope_ambiguous = False
        for rule in rules:
            if request.action not in rule.actions or request.resource not in rule.resources:
                continue
            scope_match = self._scope_matcher.match(rule.scope, request.context)
            if scope_match is PolicyScopeMatch.AMBIGUOUS:
                scope_ambiguous = True
                continue
            if scope_match is not PolicyScopeMatch.MATCH:
                continue
            if rule.status is PolicyStatus.REVOKED:
                revoked.append(rule)
            elif rule.status is PolicyStatus.EXPIRED or (
                rule.expires_at is not None
                and parse_authority_timestamp(rule.expires_at, "expires_at") <= now
            ):
                expired.append(rule)
            elif rule.status is PolicyStatus.ACTIVE and parse_authority_timestamp(
                rule.effective_at, "effective_at"
            ) <= now:
                active.append(rule)

        if scope_ambiguous:
            return self._complete(
                request,
                authority_result,
                delegation_result,
                rules=rules,
                outcome=PolicyEvaluationOutcome.CONFLICT,
                reason="policy_scope_ambiguous",
                now=now,
            )
        if not active:
            if revoked:
                outcome, reason = PolicyEvaluationOutcome.REVOKED, "matching_policy_revoked"
            elif expired:
                outcome, reason = PolicyEvaluationOutcome.EXPIRED, "matching_policy_expired"
            else:
                outcome, reason = PolicyEvaluationOutcome.DENIED, "no_matching_active_policy"
            return self._complete(
                request,
                authority_result,
                delegation_result,
                rules=rules,
                outcome=outcome,
                reason=reason,
                now=now,
                matched=tuple(rule.rule_id for rule in revoked or expired),
            )

        highest_priority = max(rule.priority for rule in active)
        selected = tuple(rule for rule in active if rule.priority == highest_priority)
        effects = {rule.effect for rule in selected}
        if len(effects) > 1:
            return self._complete(
                request,
                authority_result,
                delegation_result,
                rules=rules,
                outcome=PolicyEvaluationOutcome.CONFLICT,
                reason="conflicting_highest_priority_rules",
                now=now,
                matched=tuple(rule.rule_id for rule in selected),
                failed=tuple(
                    rule.rule_id for rule in selected if rule.effect is PolicyEffect.DENY
                ),
            )
        if PolicyEffect.DENY in effects:
            deny_rule = selected[0]
            return self._complete(
                request,
                authority_result,
                delegation_result,
                rules=rules,
                outcome=PolicyEvaluationOutcome.DENIED,
                reason=deny_rule.reason,
                now=now,
                matched=tuple(rule.rule_id for rule in selected),
                failed=tuple(rule.rule_id for rule in selected),
            )
        return self._complete(
            request,
            authority_result,
            delegation_result,
            rules=rules,
            outcome=PolicyEvaluationOutcome.AUTHORIZED,
            reason=selected[0].reason,
            now=now,
            matched=tuple(rule.rule_id for rule in selected),
        )

    def _validate_dependencies(self, request, authority, delegation):
        if authority.authority_resolution_id != request.authority_verdict_id:
            return PolicyEvaluationOutcome.DENIED, "authority_reference_mismatch"
        if authority.request_id != request.request_id:
            return PolicyEvaluationOutcome.DENIED, "authority_request_mismatch"
        if authority.outcome is AuthorityResolutionOutcome.REVOKED:
            return PolicyEvaluationOutcome.REVOKED, "authority_revoked"
        if authority.outcome is AuthorityResolutionOutcome.EXPIRED:
            return PolicyEvaluationOutcome.EXPIRED, "authority_expired"
        if authority.outcome is not AuthorityResolutionOutcome.AUTHORIZED:
            return PolicyEvaluationOutcome.DENIED, "authority_not_authorized"
        if request.delegation_id is None:
            if delegation is not None:
                return PolicyEvaluationOutcome.INVALID_POLICY, "unexpected_delegation_result"
            if authority.authority_source_id != request.requester_id:
                return PolicyEvaluationOutcome.DENIED, "requester_not_authority_source"
            return None
        if delegation is None or delegation.delegation_id != request.delegation_id:
            return PolicyEvaluationOutcome.DENIED, "delegation_result_missing_or_mismatched"
        if delegation.outcome is DelegationValidationOutcome.REVOKED:
            return PolicyEvaluationOutcome.REVOKED, "delegation_revoked"
        if delegation.outcome is DelegationValidationOutcome.EXPIRED:
            return PolicyEvaluationOutcome.EXPIRED, "delegation_expired"
        if delegation.outcome is not DelegationValidationOutcome.VALID:
            return PolicyEvaluationOutcome.DENIED, "delegation_not_valid"
        return None

    def _complete(
        self,
        request,
        authority,
        delegation,
        *,
        rules: Sequence[PolicyRule],
        outcome: PolicyEvaluationOutcome,
        reason: str,
        now: datetime,
        matched: tuple[str, ...] = (),
        failed: tuple[str, ...] = (),
    ) -> PolicyEvaluationResult:
        evidence_hash = policy_evaluation_evidence_hash(
            request, authority, delegation, rules, now
        )
        decision_hash = canonical_sha256(
            {"evidence_hash": evidence_hash, "outcome": outcome.value, "reason": reason}
        )
        with self._lock:
            cached = self._cache.get(decision_hash)
            if cached is not None:
                return cached
            decision_id = f"pdec_{decision_hash}"
            audit_event_id = f"audit_{decision_id}"
            audit = self._audit_repository.append(
                AuditRecord(
                    event_type="policy.decision",
                    actor_id=self._component_id,
                    request_id=request.request_id or None,
                    authority_verdict_id=request.authority_verdict_id or None,
                    reason=reason,
                    details={
                        "evidence_hash": evidence_hash,
                        "failed_rules": list(failed),
                        "matched_rules": list(matched),
                        "outcome": outcome.value,
                        "policy_evaluation_id": request.policy_evaluation_id,
                        "policy_version": request.policy_version,
                    },
                    occurred_at=_timestamp(now),
                ),
                audit_event_id=audit_event_id,
                chain_id=self._audit_chain_id,
            )
            if audit.append_state is not AuditAppendState.ACCEPTED:
                raise PolicyEvaluationAuditError(
                    f"policy evaluation audit append failed: {audit.reason}"
                )
            result = PolicyEvaluationResult(
                policy_decision_id=decision_id,
                policy_evaluation_id=request.policy_evaluation_id,
                outcome=outcome,
                reason=reason,
                matched_rules=matched,
                failed_rules=failed,
                evidence_hash=evidence_hash,
                evaluated_at=_timestamp(now),
                audit_event_id=audit_event_id,
            )
            self._cache[decision_hash] = result
            return result

    def _utc_now(self) -> datetime:
        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise PolicyValidationError("policy clock must be timezone-aware")
        return now.astimezone(timezone.utc)


def policy_evaluation_evidence_hash(request, authority, delegation, rules, now):
    return canonical_sha256(
        {
            "action": request.action,
            "authority_evidence_hash": authority.evidence_hash,
            "authority_verdict_id": request.authority_verdict_id,
            "context": request.context,
            "delegation_evidence_hash": delegation.evidence_hash if delegation else None,
            "delegation_id": request.delegation_id,
            "evaluated_at": _timestamp(now),
            "policy_evaluation_id": request.policy_evaluation_id,
            "policy_rules": [
                {
                    "policy_hash": rule.policy_hash,
                    "priority": rule.priority,
                    "rule_id": rule.rule_id,
                    "status": rule.status.value,
                }
                for rule in rules
            ],
            "policy_version": request.policy_version,
            "request_id": request.request_id,
            "requester_id": request.requester_id,
            "resource": request.resource,
            "subject_id": request.subject_id,
        }
    )


def _timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
