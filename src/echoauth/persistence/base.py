"""Persistence adapter foundation for Sprint 1.

This module provides a contract-shaped in-memory repository suitable for tests
and early adapter work. It intentionally contains no service-specific behavior.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from echoauth.canonical import CanonicalDataError, canonical_json_text
from echoauth.repositories import Repository


class RepositoryRecordError(ValueError):
    """Raised when a record cannot be persisted by the foundation adapter."""


class MissingRecordError(KeyError):
    """Raised when a requested record is not present."""


@dataclass(frozen=True)
class StoredRecord:
    """Persisted record representation."""

    record_id: str
    canonical_text: str
    record: Mapping[str, Any]


class InMemoryRepository(Repository):
    """Generic in-memory repository foundation.

    The identity field is configurable because the repository contracts use
    different primary key names across tables.
    """

    def __init__(self, identity_field: str = "id") -> None:
        if not identity_field:
            raise RepositoryRecordError("identity field must not be empty")
        self.identity_field = identity_field
        self._records: dict[str, StoredRecord] = {}

    def get(self, record_id: str) -> StoredRecord:
        """Read a stored record by identifier."""

        try:
            return self._records[record_id]
        except KeyError as exc:
            raise MissingRecordError(record_id) from exc

    def save(self, record: object) -> StoredRecord:
        """Persist a mapping record and preserve canonical JSON text."""

        if not isinstance(record, Mapping):
            raise RepositoryRecordError("record must be a mapping")
        raw_record_id = record.get(self.identity_field)
        if not isinstance(raw_record_id, str) or not raw_record_id:
            raise RepositoryRecordError(f"record must include non-empty {self.identity_field}")
        try:
            canonical_text = canonical_json_text(record)
        except CanonicalDataError as exc:
            raise RepositoryRecordError(str(exc)) from exc
        stored = StoredRecord(
            record_id=raw_record_id,
            canonical_text=canonical_text,
            record=json.loads(canonical_text),
        )
        self._records[raw_record_id] = stored
        return stored
