"""In-memory current-state and currentness foundation for SAL-22.

This module implements only deterministic in-process state snapshots,
compare-and-set application of already validated transitions, append-only
application history, and validation-only currentness results. It is not a
production persistence adapter or execution runtime.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from threading import RLock

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.canonical import canonical_sha256
from echoauth.models import AuditAppendState, AuditRecord
from echoauth.runtime.state_machine import RUNTIME_STATE_GRAPH_VERSION
from echoauth.runtime.state_models import RuntimeState, RuntimeTransitionDecision

# The current-state foundation preserves the exact Sprint 2L state namespace.
# A separate repository-format namespace is intentionally not invented here.
RUNTIME_CURRENT_STATE_VERSION = RUNTIME_STATE_GRAPH_VERSION


class RuntimeStateCurrentnessError(ValueError):
    """Raised when compact current-state evidence cannot advance safely."""


class RuntimeStateCurrentnessAuditError(RuntimeError):
    """Raised when required current-state audit evidence cannot append."""


class RuntimeCurrentStateNotFoundError(LookupError):
    """Raised when no explicit current-state record exists for a request."""


@dataclass(frozen=True)
class RuntimeCurrentStateRecord:
    state_record_id: str
    request_id: str
    state_namespace: str
    graph_version: str
    current_state: RuntimeState
    state_revision: int
    last_applied_transition_decision_id: str | None
    last_applied_transition_evidence_hash: str | None
    updated_at: str
    evidence_hash: str
    audit_event_id: str


@dataclass(frozen=True)
class RuntimeStateApplicationResult:
    application_id: str
    request_id: str
    prior_state: RuntimeState
    prior_revision: int
    prior_state_record_hash: str
    transition_decision_id: str
    transition_evidence_hash: str
    resulting_state: RuntimeState
    resulting_revision: int
    resulting_state_record_hash: str
    applied_at: str
    audit_event_id: str


@dataclass(frozen=True)
class RuntimeDecisionCurrentnessResult:
    currentness_result_id: str
    transition_decision_id: str
    request_id: str
    current: bool
    current_state: RuntimeState | None
    current_revision: int | None
    current_state_record_hash: str | None
    reason: str
    validated_at: str
    evidence_hash: str
    audit_event_id: str


class InMemoryRuntimeCurrentStateRepository:
    """Authoritative only within one in-process SAL-22 test/runtime foundation."""

    def __init__(
        self,
        audit_repository: InMemoryAuditLogRepository,
        *,
        audit_chain_id: str,
        component_id: str = "runtime_current_state_repository",
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if not audit_chain_id:
            raise ValueError("audit_chain_id must not be empty")
        self._audit_repository = audit_repository
        self._audit_chain_id = audit_chain_id
        self._component_id = component_id
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._current: dict[str, RuntimeCurrentStateRecord] = {}
        self._history: dict[str, list[RuntimeStateApplicationResult]] = {}
        self._applications: dict[str, RuntimeStateApplicationResult] = {}
        self._lock = RLock()

    def register_initial(
        self,
        *,
        request_id: str,
        state: RuntimeState,
        actor_id: str,
        occurred_at: str | None = None,
    ) -> RuntimeCurrentStateRecord:
        """Explicitly register revision zero; no default initial state is inferred."""

        if not isinstance(request_id, str) or not request_id:
            raise RuntimeStateCurrentnessError("request_id must be non-empty")
        if not isinstance(actor_id, str) or not actor_id:
            raise RuntimeStateCurrentnessError("actor_id must be non-empty")
        if not isinstance(state, RuntimeState):
            raise RuntimeStateCurrentnessError("initial state must be canonical")
        timestamp = _timestamp(_parse_or_now(occurred_at, self._clock))
        base = {
            "current_state": state.value,
            "graph_version": RUNTIME_STATE_GRAPH_VERSION,
            "last_applied_transition_decision_id": None,
            "last_applied_transition_evidence_hash": None,
            "request_id": request_id,
            "state_namespace": RUNTIME_CURRENT_STATE_VERSION,
            "state_revision": 0,
            "updated_at": timestamp,
        }
        evidence_hash = canonical_sha256(base)
        state_record_id = f"rstate_{evidence_hash}"
        audit_event_id = f"audit_{state_record_id}"
        record = RuntimeCurrentStateRecord(
            state_record_id=state_record_id,
            request_id=request_id,
            state_namespace=RUNTIME_CURRENT_STATE_VERSION,
            graph_version=RUNTIME_STATE_GRAPH_VERSION,
            current_state=state,
            state_revision=0,
            last_applied_transition_decision_id=None,
            last_applied_transition_evidence_hash=None,
            updated_at=timestamp,
            evidence_hash=evidence_hash,
            audit_event_id=audit_event_id,
        )
        with self._lock:
            existing = self._current.get(request_id)
            if existing is not None:
                if existing == record:
                    return existing
                raise RuntimeStateCurrentnessError(
                    "initial state already registered"
                )
            audit = self._audit_repository.append(
                AuditRecord(
                    event_type="runtime.state.initialized",
                    actor_id=actor_id,
                    request_id=request_id,
                    state_after=state.value,
                    reason="runtime_initial_state_registered",
                    details={
                        "evidence_hash": evidence_hash,
                        "state_record_id": state_record_id,
                        "state_revision": 0,
                    },
                    occurred_at=timestamp,
                ),
                audit_event_id=audit_event_id,
                chain_id=self._audit_chain_id,
            )
            if audit.append_state is not AuditAppendState.ACCEPTED:
                raise RuntimeStateCurrentnessAuditError(
                    f"initial-state audit append failed: {audit.reason}"
                )
            self._current[request_id] = record
            self._history[request_id] = []
            return record

    def get(self, request_id: str) -> RuntimeCurrentStateRecord:
        with self._lock:
            try:
                return self._current[request_id]
            except KeyError as exc:
                raise RuntimeCurrentStateNotFoundError(request_id) from exc

    def history(self, request_id: str) -> tuple[RuntimeStateApplicationResult, ...]:
        with self._lock:
            return tuple(self._history.get(request_id, ()))

    def application_for(
        self, transition_decision_id: str
    ) -> RuntimeStateApplicationResult | None:
        with self._lock:
            return self._applications.get(transition_decision_id)

    def apply(
        self,
        decision: RuntimeTransitionDecision,
        *,
        expected_revision: int,
        actor_id: str,
        applied_at: str | None = None,
    ) -> RuntimeStateApplicationResult:
        """Atomically apply one already validated transition in process."""

        _validate_transition_decision(decision)
        if not decision.allowed:
            raise RuntimeStateCurrentnessError("transition_decision_not_allowed")
        if not isinstance(expected_revision, int) or expected_revision < 0:
            raise RuntimeStateCurrentnessError(
                "expected_revision must be non-negative"
            )
        if not isinstance(actor_id, str) or not actor_id:
            raise RuntimeStateCurrentnessError("actor_id must be non-empty")
        timestamp = _timestamp(_parse_or_now(applied_at, self._clock))

        with self._lock:
            current = self._current.get(decision.request_id)
            if current is None:
                raise RuntimeCurrentStateNotFoundError(decision.request_id)
            prior_application = self._applications.get(
                decision.transition_decision_id
            )
            if prior_application is not None:
                if (
                    current.state_revision == prior_application.resulting_revision
                    and current.evidence_hash
                    == prior_application.resulting_state_record_hash
                    and current.last_applied_transition_decision_id
                    == decision.transition_decision_id
                ):
                    return prior_application
                raise RuntimeStateCurrentnessError(
                    "transition_decision_superseded"
                )
            if expected_revision != current.state_revision:
                raise RuntimeStateCurrentnessError("expected_revision_mismatch")
            if decision.evidence.graph_version != current.graph_version:
                raise RuntimeStateCurrentnessError("graph_version_mismatch")
            if decision.current_state is not current.current_state:
                raise RuntimeStateCurrentnessError("authoritative_state_mismatch")
            if not decision.audit_event_id:
                raise RuntimeStateCurrentnessError(
                    "transition_decision_audit_missing"
                )

            resulting_revision = current.state_revision + 1
            state_base = {
                "current_state": decision.next_state.value,
                "graph_version": current.graph_version,
                "last_applied_transition_decision_id": (
                    decision.transition_decision_id
                ),
                "last_applied_transition_evidence_hash": decision.evidence_hash,
                "request_id": decision.request_id,
                "state_namespace": current.state_namespace,
                "state_revision": resulting_revision,
                "updated_at": timestamp,
            }
            resulting_state_hash = canonical_sha256(state_base)
            state_record_id = f"rstate_{resulting_state_hash}"
            application_base = {
                "applied_at": timestamp,
                "prior_revision": current.state_revision,
                "prior_state": current.current_state.value,
                "prior_state_record_hash": current.evidence_hash,
                "request_id": decision.request_id,
                "resulting_revision": resulting_revision,
                "resulting_state": decision.next_state.value,
                "resulting_state_record_hash": resulting_state_hash,
                "transition_decision_id": decision.transition_decision_id,
                "transition_evidence_hash": decision.evidence_hash,
            }
            application_hash = canonical_sha256(application_base)
            application_id = f"rapply_{application_hash}"
            audit_event_id = f"audit_{application_id}"
            next_record = RuntimeCurrentStateRecord(
                state_record_id=state_record_id,
                request_id=decision.request_id,
                state_namespace=current.state_namespace,
                graph_version=current.graph_version,
                current_state=decision.next_state,
                state_revision=resulting_revision,
                last_applied_transition_decision_id=(
                    decision.transition_decision_id
                ),
                last_applied_transition_evidence_hash=decision.evidence_hash,
                updated_at=timestamp,
                evidence_hash=resulting_state_hash,
                audit_event_id=audit_event_id,
            )
            application = RuntimeStateApplicationResult(
                application_id=application_id,
                request_id=decision.request_id,
                prior_state=current.current_state,
                prior_revision=current.state_revision,
                prior_state_record_hash=current.evidence_hash,
                transition_decision_id=decision.transition_decision_id,
                transition_evidence_hash=decision.evidence_hash,
                resulting_state=decision.next_state,
                resulting_revision=resulting_revision,
                resulting_state_record_hash=resulting_state_hash,
                applied_at=timestamp,
                audit_event_id=audit_event_id,
            )
            audit = self._audit_repository.append(
                AuditRecord(
                    event_type="runtime.state.application",
                    actor_id=actor_id,
                    request_id=decision.request_id,
                    state_before=current.current_state.value,
                    state_after=decision.next_state.value,
                    reason="runtime_transition_applied",
                    details={
                        "application_id": application_id,
                        "expected_revision": expected_revision,
                        "resulting_revision": resulting_revision,
                        "resulting_state_record_id": state_record_id,
                        "resulting_state_record_hash": resulting_state_hash,
                        "transition_decision_id": (
                            decision.transition_decision_id
                        ),
                        "transition_evidence_hash": decision.evidence_hash,
                    },
                    occurred_at=timestamp,
                ),
                audit_event_id=audit_event_id,
                chain_id=self._audit_chain_id,
            )
            if audit.append_state is not AuditAppendState.ACCEPTED:
                raise RuntimeStateCurrentnessAuditError(
                    f"state-application audit append failed: {audit.reason}"
                )
            self._current[decision.request_id] = next_record
            self._history.setdefault(decision.request_id, []).append(application)
            self._applications[decision.transition_decision_id] = application
            return application


class RuntimeDecisionCurrentnessService:
    """Validate whether one applied transition decision is the current revision."""

    def __init__(
        self,
        repository: InMemoryRuntimeCurrentStateRepository,
        audit_repository: InMemoryAuditLogRepository,
        *,
        audit_chain_id: str,
        component_id: str = "runtime_decision_currentness_service",
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if not isinstance(repository, InMemoryRuntimeCurrentStateRepository):
            raise TypeError(
                "repository must be InMemoryRuntimeCurrentStateRepository"
            )
        if not audit_chain_id:
            raise ValueError("audit_chain_id must not be empty")
        self._repository = repository
        self._audit_repository = audit_repository
        self._audit_chain_id = audit_chain_id
        self._component_id = component_id
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._cache: dict[str, RuntimeDecisionCurrentnessResult] = {}
        self._lock = RLock()

    def validate(
        self, decision: RuntimeTransitionDecision
    ) -> RuntimeDecisionCurrentnessResult:
        _validate_transition_decision(decision)
        try:
            current_record = self._repository.get(decision.request_id)
        except RuntimeCurrentStateNotFoundError:
            return self._complete(
                decision,
                current_record=None,
                current=False,
                reason="current_state_not_found",
            )
        application = self._repository.application_for(
            decision.transition_decision_id
        )
        if not decision.allowed:
            current, reason = False, "transition_decision_not_allowed"
        elif decision.evidence.graph_version != current_record.graph_version:
            current, reason = False, "graph_version_mismatch"
        elif application is None:
            current, reason = False, "transition_decision_never_applied"
        elif (
            current_record.last_applied_transition_decision_id
            != decision.transition_decision_id
        ):
            current, reason = False, "transition_decision_superseded"
        elif (
            current_record.last_applied_transition_evidence_hash
            != decision.evidence_hash
        ):
            current, reason = False, "transition_evidence_hash_mismatch"
        elif current_record.current_state is not decision.next_state:
            current, reason = False, "current_state_mismatch"
        elif (
            application.resulting_revision != current_record.state_revision
            or application.resulting_state_record_hash
            != current_record.evidence_hash
        ):
            current, reason = False, "application_history_mismatch"
        else:
            current, reason = True, "runtime_transition_decision_current"
        return self._complete(
            decision,
            current_record=current_record,
            current=current,
            reason=reason,
        )

    def _complete(
        self,
        decision: RuntimeTransitionDecision,
        *,
        current_record: RuntimeCurrentStateRecord | None,
        current: bool,
        reason: str,
    ) -> RuntimeDecisionCurrentnessResult:
        evidence = {
            "current": current,
            "current_revision": (
                current_record.state_revision if current_record else None
            ),
            "current_state": (
                current_record.current_state.value if current_record else None
            ),
            "current_state_record_hash": (
                current_record.evidence_hash if current_record else None
            ),
            "decision_evidence_hash": decision.evidence_hash,
            "graph_version": decision.evidence.graph_version,
            "reason": reason,
            "request_id": decision.request_id,
            "transition_decision_id": decision.transition_decision_id,
        }
        evidence_hash = canonical_sha256(evidence)
        result_id = f"rcur_{evidence_hash}"
        with self._lock:
            cached = self._cache.get(result_id)
            if cached is not None:
                return cached
            validated_at = _timestamp(_utc_now(self._clock))
            audit_event_id = f"audit_{result_id}"
            audit = self._audit_repository.append(
                AuditRecord(
                    event_type="runtime.state.currentness.validation",
                    actor_id=self._component_id,
                    request_id=decision.request_id,
                    state_after=(
                        current_record.current_state.value
                        if current_record
                        else None
                    ),
                    reason=reason,
                    details={
                        "current": current,
                        "current_revision": (
                            current_record.state_revision
                            if current_record
                            else None
                        ),
                        "currentness_result_id": result_id,
                        "evidence_hash": evidence_hash,
                        "transition_decision_id": (
                            decision.transition_decision_id
                        ),
                    },
                    occurred_at=validated_at,
                ),
                audit_event_id=audit_event_id,
                chain_id=self._audit_chain_id,
            )
            if audit.append_state is not AuditAppendState.ACCEPTED:
                raise RuntimeStateCurrentnessAuditError(
                    f"currentness audit append failed: {audit.reason}"
                )
            result = RuntimeDecisionCurrentnessResult(
                currentness_result_id=result_id,
                transition_decision_id=decision.transition_decision_id,
                request_id=decision.request_id,
                current=current,
                current_state=(
                    current_record.current_state if current_record else None
                ),
                current_revision=(
                    current_record.state_revision if current_record else None
                ),
                current_state_record_hash=(
                    current_record.evidence_hash if current_record else None
                ),
                reason=reason,
                validated_at=validated_at,
                evidence_hash=evidence_hash,
                audit_event_id=audit_event_id,
            )
            self._cache[result_id] = result
            return result


def _validate_transition_decision(decision: RuntimeTransitionDecision) -> None:
    if not isinstance(decision, RuntimeTransitionDecision):
        raise RuntimeStateCurrentnessError(
            "decision must be RuntimeTransitionDecision"
        )
    if not isinstance(decision.request_id, str) or not decision.request_id:
        raise RuntimeStateCurrentnessError("decision request_id must be non-empty")
    if not isinstance(decision.transition_decision_id, str) or not decision.transition_decision_id:
        raise RuntimeStateCurrentnessError(
            "transition_decision_id must be non-empty"
        )
    if not isinstance(decision.current_state, RuntimeState):
        raise RuntimeStateCurrentnessError("decision current_state must be canonical")
    if not isinstance(decision.next_state, RuntimeState):
        raise RuntimeStateCurrentnessError("decision next_state must be canonical")
    if decision.evidence.graph_version != RUNTIME_STATE_GRAPH_VERSION:
        raise RuntimeStateCurrentnessError("decision graph version is not canonical")


def _parse_or_now(
    value: str | None, clock: Callable[[], datetime]
) -> datetime:
    if value is None:
        return _utc_now(clock)
    if not isinstance(value, str) or not value:
        raise RuntimeStateCurrentnessError("timestamp must be non-empty")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise RuntimeStateCurrentnessError("timestamp must be ISO 8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise RuntimeStateCurrentnessError("timestamp must be timezone-aware")
    if parsed.utcoffset().total_seconds() != 0:
        raise RuntimeStateCurrentnessError("timestamp must be UTC")
    return parsed.astimezone(timezone.utc)


def _utc_now(clock: Callable[[], datetime]) -> datetime:
    now = clock()
    if now.tzinfo is None or now.utcoffset() is None:
        raise RuntimeStateCurrentnessError("clock must be timezone-aware")
    return now.astimezone(timezone.utc)


def _timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
