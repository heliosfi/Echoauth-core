"""Pure, deterministic SniperBot stock deferral/no-action evaluator."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Outcome(str, Enum):
    DEFER = "DEFER"
    NO_ACTION = "NO_ACTION"


class ReasonCode(str, Enum):
    STOCK_DEFERRAL_EXTERNALLY_REQUIRED = "STOCK_DEFERRAL_EXTERNALLY_REQUIRED"
    STOCK_EVIDENCE_MISSING = "STOCK_EVIDENCE_MISSING"
    STOCK_EVIDENCE_STALE = "STOCK_EVIDENCE_STALE"
    STOCK_EVIDENCE_INSUFFICIENT = "STOCK_EVIDENCE_INSUFFICIENT"
    STOCK_EVIDENCE_CONTRADICTORY = "STOCK_EVIDENCE_CONTRADICTORY"
    STOCK_DEFERRAL_NO_ACTION_CONFLICT = "STOCK_DEFERRAL_NO_ACTION_CONFLICT"
    STOCK_RESTRICTED = "STOCK_RESTRICTED"
    STOCK_EXCLUDED = "STOCK_EXCLUDED"
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
    NO_ACTION_REQUIRED = "NO_ACTION_REQUIRED"


EmittableReasonCode = Enum(
    "EmittableReasonCode",
    {reason.name: reason.value for reason in ReasonCode},
    type=str,
)


class RequiredAction(str, Enum):
    NONE = "NONE"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    GOVERNANCE_REVIEW = "GOVERNANCE_REVIEW"
    FOUNDER_AUTHORITY_REQUIRED = "FOUNDER_AUTHORITY_REQUIRED"
    RESET_REQUIRED = "RESET_REQUIRED"


class StockLaneConfirmation(str, Enum):
    CONFIRMED = "CONFIRMED"
    NOT_CONFIRMED = "NOT_CONFIRMED"
    CONTRADICTORY = "CONTRADICTORY"


class AssetClass(str, Enum):
    STOCK = "STOCK"
    OPTIONS = "OPTIONS"
    CRYPTO = "CRYPTO"


_VALIDITY = {"VALID", "INVALID", "AMBIGUOUS"}
_EMITTABLE_ACTIONS = frozenset({RequiredAction.NONE, RequiredAction.HUMAN_REVIEW,
                                RequiredAction.GOVERNANCE_REVIEW})


@dataclass(frozen=True)
class GenericAssetClassContext:
    asset_class: AssetClass
    validity: str
    current: bool
    contradictory: bool
    in_scope: bool
    context_reference: str

    def __post_init__(self) -> None:
        if not isinstance(self.asset_class, AssetClass):
            raise ValueError("asset_class must be an AssetClass")
        if self.validity not in _VALIDITY:
            raise ValueError("invalid generic context validity")
        for name in ("current", "contradictory", "in_scope"):
            if not isinstance(getattr(self, name), bool):
                raise ValueError(f"{name} must be a boolean")
        if not self.context_reference:
            raise ValueError("context_reference is required")


@dataclass(frozen=True)
class AuthorityEvidence:
    validity: str
    current: bool
    revoked: bool
    contradictory: bool
    in_scope: bool
    evidence_reference: str

    def __post_init__(self) -> None:
        if self.validity not in _VALIDITY:
            raise ValueError("invalid authority validity")
        for name in ("current", "revoked", "contradictory", "in_scope"):
            if not isinstance(getattr(self, name), bool):
                raise ValueError(f"{name} must be a boolean")
        if not self.evidence_reference:
            raise ValueError("evidence_reference is required")


@dataclass(frozen=True)
class StockRequest:
    stock_reference: str
    stock_evidence_present: bool
    stock_evidence_current: bool
    stock_evidence_sufficient: bool
    stock_evidence_contradictory: bool
    stock_deferral: bool
    stock_no_action: bool
    stock_restricted: bool
    stock_excluded: bool
    correlation_reference: str
    stock_lane_confirmation: StockLaneConfirmation | None = None
    generic_asset_class_context: GenericAssetClassContext | None = None
    authority_evidence: AuthorityEvidence | None = None

    def __post_init__(self) -> None:
        if not self.stock_reference or not self.correlation_reference:
            raise ValueError("opaque references are required")
        for name in ("stock_evidence_present", "stock_evidence_current",
                     "stock_evidence_sufficient", "stock_evidence_contradictory",
                     "stock_deferral", "stock_no_action", "stock_restricted",
                     "stock_excluded"):
            if not isinstance(getattr(self, name), bool):
                raise ValueError(f"{name} must be a boolean")
        if self.stock_lane_confirmation is not None and not isinstance(self.stock_lane_confirmation, StockLaneConfirmation):
            raise ValueError("invalid stock lane confirmation")
        if self.generic_asset_class_context is not None and not isinstance(self.generic_asset_class_context, GenericAssetClassContext):
            raise ValueError("invalid generic asset-class context")
        if self.authority_evidence is not None and not isinstance(self.authority_evidence, AuthorityEvidence):
            raise ValueError("invalid authority evidence")


@dataclass(frozen=True)
class Decision:
    stock_reference: str
    outcome: Outcome
    reason_code: ReasonCode
    required_action: RequiredAction
    correlation_reference: str

    def __post_init__(self) -> None:
        if not isinstance(self.outcome, Outcome):
            raise ValueError("invalid outcome")
        if not isinstance(self.reason_code, ReasonCode):
            raise ValueError("invalid reason code")
        if not isinstance(self.required_action, RequiredAction) or self.required_action not in _EMITTABLE_ACTIONS:
            raise ValueError("required action is not emittable by this subject")
        if not self.stock_reference or not self.correlation_reference:
            raise ValueError("opaque references are required")


def create_request(**values: object) -> StockRequest:
    """Create a typed request, rejecting unknown raw enum values first."""
    lane = values.get("stock_lane_confirmation")
    if lane is not None and not isinstance(lane, StockLaneConfirmation):
        try:
            values["stock_lane_confirmation"] = StockLaneConfirmation(lane)
        except (TypeError, ValueError) as exc:
            raise ValueError("unknown raw stock lane confirmation") from exc
    return StockRequest(**values)  # type: ignore[arg-type]


def _decision(request: StockRequest, outcome: Outcome, reason: ReasonCode,
              action: RequiredAction) -> Decision:
    return Decision(request.stock_reference, outcome, reason, action,
                    request.correlation_reference)


def _authority_reason(evidence: AuthorityEvidence) -> ReasonCode | None:
    if evidence.contradictory:
        return ReasonCode.AUTHORITY_EVIDENCE_INVALID
    if evidence.validity == "AMBIGUOUS":
        return ReasonCode.AUTHORITY_EVIDENCE_INVALID
    if evidence.validity == "INVALID":
        return ReasonCode.AUTHORITY_EVIDENCE_INVALID
    if evidence.revoked:
        return ReasonCode.AUTHORITY_EVIDENCE_REVOKED
    if not evidence.current:
        return ReasonCode.AUTHORITY_EVIDENCE_STALE
    if not evidence.in_scope:
        return ReasonCode.AUTHORITY_EVIDENCE_OUT_OF_SCOPE
    return None


def _generic_reason(context: GenericAssetClassContext) -> ReasonCode | None:
    if context.contradictory:
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY
    if context.validity == "AMBIGUOUS" or context.validity == "INVALID":
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID
    if context.asset_class is not AssetClass.STOCK:
        return ReasonCode.GENERIC_ASSET_CLASS_NOT_STOCK
    if not context.current:
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_STALE
    if not context.in_scope:
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE
    return None


def evaluate(request: StockRequest) -> Decision:
    """Evaluate external stock facts using the approved first-match order."""
    if not isinstance(request, StockRequest):
        raise TypeError("request must be a StockRequest")
    if request.stock_evidence_contradictory:
        return _decision(request, Outcome.NO_ACTION, ReasonCode.STOCK_EVIDENCE_CONTRADICTORY, RequiredAction.HUMAN_REVIEW)
    if request.stock_deferral and request.stock_no_action:
        return _decision(request, Outcome.NO_ACTION, ReasonCode.STOCK_DEFERRAL_NO_ACTION_CONFLICT, RequiredAction.GOVERNANCE_REVIEW)
    if ((not request.stock_evidence_present and request.stock_evidence_current)
            or (not request.stock_evidence_present and request.stock_evidence_sufficient)
            or (not request.stock_evidence_current and request.stock_evidence_sufficient)):
        return _decision(request, Outcome.NO_ACTION, ReasonCode.UNDEFINED_INPUT_COMBINATION, RequiredAction.GOVERNANCE_REVIEW)
    if request.stock_lane_confirmation is None:
        return _decision(request, Outcome.NO_ACTION, ReasonCode.STOCK_LANE_CONFIRMATION_MISSING, RequiredAction.GOVERNANCE_REVIEW)
    if request.stock_lane_confirmation is StockLaneConfirmation.CONTRADICTORY:
        return _decision(request, Outcome.NO_ACTION, ReasonCode.STOCK_LANE_CONTRADICTORY, RequiredAction.GOVERNANCE_REVIEW)
    if request.stock_lane_confirmation is StockLaneConfirmation.NOT_CONFIRMED:
        return _decision(request, Outcome.NO_ACTION, ReasonCode.STOCK_LANE_NOT_CONFIRMED, RequiredAction.GOVERNANCE_REVIEW)
    if request.generic_asset_class_context is not None:
        reason = _generic_reason(request.generic_asset_class_context)
        if reason is not None:
            return _decision(request, Outcome.NO_ACTION, reason, RequiredAction.GOVERNANCE_REVIEW)
    if request.stock_excluded:
        return _decision(request, Outcome.NO_ACTION, ReasonCode.STOCK_EXCLUDED, RequiredAction.NONE)
    if request.stock_restricted:
        return _decision(request, Outcome.NO_ACTION, ReasonCode.STOCK_RESTRICTED, RequiredAction.NONE)
    if request.authority_evidence is not None:
        reason = _authority_reason(request.authority_evidence)
        if reason is not None:
            return _decision(request, Outcome.NO_ACTION, reason, RequiredAction.GOVERNANCE_REVIEW)
    if not request.stock_evidence_present:
        return _decision(request, Outcome.DEFER, ReasonCode.STOCK_EVIDENCE_MISSING, RequiredAction.HUMAN_REVIEW)
    if not request.stock_evidence_current:
        return _decision(request, Outcome.DEFER, ReasonCode.STOCK_EVIDENCE_STALE, RequiredAction.HUMAN_REVIEW)
    if not request.stock_evidence_sufficient:
        return _decision(request, Outcome.DEFER, ReasonCode.STOCK_EVIDENCE_INSUFFICIENT, RequiredAction.HUMAN_REVIEW)
    if request.stock_deferral:
        return _decision(request, Outcome.DEFER, ReasonCode.STOCK_DEFERRAL_EXTERNALLY_REQUIRED, RequiredAction.HUMAN_REVIEW)
    return _decision(request, Outcome.NO_ACTION, ReasonCode.NO_ACTION_REQUIRED, RequiredAction.NONE)
