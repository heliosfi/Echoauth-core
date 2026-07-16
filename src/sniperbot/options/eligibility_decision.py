"""Pure, deterministic Options Eligibility / Exclusion evaluator."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Outcome(str, Enum):
    ELIGIBLE = "ELIGIBLE"
    EXCLUDED = "EXCLUDED"
    RESTRICTED = "RESTRICTED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class ReasonCode(str, Enum):
    OPTIONS_ELIGIBLE = "OPTIONS_ELIGIBLE"
    OPTIONS_EXCLUDED = "OPTIONS_EXCLUDED"
    OPTIONS_RESTRICTED = "OPTIONS_RESTRICTED"
    OPTIONS_ELIGIBILITY_EVIDENCE_MISSING = "OPTIONS_ELIGIBILITY_EVIDENCE_MISSING"
    OPTIONS_ELIGIBILITY_EVIDENCE_STALE = "OPTIONS_ELIGIBILITY_EVIDENCE_STALE"
    OPTIONS_ELIGIBILITY_EVIDENCE_INSUFFICIENT = "OPTIONS_ELIGIBILITY_EVIDENCE_INSUFFICIENT"
    OPTIONS_ELIGIBILITY_EVIDENCE_CONTRADICTORY = "OPTIONS_ELIGIBILITY_EVIDENCE_CONTRADICTORY"
    OPTIONS_ELIGIBLE_EXCLUDED_CONFLICT = "OPTIONS_ELIGIBLE_EXCLUDED_CONFLICT"
    OPTIONS_ELIGIBLE_RESTRICTED_CONFLICT = "OPTIONS_ELIGIBLE_RESTRICTED_CONFLICT"
    AUTHORITY_EVIDENCE_INVALID = "AUTHORITY_EVIDENCE_INVALID"
    AUTHORITY_EVIDENCE_STALE = "AUTHORITY_EVIDENCE_STALE"
    AUTHORITY_EVIDENCE_REVOKED = "AUTHORITY_EVIDENCE_REVOKED"
    AUTHORITY_EVIDENCE_OUT_OF_SCOPE = "AUTHORITY_EVIDENCE_OUT_OF_SCOPE"
    UNDEFINED_INPUT_COMBINATION = "UNDEFINED_INPUT_COMBINATION"
    OPTIONS_ELIGIBILITY_UNRESOLVED = "OPTIONS_ELIGIBILITY_UNRESOLVED"


class RequiredAction(str, Enum):
    NONE = "NONE"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    GOVERNANCE_REVIEW = "GOVERNANCE_REVIEW"
    FOUNDER_AUTHORITY_REQUIRED = "FOUNDER_AUTHORITY_REQUIRED"
    RESET_REQUIRED = "RESET_REQUIRED"


class Validity(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    AMBIGUOUS = "AMBIGUOUS"


_EMITTABLE_ACTIONS = (
    RequiredAction.NONE,
    RequiredAction.HUMAN_REVIEW,
    RequiredAction.GOVERNANCE_REVIEW,
)


def _require_exact(value: object, expected: type[Enum], field: str) -> None:
    if type(value) is not expected:
        raise TypeError(f"{field} must be {expected.__name__}")


def _require_bool(value: object, field: str) -> None:
    if type(value) is not bool:
        raise TypeError(f"{field} must be bool")


def _require_reference(value: object, field: str) -> None:
    if type(value) is not str:
        raise TypeError(f"{field} must be str")
    if not value:
        raise ValueError(f"{field} is required")


@dataclass(frozen=True)
class AuthorityEvidence:
    validity: Validity
    current: bool
    revoked: bool
    contradictory: bool
    in_scope: bool
    evidence_reference: str

    def __post_init__(self) -> None:
        _require_exact(self.validity, Validity, "validity")
        _require_bool(self.current, "current")
        _require_bool(self.revoked, "revoked")
        _require_bool(self.contradictory, "contradictory")
        _require_bool(self.in_scope, "in_scope")
        _require_reference(self.evidence_reference, "evidence_reference")


@dataclass(frozen=True)
class OptionsEligibilityRequest:
    options_reference: str
    eligibility_evidence_present: bool
    eligibility_evidence_current: bool
    eligibility_evidence_sufficient: bool
    eligibility_evidence_contradictory: bool
    options_eligible: bool
    options_excluded: bool
    options_restricted: bool
    eligibility_evidence_reference: str
    correlation_reference: str
    authority_evidence: AuthorityEvidence | None = None

    def __post_init__(self) -> None:
        _require_reference(self.options_reference, "options_reference")
        _require_bool(self.eligibility_evidence_present, "eligibility_evidence_present")
        _require_bool(self.eligibility_evidence_current, "eligibility_evidence_current")
        _require_bool(self.eligibility_evidence_sufficient, "eligibility_evidence_sufficient")
        _require_bool(self.eligibility_evidence_contradictory, "eligibility_evidence_contradictory")
        _require_bool(self.options_eligible, "options_eligible")
        _require_bool(self.options_excluded, "options_excluded")
        _require_bool(self.options_restricted, "options_restricted")
        _require_reference(self.eligibility_evidence_reference, "eligibility_evidence_reference")
        _require_reference(self.correlation_reference, "correlation_reference")
        if self.authority_evidence is not None and type(self.authority_evidence) is not AuthorityEvidence:
            raise TypeError("authority_evidence must be AuthorityEvidence")


@dataclass(frozen=True)
class Decision:
    outcome: Outcome
    reason_code: ReasonCode
    required_action: RequiredAction
    options_reference: str
    eligibility_evidence_reference: str
    correlation_reference: str

    def __post_init__(self) -> None:
        _require_exact(self.outcome, Outcome, "outcome")
        _require_exact(self.reason_code, ReasonCode, "reason_code")
        _require_exact(self.required_action, RequiredAction, "required_action")
        if self.required_action not in _EMITTABLE_ACTIONS:
            raise ValueError("required_action is not emittable")
        _require_reference(self.options_reference, "options_reference")
        _require_reference(self.eligibility_evidence_reference, "eligibility_evidence_reference")
        _require_reference(self.correlation_reference, "correlation_reference")


def create_request(**values: object) -> OptionsEligibilityRequest:
    """Construct one typed request without coercion or evaluation."""
    if "authority_evidence" in values and values["authority_evidence"] is None:
        raise TypeError("explicit authority_evidence=None is not accepted")
    return OptionsEligibilityRequest(**values)


def _authority_reason(evidence: AuthorityEvidence) -> ReasonCode | None:
    if evidence.contradictory:
        return ReasonCode.AUTHORITY_EVIDENCE_INVALID
    if evidence.validity is Validity.AMBIGUOUS:
        return ReasonCode.AUTHORITY_EVIDENCE_INVALID
    if evidence.validity is Validity.INVALID:
        return ReasonCode.AUTHORITY_EVIDENCE_INVALID
    if evidence.revoked:
        return ReasonCode.AUTHORITY_EVIDENCE_REVOKED
    if not evidence.current:
        return ReasonCode.AUTHORITY_EVIDENCE_STALE
    if not evidence.in_scope:
        return ReasonCode.AUTHORITY_EVIDENCE_OUT_OF_SCOPE
    return None


def _decision(
    request: OptionsEligibilityRequest,
    outcome: Outcome,
    reason: ReasonCode,
    action: RequiredAction,
) -> Decision:
    return Decision(
        outcome=outcome,
        reason_code=reason,
        required_action=action,
        options_reference=request.options_reference,
        eligibility_evidence_reference=request.eligibility_evidence_reference,
        correlation_reference=request.correlation_reference,
    )


def evaluate(request: OptionsEligibilityRequest) -> Decision:
    """Evaluate one typed request using the approved first-match order."""
    if type(request) is not OptionsEligibilityRequest:
        raise TypeError("request must be OptionsEligibilityRequest")
    if request.eligibility_evidence_contradictory:
        return _decision(request, Outcome.REVIEW_REQUIRED, ReasonCode.OPTIONS_ELIGIBILITY_EVIDENCE_CONTRADICTORY, RequiredAction.HUMAN_REVIEW)
    if request.options_eligible and request.options_excluded:
        return _decision(request, Outcome.REVIEW_REQUIRED, ReasonCode.OPTIONS_ELIGIBLE_EXCLUDED_CONFLICT, RequiredAction.GOVERNANCE_REVIEW)
    if request.options_eligible and request.options_restricted:
        return _decision(request, Outcome.RESTRICTED, ReasonCode.OPTIONS_ELIGIBLE_RESTRICTED_CONFLICT, RequiredAction.HUMAN_REVIEW)
    undefined = (
        (not request.eligibility_evidence_present and request.eligibility_evidence_current)
        or (not request.eligibility_evidence_present and request.eligibility_evidence_sufficient)
        or (not request.eligibility_evidence_current and request.eligibility_evidence_sufficient)
    )
    if undefined:
        return _decision(request, Outcome.REVIEW_REQUIRED, ReasonCode.UNDEFINED_INPUT_COMBINATION, RequiredAction.GOVERNANCE_REVIEW)
    if request.options_excluded:
        return _decision(request, Outcome.EXCLUDED, ReasonCode.OPTIONS_EXCLUDED, RequiredAction.NONE)
    if request.options_restricted:
        return _decision(request, Outcome.RESTRICTED, ReasonCode.OPTIONS_RESTRICTED, RequiredAction.HUMAN_REVIEW)
    if request.authority_evidence is not None:
        authority_reason = _authority_reason(request.authority_evidence)
        if authority_reason is not None:
            return _decision(request, Outcome.REVIEW_REQUIRED, authority_reason, RequiredAction.GOVERNANCE_REVIEW)
    if not request.eligibility_evidence_present:
        return _decision(request, Outcome.REVIEW_REQUIRED, ReasonCode.OPTIONS_ELIGIBILITY_EVIDENCE_MISSING, RequiredAction.HUMAN_REVIEW)
    if not request.eligibility_evidence_current:
        return _decision(request, Outcome.REVIEW_REQUIRED, ReasonCode.OPTIONS_ELIGIBILITY_EVIDENCE_STALE, RequiredAction.HUMAN_REVIEW)
    if not request.eligibility_evidence_sufficient:
        return _decision(request, Outcome.REVIEW_REQUIRED, ReasonCode.OPTIONS_ELIGIBILITY_EVIDENCE_INSUFFICIENT, RequiredAction.HUMAN_REVIEW)
    if request.options_eligible:
        return _decision(request, Outcome.ELIGIBLE, ReasonCode.OPTIONS_ELIGIBLE, RequiredAction.NONE)
    return _decision(request, Outcome.REVIEW_REQUIRED, ReasonCode.OPTIONS_ELIGIBILITY_UNRESOLVED, RequiredAction.GOVERNANCE_REVIEW)


__all__ = [
    "Outcome",
    "ReasonCode",
    "RequiredAction",
    "Validity",
    "AuthorityEvidence",
    "OptionsEligibilityRequest",
    "Decision",
    "create_request",
    "evaluate",
]
