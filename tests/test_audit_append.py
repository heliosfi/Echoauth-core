"""Sprint 2A audit append foundation tests."""

from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError

from echoauth.audit import (
    InMemoryAuditLogRepository,
    audit_event_payload,
    hash_audit_event,
)
from echoauth.models import AuditAppendState, AuditRecord


def _record(**overrides: object) -> AuditRecord:
    values: dict[str, object] = {
        "event_type": "audit.record",
        "actor_id": "runtime",
        "reason": "request_accepted",
        "details": {"request": {"id": "req-1", "priority": 2}},
        "occurred_at": "2026-06-19T12:00:00Z",
        "request_id": "req-1",
    }
    values.update(overrides)
    return AuditRecord(**values)  # type: ignore[arg-type]


class AuditAppendTests(unittest.TestCase):
    def test_append_success(self) -> None:
        repository = InMemoryAuditLogRepository()

        result = repository.append(
            _record(), audit_event_id="audit-1", chain_id="audit-main"
        )

        self.assertEqual(result.append_state, AuditAppendState.ACCEPTED)
        self.assertEqual(result.chain_position, 1)
        self.assertIsNone(result.previous_hash)
        self.assertEqual(repository.get("audit-1").event_hash, result.event_hash)

    def test_hash_is_stable_for_equivalent_payloads(self) -> None:
        first = _record(details={"b": 2, "a": {"d": 4, "c": 3}})
        second = _record(details={"a": {"c": 3, "d": 4}, "b": 2})

        first_hash = hash_audit_event(audit_event_payload("audit-1", first), None)
        second_hash = hash_audit_event(audit_event_payload("audit-1", second), None)

        self.assertEqual(first_hash, second_hash)

    def test_previous_hash_chains_accepted_events(self) -> None:
        repository = InMemoryAuditLogRepository()
        first = repository.append(
            _record(), audit_event_id="audit-1", chain_id="audit-main"
        )
        second = repository.append(
            _record(reason="request_completed"),
            audit_event_id="audit-2",
            chain_id="audit-main",
            expected_previous_hash=first.event_hash,
        )

        self.assertEqual(second.append_state, AuditAppendState.ACCEPTED)
        self.assertEqual(second.previous_hash, first.event_hash)
        self.assertEqual(second.chain_position, 2)
        self.assertEqual(
            [event.audit_event_id for event in repository.chain("audit-main")],
            ["audit-1", "audit-2"],
        )

    def test_wrong_expected_previous_hash_conflicts_without_append(self) -> None:
        repository = InMemoryAuditLogRepository()
        first = repository.append(
            _record(), audit_event_id="audit-1", chain_id="audit-main"
        )

        conflict = repository.append(
            _record(reason="request_completed"),
            audit_event_id="audit-2",
            chain_id="audit-main",
            expected_previous_hash="wrong-hash",
        )

        self.assertEqual(conflict.append_state, AuditAppendState.CONFLICT)
        self.assertEqual(conflict.previous_hash, first.event_hash)
        self.assertEqual(len(repository.chain("audit-main")), 1)

    def test_stored_records_are_immutable_and_detached(self) -> None:
        details = {"request": {"id": "req-1"}}
        repository = InMemoryAuditLogRepository()
        repository.append(
            _record(details=details), audit_event_id="audit-1", chain_id="audit-main"
        )
        stored = repository.get("audit-1")
        original_text = stored.canonical_text

        details["request"]["id"] = "changed"
        with self.assertRaises(TypeError):
            stored.record["reason"] = "changed"  # type: ignore[index]
        with self.assertRaises(TypeError):
            stored.record["details"]["request"]["id"] = "changed"  # type: ignore[index]
        with self.assertRaises(FrozenInstanceError):
            stored.event_hash = "changed"  # type: ignore[misc]

        self.assertEqual(repository.get("audit-1").canonical_text, original_text)

    def test_invalid_audit_record_is_rejected(self) -> None:
        repository = InMemoryAuditLogRepository()

        result = repository.append(
            _record(actor_id=""), audit_event_id="audit-1", chain_id="audit-main"
        )

        self.assertEqual(result.append_state, AuditAppendState.REJECTED)
        self.assertEqual(result.reason, "invalid_audit_record")
        self.assertEqual(repository.chain("audit-main"), ())


if __name__ == "__main__":
    unittest.main()
