"""Append-history in-memory policy repository for Sprint 2F."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import replace
from threading import RLock

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth.authority_models import freeze_authority_value
from echoauth.auth.authority_validation import parse_authority_timestamp
from echoauth.models import AuditAppendState, AuditRecord
from echoauth.policy.models import (
    PolicyHistoryEntry,
    PolicyRule,
    PolicyStatus,
    StoredPolicyRule,
)
from echoauth.policy.validation import PolicyValidationError, validate_policy_rule


class PolicyRepositoryError(ValueError):
    pass


class PolicyNotFoundError(KeyError):
    pass


class DuplicatePolicyError(PolicyRepositoryError):
    pass


class InvalidPolicyTransitionError(PolicyRepositoryError):
    pass


class PolicyAuditError(PolicyRepositoryError):
    pass


class PolicyRepository(ABC):
    @abstractmethod
    def register(
        self,
        rule: PolicyRule,
        *,
        actor_id: str,
        reason: str,
        occurred_at: str,
        audit_event_id: str,
    ) -> StoredPolicyRule:
        """Register one immutable policy rule."""

    @abstractmethod
    def get(self, rule_id: str) -> StoredPolicyRule:
        """Return a current policy rule."""

    @abstractmethod
    def rules_for_version(self, policy_version: str) -> tuple[StoredPolicyRule, ...]:
        """Return version-pinned rules in deterministic priority order."""

    @abstractmethod
    def update_status(
        self,
        rule_id: str,
        status: PolicyStatus,
        *,
        actor_id: str,
        reason: str,
        occurred_at: str,
        audit_event_id: str,
    ) -> StoredPolicyRule:
        """Apply one audited policy lifecycle transition."""

    @abstractmethod
    def history(self, rule_id: str) -> tuple[PolicyHistoryEntry, ...]:
        """Return immutable policy history."""


_ALLOWED_TRANSITIONS = {
    PolicyStatus.DRAFT: {PolicyStatus.ACTIVE, PolicyStatus.REVOKED},
    PolicyStatus.ACTIVE: {
        PolicyStatus.RETIRED,
        PolicyStatus.REVOKED,
        PolicyStatus.EXPIRED,
    },
    PolicyStatus.RETIRED: set(),
    PolicyStatus.REVOKED: set(),
    PolicyStatus.EXPIRED: set(),
}


class InMemoryPolicyRepository(PolicyRepository):
    def __init__(
        self,
        audit_repository: InMemoryAuditLogRepository,
        *,
        audit_chain_id: str,
    ) -> None:
        if not audit_chain_id:
            raise PolicyRepositoryError("audit_chain_id must not be empty")
        self._audit_repository = audit_repository
        self._audit_chain_id = audit_chain_id
        self._records: dict[str, StoredPolicyRule] = {}
        self._policy_versions: set[tuple[str, str]] = set()
        self._history: dict[str, list[PolicyHistoryEntry]] = {}
        self._lock = RLock()

    def register(
        self,
        rule: PolicyRule,
        *,
        actor_id: str,
        reason: str,
        occurred_at: str,
        audit_event_id: str,
    ) -> StoredPolicyRule:
        validate_policy_rule(rule)
        rule = replace(rule, scope=freeze_authority_value(rule.scope))
        occurred = parse_authority_timestamp(occurred_at, "occurred_at")
        if rule.status is PolicyStatus.ACTIVE and parse_authority_timestamp(
            rule.effective_at, "effective_at"
        ) > occurred:
            raise PolicyValidationError("active policy is not yet effective")
        if (
            rule.status is PolicyStatus.ACTIVE
            and rule.expires_at is not None
            and parse_authority_timestamp(rule.expires_at, "expires_at") <= occurred
        ):
            raise PolicyValidationError("active policy is already expired")
        self._validate_operation(actor_id, reason, audit_event_id)
        with self._lock:
            if rule.rule_id in self._records:
                raise DuplicatePolicyError("duplicate rule_id")
            key = (rule.policy_id, rule.policy_version)
            if key in self._policy_versions:
                raise DuplicatePolicyError("duplicate policy_id and policy_version")
            audit = self._append_audit(
                rule, "registered", actor_id, reason, occurred_at, audit_event_id
            )
            stored = StoredPolicyRule(rule, reason)
            self._records[rule.rule_id] = stored
            self._policy_versions.add(key)
            self._history[rule.rule_id] = [
                self._history_entry(rule, "registered", actor_id, reason, occurred_at, audit)
            ]
            return stored

    def get(self, rule_id: str) -> StoredPolicyRule:
        with self._lock:
            try:
                return self._records[rule_id]
            except KeyError as exc:
                raise PolicyNotFoundError(rule_id) from exc

    def rules_for_version(self, policy_version: str) -> tuple[StoredPolicyRule, ...]:
        if not isinstance(policy_version, str) or not policy_version:
            raise PolicyValidationError("policy_version must be a non-empty string")
        with self._lock:
            return tuple(
                sorted(
                    (
                        stored
                        for stored in self._records.values()
                        if stored.policy_rule.policy_version == policy_version
                    ),
                    key=lambda stored: (
                        -stored.policy_rule.priority,
                        stored.policy_rule.effective_at,
                        stored.policy_rule.rule_id,
                    ),
                )
            )

    def update_status(
        self,
        rule_id: str,
        status: PolicyStatus,
        *,
        actor_id: str,
        reason: str,
        occurred_at: str,
        audit_event_id: str,
    ) -> StoredPolicyRule:
        self._validate_operation(actor_id, reason, audit_event_id)
        occurred = parse_authority_timestamp(occurred_at, "occurred_at")
        if not isinstance(status, PolicyStatus):
            raise PolicyValidationError("status must be canonical")
        with self._lock:
            current = self.get(rule_id)
            if status not in _ALLOWED_TRANSITIONS[current.policy_rule.status]:
                raise InvalidPolicyTransitionError(
                    f"transition from {current.policy_rule.status.value} to {status.value} is not allowed"
                )
            previous_time = parse_authority_timestamp(
                self._history[rule_id][-1].occurred_at, "occurred_at"
            )
            if occurred < previous_time:
                raise PolicyValidationError("policy history time must be monotonic")
            if status is PolicyStatus.EXPIRED and current.policy_rule.expires_at is not None:
                if occurred < parse_authority_timestamp(
                    current.policy_rule.expires_at, "expires_at"
                ):
                    raise PolicyValidationError("policy cannot expire before expires_at")
            updated = replace(current.policy_rule, status=status)
            validate_policy_rule(updated)
            audit = self._append_audit(
                updated, status.value, actor_id, reason, occurred_at, audit_event_id
            )
            stored = StoredPolicyRule(updated, reason)
            self._records[rule_id] = stored
            self._history[rule_id].append(
                self._history_entry(updated, status.value, actor_id, reason, occurred_at, audit)
            )
            return stored

    def history(self, rule_id: str) -> tuple[PolicyHistoryEntry, ...]:
        with self._lock:
            try:
                return tuple(self._history[rule_id])
            except KeyError as exc:
                raise PolicyNotFoundError(rule_id) from exc

    def _append_audit(
        self,
        rule: PolicyRule,
        operation: str,
        actor_id: str,
        reason: str,
        occurred_at: str,
        audit_event_id: str,
    ):
        result = self._audit_repository.append(
            AuditRecord(
                event_type=f"policy.rule_{operation}",
                actor_id=actor_id,
                reason=reason,
                details={
                    "policy_hash": rule.policy_hash,
                    "policy_id": rule.policy_id,
                    "policy_version": rule.policy_version,
                    "priority": rule.priority,
                    "rule_id": rule.rule_id,
                    "status": rule.status.value,
                },
                occurred_at=occurred_at,
            ),
            audit_event_id=audit_event_id,
            chain_id=self._audit_chain_id,
        )
        if result.append_state is not AuditAppendState.ACCEPTED:
            raise PolicyAuditError(f"policy audit append failed: {result.reason}")
        return result

    def _history_entry(self, rule, operation, actor_id, reason, occurred_at, audit):
        return PolicyHistoryEntry(
            sequence=len(self._history.get(rule.rule_id, ())) + 1,
            operation=operation,
            policy_rule=rule,
            actor_id=actor_id,
            reason=reason,
            occurred_at=occurred_at,
            audit_event_id=audit.audit_event_id,
            audit_event_hash=audit.event_hash,
            previous_audit_hash=audit.previous_hash,
        )

    @staticmethod
    def _validate_operation(actor_id: str, reason: str, audit_event_id: str) -> None:
        for field_name, value in (
            ("actor_id", actor_id),
            ("reason", reason),
            ("audit_event_id", audit_event_id),
        ):
            if not isinstance(value, str) or not value:
                raise PolicyValidationError(f"{field_name} must be a non-empty string")
