"""Validation-only request-scoped event ordering for Sprint 2U."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone

from echoauth.canonical import canonical_sha256
from echoauth.events import EventEnvelope
from echoauth.events_validation import EventValidationError, validate_event_envelope

EVENT_ORDERING_VERSION = "echoauth.event-ordering.v1"


@dataclass(frozen=True)
class RequestEventOrder:
    """Deterministic event ID order for one explicit request scope."""

    request_id: str
    ordered_event_ids: tuple[str, ...]
    ordering_rule: str = "occurred_at_then_event_id"


@dataclass(frozen=True)
class UnscopedEventEvidence:
    """Event reference for which no ordering guarantee is inferred."""

    event_id: str
    ordering_guarantee: str = "none"


@dataclass(frozen=True)
class EventOrderingResult:
    """Immutable ordering validation evidence with no delivery effect."""

    valid: bool
    reason: str
    request_orders: tuple[RequestEventOrder, ...]
    unscoped_events: tuple[UnscopedEventEvidence, ...]
    evidence_hash: str


class EventOrderingValidator:
    """Validate and describe request-scoped order without sequencing events."""

    def validate(
        self,
        events: Sequence[EventEnvelope | Mapping[str, object]],
    ) -> EventOrderingResult:
        if isinstance(events, (str, bytes)) or not isinstance(events, Sequence):
            return _rejected("events_must_be_ordered", ())

        validated: list[tuple[dict[str, object], datetime]] = []
        event_ids: list[str] = []
        for event in events:
            try:
                data = validate_event_envelope(event)
            except EventValidationError:
                return _rejected("invalid_event_envelope", tuple(event_ids))
            event_id = data["event_id"]
            occurred_at = data["occurred_at"]
            if not isinstance(event_id, str):
                return _rejected("invalid_event_id", tuple(event_ids))
            try:
                timestamp = _parse_utc(occurred_at)
            except ValueError:
                return _rejected(
                    "invalid_occurred_at",
                    tuple(event_ids + [event_id]),
                )
            event_ids.append(event_id)
            validated.append((data, timestamp))

        if len(set(event_ids)) != len(event_ids):
            return _rejected("duplicate_event_id", tuple(event_ids))

        groups: dict[str, list[tuple[datetime, str]]] = {}
        unscoped: list[str] = []
        for data, timestamp in validated:
            event_id = str(data["event_id"])
            request_id = data.get("request_id")
            if request_id is None:
                unscoped.append(event_id)
                continue
            if not isinstance(request_id, str) or not request_id:
                return _rejected("invalid_request_id", tuple(event_ids))
            groups.setdefault(request_id, []).append((timestamp, event_id))

        request_orders = tuple(
            RequestEventOrder(
                request_id=request_id,
                ordered_event_ids=tuple(
                    event_id
                    for _, event_id in sorted(
                        groups[request_id],
                        key=lambda item: (item[0], item[1]),
                    )
                ),
            )
            for request_id in sorted(groups)
        )
        unscoped_events = tuple(
            UnscopedEventEvidence(event_id=event_id)
            for event_id in sorted(unscoped)
        )
        reason = (
            "ordered_with_unscoped_events"
            if unscoped_events
            else "ordered"
        )
        evidence_hash = canonical_sha256(
            {
                "format_version": EVENT_ORDERING_VERSION,
                "reason": reason,
                "request_orders": [
                    {
                        "ordered_event_ids": list(order.ordered_event_ids),
                        "ordering_rule": order.ordering_rule,
                        "request_id": order.request_id,
                    }
                    for order in request_orders
                ],
                "unscoped_events": [
                    {
                        "event_id": event.event_id,
                        "ordering_guarantee": event.ordering_guarantee,
                    }
                    for event in unscoped_events
                ],
                "valid": True,
            }
        )
        return EventOrderingResult(
            valid=True,
            reason=reason,
            request_orders=request_orders,
            unscoped_events=unscoped_events,
            evidence_hash=evidence_hash,
        )


def _rejected(reason: str, event_ids: tuple[str, ...]) -> EventOrderingResult:
    evidence_hash = canonical_sha256(
        {
            "event_ids": list(event_ids),
            "format_version": EVENT_ORDERING_VERSION,
            "reason": reason,
            "valid": False,
        }
    )
    return EventOrderingResult(
        valid=False,
        reason=reason,
        request_orders=(),
        unscoped_events=(),
        evidence_hash=evidence_hash,
    )


def _parse_utc(value: object) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError("occurred_at must be a non-empty string")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("occurred_at must be timezone-aware")
    if parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise ValueError("occurred_at must be UTC")
    return parsed.astimezone(timezone.utc)
