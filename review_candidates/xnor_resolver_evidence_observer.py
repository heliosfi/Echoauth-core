"""Test-only observer for real gate resolver output versus untrusted XNOR claims.

Observer does not change gate decision path, authenticate XNOR evidence,
or grant any authority. Use only in isolated test instrumentation.
"""
from dataclasses import dataclass
from enum import Enum


class ObservationState(str, Enum):
    MATCHED_FOR_REVIEW = "MATCHED_FOR_REVIEW"
    HOLD = "HOLD"


@dataclass(frozen=True)
class ClaimedEvidence:
    authority_record_id: str
    grantor_id: str
    subject_id: str
    action: str
    resource: str


@dataclass(frozen=True)
class Observation:
    state: ObservationState
    reason: str
    authority_granted: bool = False
    execution_authorized: bool = False


def observe_resolver_binding(resolution_request, resolution, claimed):
    def hold(reason):
        return Observation(ObservationState.HOLD, reason)
    if resolution_request is None or resolution is None or not isinstance(claimed, ClaimedEvidence):
        return hold("missing_evidence")
    if getattr(resolution, "outcome", None) is None or getattr(resolution, "outcome").value != "authorized":
        return hold("resolver_not_authorized")
    actual = {
        "authority_record_id": getattr(resolution, "authority_record_id", None),
        "grantor_id": getattr(resolution_request, "requester_id", None),
        "subject_id": getattr(resolution_request, "subject_id", None),
        "action": getattr(resolution_request, "action", None),
        "resource": getattr(resolution_request, "resource", None),
    }
    for field, resolved in actual.items():
        claimed_value = getattr(claimed, field)
        if not isinstance(resolved, str) or not resolved or claimed_value != resolved:
            return hold(field + "_mismatch")
    return Observation(ObservationState.MATCHED_FOR_REVIEW,
                       "real_resolver_fields_match_untrusted_claim_only")
