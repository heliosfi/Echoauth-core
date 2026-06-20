"""Event envelope validation helpers for Sprint 1."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from echoauth.canonical import CanonicalDataError, canonical_json_text
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


def validate_event_envelope(event: EventEnvelope | Mapping[str, Any]) -> dict[str, Any]:
    """Validate required event envelope fields and canonical payload shape."""

    data = _event_to_mapping(event)
    missing = [field for field in REQUIRED_EVENT_FIELDS if not data.get(field)]
    if missing:
        raise EventValidationError(f"missing event fields: {', '.join(missing)}")
    try:
        canonical_json_text(data["payload"])
    except CanonicalDataError as exc:
        raise EventValidationError(f"invalid event payload: {exc}") from exc
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


def _event_to_mapping(event: EventEnvelope | Mapping[str, Any]) -> dict[str, Any]:
    if isinstance(event, Mapping):
        return dict(event)
    if is_dataclass(event):
        return asdict(event)
    raise EventValidationError("event must be an EventEnvelope or mapping")
