"""Pure, deterministic SniperBot crypto deferral/no-action evaluator."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Outcome(str, Enum):
    DEFER = "DEFER"
    NO_ACTION = "NO_ACTION"


class ReasonCode(str, Enum):
    CRYPTO_DEFERRAL_EXTERNALLY_REQUIRED = "CRYPTO_DEFERRAL_EXTERNALLY_REQUIRED"
    CRYPTO_EVIDENCE_MISSING = "CRYPTO_EVIDENCE_MISSING"
    CRYPTO_EVIDENCE_STALE = "CRYPTO_EVIDENCE_STALE"
    CRYPTO_EVIDENCE_INSUFFICIENT = "CRYPTO_EVIDENCE_INSUFFICIENT"
    CRYPTO_EVIDENCE_CONTRADICTORY = "CRYPTO_EVIDENCE_CONTRADICTORY"
    CRYPTO_DEFERRAL_NO_ACTION_CONFLICT = "CRYPTO_DEFERRAL_NO_ACTION_CONFLICT"
    CRYPTO_RESTRICTED = "CRYPTO_RESTRICTED"
    CRYPTO_EXCLUDED = "CRYPTO_EXCLUDED"
    CRYPTO_LANE_CONFIRMATION_MISSING = "CRYPTO_LANE_CONFIRMATION_MISSING"
    CRYPTO_LANE_NOT_CONFIRMED = "CRYPTO_LANE_NOT_CONFIRMED"
    CRYPTO_LANE_CONTRADICTORY = "CRYPTO_LANE_CONTRADICTORY"
    GENERIC_ASSET_CLASS_CONTEXT_INVALID = "GENERIC_ASSET_CLASS_CONTEXT_INVALID"
    GENERIC_ASSET_CLASS_CONTEXT_STALE = "GENERIC_ASSET_CLASS_CONTEXT_STALE"
    GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY = "GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY"
    GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE = "GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE"
    GENERIC_ASSET_CLASS_NOT_CRYPTO = "GENERIC_ASSET_CLASS_NOT_CRYPTO"
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


class CryptoLaneConfirmation(str, Enum):
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
class CryptoRequest:
    crypto_reference: str
    crypto_evidence_present: bool
    crypto_evidence_current: bool
    crypto_evidence_sufficient: bool
    crypto_evidence_contradictory: bool
    crypto_deferral: bool
    crypto_no_action: bool
    crypto_restricted: bool
    crypto_excluded: bool
    correlation_reference: str
    crypto_lane_confirmation: CryptoLaneConfirmation | None = None
    generic_asset_class_context: GenericAssetClassContext | None = None
    authority_evidence: AuthorityEvidence | None = None

    def __post_init__(self) -> None:
        if not self.crypto_reference or not self.correlation_reference:
            raise ValueError("opaque references are required")
        for name in (
            "crypto_evidence_present",
            "crypto_evidence_current",
            "crypto_evidence_sufficient",
            "crypto_evidence_contradictory",
            "crypto_deferral",
            "crypto_no_action",
            "crypto_restricted",
            "crypto_excluded",
        ):
            if not isinstance(getattr(self, name), bool):
                raise ValueError(f"{name} must be a boolean")
        if self.crypto_lane_confirmation is not None and not isinstance(
            self.crypto_lane_confirmation, CryptoLaneConfirmation
        ):
            raise ValueError("invalid crypto lane confirmation")
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
    crypto_reference: str
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
        if not self.crypto_reference or not self.correlation_reference:
            raise ValueError("opaque references are required")


def create_request(**values: object) -> CryptoRequest:
    """Create one typed request without coercing raw values."""
    return CryptoRequest(**values)  # type: ignore[arg-type]


def _decision(
    request: CryptoRequest,
    outcome: Outcome,
    reason: ReasonCode,
    action: RequiredAction,
) -> Decision:
    return Decision(
        request.crypto_reference,
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
    if context.asset_class is not AssetClass.CRYPTO:
        return ReasonCode.GENERIC_ASSET_CLASS_NOT_CRYPTO
    if not context.current:
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_STALE
    if not context.in_scope:
        return ReasonCode.GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE
    return None


def evaluate(request: CryptoRequest) -> Decision:
    """Evaluate external crypto facts using the approved first-match order."""
    if not isinstance(request, CryptoRequest):
        raise TypeError("request must be an CryptoRequest")
    if request.crypto_evidence_contradictory:
        return _decision(
            request,
            Outcome.NO_ACTION,
            ReasonCode.CRYPTO_EVIDENCE_CONTRADICTORY,
            RequiredAction.HUMAN_REVIEW,
        )
    if request.crypto_deferral and request.crypto_no_action:
        return _decision(
            request,
            Outcome.NO_ACTION,
            ReasonCode.CRYPTO_DEFERRAL_NO_ACTION_CONFLICT,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if (
        (not request.crypto_evidence_present and request.crypto_evidence_current)
        or (not request.crypto_evidence_present and request.crypto_evidence_sufficient)
        or (not request.crypto_evidence_current and request.crypto_evidence_sufficient)
    ):
        return _decision(
            request,
            Outcome.NO_ACTION,
            ReasonCode.UNDEFINED_INPUT_COMBINATION,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if request.crypto_lane_confirmation is None:
        return _decision(
            request,
            Outcome.NO_ACTION,
            ReasonCode.CRYPTO_LANE_CONFIRMATION_MISSING,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if request.crypto_lane_confirmation is CryptoLaneConfirmation.CONTRADICTORY:
        return _decision(
            request,
            Outcome.NO_ACTION,
            ReasonCode.CRYPTO_LANE_CONTRADICTORY,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if request.crypto_lane_confirmation is CryptoLaneConfirmation.NOT_CONFIRMED:
        return _decision(
            request,
            Outcome.NO_ACTION,
            ReasonCode.CRYPTO_LANE_NOT_CONFIRMED,
            RequiredAction.GOVERNANCE_REVIEW,
        )
    if request.generic_asset_class_context is not None:
        reason = _generic_reason(request.generic_asset_class_context)
        if reason is not None:
            return _decision(
                request, Outcome.NO_ACTION, reason, RequiredAction.GOVERNANCE_REVIEW
            )
    if request.crypto_excluded:
        return _decision(
            request,
            Outcome.NO_ACTION,
            ReasonCode.CRYPTO_EXCLUDED,
            RequiredAction.NONE,
        )
    if request.crypto_restricted:
        return _decision(
            request,
            Outcome.NO_ACTION,
            ReasonCode.CRYPTO_RESTRICTED,
            RequiredAction.NONE,
        )
    if request.authority_evidence is not None:
        reason = _authority_reason(request.authority_evidence)
        if reason is not None:
            return _decision(
                request, Outcome.NO_ACTION, reason, RequiredAction.GOVERNANCE_REVIEW
            )
    if not request.crypto_evidence_present:
        return _decision(
            request,
            Outcome.DEFER,
            ReasonCode.CRYPTO_EVIDENCE_MISSING,
            RequiredAction.HUMAN_REVIEW,
        )
    if not request.crypto_evidence_current:
        return _decision(
            request,
            Outcome.DEFER,
            ReasonCode.CRYPTO_EVIDENCE_STALE,
            RequiredAction.HUMAN_REVIEW,
        )
    if not request.crypto_evidence_sufficient:
        return _decision(
            request,
            Outcome.DEFER,
            ReasonCode.CRYPTO_EVIDENCE_INSUFFICIENT,
            RequiredAction.HUMAN_REVIEW,
        )
    if request.crypto_deferral:
        return _decision(
            request,
            Outcome.DEFER,
            ReasonCode.CRYPTO_DEFERRAL_EXTERNALLY_REQUIRED,
            RequiredAction.HUMAN_REVIEW,
        )
    if request.crypto_no_action:
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
