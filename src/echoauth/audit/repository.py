"""Append-only in-memory audit repository for Sprint 2A.

Specifications: specs/audit-record.md, specs/audit-chain.md,
specs/audit-log-spec.md
Contracts: schemas/audit-record.schema.json, database/schema.sql
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from threading import RLock
from types import MappingProxyType
from typing import Any

from echoauth.audit.hashing import (
    AuditRecordValidationError,
    audit_event_payload,
    hash_audit_event,
)
from echoauth.canonical import canonical_json_text
from echoauth.models import AuditAppendResult, AuditAppendState, AuditRecord
from echoauth.persistence import MissingRecordError
from echoauth.repositories import AuditLogRepository


@dataclass(frozen=True)
class StoredAuditEvent:
    """Immutable representation of one accepted audit-chain event."""

    audit_event_id: str
    chain_id: str
    chain_position: int
    previous_hash: str | None
    event_hash: str
    canonical_text: str
    record: Mapping[str, Any]


class InMemoryAuditLogRepository(AuditLogRepository):
    """Thread-safe append-only repository with per-chain sequencing."""

    def __init__(self) -> None:
        self._events: dict[str, StoredAuditEvent] = {}
        self._chains: dict[str, list[str]] = {}
        self._lock = RLock()

    def get(self, record_id: str) -> StoredAuditEvent:
        """Read an accepted event by identifier."""

        with self._lock:
            try:
                return self._events[record_id]
            except KeyError as exc:
                raise MissingRecordError(record_id) from exc

    def save(self, record: object) -> object:
        """Reject generic saves because audit storage is append-only."""

        raise TypeError("audit records must be persisted through append()")

    def append(
        self,
        record: AuditRecord,
        *,
        audit_event_id: str,
        chain_id: str,
        expected_previous_hash: str | None = None,
    ) -> AuditAppendResult:
        """Validate, hash, and atomically append one audit event."""

        if not isinstance(chain_id, str) or not chain_id:
            return _rejected("invalid_chain_id")
        try:
            payload = audit_event_payload(audit_event_id, record)
        except AuditRecordValidationError:
            return _rejected("invalid_audit_record", audit_event_id)

        with self._lock:
            if audit_event_id in self._events:
                return _rejected("duplicate_audit_event_id", audit_event_id)

            chain = self._chains.get(chain_id, [])
            previous_hash = self._events[chain[-1]].event_hash if chain else None
            if expected_previous_hash is not None and expected_previous_hash != previous_hash:
                return AuditAppendResult(
                    append_state=AuditAppendState.CONFLICT,
                    audit_event_id=audit_event_id,
                    previous_hash=previous_hash,
                    reason="expected_previous_hash_mismatch",
                )

            event_hash = hash_audit_event(payload, previous_hash)
            canonical_text = canonical_json_text(payload)
            stored = StoredAuditEvent(
                audit_event_id=audit_event_id,
                chain_id=chain_id,
                chain_position=len(chain) + 1,
                previous_hash=previous_hash,
                event_hash=event_hash,
                canonical_text=canonical_text,
                record=_deep_freeze(json.loads(canonical_text)),
            )
            self._events[audit_event_id] = stored
            self._chains.setdefault(chain_id, []).append(audit_event_id)
            return AuditAppendResult(
                append_state=AuditAppendState.ACCEPTED,
                audit_event_id=audit_event_id,
                event_hash=event_hash,
                previous_hash=previous_hash,
                chain_position=stored.chain_position,
                reason="accepted",
            )

    def chain(self, chain_id: str) -> tuple[StoredAuditEvent, ...]:
        """Return an immutable snapshot of a chain in accepted append order."""

        with self._lock:
            return tuple(self._events[event_id] for event_id in self._chains.get(chain_id, ()))


def _rejected(reason: str, audit_event_id: str | None = None) -> AuditAppendResult:
    return AuditAppendResult(
        append_state=AuditAppendState.REJECTED,
        audit_event_id=audit_event_id,
        reason=reason,
    )


def _deep_freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _deep_freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_deep_freeze(item) for item in value)
    return value
