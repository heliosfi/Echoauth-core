"""Canonical invariant validation models for Sprint 2N."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class InvariantResultState(str, Enum):
    VALID = "valid"
    INVALID = "invalid"
    HOLD = "hold"
    HALT = "halt"


class InvariantFailureState(str, Enum):
    INVALID = "invalid"
    HALT = "halt"


@dataclass(frozen=True)
class InvariantRule:
    invariant_id: str
    fact_key: str
    expected_value: Any
    failure_state: InvariantFailureState


@dataclass(frozen=True)
class InvariantSet:
    invariant_version: str
    active: bool
    rules: tuple[InvariantRule, ...]


@dataclass(frozen=True)
class InvariantValidationRequest:
    validation_id: str
    request_id: str
    invariant_version: str
    runtime_state: str
    facts: Mapping[str, Any]
    envelope_id: str | None = None


@dataclass(frozen=True)
class InvariantResult:
    invariant_result_id: str
    validation_id: str
    request_id: str
    invariant_version: str
    state: InvariantResultState
    failed_invariants: tuple[str, ...]
    reason: str
    facts_hash: str
    definition_hash: str | None
    evaluation_order: tuple[str, ...]
    evaluated_at: str
    envelope_id: str | None = None
    audit_event_id: str | None = None
