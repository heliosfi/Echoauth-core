"""Canonical authority registry models for Sprint 2C.

Specification: specs/authority-registry.md
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class AuthorityType(str, Enum):
    """Authority categories required by the Sprint 2C contract."""

    PARENT = "parent"
    CAREGIVER = "caregiver"
    INSTITUTION = "institution"
    DELEGATED = "delegated"
    EMERGENCY = "emergency"
    RUNTIME_SERVICE = "runtime-service"


class AuthorityStatus(str, Enum):
    """Persisted authority lifecycle statuses."""

    ACTIVE = "active"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    EXPIRED = "expired"


class AuthorityRegistryState(str, Enum):
    """Authority registry operation states."""

    REGISTERED = "registered"
    UPDATED = "updated"
    FOUND = "found"
    NOT_FOUND = "not_found"
    REJECTED = "rejected"


class FrozenDict(dict[str, Any]):
    """JSON-compatible dictionary that rejects mutation."""

    def _immutable(self, *args: object, **kwargs: object) -> None:
        raise TypeError("authority evidence is immutable")

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    pop = _immutable
    popitem = _immutable
    setdefault = _immutable
    update = _immutable


@dataclass(frozen=True)
class AuthorityRecord:
    """Explicit permission-source record; identity fields grant no authority."""

    authority_record_id: str
    authority_source_id: str
    subject_id: str
    authority_type: AuthorityType
    scope: Mapping[str, Any]
    priority: int
    issued_at: str
    expires_at: str | None
    evidence_hash: str
    status: AuthorityStatus
    source_document_hash: str | None = None


@dataclass(frozen=True)
class StoredAuthorityRecord:
    """Immutable current or historical authority registry record."""

    registry_result_id: str
    state: AuthorityRegistryState
    authority_record: AuthorityRecord
    reason: str


@dataclass(frozen=True)
class AuthorityHistoryEntry:
    """One immutable, audit-bound authority lifecycle entry."""

    sequence: int
    operation: str
    authority_record: AuthorityRecord
    actor_id: str
    reason: str
    occurred_at: str
    audit_event_id: str
    audit_event_hash: str
    previous_audit_hash: str | None


def freeze_authority_value(value: Any) -> Any:
    """Recursively detach and freeze a canonical authority value."""

    if isinstance(value, Mapping):
        return FrozenDict({key: freeze_authority_value(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(freeze_authority_value(item) for item in value)
    return value
