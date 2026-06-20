"""Deterministic identity record and request validation."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, replace
from datetime import datetime
from typing import Any

from echoauth.canonical import CanonicalDataError, canonical_json_text, canonical_sha256
from echoauth.identity.models import IdentityRecord, IdentityStatus
from echoauth.models import ActorType, AssuranceLevel, IdentityResolutionRequest


class IdentityValidationError(ValueError):
    """Raised when identity data violates the canonical specification."""


def normalize_identity_record(record: IdentityRecord) -> IdentityRecord:
    """Validate a record and canonicalize credential-reference ordering."""

    if not isinstance(record, IdentityRecord):
        raise IdentityValidationError("record must be an IdentityRecord")
    for field_name in ("identity_record_id", "actor_id", "created_at", "updated_at"):
        value = getattr(record, field_name)
        if not isinstance(value, str) or not value.strip():
            raise IdentityValidationError(f"{field_name} must be a non-empty string")
    if not isinstance(record.status, IdentityStatus):
        raise IdentityValidationError("status must be a canonical identity status")
    if not isinstance(record.actor_type, ActorType):
        raise IdentityValidationError("actor_type must be a canonical actor type")
    _validate_references(record.credential_refs, "credential_refs")
    _validate_references(record.role_refs, "role_refs")
    if record.status is IdentityStatus.ACTIVE and not record.credential_refs:
        raise IdentityValidationError("active identities require credential references")
    _parse_utc(record.created_at, "created_at")
    _parse_utc(record.updated_at, "updated_at")
    if _parse_utc(record.updated_at, "updated_at") < _parse_utc(record.created_at, "created_at"):
        raise IdentityValidationError("updated_at must not precede created_at")
    return replace(record, credential_refs=tuple(sorted(record.credential_refs)))


def identity_record_hash(record: IdentityRecord) -> str:
    """Return the canonical hash of a normalized identity record."""

    normalized = normalize_identity_record(record)
    payload = asdict(normalized)
    payload["actor_type"] = normalized.actor_type.value
    payload["status"] = normalized.status.value
    return canonical_sha256(payload)


def validate_resolution_request(request: IdentityResolutionRequest) -> None:
    """Validate contract-level identity resolution inputs."""

    if not isinstance(request, IdentityResolutionRequest):
        raise IdentityValidationError("request must be an IdentityResolutionRequest")
    for field_name in ("identity_request_id", "actor_id"):
        value = getattr(request, field_name)
        if not isinstance(value, str) or not value.strip():
            raise IdentityValidationError(f"{field_name} must be a non-empty string")
    if not isinstance(request.actor_type, ActorType):
        raise IdentityValidationError("actor_type must be a canonical actor type")
    if not isinstance(request.required_assurance, AssuranceLevel):
        raise IdentityValidationError("required_assurance must be a canonical assurance level")
    for field_name in ("credential_set", "context"):
        value = getattr(request, field_name)
        if not isinstance(value, Mapping):
            raise IdentityValidationError(f"{field_name} must be a canonical JSON object")
        try:
            canonical_json_text(value)
        except (CanonicalDataError, TypeError, ValueError) as exc:
            raise IdentityValidationError(f"{field_name} is not canonical JSON: {exc}") from exc


def identity_evidence_hash(
    request: IdentityResolutionRequest,
    *,
    record_hash: str | None,
    verification_evidence: Mapping[str, Any] | None = None,
) -> str:
    """Bind identity evidence to actor, context, assurance, and session."""

    payload: dict[str, Any] = {
        "actor_id": request.actor_id,
        "actor_type": _enum_value(request.actor_type),
        "context": request.context,
        "credential_set": request.credential_set,
        "identity_request_id": request.identity_request_id,
        "record_hash": record_hash,
        "required_assurance": _enum_value(request.required_assurance),
        "session_id": request.session_id,
        "verification_evidence": verification_evidence or {},
    }
    return canonical_sha256(payload)


def _enum_value(value: object) -> str:
    raw_value = getattr(value, "value", value)
    return raw_value if isinstance(raw_value, str) else repr(raw_value)


def _validate_references(values: object, field_name: str) -> None:
    if not isinstance(values, tuple):
        raise IdentityValidationError(f"{field_name} must be a tuple of strings")
    if any(not isinstance(value, str) or not value for value in values):
        raise IdentityValidationError(f"{field_name} entries must be non-empty strings")
    if len(set(values)) != len(values):
        raise IdentityValidationError(f"{field_name} entries must be unique")


def _parse_utc(value: str, field_name: str) -> datetime:
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise IdentityValidationError(f"{field_name} must be an ISO 8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise IdentityValidationError(f"{field_name} must include a UTC offset")
    if parsed.utcoffset().total_seconds() != 0:
        raise IdentityValidationError(f"{field_name} must be in UTC")
    return parsed
