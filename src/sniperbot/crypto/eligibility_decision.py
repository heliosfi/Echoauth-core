"""Pure, deterministic Crypto Eligibility / Exclusion evaluator."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AssetClass(str, Enum):
    STOCK = "STOCK"
    OPTIONS = "OPTIONS"
    CRYPTO = "CRYPTO"


class CryptoLaneConfirmation(str, Enum):
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
    CRYPTO_ELIGIBLE = "CRYPTO_ELIGIBLE"
    CRYPTO_EXCLUDED = "CRYPTO_EXCLUDED"
    CRYPTO_RESTRICTED = "CRYPTO_RESTRICTED"
    CRYPTO_ELIGIBILITY_EVIDENCE_MISSING = "CRYPTO_ELIGIBILITY_EVIDENCE_MISSING"
    CRYPTO_ELIGIBILITY_EVIDENCE_STALE = "CRYPTO_ELIGIBILITY_EVIDENCE_STALE"
    CRYPTO_ELIGIBILITY_EVIDENCE_INSUFFICIENT = "CRYPTO_ELIGIBILITY_EVIDENCE_INSUFFICIENT"
    CRYPTO_ELIGIBILITY_EVIDENCE_CONTRADICTORY = (
        "CRYPTO_ELIGIBILITY_EVIDENCE_CONTRADICTORY"
    )
    CRYPTO_ELIGIBLE_EXCLUDED_CONFLICT = "CRYPTO_ELIGIBLE_EXCLUDED_CONFLICT"
    CRYPTO_ELIGIBLE_RESTRICTED_CONFLICT = "CRYPTO_ELIGIBLE_RESTRICTED_CONFLICT"
    CRYPTO_LANE_CONFIRMATION_MISSING = "CRYPTO_LANE_CONFIRMATION_MISSING"
    CRYPTO_LANE_NOT_CONFIRMED = "CRYPTO_LANE_NOT_CONFIRMED"
    CRYPTO_LANE_CONTRADICTORY = "CRYPTO_LANE_CONTRADICTORY"
    GENERIC_ASSET_CLASS_CONTEXT_INVALID = "GENERIC_ASSET_CLASS_CONTEXT_INVALID"
    GENERIC_ASSET_CLASS_CONTEXT_STALE = "GENERIC_ASSET_CLASS_CONTEXT_STALE"
    GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY = (
        "GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY"
    )
    GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE = (
        "GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE"
    )
    GENERIC_ASSET_CLASS_NOT_CRYPTO = "GENERIC_ASSET_CLASS_NOT_CRYPTO"
    AUTHORITY_EVIDENCE_INVALID = "AUTHORITY_EVIDENCE_INVALID"
    AUTHORITY_EVIDENCE_STALE = "AUTHORITY_EVIDENCE_STALE"
    AUTHORITY_EVIDENCE_REVOKED = "AUTHORITY_EVIDENCE_REVOKED"
    AUTHORITY_EVIDENCE_OUT_OF_SCOPE = "AUTHORITY_EVIDENCE_OUT_OF_SCOPE"
    UNDEFINED_INPUT_COMBINATION = "UNDEFINED_INPUT_COMBINATION"
    CRYPTO_ELIGIBILITY_UNRESOLVED = "CRYPTO_ELIGIBILITY_UNRESOLVED"


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
class CryptoEligibilityRequest:
    crypto_reference: str
    eligibility_evidence_present: bool
    eligibility_evidence_current: bool
    eligibility_evidence_sufficient: bool
    eligibility_evidence_contradictory: bool
    crypto_eligible: bool
    crypto_excluded: bool
    crypto_restricted: bool
    eligibility_evidence_reference: str
    correlation_reference: str
    crypto_lane_confirmation: CryptoLaneConfirmation | None = None
    generic_asset_class_context: GenericAssetClassContext | None = None
    authority_evidence: AuthorityEvidence | None = None

    def __post_init__(self) -> None:
        _require_reference(self.crypto_reference, "crypto_reference")
        _require_bool(self.eligibility_evidence_present, "eligibility_evidence_present")
        _require_bool(self.eligibility_evidence_current, "eligibility_evidence_current")
        _require_bool(self.eligibility_evidence_sufficient, "eligibility_evidence_sufficient")
        _require_bool(
            self.eligibility_evidence_contradictory,
            "eligibility_evidence_contradictory",
        )
        _require_bool(self.crypto_eligible, "crypto_eligible")
        _require_bool(self.crypto_excluded, "crypto_excluded")
        _require_bool(self.crypto_restricted, "crypto_restricted")
        _require_reference(
            self.eligibility_evidence_reference,
            "eligibility_evidence_reference",
        )
        _require_reference(self.correlation_reference, "correlation_reference")
        if self.crypto_lane_confirmation is not None:
            _require_exact(
                self.crypto_lane_confirmation,
                CryptoLaneConfirmation,
                "crypto_lane_confirmation",
            )
        if (
            self.generic_asset_class_context is not None
            and type(self.generic_asset_class_context) is not GenericAssetClassContext
        ):
            raise TypeError(
                "generic_asset_class_context must be GenericAssetClassContext"
            )
        if (
            self.authority_evidence is not None
            and type(self.authority_evidence) is not AuthorityEvidence
        ):
            raise TypeError("authority_evidence must be AuthorityEvidence")


@dataclass(frozen=True)
class Decision:
    outcome: Outcome
    reason_code: ReasonCode
    required_action: RequiredAction
    crypto_reference: str
    eligibility_evidence_reference: str
    correlation_reference: str

    def __post_init__(self) -> None:
        _require_exact(self.outcome, Outcome, "outcome")
        _require_exact(self.reason_code, ReasonCode, "reason_code")
        _require_exact(self.required_action, RequiredAction, "required_action")
        if self.required_action not in _EMITTABLE_ACTIONS:
            raise ValueError("required_action is not emittable")
        _require_reference(self.crypto_reference, "crypto_reference")
        _require_reference(
            self.eligibility_evidence_reference,
            "eligibility_evidence_reference",
        )
        _require_reference(self.correlation_reference, "correlation_reference")


def create_request(**values: object) -> CryptoEligibilityRequest:
    """Construct one strictly typed request without coercion or evaluation."""
    if (
        "generic_asset_class_context" in values
        and values["generic_asset_class_context"] is None
    ):
        raise TypeError("explicit generic_asset_class_context=None is not accepted")
    if "authority_evidence" in values and values["authority_evidence"] is None:
        raise TypeError("explicit authority_evidence=None is not accepted")
    return CryptoEligibilityRequest(**values)


def _generic_reason(context: GenericAssetClassContext) -> ReasonCode | None:
    if context.contradictory:
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY
    if context.validity is Validity.AMBIGUOUS:
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID
    if context.validity is Validity.INVALID:
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID
    if context.asset_class is not AssetClass.CRYPTO:
        return ReasonCode.GENERIC_ASSET_CLASS_NOT_CRYPTO
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
    request: CryptoEligibilityRequest,
    outcome: Outcome,
    reason: ReasonCode,
    action: RequiredAction,
) -> Decision:
    return Decision(
        outcome=outcome,
        reason_code=reason,
        required_action=action,
        crypto_reference=request.crypto_reference,
        eligibility_evidence_reference=request.eligibility_evidence_reference,
        correlation_reference=request.correlation_reference,
    )


def evaluate(request: CryptoEligibilityRequest) -> Decision:
    """Evaluate one typed request using the governed first-match order."""
    if type(request) is not CryptoEligibilityRequest:
        raise TypeError("request must be CryptoEligibilityRequest")
    if request.eligibility_evidence_contradictory:
        return _decision(
            request,
            Outcome.REVIEW_REQUIRED,
            ReasonCode.CRYPTO_ELIGIBILITY_EVIDENCE_CONTRADICTORY,
            RequiredAction.HUMAN_REVIEW,
        )
    if request.crypto_eligible and request.crypto_excluded:
        return _decision(
            request,
            Outcome.REVIEW_REQUIRED,
            ReasonCode.CRYPTO_ELIGIBLE_EXCLUDED_CONFLICT,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if request.crypto_eligible and request.crypto_restricted:
        return _decision(
            request,
            Outcome.RESTRICTED,
            ReasonCode.CRYPTO_ELIGIBLE_RESTRICTED_CONFLICT,
            RequiredAction.HUMAN_REVIEW,
        )
    undefined = (
        not request.eligibility_evidence_present
        and request.eligibility_evidence_current
    ) or (
        not request.eligibility_evidence_present
        and request.eligibility_evidence_sufficient
    ) or (
        not request.eligibility_evidence_current
        and request.eligibility_evidence_sufficient
    )
    if undefined:
        return _decision(
            request,
            Outcome.REVIEW_REQUIRED,
            ReasonCode.UNDEFINED_INPUT_COMBINATION,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if request.crypto_lane_confirmation is None:
        return _decision(
            request,
            Outcome.REVIEW_REQUIRED,
            ReasonCode.CRYPTO_LANE_CONFIRMATION_MISSING,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if request.crypto_lane_confirmation is CryptoLaneConfirmation.CONTRADICTORY:
        return _decision(
            request,
            Outcome.REVIEW_REQUIRED,
            ReasonCode.CRYPTO_LANE_CONTRADICTORY,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if request.crypto_lane_confirmation is CryptoLaneConfirmation.NOT_CONFIRMED:
        return _decision(
            request,
            Outcome.REVIEW_REQUIRED,
            ReasonCode.CRYPTO_LANE_NOT_CONFIRMED,
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
    if request.crypto_excluded:
        return _decision(
            request,
            Outcome.EXCLUDED,
            ReasonCode.CRYPTO_EXCLUDED,
            RequiredAction.NONE,
        )
    if request.crypto_restricted:
        return _decision(
            request,
            Outcome.RESTRICTED,
            ReasonCode.CRYPTO_RESTRICTED,
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
            ReasonCode.CRYPTO_ELIGIBILITY_EVIDENCE_MISSING,
            RequiredAction.HUMAN_REVIEW,
        )
    if not request.eligibility_evidence_current:
        return _decision(
            request,
            Outcome.REVIEW_REQUIRED,
            ReasonCode.CRYPTO_ELIGIBILITY_EVIDENCE_STALE,
            RequiredAction.HUMAN_REVIEW,
        )
    if not request.eligibility_evidence_sufficient:
        return _decision(
            request,
            Outcome.REVIEW_REQUIRED,
            ReasonCode.CRYPTO_ELIGIBILITY_EVIDENCE_INSUFFICIENT,
            RequiredAction.HUMAN_REVIEW,
        )
    if request.crypto_eligible:
        return _decision(
            request,
            Outcome.ELIGIBLE,
            ReasonCode.CRYPTO_ELIGIBLE,
            RequiredAction.NONE,
        )
    return _decision(
        request,
        Outcome.REVIEW_REQUIRED,
        ReasonCode.CRYPTO_ELIGIBILITY_UNRESOLVED,
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
    "CryptoEligibilityRequest",
    "CryptoLaneConfirmation",
    "Validity",
    "create_request",
    "evaluate",
]
