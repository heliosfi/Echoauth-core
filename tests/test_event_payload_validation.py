"""Sprint 2T validation-only event payload schema tests."""

from __future__ import annotations

import json
import unittest
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory

from echoauth.event_authorization import (
    AuthorizedEventAcceptance,
    ProducerAuthorizationEvidence,
    producer_authorization_hash,
)
from echoauth.event_payload_validation import (
    EventPayloadSchemaValidator,
    SchemaValidatedEventAcceptance,
)
from echoauth.event_subscriber_authorization import (
    EventSubscriberAuthorization,
    SubscriberAuthorizationEvidence,
    subscriber_authorization_hash,
)
from echoauth.events import EventDeliveryState, EventEnvelope, InProcessEventAcceptance


def _audit_payload() -> dict[str, object]:
    return {
        "event_type": "audit.record",
        "actor_id": "audit-service",
        "reason": "accepted",
        "details": {"audit_event_id": "audit-1", "nested": {"open": True}},
        "occurred_at": "2026-06-20T12:00:00Z",
    }


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


class EventPayloadValidationTests(unittest.TestCase):
    def test_valid_payload_is_accepted_for_selected_event_type(self) -> None:
        event = EventEnvelope(
            event_id="event-1",
            event_type="audit.record",
            producer_id="audit-service",
            correlation_id="correlation-1",
            payload=_audit_payload(),
            occurred_at="2026-06-20T12:00:00Z",
        )

        result = SchemaValidatedEventAcceptance().accept(event)

        self.assertIs(result.delivery_state, EventDeliveryState.ACCEPTED)
        self.assertEqual(result.reason, "accepted")

    def test_invalid_payload_is_rejected_for_selected_event_type(self) -> None:
        event = EventEnvelope(
            event_id="event-2",
            event_type="audit.record",
            producer_id="audit-service",
            correlation_id="correlation-2",
            payload={"event_type": "audit.record"},
            occurred_at="2026-06-20T12:00:00Z",
        )

        result = SchemaValidatedEventAcceptance().accept(event)

        self.assertIs(result.delivery_state, EventDeliveryState.REJECTED)
        self.assertEqual(result.reason, "payload_schema_mismatch")

    def test_missing_schema_is_rejected(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog = root / "event-catalog.yaml"
            catalog.write_text(
                "events:\n  - event_type: test.missing\n    payload_schema: missing.schema.json\n",
                encoding="utf-8",
            )
            result = EventPayloadSchemaValidator(catalog).validate(
                "test.missing",
                {},
            )

        self.assertFalse(result.valid)
        self.assertEqual(result.reason, "schema_not_found")

    def test_unresolved_reference_is_rejected(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog = root / "event-catalog.yaml"
            schema = root / "payload.schema.json"
            catalog.write_text(
                "events:\n  - event_type: test.unresolved\n    payload_schema: payload.schema.json\n",
                encoding="utf-8",
            )
            schema.write_text(
                json.dumps(
                    {
                        "$schema": "https://json-schema.org/draft/2020-12/schema",
                        "type": "object",
                        "properties": {
                            "value": {"$ref": "missing.schema.json#/$defs/Value"}
                        },
                    }
                ),
                encoding="utf-8",
            )
            result = EventPayloadSchemaValidator(catalog).validate(
                "test.unresolved",
                {"value": "x"},
            )

        self.assertFalse(result.valid)
        self.assertEqual(result.reason, "unresolved_schema_reference")

    def test_malformed_schema_is_rejected(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog = root / "event-catalog.yaml"
            schema = root / "payload.schema.json"
            catalog.write_text(
                "events:\n  - event_type: test.malformed\n    payload_schema: payload.schema.json\n",
                encoding="utf-8",
            )
            schema.write_text("{bad", encoding="utf-8")
            result = EventPayloadSchemaValidator(catalog).validate(
                "test.malformed",
                {},
            )

        self.assertFalse(result.valid)
        self.assertEqual(result.reason, "malformed_schema")

    def test_open_canonical_object_schema_remains_open(self) -> None:
        payload = {
            "domain_specific": {"nested": [1, 2, {"allowed": True}]},
            "unmodeled": "preserved",
        }

        result = EventPayloadSchemaValidator().validate("identity.verdict", payload)

        self.assertTrue(result.valid)
        self.assertEqual(result.reason, "valid")

    def test_runtime_recovered_is_rejected_before_payload_validation(self) -> None:
        with TemporaryDirectory() as tmp:
            catalog = Path(tmp) / "event-catalog.yaml"
            catalog.write_text(
                "events:\n  - event_type: runtime.recovered\n    payload_schema: missing.schema.json\n",
                encoding="utf-8",
            )
            event = EventEnvelope(
                event_id="event-recovered",
                event_type="runtime.recovered",
                producer_id="recovery-service",
                correlation_id="correlation-recovered",
                payload={},
                occurred_at="2026-06-20T12:00:00Z",
            )
            result = SchemaValidatedEventAcceptance(catalog).accept(event)

        self.assertIs(result.delivery_state, EventDeliveryState.REJECTED)
        self.assertEqual(result.reason, "catalog_only_event_type")

    def test_sprint_2q_2r_and_2s_behavior_remains_unchanged(self) -> None:
        event = EventEnvelope(
            event_id="event-existing",
            event_type="audit.record",
            producer_id="audit-service",
            correlation_id="correlation-existing",
            payload={"audit_event_id": "minimal-existing-payload"},
            occurred_at="2026-06-20T12:00:00Z",
        )

        sprint_2q = InProcessEventAcceptance().accept(event)
        sprint_2r = AuthorizedEventAcceptance((_producer_evidence(),)).accept(event)
        sprint_2s = EventSubscriberAuthorization((_subscriber_evidence(),)).authorize(
            "audit-monitor",
            "audit.record",
        )

        self.assertIs(sprint_2q.delivery_state, EventDeliveryState.ACCEPTED)
        self.assertIs(sprint_2r.delivery_state, EventDeliveryState.ACCEPTED)
        self.assertTrue(sprint_2s.authorized)


if __name__ == "__main__":
    unittest.main()
