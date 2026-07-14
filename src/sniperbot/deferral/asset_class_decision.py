"""Pure, deterministic Asset-Class Deferral / No-Action evaluator."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AssetClass(str, Enum):
    STOCK = "STOCK"
    OPTIONS = "OPTIONS"
    CRYPTO = "CRYPTO"


class Outcome(str, Enum):
    DEFER = "DEFER"
    NO_ACTION = "NO_ACTION"


class ReasonCode(str, Enum):
    EXTERNAL_DEFERRAL_REQUIRED = "EXTERNAL_DEFERRAL_REQUIRED"
    NO_ACTION_REQUIRED = "NO_ACTION_REQUIRED"
    EVIDENCE_MISSING = "EVIDENCE_MISSING"
    EVIDENCE_STALE = "EVIDENCE_STALE"
    EVIDENCE_INSUFFICIENT = "EVIDENCE_INSUFFICIENT"
    EVIDENCE_CONTRADICTORY = "EVIDENCE_CONTRADICTORY"
    EXTERNALLY_EXCLUDED = "EXTERNALLY_EXCLUDED"
    AUTHORITY_EVIDENCE_INVALID = "AUTHORITY_EVIDENCE_INVALID"
    AUTHORITY_EVIDENCE_STALE = "AUTHORITY_EVIDENCE_STALE"
    AUTHORITY_EVIDENCE_REVOKED = "AUTHORITY_EVIDENCE_REVOKED"
    AUTHORITY_EVIDENCE_OUT_OF_SCOPE = "AUTHORITY_EVIDENCE_OUT_OF_SCOPE"
    UNKNOWN_ASSET_CLASS = "UNKNOWN_ASSET_CLASS"
    UNDEFINED_INPUT_COMBINATION = "UNDEFINED_INPUT_COMBINATION"


class RequiredAction(str, Enum):
    NONE = "NONE"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    GOVERNANCE_REVIEW = "GOVERNANCE_REVIEW"
    FOUNDER_AUTHORITY_REQUIRED = "FOUNDER_AUTHORITY_REQUIRED"
    RESET_REQUIRED = "RESET_REQUIRED"


_VALIDITY = {"VALID", "INVALID", "AMBIGUOUS"}
_CURRENTNESS = {"CURRENT", "STALE"}
_REVOCATION = {"NON_REVOKED", "REVOKED"}
_SCOPE = {"IN_SCOPE", "OUT_OF_SCOPE", "AMBIGUOUS"}


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
class DeferralRequest:
    asset_class: AssetClass
    evidence_present: bool
    evidence_current: bool
    evidence_sufficient: bool
    evidence_contradictory: bool
    eligibility_status: bool | None
    exclusion_status: bool | None
    explicit_deferral_required: bool
    authority_evidence: AuthorityEvidence | None
    correlation_reference: str

    def __post_init__(self) -> None:
        if not isinstance(self.asset_class, AssetClass):
            raise ValueError("asset_class must be a supported AssetClass")
        if not isinstance(self.authority_evidence, (AuthorityEvidence, type(None))):
            raise ValueError("authority_evidence must be AuthorityEvidence or None")
        if not self.correlation_reference:
            raise ValueError("correlation_reference is required")


@dataclass(frozen=True)
class Decision:
    asset_class: AssetClass
    outcome: Outcome
    reason_code: ReasonCode
    required_action: RequiredAction
    correlation_reference: str


def create_request(asset_class: str | AssetClass, **kwargs: object) -> DeferralRequest:
    """Construct a typed request; unknown raw asset classes are rejected first."""
    if not isinstance(asset_class, AssetClass):
        try:
            asset_class = AssetClass(asset_class)
        except (TypeError, ValueError) as exc:
            raise ValueError("unknown raw asset class") from exc
    return DeferralRequest(asset_class=asset_class, **kwargs)


def _authority_reason(evidence: AuthorityEvidence) -> ReasonCode | None:
    if evidence.validity == "AMBIGUOUS":
        return ReasonCode.AUTHORITY_EVIDENCE_INVALID
    if evidence.validity == "INVALID":
        return ReasonCode.AUTHORITY_EVIDENCE_INVALID
    if evidence.revocation == "REVOKED":
        return ReasonCode.AUTHORITY_EVIDENCE_REVOKED
    if evidence.currentness == "STALE":
        return ReasonCode.AUTHORITY_EVIDENCE_STALE
    if evidence.scope in {"OUT_OF_SCOPE", "AMBIGUOUS"}:
        return ReasonCode.AUTHORITY_EVIDENCE_OUT_OF_SCOPE
    return None


def _result(request: DeferralRequest, outcome: Outcome, reason: ReasonCode,
            action: RequiredAction) -> Decision:
    return Decision(request.asset_class, outcome, reason, action, request.correlation_reference)


def evaluate(request: DeferralRequest) -> Decision:
    """Evaluate one typed request using the approved first-match order."""
    if not isinstance(request, DeferralRequest):
        raise TypeError("request must be a DeferralRequest")
    if request.evidence_contradictory:
        return _result(request, Outcome.NO_ACTION, ReasonCode.EVIDENCE_CONTRADICTORY, RequiredAction.HUMAN_REVIEW)
    undefined = (
        (not request.evidence_present and request.evidence_current)
        or (not request.evidence_present and request.evidence_sufficient)
        or (not request.evidence_current and request.evidence_sufficient)
        or (request.eligibility_status is True and request.exclusion_status is True)
    )
    if undefined:
        return _result(request, Outcome.NO_ACTION, ReasonCode.UNDEFINED_INPUT_COMBINATION, RequiredAction.GOVERNANCE_REVIEW)
    if request.exclusion_status is True:
        return _result(request, Outcome.NO_ACTION, ReasonCode.EXTERNALLY_EXCLUDED, RequiredAction.NONE)
    if request.authority_evidence is not None:
        reason = _authority_reason(request.authority_evidence)
        if reason is not None:
            return _result(request, Outcome.NO_ACTION, reason, RequiredAction.GOVERNANCE_REVIEW)
    if not request.evidence_present:
        return _result(request, Outcome.DEFER, ReasonCode.EVIDENCE_MISSING, RequiredAction.HUMAN_REVIEW)
    if not request.evidence_current:
        return _result(request, Outcome.DEFER, ReasonCode.EVIDENCE_STALE, RequiredAction.HUMAN_REVIEW)
    if not request.evidence_sufficient:
        return _result(request, Outcome.DEFER, ReasonCode.EVIDENCE_INSUFFICIENT, RequiredAction.HUMAN_REVIEW)
    if request.explicit_deferral_required:
        return _result(request, Outcome.DEFER, ReasonCode.EXTERNAL_DEFERRAL_REQUIRED, RequiredAction.NONE)
    return _result(request, Outcome.NO_ACTION, ReasonCode.NO_ACTION_REQUIRED, RequiredAction.NONE)
