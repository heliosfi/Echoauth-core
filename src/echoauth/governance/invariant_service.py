"""Versioned deterministic Invariant Validator for Sprint 2N."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from datetime import datetime, timezone
from threading import RLock

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.canonical import CanonicalDataError, canonical_json_text, canonical_sha256
from echoauth.governance.invariant_models import (
    InvariantFailureState,
    InvariantResult,
    InvariantResultState,
    InvariantRule,
    InvariantSet,
    InvariantValidationRequest,
)
from echoauth.models import AuditAppendState, AuditRecord

INVARIANT_VALIDATOR_VERSION = "echoauth.invariant-validator.v1"


class InvariantValidationError(ValueError):
    pass


class InvariantAuditError(RuntimeError):
    pass


class InvariantService:
    """Evaluate immutable versioned invariant definitions without side effects."""

    def __init__(
        self,
        audit_repository: InMemoryAuditLogRepository,
        *,
        audit_chain_id: str,
        invariant_sets: Sequence[InvariantSet],
        component_id: str = "invariant_service",
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if not audit_chain_id:
            raise ValueError("audit_chain_id must not be empty")
        self._sets = _validate_sets(invariant_sets)
        self._audit_repository = audit_repository
        self._audit_chain_id = audit_chain_id
        self._component_id = component_id
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._cache: dict[str, InvariantResult] = {}
        self._lock = RLock()

    def validate(self, request: InvariantValidationRequest) -> InvariantResult:
        """Validate canonical facts against one explicitly pinned invariant set."""

        validate_invariant_request(request)
        facts_hash = canonical_sha256(request.facts)
        invariant_set = self._sets.get(request.invariant_version)
        if invariant_set is None:
            state = InvariantResultState.HOLD
            failed: tuple[str, ...] = ()
            reason = "invariant_version_unknown"
            definition_hash = None
            evaluation_order: tuple[str, ...] = ()
        elif not invariant_set.active:
            state = InvariantResultState.HOLD
            failed = ()
            reason = "invariant_version_inactive"
            definition_hash = _definition_hash(invariant_set)
            evaluation_order = tuple(rule.invariant_id for rule in invariant_set.rules)
        else:
            state, failed, reason = _evaluate(invariant_set, request.facts)
            definition_hash = _definition_hash(invariant_set)
            evaluation_order = tuple(rule.invariant_id for rule in invariant_set.rules)

        result_hash = canonical_sha256(
            {
                "definition_hash": definition_hash,
                "facts_hash": facts_hash,
                "failed_invariants": list(failed),
                "invariant_version": request.invariant_version,
                "reason": reason,
                "request_id": request.request_id,
                "runtime_state": request.runtime_state,
                "state": state.value,
                "validation_id": request.validation_id,
                "envelope_id": request.envelope_id,
                "validator_version": INVARIANT_VALIDATOR_VERSION,
            }
        )
        with self._lock:
            cached = self._cache.get(result_hash)
            if cached is not None:
                return cached
            now = self._utc_now()
            invariant_result_id = f"invres_{result_hash}"
            audit_event_id = f"audit_{invariant_result_id}"
            audit = self._audit_repository.append(
                AuditRecord(
                    event_type="invariant.result",
                    actor_id=self._component_id,
                    request_id=request.request_id,
                    reason=reason,
                    details={
                        "definition_hash": definition_hash,
                        "evaluation_order": list(evaluation_order),
                        "facts_hash": facts_hash,
                        "failed_invariants": list(failed),
                        "invariant_result_id": invariant_result_id,
                        "invariant_version": request.invariant_version,
                        "runtime_state": request.runtime_state,
                        "state": state.value,
                        "validator_version": INVARIANT_VALIDATOR_VERSION,
                    },
                    occurred_at=_timestamp(now),
                ),
                audit_event_id=audit_event_id,
                chain_id=self._audit_chain_id,
            )
            if audit.append_state is not AuditAppendState.ACCEPTED:
                raise InvariantAuditError(
                    f"invariant result audit append failed: {audit.reason}"
                )
            result = InvariantResult(
                invariant_result_id=invariant_result_id,
                validation_id=request.validation_id,
                request_id=request.request_id,
                invariant_version=request.invariant_version,
                state=state,
                failed_invariants=failed,
                reason=reason,
                facts_hash=facts_hash,
                definition_hash=definition_hash,
                evaluation_order=evaluation_order,
                evaluated_at=_timestamp(now),
                envelope_id=request.envelope_id,
                audit_event_id=audit_event_id,
            )
            self._cache[result_hash] = result
            return result

    def _utc_now(self) -> datetime:
        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise InvariantValidationError("invariant clock must be timezone-aware")
        return now.astimezone(timezone.utc)


def validate_invariant_request(request: InvariantValidationRequest) -> None:
    if not isinstance(request, InvariantValidationRequest):
        raise InvariantValidationError(
            "request must be an InvariantValidationRequest"
        )
    for field_name in (
        "validation_id",
        "request_id",
        "invariant_version",
        "runtime_state",
    ):
        value = getattr(request, field_name)
        if not isinstance(value, str) or not value:
            raise InvariantValidationError(f"{field_name} must be non-empty")
    if request.envelope_id is not None and (
        not isinstance(request.envelope_id, str) or not request.envelope_id
    ):
        raise InvariantValidationError("envelope_id must be non-empty when present")
    if not isinstance(request.facts, Mapping):
        raise InvariantValidationError("facts must be a canonical JSON object")
    try:
        canonical_json_text(request.facts)
    except (CanonicalDataError, TypeError, ValueError) as exc:
        raise InvariantValidationError(f"facts are not canonical JSON: {exc}") from exc


def _validate_sets(
    invariant_sets: Sequence[InvariantSet],
) -> dict[str, InvariantSet]:
    if not isinstance(invariant_sets, (list, tuple)):
        raise InvariantValidationError("invariant_sets must be ordered")
    result: dict[str, InvariantSet] = {}
    for invariant_set in invariant_sets:
        if not isinstance(invariant_set, InvariantSet):
            raise InvariantValidationError("invariant set must be canonical")
        if not invariant_set.invariant_version:
            raise InvariantValidationError("invariant_version must be non-empty")
        if not isinstance(invariant_set.active, bool):
            raise InvariantValidationError("invariant set active must be boolean")
        if not isinstance(invariant_set.rules, tuple) or not invariant_set.rules:
            raise InvariantValidationError("invariant rules must be a non-empty tuple")
        if invariant_set.invariant_version in result:
            raise InvariantValidationError("invariant_version must be unique")
        rule_ids: set[str] = set()
        frozen_rules: list[InvariantRule] = []
        for rule in invariant_set.rules:
            if not isinstance(rule, InvariantRule):
                raise InvariantValidationError("invariant rule must be canonical")
            if not rule.invariant_id or not rule.fact_key:
                raise InvariantValidationError("invariant rule fields must be non-empty")
            if rule.invariant_id in rule_ids:
                raise InvariantValidationError("invariant_id must be unique per set")
            if not isinstance(rule.failure_state, InvariantFailureState):
                raise InvariantValidationError("failure_state must be canonical")
            try:
                canonical_sha256({"expected_value": rule.expected_value})
            except (CanonicalDataError, TypeError, ValueError) as exc:
                raise InvariantValidationError(
                    f"expected_value is not canonical JSON: {exc}"
                ) from exc
            rule_ids.add(rule.invariant_id)
            frozen_rules.append(
                InvariantRule(
                    invariant_id=rule.invariant_id,
                    fact_key=rule.fact_key,
                    expected_value=_freeze_value(rule.expected_value),
                    failure_state=rule.failure_state,
                )
            )
        frozen_set = InvariantSet(
            invariant_version=invariant_set.invariant_version,
            active=invariant_set.active,
            rules=tuple(frozen_rules),
        )
        result[frozen_set.invariant_version] = frozen_set
    return result


def _evaluate(
    invariant_set: InvariantSet,
    facts: Mapping[str, object],
) -> tuple[InvariantResultState, tuple[str, ...], str]:
    missing: list[str] = []
    invalid: list[str] = []
    halted: list[str] = []
    for rule in invariant_set.rules:
        if rule.fact_key not in facts:
            missing.append(rule.invariant_id)
            continue
        actual_hash = canonical_sha256({"value": facts[rule.fact_key]})
        expected_hash = canonical_sha256({"value": rule.expected_value})
        if actual_hash != expected_hash:
            if rule.failure_state is InvariantFailureState.HALT:
                halted.append(rule.invariant_id)
            else:
                invalid.append(rule.invariant_id)
    failed = tuple(
        rule.invariant_id
        for rule in invariant_set.rules
        if rule.invariant_id in {*missing, *invalid, *halted}
    )
    if halted:
        return InvariantResultState.HALT, failed, "critical_invariant_failed"
    if invalid:
        return InvariantResultState.INVALID, failed, "invariant_failed"
    if missing:
        return InvariantResultState.HOLD, failed, "required_fact_missing"
    return InvariantResultState.VALID, (), "invariants_valid"


def _definition_hash(invariant_set: InvariantSet) -> str:
    return canonical_sha256(
        {
            "active": invariant_set.active,
            "invariant_version": invariant_set.invariant_version,
            "rules": [
                {
                    "expected_value": rule.expected_value,
                    "fact_key": rule.fact_key,
                    "failure_state": rule.failure_state.value,
                    "invariant_id": rule.invariant_id,
                }
                for rule in invariant_set.rules
            ],
            "validator_version": INVARIANT_VALIDATOR_VERSION,
        }
    )


class _FrozenDict(dict[str, object]):
    def _immutable(self, *args: object, **kwargs: object) -> None:
        raise TypeError("invariant definition is immutable")

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    pop = _immutable
    popitem = _immutable
    setdefault = _immutable
    update = _immutable


def _freeze_value(value: object) -> object:
    if isinstance(value, Mapping):
        return _FrozenDict({key: _freeze_value(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_value(item) for item in value)
    return value


def _timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
