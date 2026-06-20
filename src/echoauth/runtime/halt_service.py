"""Deterministic, evidence-only Halt Decision service for Sprint 2O."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import asdict
from datetime import datetime, timezone
from threading import RLock

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.canonical import CanonicalDataError, canonical_json_text, canonical_sha256
from echoauth.models import AuditAppendState, AuditRecord
from echoauth.runtime.halt_models import (
    HaltCause,
    HaltDecision,
    HaltDecisionEvidence,
    HaltOutcome,
    HaltRequest,
    HaltSeverity,
)

HALT_CLASSIFIER_VERSION = "echoauth.halt-decision.v1"


class HaltValidationError(ValueError):
    pass


class HaltAuditError(RuntimeError):
    pass


class HaltDecisionService:
    """Classify supplied safety evidence without changing runtime state."""

    def __init__(
        self,
        audit_repository: InMemoryAuditLogRepository,
        *,
        audit_chain_id: str,
        component_id: str = "halt_decision_service",
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if not audit_chain_id:
            raise ValueError("audit_chain_id must not be empty")
        self._audit_repository = audit_repository
        self._audit_chain_id = audit_chain_id
        self._component_id = component_id
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._cache: dict[str, HaltDecision] = {}
        self._lock = RLock()

    def decide(self, request: HaltRequest) -> HaltDecision:
        """Validate and classify one halt request as immutable evidence."""

        validate_halt_request(request)
        outcome, reason = _classify(request)
        required_reviewer = (
            request.evidence.get("required_reviewer")
            if outcome is HaltOutcome.ESCALATED
            else None
        )
        source_references = _source_references(request.evidence)
        decision_evidence = HaltDecisionEvidence(
            classifier_version=HALT_CLASSIFIER_VERSION,
            halt_event_id=request.halt_event_id,
            failure_type=request.failure_type,
            severity=request.severity,
            state_before=request.state_before,
            source_evidence_hash=canonical_sha256(request.evidence),
            source_references=source_references,
            occurred_at=request.occurred_at,
        )
        evidence_hash = canonical_sha256(asdict(decision_evidence))
        decision_hash = canonical_sha256(
            {
                "evidence_hash": evidence_hash,
                "outcome": outcome.value,
                "reason": reason,
                "request_id": request.request_id,
            }
        )
        with self._lock:
            cached = self._cache.get(decision_hash)
            if cached is not None:
                return cached
            now = self._utc_now()
            halt_decision_id = f"haltdec_{decision_hash}"
            audit_event_id = f"audit_{halt_decision_id}"
            audit = self._audit_repository.append(
                AuditRecord(
                    event_type="runtime.halt.decision",
                    actor_id=self._component_id,
                    request_id=request.request_id,
                    reason=reason,
                    details={
                        "classifier_version": HALT_CLASSIFIER_VERSION,
                        "detected_by": request.detected_by,
                        "evidence_hash": evidence_hash,
                        "failure_type": request.failure_type.value,
                        "halt_decision_id": halt_decision_id,
                        "halt_event_id": request.halt_event_id,
                        "outcome": outcome.value,
                        "recovery_allowed": outcome
                        in {HaltOutcome.HOLD, HaltOutcome.ESCALATED},
                        "severity": request.severity.value,
                        "state_before": request.state_before,
                    },
                    occurred_at=_timestamp(now),
                ),
                audit_event_id=audit_event_id,
                chain_id=self._audit_chain_id,
            )
            if audit.append_state is not AuditAppendState.ACCEPTED:
                raise HaltAuditError(f"halt decision audit append failed: {audit.reason}")
            decision = HaltDecision(
                halt_decision_id=halt_decision_id,
                halt_event_id=request.halt_event_id,
                request_id=request.request_id,
                runtime_state=outcome,
                reason=reason,
                recovery_allowed=outcome
                in {HaltOutcome.HOLD, HaltOutcome.ESCALATED},
                required_reviewer=(
                    str(required_reviewer) if required_reviewer is not None else None
                ),
                evidence=decision_evidence,
                evidence_hash=evidence_hash,
                decided_at=_timestamp(now),
                audit_event_id=audit_event_id,
            )
            self._cache[decision_hash] = decision
            return decision

    def _utc_now(self) -> datetime:
        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise HaltValidationError("halt decision clock must be timezone-aware")
        return now.astimezone(timezone.utc)


def validate_halt_request(request: HaltRequest) -> None:
    if not isinstance(request, HaltRequest):
        raise HaltValidationError("request must be a HaltRequest")
    for field_name in (
        "halt_event_id",
        "request_id",
        "detected_by",
        "state_before",
        "occurred_at",
    ):
        value = getattr(request, field_name)
        if not isinstance(value, str) or not value:
            raise HaltValidationError(f"{field_name} must be non-empty")
    for field_name in ("envelope_id", "execution_token_id"):
        value = getattr(request, field_name)
        if value is not None and (not isinstance(value, str) or not value):
            raise HaltValidationError(f"{field_name} must be non-empty when present")
    if not isinstance(request.failure_type, HaltCause):
        raise HaltValidationError("failure_type must be canonical")
    if not isinstance(request.severity, HaltSeverity):
        raise HaltValidationError("severity must be canonical")
    if not isinstance(request.evidence, Mapping) or not request.evidence:
        raise HaltValidationError(
            "evidence must be a non-empty canonical JSON object"
        )
    try:
        canonical_json_text(request.evidence)
    except (CanonicalDataError, TypeError, ValueError) as exc:
        raise HaltValidationError(f"evidence is not canonical JSON: {exc}") from exc
    _parse_utc(request.occurred_at)
    _validate_cause_evidence(request)


def _validate_cause_evidence(request: HaltRequest) -> None:
    evidence = request.evidence
    required = _REQUIRED_STRING_EVIDENCE[request.failure_type]
    for key in required:
        value = evidence.get(key)
        if not isinstance(value, str) or not value:
            raise HaltValidationError(
                f"{key} is required for {request.failure_type.value}"
            )
    if request.failure_type is HaltCause.MISSING_EVIDENCE:
        missing = evidence.get("missing_evidence")
        if (
            not isinstance(missing, (list, tuple))
            or not missing
            or any(not isinstance(item, str) or not item for item in missing)
        ):
            raise HaltValidationError(
                "missing_evidence must be a non-empty string list"
            )
    if request.failure_type is HaltCause.FAILED_INVARIANT and evidence.get(
        "invariant_state"
    ) not in {"invalid", "hold", "halt"}:
        raise HaltValidationError("failed invariant state must be invalid, hold, or halt")
    if request.failure_type is HaltCause.EXPIRED_DEPENDENCY and evidence.get(
        "dependency_status"
    ) != "expired":
        raise HaltValidationError("expired dependency status must be expired")
    if request.failure_type is HaltCause.INVALID_DEPENDENCY and evidence.get(
        "dependency_status"
    ) not in {"invalid", "revoked", "conflict"}:
        raise HaltValidationError(
            "invalid dependency status must be invalid, revoked, or conflict"
        )
    if request.failure_type is HaltCause.UNRESOLVED_OVERRIDE and evidence.get(
        "override_outcome"
    ) not in {"deferred", "unresolved"}:
        raise HaltValidationError(
            "unresolved override outcome must be deferred or unresolved"
        )
    if request.failure_type is HaltCause.UNSAFE_EXECUTION and evidence.get(
        "execution_outcome"
    ) not in {
        "blocked",
        "invalid_state",
        "missing_authority",
        "missing_evidence",
        "expired",
        "halted",
    }:
        raise HaltValidationError("unsafe execution outcome is not fail-closed")


def _classify(request: HaltRequest) -> tuple[HaltOutcome, str]:
    if request.severity is HaltSeverity.CRITICAL:
        return HaltOutcome.HALTED, "critical_failure"
    if request.failure_type is HaltCause.FAILED_INVARIANT:
        return {
            "halt": (HaltOutcome.HALTED, "critical_invariant_failed"),
            "invalid": (HaltOutcome.REFUSED, "invariant_invalid"),
            "hold": (HaltOutcome.HOLD, "invariant_evidence_incomplete"),
        }[str(request.evidence["invariant_state"])]
    return _CAUSE_CLASSIFICATION[request.failure_type]


def _source_references(evidence: Mapping[str, object]) -> tuple[str, ...]:
    references: list[str] = []
    for key in _REFERENCE_KEYS:
        value = evidence.get(key)
        if isinstance(value, str) and value:
            references.append(value)
    return tuple(references)


_REQUIRED_STRING_EVIDENCE = {
    HaltCause.MISSING_AUTHORITY: (
        "authority_check_id",
        "authority_evidence_hash",
        "authority_status",
    ),
    HaltCause.MISSING_EVIDENCE: ("source_evidence_hash",),
    HaltCause.INVALID_STATE: (
        "runtime_transition_decision_id",
        "runtime_transition_evidence_hash",
    ),
    HaltCause.FAILED_INVARIANT: (
        "invariant_result_id",
        "invariant_state",
        "facts_hash",
    ),
    HaltCause.EXPIRED_DEPENDENCY: (
        "dependency_id",
        "dependency_evidence_hash",
        "dependency_status",
    ),
    HaltCause.INVALID_DEPENDENCY: (
        "dependency_id",
        "dependency_evidence_hash",
        "dependency_status",
    ),
    HaltCause.UNRESOLVED_OVERRIDE: (
        "override_decision_id",
        "override_evidence_hash",
        "override_outcome",
        "required_reviewer",
    ),
    HaltCause.UNSAFE_EXECUTION: (
        "execution_decision_id",
        "execution_evidence_hash",
        "execution_outcome",
    ),
}

_CAUSE_CLASSIFICATION = {
    HaltCause.MISSING_AUTHORITY: (HaltOutcome.REFUSED, "authority_missing"),
    HaltCause.MISSING_EVIDENCE: (HaltOutcome.HOLD, "evidence_missing"),
    HaltCause.INVALID_STATE: (HaltOutcome.HALTED, "runtime_state_invalid"),
    HaltCause.EXPIRED_DEPENDENCY: (
        HaltOutcome.REFUSED,
        "dependency_expired",
    ),
    HaltCause.INVALID_DEPENDENCY: (
        HaltOutcome.REFUSED,
        "dependency_invalid",
    ),
    HaltCause.UNRESOLVED_OVERRIDE: (
        HaltOutcome.ESCALATED,
        "override_unresolved",
    ),
    HaltCause.UNSAFE_EXECUTION: (HaltOutcome.HALTED, "execution_unsafe"),
}

_REFERENCE_KEYS = (
    "authority_check_id",
    "runtime_transition_decision_id",
    "invariant_result_id",
    "dependency_id",
    "override_decision_id",
    "execution_decision_id",
    "required_reviewer",
)


def _parse_utc(value: str) -> datetime:
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise HaltValidationError("occurred_at must be ISO 8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise HaltValidationError("occurred_at must be timezone-aware")
    if parsed.utcoffset().total_seconds() != 0:
        raise HaltValidationError("occurred_at must be UTC")
    return parsed.astimezone(timezone.utc)


def _timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
