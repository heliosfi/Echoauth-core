"""Deterministic audit validation and hash-chain helpers.

Specifications: specs/audit-record.md, specs/audit-chain.md
Contracts: schemas/audit-record.schema.json
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict
from datetime import datetime
from typing import Any

from echoauth.canonical import CanonicalDataError, canonical_sha256
from echoauth.models import AuditRecord

AUDIT_HASH_FORMAT = "echoauth.audit-chain.v1"


class AuditRecordValidationError(ValueError):
    """Raised when an audit record violates its canonical contract."""


def validate_audit_record(record: AuditRecord) -> None:
    """Validate the implementation-ready rules for an audit record."""

    if not isinstance(record, AuditRecord):
        raise AuditRecordValidationError("record must be an AuditRecord")
    for field_name in ("event_type", "actor_id", "reason", "occurred_at"):
        value = getattr(record, field_name)
        if not isinstance(value, str) or not value.strip():
            raise AuditRecordValidationError(f"{field_name} must be a non-empty string")
    if not isinstance(record.details, Mapping):
        raise AuditRecordValidationError("details must be a canonical JSON object")
    try:
        canonical_sha256(record.details)
    except (CanonicalDataError, TypeError, ValueError) as exc:
        raise AuditRecordValidationError(f"details are not canonical JSON: {exc}") from exc
    if (record.state_before is None) != (record.state_after is None):
        raise AuditRecordValidationError(
            "state_before and state_after must both be present for state transitions"
        )
    _validate_utc_timestamp(record.occurred_at)


def audit_event_payload(audit_event_id: str, record: AuditRecord) -> dict[str, Any]:
    """Return the canonical payload sealed into an audit-chain event."""

    if not isinstance(audit_event_id, str) or not audit_event_id:
        raise AuditRecordValidationError("audit_event_id must be a non-empty string")
    validate_audit_record(record)
    payload = {key: value for key, value in asdict(record).items() if value is not None}
    payload["audit_event_id"] = audit_event_id
    return payload


def hash_audit_event(event_payload: Mapping[str, Any], previous_hash: str | None) -> str:
    """Hash a versioned canonical event payload and its previous chain hash."""

    if not isinstance(event_payload, Mapping):
        raise AuditRecordValidationError("event_payload must be a canonical JSON object")
    if previous_hash is not None and (not isinstance(previous_hash, str) or not previous_hash):
        raise AuditRecordValidationError("previous_hash must be a non-empty string or None")
    hash_input = {
        "event_payload": event_payload,
        "format": AUDIT_HASH_FORMAT,
        "previous_hash": previous_hash,
    }
    try:
        return canonical_sha256(hash_input)
    except (CanonicalDataError, TypeError, ValueError) as exc:
        raise AuditRecordValidationError(f"event payload is not canonical JSON: {exc}") from exc


def _validate_utc_timestamp(value: str) -> None:
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise AuditRecordValidationError("occurred_at must be an ISO 8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise AuditRecordValidationError("occurred_at must include a UTC offset")
    if parsed.utcoffset().total_seconds() != 0:
        raise AuditRecordValidationError("occurred_at must be in UTC")
