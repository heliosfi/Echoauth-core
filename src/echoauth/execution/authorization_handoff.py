"""Validation-only authorization-to-execution evidence handoff for SAL-24."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth.authorization_gate import AuthorizationGateService
from echoauth.auth.authorization_models import (
    AuthorizationDecision,
    AuthorizationOutcome,
    AuthorizationRequest,
)
from echoauth.canonical import canonical_sha256
from echoauth.execution.models import ExecutionRequest
from echoauth.models import AuditAppendState, AuditRecord
from echoauth.persistence import MissingRecordError


HANDOFF_VERSION = "echoauth.authorization-execution-handoff.v1"


class AuthorizationExecutionHandoffValidationError(ValueError):
    pass


class AuthorizationExecutionHandoffAuditError(RuntimeError):
    pass


@dataclass(frozen=True)
class AuthorizationExecutionHandoffDecision:
    handoff_validation_id: str
    request_id: str
    requester_id: str
    subject_id: str
    action: str
    resource: str
    payload_hash: str
    context_hash: str
    policy_version: str
    delegation_id: str | None
    prior_authorization_decision_id: str
    fresh_authorization_decision_id: str | None
    fresh_authorization_evidence_hash: str | None
    fresh_authorization_audit_event_id: str | None
    identity_verdict_id: str | None
    authority_resolution_id: str | None
    delegation_validation_id: str | None
    policy_decision_id: str | None
    accepted: bool
    reason: str
    validated_at: str
    evidence_hash: str
    audit_event_id: str


class AuthorizationExecutionHandoffValidator:
    """Revalidate authorization and bind it to one execution-eligibility request.

    This service performs no execution, dispatch, envelope creation, token issuance,
    claim, or runtime-state mutation.
    """

    def __init__(
        self,
        authorization_gate: AuthorizationGateService,
        audit_repository: InMemoryAuditLogRepository,
        *,
        audit_chain_id: str,
        component_id: str = "authorization_execution_handoff_validator",
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if not audit_chain_id:
            raise ValueError("audit_chain_id must not be empty")
        self._authorization_gate = authorization_gate
        self._audit_repository = audit_repository
        self._audit_chain_id = audit_chain_id
        self._component_id = component_id
        self._clock = clock or (lambda: datetime.now(timezone.utc))

    def validate(
        self,
        execution_request: ExecutionRequest,
        authorization_request: AuthorizationRequest,
        prior_decision: AuthorizationDecision,
    ) -> AuthorizationExecutionHandoffDecision:
        if not isinstance(execution_request, ExecutionRequest):
            raise AuthorizationExecutionHandoffValidationError(
                "execution_request must be an ExecutionRequest"
            )
        if not isinstance(authorization_request, AuthorizationRequest):
            raise AuthorizationExecutionHandoffValidationError(
                "authorization_request must be an AuthorizationRequest"
            )
        if not isinstance(prior_decision, AuthorizationDecision):
            raise AuthorizationExecutionHandoffValidationError(
                "prior_decision must be an AuthorizationDecision"
            )

        now = self._utc_now()
        binding_reason = _request_binding_failure(execution_request, authorization_request)
        if binding_reason is not None:
            return self._complete(
                execution_request,
                authorization_request,
                prior_decision,
                fresh_decision=None,
                accepted=False,
                reason=binding_reason,
                now=now,
            )
        if prior_decision.outcome is not AuthorizationOutcome.AUTHORIZED:
            return self._complete(
                execution_request,
                authorization_request,
                prior_decision,
                fresh_decision=None,
                accepted=False,
                reason="prior_authorization_not_authorized",
                now=now,
            )
        if prior_decision.request_id != authorization_request.request_id:
            return self._complete(
                execution_request,
                authorization_request,
                prior_decision,
                fresh_decision=None,
                accepted=False,
                reason="prior_authorization_request_mismatch",
                now=now,
            )
        if not self._authorization_audit_matches(prior_decision):
            return self._complete(
                execution_request,
                authorization_request,
                prior_decision,
                fresh_decision=None,
                accepted=False,
                reason="prior_authorization_audit_mismatch",
                now=now,
            )

        # Currentness is established by a fresh gate invocation at consumption time.
        fresh_decision = self._authorization_gate.authorize(authorization_request)
        if not self._authorization_audit_matches(fresh_decision):
            return self._complete(
                execution_request,
                authorization_request,
                prior_decision,
                fresh_decision=fresh_decision,
                accepted=False,
                reason="fresh_authorization_audit_mismatch",
                now=now,
            )
        if fresh_decision.outcome is not AuthorizationOutcome.AUTHORIZED:
            return self._complete(
                execution_request,
                authorization_request,
                prior_decision,
                fresh_decision=fresh_decision,
                accepted=False,
                reason="fresh_authorization_not_authorized",
                now=now,
            )

        return self._complete(
            execution_request,
            authorization_request,
            prior_decision,
            fresh_decision=fresh_decision,
            accepted=True,
            reason="authorization_current_and_bound",
            now=now,
        )

    def _authorization_audit_matches(self, decision: AuthorizationDecision) -> bool:
        if not decision.audit_event_id:
            return False
        try:
            event = self._audit_repository.get(decision.audit_event_id)
        except MissingRecordError:
            return False
        details = event.record.get("details", {})
        return (
            event.record.get("event_type") == "authorization.decision"
            and event.record.get("request_id") == decision.request_id
            and details.get("authorization_decision_id")
            == decision.authorization_decision_id
            and details.get("evidence_hash") == decision.evidence_hash
            and details.get("outcome") == decision.outcome.value
        )

    def _complete(
        self,
        execution_request: ExecutionRequest,
        authorization_request: AuthorizationRequest,
        prior_decision: AuthorizationDecision,
        *,
        fresh_decision: AuthorizationDecision | None,
        accepted: bool,
        reason: str,
        now: datetime,
    ) -> AuthorizationExecutionHandoffDecision:
        payload_hash = canonical_sha256(authorization_request.payload)
        context_hash = canonical_sha256(authorization_request.context)
        evidence_package = {
            "handoff_version": HANDOFF_VERSION,
            "request_id": authorization_request.request_id,
            "requester_id": authorization_request.requester_id,
            "subject_id": authorization_request.subject_id,
            "action": authorization_request.action,
            "resource": authorization_request.resource,
            "payload_hash": payload_hash,
            "context_hash": context_hash,
            "policy_version": authorization_request.policy_version,
            "delegation_id": authorization_request.delegation_id,
            "prior_authorization_decision_id": prior_decision.authorization_decision_id,
            "prior_authorization_evidence_hash": prior_decision.evidence_hash,
            "fresh_authorization_decision_id": (
                fresh_decision.authorization_decision_id if fresh_decision else None
            ),
            "fresh_authorization_evidence_hash": (
                fresh_decision.evidence_hash if fresh_decision else None
            ),
            "fresh_authorization_audit_event_id": (
                fresh_decision.audit_event_id if fresh_decision else None
            ),
            "accepted": accepted,
            "reason": reason,
            "validated_at": _timestamp(now),
        }
        evidence_hash = canonical_sha256(evidence_package)
        handoff_validation_id = f"aeh_{canonical_sha256(evidence_package)}"
        audit_event_id = f"audit_{handoff_validation_id}"
        audit = self._audit_repository.append(
            AuditRecord(
                event_type="authorization.execution_handoff.validation",
                actor_id=self._component_id,
                request_id=authorization_request.request_id,
                authority_verdict_id=(
                    fresh_decision.authority_resolution_id if fresh_decision else None
                ),
                reason=reason,
                details={
                    "accepted": accepted,
                    "evidence_hash": evidence_hash,
                    "fresh_authorization_decision_id": (
                        fresh_decision.authorization_decision_id
                        if fresh_decision
                        else None
                    ),
                    "handoff_validation_id": handoff_validation_id,
                    "prior_authorization_decision_id": (
                        prior_decision.authorization_decision_id
                    ),
                },
                occurred_at=_timestamp(now),
            ),
            audit_event_id=audit_event_id,
            chain_id=self._audit_chain_id,
        )
        if audit.append_state is not AuditAppendState.ACCEPTED:
            raise AuthorizationExecutionHandoffAuditError(
                f"authorization execution handoff audit failed: {audit.reason}"
            )
        return AuthorizationExecutionHandoffDecision(
            handoff_validation_id=handoff_validation_id,
            request_id=authorization_request.request_id,
            requester_id=authorization_request.requester_id,
            subject_id=authorization_request.subject_id,
            action=authorization_request.action,
            resource=authorization_request.resource,
            payload_hash=payload_hash,
            context_hash=context_hash,
            policy_version=authorization_request.policy_version,
            delegation_id=authorization_request.delegation_id,
            prior_authorization_decision_id=prior_decision.authorization_decision_id,
            fresh_authorization_decision_id=(
                fresh_decision.authorization_decision_id if fresh_decision else None
            ),
            fresh_authorization_evidence_hash=(
                fresh_decision.evidence_hash if fresh_decision else None
            ),
            fresh_authorization_audit_event_id=(
                fresh_decision.audit_event_id if fresh_decision else None
            ),
            identity_verdict_id=(
                fresh_decision.identity_verdict_id if fresh_decision else None
            ),
            authority_resolution_id=(
                fresh_decision.authority_resolution_id if fresh_decision else None
            ),
            delegation_validation_id=(
                fresh_decision.delegation_validation_id if fresh_decision else None
            ),
            policy_decision_id=(
                fresh_decision.policy_decision_id if fresh_decision else None
            ),
            accepted=accepted,
            reason=reason,
            validated_at=_timestamp(now),
            evidence_hash=evidence_hash,
            audit_event_id=audit_event_id,
        )

    def _utc_now(self) -> datetime:
        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise AuthorizationExecutionHandoffValidationError(
                "handoff clock must be timezone-aware"
            )
        return now.astimezone(timezone.utc)


def _request_binding_failure(
    execution_request: ExecutionRequest,
    authorization_request: AuthorizationRequest,
) -> str | None:
    if execution_request.request_id != authorization_request.request_id:
        return "request_id_mismatch"
    if execution_request.actor_id != authorization_request.requester_id:
        return "requester_mismatch"
    if execution_request.subject_id != authorization_request.subject_id:
        return "subject_mismatch"
    if execution_request.action != authorization_request.action:
        return "action_mismatch"
    if execution_request.resource != authorization_request.resource:
        return "resource_mismatch"
    if execution_request.payload_hash != canonical_sha256(authorization_request.payload):
        return "payload_mismatch"
    if execution_request.context_hash != canonical_sha256(authorization_request.context):
        return "context_mismatch"
    if execution_request.policy_version != authorization_request.policy_version:
        return "policy_mismatch"
    if execution_request.delegation_id != authorization_request.delegation_id:
        return "delegation_mismatch"
    return None


def _timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
