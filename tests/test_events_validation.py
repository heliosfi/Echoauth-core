"""Sprint 1 event validation tests."""

from __future__ import annotations

import unittest

from echoauth.events import EventEnvelope
from echoauth.events_validation import (
    EventValidationError,
    load_event_catalog,
    payload_schema_for_event,
    validate_event_envelope,
)


class EventValidationTests(unittest.TestCase):
    def test_event_envelope_validates_required_fields(self) -> None:
        envelope = EventEnvelope(
            event_id="evt-1",
            event_type="request.submitted",
            producer_id="runtime",
            correlation_id="corr-1",
            payload={"request_id": "req-1"},
            occurred_at="2026-06-18T00:00:00Z",
        )

        data = validate_event_envelope(envelope)

        self.assertEqual(data["event_id"], "evt-1")

    def test_event_envelope_rejects_missing_required_fields(self) -> None:
        with self.assertRaises(EventValidationError):
            validate_event_envelope(
                {
                    "event_id": "evt-1",
                    "event_type": "request.submitted",
                    "producer_id": "runtime",
                    "payload": {},
                    "occurred_at": "2026-06-18T00:00:00Z",
                }
            )

    def test_event_envelope_rejects_non_object_payload(self) -> None:
        with self.assertRaises(EventValidationError):
            validate_event_envelope(
                {
                    "event_id": "evt-1",
                    "event_type": "request.submitted",
                    "producer_id": "runtime",
                    "correlation_id": "corr-1",
                    "payload": ["not", "object"],
                    "occurred_at": "2026-06-18T00:00:00Z",
                }
            )

    def test_event_catalog_maps_event_types(self) -> None:
        catalog = load_event_catalog()

        self.assertEqual(catalog["request.submitted"], "../schemas/echoauth-request.schema.json")
        self.assertEqual(payload_schema_for_event("audit.record"), "../schemas/audit-record.schema.json")

    def test_unknown_event_type_fails_deterministically(self) -> None:
        with self.assertRaises(EventValidationError):
            payload_schema_for_event("unknown.event")


if __name__ == "__main__":
    unittest.main()
