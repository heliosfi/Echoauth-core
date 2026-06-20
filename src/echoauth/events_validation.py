"""Event envelope validation helpers for Sprint 1."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

from echoauth.canonical import CanonicalDataError, canonical_json_text

if TYPE_CHECKING:
    from echoauth.events import EventEnvelope


class EventValidationError(ValueError):
    """Raised when an event envelope or catalog entry is invalid."""


REQUIRED_EVENT_FIELDS = (
    "event_id",
    "event_type",
    "producer_id",
    "correlation_id",
    "payload",
    "occurred_at",
)
EVENT_FIELDS = frozenset(REQUIRED_EVENT_FIELDS + ("request_id", "causation_id"))


def validate_event_envelope(
    event: "EventEnvelope" | Mapping[str, Any],
) -> dict[str, Any]:
    """Validate required event envelope fields and canonical payload shape."""

    data = _event_to_mapping(event)
    unknown = sorted(set(data) - EVENT_FIELDS)
    if unknown:
        raise EventValidationError(
            f"unknown event fields: {', '.join(unknown)}"
        )
    missing = [field for field in REQUIRED_EVENT_FIELDS if field not in data]
    if missing:
        raise EventValidationError(f"missing event fields: {', '.join(missing)}")
    for field in ("event_id", "event_type", "producer_id", "correlation_id"):
        if not isinstance(data[field], str) or not data[field]:
            raise EventValidationError(f"{field} must be a non-empty string")
    for field in ("request_id", "causation_id"):
        value = data.get(field)
        if value is not None and (not isinstance(value, str) or not value):
            raise EventValidationError(
                f"{field} must be a non-empty string when present"
            )
    if not isinstance(data["payload"], Mapping):
        raise EventValidationError("invalid event payload: payload must be an object")
    try:
        canonical_json_text(data["payload"])
    except (CanonicalDataError, TypeError, ValueError) as exc:
        raise EventValidationError(f"invalid event payload: {exc}") from exc
    _validate_utc_timestamp(data["occurred_at"])
    return data


def load_event_catalog(path: str | Path = "events/event-catalog.yaml") -> dict[str, str]:
    """Load event type to payload schema mappings from the repository catalog."""

    catalog_path = Path(path)
    if not catalog_path.is_file():
        raise EventValidationError(f"event catalog not found: {catalog_path}")
    events: dict[str, str] = {}
    current_event_type: str | None = None
    for raw_line in catalog_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("- event_type:"):
            current_event_type = line.split(":", 1)[1].strip()
            if not current_event_type:
                raise EventValidationError("event_type entry is empty")
            if current_event_type in events:
                raise EventValidationError(
                    f"duplicate event_type: {current_event_type}"
                )
            continue
        if line.startswith("payload_schema:"):
            if current_event_type is None:
                raise EventValidationError("payload_schema entry without event_type")
            payload_schema = line.split(":", 1)[1].strip()
            if not payload_schema:
                raise EventValidationError(f"payload_schema for {current_event_type} is empty")
            events[current_event_type] = payload_schema
            current_event_type = None
    if not events:
        raise EventValidationError("event catalog contains no events")
    return events


def payload_schema_for_event(
    event_type: str,
    catalog_path: str | Path = "events/event-catalog.yaml",
) -> str:
    """Return the payload schema path for an event type."""

    catalog = load_event_catalog(catalog_path)
    try:
        return catalog[event_type]
    except KeyError as exc:
        raise EventValidationError(f"unknown event type: {event_type}") from exc


def resolve_payload_schema_path(
    event_type: str,
    catalog_path: str | Path = "events/event-catalog.yaml",
) -> Path:
    """Resolve a catalog payload schema reference relative to its catalog."""

    resolved_catalog = Path(catalog_path).resolve()
    schema_reference = payload_schema_for_event(event_type, resolved_catalog)
    schema_path = Path(schema_reference)
    if schema_path.is_absolute():
        raise EventValidationError("payload schema path must be relative")
    return (resolved_catalog.parent / schema_path).resolve()


def _event_to_mapping(
    event: "EventEnvelope" | Mapping[str, Any],
) -> dict[str, Any]:
    if isinstance(event, Mapping):
        return dict(event)
    if is_dataclass(event):
        return asdict(event)
    raise EventValidationError("event must be an EventEnvelope or mapping")


def _validate_utc_timestamp(value: object) -> None:
    if not isinstance(value, str) or not value:
        raise EventValidationError("occurred_at must be a non-empty UTC timestamp")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise EventValidationError("occurred_at must be ISO 8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise EventValidationError("occurred_at must be timezone-aware")
    if parsed.astimezone(timezone.utc).utcoffset() != parsed.utcoffset():
        raise EventValidationError("occurred_at must be UTC")
