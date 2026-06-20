"""Sprint 2W validation-only event relationship tests."""

from __future__ import annotations

import unittest
from dataclasses import replace

from echoauth.event_authorization import (
    AuthorizedEventAcceptance,
    ProducerAuthorizationEvidence,
    producer_authorization_hash,
)
from echoauth.event_correlation import (
    CausationEvidenceState,
    EventCorrelationValidator,
)
from echoauth.event_ordering import EventOrderingValidator
from echoauth.event_payload_validation import EventPayloadSchemaValidator
from echoauth.event_schema_binding import EventSchemaBindingValidator
from echoauth.event_subscriber_authorization import (
    EventSubscriberAuthorization,
    SubscriberAuthorizationEvidence,
    subscriber_authorization_hash,
)
from echoauth.events import EventDeliveryState, EventEnvelope, InProcessEventAcceptance


def _event(
    event_id: str,
    *,
    correlation_id: str = "correlation-1",
    causation_id: str | None = None,
) -> EventEnvelope:
    return EventEnvelope(
        event_id=event_id,
        event_type="audit.record",
        producer_id="audit-service",
        correlation_id=correlation_id,
        payload={"audit_event_id": event_id},
        occurred_at="2026-06-20T12:00:00Z",
        request_id="request-1",
        causation_id=causation_id,
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


class EventCorrelationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = EventCorrelationValidator()

    def test_valid_shared_correlation_id_is_accepted(self) -> None:
        result = self.validator.validate((_event("event-1"), _event("event-2")))

        self.assertTrue(result.valid)
        self.assertEqual(result.reason, "validated")
        self.assertEqual(len(result.correlation_groups), 1)
        self.assertEqual(
            result.correlation_groups[0].event_ids,
            ("event-1", "event-2"),
        )

    def test_malformed_correlation_id_is_rejected(self) -> None:
        event = replace(_event("event-1"), correlation_id="")

        result = self.validator.validate((event,))

        self.assertFalse(result.valid)
        self.assertEqual(result.reason, "invalid_event_envelope")

    def test_present_causation_reference_is_resolved(self) -> None:
        result = self.validator.validate(
            (_event("event-1"), _event("event-2", causation_id="event-1"))
        )

        self.assertTrue(result.valid)
        child = next(item for item in result.event_evidence if item.event_id == "event-2")
        self.assertIs(child.causation_state, CausationEvidenceState.RESOLVED)

    def test_absent_causal_event_is_unresolved_without_inference(self) -> None:
        result = self.validator.validate(
            (_event("event-2", causation_id="event-outside-batch"),)
        )

        self.assertTrue(result.valid)
        self.assertEqual(result.reason, "validated_with_unresolved_causation")
        self.assertEqual(result.unresolved_causation_ids, ("event-outside-batch",))
        self.assertIs(
            result.event_evidence[0].causation_state,
            CausationEvidenceState.UNRESOLVED,
        )

    def test_missing_causation_is_valid_absent_evidence(self) -> None:
        result = self.validator.validate((_event("event-1"),))

        self.assertTrue(result.valid)
        self.assertIsNone(result.event_evidence[0].causation_id)
        self.assertIs(
            result.event_evidence[0].causation_state,
            CausationEvidenceState.ABSENT,
        )

    def test_causation_self_reference_is_rejected(self) -> None:
        result = self.validator.validate(
            (_event("event-1", causation_id="event-1"),)
        )

        self.assertFalse(result.valid)
        self.assertEqual(result.reason, "causation_self_reference")

    def test_no_tracing_persistence_or_delivery_behavior_is_exposed(self) -> None:
        for method in ("trace", "save", "persist", "publish", "deliver", "route"):
            self.assertFalse(hasattr(self.validator, method))

    def test_prior_event_validation_behavior_remains_unchanged(self) -> None:
        event = _event("event-existing")
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
        sprint_2u = EventOrderingValidator().validate((event,))
        schema_validator = EventSchemaBindingValidator()
        schema_evidence = schema_validator.schema_evidence("identity.verdict")
        sprint_2v = schema_validator.validate(
            "identity.verdict",
            {"open": "payload"},
            schema_evidence,
        )

        self.assertIs(sprint_2q.delivery_state, EventDeliveryState.ACCEPTED)
        self.assertIs(sprint_2r.delivery_state, EventDeliveryState.ACCEPTED)
        self.assertTrue(sprint_2s.authorized)
        self.assertTrue(sprint_2t.valid)
        self.assertTrue(sprint_2u.valid)
        self.assertTrue(sprint_2v.valid)


if __name__ == "__main__":
    unittest.main()
