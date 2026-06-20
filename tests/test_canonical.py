"""Sprint 1 canonical data utility tests."""

from __future__ import annotations

import unittest

from echoauth.canonical import (
    CanonicalDataError,
    canonical_json_text,
    canonical_sha256,
    validate_error_list,
    validate_string_reference_list,
)


class CanonicalDataTests(unittest.TestCase):
    def test_equivalent_objects_serialize_identically(self) -> None:
        left = {"b": 2, "a": {"d": 4, "c": 3}}
        right = {"a": {"c": 3, "d": 4}, "b": 2}

        self.assertEqual(canonical_json_text(left), canonical_json_text(right))

    def test_hash_is_stable_for_equivalent_objects(self) -> None:
        left = {"resource": "student-record", "action": "read"}
        right = {"action": "read", "resource": "student-record"}

        self.assertEqual(canonical_sha256(left), canonical_sha256(right))

    def test_non_object_canonical_json_fails(self) -> None:
        with self.assertRaises(CanonicalDataError):
            canonical_json_text(["not", "an", "object"])  # type: ignore[arg-type]

    def test_string_reference_list_preserves_order(self) -> None:
        refs = validate_string_reference_list(["credential:a", "credential:b"])

        self.assertEqual(refs, ("credential:a", "credential:b"))

    def test_string_reference_list_rejects_empty_or_non_string_entries(self) -> None:
        with self.assertRaises(CanonicalDataError):
            validate_string_reference_list([])
        with self.assertRaises(CanonicalDataError):
            validate_string_reference_list(["credential:a", 7])

    def test_validation_error_list_preserves_order(self) -> None:
        errors = validate_error_list(["missing_context", "invalid_scope"])

        self.assertEqual(errors, ("missing_context", "invalid_scope"))

    def test_validation_error_list_rejects_empty_or_non_string_entries(self) -> None:
        with self.assertRaises(CanonicalDataError):
            validate_error_list([])
        with self.assertRaises(CanonicalDataError):
            validate_error_list(["missing_context", ""])


if __name__ == "__main__":
    unittest.main()
