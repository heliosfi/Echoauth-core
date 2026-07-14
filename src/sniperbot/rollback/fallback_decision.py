"""Pure, deterministic SniperBot rollback/no-action fallback evaluator."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Outcome(str, Enum):
    DEFER = "DEFER"
    NO_ACTION = "NO_ACTION"


class ReasonCode(str, Enum):
    ROLLBACK_EXTERNALLY_REQUIRED = "ROLLBACK_EXTERNALLY_REQUIRED"
    ROLLBACK_UNAVAILABLE = "ROLLBACK_UNAVAILABLE"
    ROLLBACK_EVIDENCE_MISSING = "ROLLBACK_EVIDENCE_MISSING"
    ROLLBACK_EVIDENCE_STALE = "ROLLBACK_EVIDENCE_STALE"
    ROLLBACK_EVIDENCE_INSUFFICIENT = "ROLLBACK_EVIDENCE_INSUFFICIENT"
    ROLLBACK_EVIDENCE_CONTRADICTORY = "ROLLBACK_EVIDENCE_CONTRADICTORY"
    ROLLBACK_AND_NO_ACTION_CONFLICT = "ROLLBACK_AND_NO_ACTION_CONFLICT"
    AUTHORITY_EVIDENCE_INVALID = "AUTHORITY_EVIDENCE_INVALID"
    AUTHORITY_EVIDENCE_STALE = "AUTHORITY_EVIDENCE_STALE"
    AUTHORITY_EVIDENCE_REVOKED = "AUTHORITY_EVIDENCE_REVOKED"
    AUTHORITY_EVIDENCE_OUT_OF_SCOPE = "AUTHORITY_EVIDENCE_OUT_OF_SCOPE"
    UNKNOWN_CONDITION = "UNKNOWN_CONDITION"
    UNDEFINED_INPUT_COMBINATION = "UNDEFINED_INPUT_COMBINATION"
    NO_ACTION_REQUIRED = "NO_ACTION_REQUIRED"


class EmittableReasonCode(str, Enum):
    ROLLBACK_EXTERNALLY_REQUIRED = ReasonCode.ROLLBACK_EXTERNALLY_REQUIRED.value
    ROLLBACK_UNAVAILABLE = ReasonCode.ROLLBACK_UNAVAILABLE.value
    ROLLBACK_EVIDENCE_MISSING = ReasonCode.ROLLBACK_EVIDENCE_MISSING.value
    ROLLBACK_EVIDENCE_STALE = ReasonCode.ROLLBACK_EVIDENCE_STALE.value
    ROLLBACK_EVIDENCE_INSUFFICIENT = ReasonCode.ROLLBACK_EVIDENCE_INSUFFICIENT.value
    ROLLBACK_EVIDENCE_CONTRADICTORY = ReasonCode.ROLLBACK_EVIDENCE_CONTRADICTORY.value
    ROLLBACK_AND_NO_ACTION_CONFLICT = ReasonCode.ROLLBACK_AND_NO_ACTION_CONFLICT.value
    AUTHORITY_EVIDENCE_INVALID = ReasonCode.AUTHORITY_EVIDENCE_INVALID.value
    AUTHORITY_EVIDENCE_STALE = ReasonCode.AUTHORITY_EVIDENCE_STALE.value
    AUTHORITY_EVIDENCE_REVOKED = ReasonCode.AUTHORITY_EVIDENCE_REVOKED.value
    AUTHORITY_EVIDENCE_OUT_OF_SCOPE = ReasonCode.AUTHORITY_EVIDENCE_OUT_OF_SCOPE.value
    UNDEFINED_INPUT_COMBINATION = ReasonCode.UNDEFINED_INPUT_COMBINATION.value
    NO_ACTION_REQUIRED = ReasonCode.NO_ACTION_REQUIRED.value


class RequiredAction(str, Enum):
    NONE = "NONE"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    GOVERNANCE_REVIEW = "GOVERNANCE_REVIEW"
    FOUNDER_AUTHORITY_REQUIRED = "FOUNDER_AUTHORITY_REQUIRED"
    RESET_REQUIRED = "RESET_REQUIRED"


class State(str, Enum):
    PAUSE = "PAUSE"
    READY = "READY"
    ARMED_MANUAL = "ARMED_MANUAL"
    ARMED_AUTO = "ARMED_AUTO"
    IN_TRADE = "IN_TRADE"
    LOCKOUT = "LOCKOUT"


_VALIDITY = {"VALID", "INVALID", "AMBIGUOUS"}
_CURRENTNESS = {"CURRENT", "STALE"}
_REVOCATION = {"NON_REVOKED", "REVOKED"}
_SCOPE = {"IN_SCOPE", "OUT_OF_SCOPE", "AMBIGUOUS"}
_EMITTABLE_REASONS = frozenset(EmittableReasonCode)
_EMITTABLE_ACTIONS = frozenset({RequiredAction.NONE, RequiredAction.HUMAN_REVIEW,
                                RequiredAction.GOVERNANCE_REVIEW})


@dataclass(frozen=True)
class AuthorityEvidence:
    validity: str
    currentness: str
    revocation: str
    scope: str
    evidence_reference: str

    def __post_init__(self) -> None:
        if self.validity not in _VALIDITY:
            raise ValueError("invalid authority validity")
        if self.currentness not in _CURRENTNESS:
            raise ValueError("invalid authority currentness")
        if self.revocation not in _REVOCATION:
            raise ValueError("invalid authority revocation")
        if self.scope not in _SCOPE:
            raise ValueError("invalid authority scope")
        if not self.evidence_reference:
            raise ValueError("evidence_reference is required")


@dataclass(frozen=True)
class Context:
    """Opaque descriptive FSM and recovery context; never drives evaluation."""

    fsm_state_reference: State | None = None
    halt_context: bool | None = None
    failure_context: bool | None = None
    recovery_context: bool | None = None
    reset_context: bool | None = None

    def __post_init__(self) -> None:
        if self.fsm_state_reference is not None and not isinstance(self.fsm_state_reference, State):
            raise ValueError("fsm_state_reference must be a State or None")
        for name in ("halt_context", "failure_context", "recovery_context", "reset_context"):
            value = getattr(self, name)
            if value is not None and not isinstance(value, bool):
                raise ValueError(f"{name} must be a boolean or None")


@dataclass(frozen=True)
class RollbackRequest:
    current_condition_reference: str
    rollback_required: bool
    rollback_available: bool
    rollback_evidence_present: bool
    rollback_evidence_current: bool
    rollback_evidence_sufficient: bool
    rollback_evidence_contradictory: bool
    no_action: bool
    correlation_reference: str
    authority_evidence: AuthorityEvidence | None = None
    fsm_state_reference: State | None = None
    halt_context: bool | None = None
    failure_context: bool | None = None
    recovery_context: bool | None = None
    reset_context: bool | None = None

    def __post_init__(self) -> None:
        if not self.current_condition_reference:
            raise ValueError("current_condition_reference is required")
        if not self.correlation_reference:
            raise ValueError("correlation_reference is required")
        for name in ("rollback_required", "rollback_available", "rollback_evidence_present",
                     "rollback_evidence_current", "rollback_evidence_sufficient",
                     "rollback_evidence_contradictory", "no_action"):
            if not isinstance(getattr(self, name), bool):
                raise ValueError(f"{name} must be a boolean")
        if self.authority_evidence is not None and not isinstance(self.authority_evidence, AuthorityEvidence):
            raise ValueError("authority_evidence must be AuthorityEvidence or None")
        Context(self.fsm_state_reference, self.halt_context, self.failure_context,
                self.recovery_context, self.reset_context)


@dataclass(frozen=True)
class Decision:
    outcome: Outcome
    reason_code: ReasonCode
    required_action: RequiredAction
    correlation_reference: str
    rollback_no_action_posture: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.outcome, Outcome):
            raise ValueError("outcome must be an Outcome")
        if not isinstance(self.reason_code, ReasonCode) or self.reason_code not in _EMITTABLE_REASONS:
            raise ValueError("reason_code is not emittable by this subject")
        if not isinstance(self.required_action, RequiredAction) or self.required_action not in _EMITTABLE_ACTIONS:
            raise ValueError("required_action is not emittable by this subject")
        if not self.correlation_reference:
            raise ValueError("correlation_reference is required")
        if self.rollback_no_action_posture not in {None, "ROLLBACK_REVIEW", "NO_ACTION"}:
            raise ValueError("invalid rollback_no_action_posture")


def create_request(**values: object) -> RollbackRequest:
    """Create a typed request, rejecting unknown closed enum values first."""
    state = values.get("fsm_state_reference")
    if state is not None and not isinstance(state, State):
        try:
            values["fsm_state_reference"] = State(state)
        except (TypeError, ValueError) as exc:
            raise ValueError("unknown raw FSM state") from exc
    return RollbackRequest(**values)  # type: ignore[arg-type]


def _authority_reason(evidence: AuthorityEvidence) -> ReasonCode | None:
    if evidence.validity == "AMBIGUOUS" or evidence.scope == "AMBIGUOUS":
        return ReasonCode.AUTHORITY_EVIDENCE_INVALID
    if evidence.validity == "INVALID":
        return ReasonCode.AUTHORITY_EVIDENCE_INVALID
    if evidence.revocation == "REVOKED":
        return ReasonCode.AUTHORITY_EVIDENCE_REVOKED
    if evidence.currentness == "STALE":
        return ReasonCode.AUTHORITY_EVIDENCE_STALE
    if evidence.scope == "OUT_OF_SCOPE":
        return ReasonCode.AUTHORITY_EVIDENCE_OUT_OF_SCOPE
    return None


def _decision(request: RollbackRequest, outcome: Outcome, reason: ReasonCode,
              action: RequiredAction) -> Decision:
    return Decision(outcome, reason, action, request.correlation_reference)


def evaluate(request: RollbackRequest) -> Decision:
    """Evaluate supplied descriptive facts using the approved first-match order."""
    if not isinstance(request, RollbackRequest):
        raise TypeError("request must be a RollbackRequest")
    if request.rollback_evidence_contradictory:
        return _decision(request, Outcome.NO_ACTION, ReasonCode.ROLLBACK_EVIDENCE_CONTRADICTORY, RequiredAction.HUMAN_REVIEW)
    if request.rollback_required and request.no_action:
        return _decision(request, Outcome.NO_ACTION, ReasonCode.ROLLBACK_AND_NO_ACTION_CONFLICT, RequiredAction.GOVERNANCE_REVIEW)
    if ((not request.rollback_evidence_present and request.rollback_evidence_current)
            or (not request.rollback_evidence_present and request.rollback_evidence_sufficient)
            or (not request.rollback_evidence_current and request.rollback_evidence_sufficient)):
        return _decision(request, Outcome.NO_ACTION, ReasonCode.UNDEFINED_INPUT_COMBINATION, RequiredAction.GOVERNANCE_REVIEW)
    if request.authority_evidence is not None:
        reason = _authority_reason(request.authority_evidence)
        if reason is not None:
            return _decision(request, Outcome.NO_ACTION, reason, RequiredAction.GOVERNANCE_REVIEW)
    if not request.rollback_evidence_present:
        return _decision(request, Outcome.DEFER, ReasonCode.ROLLBACK_EVIDENCE_MISSING, RequiredAction.HUMAN_REVIEW)
    if not request.rollback_evidence_current:
        return _decision(request, Outcome.DEFER, ReasonCode.ROLLBACK_EVIDENCE_STALE, RequiredAction.HUMAN_REVIEW)
    if not request.rollback_evidence_sufficient:
        return _decision(request, Outcome.DEFER, ReasonCode.ROLLBACK_EVIDENCE_INSUFFICIENT, RequiredAction.HUMAN_REVIEW)
    if request.rollback_required and not request.rollback_available:
        return _decision(request, Outcome.DEFER, ReasonCode.ROLLBACK_UNAVAILABLE, RequiredAction.HUMAN_REVIEW)
    if request.rollback_required:
        return _decision(request, Outcome.DEFER, ReasonCode.ROLLBACK_EXTERNALLY_REQUIRED, RequiredAction.HUMAN_REVIEW)
    return _decision(request, Outcome.NO_ACTION, ReasonCode.NO_ACTION_REQUIRED, RequiredAction.NONE)
