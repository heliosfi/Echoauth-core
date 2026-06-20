"""Sprint 2R validation-only event producer authorization tests."""

from __future__ import annotations

import unittest
from dataclasses import replace

from echoauth.event_authorization import (
    AuthorizedEventAcceptance,
    EventProducerAuthorizationError,
    ProducerAuthorizationEvidence,
    producer_authorization_hash,
)
from echoauth.events import EventDeliveryState, EventEnvelope


def _producer_evidence(
    *,
    producer_id: str = "audit-service",
    allowed_event_types: tuple[str, ...] = ("audit.record",),
) -> ProducerAuthorizationEvidence:
    evidence = ProducerAuthorizationEvidence(
        authorization_id=f"authorization-{producer_id}",
        producer_id=producer_id,
        allowed_event_types=allowed_event_types,
        evidence_hash="pending",
    )
    return replace(evidence, evidence_hash=producer_authorization_hash(evidence))


class EventProducerAuthorizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.acceptance = AuthorizedEventAcceptance((_producer_evidence(),))
        self.event = EventEnvelope(
            event_id="event-1",
            event_type="audit.record",
            producer_id="audit-service",
            correlation_id="correlation-1",
            payload={"audit_event_id": "audit-1"},
            occurred_at="2026-06-20T12:00:00Z",
        )

    def test_explicitly_authorized_producer_is_accepted(self) -> None:
        result = self.acceptance.accept(self.event)

        self.assertIs(result.delivery_state, EventDeliveryState.ACCEPTED)
        self.assertEqual(result.reason, "accepted")
        self.assertEqual(result.subscribers_notified, ())

    def test_unknown_producer_is_rejected_before_event_acceptance(self) -> None:
        event = replace(self.event, producer_id="unknown-producer")

        result = self.acceptance.accept(event)

        self.assertIs(result.delivery_state, EventDeliveryState.REJECTED)
        self.assertEqual(result.reason, "unknown_producer")
        self.assertIsNone(result.payload_hash)

    def test_known_producer_outside_scope_is_rejected(self) -> None:
        event = replace(self.event, event_type="authority.verdict")

        result = self.acceptance.accept(event)

        self.assertIs(result.delivery_state, EventDeliveryState.REJECTED)
        self.assertEqual(result.reason, "producer_event_type_not_authorized")

    def test_malformed_authorization_evidence_fails_closed(self) -> None:
        evidence = replace(_producer_evidence(), evidence_hash="wrong-hash")

        with self.assertRaises(EventProducerAuthorizationError):
            AuthorizedEventAcceptance((evidence,))

    def test_sprint_2q_validation_rejection_is_unchanged(self) -> None:
        malformed = replace(self.event, occurred_at="not-a-timestamp")

        result = self.acceptance.accept(malformed)

        self.assertIs(result.delivery_state, EventDeliveryState.REJECTED)
        self.assertEqual(result.reason, "invalid_event_envelope")

    def test_runtime_recovered_cannot_be_configured_for_production(self) -> None:
        evidence = _producer_evidence(
            producer_id="recovery-service",
            allowed_event_types=("runtime.recovered",),
        )

        with self.assertRaises(EventProducerAuthorizationError):
            AuthorizedEventAcceptance((evidence,))

    def test_empty_configuration_rejects_every_producer(self) -> None:
        acceptance = AuthorizedEventAcceptance(())

        result = acceptance.accept(self.event)

        self.assertIs(result.delivery_state, EventDeliveryState.REJECTED)
        self.assertEqual(result.reason, "unknown_producer")


if __name__ == "__main__":
    unittest.main()
