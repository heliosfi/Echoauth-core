"""Deterministic authority validation and evidence hashing."""

from __future__ import annotations

import hmac
from collections.abc import Mapping
from dataclasses import replace
from datetime import datetime

from echoauth.auth.authority_models import (
    AuthorityRecord,
    AuthorityStatus,
    AuthorityType,
    freeze_authority_value,
)
from echoauth.canonical import CanonicalDataError, canonical_json_text, canonical_sha256


class AuthorityValidationError(ValueError):
    """Raised when an authority record fails closed validation."""


def build_authority_record(
    *,
    authority_record_id: str,
    authority_source_id: str,
    subject_id: str,
    authority_type: AuthorityType,
    scope: Mapping[str, object],
    priority: int,
    issued_at: str,
    expires_at: str | None,
    status: AuthorityStatus = AuthorityStatus.ACTIVE,
    source_document_hash: str | None = None,
) -> AuthorityRecord:
    """Construct a detached record with its canonical evidence hash."""

    record = AuthorityRecord(
        authority_record_id=authority_record_id,
        authority_source_id=authority_source_id,
        subject_id=subject_id,
        authority_type=authority_type,
        scope=freeze_authority_value(scope),
        priority=priority,
        issued_at=issued_at,
        expires_at=expires_at,
        evidence_hash="",
        status=status,
        source_document_hash=source_document_hash,
    )
    record = replace(record, evidence_hash=authority_evidence_hash(record))
    validate_authority_record(record)
    return record


def authority_evidence_hash(record: AuthorityRecord) -> str:
    """Hash immutable authority evidence independently of lifecycle status."""

    payload = {
        "authority_record_id": record.authority_record_id,
        "authority_source_id": record.authority_source_id,
        "authority_type": _enum_value(record.authority_type),
        "expires_at": record.expires_at,
        "issued_at": record.issued_at,
        "priority": record.priority,
        "scope": record.scope,
        "source_document_hash": record.source_document_hash,
        "subject_id": record.subject_id,
    }
    try:
        return canonical_sha256(payload)
    except (CanonicalDataError, TypeError, ValueError) as exc:
        raise AuthorityValidationError(f"authority evidence is not canonical JSON: {exc}") from exc


def validate_authority_record(record: AuthorityRecord) -> None:
    """Validate required fields, dates, scope, enums, and evidence integrity."""

    if not isinstance(record, AuthorityRecord):
        raise AuthorityValidationError("record must be an AuthorityRecord")
    for field_name in ("authority_record_id", "authority_source_id", "subject_id"):
        value = getattr(record, field_name)
        if not isinstance(value, str) or not value.strip():
            raise AuthorityValidationError(f"{field_name} must be a non-empty string")
    if not isinstance(record.authority_type, AuthorityType):
        raise AuthorityValidationError("authority_type must be a canonical authority type")
    if not isinstance(record.status, AuthorityStatus):
        raise AuthorityValidationError("status must be a canonical authority status")
    if isinstance(record.priority, bool) or not isinstance(record.priority, int):
        raise AuthorityValidationError("priority must be an integer")
    if record.source_document_hash is not None and (
        not isinstance(record.source_document_hash, str) or not record.source_document_hash
    ):
        raise AuthorityValidationError("source_document_hash must be a non-empty string")
    if not isinstance(record.scope, Mapping) or not record.scope:
        raise AuthorityValidationError("scope must be a non-empty canonical JSON object")
    try:
        canonical_json_text(record.scope)
    except (CanonicalDataError, TypeError, ValueError) as exc:
        raise AuthorityValidationError(f"scope is not canonical JSON: {exc}") from exc
    issued_at = parse_authority_timestamp(record.issued_at, "issued_at")
    if record.expires_at is not None:
        expires_at = parse_authority_timestamp(record.expires_at, "expires_at")
        if expires_at <= issued_at:
            raise AuthorityValidationError("expires_at must be later than issued_at")
    if not isinstance(record.evidence_hash, str) or not record.evidence_hash:
        raise AuthorityValidationError("evidence_hash must be a non-empty string")
    expected_hash = authority_evidence_hash(record)
    if not hmac.compare_digest(record.evidence_hash, expected_hash):
        raise AuthorityValidationError("evidence_hash does not match authority evidence")


def parse_authority_timestamp(value: str, field_name: str) -> datetime:
    """Parse a canonical UTC authority timestamp."""

    if not isinstance(value, str) or not value:
        raise AuthorityValidationError(f"{field_name} must be a non-empty string")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise AuthorityValidationError(f"{field_name} must be an ISO 8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise AuthorityValidationError(f"{field_name} must include a UTC offset")
    if parsed.utcoffset().total_seconds() != 0:
        raise AuthorityValidationError(f"{field_name} must be in UTC")
    return parsed


def _enum_value(value: object) -> str:
    raw_value = getattr(value, "value", value)
    return raw_value if isinstance(raw_value, str) else repr(raw_value)
