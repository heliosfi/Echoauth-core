"""Deterministic Runtime Authorization Gate foundation for Sprint 2G."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from threading import RLock
from typing import Any

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth.authority_models import freeze_authority_value
from echoauth.auth.authorization_models import (
    AuthorizationDecision,
    AuthorizationOutcome,
    AuthorizationRequest,
)
from echoauth.auth.authority_resolution import (
    AuthorityResolutionOutcome,
    AuthorityResolutionService,
)
from echoauth.auth.authority_validation import parse_authority_timestamp
from echoauth.auth.delegation_models import (
    DelegationValidationOutcome,
    DelegationValidationRequest,
)
from echoauth.auth.delegation_repository import (
    DelegationNotFoundError,
    DelegationRepository,
)
from echoauth.auth.delegation_service import DelegationValidationService
from echoauth.canonical import CanonicalDataError, canonical_json_text, canonical_sha256
from echoauth.identity.service import RegistryIdentityService
from echoauth.models import (
    ActorType,
    AssuranceLevel,
    AuditAppendState,
    AuditRecord,
    AuthorityResolutionRequest,
    IdentityResolutionRequest,
)
from echoauth.policy.models import PolicyEvaluationOutcome, PolicyEvaluationRequest
from echoauth.policy.service import PolicyEvaluationService


class AuthorizationGateValidationError(ValueError):
    pass


class AuthorizationGateAuditError(RuntimeError):
    pass


class AuthorizationGateService:
    """Run identity, authority, delegation, and policy in fixed order."""

    def __init__(
        self,
        identity_service: RegistryIdentityService,
        authority_service: AuthorityResolutionService,
        delegation_repository: DelegationRepository,
        delegation_service: DelegationValidationService,
        policy_service: PolicyEvaluationService,
        audit_repository: InMemoryAuditLogRepository,
        *,
        audit_chain_id: str,
        component_id: str = "authorization_gate_service",
        clock=None,
    ) -> None:
        if not audit_chain_id:
            raise ValueError("audit_chain_id must not be empty")
        self._identity_service = identity_service
        self._authority_service = authority_service
        self._delegation_repository = delegation_repository
        self._delegation_service = delegation_service
        self._policy_service = policy_service
        self._audit_repository = audit_repository
        self._audit_chain_id = audit_chain_id
        self._component_id = component_id
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._cache: dict[str, AuthorizationDecision] = {}
        self._lock = RLock()

    def authorize(self, request: AuthorizationRequest) -> AuthorizationDecision:
        now = self._utc_now()
        try:
            validate_authorization_request(request)
        except AuthorizationGateValidationError:
            return self._complete(
                request,
                AuthorizationOutcome.DENIED,
                "invalid_authorization_request",
                now,
                evidence={},
            )

        evidence: dict[str, Any] = {
            "evaluation_order": (
                "identity",
                "authority",
                "delegation",
                "policy",
            ),
            "payload_hash": canonical_sha256(request.payload),
            "context_hash": canonical_sha256(request.context),
        }

        try:
            identity = self._identity_service.resolve(
                IdentityResolutionRequest(
                    identity_request_id=f"identity_{request.request_id}",
                    actor_id=request.requester_id,
                    actor_type=request.requester_type,
                    credential_set=request.credential_set,
                    context=request.context,
                    required_assurance=request.required_assurance,
                    subject_id=request.subject_id,
                    session_id=request.session_id,
                )
            )
        except Exception as exc:
            evidence["identity"] = {"error": type(exc).__name__}
            return self._complete(
                request,
                AuthorizationOutcome.INVALID_IDENTITY,
                "identity_dependency_failed",
                now,
                evidence=evidence,
            )
        evidence["identity"] = {
            "evidence_hash": identity.evidence_hash,
            "expires_at": identity.expires_at,
            "state": identity.state,
            "verdict_id": identity.identity_verdict_id,
        }
        if identity.state == "expired" or parse_authority_timestamp(
            identity.expires_at, "identity_expires_at"
        ) <= now:
            return self._complete(
                request,
                AuthorizationOutcome.EXPIRED,
                "identity_expired",
                now,
                evidence=evidence,
                identity_id=identity.identity_verdict_id,
            )
        if identity.state == "conflict":
            return self._complete(
                request,
                AuthorizationOutcome.CONFLICT,
                "identity_conflict",
                now,
                evidence=evidence,
                identity_id=identity.identity_verdict_id,
            )
        if identity.state != "verified":
            return self._complete(
                request,
                AuthorizationOutcome.INVALID_IDENTITY,
                "identity_not_verified",
                now,
                evidence=evidence,
                identity_id=identity.identity_verdict_id,
            )

        grant = None
        authority_requester = request.requester_id
        if request.delegation_id is not None:
            try:
                grant = self._delegation_repository.get(
                    request.delegation_id
                ).delegation_grant
                authority_requester = grant.grantor_id
            except DelegationNotFoundError:
                evidence["delegation"] = {
                    "delegation_id": request.delegation_id,
                    "state": "not_found",
                }
                return self._complete(
                    request,
                    AuthorizationOutcome.INVALID_DELEGATION,
                    "delegation_not_found",
                    now,
                    evidence=evidence,
                    identity_id=identity.identity_verdict_id,
                )

        try:
            authority = self._authority_service.resolve(
                AuthorityResolutionRequest(
                    request_id=request.request_id,
                    subject_id=request.subject_id,
                    requester_id=authority_requester,
                    action=request.action,
                    resource=request.resource,
                    context=request.context,
                    identity_verdict_id=identity.identity_verdict_id,
                    authority_records=(),
                    policy_version=request.policy_version,
                )
            )
        except Exception as exc:
            evidence["authority"] = {"error": type(exc).__name__}
            return self._complete(
                request,
                AuthorizationOutcome.INVALID_AUTHORITY,
                "authority_dependency_failed",
                now,
                evidence=evidence,
                identity_id=identity.identity_verdict_id,
            )
        evidence["authority"] = {
            "authority_record_id": authority.authority_record_id,
            "evidence_hash": authority.evidence_hash,
            "outcome": authority.outcome.value,
            "resolution_id": authority.authority_resolution_id,
        }
        authority_failure = _authority_failure(authority.outcome)
        if authority_failure is not None:
            outcome, reason = authority_failure
            return self._complete(
                request,
                outcome,
                reason,
                now,
                evidence=evidence,
                identity_id=identity.identity_verdict_id,
                authority_id=authority.authority_resolution_id,
            )
        if grant is not None and authority.authority_record_id != grant.source_authority_reference:
            return self._complete(
                request,
                AuthorizationOutcome.INVALID_AUTHORITY,
                "delegation_authority_source_mismatch",
                now,
                evidence=evidence,
                identity_id=identity.identity_verdict_id,
                authority_id=authority.authority_resolution_id,
            )

        delegation = None
        if grant is None:
            evidence["delegation"] = {"required": False, "state": "not_required"}
        else:
            try:
                delegation = self._delegation_service.validate(
                    DelegationValidationRequest(
                        validation_id=f"delegation_{request.request_id}",
                        delegation_id=grant.delegation_id,
                        requester_id=request.requester_id,
                        subject_id=request.subject_id,
                        action=request.action,
                        resource=request.resource,
                        context=request.context,
                        authority_verdict_id=grant.authority_resolution_id,
                    )
                )
            except Exception as exc:
                evidence["delegation"] = {"error": type(exc).__name__}
                return self._complete(
                    request,
                    AuthorizationOutcome.INVALID_DELEGATION,
                    "delegation_dependency_failed",
                    now,
                    evidence=evidence,
                    identity_id=identity.identity_verdict_id,
                    authority_id=authority.authority_resolution_id,
                )
            evidence["delegation"] = {
                "delegation_id": delegation.delegation_id,
                "evidence_hash": delegation.evidence_hash,
                "outcome": delegation.outcome.value,
                "validation_id": delegation.validation_id,
            }
            delegation_failure = _delegation_failure(delegation.outcome)
            if delegation_failure is not None:
                outcome, reason = delegation_failure
                return self._complete(
                    request,
                    outcome,
                    reason,
                    now,
                    evidence=evidence,
                    identity_id=identity.identity_verdict_id,
                    authority_id=authority.authority_resolution_id,
                    delegation_id=delegation.validation_id,
                )

        try:
            policy = self._policy_service.evaluate(
                PolicyEvaluationRequest(
                    policy_evaluation_id=f"policy_{request.request_id}",
                    request_id=request.request_id,
                    subject_id=request.subject_id,
                    requester_id=request.requester_id,
                    authority_verdict_id=authority.authority_resolution_id,
                    delegation_id=request.delegation_id,
                    action=request.action,
                    resource=request.resource,
                    context=request.context,
                    policy_version=request.policy_version,
                ),
                authority,
                delegation,
            )
        except Exception as exc:
            evidence["policy"] = {"error": type(exc).__name__}
            return self._complete(
                request,
                AuthorizationOutcome.INVALID_POLICY,
                "policy_dependency_failed",
                now,
                evidence=evidence,
                identity_id=identity.identity_verdict_id,
                authority_id=authority.authority_resolution_id,
                delegation_id=delegation.validation_id if delegation else None,
            )
        evidence["policy"] = {
            "decision_id": policy.policy_decision_id,
            "evidence_hash": policy.evidence_hash,
            "outcome": policy.outcome.value,
        }
        outcome, reason = _policy_outcome(policy.outcome)
        return self._complete(
            request,
            outcome,
            reason,
            now,
            evidence=evidence,
            identity_id=identity.identity_verdict_id,
            authority_id=authority.authority_resolution_id,
            delegation_id=delegation.validation_id if delegation else None,
            policy_id=policy.policy_decision_id,
        )

    def _complete(
        self,
        request,
        outcome,
        reason,
        now,
        *,
        evidence,
        identity_id=None,
        authority_id=None,
        delegation_id=None,
        policy_id=None,
    ):
        evidence_package = {
            **evidence,
            "correlation_id": request.correlation_id,
            "idempotency_key": request.idempotency_key,
            "request_id": request.request_id,
        }
        evidence_hash = canonical_sha256(evidence_package)
        decision_hash = canonical_sha256(
            {"evidence_hash": evidence_hash, "outcome": outcome.value, "reason": reason}
        )
        with self._lock:
            cached = self._cache.get(decision_hash)
            if cached is not None:
                return cached
            decision_id = f"adec_{decision_hash}"
            audit_event_id = f"audit_{decision_id}"
            audit = self._audit_repository.append(
                AuditRecord(
                    event_type="authorization.decision",
                    actor_id=self._component_id,
                    request_id=request.request_id or None,
                    authority_verdict_id=authority_id,
                    reason=reason,
                    details={
                        "authorization_decision_id": decision_id,
                        "evidence_hash": evidence_hash,
                        "outcome": outcome.value,
                    },
                    occurred_at=_timestamp(now),
                ),
                audit_event_id=audit_event_id,
                chain_id=self._audit_chain_id,
            )
            if audit.append_state is not AuditAppendState.ACCEPTED:
                raise AuthorizationGateAuditError(
                    f"authorization decision audit failed: {audit.reason}"
                )
            decision = AuthorizationDecision(
                authorization_decision_id=decision_id,
                request_id=request.request_id,
                outcome=outcome,
                reason=reason,
                evidence_hash=evidence_hash,
                evidence=freeze_authority_value(evidence_package),
                decided_at=_timestamp(now),
                identity_verdict_id=identity_id,
                authority_resolution_id=authority_id,
                delegation_validation_id=delegation_id,
                policy_decision_id=policy_id,
                audit_event_id=audit_event_id,
            )
            self._cache[decision_hash] = decision
            return decision

    def _utc_now(self):
        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise AuthorizationGateValidationError("gate clock must be timezone-aware")
        return now.astimezone(timezone.utc)


def validate_authorization_request(request: AuthorizationRequest) -> None:
    if not isinstance(request, AuthorizationRequest):
        raise AuthorizationGateValidationError("request must be AuthorizationRequest")
    for field_name in (
        "request_id",
        "requester_id",
        "subject_id",
        "action",
        "resource",
        "policy_version",
        "correlation_id",
        "idempotency_key",
    ):
        value = getattr(request, field_name)
        if not isinstance(value, str) or not value:
            raise AuthorizationGateValidationError(f"{field_name} must be non-empty")
    if not isinstance(request.requester_type, ActorType):
        raise AuthorizationGateValidationError("requester_type must be canonical")
    if not isinstance(request.required_assurance, AssuranceLevel):
        raise AuthorizationGateValidationError("required_assurance must be canonical")
    for field_name in ("credential_set", "payload", "context"):
        value = getattr(request, field_name)
        if not isinstance(value, Mapping):
            raise AuthorizationGateValidationError(f"{field_name} must be an object")
        try:
            canonical_json_text(value)
        except (CanonicalDataError, TypeError, ValueError) as exc:
            raise AuthorizationGateValidationError(
                f"{field_name} is not canonical JSON: {exc}"
            ) from exc


def _authority_failure(outcome):
    if outcome is AuthorityResolutionOutcome.AUTHORIZED:
        return None
    if outcome is AuthorityResolutionOutcome.REVOKED:
        return AuthorizationOutcome.REVOKED, "authority_revoked"
    if outcome is AuthorityResolutionOutcome.EXPIRED:
        return AuthorizationOutcome.EXPIRED, "authority_expired"
    if outcome is AuthorityResolutionOutcome.CONFLICT:
        return AuthorizationOutcome.CONFLICT, "authority_conflict"
    return AuthorizationOutcome.INVALID_AUTHORITY, "authority_not_valid"


def _delegation_failure(outcome):
    if outcome is DelegationValidationOutcome.VALID:
        return None
    if outcome is DelegationValidationOutcome.REVOKED:
        return AuthorizationOutcome.REVOKED, "delegation_revoked"
    if outcome is DelegationValidationOutcome.EXPIRED:
        return AuthorizationOutcome.EXPIRED, "delegation_expired"
    if outcome is DelegationValidationOutcome.CONFLICT:
        return AuthorizationOutcome.CONFLICT, "delegation_conflict"
    return AuthorizationOutcome.INVALID_DELEGATION, "delegation_not_valid"


def _policy_outcome(outcome):
    if outcome is PolicyEvaluationOutcome.AUTHORIZED:
        return AuthorizationOutcome.AUTHORIZED, "authorization_dependencies_valid"
    if outcome is PolicyEvaluationOutcome.REVOKED:
        return AuthorizationOutcome.REVOKED, "policy_revoked"
    if outcome is PolicyEvaluationOutcome.EXPIRED:
        return AuthorizationOutcome.EXPIRED, "policy_expired"
    if outcome is PolicyEvaluationOutcome.CONFLICT:
        return AuthorizationOutcome.CONFLICT, "policy_conflict"
    if outcome is PolicyEvaluationOutcome.INVALID_POLICY:
        return AuthorizationOutcome.INVALID_POLICY, "policy_invalid"
    return AuthorizationOutcome.DENIED, "policy_denied"


def _timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
