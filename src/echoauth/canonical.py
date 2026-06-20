"""Canonical data utilities for Sprint 1 foundations.

These helpers implement contract-level handling for the shared types defined in
schemas/common.schema.json. They do not validate nested business semantics.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from typing import Any

CanonicalJsonObject = Mapping[str, Any]


class CanonicalDataError(ValueError):
    """Raised when data does not match a Sprint 1 canonical contract type."""


def canonical_json_text(value: CanonicalJsonObject) -> str:
    """Return deterministic JSON text for a canonical JSON object."""

    if not isinstance(value, Mapping):
        raise CanonicalDataError("canonical JSON value must be an object")
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def canonical_sha256(value: CanonicalJsonObject) -> str:
    """Return a stable SHA-256 hash of canonical JSON text."""

    text = canonical_json_text(value)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_string_reference_list(value: object) -> tuple[str, ...]:
    """Validate an ordered list of stable string references."""

    return _validate_string_list(value, "string reference list")


def validate_error_list(value: object) -> tuple[str, ...]:
    """Validate an ordered list of validation errors."""

    return _validate_string_list(value, "validation error list")


def _validate_string_list(value: object, label: str) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise CanonicalDataError(f"{label} must be a list of strings")
    items = tuple(value)
    if not items:
        raise CanonicalDataError(f"{label} must not be empty")
    invalid = [item for item in items if not isinstance(item, str) or not item]
    if invalid:
        raise CanonicalDataError(f"{label} entries must be non-empty strings")
    return items
