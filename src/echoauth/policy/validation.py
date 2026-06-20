"""Deterministic policy artifact and request validation."""

from __future__ import annotations

import hmac
from collections.abc import Mapping, Sequence
from dataclasses import replace

from echoauth.auth.authority_models import freeze_authority_value
from echoauth.auth.authority_validation import parse_authority_timestamp
from echoauth.canonical import CanonicalDataError, canonical_json_text, canonical_sha256
from echoauth.policy.models import (
    PolicyEffect,
    PolicyEvaluationRequest,
    PolicyRule,
    PolicyStatus,
    PolicyType,
)


class PolicyValidationError(ValueError):
    """Raised when policy evidence fails closed validation."""


def build_policy_rule(
    *,
    rule_id: str,
    policy_id: str,
    policy_version: str,
    policy_type: PolicyType,
    effect: PolicyEffect,
    actions: Sequence[str],
    resources: Sequence[str],
    scope: Mapping[str, object],
    priority: int,
    reason: str,
    created_by: str,
    effective_at: str,
    expires_at: str | None = None,
    status: PolicyStatus = PolicyStatus.ACTIVE,
) -> PolicyRule:
    rule = PolicyRule(
        rule_id=rule_id,
        policy_id=policy_id,
        policy_version=policy_version,
        policy_type=policy_type,
        effect=effect,
        actions=tuple(sorted(actions)),
        resources=tuple(sorted(resources)),
        scope=freeze_authority_value(scope),
        priority=priority,
        reason=reason,
        status=status,
        created_by=created_by,
        effective_at=effective_at,
        expires_at=expires_at,
        policy_hash="",
    )
    rule = replace(rule, policy_hash=policy_rule_hash(rule))
    validate_policy_rule(rule)
    return rule


def policy_rule_hash(rule: PolicyRule) -> str:
    try:
        return canonical_sha256(
            {
                "actions": rule.actions,
                "created_by": rule.created_by,
                "effect": _enum_value(rule.effect),
                "effective_at": rule.effective_at,
                "expires_at": rule.expires_at,
                "policy_id": rule.policy_id,
                "policy_type": _enum_value(rule.policy_type),
                "policy_version": rule.policy_version,
                "priority": rule.priority,
                "reason": rule.reason,
                "resources": rule.resources,
                "rule_id": rule.rule_id,
                "scope": rule.scope,
            }
        )
    except (CanonicalDataError, TypeError, ValueError) as exc:
        raise PolicyValidationError(f"policy is not canonical JSON: {exc}") from exc


def validate_policy_rule(rule: PolicyRule) -> None:
    if not isinstance(rule, PolicyRule):
        raise PolicyValidationError("rule must be a PolicyRule")
    for field_name in (
        "rule_id",
        "policy_id",
        "policy_version",
        "reason",
        "created_by",
    ):
        value = getattr(rule, field_name)
        if not isinstance(value, str) or not value:
            raise PolicyValidationError(f"{field_name} must be a non-empty string")
    if not isinstance(rule.policy_type, PolicyType):
        raise PolicyValidationError("policy_type must be canonical")
    if not isinstance(rule.effect, PolicyEffect):
        raise PolicyValidationError("effect must be canonical")
    if not isinstance(rule.status, PolicyStatus):
        raise PolicyValidationError("status must be canonical")
    if isinstance(rule.priority, bool) or not isinstance(rule.priority, int):
        raise PolicyValidationError("priority must be an integer")
    _validate_string_tuple(rule.actions, "actions")
    _validate_string_tuple(rule.resources, "resources")
    _validate_object(rule.scope, "scope")
    effective_at = parse_authority_timestamp(rule.effective_at, "effective_at")
    if rule.expires_at is not None and parse_authority_timestamp(
        rule.expires_at, "expires_at"
    ) <= effective_at:
        raise PolicyValidationError("expires_at must be later than effective_at")
    if not rule.policy_hash or not hmac.compare_digest(rule.policy_hash, policy_rule_hash(rule)):
        raise PolicyValidationError("policy_hash does not match policy evidence")


def validate_policy_request(request: PolicyEvaluationRequest) -> None:
    if not isinstance(request, PolicyEvaluationRequest):
        raise PolicyValidationError("request must be a PolicyEvaluationRequest")
    for field_name in (
        "policy_evaluation_id",
        "request_id",
        "subject_id",
        "requester_id",
        "authority_verdict_id",
        "action",
        "resource",
        "policy_version",
    ):
        value = getattr(request, field_name)
        if not isinstance(value, str) or not value:
            raise PolicyValidationError(f"{field_name} must be a non-empty string")
    _validate_object(request.context, "context")


def _validate_string_tuple(value: object, field_name: str) -> None:
    if not isinstance(value, tuple) or not value:
        raise PolicyValidationError(f"{field_name} must be a non-empty tuple")
    if any(not isinstance(item, str) or not item for item in value):
        raise PolicyValidationError(f"{field_name} entries must be non-empty strings")
    if len(set(value)) != len(value):
        raise PolicyValidationError(f"{field_name} entries must be unique")


def _validate_object(value: object, field_name: str) -> None:
    if not isinstance(value, Mapping):
        raise PolicyValidationError(f"{field_name} must be a canonical JSON object")
    try:
        canonical_json_text(value)
    except (CanonicalDataError, TypeError, ValueError) as exc:
        raise PolicyValidationError(f"{field_name} is not canonical JSON: {exc}") from exc


def _enum_value(value: object) -> str:
    raw = getattr(value, "value", value)
    return raw if isinstance(raw, str) else repr(raw)
