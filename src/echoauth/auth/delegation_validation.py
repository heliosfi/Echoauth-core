"""Deterministic delegation grant validation and evidence hashing."""

from __future__ import annotations

import hmac
from collections.abc import Mapping, Sequence
from dataclasses import replace

from echoauth.auth.authority_models import freeze_authority_value
from echoauth.auth.authority_validation import parse_authority_timestamp
from echoauth.auth.delegation_models import (
    DelegationGrant,
    DelegationState,
    DelegationValidationRequest,
)
from echoauth.canonical import CanonicalDataError, canonical_json_text, canonical_sha256


class DelegationValidationError(ValueError):
    """Raised when delegation evidence fails closed validation."""


def build_delegation_grant(
    *,
    delegation_id: str,
    grantor_id: str,
    delegate_id: str,
    subject_id: str,
    role: str,
    allowed_actions: Sequence[str],
    allowed_resources: Sequence[str],
    context_constraints: Mapping[str, object],
    issued_at: str,
    expires_at: str,
    source_authority_reference: str,
    authority_resolution_id: str,
    chain_metadata: Mapping[str, object] | None = None,
    state: DelegationState = DelegationState.ISSUED,
) -> DelegationGrant:
    """Construct a detached grant with canonical scope ordering and hash."""

    grant = DelegationGrant(
        delegation_id=delegation_id,
        grantor_id=grantor_id,
        delegate_id=delegate_id,
        subject_id=subject_id,
        role=role,
        allowed_actions=tuple(sorted(allowed_actions)),
        allowed_resources=tuple(sorted(allowed_resources)),
        context_constraints=freeze_authority_value(context_constraints),
        issued_at=issued_at,
        expires_at=expires_at,
        source_authority_reference=source_authority_reference,
        authority_resolution_id=authority_resolution_id,
        chain_metadata=freeze_authority_value(chain_metadata or {}),
        evidence_hash="",
        state=state,
    )
    grant = replace(grant, evidence_hash=delegation_evidence_hash(grant))
    validate_delegation_grant(grant)
    return grant


def delegation_evidence_hash(grant: DelegationGrant) -> str:
    """Hash immutable grant evidence independently of lifecycle state."""

    try:
        return canonical_sha256(
            {
                "allowed_actions": grant.allowed_actions,
                "allowed_resources": grant.allowed_resources,
                "authority_resolution_id": grant.authority_resolution_id,
                "chain_metadata": grant.chain_metadata,
                "context_constraints": grant.context_constraints,
                "delegate_id": grant.delegate_id,
                "delegation_id": grant.delegation_id,
                "expires_at": grant.expires_at,
                "grantor_id": grant.grantor_id,
                "issued_at": grant.issued_at,
                "role": grant.role,
                "source_authority_reference": grant.source_authority_reference,
                "subject_id": grant.subject_id,
            }
        )
    except (CanonicalDataError, TypeError, ValueError) as exc:
        raise DelegationValidationError(
            f"delegation evidence is not canonical JSON: {exc}"
        ) from exc


def validate_delegation_grant(grant: DelegationGrant) -> None:
    """Validate required fields, explicit scope, dates, and evidence integrity."""

    if not isinstance(grant, DelegationGrant):
        raise DelegationValidationError("grant must be a DelegationGrant")
    for field_name in (
        "delegation_id",
        "grantor_id",
        "delegate_id",
        "subject_id",
        "role",
        "source_authority_reference",
        "authority_resolution_id",
    ):
        value = getattr(grant, field_name)
        if not isinstance(value, str) or not value:
            raise DelegationValidationError(f"{field_name} must be a non-empty string")
    if grant.grantor_id == grant.delegate_id:
        raise DelegationValidationError("self-delegation is not permitted")
    _validate_scope_list(grant.allowed_actions, "allowed_actions")
    _validate_scope_list(grant.allowed_resources, "allowed_resources")
    _validate_canonical_object(grant.context_constraints, "context_constraints")
    _validate_canonical_object(grant.chain_metadata, "chain_metadata")
    issued_at = parse_authority_timestamp(grant.issued_at, "issued_at")
    expires_at = parse_authority_timestamp(grant.expires_at, "expires_at")
    if expires_at <= issued_at:
        raise DelegationValidationError("expires_at must be later than issued_at")
    if not isinstance(grant.state, DelegationState):
        raise DelegationValidationError("state must be a canonical delegation state")
    if grant.revoked_at is not None:
        revoked_at = parse_authority_timestamp(grant.revoked_at, "revoked_at")
        if revoked_at < issued_at:
            raise DelegationValidationError("revoked_at must not precede issued_at")
    if not isinstance(grant.evidence_hash, str) or not grant.evidence_hash:
        raise DelegationValidationError("evidence_hash must be a non-empty string")
    if not hmac.compare_digest(grant.evidence_hash, delegation_evidence_hash(grant)):
        raise DelegationValidationError("evidence_hash does not match delegation evidence")


def validate_delegation_request(request: DelegationValidationRequest) -> None:
    """Validate contract-level request fields and canonical context."""

    if not isinstance(request, DelegationValidationRequest):
        raise DelegationValidationError(
            "request must be a DelegationValidationRequest"
        )
    for field_name in (
        "validation_id",
        "delegation_id",
        "requester_id",
        "subject_id",
        "action",
        "resource",
        "authority_verdict_id",
    ):
        value = getattr(request, field_name)
        if not isinstance(value, str) or not value:
            raise DelegationValidationError(f"{field_name} must be a non-empty string")
    _validate_canonical_object(request.context, "context")


def _validate_scope_list(value: object, field_name: str) -> None:
    if not isinstance(value, tuple) or not value:
        raise DelegationValidationError(f"{field_name} must be a non-empty tuple")
    if any(not isinstance(item, str) or not item for item in value):
        raise DelegationValidationError(
            f"{field_name} entries must be non-empty strings"
        )
    if len(set(value)) != len(value):
        raise DelegationValidationError(f"{field_name} entries must be unique")


def _validate_canonical_object(value: object, field_name: str) -> None:
    if not isinstance(value, Mapping):
        raise DelegationValidationError(f"{field_name} must be a canonical JSON object")
    try:
        canonical_json_text(value)
    except (CanonicalDataError, TypeError, ValueError) as exc:
        raise DelegationValidationError(
            f"{field_name} is not canonical JSON: {exc}"
        ) from exc
