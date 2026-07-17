"""Pure, deterministic, non-executing SniperBot FSM transition evaluator."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class State(str, Enum):
    PAUSE = "PAUSE"
    READY = "READY"
    ARMED_MANUAL = "ARMED_MANUAL"
    ARMED_AUTO = "ARMED_AUTO"
    IN_TRADE = "IN_TRADE"
    LOCKOUT = "LOCKOUT"


class TransitionRequestName(str, Enum):
    PAUSE_TO_READY = "PAUSE_TO_READY"
    READY_TO_ARMED_MANUAL = "READY_TO_ARMED_MANUAL"
    READY_TO_ARMED_AUTO = "READY_TO_ARMED_AUTO"
    ARMED_AUTO_TO_IN_TRADE = "ARMED_AUTO_TO_IN_TRADE"
    ARMED_MANUAL_TO_IN_TRADE = "ARMED_MANUAL_TO_IN_TRADE"
    IN_TRADE_TO_READY = "IN_TRADE_TO_READY"
    IN_TRADE_TO_PAUSE = "IN_TRADE_TO_PAUSE"
    ANY_TO_LOCKOUT = "ANY_TO_LOCKOUT"
    LOCKOUT_TO_PAUSE = "LOCKOUT_TO_PAUSE"


class ReasonCode(str, Enum):
    ALLOWED = "ALLOWED"
    UNDEFINED_TRANSITION = "UNDEFINED_TRANSITION"
    UNKNOWN_STATE = "UNKNOWN_STATE"
    READINESS_FACTS_MISSING = "READINESS_FACTS_MISSING"
    AUTHORITY_MISSING = "AUTHORITY_MISSING"
    AUTHORITY_INVALID = "AUTHORITY_INVALID"
    AUTHORITY_STALE = "AUTHORITY_STALE"
    AUTHORITY_REVOKED = "AUTHORITY_REVOKED"
    AUTHORITY_OUT_OF_SCOPE = "AUTHORITY_OUT_OF_SCOPE"
    TRANSITION_FOUNDER_DENIED = "TRANSITION_FOUNDER_DENIED"
    CONFIRMED_POSITION_FACT_MISSING = "CONFIRMED_POSITION_FACT_MISSING"
    POSITION_CLOSED_FACT_MISSING = "POSITION_CLOSED_FACT_MISSING"
    COOLDOWN_FACT_MISSING = "COOLDOWN_FACT_MISSING"
    LOCKOUT_REQUIRED = "LOCKOUT_REQUIRED"
    RESET_EVIDENCE_MISSING = "RESET_EVIDENCE_MISSING"
    RESET_FACTS_MISSING = "RESET_FACTS_MISSING"
    AMBIGUOUS_OR_CONTRADICTORY_INPUT = "AMBIGUOUS_OR_CONTRADICTORY_INPUT"


class RequiredAction(str, Enum):
    NONE = "NONE"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    GOVERNANCE_REVIEW = "GOVERNANCE_REVIEW"
    FOUNDER_AUTHORITY_REQUIRED = "FOUNDER_AUTHORITY_REQUIRED"
    RESET_REQUIRED = "RESET_REQUIRED"


@dataclass(frozen=True)
class ExternalFacts:
    readiness_preconditions_satisfied: bool
    confirmed_position_exists: bool
    position_closed: bool
    cooldown_complete: bool
    lockout_required: bool
    logging_failure_indicated: bool
    reset_facts_explicit: bool


@dataclass(frozen=True)
class AuthorityEvidence:
    presence: str
    subject_scope: str
    currentness: str
    revocation: str
    validity_outcome: str
    authority_reference: str


@dataclass(frozen=True)
class TransitionRequest:
    current_state: State
    requested_state: State
    transition_request: TransitionRequestName
    correlation_reference: str
    external_facts: ExternalFacts
    authority_evidence: AuthorityEvidence | None


@dataclass(frozen=True)
class TransitionDecision:
    current_state: State
    requested_state: State
    allowed: bool
    resulting_state: State
    reason_code: ReasonCode
    required_next_human_or_governance_action: RequiredAction
    correlation_reference: str


def _require_exact_type(value: object, expected_type: type, field_name: str) -> None:
    if type(value) is not expected_type:
        raise TypeError(f"{field_name} must be a {expected_type.__name__}")


def _require_non_empty_string(value: object, field_name: str) -> None:
    _require_exact_type(value, str, field_name)
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _require_closed_string(
    value: object, allowed: frozenset[str], field_name: str
) -> None:
    _require_exact_type(value, str, field_name)
    if value not in allowed:
        raise ValueError(f"{field_name} is outside the closed vocabulary")


def _validate_external_facts(value: object) -> ExternalFacts:
    _require_exact_type(value, ExternalFacts, "external_facts")
    for field_name in (
        "readiness_preconditions_satisfied",
        "confirmed_position_exists",
        "position_closed",
        "cooldown_complete",
        "lockout_required",
        "logging_failure_indicated",
        "reset_facts_explicit",
    ):
        _require_exact_type(getattr(value, field_name), bool, f"external_facts.{field_name}")
    return value


def _validate_authority_evidence(value: object) -> None:
    if value is None:
        return
    _require_exact_type(value, AuthorityEvidence, "authority_evidence")
    _require_closed_string(
        value.presence, frozenset({"PRESENT", "ABSENT"}), "authority_evidence.presence"
    )
    _require_non_empty_string(value.subject_scope, "authority_evidence.subject_scope")
    _require_closed_string(
        value.currentness, frozenset({"CURRENT", "STALE"}), "authority_evidence.currentness"
    )
    _require_closed_string(
        value.revocation,
        frozenset({"NON_REVOKED", "REVOKED"}),
        "authority_evidence.revocation",
    )
    _require_closed_string(
        value.validity_outcome,
        frozenset({"VALID", "INVALID", "AMBIGUOUS", "OUT_OF_SCOPE"}),
        "authority_evidence.validity_outcome",
    )
    _require_non_empty_string(
        value.authority_reference, "authority_evidence.authority_reference"
    )


def _validate_request(request: object) -> TransitionRequest:
    _require_exact_type(request, TransitionRequest, "request")
    _require_exact_type(request.current_state, State, "current_state")
    _require_exact_type(request.requested_state, State, "requested_state")
    _require_exact_type(
        request.transition_request, TransitionRequestName, "transition_request"
    )
    _require_non_empty_string(request.correlation_reference, "correlation_reference")
    _validate_external_facts(request.external_facts)
    if request.authority_evidence is None and (
        (
            request.current_state is State.READY
            and request.requested_state is State.ARMED_MANUAL
        )
        or (
            request.current_state is State.LOCKOUT
            and request.requested_state is State.PAUSE
        )
    ):
        raise ValueError(
            "authority_evidence must not be None for an authority-required transition"
        )
    _validate_authority_evidence(request.authority_evidence)
    return request


def _authority_reason(evidence: AuthorityEvidence | None) -> ReasonCode | None:
    if evidence is None or evidence.presence == "ABSENT":
        return ReasonCode.AUTHORITY_MISSING
    if evidence.currentness == "STALE":
        return ReasonCode.AUTHORITY_STALE
    if evidence.revocation == "REVOKED":
        return ReasonCode.AUTHORITY_REVOKED
    if evidence.validity_outcome == "OUT_OF_SCOPE" or not evidence.subject_scope:
        return ReasonCode.AUTHORITY_OUT_OF_SCOPE
    if evidence.validity_outcome != "VALID":
        return ReasonCode.AUTHORITY_INVALID
    if evidence.presence != "PRESENT" or evidence.currentness != "CURRENT":
        return ReasonCode.AUTHORITY_INVALID
    if not evidence.authority_reference:
        return ReasonCode.AUTHORITY_INVALID
    return None


def _decision(request: TransitionRequest, allowed: bool, resulting: State,
              reason: ReasonCode, action: RequiredAction) -> TransitionDecision:
    return TransitionDecision(
        current_state=request.current_state,
        requested_state=request.requested_state,
        allowed=allowed,
        resulting_state=resulting,
        reason_code=reason,
        required_next_human_or_governance_action=action,
        correlation_reference=request.correlation_reference,
    )


def evaluate_transition(request: TransitionRequest) -> TransitionDecision:
    """Evaluate one request without mutation, persistence, or external effects."""
    request = _validate_request(request)
    facts = request.external_facts
    if facts.lockout_required:
        return _decision(request, True, State.LOCKOUT, ReasonCode.LOCKOUT_REQUIRED, RequiredAction.NONE)
    if facts.confirmed_position_exists and facts.position_closed:
        return _decision(request, False, request.current_state, ReasonCode.AMBIGUOUS_OR_CONTRADICTORY_INPUT, RequiredAction.HUMAN_REVIEW)
    current, requested = request.current_state, request.requested_state
    if not isinstance(current, State) or not isinstance(requested, State):
        return _decision(request, False, current if isinstance(current, State) else State.PAUSE, ReasonCode.UNKNOWN_STATE, RequiredAction.GOVERNANCE_REVIEW)
    if current is State.PAUSE and requested is State.READY:
        if not facts.readiness_preconditions_satisfied:
            return _decision(request, False, current, ReasonCode.READINESS_FACTS_MISSING, RequiredAction.GOVERNANCE_REVIEW)
        return _decision(request, True, requested, ReasonCode.ALLOWED, RequiredAction.NONE)
    if current is State.READY and requested is State.ARMED_MANUAL:
        reason = _authority_reason(request.authority_evidence)
        if reason:
            action = RequiredAction.GOVERNANCE_REVIEW if reason is ReasonCode.AUTHORITY_OUT_OF_SCOPE else RequiredAction.FOUNDER_AUTHORITY_REQUIRED
            return _decision(request, False, current, reason, action)
        return _decision(request, True, requested, ReasonCode.ALLOWED, RequiredAction.NONE)
    if current is State.READY and requested is State.ARMED_AUTO:
        return _decision(request, False, current, ReasonCode.TRANSITION_FOUNDER_DENIED, RequiredAction.FOUNDER_AUTHORITY_REQUIRED)
    if current is State.ARMED_AUTO and requested is State.IN_TRADE:
        if not facts.confirmed_position_exists:
            return _decision(request, False, current, ReasonCode.CONFIRMED_POSITION_FACT_MISSING, RequiredAction.GOVERNANCE_REVIEW)
        return _decision(request, True, requested, ReasonCode.ALLOWED, RequiredAction.NONE)
    if current is State.ARMED_MANUAL and requested is State.IN_TRADE:
        return _decision(request, False, current, ReasonCode.UNDEFINED_TRANSITION, RequiredAction.GOVERNANCE_REVIEW)
    if current is State.IN_TRADE and requested is State.READY:
        return _decision(request, False, current, ReasonCode.UNDEFINED_TRANSITION, RequiredAction.GOVERNANCE_REVIEW)
    if current is State.IN_TRADE and requested is State.PAUSE:
        if not facts.position_closed:
            return _decision(request, False, current, ReasonCode.POSITION_CLOSED_FACT_MISSING, RequiredAction.GOVERNANCE_REVIEW)
        if not facts.cooldown_complete:
            return _decision(request, False, current, ReasonCode.COOLDOWN_FACT_MISSING, RequiredAction.GOVERNANCE_REVIEW)
        return _decision(request, True, requested, ReasonCode.ALLOWED, RequiredAction.NONE)
    if current is State.LOCKOUT and requested is State.PAUSE:
        reason = _authority_reason(request.authority_evidence)
        if reason:
            return _decision(request, False, current, ReasonCode.RESET_EVIDENCE_MISSING if reason is ReasonCode.AUTHORITY_MISSING else reason, RequiredAction.RESET_REQUIRED)
        if not facts.reset_facts_explicit:
            return _decision(request, False, current, ReasonCode.RESET_FACTS_MISSING, RequiredAction.RESET_REQUIRED)
        return _decision(request, True, requested, ReasonCode.ALLOWED, RequiredAction.NONE)
    if request.transition_request is TransitionRequestName.ANY_TO_LOCKOUT:
        return _decision(request, False, current, ReasonCode.UNDEFINED_TRANSITION, RequiredAction.GOVERNANCE_REVIEW)
    return _decision(request, False, current, ReasonCode.UNDEFINED_TRANSITION, RequiredAction.GOVERNANCE_REVIEW)
