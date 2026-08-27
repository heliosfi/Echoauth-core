"""Fresh authorization-to-execution evidence binding for SAL-19.

This module is validation-only. It does not create envelopes, issue tokens,
claim execution, dispatch commands, mutate runtime state, or call external
systems.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from threading import RLock
from typing import Any

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth.authorization_gate import AuthorizationGateService
from echoauth.auth.authorization_models import (
    AuthorizationOutcome,
    AuthorizationRequest,
)
from echoauth.canonical import canonical_sha256
from echoauth.models import AuditAppendState, AuditRecord

AUTHORIZATION_EXECUTION_BINDING_VERSION = "echoauth.authorization-execution-binding.v1"


class AuthorizationExecutionBindingError(ValueError):
    """Raised when fresh authorization cannot be bound to execution facts."""


class AuthorizationExecutionBindingAuditError(RuntimeError):
    """Raised when required binding audit evidence cannot append."""


@dataclass(frozen=True)
class AuthorizationExecutionEvidence:
    binding_version: str
    binding_id: str
    execution_request_id: str
    request_id: str
    requester_id: str
    subject_id: str
    action: str
    resource: str
    payload_hash: str
    context_hash: str
    policy_version: str
    delegation_id: str | None
    correlation_id: str
    idempotency_key: str
    authorization_decision_id: str
    authorization_evidence_hash: str
    authorization_decided_at: str
    authorization_reason: str
    identity_verdict_id: str
    identity_evidence_hash: str
    identity_expires_at: str
    authority_resolution_id: str
    authority_record_id: str
    authority_evidence_hash: str
    delegation_validation_id: str | None
    delegation_evidence_hash: str | None
    policy_decision_id: str
    policy_evidence_hash: str
    authorization_audit_event_id: str
    validated_at: str
    binding_evidence_hash: str
    binding_audit_event_id: str | None = None


class AuthorizationExecutionBinder:
    """Obtain fresh authorization and bind it to one execution request."""

    def __init__(
        self,
        authorization_gate: AuthorizationGateService,
        audit_repository: InMemoryAuditLogRepository,
        *,
        audit_chain_id: str,
        component_id: str = "authorization_execution_binder",
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if not isinstance(authorization_gate, AuthorizationGateService):
            raise TypeError("authorization_gate must be AuthorizationGateService")
        if not audit_chain_id:
            raise ValueError("audit_chain_id must not be empty")
        self._authorization_gate = authorization_gate
        self._audit_repository = audit_repository
        self._audit_chain_id = audit_chain_id
        self._component_id = component_id
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._cache: dict[str, AuthorizationExecutionEvidence] = {}
        self._lock = RLock()

    def bind(
        self,
        authorization_request: AuthorizationRequest,
        *,
        execution_request_id: str,
        actor_id: str,
        action: str,
        resource: str,
    ) -> AuthorizationExecutionEvidence:
        """Return fresh permission evidence for execution-eligibility assessment."""

        if not isinstance(authorization_request, AuthorizationRequest):
            raise AuthorizationExecutionBindingError(
                "authorization_request must be AuthorizationRequest"
            )
        for field_name, value in (
            ("execution_request_id", execution_request_id),
            ("actor_id", actor_id),
            ("action", action),
            ("resource", resource),
        ):
            if not isinstance(value, str) or not value:
                raise AuthorizationExecutionBindingError(
                    f"{field_name} must be non-empty"
                )
        if actor_id != authorization_request.requester_id:
            raise AuthorizationExecutionBindingError("authorization_actor_mismatch")
        if action != authorization_request.action:
            raise AuthorizationExecutionBindingError("authorization_action_mismatch")
        if resource != authorization_request.resource:
            raise AuthorizationExecutionBindingError("authorization_resource_mismatch")

        decision = self._authorization_gate.authorize(authorization_request)
        if decision.outcome is not AuthorizationOutcome.AUTHORIZED:
            raise AuthorizationExecutionBindingError(
                f"authorization_not_authorized:{decision.reason}"
            )
        if decision.request_id != authorization_request.request_id:
            raise AuthorizationExecutionBindingError("authorization_request_mismatch")
        if not decision.audit_event_id:
            raise AuthorizationExecutionBindingError("authorization_audit_missing")

        payload_hash = canonical_sha256(authorization_request.payload)
        context_hash = canonical_sha256(authorization_request.context)
        if decision.evidence.get("payload_hash") != payload_hash:
            raise AuthorizationExecutionBindingError("authorization_payload_hash_mismatch")
        if decision.evidence.get("context_hash") != context_hash:
            raise AuthorizationExecutionBindingError("authorization_context_hash_mismatch")

        identity = _required_mapping(decision.evidence, "identity")
        authority = _required_mapping(decision.evidence, "authority")
        policy = _required_mapping(decision.evidence, "policy")
        delegation = _optional_mapping(decision.evidence, "delegation")

        identity_verdict_id = _required_string(identity, "verdict_id")
        identity_evidence_hash = _required_string(identity, "evidence_hash")
        identity_expires_at = _required_string(identity, "expires_at")
        authority_resolution_id = _required_string(authority, "resolution_id")
        authority_record_id = _required_string(authority, "authority_record_id")
        authority_evidence_hash = _required_string(authority, "evidence_hash")
        policy_decision_id = _required_string(policy, "decision_id")
        policy_evidence_hash = _required_string(policy, "evidence_hash")

        if decision.identity_verdict_id != identity_verdict_id:
            raise AuthorizationExecutionBindingError("identity_reference_mismatch")
        if decision.authority_resolution_id != authority_resolution_id:
            raise AuthorizationExecutionBindingError("authority_reference_mismatch")
        if decision.policy_decision_id != policy_decision_id:
            raise AuthorizationExecutionBindingError("policy_reference_mismatch")

        delegation_validation_id: str | None = None
        delegation_evidence_hash: str | None = None
        if authorization_request.delegation_id is not None:
            if delegation is None:
                raise AuthorizationExecutionBindingError("delegation_evidence_missing")
            delegation_validation_id = _required_string(delegation, "validation_id")
            delegation_evidence_hash = _required_string(delegation, "evidence_hash")
            if decision.delegation_validation_id != delegation_validation_id:
                raise AuthorizationExecutionBindingError("delegation_reference_mismatch")
        elif decision.delegation_validation_id is not None:
            raise AuthorizationExecutionBindingError("unexpected_delegation_reference")

        validated_at = _timestamp(self._utc_now())
        base: dict[str, Any] = {
            "binding_version": AUTHORIZATION_EXECUTION_BINDING_VERSION,
            "execution_request_id": execution_request_id,
            "request_id": authorization_request.request_id,
            "requester_id": authorization_request.requester_id,
            "subject_id": authorization_request.subject_id,
            "action": authorization_request.action,
            "resource": authorization_request.resource,
            "payload_hash": payload_hash,
            "context_hash": context_hash,
            "policy_version": authorization_request.policy_version,
            "delegation_id": authorization_request.delegation_id,
            "correlation_id": authorization_request.correlation_id,
            "idempotency_key": authorization_request.idempotency_key,
            "authorization_decision_id": decision.authorization_decision_id,
            "authorization_evidence_hash": decision.evidence_hash,
            "authorization_decided_at": decision.decided_at,
            "authorization_reason": decision.reason,
            "identity_verdict_id": identity_verdict_id,
            "identity_evidence_hash": identity_evidence_hash,
            "identity_expires_at": identity_expires_at,
            "authority_resolution_id": authority_resolution_id,
            "authority_record_id": authority_record_id,
            "authority_evidence_hash": authority_evidence_hash,
            "delegation_validation_id": delegation_validation_id,
            "delegation_evidence_hash": delegation_evidence_hash,
            "policy_decision_id": policy_decision_id,
            "policy_evidence_hash": policy_evidence_hash,
            "authorization_audit_event_id": decision.audit_event_id,
            "validated_at": validated_at,
        }
        binding_evidence_hash = canonical_sha256(base)
        binding_id = f"aeb_{binding_evidence_hash}"

        with self._lock:
            cached = self._cache.get(binding_id)
            if cached is not None:
                return cached
            audit_event_id = f"audit_{binding_id}"
            audit = self._audit_repository.append(
                AuditRecord(
                    event_type="authorization.execution.binding.validation",
                    actor_id=self._component_id,
                    request_id=authorization_request.request_id,
                    authority_verdict_id=authority_resolution_id,
                    reason="authorization_execution_binding_valid",
                    details={
                        "authorization_decision_id": decision.authorization_decision_id,
                        "binding_evidence_hash": binding_evidence_hash,
                        "binding_id": binding_id,
                        "execution_request_id": execution_request_id,
                    },
                    occurred_at=validated_at,
                ),
                audit_event_id=audit_event_id,
                chain_id=self._audit_chain_id,
            )
            if audit.append_state is not AuditAppendState.ACCEPTED:
                raise AuthorizationExecutionBindingAuditError(
                    f"authorization execution binding audit failed: {audit.reason}"
                )
            evidence = AuthorizationExecutionEvidence(
                binding_id=binding_id,
                binding_evidence_hash=binding_evidence_hash,
                binding_audit_event_id=audit_event_id,
                **base,
            )
            self._cache[binding_id] = evidence
            return evidence

    def _utc_now(self) -> datetime:
        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise AuthorizationExecutionBindingError(
                "binding clock must be timezone-aware"
            )
        return now.astimezone(timezone.utc)


def authorization_execution_evidence_mapping(
    evidence: AuthorizationExecutionEvidence,
) -> dict[str, Any]:
    """Return the canonical mapping consumed by ExecutionControl evidence hashing."""

    if not isinstance(evidence, AuthorizationExecutionEvidence):
        raise AuthorizationExecutionBindingError(
            "evidence must be AuthorizationExecutionEvidence"
        )
    result = asdict(evidence)
    # Compatibility keys are explicit aliases for this fresh binding, not an
    # authority-registry record.
    result["authority_reference"] = evidence.binding_id
    result["authority_evidence_hash"] = evidence.binding_evidence_hash
    return result


def validate_bound_execution_facts(
    evidence: AuthorizationExecutionEvidence,
    *,
    execution_request_id: str,
    request_id: str,
    actor_id: str,
    action: str,
    resource: str,
) -> None:
    """Verify the fresh binding matches the execution facts exactly."""

    if not isinstance(evidence, AuthorizationExecutionEvidence):
        raise AuthorizationExecutionBindingError(
            "authorization binding evidence must be canonical"
        )
    expected = {
        "execution_request_id": execution_request_id,
        "request_id": request_id,
        "requester_id": actor_id,
        "action": action,
        "resource": resource,
    }
    for field_name, expected_value in expected.items():
        if getattr(evidence, field_name) != expected_value:
            raise AuthorizationExecutionBindingError(
                f"authorization_binding_{field_name}_mismatch"
            )
    base = asdict(evidence)
    base.pop("binding_id")
    base.pop("binding_evidence_hash")
    base.pop("binding_audit_event_id")
    if canonical_sha256(base) != evidence.binding_evidence_hash:
        raise AuthorizationExecutionBindingError(
            "authorization_binding_evidence_hash_mismatch"
        )


def _required_mapping(source: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = source.get(key)
    if not isinstance(value, Mapping):
        raise AuthorizationExecutionBindingError(f"{key}_evidence_missing")
    return value


def _optional_mapping(
    source: Mapping[str, Any], key: str
) -> Mapping[str, Any] | None:
    value = source.get(key)
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise AuthorizationExecutionBindingError(f"{key}_evidence_invalid")
    return value


def _required_string(source: Mapping[str, Any], key: str) -> str:
    value = source.get(key)
    if not isinstance(value, str) or not value:
        raise AuthorizationExecutionBindingError(f"{key}_missing")
    return value


def _timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
