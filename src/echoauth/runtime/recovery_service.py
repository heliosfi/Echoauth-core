"""Deterministic Recovery Eligibility validation for Sprint 2P.

This module produces governance evidence only. It cannot authorize, execute,
or mutate runtime state.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import asdict
from datetime import datetime, timezone
from threading import RLock

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth.authority_resolution import (
    AuthorityResolutionOutcome,
    AuthorityResolutionResult,
)
from echoauth.canonical import CanonicalDataError, canonical_json_text, canonical_sha256
from echoauth.governance.review_models import ReviewDecision
from echoauth.models import AuditAppendState, AuditRecord
from echoauth.runtime.halt_models import HaltDecision, HaltOutcome
from echoauth.runtime.recovery_models import (
    RecoveryEligibilityRequest,
    RecoveryEligibilityResult,
    RecoveryFailureCode,
    RecoveryOutcome,
    RecoveryPath,
    RecoveryProtocolStatus,
    RecoveryReviewProtocol,
    RecoverySourceState,
)
from echoauth.persistence import MissingRecordError

RECOVERY_ELIGIBILITY_VERSION = "echoauth.recovery-eligibility.v1"
_REQUIRED_VALIDATIONS = (
    "identity",
    "authority",
    "delegation_if_applicable",
    "policy",
    "invariants",
    "audit_path",
)


class RecoveryEligibilityValidationError(ValueError):
    pass


class RecoveryEligibilityAuditError(RuntimeError):
    pass


class RecoveryEligibilityService:
    """Classify Recovery eligibility without recovering or changing state."""

    def __init__(
        self,
        audit_repository: InMemoryAuditLogRepository,
        *,
        audit_chain_id: str,
        component_id: str = "recovery_eligibility_service",
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if not audit_chain_id:
            raise ValueError("audit_chain_id must not be empty")
        if not component_id:
            raise ValueError("component_id must not be empty")
        self._audit_repository = audit_repository
        self._audit_chain_id = audit_chain_id
        self._component_id = component_id
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._cache: dict[str, RecoveryEligibilityResult] = {}
        self._lock = RLock()

    def validate(
        self,
        request: RecoveryEligibilityRequest,
        authority_resolution: AuthorityResolutionResult,
        halt_decision: HaltDecision,
        *,
        review_decision: ReviewDecision | None = None,
        review_authority_resolution: AuthorityResolutionResult | None = None,
    ) -> RecoveryEligibilityResult:
        """Return an inert eligibility result from supplied immutable evidence."""

        validate_recovery_request(request)
        evidence_input = _evidence_input(
            request,
            authority_resolution,
            halt_decision,
            review_decision,
            review_authority_resolution,
        )
        request_hash = canonical_sha256(evidence_input)
        with self._lock:
            cached = self._cache.get(request_hash)
            if cached is not None:
                return cached

            requested_audit_id = f"audit_recreq_{request_hash}"
            requested_audit = self._audit_repository.append(
                AuditRecord(
                    event_type="recovery.eligibility.requested",
                    actor_id=self._component_id,
                    request_id=request.request_id,
                    authority_verdict_id=request.authority_resolution_id,
                    reason="recovery_eligibility_requested",
                    details={
                        "authority_resolution_id": request.authority_resolution_id,
                        "changed_evidence_hash": request.changed_evidence_hash,
                        "failure_code": request.failure_code.value,
                        "halt_decision_id": request.halt_decision_id,
                        "original_failure_audit_event_id": (
                            request.original_failure_audit_event_id
                        ),
                        "original_failure_evidence_hash": (
                            request.original_failure_evidence_hash
                        ),
                        "recovery_actor_id": request.recovery_actor_id,
                        "recovery_authority_reference": (
                            request.recovery_authority_reference
                        ),
                        "recovery_id": request.recovery_id,
                        "recovery_policy_version": request.recovery_policy_version,
                        "requested_at": request.requested_at,
                        "requested_recovery_path": (
                            request.requested_recovery_path.value
                        ),
                        "source_state": request.source_state.value,
                    },
                    occurred_at=request.requested_at,
                ),
                audit_event_id=requested_audit_id,
                chain_id=self._audit_chain_id,
            )
            if requested_audit.append_state is not AuditAppendState.ACCEPTED:
                raise RecoveryEligibilityAuditError(
                    f"recovery request audit append failed: {requested_audit.reason}"
                )

            now = self._utc_now()
            outcome, reason, required_validations = _classify(
                request,
                authority_resolution,
                halt_decision,
                review_decision,
                review_authority_resolution,
                self._audit_repository,
                now,
            )
            evidence_hash = canonical_sha256(
                {
                    "eligibility_version": RECOVERY_ELIGIBILITY_VERSION,
                    "input": evidence_input,
                    "outcome": outcome.value,
                    "reason": reason,
                    "required_validations": list(required_validations),
                    "requested_audit_event_id": requested_audit_id,
                }
            )
            decision_hash = canonical_sha256(
                {
                    "evidence_hash": evidence_hash,
                    "outcome": outcome.value,
                    "recovery_id": request.recovery_id,
                    "reason": reason,
                }
            )
            recovery_decision_id = f"recdec_{decision_hash}"
            decided_audit_id = f"audit_{recovery_decision_id}"
            decided_at = _timestamp(now)
            decided_audit = self._audit_repository.append(
                AuditRecord(
                    event_type="recovery.eligibility.decided",
                    actor_id=self._component_id,
                    request_id=request.request_id,
                    authority_verdict_id=request.authority_resolution_id,
                    reason=reason,
                    details={
                        "decided_at": decided_at,
                        "evidence_hash": evidence_hash,
                        "failure_code": request.failure_code.value,
                        "outcome": outcome.value,
                        "recovery_decision_id": recovery_decision_id,
                        "recovery_id": request.recovery_id,
                        "required_validations": list(required_validations),
                        "source_state": request.source_state.value,
                    },
                    occurred_at=decided_at,
                ),
                audit_event_id=decided_audit_id,
                chain_id=self._audit_chain_id,
            )
            if decided_audit.append_state is not AuditAppendState.ACCEPTED:
                raise RecoveryEligibilityAuditError(
                    f"recovery decision audit append failed: {decided_audit.reason}"
                )
            result = RecoveryEligibilityResult(
                recovery_decision_id=recovery_decision_id,
                recovery_id=request.recovery_id,
                request_id=request.request_id,
                source_state=request.source_state,
                outcome=outcome,
                reason=reason,
                required_validations=required_validations,
                evidence_hash=evidence_hash,
                decided_at=decided_at,
                audit_event_id=decided_audit_id,
            )
            self._cache[request_hash] = result
            return result

    def _utc_now(self) -> datetime:
        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise RecoveryEligibilityValidationError(
                "recovery eligibility clock must be timezone-aware"
            )
        return now.astimezone(timezone.utc)


def validate_recovery_request(request: RecoveryEligibilityRequest) -> None:
    """Validate the canonical Recovery request schema boundary."""

    if not isinstance(request, RecoveryEligibilityRequest):
        raise RecoveryEligibilityValidationError(
            "request must be a RecoveryEligibilityRequest"
        )
    for field_name in (
        "recovery_id",
        "request_id",
        "recovery_actor_id",
        "recovery_authority_reference",
        "authority_resolution_id",
        "authority_evidence_hash",
        "halt_decision_id",
        "halt_decision_evidence_hash",
        "original_failure_evidence_hash",
        "original_failure_audit_event_id",
        "changed_evidence_reference",
        "changed_evidence_hash",
        "recovery_policy_version",
        "requested_at",
    ):
        value = getattr(request, field_name)
        if not isinstance(value, str) or not value:
            raise RecoveryEligibilityValidationError(
                f"{field_name} must be non-empty"
            )
    if not isinstance(request.source_state, RecoverySourceState):
        raise RecoveryEligibilityValidationError("source_state must be canonical")
    if not isinstance(request.failure_code, RecoveryFailureCode):
        raise RecoveryEligibilityValidationError("failure_code must be canonical")
    if not isinstance(request.requested_recovery_path, RecoveryPath):
        raise RecoveryEligibilityValidationError(
            "requested_recovery_path must be canonical"
        )
    if request.failure_code not in _FAILURE_POLICY[request.source_state]:
        raise RecoveryEligibilityValidationError(
            "failure_code is invalid for source_state"
        )
    if not isinstance(request.guard_evidence, Mapping):
        raise RecoveryEligibilityValidationError(
            "guard_evidence must be a canonical JSON object"
        )
    unknown_guard_fields = set(request.guard_evidence) - _GUARD_FIELDS
    if unknown_guard_fields:
        raise RecoveryEligibilityValidationError(
            "guard_evidence contains unsupported fields"
        )
    try:
        canonical_json_text(request.guard_evidence)
    except (CanonicalDataError, TypeError, ValueError) as exc:
        raise RecoveryEligibilityValidationError(
            f"guard_evidence is not canonical JSON: {exc}"
        ) from exc
    if not isinstance(request.invalidated_token_refs, tuple) or any(
        not isinstance(reference, str) or not reference
        for reference in request.invalidated_token_refs
    ):
        raise RecoveryEligibilityValidationError(
            "invalidated_token_refs must be a string tuple"
        )
    if len(set(request.invalidated_token_refs)) != len(
        request.invalidated_token_refs
    ):
        raise RecoveryEligibilityValidationError(
            "invalidated_token_refs must be unique"
        )
    _parse_utc(request.requested_at, "requested_at")


def recovery_review_protocol_hash(protocol: RecoveryReviewProtocol) -> str:
    """Return the canonical hash for protocol fields other than evidence_hash."""

    payload = asdict(protocol)
    payload.pop("evidence_hash")
    return canonical_sha256(payload)


def _classify(
    request: RecoveryEligibilityRequest,
    authority: AuthorityResolutionResult,
    halt: HaltDecision,
    review: ReviewDecision | None,
    review_authority: AuthorityResolutionResult | None,
    audit_repository: InMemoryAuditLogRepository,
    now: datetime,
) -> tuple[RecoveryOutcome, str, tuple[str, ...]]:
    authority_failure = _authority_failure(request, authority)
    if authority_failure:
        return RecoveryOutcome.REJECTED, authority_failure, ()
    halt_failure = _halt_failure(request, halt)
    if halt_failure:
        return RecoveryOutcome.REJECTED, halt_failure, ()
    audit_link_failure = _audit_link_failure(request, halt, audit_repository)
    if audit_link_failure:
        return RecoveryOutcome.REJECTED, audit_link_failure, ()
    if request.changed_evidence_hash == request.original_failure_evidence_hash:
        return RecoveryOutcome.REJECTED, "changed_evidence_not_distinct", ()

    policy = _FAILURE_POLICY[request.source_state][request.failure_code]
    missing_guards = tuple(
        field for field in policy.required_guard_fields if not _guard_present(
            request.guard_evidence, field
        )
    )
    if missing_guards:
        return RecoveryOutcome.REJECTED, "required_guard_evidence_missing", ()
    if not _guards_satisfied(request):
        return RecoveryOutcome.REJECTED, "recovery_guard_not_satisfied", ()

    if request.requested_recovery_path is RecoveryPath.CREATE_NEW_REQUEST:
        if request.recovery_review_protocol is not None:
            return RecoveryOutcome.REJECTED, "review_protocol_not_required", ()
        return RecoveryOutcome.NEW_REQUEST_REQUIRED, "new_request_path_selected", ()

    if policy.review_protocol_required:
        review_failure = _review_failure(
            request, review, review_authority, now
        )
        if review_failure:
            return RecoveryOutcome.NEW_REQUEST_REQUIRED, review_failure, ()
        return (
            RecoveryOutcome.REVALIDATION_REQUIRED,
            "recovery_revalidation_eligible",
            policy.required_validations,
        )
    if request.recovery_review_protocol is not None:
        return RecoveryOutcome.REJECTED, "review_protocol_not_required", ()
    return policy.default_outcome, policy.default_reason, policy.required_validations


def _authority_failure(
    request: RecoveryEligibilityRequest,
    authority: AuthorityResolutionResult,
) -> str | None:
    if not isinstance(authority, AuthorityResolutionResult):
        return "authority_evidence_unavailable"
    if authority.outcome is not AuthorityResolutionOutcome.AUTHORIZED:
        return "recovery_authority_not_authorized"
    if (
        authority.request_id != request.request_id
        or authority.authority_resolution_id != request.authority_resolution_id
        or authority.evidence_hash != request.authority_evidence_hash
        or authority.authority_source_id != request.recovery_authority_reference
    ):
        return "recovery_authority_evidence_mismatch"
    return None


def _halt_failure(
    request: RecoveryEligibilityRequest,
    halt: HaltDecision,
) -> str | None:
    if not isinstance(halt, HaltDecision):
        return "halt_evidence_unavailable"
    expected_outcome = (
        HaltOutcome.HOLD
        if request.source_state is RecoverySourceState.EXECUTION_BLOCKED
        else HaltOutcome.HALTED
    )
    if (
        halt.request_id != request.request_id
        or halt.halt_decision_id != request.halt_decision_id
        or halt.evidence_hash != request.halt_decision_evidence_hash
        or halt.runtime_state is not expected_outcome
        or halt.audit_event_id != request.guard_evidence.get("halt_audit_event_id")
    ):
        return "halt_evidence_mismatch"
    return None


def _review_failure(
    request: RecoveryEligibilityRequest,
    review: ReviewDecision | None,
    review_authority: AuthorityResolutionResult | None,
    now: datetime,
) -> str | None:
    protocol = request.recovery_review_protocol
    if not isinstance(protocol, RecoveryReviewProtocol):
        return "recovery_review_protocol_required"
    if protocol.protocol_status is not RecoveryProtocolStatus.ACTIVE:
        return "recovery_review_protocol_inactive"
    if protocol.permitted_recovery_path is not RecoveryPath.REVALIDATE_REQUEST:
        return "recovery_review_path_not_permitted"
    if not protocol.scope:
        return "recovery_review_scope_missing"
    try:
        canonical_json_text(protocol.scope)
    except (CanonicalDataError, TypeError, ValueError):
        return "recovery_review_scope_invalid"
    if recovery_review_protocol_hash(protocol) != protocol.evidence_hash:
        return "recovery_review_protocol_hash_mismatch"
    if _parse_utc(protocol.expires_at, "review_protocol.expires_at") <= now:
        return "recovery_review_protocol_expired"
    if (
        protocol.request_id != request.request_id
        or protocol.halt_decision_id != request.halt_decision_id
        or protocol.halt_decision_evidence_hash
        != request.halt_decision_evidence_hash
    ):
        return "recovery_review_protocol_mismatch"
    if not isinstance(review, ReviewDecision) or (
        review.request_id != request.request_id
        or review.review_decision_id != protocol.review_decision_id
        or review.evidence_hash != protocol.review_decision_evidence_hash
        or review.reviewer_id != protocol.reviewer_id
        or review.reviewer_authority_reference
        != protocol.reviewer_authority_reference
    ):
        return "recovery_review_decision_mismatch"
    if not isinstance(review_authority, AuthorityResolutionResult) or (
        review_authority.outcome is not AuthorityResolutionOutcome.AUTHORIZED
        or review_authority.request_id != request.request_id
        or review_authority.authority_resolution_id
        != protocol.reviewer_authority_resolution_id
        or review_authority.evidence_hash
        != protocol.reviewer_authority_evidence_hash
        or review_authority.authority_source_id
        != protocol.reviewer_authority_reference
    ):
        return "recovery_review_authority_invalid"
    return None


def _audit_link_failure(
    request: RecoveryEligibilityRequest,
    halt: HaltDecision,
    repository: InMemoryAuditLogRepository,
) -> str | None:
    try:
        original_event = repository.get(request.original_failure_audit_event_id)
        halt_event = repository.get(str(halt.audit_event_id))
    except MissingRecordError:
        return "recovery_audit_reference_missing"
    original_details = original_event.record.get("details")
    halt_details = halt_event.record.get("details")
    if (
        original_event.event_hash
        != request.guard_evidence.get("original_failure_event_hash")
        or not isinstance(original_details, Mapping)
        or original_details.get("evidence_hash")
        != request.original_failure_evidence_hash
    ):
        return "original_failure_audit_mismatch"
    if (
        not isinstance(halt_details, Mapping)
        or halt_details.get("halt_decision_id") != request.halt_decision_id
        or halt_details.get("evidence_hash")
        != request.halt_decision_evidence_hash
    ):
        return "halt_audit_mismatch"
    return None


def _guards_satisfied(request: RecoveryEligibilityRequest) -> bool:
    evidence = request.guard_evidence
    if request.failure_code is RecoveryFailureCode.DEPENDENCY_UNAVAILABLE:
        return evidence.get("dependency_status") == "available"
    if request.failure_code is RecoveryFailureCode.AUDIT_PATH_DEGRADED:
        return evidence.get("audit_path_status") == "restored"
    if request.failure_code is RecoveryFailureCode.CRITICAL_INVARIANT_FAILURE:
        return evidence.get("invariant_state") == "valid"
    if request.failure_code is RecoveryFailureCode.UNSAFE_EXECUTION:
        return evidence.get("execution_outcome") in {
            "blocked",
            "invalid_state",
            "missing_authority",
            "missing_evidence",
            "expired",
            "halted",
        }
    return True


def _guard_present(evidence: Mapping[str, object], field: str) -> bool:
    value = evidence.get(field)
    if field == "missing_evidence_refs":
        return (
            isinstance(value, (list, tuple))
            and bool(value)
            and all(isinstance(item, str) and bool(item) for item in value)
            and len(set(value)) == len(value)
        )
    return isinstance(value, str) and bool(value)


def _evidence_input(
    request: RecoveryEligibilityRequest,
    authority: object,
    halt: object,
    review: object,
    review_authority: object,
) -> dict[str, object]:
    return {
        "authority_evidence_hash": getattr(authority, "evidence_hash", None),
        "authority_resolution_id": getattr(
            authority, "authority_resolution_id", None
        ),
        "halt_decision_evidence_hash": getattr(halt, "evidence_hash", None),
        "halt_decision_id": getattr(halt, "halt_decision_id", None),
        "request": asdict(request),
        "review_authority_evidence_hash": getattr(
            review_authority, "evidence_hash", None
        ),
        "review_authority_resolution_id": getattr(
            review_authority, "authority_resolution_id", None
        ),
        "review_decision_evidence_hash": getattr(review, "evidence_hash", None),
        "review_decision_id": getattr(review, "review_decision_id", None),
    }


class _FailurePolicy:
    def __init__(
        self,
        *,
        default_outcome: RecoveryOutcome,
        default_reason: str,
        required_guard_fields: tuple[str, ...],
        review_protocol_required: bool,
        required_validations: tuple[str, ...],
    ) -> None:
        self.default_outcome = default_outcome
        self.default_reason = default_reason
        self.required_guard_fields = required_guard_fields
        self.review_protocol_required = review_protocol_required
        self.required_validations = required_validations


_BASE_GUARDS = (
    "audit_chain_id",
    "original_failure_event_hash",
    "halt_audit_event_id",
)
_FAILURE_POLICY = {
    RecoverySourceState.EXECUTION_BLOCKED: {
        RecoveryFailureCode.MISSING_EVIDENCE: _FailurePolicy(
            default_outcome=RecoveryOutcome.REVALIDATION_REQUIRED,
            default_reason="recovery_revalidation_eligible",
            required_guard_fields=("missing_evidence_refs",) + _BASE_GUARDS,
            review_protocol_required=False,
            required_validations=_REQUIRED_VALIDATIONS,
        ),
        RecoveryFailureCode.DEPENDENCY_UNAVAILABLE: _FailurePolicy(
            default_outcome=RecoveryOutcome.REVALIDATION_REQUIRED,
            default_reason="recovery_revalidation_eligible",
            required_guard_fields=(
                "dependency_id",
                "dependency_status",
                "dependency_evidence_hash",
            )
            + _BASE_GUARDS,
            review_protocol_required=False,
            required_validations=_REQUIRED_VALIDATIONS,
        ),
        RecoveryFailureCode.AUDIT_PATH_DEGRADED: _FailurePolicy(
            default_outcome=RecoveryOutcome.REVALIDATION_REQUIRED,
            default_reason="recovery_revalidation_eligible",
            required_guard_fields=("audit_path_status", "audit_path_evidence_hash")
            + _BASE_GUARDS,
            review_protocol_required=False,
            required_validations=_REQUIRED_VALIDATIONS,
        ),
        RecoveryFailureCode.COORDINATION_INTERRUPTED: _FailurePolicy(
            default_outcome=RecoveryOutcome.REVALIDATION_REQUIRED,
            default_reason="recovery_revalidation_eligible",
            required_guard_fields=("coordination_context_hash",) + _BASE_GUARDS,
            review_protocol_required=False,
            required_validations=_REQUIRED_VALIDATIONS,
        ),
    },
    RecoverySourceState.HALTED: {
        RecoveryFailureCode.CRITICAL_INVARIANT_FAILURE: _FailurePolicy(
            default_outcome=RecoveryOutcome.NEW_REQUEST_REQUIRED,
            default_reason="halted_request_requires_new_request",
            required_guard_fields=(
                "invariant_result_id",
                "invariant_state",
                "invariant_facts_hash",
            )
            + _BASE_GUARDS,
            review_protocol_required=True,
            required_validations=_REQUIRED_VALIDATIONS,
        ),
        RecoveryFailureCode.INVALID_STATE: _FailurePolicy(
            default_outcome=RecoveryOutcome.NEW_REQUEST_REQUIRED,
            default_reason="halted_request_requires_new_request",
            required_guard_fields=(
                "runtime_transition_decision_id",
                "runtime_transition_evidence_hash",
            )
            + _BASE_GUARDS,
            review_protocol_required=False,
            required_validations=(),
        ),
        RecoveryFailureCode.UNSAFE_EXECUTION: _FailurePolicy(
            default_outcome=RecoveryOutcome.NEW_REQUEST_REQUIRED,
            default_reason="halted_request_requires_new_request",
            required_guard_fields=(
                "execution_decision_id",
                "execution_outcome",
                "execution_evidence_hash",
            )
            + _BASE_GUARDS,
            review_protocol_required=False,
            required_validations=(),
        ),
        RecoveryFailureCode.EVIDENCE_INTEGRITY_FAILURE: _FailurePolicy(
            default_outcome=RecoveryOutcome.NEW_REQUEST_REQUIRED,
            default_reason="halted_request_requires_new_request",
            required_guard_fields=_BASE_GUARDS,
            review_protocol_required=False,
            required_validations=(),
        ),
        RecoveryFailureCode.AUDIT_CHAIN_FAILURE: _FailurePolicy(
            default_outcome=RecoveryOutcome.REJECTED,
            default_reason="audit_chain_failure",
            required_guard_fields=_BASE_GUARDS,
            review_protocol_required=False,
            required_validations=(),
        ),
    },
}
_GUARD_FIELDS = {
    "audit_chain_id",
    "original_failure_event_hash",
    "halt_audit_event_id",
    "missing_evidence_refs",
    "dependency_id",
    "dependency_status",
    "dependency_evidence_hash",
    "audit_path_status",
    "audit_path_evidence_hash",
    "coordination_context_hash",
    "invariant_result_id",
    "invariant_state",
    "invariant_facts_hash",
    "runtime_transition_decision_id",
    "runtime_transition_evidence_hash",
    "execution_decision_id",
    "execution_outcome",
    "execution_evidence_hash",
}


def _parse_utc(value: str, field_name: str) -> datetime:
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except (TypeError, ValueError) as exc:
        raise RecoveryEligibilityValidationError(
            f"{field_name} must be ISO 8601"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise RecoveryEligibilityValidationError(
            f"{field_name} must be timezone-aware"
        )
    if parsed.utcoffset().total_seconds() != 0:
        raise RecoveryEligibilityValidationError(f"{field_name} must be UTC")
    return parsed.astimezone(timezone.utc)


def _timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
