"""Sprint 2V validation-only event schema binding tests."""

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
from echoauth.event_ordering import EventOrderingValidator
from echoauth.event_payload_validation import EventPayloadSchemaValidator
from echoauth.event_schema_binding import (
    EventSchemaBindingValidator,
    EventSchemaEvidence,
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
        "details": {"audit_event_id": "audit-1"},
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


class EventSchemaBindingTests(unittest.TestCase):
    def test_valid_payload_schema_binding_is_accepted(self) -> None:
        validator = EventSchemaBindingValidator()
        evidence = validator.schema_evidence("audit.record")

        result = validator.validate("audit.record", _audit_payload(), evidence)

        self.assertTrue(result.valid)
        self.assertEqual(result.reason, "bound")
        self.assertIsNotNone(result.payload_hash)
        self.assertIsNotNone(result.binding_hash)
        self.assertEqual(result.schema_evidence, evidence)

    def test_payload_bound_to_wrong_schema_is_rejected(self) -> None:
        validator = EventSchemaBindingValidator()
        wrong_evidence = validator.schema_evidence("identity.verdict")

        result = validator.validate(
            "audit.record",
            _audit_payload(),
            wrong_evidence,
        )

        self.assertFalse(result.valid)
        self.assertEqual(result.reason, "schema_binding_mismatch")

    def test_local_reference_dependency_affects_fingerprint(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog = root / "event-catalog.yaml"
            schema = root / "root.schema.json"
            dependency = root / "dependency.schema.json"
            catalog.write_text(
                "events:\n  - event_type: test.bound\n    payload_schema: root.schema.json\n",
                encoding="utf-8",
            )
            schema.write_text(
                json.dumps(
                    {
                        "$schema": "https://json-schema.org/draft/2020-12/schema",
                        "$id": "https://echoauth.local/test/root.schema.json",
                        "type": "object",
                        "properties": {
                            "value": {
                                "$ref": "dependency.schema.json#/$defs/Value"
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            dependency.write_text(
                json.dumps(
                    {
                        "$schema": "https://json-schema.org/draft/2020-12/schema",
                        "$id": "https://echoauth.local/test/dependency.schema.json",
                        "$defs": {"Value": {"type": "string"}},
                    }
                ),
                encoding="utf-8",
            )
            validator = EventSchemaBindingValidator(catalog)
            first = validator.schema_evidence("test.bound")
            dependency.write_text(
                json.dumps(
                    {
                        "$schema": "https://json-schema.org/draft/2020-12/schema",
                        "$id": "https://echoauth.local/test/dependency.schema.json",
                        "$defs": {"Value": {"type": "string", "minLength": 2}},
                    }
                ),
                encoding="utf-8",
            )
            second = validator.schema_evidence("test.bound")

        self.assertEqual(first.schema_hash, second.schema_hash)
        self.assertNotEqual(first.dependencies, second.dependencies)

    def test_missing_schema_binding_is_rejected(self) -> None:
        result = EventSchemaBindingValidator().validate(
            "audit.record",
            _audit_payload(),
            None,
        )

        self.assertFalse(result.valid)
        self.assertEqual(result.reason, "missing_schema_binding")

    def test_ambiguous_schema_version_evidence_is_rejected(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog = root / "event-catalog.yaml"
            schema = root / "root.schema.json"
            first = root / "first.schema.json"
            second = root / "second.schema.json"
            catalog.write_text(
                "events:\n  - event_type: test.ambiguous\n    payload_schema: root.schema.json\n",
                encoding="utf-8",
            )
            schema.write_text(
                json.dumps(
                    {
                        "$schema": "https://json-schema.org/draft/2020-12/schema",
                        "$id": "https://echoauth.local/test/root.schema.json",
                        "type": "object",
                        "properties": {
                            "a": {"$ref": "first.schema.json#/$defs/Value"},
                            "b": {"$ref": "second.schema.json#/$defs/Value"},
                        },
                    }
                ),
                encoding="utf-8",
            )
            shared_id = "https://echoauth.local/test/shared.schema.json"
            for path, value_type in ((first, "string"), (second, "integer")):
                path.write_text(
                    json.dumps(
                        {
                            "$schema": "https://json-schema.org/draft/2020-12/schema",
                            "$id": shared_id,
                            "$defs": {"Value": {"type": value_type}},
                        }
                    ),
                    encoding="utf-8",
                )
            validator = EventSchemaBindingValidator(catalog)
            result = validator.validate(
                "test.ambiguous",
                {"a": "value", "b": 1},
                EventSchemaEvidence(
                    schema_id="https://echoauth.local/test/root.schema.json",
                    schema_hash="expected",
                    dependencies=(),
                ),
            )

        self.assertFalse(result.valid)
        self.assertEqual(result.reason, "ambiguous_schema_binding")

    def test_no_signing_persistence_or_delivery_behavior_is_exposed(self) -> None:
        validator = EventSchemaBindingValidator()

        for method in ("sign", "save", "persist", "publish", "deliver", "replay"):
            self.assertFalse(hasattr(validator, method))

    def test_prior_event_validation_behavior_remains_unchanged(self) -> None:
        event = EventEnvelope(
            event_id="event-existing",
            event_type="audit.record",
            producer_id="audit-service",
            correlation_id="correlation-existing",
            payload={"audit_event_id": "minimal-existing-payload"},
            occurred_at="2026-06-20T12:00:00Z",
            request_id="request-1",
        )
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

        self.assertIs(sprint_2q.delivery_state, EventDeliveryState.ACCEPTED)
        self.assertIs(sprint_2r.delivery_state, EventDeliveryState.ACCEPTED)
        self.assertTrue(sprint_2s.authorized)
        self.assertTrue(sprint_2t.valid)
        self.assertTrue(sprint_2u.valid)


if __name__ == "__main__":
    unittest.main()
