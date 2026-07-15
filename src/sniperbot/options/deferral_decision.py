"""Pure, deterministic SniperBot options deferral/no-action evaluator."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Outcome(str, Enum):
    DEFER = "DEFER"
    NO_ACTION = "NO_ACTION"


class ReasonCode(str, Enum):
    OPTIONS_DEFERRAL_EXTERNALLY_REQUIRED = "OPTIONS_DEFERRAL_EXTERNALLY_REQUIRED"
    OPTIONS_EVIDENCE_MISSING = "OPTIONS_EVIDENCE_MISSING"
    OPTIONS_EVIDENCE_STALE = "OPTIONS_EVIDENCE_STALE"
    OPTIONS_EVIDENCE_INSUFFICIENT = "OPTIONS_EVIDENCE_INSUFFICIENT"
    OPTIONS_EVIDENCE_CONTRADICTORY = "OPTIONS_EVIDENCE_CONTRADICTORY"
    OPTIONS_DEFERRAL_NO_ACTION_CONFLICT = "OPTIONS_DEFERRAL_NO_ACTION_CONFLICT"
    OPTIONS_RESTRICTED = "OPTIONS_RESTRICTED"
    OPTIONS_EXCLUDED = "OPTIONS_EXCLUDED"
    OPTIONS_LANE_CONFIRMATION_MISSING = "OPTIONS_LANE_CONFIRMATION_MISSING"
    OPTIONS_LANE_NOT_CONFIRMED = "OPTIONS_LANE_NOT_CONFIRMED"
    OPTIONS_LANE_CONTRADICTORY = "OPTIONS_LANE_CONTRADICTORY"
    GENERIC_ASSET_CLASS_CONTEXT_INVALID = "GENERIC_ASSET_CLASS_CONTEXT_INVALID"
    GENERIC_ASSET_CLASS_CONTEXT_STALE = "GENERIC_ASSET_CLASS_CONTEXT_STALE"
    GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY = "GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY"
    GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE = "GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE"
    GENERIC_ASSET_CLASS_NOT_OPTIONS = "GENERIC_ASSET_CLASS_NOT_OPTIONS"
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


class OptionsLaneConfirmation(str, Enum):
    CONFIRMED = "CONFIRMED"
    NOT_CONFIRMED = "NOT_CONFIRMED"
    CONTRADICTORY = "CONTRADICTORY"


class AssetClass(str, Enum):
    STOCK = "STOCK"
    OPTIONS = "OPTIONS"
    CRYPTO = "CRYPTO"


_VALIDITY = {"VALID", "INVALID", "AMBIGUOUS"}
_EMITTABLE_ACTIONS = frozenset(
    {RequiredAction.NONE, RequiredAction.HUMAN_REVIEW, RequiredAction.GOVERNANCE_REVIEW}
)


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
class OptionsRequest:
    options_reference: str
    options_evidence_present: bool
    options_evidence_current: bool
    options_evidence_sufficient: bool
    options_evidence_contradictory: bool
    options_deferral: bool
    options_no_action: bool
    options_restricted: bool
    options_excluded: bool
    correlation_reference: str
    options_lane_confirmation: OptionsLaneConfirmation | None = None
    generic_asset_class_context: GenericAssetClassContext | None = None
    authority_evidence: AuthorityEvidence | None = None

    def __post_init__(self) -> None:
        if not self.options_reference or not self.correlation_reference:
            raise ValueError("opaque references are required")
        for name in (
            "options_evidence_present",
            "options_evidence_current",
            "options_evidence_sufficient",
            "options_evidence_contradictory",
            "options_deferral",
            "options_no_action",
            "options_restricted",
            "options_excluded",
        ):
            if not isinstance(getattr(self, name), bool):
                raise ValueError(f"{name} must be a boolean")
        if self.options_lane_confirmation is not None and not isinstance(
            self.options_lane_confirmation, OptionsLaneConfirmation
        ):
            raise ValueError("invalid options lane confirmation")
        if self.generic_asset_class_context is not None and not isinstance(
            self.generic_asset_class_context, GenericAssetClassContext
        ):
            raise ValueError("invalid generic asset-class context")
        if self.authority_evidence is not None and not isinstance(
            self.authority_evidence, AuthorityEvidence
        ):
            raise ValueError("invalid authority evidence")


@dataclass(frozen=True)
class Decision:
    options_reference: str
    outcome: Outcome
    reason_code: ReasonCode
    required_action: RequiredAction
    correlation_reference: str

    def __post_init__(self) -> None:
        if not isinstance(self.outcome, Outcome):
            raise ValueError("invalid outcome")
        if not isinstance(self.reason_code, ReasonCode):
            raise ValueError("invalid reason code")
        if (
            not isinstance(self.required_action, RequiredAction)
            or self.required_action not in _EMITTABLE_ACTIONS
        ):
            raise ValueError("required action is not emittable by this subject")
        if not self.options_reference or not self.correlation_reference:
            raise ValueError("opaque references are required")


def create_request(**values: object) -> OptionsRequest:
    """Create one typed request without coercing raw values."""
    return OptionsRequest(**values)  # type: ignore[arg-type]


def _decision(
    request: OptionsRequest,
    outcome: Outcome,
    reason: ReasonCode,
    action: RequiredAction,
) -> Decision:
    return Decision(
        request.options_reference,
        outcome,
        reason,
        action,
        request.correlation_reference,
    )


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
    if context.validity == "AMBIGUOUS":
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID
    if context.validity == "INVALID":
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_INVALID
    if context.asset_class is not AssetClass.OPTIONS:
        return ReasonCode.GENERIC_ASSET_CLASS_NOT_OPTIONS
    if not context.current:
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_STALE
    if not context.in_scope:
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE
    return None


def evaluate(request: OptionsRequest) -> Decision:
    """Evaluate external options facts using the approved first-match order."""
    if not isinstance(request, OptionsRequest):
        raise TypeError("request must be an OptionsRequest")
    if request.options_evidence_contradictory:
        return _decision(
            request,
            Outcome.NO_ACTION,
            ReasonCode.OPTIONS_EVIDENCE_CONTRADICTORY,
            RequiredAction.HUMAN_REVIEW,
        )
    if request.options_deferral and request.options_no_action:
        return _decision(
            request,
            Outcome.NO_ACTION,
            ReasonCode.OPTIONS_DEFERRAL_NO_ACTION_CONFLICT,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if (
        (not request.options_evidence_present and request.options_evidence_current)
        or (not request.options_evidence_present and request.options_evidence_sufficient)
        or (not request.options_evidence_current and request.options_evidence_sufficient)
    ):
        return _decision(
            request,
            Outcome.NO_ACTION,
            ReasonCode.UNDEFINED_INPUT_COMBINATION,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if request.options_lane_confirmation is None:
        return _decision(
            request,
            Outcome.NO_ACTION,
            ReasonCode.OPTIONS_LANE_CONFIRMATION_MISSING,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if request.options_lane_confirmation is OptionsLaneConfirmation.CONTRADICTORY:
        return _decision(
            request,
            Outcome.NO_ACTION,
            ReasonCode.OPTIONS_LANE_CONTRADICTORY,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if request.options_lane_confirmation is OptionsLaneConfirmation.NOT_CONFIRMED:
        return _decision(
            request,
            Outcome.NO_ACTION,
            ReasonCode.OPTIONS_LANE_NOT_CONFIRMED,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if request.generic_asset_class_context is not None:
        reason = _generic_reason(request.generic_asset_class_context)
        if reason is not None:
            return _decision(
                request, Outcome.NO_ACTION, reason, RequiredAction.GOVERNANCE_REVIEW
            )
    if request.options_excluded:
        return _decision(
            request,
            Outcome.NO_ACTION,
            ReasonCode.OPTIONS_EXCLUDED,
            RequiredAction.NONE,
        )
    if request.options_restricted:
        return _decision(
            request,
            Outcome.NO_ACTION,
            ReasonCode.OPTIONS_RESTRICTED,
            RequiredAction.NONE,
        )
    if request.authority_evidence is not None:
        reason = _authority_reason(request.authority_evidence)
        if reason is not None:
            return _decision(
                request, Outcome.NO_ACTION, reason, RequiredAction.GOVERNANCE_REVIEW
            )
    if not request.options_evidence_present:
        return _decision(
            request,
            Outcome.DEFER,
            ReasonCode.OPTIONS_EVIDENCE_MISSING,
            RequiredAction.HUMAN_REVIEW,
        )
    if not request.options_evidence_current:
        return _decision(
            request,
            Outcome.DEFER,
            ReasonCode.OPTIONS_EVIDENCE_STALE,
            RequiredAction.HUMAN_REVIEW,
        )
    if not request.options_evidence_sufficient:
        return _decision(
            request,
            Outcome.DEFER,
            ReasonCode.OPTIONS_EVIDENCE_INSUFFICIENT,
            RequiredAction.HUMAN_REVIEW,
        )
    if request.options_deferral:
        return _decision(
            request,
            Outcome.DEFER,
            ReasonCode.OPTIONS_DEFERRAL_EXTERNALLY_REQUIRED,
            RequiredAction.HUMAN_REVIEW,
        )
    if request.options_no_action:
        return _decision(
            request,
            Outcome.NO_ACTION,
            ReasonCode.NO_ACTION_REQUIRED,
            RequiredAction.NONE,
        )
    return _decision(
        request,
        Outcome.NO_ACTION,
        ReasonCode.NO_ACTION_REQUIRED,
        RequiredAction.NONE,
    )
