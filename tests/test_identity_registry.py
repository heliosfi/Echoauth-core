"""Sprint 2B identity registry tests."""

from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError

from echoauth.identity import (
    DuplicateIdentityError,
    IdentityRecord,
    IdentityState,
    IdentityStatus,
    IdentityValidationError,
    InMemoryIdentityRepository,
    InvalidIdentityTransitionError,
)
from echoauth.models import ActorType


def _record(**overrides: object) -> IdentityRecord:
    values: dict[str, object] = {
        "identity_record_id": "identity-1",
        "actor_id": "actor-1",
        "actor_type": ActorType.HUMAN,
        "status": IdentityStatus.ACTIVE,
        "credential_refs": ("credential-b", "credential-a"),
        "created_at": "2026-06-19T12:00:00Z",
        "updated_at": "2026-06-19T12:00:00Z",
        "role_refs": ("caregiver",),
    }
    values.update(overrides)
    return IdentityRecord(**values)  # type: ignore[arg-type]


class IdentityRegistryTests(unittest.TestCase):
    def test_register_normalizes_credentials_and_hashes_deterministically(self) -> None:
        first_repository = InMemoryIdentityRepository()
        second_repository = InMemoryIdentityRepository()

        first = first_repository.register(_record())
        second = second_repository.register(
            _record(credential_refs=("credential-a", "credential-b"))
        )

        self.assertEqual(first.identity_state, IdentityState.REGISTERED)
        self.assertEqual(first.identity_record.credential_refs, ("credential-a", "credential-b"))
        self.assertEqual(first.record_hash, second.record_hash)

    def test_duplicate_record_or_actor_is_rejected(self) -> None:
        repository = InMemoryIdentityRepository()
        repository.register(_record())

        with self.assertRaises(DuplicateIdentityError):
            repository.register(_record())
        with self.assertRaises(DuplicateIdentityError):
            repository.register(_record(identity_record_id="identity-2"))

    def test_active_identity_requires_credentials(self) -> None:
        repository = InMemoryIdentityRepository()

        with self.assertRaises(IdentityValidationError):
            repository.register(_record(credential_refs=()))

    def test_status_lifecycle_and_revocation_history(self) -> None:
        repository = InMemoryIdentityRepository()
        repository.register(_record())
        suspended = repository.transition(
            "identity-1",
            IdentityStatus.SUSPENDED,
            updated_at="2026-06-19T12:01:00Z",
        )
        active = repository.transition(
            "identity-1",
            IdentityStatus.ACTIVE,
            updated_at="2026-06-19T12:02:00Z",
        )
        revoked = repository.transition(
            "identity-1",
            IdentityStatus.REVOKED,
            updated_at="2026-06-19T12:03:00Z",
        )
        archived = repository.transition(
            "identity-1",
            IdentityStatus.ARCHIVED,
            updated_at="2026-06-19T12:04:00Z",
        )

        self.assertEqual(suspended.identity_state, IdentityState.SUSPENDED)
        self.assertEqual(active.identity_state, IdentityState.ACTIVE)
        self.assertEqual(revoked.identity_state, IdentityState.REVOKED)
        self.assertEqual(archived.identity_state, IdentityState.ARCHIVED)
        self.assertEqual(len(repository.history("identity-1")), 5)

    def test_invalid_transition_is_rejected(self) -> None:
        repository = InMemoryIdentityRepository()
        repository.register(_record())
        repository.transition(
            "identity-1",
            IdentityStatus.REVOKED,
            updated_at="2026-06-19T12:01:00Z",
        )

        with self.assertRaises(InvalidIdentityTransitionError):
            repository.transition(
                "identity-1",
                IdentityStatus.ACTIVE,
                updated_at="2026-06-19T12:02:00Z",
            )

    def test_history_records_are_immutable(self) -> None:
        repository = InMemoryIdentityRepository()
        stored = repository.register(_record())

        with self.assertRaises(FrozenInstanceError):
            stored.record_hash = "changed"  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            stored.identity_record.status = IdentityStatus.REVOKED  # type: ignore[misc]

        self.assertEqual(repository.get("identity-1"), stored)


if __name__ == "__main__":
    unittest.main()
