"""Explicit, validation-only runtime state graph for Sprint 2L."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import asdict
from datetime import datetime, timezone
from threading import RLock

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.canonical import CanonicalDataError, canonical_json_text, canonical_sha256
from echoauth.models import AuditAppendState, AuditRecord
from echoauth.runtime.state_models import (
    RuntimeState,
    RuntimeStateEvidence,
    RuntimeTransition,
    RuntimeTransitionDecision,
    RuntimeTransitionRequest,
)

RUNTIME_STATE_GRAPH_VERSION = "echoauth.runtime-state.v1"


class RuntimeTransitionValidationError(ValueError):
    pass


class RuntimeTransitionAuditError(RuntimeError):
    pass


RUNTIME_STATE_GRAPH: Mapping[
    tuple[RuntimeState, RuntimeTransition], RuntimeState
] = {
    (RuntimeState.REQUESTED, RuntimeTransition.AUTHORIZE): RuntimeState.AUTHORIZED,
    (RuntimeState.REQUESTED, RuntimeTransition.REFUSE): RuntimeState.REFUSED,
    (RuntimeState.REQUESTED, RuntimeTransition.ESCALATE): RuntimeState.ESCALATED,
    (RuntimeState.REQUESTED, RuntimeTransition.EXPIRE): RuntimeState.EXPIRED,
    (RuntimeState.REQUESTED, RuntimeTransition.HALT): RuntimeState.HALTED,
    (RuntimeState.AUTHORIZED, RuntimeTransition.MARK_READY): RuntimeState.READY,
    (RuntimeState.AUTHORIZED, RuntimeTransition.REFUSE): RuntimeState.REFUSED,
    (RuntimeState.AUTHORIZED, RuntimeTransition.ESCALATE): RuntimeState.ESCALATED,
    (
        RuntimeState.AUTHORIZED,
        RuntimeTransition.BLOCK_EXECUTION,
    ): RuntimeState.EXECUTION_BLOCKED,
    (RuntimeState.AUTHORIZED, RuntimeTransition.EXPIRE): RuntimeState.EXPIRED,
    (RuntimeState.AUTHORIZED, RuntimeTransition.HALT): RuntimeState.HALTED,
    (RuntimeState.REFUSED, RuntimeTransition.ESCALATE): RuntimeState.ESCALATED,
    (
        RuntimeState.ESCALATED,
        RuntimeTransition.BEGIN_REVIEW,
    ): RuntimeState.UNDER_REVIEW,
    (RuntimeState.ESCALATED, RuntimeTransition.REFUSE): RuntimeState.REFUSED,
    (RuntimeState.ESCALATED, RuntimeTransition.EXPIRE): RuntimeState.EXPIRED,
    (RuntimeState.ESCALATED, RuntimeTransition.HALT): RuntimeState.HALTED,
    (
        RuntimeState.UNDER_REVIEW,
        RuntimeTransition.OVERRIDE,
    ): RuntimeState.OVERRIDDEN,
    (RuntimeState.UNDER_REVIEW, RuntimeTransition.REFUSE): RuntimeState.REFUSED,
    (
        RuntimeState.UNDER_REVIEW,
        RuntimeTransition.ESCALATE,
    ): RuntimeState.ESCALATED,
    (RuntimeState.UNDER_REVIEW, RuntimeTransition.EXPIRE): RuntimeState.EXPIRED,
    (RuntimeState.UNDER_REVIEW, RuntimeTransition.HALT): RuntimeState.HALTED,
    (RuntimeState.OVERRIDDEN, RuntimeTransition.MARK_READY): RuntimeState.READY,
    (
        RuntimeState.OVERRIDDEN,
        RuntimeTransition.BLOCK_EXECUTION,
    ): RuntimeState.EXECUTION_BLOCKED,
    (RuntimeState.OVERRIDDEN, RuntimeTransition.EXPIRE): RuntimeState.EXPIRED,
    (RuntimeState.OVERRIDDEN, RuntimeTransition.HALT): RuntimeState.HALTED,
    (
        RuntimeState.READY,
        RuntimeTransition.BLOCK_EXECUTION,
    ): RuntimeState.EXECUTION_BLOCKED,
    (RuntimeState.READY, RuntimeTransition.EXPIRE): RuntimeState.EXPIRED,
    (RuntimeState.READY, RuntimeTransition.HALT): RuntimeState.HALTED,
    (
        RuntimeState.EXECUTION_BLOCKED,
        RuntimeTransition.RELEASE_BLOCK,
    ): RuntimeState.READY,
    (
        RuntimeState.EXECUTION_BLOCKED,
        RuntimeTransition.ESCALATE,
    ): RuntimeState.ESCALATED,
    (
        RuntimeState.EXECUTION_BLOCKED,
        RuntimeTransition.EXPIRE,
    ): RuntimeState.EXPIRED,
    (
        RuntimeState.EXECUTION_BLOCKED,
        RuntimeTransition.HALT,
    ): RuntimeState.HALTED,
    (RuntimeState.HALTED, RuntimeTransition.ESCALATE): RuntimeState.ESCALATED,
}


class RuntimeStateMachine:
    """Validate proposed state transitions without applying or persisting them."""

    def __init__(
        self,
        audit_repository: InMemoryAuditLogRepository,
        *,
        audit_chain_id: str,
        component_id: str = "runtime_state_machine",
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if not audit_chain_id:
            raise ValueError("audit_chain_id must not be empty")
        self._audit_repository = audit_repository
        self._audit_chain_id = audit_chain_id
        self._component_id = component_id
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._cache: dict[str, RuntimeTransitionDecision] = {}
        self._lock = RLock()

    def validate(
        self, request: RuntimeTransitionRequest
    ) -> RuntimeTransitionDecision:
        """Validate and audit one proposed transition without changing state."""

        validate_transition_request(request)
        expected_state = RUNTIME_STATE_GRAPH.get(
            (request.current_state, request.transition)
        )
        allowed = expected_state is request.requested_state
        if expected_state is None:
            reason = "undefined_transition"
        elif not allowed:
            reason = "requested_state_mismatch"
        else:
            reason = "transition_valid"
        validated_state = request.requested_state if allowed else request.current_state
        evidence = RuntimeStateEvidence(
            graph_version=RUNTIME_STATE_GRAPH_VERSION,
            request_id=request.request_id,
            current_state=request.current_state,
            transition=request.transition,
            requested_state=request.requested_state,
            validated_state=validated_state,
            actor_id=request.actor_id,
            reason=request.reason,
            source_evidence_hash=canonical_sha256(request.evidence),
            occurred_at=request.occurred_at,
        )
        evidence_hash = canonical_sha256(asdict(evidence))
        decision_hash = canonical_sha256(
            {
                "allowed": allowed,
                "evidence_hash": evidence_hash,
                "reason": reason,
                "transition_request_id": request.transition_request_id,
            }
        )
        with self._lock:
            cached = self._cache.get(decision_hash)
            if cached is not None:
                return cached
            validated_at = self._utc_now()
            transition_decision_id = f"rtdec_{decision_hash}"
            audit_event_id = f"audit_{transition_decision_id}"
            audit = self._audit_repository.append(
                AuditRecord(
                    event_type="runtime.transition.validation",
                    actor_id=self._component_id,
                    request_id=request.request_id,
                    state_before=request.current_state.value,
                    state_after=validated_state.value,
                    reason=reason,
                    details={
                        "allowed": allowed,
                        "evidence_hash": evidence_hash,
                        "graph_version": RUNTIME_STATE_GRAPH_VERSION,
                        "requested_state": request.requested_state.value,
                        "transition": request.transition.value,
                        "transition_decision_id": transition_decision_id,
                        "transition_request_id": request.transition_request_id,
                    },
                    occurred_at=request.occurred_at,
                ),
                audit_event_id=audit_event_id,
                chain_id=self._audit_chain_id,
            )
            if audit.append_state is not AuditAppendState.ACCEPTED:
                raise RuntimeTransitionAuditError(
                    f"runtime transition audit append failed: {audit.reason}"
                )
            decision = RuntimeTransitionDecision(
                transition_decision_id=transition_decision_id,
                transition_request_id=request.transition_request_id,
                request_id=request.request_id,
                allowed=allowed,
                current_state=request.current_state,
                next_state=validated_state,
                transition=request.transition,
                reason=reason,
                evidence=evidence,
                evidence_hash=evidence_hash,
                validated_at=_timestamp(validated_at),
                audit_event_id=audit_event_id,
            )
            self._cache[decision_hash] = decision
            return decision

    def _utc_now(self) -> datetime:
        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise RuntimeTransitionValidationError(
                "runtime state clock must be timezone-aware"
            )
        return now.astimezone(timezone.utc)


def validate_transition_request(request: RuntimeTransitionRequest) -> None:
    if not isinstance(request, RuntimeTransitionRequest):
        raise RuntimeTransitionValidationError(
            "request must be a RuntimeTransitionRequest"
        )
    for field_name in (
        "transition_request_id",
        "request_id",
        "actor_id",
        "reason",
        "occurred_at",
    ):
        value = getattr(request, field_name)
        if not isinstance(value, str) or not value:
            raise RuntimeTransitionValidationError(f"{field_name} must be non-empty")
    if not isinstance(request.current_state, RuntimeState):
        raise RuntimeTransitionValidationError("current_state must be canonical")
    if not isinstance(request.requested_state, RuntimeState):
        raise RuntimeTransitionValidationError("requested_state must be canonical")
    if not isinstance(request.transition, RuntimeTransition):
        raise RuntimeTransitionValidationError("transition must be canonical")
    if not isinstance(request.evidence, Mapping) or not request.evidence:
        raise RuntimeTransitionValidationError(
            "evidence must be a non-empty canonical JSON object"
        )
    try:
        canonical_json_text(request.evidence)
    except (CanonicalDataError, TypeError, ValueError) as exc:
        raise RuntimeTransitionValidationError(
            f"evidence is not canonical JSON: {exc}"
        ) from exc
    _parse_utc(request.occurred_at)


def _parse_utc(value: str) -> datetime:
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise RuntimeTransitionValidationError(
            "occurred_at must be ISO 8601"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise RuntimeTransitionValidationError("occurred_at must be timezone-aware")
    if parsed.utcoffset().total_seconds() != 0:
        raise RuntimeTransitionValidationError("occurred_at must be UTC")
    return parsed.astimezone(timezone.utc)


def _timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
