"""Event bus interfaces for EchoAuth runtime skeleton."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from threading import RLock

from echoauth.canonical import canonical_sha256
from echoauth.events_validation import (
    EventValidationError,
    load_event_catalog,
    validate_event_envelope,
)
from echoauth.models import CanonicalJsonObject


@dataclass(frozen=True)
class EventEnvelope:
    """Event contract from events/event-envelope.schema.json."""

    event_id: str
    event_type: str
    producer_id: str
    correlation_id: str
    payload: CanonicalJsonObject
    occurred_at: str
    request_id: str | None = None
    causation_id: str | None = None


class EventDeliveryState(str, Enum):
    """Event-bus states; Sprint 2Q emits only accepted or rejected."""

    ACCEPTED = "accepted"
    PUBLISHED = "published"
    REJECTED = "rejected"
    DEAD_LETTERED = "dead_lettered"


@dataclass(frozen=True)
class EventAcceptanceResult:
    """Validation evidence that grants no delivery or execution semantics."""

    event_id: str | None
    event_type: str | None
    delivery_state: EventDeliveryState
    subscribers_notified: tuple[str, ...]
    reason: str
    payload_hash: str | None = None


class InProcessEventAcceptance:
    """Validate event envelopes without publishing, persisting, or delivering."""

    def __init__(
        self,
        catalog_path: str | Path = "events/event-catalog.yaml",
    ) -> None:
        self._catalog = load_event_catalog(catalog_path)
        self._accepted_event_ids: set[str] = set()
        self._lock = RLock()

    def accept(
        self,
        event: EventEnvelope | CanonicalJsonObject,
    ) -> EventAcceptanceResult:
        """Return accepted or fail-closed rejected validation evidence."""

        try:
            data = validate_event_envelope(event)
        except EventValidationError:
            return _rejected(event, "invalid_event_envelope")

        event_id = data["event_id"]
        event_type = data["event_type"]
        if event_type not in self._catalog:
            return _rejected(data, "unknown_event_type")
        if event_type in _CATALOG_ONLY_EVENT_TYPES:
            return _rejected(data, "catalog_only_event_type")

        with self._lock:
            if event_id in self._accepted_event_ids:
                return _rejected(data, "duplicate_event_id")
            self._accepted_event_ids.add(event_id)

        return EventAcceptanceResult(
            event_id=event_id,
            event_type=event_type,
            delivery_state=EventDeliveryState.ACCEPTED,
            subscribers_notified=(),
            reason="accepted",
            payload_hash=canonical_sha256(data["payload"]),
        )


class EventBus(ABC):
    """Specification: specs/event-bus.md.

    Contract: events/event-envelope.schema.json, events/event-catalog.yaml
    """

    @abstractmethod
    def publish(self, event: EventEnvelope) -> object:
        """Publish an event envelope."""

    @abstractmethod
    def subscribe(self, event_type: str, subscriber_id: str) -> object:
        """Register a subscriber for an event type."""


_CATALOG_ONLY_EVENT_TYPES = frozenset({"runtime.recovered"})


def _rejected(
    event: EventEnvelope | CanonicalJsonObject,
    reason: str,
) -> EventAcceptanceResult:
    event_id: str | None = None
    event_type: str | None = None
    if isinstance(event, EventEnvelope):
        event_id = event.event_id if isinstance(event.event_id, str) else None
        event_type = event.event_type if isinstance(event.event_type, str) else None
    elif isinstance(event, dict):
        raw_event_id = event.get("event_id")
        raw_event_type = event.get("event_type")
        event_id = raw_event_id if isinstance(raw_event_id, str) else None
        event_type = raw_event_type if isinstance(raw_event_type, str) else None
    return EventAcceptanceResult(
        event_id=event_id,
        event_type=event_type,
        delivery_state=EventDeliveryState.REJECTED,
        subscribers_notified=(),
        reason=reason,
    )
