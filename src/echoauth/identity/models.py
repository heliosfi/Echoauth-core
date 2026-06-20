"""Identity registry models derived from specs/identity-model.md."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from echoauth.models import ActorType, AssuranceLevel, CanonicalJsonObject


class IdentityStatus(str, Enum):
    """Persisted identity statuses."""

    ACTIVE = "active"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    ARCHIVED = "archived"


class IdentityState(str, Enum):
    """Identity registry operation states."""

    REGISTERED = "registered"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    ARCHIVED = "archived"
    REJECTED = "rejected"


class IdentityVerdictState(str, Enum):
    """Identity resolution states from specs/identity-resolution.md."""

    VERIFIED = "verified"
    REFUSED = "refused"
    HOLD = "hold"
    EXPIRED = "expired"
    CONFLICT = "conflict"


@dataclass(frozen=True)
class IdentityRecord:
    """Canonical persisted identity record."""

    identity_record_id: str
    actor_id: str
    actor_type: ActorType
    status: IdentityStatus
    credential_refs: tuple[str, ...]
    created_at: str
    updated_at: str
    display_label: str | None = None
    role_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class StoredIdentityRecord:
    """Immutable identity record plus deterministic registry metadata."""

    identity_state: IdentityState
    identity_record: IdentityRecord
    record_hash: str
    reason: str


@dataclass(frozen=True)
class CredentialVerification:
    """Result returned by an injected identity credential verifier."""

    state: IdentityVerdictState
    assurance_level: AssuranceLevel
    reason: str
    verifier_component: str
    evidence: CanonicalJsonObject
