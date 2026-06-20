"""Sprint 2S validation-only event subscriber authorization tests."""

from __future__ import annotations

import unittest
from dataclasses import replace

from echoauth.event_authorization import (
    AuthorizedEventAcceptance,
    ProducerAuthorizationEvidence,
    producer_authorization_hash,
)
from echoauth.event_subscriber_authorization import (
    EventSubscriberAuthorization,
    EventSubscriberAuthorizationError,
    SubscriberAuthorizationEvidence,
    subscriber_authorization_hash,
)
from echoauth.events import EventDeliveryState, EventEnvelope, InProcessEventAcceptance


def _subscriber_evidence(
    *,
    subscriber_id: str = "audit-monitor",
    allowed_event_types: tuple[str, ...] = ("audit.record",),
) -> SubscriberAuthorizationEvidence:
    evidence = SubscriberAuthorizationEvidence(
        authorization_id=f"authorization-{subscriber_id}",
        subscriber_id=subscriber_id,
        allowed_event_types=allowed_event_types,
        evidence_hash="pending",
    )
    return replace(evidence, evidence_hash=subscriber_authorization_hash(evidence))


def _producer_evidence() -> ProducerAuthorizationEvidence:
    evidence = ProducerAuthorizationEvidence(
        authorization_id="authorization-audit-service",
        producer_id="audit-service",
        allowed_event_types=("audit.record",),
        evidence_hash="pending",
    )
    return replace(evidence, evidence_hash=producer_authorization_hash(evidence))


class EventSubscriberAuthorizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.authorization = EventSubscriberAuthorization((_subscriber_evidence(),))

    def test_authorized_subscriber_for_allowed_event_type(self) -> None:
        result = self.authorization.authorize("audit-monitor", "audit.record")

        self.assertTrue(result.authorized)
        self.assertEqual(result.reason, "authorized")
        self.assertEqual(result.authorization_id, "authorization-audit-monitor")
        self.assertIsNotNone(result.evidence_hash)

    def test_unknown_subscriber_is_rejected(self) -> None:
        result = self.authorization.authorize("unknown", "audit.record")

        self.assertFalse(result.authorized)
        self.assertEqual(result.reason, "unknown_subscriber")
        self.assertIsNone(result.authorization_id)

    def test_malformed_subscriber_evidence_is_rejected(self) -> None:
        evidence = replace(_subscriber_evidence(), evidence_hash="wrong-hash")

        with self.assertRaises(EventSubscriberAuthorizationError):
            EventSubscriberAuthorization((evidence,))

    def test_subscriber_outside_event_scope_is_rejected(self) -> None:
        result = self.authorization.authorize(
            "audit-monitor",
            "authority.verdict",
        )

        self.assertFalse(result.authorized)
        self.assertEqual(
            result.reason,
            "subscriber_event_type_not_authorized",
        )

    def test_runtime_recovered_cannot_be_authorized(self) -> None:
        evidence = _subscriber_evidence(
            subscriber_id="recovery-monitor",
            allowed_event_types=("runtime.recovered",),
        )

        with self.assertRaises(EventSubscriberAuthorizationError):
            EventSubscriberAuthorization((evidence,))

    def test_malformed_authorization_request_fails_closed(self) -> None:
        missing_subscriber = self.authorization.authorize("", "audit.record")
        missing_event_type = self.authorization.authorize("audit-monitor", None)

        self.assertFalse(missing_subscriber.authorized)
        self.assertEqual(missing_subscriber.reason, "malformed_subscriber")
        self.assertFalse(missing_event_type.authorized)
        self.assertEqual(missing_event_type.reason, "malformed_event_type")

    def test_sprint_2q_and_2r_acceptance_remains_unchanged(self) -> None:
        event = EventEnvelope(
            event_id="event-1",
            event_type="audit.record",
            producer_id="audit-service",
            correlation_id="correlation-1",
            payload={"audit_event_id": "audit-1"},
            occurred_at="2026-06-20T12:00:00Z",
        )
        sprint_2q = InProcessEventAcceptance().accept(event)
        sprint_2r = AuthorizedEventAcceptance((_producer_evidence(),)).accept(event)

        self.assertIs(sprint_2q.delivery_state, EventDeliveryState.ACCEPTED)
        self.assertIs(sprint_2r.delivery_state, EventDeliveryState.ACCEPTED)
        self.assertEqual(sprint_2q.payload_hash, sprint_2r.payload_hash)


if __name__ == "__main__":
    unittest.main()
