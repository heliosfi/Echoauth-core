"""Sprint 2U validation-only event ordering tests."""

from __future__ import annotations

import unittest
from dataclasses import replace

from echoauth.event_authorization import (
    AuthorizedEventAcceptance,
    ProducerAuthorizationEvidence,
    producer_authorization_hash,
)
from echoauth.event_ordering import EventOrderingValidator
from echoauth.event_payload_validation import EventPayloadSchemaValidator
from echoauth.event_subscriber_authorization import (
    EventSubscriberAuthorization,
    SubscriberAuthorizationEvidence,
    subscriber_authorization_hash,
)
from echoauth.events import EventDeliveryState, EventEnvelope, InProcessEventAcceptance


def _event(
    event_id: str,
    occurred_at: str,
    *,
    request_id: str | None = "request-1",
) -> EventEnvelope:
    return EventEnvelope(
        event_id=event_id,
        event_type="audit.record",
        producer_id="audit-service",
        correlation_id="correlation-1",
        payload={"audit_event_id": event_id},
        occurred_at=occurred_at,
        request_id=request_id,
    )


def _producer_evidence() -> ProducerAuthorizationEvidence:
    evidence = ProducerAuthorizationEvidence(
        authorization_id="authorization-audit-service",
        producer_id="audit-service",
        allowed_event_types=("audit.record",),
        evidence_hash="pending",
    )
    return replace(evidence, evidence_hash=producer_authorization_hash(evidence))


def _subscriber_evidence() -> SubscriberAuthorizationEvidence:
    evidence = SubscriberAuthorizationEvidence(
        authorization_id="authorization-audit-monitor",
        subscriber_id="audit-monitor",
        allowed_event_types=("audit.record",),
        evidence_hash="pending",
    )
    return replace(evidence, evidence_hash=subscriber_authorization_hash(evidence))


class EventOrderingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = EventOrderingValidator()

    def test_deterministic_ordering_by_occurred_at(self) -> None:
        result = self.validator.validate(
            (
                _event("event-late", "2026-06-20T12:02:00Z"),
                _event("event-early", "2026-06-20T12:00:00Z"),
                _event("event-middle", "2026-06-20T12:01:00Z"),
            )
        )

        self.assertTrue(result.valid)
        self.assertEqual(
            result.request_orders[0].ordered_event_ids,
            ("event-early", "event-middle", "event-late"),
        )

    def test_deterministic_tie_break_by_event_id(self) -> None:
        result = self.validator.validate(
            (
                _event("event-z", "2026-06-20T12:00:00Z"),
                _event("event-a", "2026-06-20T12:00:00Z"),
            )
        )

        self.assertTrue(result.valid)
        self.assertEqual(
            result.request_orders[0].ordered_event_ids,
            ("event-a", "event-z"),
        )

    def test_duplicate_event_id_is_rejected(self) -> None:
        result = self.validator.validate(
            (
                _event("event-1", "2026-06-20T12:00:00Z"),
                _event("event-1", "2026-06-20T12:01:00Z"),
            )
        )

        self.assertFalse(result.valid)
        self.assertEqual(result.reason, "duplicate_event_id")
        self.assertEqual(result.request_orders, ())

    def test_malformed_and_non_utc_occurred_at_are_rejected(self) -> None:
        for value in ("not-a-time", "2026-06-20T08:00:00-04:00"):
            with self.subTest(value=value):
                result = self.validator.validate((_event("event-1", value),))
                self.assertFalse(result.valid)
                self.assertIn(
                    result.reason,
                    {"invalid_event_envelope", "invalid_occurred_at"},
                )

    def test_unscoped_events_have_no_ordering_guarantee(self) -> None:
        result = self.validator.validate(
            (
                _event("event-z", "2026-06-20T12:01:00Z", request_id=None),
                _event("event-a", "2026-06-20T12:00:00Z", request_id=None),
            )
        )

        self.assertTrue(result.valid)
        self.assertEqual(result.reason, "ordered_with_unscoped_events")
        self.assertEqual(result.request_orders, ())
        self.assertEqual(
            {event.ordering_guarantee for event in result.unscoped_events},
            {"none"},
        )

    def test_no_delivery_or_replay_behavior_is_exposed(self) -> None:
        self.assertFalse(hasattr(self.validator, "publish"))
        self.assertFalse(hasattr(self.validator, "deliver"))
        self.assertFalse(hasattr(self.validator, "replay"))
        self.assertFalse(hasattr(self.validator, "offset"))

    def test_prior_event_validation_behavior_remains_unchanged(self) -> None:
        event = _event("event-existing", "2026-06-20T12:00:00Z")
        sprint_2q = InProcessEventAcceptance().accept(event)
        sprint_2r = AuthorizedEventAcceptance((_producer_evidence(),)).accept(event)
        sprint_2s = EventSubscriberAuthorization((_subscriber_evidence(),)).authorize(
            "audit-monitor",
            "audit.record",
        )
        sprint_2t = EventPayloadSchemaValidator().validate(
            "identity.verdict",
            {"open": "payload"},
        )

        self.assertIs(sprint_2q.delivery_state, EventDeliveryState.ACCEPTED)
        self.assertIs(sprint_2r.delivery_state, EventDeliveryState.ACCEPTED)
        self.assertTrue(sprint_2s.authorized)
        self.assertTrue(sprint_2t.valid)


if __name__ == "__main__":
    unittest.main()
