"""Event bus interfaces for EchoAuth runtime skeleton."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

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
