"""Deterministic, side-effect-free Execution Control for Sprint 2M."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import asdict
from datetime import datetime, timezone
from threading import RLock

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.canonical import CanonicalDataError, canonical_json_text, canonical_sha256
from echoauth.execution.models import (
    ExecutionConstraint,
    ExecutionDecision,
    ExecutionEvidence,
    ExecutionOutcome,
    ExecutionRequest,
)
from echoauth.models import AuditAppendState, AuditRecord
from echoauth.runtime import RuntimeState, RuntimeTransitionDecision

EXECUTION_CONTROL_VERSION = "echoauth.execution-control.v1"


class ExecutionControlValidationError(ValueError):
    pass


class ExecutionControlAuditError(RuntimeError):
    pass


class ExecutionControl:
    """Validate execution eligibility without dispatching or changing state."""

    def __init__(
        self,
        audit_repository: InMemoryAuditLogRepository,
        *,
        audit_chain_id: str,
        constraints: Sequence[ExecutionConstraint],
        component_id: str = "execution_control",
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if not audit_chain_id:
            raise ValueError("audit_chain_id must not be empty")
        self._constraints = _validate_constraints(constraints)
        self._audit_repository = audit_repository
        self._audit_chain_id = audit_chain_id
        self._component_id = component_id
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._cache: dict[str, ExecutionDecision] = {}
        self._lock = RLock()

    def validate(
        self,
        request: ExecutionRequest,
        runtime_decision: RuntimeTransitionDecision,
    ) -> ExecutionDecision:
        """Return eligibility evidence from one validated state decision."""

        validate_execution_request(request)
        if self._constraints.get(request.constraint.constraint_id) != request.constraint:
            raise ExecutionControlValidationError(
                "execution constraint is not configured"
            )
        self._validate_runtime_decision(request, runtime_decision)
        now = self._utc_now()
        outcome, reason = _classify(request, runtime_decision, now)
        evidence = ExecutionEvidence(
            control_version=EXECUTION_CONTROL_VERSION,
            request_id=request.request_id,
            actor_id=request.actor_id,
            action=request.action,
            resource=request.resource,
            requested_at=request.requested_at,
            runtime_transition_decision_id=runtime_decision.transition_decision_id,
            runtime_transition_evidence_hash=runtime_decision.evidence_hash,
            runtime_state=runtime_decision.next_state,
            constraint_hash=canonical_sha256(asdict(request.constraint)),
            authority_evidence_hash=_optional_hash(request.authority_evidence),
            refusal_evidence_hash=_optional_hash(request.refusal_evidence),
            escalation_evidence_hash=_optional_hash(request.escalation_evidence),
            review_evidence_hash=_optional_hash(request.review_evidence),
            override_evidence_hash=_optional_hash(request.override_evidence),
            request_evidence_hash=canonical_sha256(request.evidence),
            audit_references=request.audit_references,
        )
        evidence_hash = canonical_sha256(asdict(evidence))
        decision_hash = canonical_sha256(
            {
                "evidence_hash": evidence_hash,
                "execution_request_id": request.execution_request_id,
                "outcome": outcome.value,
                "reason": reason,
            }
        )
        with self._lock:
            cached = self._cache.get(decision_hash)
            if cached is not None:
                return cached
            execution_decision_id = f"execdec_{decision_hash}"
            audit_event_id = f"audit_{execution_decision_id}"
            audit = self._audit_repository.append(
                AuditRecord(
                    event_type="execution.eligibility.validation",
                    actor_id=self._component_id,
                    request_id=request.request_id,
                    reason=reason,
                    details={
                        "action": request.action,
                        "control_version": EXECUTION_CONTROL_VERSION,
                        "eligible": outcome is ExecutionOutcome.ELIGIBLE,
                        "evidence_hash": evidence_hash,
                        "execution_decision_id": execution_decision_id,
                        "execution_request_id": request.execution_request_id,
                        "outcome": outcome.value,
                        "resource": request.resource,
                        "runtime_state": runtime_decision.next_state.value,
                        "runtime_transition_decision_id": (
                            runtime_decision.transition_decision_id
                        ),
                    },
                    occurred_at=_timestamp(now),
                ),
                audit_event_id=audit_event_id,
                chain_id=self._audit_chain_id,
            )
            if audit.append_state is not AuditAppendState.ACCEPTED:
                raise ExecutionControlAuditError(
                    f"execution eligibility audit append failed: {audit.reason}"
                )
            decision = ExecutionDecision(
                execution_decision_id=execution_decision_id,
                execution_request_id=request.execution_request_id,
                request_id=request.request_id,
                outcome=outcome,
                eligible=outcome is ExecutionOutcome.ELIGIBLE,
                reason=reason,
                evidence=evidence,
                evidence_hash=evidence_hash,
                decided_at=_timestamp(now),
                audit_event_id=audit_event_id,
            )
            self._cache[decision_hash] = decision
            return decision

    @staticmethod
    def _validate_runtime_decision(
        request: ExecutionRequest,
        decision: RuntimeTransitionDecision,
    ) -> None:
        if not isinstance(decision, RuntimeTransitionDecision):
            raise ExecutionControlValidationError(
                "runtime_decision must be a RuntimeTransitionDecision"
            )
        if (
            request.request_id != decision.request_id
            or request.runtime_transition_decision_id
            != decision.transition_decision_id
        ):
            raise ExecutionControlValidationError(
                "execution request does not match runtime decision"
            )
        if decision.audit_event_id not in request.audit_references:
            raise ExecutionControlValidationError(
                "runtime transition audit reference is required"
            )

    def _utc_now(self) -> datetime:
        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise ExecutionControlValidationError(
                "execution control clock must be timezone-aware"
            )
        return now.astimezone(timezone.utc)


def validate_execution_request(request: ExecutionRequest) -> None:
    if not isinstance(request, ExecutionRequest):
        raise ExecutionControlValidationError("request must be an ExecutionRequest")
    for field_name in (
        "execution_request_id",
        "request_id",
        "runtime_transition_decision_id",
        "actor_id",
        "action",
        "resource",
        "requested_at",
    ):
        value = getattr(request, field_name)
        if not isinstance(value, str) or not value:
            raise ExecutionControlValidationError(f"{field_name} must be non-empty")
    if not isinstance(request.constraint, ExecutionConstraint):
        raise ExecutionControlValidationError("constraint must be canonical")
    _validate_constraint(request.constraint)
    for field_name in (
        "authority_evidence",
        "refusal_evidence",
        "escalation_evidence",
        "review_evidence",
        "override_evidence",
        "evidence",
    ):
        value = getattr(request, field_name)
        if not isinstance(value, Mapping):
            raise ExecutionControlValidationError(
                f"{field_name} must be a canonical JSON object"
            )
        try:
            canonical_json_text(value)
        except (CanonicalDataError, TypeError, ValueError) as exc:
            raise ExecutionControlValidationError(
                f"{field_name} is not canonical JSON: {exc}"
            ) from exc
    if not request.evidence:
        raise ExecutionControlValidationError("evidence must not be empty")
    _validate_references(request.audit_references)
    _parse_utc(request.requested_at, "requested_at")


def _validate_constraint(constraint: ExecutionConstraint) -> None:
    if not isinstance(constraint.constraint_id, str) or not constraint.constraint_id:
        raise ExecutionControlValidationError("constraint_id must be non-empty")
    if constraint.required_state is not RuntimeState.READY:
        raise ExecutionControlValidationError("execution required_state must be READY")
    if not isinstance(constraint.execution_enabled, bool):
        raise ExecutionControlValidationError("execution_enabled must be boolean")
    for field_name in (
        "require_refusal_evidence",
        "require_escalation_evidence",
        "require_review_evidence",
        "require_override_evidence",
    ):
        if not isinstance(getattr(constraint, field_name), bool):
            raise ExecutionControlValidationError(f"{field_name} must be boolean")
    _parse_utc(constraint.expires_at, "expires_at")


def _validate_constraints(
    constraints: Sequence[ExecutionConstraint],
) -> dict[str, ExecutionConstraint]:
    if not isinstance(constraints, (list, tuple)):
        raise ExecutionControlValidationError("constraints must be ordered")
    result: dict[str, ExecutionConstraint] = {}
    for constraint in constraints:
        if not isinstance(constraint, ExecutionConstraint):
            raise ExecutionControlValidationError(
                "configured constraint must be canonical"
            )
        _validate_constraint(constraint)
        if constraint.constraint_id in result:
            raise ExecutionControlValidationError(
                "constraint_id must be unique"
            )
        result[constraint.constraint_id] = constraint
    return result


def _classify(
    request: ExecutionRequest,
    decision: RuntimeTransitionDecision,
    now: datetime,
) -> tuple[ExecutionOutcome, str]:
    if not decision.allowed:
        return ExecutionOutcome.BLOCKED, "runtime_transition_rejected"
    if decision.next_state is RuntimeState.HALTED:
        return ExecutionOutcome.HALTED, "runtime_halted"
    if decision.next_state is RuntimeState.EXPIRED:
        return ExecutionOutcome.EXPIRED, "runtime_expired"
    expires_at = _parse_utc(request.constraint.expires_at, "expires_at")
    requested_at = _parse_utc(request.requested_at, "requested_at")
    if expires_at <= now or expires_at <= requested_at:
        return ExecutionOutcome.EXPIRED, "execution_constraint_expired"
    if (
        not request.constraint.execution_enabled
        or decision.next_state is RuntimeState.EXECUTION_BLOCKED
    ):
        return ExecutionOutcome.BLOCKED, "execution_blocked"
    if decision.next_state is not RuntimeState.READY:
        return ExecutionOutcome.INVALID_STATE, "runtime_not_ready"
    if not _evidence_has(
        request.authority_evidence,
        "authority_reference",
        "authority_evidence_hash",
    ):
        return ExecutionOutcome.MISSING_AUTHORITY, "authority_evidence_missing"
    required_evidence = (
        (
            request.constraint.require_refusal_evidence,
            request.refusal_evidence,
            ("refusal_decision_id", "refusal_evidence_hash"),
        ),
        (
            request.constraint.require_escalation_evidence,
            request.escalation_evidence,
            ("escalation_decision_id", "escalation_evidence_hash"),
        ),
        (
            request.constraint.require_review_evidence,
            request.review_evidence,
            ("review_decision_id", "review_evidence_hash"),
        ),
        (
            request.constraint.require_override_evidence,
            request.override_evidence,
            ("override_decision_id", "override_evidence_hash"),
        ),
    )
    if any(required and not _evidence_has(evidence, *keys) for required, evidence, keys in required_evidence):
        return ExecutionOutcome.MISSING_EVIDENCE, "required_evidence_missing"
    return ExecutionOutcome.ELIGIBLE, "execution_eligible"


def _evidence_has(evidence: Mapping[str, object], *keys: str) -> bool:
    return all(isinstance(evidence.get(key), str) and evidence.get(key) for key in keys)


def _optional_hash(evidence: Mapping[str, object]) -> str | None:
    return canonical_sha256(evidence) if evidence else None


def _validate_references(references: object) -> None:
    if not isinstance(references, tuple):
        raise ExecutionControlValidationError("audit_references must be a tuple")
    if any(not isinstance(item, str) or not item for item in references):
        raise ExecutionControlValidationError(
            "audit_references entries must be non-empty strings"
        )
    if len(set(references)) != len(references):
        raise ExecutionControlValidationError(
            "audit_references entries must be unique"
        )


def _parse_utc(value: str, field_name: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ExecutionControlValidationError(f"{field_name} must be non-empty")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ExecutionControlValidationError(
            f"{field_name} must be ISO 8601"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ExecutionControlValidationError(
            f"{field_name} must be timezone-aware"
        )
    if parsed.utcoffset().total_seconds() != 0:
        raise ExecutionControlValidationError(f"{field_name} must be UTC")
    return parsed.astimezone(timezone.utc)


def _timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
