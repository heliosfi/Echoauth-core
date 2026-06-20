"""Sprint 2C canonical authority registry foundation tests."""

from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError, replace

from echoauth.audit import InMemoryAuditLogRepository
from echoauth.auth.authority import (
    AuthorityAuditError,
    AuthorityNotFoundError,
    AuthorityStatus,
    AuthorityType,
    AuthorityValidationError,
    InMemoryAuthorityRepository,
    InvalidAuthorityTransitionError,
    authority_evidence_hash,
    build_authority_record,
)


def _record(**overrides: object):
    values: dict[str, object] = {
        "authority_record_id": "authority-1",
        "authority_source_id": "source-1",
        "subject_id": "subject-1",
        "authority_type": AuthorityType.PARENT,
        "scope": {
            "actions": ["read", "support"],
            "resources": {"records": True},
        },
        "priority": 10,
        "issued_at": "2026-06-19T12:00:00Z",
        "expires_at": "2026-07-19T12:00:00Z",
        "status": AuthorityStatus.ACTIVE,
        "source_document_hash": "document-hash-1",
    }
    values.update(overrides)
    return build_authority_record(**values)  # type: ignore[arg-type]


class AuthorityRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.audit = InMemoryAuditLogRepository()
        self.repository = InMemoryAuthorityRepository(
            self.audit, audit_chain_id="authority-audit"
        )

    def _create(self, record=None, audit_event_id: str = "audit-authority-1"):
        return self.repository.create(
            record or _record(),
            actor_id="registry-admin",
            reason="authority_registered",
            occurred_at="2026-06-19T12:01:00Z",
            audit_event_id=audit_event_id,
        )

    def test_valid_authority_creation_supports_all_categories(self) -> None:
        for index, authority_type in enumerate(AuthorityType, start=1):
            repository = InMemoryAuthorityRepository(
                InMemoryAuditLogRepository(), audit_chain_id=f"authority-{index}"
            )
            record = _record(
                authority_record_id=f"authority-{index}",
                authority_type=authority_type,
            )

            stored = repository.create(
                record,
                actor_id="registry-admin",
                reason="authority_registered",
                occurred_at="2026-06-19T12:01:00Z",
                audit_event_id=f"audit-{index}",
            )

            self.assertEqual(stored.authority_record.authority_type, authority_type)
            self.assertEqual(stored.authority_record.status, AuthorityStatus.ACTIVE)

    def test_invalid_authority_creation_fails_closed(self) -> None:
        with self.assertRaises(AuthorityValidationError):
            _record(scope={})

        valid = _record()
        invalid = replace(valid, evidence_hash="wrong-hash")
        with self.assertRaises(AuthorityValidationError):
            self._create(invalid)

        self.assertEqual(self.audit.chain("authority-audit"), ())

    def test_equal_priority_conflict_fails_closed_without_policy(self) -> None:
        self._create()

        with self.assertRaises(AuthorityValidationError):
            self.repository.create(
                _record(
                    authority_record_id="authority-2",
                    authority_source_id="source-2",
                ),
                actor_id="registry-admin",
                reason="authority_registered",
                occurred_at="2026-06-19T12:02:00Z",
                audit_event_id="audit-authority-2",
            )

        self.assertEqual(len(self.audit.chain("authority-audit")), 1)

    def test_expiration_rules_and_expired_transition(self) -> None:
        with self.assertRaises(AuthorityValidationError):
            _record(expires_at="2026-06-19T11:59:00Z")

        self._create()
        expired = self.repository.update_status(
            "authority-1",
            AuthorityStatus.EXPIRED,
            actor_id="registry-admin",
            reason="authority_expired",
            occurred_at="2026-07-19T12:00:00Z",
            audit_event_id="audit-authority-2",
        )

        self.assertEqual(expired.authority_record.status, AuthorityStatus.EXPIRED)

    def test_status_transitions_preserve_evidence_hash(self) -> None:
        created = self._create()
        suspended = self.repository.update_status(
            "authority-1",
            AuthorityStatus.SUSPENDED,
            actor_id="registry-admin",
            reason="authority_suspended",
            occurred_at="2026-06-19T12:02:00Z",
            audit_event_id="audit-authority-2",
        )
        active = self.repository.update_status(
            "authority-1",
            AuthorityStatus.ACTIVE,
            actor_id="registry-admin",
            reason="authority_reactivated",
            occurred_at="2026-06-19T12:03:00Z",
            audit_event_id="audit-authority-3",
        )

        self.assertEqual(created.authority_record.evidence_hash, suspended.authority_record.evidence_hash)
        self.assertEqual(suspended.authority_record.evidence_hash, active.authority_record.evidence_hash)

    def test_revocation_is_terminal(self) -> None:
        self._create()
        revoked = self.repository.revoke(
            "authority-1",
            actor_id="registry-admin",
            reason="authority_revoked",
            occurred_at="2026-06-19T12:02:00Z",
            audit_event_id="audit-authority-2",
        )

        self.assertEqual(revoked.authority_record.status, AuthorityStatus.REVOKED)
        with self.assertRaises(InvalidAuthorityTransitionError):
            self.repository.update_status(
                "authority-1",
                AuthorityStatus.ACTIVE,
                actor_id="registry-admin",
                reason="invalid_reactivation",
                occurred_at="2026-06-19T12:03:00Z",
                audit_event_id="audit-authority-3",
            )

    def test_evidence_hash_is_stable_and_reproducible(self) -> None:
        first = _record(scope={"b": 2, "a": {"d": 4, "c": 3}})
        second = _record(scope={"a": {"c": 3, "d": 4}, "b": 2})

        self.assertEqual(first.evidence_hash, second.evidence_hash)
        self.assertEqual(first.evidence_hash, authority_evidence_hash(first))

    def test_repository_detaches_and_immutably_stores_scope(self) -> None:
        scope = {"resources": {"records": True}}
        record = _record(scope=scope)
        stored = self._create(record)

        scope["resources"]["records"] = False
        with self.assertRaises(TypeError):
            stored.authority_record.scope["new"] = True  # type: ignore[index]
        with self.assertRaises(TypeError):
            stored.authority_record.scope["resources"]["records"] = False  # type: ignore[index]
        with self.assertRaises(FrozenInstanceError):
            stored.authority_record.status = AuthorityStatus.REVOKED  # type: ignore[misc]

        self.assertTrue(stored.authority_record.scope["resources"]["records"])

    def test_audit_history_is_append_only_and_hash_chained(self) -> None:
        self._create()
        self.repository.update_status(
            "authority-1",
            AuthorityStatus.SUSPENDED,
            actor_id="registry-admin",
            reason="authority_suspended",
            occurred_at="2026-06-19T12:02:00Z",
            audit_event_id="audit-authority-2",
        )
        history = self.repository.history("authority-1")

        self.assertEqual([entry.sequence for entry in history], [1, 2])
        self.assertEqual(history[1].previous_audit_hash, history[0].audit_event_hash)
        self.assertEqual(
            [event.audit_event_id for event in self.audit.chain("authority-audit")],
            ["audit-authority-1", "audit-authority-2"],
        )
        with self.assertRaises(FrozenInstanceError):
            history[0].reason = "changed"  # type: ignore[misc]

    def test_retrieve_appends_lookup_audit_evidence(self) -> None:
        self._create()

        found = self.repository.retrieve(
            "authority-1",
            actor_id="registry-reader",
            occurred_at="2026-06-19T12:02:00Z",
            audit_event_id="audit-authority-lookup",
        )

        self.assertEqual(found.authority_record.authority_record_id, "authority-1")
        self.assertEqual(len(self.audit.chain("authority-audit")), 2)

    def test_failed_audit_append_prevents_authority_creation(self) -> None:
        self._create()

        with self.assertRaises(AuthorityAuditError):
            self.repository.create(
                _record(authority_record_id="authority-2", priority=20),
                actor_id="registry-admin",
                reason="authority_registered",
                occurred_at="2026-06-19T12:02:00Z",
                audit_event_id="audit-authority-1",
            )
        with self.assertRaises(AuthorityNotFoundError):
            self.repository.history("authority-2")


if __name__ == "__main__":
    unittest.main()
