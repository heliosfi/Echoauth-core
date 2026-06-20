"""Sprint 1 persistence foundation tests."""

from __future__ import annotations

import unittest

from echoauth.canonical import canonical_json_text
from echoauth.persistence import InMemoryRepository, MissingRecordError, RepositoryRecordError


class PersistenceBaseTests(unittest.TestCase):
    def test_save_get_round_trip(self) -> None:
        repository = InMemoryRepository(identity_field="request_id")
        record = {"request_id": "req-1", "payload": {"b": 2, "a": 1}}

        stored = repository.save(record)
        loaded = repository.get("req-1")

        self.assertEqual(stored, loaded)
        self.assertEqual(loaded.record["request_id"], "req-1")

    def test_missing_record_fails_deterministically(self) -> None:
        repository = InMemoryRepository(identity_field="request_id")

        with self.assertRaises(MissingRecordError):
            repository.get("missing")

    def test_canonical_json_text_is_preserved(self) -> None:
        repository = InMemoryRepository(identity_field="request_id")
        record = {"payload": {"z": 1, "a": 2}, "request_id": "req-1"}

        stored = repository.save(record)

        self.assertEqual(stored.canonical_text, canonical_json_text(record))

    def test_invalid_record_fails_deterministically(self) -> None:
        repository = InMemoryRepository(identity_field="request_id")

        with self.assertRaises(RepositoryRecordError):
            repository.save(["not", "a", "mapping"])
        with self.assertRaises(RepositoryRecordError):
            repository.save({"payload": {}})


if __name__ == "__main__":
    unittest.main()
