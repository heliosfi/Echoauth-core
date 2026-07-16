"""Pure, deterministic Stock Eligibility / Exclusion evaluator."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AssetClass(str, Enum):
    STOCK = "STOCK"
    OPTIONS = "OPTIONS"
    CRYPTO = "CRYPTO"


class StockLaneConfirmation(str, Enum):
    CONFIRMED = "CONFIRMED"
    NOT_CONFIRMED = "NOT_CONFIRMED"
    CONTRADICTORY = "CONTRADICTORY"


class Validity(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    AMBIGUOUS = "AMBIGUOUS"


class Outcome(str, Enum):
    ELIGIBLE = "ELIGIBLE"
    EXCLUDED = "EXCLUDED"
    RESTRICTED = "RESTRICTED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


class ReasonCode(str, Enum):
    STOCK_ELIGIBLE = "STOCK_ELIGIBLE"
    STOCK_EXCLUDED = "STOCK_EXCLUDED"
    STOCK_RESTRICTED = "STOCK_RESTRICTED"
    STOCK_ELIGIBILITY_EVIDENCE_MISSING = "STOCK_ELIGIBILITY_EVIDENCE_MISSING"
    STOCK_ELIGIBILITY_EVIDENCE_STALE = "STOCK_ELIGIBILITY_EVIDENCE_STALE"
    STOCK_ELIGIBILITY_EVIDENCE_INSUFFICIENT = "STOCK_ELIGIBILITY_EVIDENCE_INSUFFICIENT"
    STOCK_ELIGIBILITY_EVIDENCE_CONTRADICTORY = "STOCK_ELIGIBILITY_EVIDENCE_CONTRADICTORY"
    STOCK_ELIGIBLE_EXCLUDED_CONFLICT = "STOCK_ELIGIBLE_EXCLUDED_CONFLICT"
    STOCK_ELIGIBLE_RESTRICTED_CONFLICT = "STOCK_ELIGIBLE_RESTRICTED_CONFLICT"
    STOCK_LANE_CONFIRMATION_MISSING = "STOCK_LANE_CONFIRMATION_MISSING"
    STOCK_LANE_NOT_CONFIRMED = "STOCK_LANE_NOT_CONFIRMED"
    STOCK_LANE_CONTRADICTORY = "STOCK_LANE_CONTRADICTORY"
    GENERIC_ASSET_CLASS_CONTEXT_INVALID = "GENERIC_ASSET_CLASS_CONTEXT_INVALID"
    GENERIC_ASSET_CLASS_CONTEXT_STALE = "GENERIC_ASSET_CLASS_CONTEXT_STALE"
    GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY = "GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY"
    GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE = "GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE"
    GENERIC_ASSET_CLASS_NOT_STOCK = "GENERIC_ASSET_CLASS_NOT_STOCK"
    AUTHORITY_EVIDENCE_INVALID = "AUTHORITY_EVIDENCE_INVALID"
    AUTHORITY_EVIDENCE_STALE = "AUTHORITY_EVIDENCE_STALE"
    AUTHORITY_EVIDENCE_REVOKED = "AUTHORITY_EVIDENCE_REVOKED"
    AUTHORITY_EVIDENCE_OUT_OF_SCOPE = "AUTHORITY_EVIDENCE_OUT_OF_SCOPE"
    UNDEFINED_INPUT_COMBINATION = "UNDEFINED_INPUT_COMBINATION"
    STOCK_ELIGIBILITY_UNRESOLVED = "STOCK_ELIGIBILITY_UNRESOLVED"


class RequiredAction(str, Enum):
    NONE = "NONE"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    GOVERNANCE_REVIEW = "GOVERNANCE_REVIEW"
    FOUNDER_AUTHORITY_REQUIRED = "FOUNDER_AUTHORITY_REQUIRED"
    RESET_REQUIRED = "RESET_REQUIRED"


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
    if not value.strip():
        raise ValueError(f"{field} must contain a non-whitespace character")


@dataclass(frozen=True)
class GenericAssetClassContext:
    asset_class: AssetClass
    validity: Validity
    current: bool
    contradictory: bool
    in_scope: bool
    context_reference: str

    def __post_init__(self) -> None:
        _require_exact(self.asset_class, AssetClass, "asset_class")
        _require_exact(self.validity, Validity, "validity")
        _require_bool(self.current, "current")
        _require_bool(self.contradictory, "contradictory")
        _require_bool(self.in_scope, "in_scope")
        _require_reference(self.context_reference, "context_reference")


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
class StockEligibilityRequest:
    stock_reference: str
    eligibility_evidence_present: bool
    eligibility_evidence_current: bool
    eligibility_evidence_sufficient: bool
    eligibility_evidence_contradictory: bool
    stock_eligible: bool
    stock_excluded: bool
    stock_restricted: bool
    eligibility_evidence_reference: str
    correlation_reference: str
    stock_lane_confirmation: StockLaneConfirmation | None = None
    generic_asset_class_context: GenericAssetClassContext | None = None
    authority_evidence: AuthorityEvidence | None = None

    def __post_init__(self) -> None:
        _require_reference(self.stock_reference, "stock_reference")
        _require_bool(self.eligibility_evidence_present, "eligibility_evidence_present")
        _require_bool(self.eligibility_evidence_current, "eligibility_evidence_current")
        _require_bool(self.eligibility_evidence_sufficient, "eligibility_evidence_sufficient")
        _require_bool(self.eligibility_evidence_contradictory, "eligibility_evidence_contradictory")
        _require_bool(self.stock_eligible, "stock_eligible")
        _require_bool(self.stock_excluded, "stock_excluded")
        _require_bool(self.stock_restricted, "stock_restricted")
        _require_reference(self.eligibility_evidence_reference, "eligibility_evidence_reference")
        _require_reference(self.correlation_reference, "correlation_reference")
        if self.stock_lane_confirmation is not None:
            _require_exact(
                self.stock_lane_confirmation,
                StockLaneConfirmation,
                "stock_lane_confirmation",
            )
        if (
            self.generic_asset_class_context is not None
            and type(self.generic_asset_class_context) is not GenericAssetClassContext
        ):
            raise TypeError("generic_asset_class_context must be GenericAssetClassContext")
        if self.authority_evidence is not None and type(self.authority_evidence) is not AuthorityEvidence:
            raise TypeError("authority_evidence must be AuthorityEvidence")


@dataclass(frozen=True)
class Decision:
    outcome: Outcome
    reason_code: ReasonCode
    required_action: RequiredAction
    stock_reference: str
    eligibility_evidence_reference: str
    correlation_reference: str

    def __post_init__(self) -> None:
        _require_exact(self.outcome, Outcome, "outcome")
        _require_exact(self.reason_code, ReasonCode, "reason_code")
        _require_exact(self.required_action, RequiredAction, "required_action")
        if self.required_action not in _EMITTABLE_ACTIONS:
            raise ValueError("required_action is not emittable")
        _require_reference(self.stock_reference, "stock_reference")
        _require_reference(self.eligibility_evidence_reference, "eligibility_evidence_reference")
        _require_reference(self.correlation_reference, "correlation_reference")


def create_request(**values: object) -> StockEligibilityRequest:
    """Construct one strictly typed request without coercion or evaluation."""
    if "generic_asset_class_context" in values and values["generic_asset_class_context"] is None:
        raise TypeError("explicit generic_asset_class_context=None is not accepted")
    if "authority_evidence" in values and values["authority_evidence"] is None:
        raise TypeError("explicit authority_evidence=None is not accepted")
    return StockEligibilityRequest(**values)


def _generic_reason(context: GenericAssetClassContext) -> ReasonCode | None:
    if context.contradictory:
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY
    if context.validity is Validity.AMBIGUOUS:
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID
    if context.validity is Validity.INVALID:
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID
    if context.asset_class is not AssetClass.STOCK:
        return ReasonCode.GENERIC_ASSET_CLASS_NOT_STOCK
    if not context.current:
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_STALE
    if not context.in_scope:
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE
    return None


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
    request: StockEligibilityRequest,
    outcome: Outcome,
    reason: ReasonCode,
    action: RequiredAction,
) -> Decision:
    return Decision(
        outcome=outcome,
        reason_code=reason,
        required_action=action,
        stock_reference=request.stock_reference,
        eligibility_evidence_reference=request.eligibility_evidence_reference,
        correlation_reference=request.correlation_reference,
    )


def evaluate(request: StockEligibilityRequest) -> Decision:
    """Evaluate one typed request using the governed first-match order."""
    if type(request) is not StockEligibilityRequest:
        raise TypeError("request must be StockEligibilityRequest")
    if request.eligibility_evidence_contradictory:
        return _decision(
            request,
            Outcome.REVIEW_REQUIRED,
            ReasonCode.STOCK_ELIGIBILITY_EVIDENCE_CONTRADICTORY,
            RequiredAction.HUMAN_REVIEW,
        )
    if request.stock_eligible and request.stock_excluded:
        return _decision(
            request,
            Outcome.REVIEW_REQUIRED,
            ReasonCode.STOCK_ELIGIBLE_EXCLUDED_CONFLICT,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if request.stock_eligible and request.stock_restricted:
        return _decision(
            request,
            Outcome.RESTRICTED,
            ReasonCode.STOCK_ELIGIBLE_RESTRICTED_CONFLICT,
            RequiredAction.HUMAN_REVIEW,
        )
    undefined = (
        not request.eligibility_evidence_present and request.eligibility_evidence_current
    ) or (
        not request.eligibility_evidence_present and request.eligibility_evidence_sufficient
    ) or (
        not request.eligibility_evidence_current and request.eligibility_evidence_sufficient
    )
    if undefined:
        return _decision(
            request,
            Outcome.REVIEW_REQUIRED,
            ReasonCode.UNDEFINED_INPUT_COMBINATION,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if request.stock_lane_confirmation is None:
        return _decision(
            request,
            Outcome.REVIEW_REQUIRED,
            ReasonCode.STOCK_LANE_CONFIRMATION_MISSING,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if request.stock_lane_confirmation is StockLaneConfirmation.CONTRADICTORY:
        return _decision(
            request,
            Outcome.REVIEW_REQUIRED,
            ReasonCode.STOCK_LANE_CONTRADICTORY,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if request.stock_lane_confirmation is StockLaneConfirmation.NOT_CONFIRMED:
        return _decision(
            request,
            Outcome.REVIEW_REQUIRED,
            ReasonCode.STOCK_LANE_NOT_CONFIRMED,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if request.generic_asset_class_context is not None:
        generic_reason = _generic_reason(request.generic_asset_class_context)
        if generic_reason is not None:
            return _decision(
                request,
                Outcome.REVIEW_REQUIRED,
                generic_reason,
                RequiredAction.GOVERNANCE_REVIEW,
            )
    if request.stock_excluded:
        return _decision(
            request,
            Outcome.EXCLUDED,
            ReasonCode.STOCK_EXCLUDED,
            RequiredAction.NONE,
        )
    if request.stock_restricted:
        return _decision(
            request,
            Outcome.RESTRICTED,
            ReasonCode.STOCK_RESTRICTED,
            RequiredAction.HUMAN_REVIEW,
        )
    if request.authority_evidence is not None:
        authority_reason = _authority_reason(request.authority_evidence)
        if authority_reason is not None:
            return _decision(
                request,
                Outcome.REVIEW_REQUIRED,
                authority_reason,
                RequiredAction.GOVERNANCE_REVIEW,
            )
    if not request.eligibility_evidence_present:
        return _decision(
            request,
            Outcome.REVIEW_REQUIRED,
            ReasonCode.STOCK_ELIGIBILITY_EVIDENCE_MISSING,
            RequiredAction.HUMAN_REVIEW,
        )
    if not request.eligibility_evidence_current:
        return _decision(
            request,
            Outcome.REVIEW_REQUIRED,
            ReasonCode.STOCK_ELIGIBILITY_EVIDENCE_STALE,
            RequiredAction.HUMAN_REVIEW,
        )
    if not request.eligibility_evidence_sufficient:
        return _decision(
            request,
            Outcome.REVIEW_REQUIRED,
            ReasonCode.STOCK_ELIGIBILITY_EVIDENCE_INSUFFICIENT,
            RequiredAction.HUMAN_REVIEW,
        )
    if request.stock_eligible:
        return _decision(
            request,
            Outcome.ELIGIBLE,
            ReasonCode.STOCK_ELIGIBLE,
            RequiredAction.NONE,
        )
    return _decision(
        request,
        Outcome.REVIEW_REQUIRED,
        ReasonCode.STOCK_ELIGIBILITY_UNRESOLVED,
        RequiredAction.GOVERNANCE_REVIEW,
    )


__all__ = [
    "AssetClass",
    "AuthorityEvidence",
    "Decision",
    "GenericAssetClassContext",
    "Outcome",
    "ReasonCode",
    "RequiredAction",
    "StockEligibilityRequest",
    "StockLaneConfirmation",
    "Validity",
    "create_request",
    "evaluate",
]
