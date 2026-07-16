"""Pure, deterministic Asset-Class Eligibility / Exclusion evaluator."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AssetClass(str, Enum):
    STOCK = "STOCK"
    OPTIONS = "OPTIONS"
    CRYPTO = "CRYPTO"


class Outcome(str, Enum):
    ELIGIBLE = "ELIGIBLE"
    EXCLUDED = "EXCLUDED"
    RESTRICTED = "RESTRICTED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class ReasonCode(str, Enum):
    ASSET_CLASS_ELIGIBLE = "ASSET_CLASS_ELIGIBLE"
    ASSET_CLASS_EXCLUDED = "ASSET_CLASS_EXCLUDED"
    ASSET_CLASS_RESTRICTED = "ASSET_CLASS_RESTRICTED"
    ELIGIBILITY_EVIDENCE_MISSING = "ELIGIBILITY_EVIDENCE_MISSING"
    ELIGIBILITY_EVIDENCE_STALE = "ELIGIBILITY_EVIDENCE_STALE"
    ELIGIBILITY_EVIDENCE_INSUFFICIENT = "ELIGIBILITY_EVIDENCE_INSUFFICIENT"
    ELIGIBILITY_EVIDENCE_CONTRADICTORY = "ELIGIBILITY_EVIDENCE_CONTRADICTORY"
    ELIGIBLE_EXCLUDED_CONFLICT = "ELIGIBLE_EXCLUDED_CONFLICT"
    ELIGIBLE_RESTRICTED_CONFLICT = "ELIGIBLE_RESTRICTED_CONFLICT"
    AUTHORITY_EVIDENCE_INVALID = "AUTHORITY_EVIDENCE_INVALID"
    AUTHORITY_EVIDENCE_STALE = "AUTHORITY_EVIDENCE_STALE"
    AUTHORITY_EVIDENCE_REVOKED = "AUTHORITY_EVIDENCE_REVOKED"
    AUTHORITY_EVIDENCE_OUT_OF_SCOPE = "AUTHORITY_EVIDENCE_OUT_OF_SCOPE"
    UNDEFINED_INPUT_COMBINATION = "UNDEFINED_INPUT_COMBINATION"
    ELIGIBILITY_UNRESOLVED = "ELIGIBILITY_UNRESOLVED"


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
class EligibilityRequest:
    asset_class: AssetClass
    eligibility_reference: str
    eligibility_evidence_present: bool
    eligibility_evidence_current: bool
    eligibility_evidence_sufficient: bool
    eligibility_evidence_contradictory: bool
    asset_class_eligible: bool
    asset_class_excluded: bool
    asset_class_restricted: bool
    correlation_reference: str
    authority_evidence: AuthorityEvidence | None = None

    def __post_init__(self) -> None:
        _require_exact(self.asset_class, AssetClass, "asset_class")
        _require_reference(self.eligibility_reference, "eligibility_reference")
        _require_bool(self.eligibility_evidence_present, "eligibility_evidence_present")
        _require_bool(self.eligibility_evidence_current, "eligibility_evidence_current")
        _require_bool(self.eligibility_evidence_sufficient, "eligibility_evidence_sufficient")
        _require_bool(self.eligibility_evidence_contradictory, "eligibility_evidence_contradictory")
        _require_bool(self.asset_class_eligible, "asset_class_eligible")
        _require_bool(self.asset_class_excluded, "asset_class_excluded")
        _require_bool(self.asset_class_restricted, "asset_class_restricted")
        _require_reference(self.correlation_reference, "correlation_reference")
        if self.authority_evidence is not None and type(self.authority_evidence) is not AuthorityEvidence:
            raise TypeError("authority_evidence must be AuthorityEvidence")


@dataclass(frozen=True)
class Decision:
    asset_class: AssetClass
    eligibility_reference: str
    outcome: Outcome
    reason_code: ReasonCode
    required_action: RequiredAction
    correlation_reference: str

    def __post_init__(self) -> None:
        _require_exact(self.asset_class, AssetClass, "asset_class")
        _require_reference(self.eligibility_reference, "eligibility_reference")
        _require_exact(self.outcome, Outcome, "outcome")
        _require_exact(self.reason_code, ReasonCode, "reason_code")
        _require_exact(self.required_action, RequiredAction, "required_action")
        if self.required_action not in _EMITTABLE_ACTIONS:
            raise ValueError("required_action is not emittable")
        _require_reference(self.correlation_reference, "correlation_reference")


def create_request(**values: object) -> EligibilityRequest:
    """Construct one typed request without coercion or evaluation."""
    if "authority_evidence" in values and values["authority_evidence"] is None:
        raise TypeError("explicit authority_evidence=None is not accepted")
    return EligibilityRequest(**values)


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


def _decision(request: EligibilityRequest, outcome: Outcome, reason: ReasonCode,
              action: RequiredAction) -> Decision:
    return Decision(
        asset_class=request.asset_class,
        eligibility_reference=request.eligibility_reference,
        outcome=outcome,
        reason_code=reason,
        required_action=action,
        correlation_reference=request.correlation_reference,
    )


def evaluate(request: EligibilityRequest) -> Decision:
    """Evaluate one typed request using the approved first-match order."""
    if type(request) is not EligibilityRequest:
        raise TypeError("request must be EligibilityRequest")
    if request.eligibility_evidence_contradictory:
        return _decision(request, Outcome.REVIEW_REQUIRED, ReasonCode.ELIGIBILITY_EVIDENCE_CONTRADICTORY, RequiredAction.HUMAN_REVIEW)
    if request.asset_class_eligible and request.asset_class_excluded:
        return _decision(request, Outcome.REVIEW_REQUIRED, ReasonCode.ELIGIBLE_EXCLUDED_CONFLICT, RequiredAction.GOVERNANCE_REVIEW)
    if request.asset_class_eligible and request.asset_class_restricted:
        return _decision(request, Outcome.RESTRICTED, ReasonCode.ELIGIBLE_RESTRICTED_CONFLICT, RequiredAction.HUMAN_REVIEW)
    undefined = (
        (not request.eligibility_evidence_present and request.eligibility_evidence_current)
        or (not request.eligibility_evidence_present and request.eligibility_evidence_sufficient)
        or (not request.eligibility_evidence_current and request.eligibility_evidence_sufficient)
    )
    if undefined:
        return _decision(request, Outcome.REVIEW_REQUIRED, ReasonCode.UNDEFINED_INPUT_COMBINATION, RequiredAction.GOVERNANCE_REVIEW)
    if request.asset_class_excluded:
        return _decision(request, Outcome.EXCLUDED, ReasonCode.ASSET_CLASS_EXCLUDED, RequiredAction.NONE)
    if request.asset_class_restricted:
        return _decision(request, Outcome.RESTRICTED, ReasonCode.ASSET_CLASS_RESTRICTED, RequiredAction.HUMAN_REVIEW)
    if request.authority_evidence is not None:
        authority_reason = _authority_reason(request.authority_evidence)
        if authority_reason is not None:
            return _decision(request, Outcome.REVIEW_REQUIRED, authority_reason, RequiredAction.GOVERNANCE_REVIEW)
    if not request.eligibility_evidence_present:
        return _decision(request, Outcome.REVIEW_REQUIRED, ReasonCode.ELIGIBILITY_EVIDENCE_MISSING, RequiredAction.HUMAN_REVIEW)
    if not request.eligibility_evidence_current:
        return _decision(request, Outcome.REVIEW_REQUIRED, ReasonCode.ELIGIBILITY_EVIDENCE_STALE, RequiredAction.HUMAN_REVIEW)
    if not request.eligibility_evidence_sufficient:
        return _decision(request, Outcome.REVIEW_REQUIRED, ReasonCode.ELIGIBILITY_EVIDENCE_INSUFFICIENT, RequiredAction.HUMAN_REVIEW)
    if request.asset_class_eligible:
        return _decision(request, Outcome.ELIGIBLE, ReasonCode.ASSET_CLASS_ELIGIBLE, RequiredAction.NONE)
    return _decision(request, Outcome.REVIEW_REQUIRED, ReasonCode.ELIGIBILITY_UNRESOLVED, RequiredAction.GOVERNANCE_REVIEW)
