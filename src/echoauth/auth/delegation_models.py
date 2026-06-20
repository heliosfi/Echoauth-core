"""Canonical delegation models for Sprint 2E.

Specifications: specs/delegation-model.md, specs/delegation-validation.md
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class DelegationState(str, Enum):
    """Persisted delegation grant lifecycle states."""

    DRAFT = "draft"
    ISSUED = "issued"
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    OUT_OF_SCOPE = "out_of_scope"
    INVALID = "invalid"


class DelegationValidationOutcome(str, Enum):
    """Canonical Sprint 2E validation outcomes."""

    VALID = "valid"
    EXPIRED = "expired"
    REVOKED = "revoked"
    INVALID_GRANTOR = "invalid_grantor"
    INVALID_SCOPE = "invalid_scope"
    INVALID_SUBJECT = "invalid_subject"
    CONFLICT = "conflict"


class DelegationContextMatch(str, Enum):
    """Provider-neutral context constraint result."""

    MATCH = "match"
    MISMATCH = "mismatch"
    AMBIGUOUS = "ambiguous"


@dataclass(frozen=True)
class DelegationGrant:
    """Explicit, bounded delegation derived from an authority result."""

    delegation_id: str
    grantor_id: str
    delegate_id: str
    subject_id: str
    role: str
    allowed_actions: tuple[str, ...]
    allowed_resources: tuple[str, ...]
    context_constraints: Mapping[str, Any]
    issued_at: str
    expires_at: str
    source_authority_reference: str
    authority_resolution_id: str
    chain_metadata: Mapping[str, Any]
    evidence_hash: str
    state: DelegationState
    revoked_at: str | None = None


@dataclass(frozen=True)
class StoredDelegationGrant:
    """Immutable current or historical delegation grant."""

    delegation_grant: DelegationGrant
    reason: str


@dataclass(frozen=True)
class DelegationHistoryEntry:
    """One immutable, audit-bound delegation lifecycle event."""

    sequence: int
    operation: str
    delegation_grant: DelegationGrant
    actor_id: str
    reason: str
    occurred_at: str
    audit_event_id: str
    audit_event_hash: str
    previous_audit_hash: str | None


@dataclass(frozen=True)
class DelegationValidationRequest:
    """Runtime request from specs/delegation-validation.md."""

    validation_id: str
    delegation_id: str
    requester_id: str
    subject_id: str
    action: str
    resource: str
    context: Mapping[str, Any]
    authority_verdict_id: str


@dataclass(frozen=True)
class DelegationValidationResult:
    """Deterministic Sprint 2E delegation result."""

    validation_id: str
    delegation_id: str
    outcome: DelegationValidationOutcome
    reason: str
    evidence_hash: str
    validated_at: str
    effective_scope: Mapping[str, Any] | None = None
    audit_event_id: str | None = None
