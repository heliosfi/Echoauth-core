"""Append-history in-memory identity registry for Sprint 2B."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import replace
from threading import RLock

from echoauth.identity.models import (
    IdentityRecord,
    IdentityState,
    IdentityStatus,
    StoredIdentityRecord,
)
from echoauth.identity.validation import identity_record_hash, normalize_identity_record


class IdentityRepositoryError(ValueError):
    """Base deterministic identity repository error."""


class IdentityNotFoundError(KeyError):
    """Raised when an identity record or actor is absent."""


class DuplicateIdentityError(IdentityRepositoryError):
    """Raised when a record ID or actor ID is already registered."""


class InvalidIdentityTransitionError(IdentityRepositoryError):
    """Raised when an identity lifecycle transition is not permitted."""


class IdentityRepository(ABC):
    """Identity persistence boundary from specs/identity-model.md."""

    @abstractmethod
    def register(self, record: IdentityRecord) -> StoredIdentityRecord:
        """Register one unique identity."""

    @abstractmethod
    def get(self, identity_record_id: str) -> StoredIdentityRecord:
        """Read the current identity by record ID."""

    @abstractmethod
    def get_by_actor(self, actor_id: str) -> StoredIdentityRecord:
        """Read the current identity by actor ID."""

    @abstractmethod
    def transition(
        self,
        identity_record_id: str,
        status: IdentityStatus,
        *,
        updated_at: str,
    ) -> StoredIdentityRecord:
        """Apply one validated lifecycle transition."""

    @abstractmethod
    def history(self, identity_record_id: str) -> tuple[StoredIdentityRecord, ...]:
        """Return immutable identity history in persistence order."""


_ALLOWED_TRANSITIONS = {
    IdentityStatus.ACTIVE: {
        IdentityStatus.SUSPENDED,
        IdentityStatus.REVOKED,
        IdentityStatus.ARCHIVED,
    },
    IdentityStatus.SUSPENDED: {IdentityStatus.ACTIVE, IdentityStatus.REVOKED},
    IdentityStatus.REVOKED: {IdentityStatus.ARCHIVED},
    IdentityStatus.ARCHIVED: set(),
}


class InMemoryIdentityRepository(IdentityRepository):
    """Thread-safe identity repository retaining immutable status history."""

    def __init__(self) -> None:
        self._records: dict[str, list[StoredIdentityRecord]] = {}
        self._actor_index: dict[str, str] = {}
        self._lock = RLock()

    def register(self, record: IdentityRecord) -> StoredIdentityRecord:
        normalized = normalize_identity_record(record)
        with self._lock:
            if normalized.identity_record_id in self._records:
                raise DuplicateIdentityError("duplicate identity_record_id")
            if normalized.actor_id in self._actor_index:
                raise DuplicateIdentityError("duplicate actor_id")
            stored = _stored(normalized, IdentityState.REGISTERED, "registered")
            self._records[normalized.identity_record_id] = [stored]
            self._actor_index[normalized.actor_id] = normalized.identity_record_id
            return stored

    def get(self, identity_record_id: str) -> StoredIdentityRecord:
        with self._lock:
            try:
                return self._records[identity_record_id][-1]
            except KeyError as exc:
                raise IdentityNotFoundError(identity_record_id) from exc

    def get_by_actor(self, actor_id: str) -> StoredIdentityRecord:
        with self._lock:
            try:
                identity_record_id = self._actor_index[actor_id]
            except KeyError as exc:
                raise IdentityNotFoundError(actor_id) from exc
            return self._records[identity_record_id][-1]

    def transition(
        self,
        identity_record_id: str,
        status: IdentityStatus,
        *,
        updated_at: str,
    ) -> StoredIdentityRecord:
        with self._lock:
            current = self.get(identity_record_id)
            current_status = current.identity_record.status
            if status not in _ALLOWED_TRANSITIONS[current_status]:
                raise InvalidIdentityTransitionError(
                    f"transition from {current_status.value} to {status.value} is not allowed"
                )
            record = normalize_identity_record(
                replace(current.identity_record, status=status, updated_at=updated_at)
            )
            stored = _stored(record, IdentityState(status.value), status.value)
            self._records[identity_record_id].append(stored)
            return stored

    def history(self, identity_record_id: str) -> tuple[StoredIdentityRecord, ...]:
        with self._lock:
            if identity_record_id not in self._records:
                raise IdentityNotFoundError(identity_record_id)
            return tuple(self._records[identity_record_id])


def _stored(record: IdentityRecord, state: IdentityState, reason: str) -> StoredIdentityRecord:
    return StoredIdentityRecord(
        identity_state=state,
        identity_record=record,
        record_hash=identity_record_hash(record),
        reason=reason,
    )
