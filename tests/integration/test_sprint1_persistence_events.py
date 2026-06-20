"""Sprint 1 persistence and event integration tests."""

from __future__ import annotations

import unittest

from echoauth.canonical import canonical_json_text
from echoauth.events import EventEnvelope
from echoauth.events_validation import payload_schema_for_event, validate_event_envelope
from echoauth.persistence import InMemoryRepository


class Sprint1PersistenceEventIntegrationTests(unittest.TestCase):
    def test_canonical_data_persists_and_event_validates(self) -> None:
        repository = InMemoryRepository(identity_field="event_id")
        envelope = EventEnvelope(
            event_id="evt-1",
            event_type="request.submitted",
            producer_id="runtime",
            correlation_id="corr-1",
            payload={"request_id": "req-1", "context": {"b": 2, "a": 1}},
            occurred_at="2026-06-18T00:00:00Z",
        )

        event_data = validate_event_envelope(envelope)
        stored = repository.save(event_data)

        self.assertEqual(stored.canonical_text, canonical_json_text(event_data))
        self.assertEqual(repository.get("evt-1"), stored)
        self.assertEqual(
            payload_schema_for_event("request.submitted"),
            "../schemas/echoauth-request.schema.json",
        )


if __name__ == "__main__":
    unittest.main()
