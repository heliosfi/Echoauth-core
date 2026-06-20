"""Sprint 2X validation-only event audit evidence tests."""

from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError, replace

from echoauth.event_audit_evidence import EventAuditEvidencePackager
from echoauth.event_authorization import (
    AuthorizedEventAcceptance,
    ProducerAuthorizationEvidence,
    producer_authorization_hash,
)
from echoauth.event_correlation import EventCorrelationValidator
from echoauth.event_ordering import EventOrderingValidator
from echoauth.event_payload_validation import EventPayloadSchemaValidator
from echoauth.event_schema_binding import EventSchemaBindingValidator
from echoauth.event_subscriber_authorization import (
    EventSubscriberAuthorization,
    SubscriberAuthorizationEvidence,
    subscriber_authorization_hash,
)
from echoauth.events import EventDeliveryState, EventEnvelope, InProcessEventAcceptance


def _event(event_id: str = "event-1") -> EventEnvelope:
    return EventEnvelope(
        event_id=event_id,
        event_type="audit.record",
        producer_id="audit-service",
        correlation_id="correlation-1",
        payload={"audit_event_id": "audit-1"},
        occurred_at="2026-06-20T12:00:00Z",
        request_id="request-1",
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


class EventAuditEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.packager = EventAuditEvidencePackager()

    def test_accepted_event_evidence_is_deterministic_and_immutable(self) -> None:
        event = _event()
        acceptance = InProcessEventAcceptance().accept(event)

        first = self.packager.package(event, acceptance)
        second = self.packager.package(event, acceptance)

        self.assertEqual(first, second)
        self.assertIs(first.delivery_state, EventDeliveryState.ACCEPTED)
        self.assertEqual(first.producer_id, "audit-service")
        self.assertEqual(first.correlation_id, "correlation-1")
        self.assertEqual(first.occurred_at, "2026-06-20T12:00:00Z")
        with self.assertRaises(FrozenInstanceError):
            first.reason = "changed"  # type: ignore[misc]

    def test_rejected_event_evidence_is_packaged_deterministically(self) -> None:
        event = replace(_event(), event_type="unknown.event")
        rejection = InProcessEventAcceptance().accept(event)

        first = self.packager.package(event, rejection)
        second = self.packager.package(event, rejection)

        self.assertEqual(first, second)
        self.assertIs(first.delivery_state, EventDeliveryState.REJECTED)
        self.assertEqual(first.reason, "unknown_event_type")

    def test_malformed_rejection_with_missing_identifiers_is_safe(self) -> None:
        event = {
            "producer_id": "partial-producer",
            "payload": {},
            "occurred_at": "2026-06-20T12:00:00Z",
        }
        rejection = InProcessEventAcceptance().accept(event)

        evidence = self.packager.package(event, rejection)

        self.assertIsNone(evidence.event_id)
        self.assertIsNone(evidence.event_type)
        self.assertIsNone(evidence.correlation_id)
        self.assertEqual(evidence.producer_id, "partial-producer")
        self.assertEqual(evidence.reason, "invalid_event_envelope")

    def test_evidence_hash_changes_when_material_fields_change(self) -> None:
        first_event = _event("event-1")
        second_event = _event("event-2")
        first = self.packager.package(
            first_event,
            InProcessEventAcceptance().accept(first_event),
        )
        second = self.packager.package(
            second_event,
            InProcessEventAcceptance().accept(second_event),
        )

        self.assertNotEqual(first.evidence_hash, second.evidence_hash)

    def test_evidence_does_not_claim_persistence_or_audit_append(self) -> None:
        evidence = self.packager.package(
            _event(),
            InProcessEventAcceptance().accept(_event()),
        )

        for field in ("audit_appended", "persisted", "record_id", "chain_position"):
            self.assertFalse(hasattr(evidence, field))
        for method in ("append", "save", "persist"):
            self.assertFalse(hasattr(self.packager, method))

    def test_evidence_is_non_authorizing(self) -> None:
        evidence = self.packager.package(
            _event(),
            InProcessEventAcceptance().accept(_event()),
        )

        for field in ("authorized", "permission", "authority_id"):
            self.assertFalse(hasattr(evidence, field))
        self.assertFalse(hasattr(self.packager, "authorize"))

    def test_no_signing_delivery_or_replay_behavior_is_exposed(self) -> None:
        for method in ("sign", "publish", "deliver", "route", "replay"):
            self.assertFalse(hasattr(self.packager, method))

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
        sprint_2v = schema_validator.validate(
            "identity.verdict",
            {"open": "payload"},
            schema_validator.schema_evidence("identity.verdict"),
        )
        sprint_2w = EventCorrelationValidator().validate((event,))

        self.assertIs(sprint_2q.delivery_state, EventDeliveryState.ACCEPTED)
        self.assertIs(sprint_2r.delivery_state, EventDeliveryState.ACCEPTED)
        self.assertTrue(sprint_2s.authorized)
        self.assertTrue(sprint_2t.valid)
        self.assertTrue(sprint_2u.valid)
        self.assertTrue(sprint_2v.valid)
        self.assertTrue(sprint_2w.valid)


if __name__ == "__main__":
    unittest.main()
