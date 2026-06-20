"""Sprint 2Q validation-only event acceptance tests."""

from __future__ import annotations

import unittest

from echoauth.canonical import canonical_sha256
from echoauth.events import (
    EventAcceptanceResult,
    EventDeliveryState,
    EventEnvelope,
    InProcessEventAcceptance,
)


class EventBusAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.acceptance = InProcessEventAcceptance()
        self.event = EventEnvelope(
            event_id="event-1",
            event_type="audit.record",
            producer_id="audit-service",
            correlation_id="correlation-1",
            payload={"audit_event_id": "audit-1"},
            occurred_at="2026-06-20T12:00:00Z",
            request_id="request-1",
        )

    def test_valid_catalog_event_is_accepted(self) -> None:
        result = self.acceptance.accept(self.event)

        self.assertIsInstance(result, EventAcceptanceResult)
        self.assertIs(result.delivery_state, EventDeliveryState.ACCEPTED)
        self.assertEqual(result.reason, "accepted")
        self.assertEqual(result.subscribers_notified, ())
        self.assertEqual(result.payload_hash, canonical_sha256(self.event.payload))

    def test_missing_required_field_is_rejected(self) -> None:
        result = self.acceptance.accept(
            {
                "event_id": "event-2",
                "event_type": "audit.record",
                "producer_id": "audit-service",
                "payload": {},
                "occurred_at": "2026-06-20T12:00:00Z",
            }
        )

        self.assertIs(result.delivery_state, EventDeliveryState.REJECTED)
        self.assertEqual(result.reason, "invalid_event_envelope")

    def test_unknown_event_type_is_rejected(self) -> None:
        event = EventEnvelope(
            event_id="event-2",
            event_type="unknown.event",
            producer_id="test",
            correlation_id="correlation-2",
            payload={},
            occurred_at="2026-06-20T12:00:00Z",
        )

        result = self.acceptance.accept(event)

        self.assertIs(result.delivery_state, EventDeliveryState.REJECTED)
        self.assertEqual(result.reason, "unknown_event_type")

    def test_duplicate_accepted_event_id_is_rejected(self) -> None:
        first = self.acceptance.accept(self.event)
        second = self.acceptance.accept(self.event)

        self.assertIs(first.delivery_state, EventDeliveryState.ACCEPTED)
        self.assertIs(second.delivery_state, EventDeliveryState.REJECTED)
        self.assertEqual(second.reason, "duplicate_event_id")

    def test_non_utc_timestamp_is_rejected(self) -> None:
        event = EventEnvelope(
            event_id="event-2",
            event_type="audit.record",
            producer_id="audit-service",
            correlation_id="correlation-2",
            payload={},
            occurred_at="2026-06-20T08:00:00-04:00",
        )

        result = self.acceptance.accept(event)

        self.assertIs(result.delivery_state, EventDeliveryState.REJECTED)
        self.assertEqual(result.reason, "invalid_event_envelope")

    def test_unknown_envelope_field_is_rejected(self) -> None:
        result = self.acceptance.accept(
            {
                "event_id": "event-2",
                "event_type": "audit.record",
                "producer_id": "audit-service",
                "correlation_id": "correlation-2",
                "payload": {},
                "occurred_at": "2026-06-20T12:00:00Z",
                "command": "do-not-execute",
            }
        )

        self.assertIs(result.delivery_state, EventDeliveryState.REJECTED)
        self.assertEqual(result.reason, "invalid_event_envelope")

    def test_runtime_recovered_remains_catalog_only(self) -> None:
        event = EventEnvelope(
            event_id="event-recovered",
            event_type="runtime.recovered",
            producer_id="recovery-eligibility",
            correlation_id="correlation-recovered",
            payload={},
            occurred_at="2026-06-20T12:00:00Z",
        )

        result = self.acceptance.accept(event)

        self.assertIs(result.delivery_state, EventDeliveryState.REJECTED)
        self.assertEqual(result.reason, "catalog_only_event_type")

    def test_acceptance_has_no_delivery_methods_or_callbacks(self) -> None:
        self.assertFalse(hasattr(self.acceptance, "publish"))
        self.assertFalse(hasattr(self.acceptance, "subscribe"))
        result = self.acceptance.accept(self.event)
        self.assertEqual(result.subscribers_notified, ())


if __name__ == "__main__":
    unittest.main()
