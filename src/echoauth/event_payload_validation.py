"""Validation-only event payload schema enforcement for Sprint 2T."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from echoauth.canonical import CanonicalDataError, canonical_sha256
from echoauth.events import (
    EventAcceptanceResult,
    EventDeliveryState,
    EventEnvelope,
    InProcessEventAcceptance,
)
from echoauth.events_validation import (
    EventValidationError,
    resolve_payload_schema_path,
    validate_event_envelope,
)

_DRAFT_2020_12 = "https://json-schema.org/draft/2020-12/schema"
_CATALOG_ONLY_EVENT_TYPES = frozenset({"runtime.recovered"})
_ANNOTATION_KEYWORDS = {
    "$id",
    "$schema",
    "$defs",
    "title",
    "description",
    "deprecated",
}
_VALIDATION_KEYWORDS = {
    "$ref",
    "type",
    "required",
    "properties",
    "additionalProperties",
    "items",
    "minLength",
    "minItems",
    "uniqueItems",
    "enum",
    "const",
    "format",
    "allOf",
    "if",
    "then",
}


@dataclass(frozen=True)
class EventPayloadValidationResult:
    """Deterministic schema-validation evidence for one event payload."""

    event_type: str | None
    valid: bool
    reason: str
    schema_path: str | None = None
    payload_hash: str | None = None


class EventPayloadSchemaValidator:
    """Validate payloads against catalog-selected local JSON Schemas."""

    def __init__(
        self,
        catalog_path: str | Path = "events/event-catalog.yaml",
    ) -> None:
        self._catalog_path = Path(catalog_path).resolve()

    def validate(
        self,
        event_type: object,
        payload: object,
    ) -> EventPayloadValidationResult:
        if not isinstance(event_type, str) or not event_type:
            return _invalid(None, "malformed_event_type")
        if event_type in _CATALOG_ONLY_EVENT_TYPES:
            return _invalid(event_type, "catalog_only_event_type")
        if not isinstance(payload, Mapping):
            return _invalid(event_type, "payload_schema_mismatch")
        try:
            payload_hash = canonical_sha256(payload)
        except (CanonicalDataError, TypeError, ValueError):
            return _invalid(event_type, "payload_schema_mismatch")
        try:
            schema_path = resolve_payload_schema_path(
                event_type,
                self._catalog_path,
            )
        except EventValidationError:
            return _invalid(event_type, "unknown_event_type")
        if not schema_path.is_file():
            return _invalid(
                event_type,
                "schema_not_found",
                schema_path=schema_path,
            )
        try:
            schema = _load_schema(schema_path)
        except _MalformedSchemaError:
            return _invalid(
                event_type,
                "malformed_schema",
                schema_path=schema_path,
            )
        try:
            _validate_instance(payload, schema, schema_path, ())
        except _UnresolvedReferenceError:
            return _invalid(
                event_type,
                "unresolved_schema_reference",
                schema_path=schema_path,
            )
        except _MalformedSchemaError:
            return _invalid(
                event_type,
                "malformed_schema",
                schema_path=schema_path,
            )
        except _SchemaMismatchError:
            return _invalid(
                event_type,
                "payload_schema_mismatch",
                schema_path=schema_path,
            )
        return EventPayloadValidationResult(
            event_type=event_type,
            valid=True,
            reason="valid",
            schema_path=schema_path.as_posix(),
            payload_hash=payload_hash,
        )


class SchemaValidatedEventAcceptance:
    """Apply payload schema validation before Sprint 2Q acceptance."""

    def __init__(
        self,
        catalog_path: str | Path = "events/event-catalog.yaml",
    ) -> None:
        self._validator = EventPayloadSchemaValidator(catalog_path)
        self._acceptance = InProcessEventAcceptance(catalog_path)

    def accept(
        self,
        event: EventEnvelope | Mapping[str, object],
    ) -> EventAcceptanceResult:
        event_id, event_type = _event_identity(event)
        if event_type in _CATALOG_ONLY_EVENT_TYPES:
            return _rejected(event_id, event_type, "catalog_only_event_type")
        try:
            data = validate_event_envelope(event)
        except EventValidationError:
            return self._acceptance.accept(event)
        result = self._validator.validate(data["event_type"], data["payload"])
        if not result.valid:
            return _rejected(event_id, event_type, result.reason)
        return self._acceptance.accept(event)


class _SchemaMismatchError(ValueError):
    pass


class _MalformedSchemaError(ValueError):
    pass


class _UnresolvedReferenceError(ValueError):
    pass


def _load_schema(path: Path) -> Mapping[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise _MalformedSchemaError("schema cannot be loaded") from exc
    if not isinstance(value, Mapping):
        raise _MalformedSchemaError("schema root must be an object")
    if value.get("$schema") != _DRAFT_2020_12:
        raise _MalformedSchemaError("schema must declare Draft 2020-12")
    return value


def _validate_instance(
    instance: object,
    schema: Mapping[str, Any],
    schema_path: Path,
    reference_stack: tuple[tuple[Path, str], ...],
) -> None:
    unknown = set(schema) - _ANNOTATION_KEYWORDS - _VALIDATION_KEYWORDS
    if unknown:
        raise _MalformedSchemaError("unsupported schema keyword")
    reference = schema.get("$ref")
    if reference is not None:
        resolved_schema, resolved_path, key = _resolve_reference(
            reference,
            schema,
            schema_path,
        )
        if key in reference_stack:
            raise _UnresolvedReferenceError("cyclic schema reference")
        _validate_instance(
            instance,
            resolved_schema,
            resolved_path,
            reference_stack + (key,),
        )
    _validate_type(instance, schema.get("type"))
    if "const" in schema and instance != schema["const"]:
        raise _SchemaMismatchError("const mismatch")
    if "enum" in schema:
        enum_values = schema["enum"]
        if not isinstance(enum_values, list):
            raise _MalformedSchemaError("enum must be an array")
        if instance not in enum_values:
            raise _SchemaMismatchError("enum mismatch")
    if isinstance(instance, str):
        _validate_string(instance, schema)
    if isinstance(instance, Mapping):
        _validate_object(instance, schema, schema_path, reference_stack)
    if isinstance(instance, list):
        _validate_array(instance, schema, schema_path, reference_stack)
    all_of = schema.get("allOf")
    if all_of is not None:
        if not isinstance(all_of, list):
            raise _MalformedSchemaError("allOf must be an array")
        for child_schema in all_of:
            _require_schema(child_schema)
            _validate_instance(instance, child_schema, schema_path, reference_stack)
    conditional = schema.get("if")
    if conditional is not None:
        _require_schema(conditional)
        try:
            _validate_instance(instance, conditional, schema_path, reference_stack)
        except _SchemaMismatchError:
            pass
        else:
            then_schema = schema.get("then")
            if then_schema is not None:
                _require_schema(then_schema)
                _validate_instance(instance, then_schema, schema_path, reference_stack)


def _resolve_reference(
    reference: object,
    root_schema: Mapping[str, Any],
    schema_path: Path,
) -> tuple[Mapping[str, Any], Path, tuple[Path, str]]:
    if not isinstance(reference, str) or not reference:
        raise _MalformedSchemaError("$ref must be a non-empty string")
    file_part, separator, fragment = reference.partition("#")
    if file_part:
        referenced_path = Path(file_part)
        if referenced_path.is_absolute() or "://" in file_part:
            raise _UnresolvedReferenceError("only local schema references are allowed")
        resolved_path = (schema_path.parent / referenced_path).resolve()
        if not resolved_path.is_file():
            raise _UnresolvedReferenceError("referenced schema is missing")
        referenced_root = _load_schema(resolved_path)
    else:
        resolved_path = schema_path.resolve()
        referenced_root = root_schema
    if not separator or not fragment:
        resolved = referenced_root
        normalized_fragment = ""
    else:
        if not fragment.startswith("/"):
            raise _UnresolvedReferenceError("only JSON Pointer fragments are allowed")
        resolved = _resolve_json_pointer(referenced_root, fragment)
        normalized_fragment = fragment
    _require_schema(resolved)
    return resolved, resolved_path, (resolved_path, normalized_fragment)


def _resolve_json_pointer(root: object, fragment: str) -> object:
    current = root
    for encoded_part in fragment[1:].split("/"):
        part = encoded_part.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, Mapping) or part not in current:
            raise _UnresolvedReferenceError("JSON Pointer target is missing")
        current = current[part]
    return current


def _validate_type(instance: object, expected: object) -> None:
    if expected is None:
        return
    if not isinstance(expected, str) or expected not in _TYPE_CHECKS:
        raise _MalformedSchemaError("unsupported schema type")
    if not _TYPE_CHECKS[expected](instance):
        raise _SchemaMismatchError("type mismatch")


def _validate_string(value: str, schema: Mapping[str, Any]) -> None:
    minimum = schema.get("minLength")
    if minimum is not None:
        if not isinstance(minimum, int) or minimum < 0:
            raise _MalformedSchemaError("minLength must be non-negative")
        if len(value) < minimum:
            raise _SchemaMismatchError("string is too short")
    value_format = schema.get("format")
    if value_format is None:
        return
    if value_format != "date-time":
        raise _MalformedSchemaError("unsupported string format")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise _SchemaMismatchError("invalid date-time") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise _SchemaMismatchError("date-time must be timezone-aware")


def _validate_object(
    value: Mapping[str, object],
    schema: Mapping[str, Any],
    schema_path: Path,
    reference_stack: tuple[tuple[Path, str], ...],
) -> None:
    required = schema.get("required", [])
    if not isinstance(required, list) or any(not isinstance(item, str) for item in required):
        raise _MalformedSchemaError("required must be a string array")
    if any(item not in value for item in required):
        raise _SchemaMismatchError("required property is missing")
    properties = schema.get("properties", {})
    if not isinstance(properties, Mapping):
        raise _MalformedSchemaError("properties must be an object")
    for key, child_schema in properties.items():
        if not isinstance(key, str):
            raise _MalformedSchemaError("property names must be strings")
        _require_schema(child_schema)
        if key in value:
            _validate_instance(
                value[key],
                child_schema,
                schema_path,
                reference_stack,
            )
    additional = schema.get("additionalProperties", True)
    extras = set(value) - set(properties)
    if additional is False and extras:
        raise _SchemaMismatchError("additional properties are not allowed")
    if isinstance(additional, Mapping):
        for key in extras:
            _validate_instance(
                value[key],
                additional,
                schema_path,
                reference_stack,
            )
    elif not isinstance(additional, bool):
        raise _MalformedSchemaError("additionalProperties must be boolean or schema")


def _validate_array(
    value: list[object],
    schema: Mapping[str, Any],
    schema_path: Path,
    reference_stack: tuple[tuple[Path, str], ...],
) -> None:
    minimum = schema.get("minItems")
    if minimum is not None:
        if not isinstance(minimum, int) or minimum < 0:
            raise _MalformedSchemaError("minItems must be non-negative")
        if len(value) < minimum:
            raise _SchemaMismatchError("array has too few items")
    if schema.get("uniqueItems") is True:
        serialized = [
            json.dumps(item, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
            for item in value
        ]
        if len(set(serialized)) != len(serialized):
            raise _SchemaMismatchError("array items must be unique")
    elif "uniqueItems" in schema and schema["uniqueItems"] is not False:
        raise _MalformedSchemaError("uniqueItems must be boolean")
    item_schema = schema.get("items")
    if item_schema is not None:
        _require_schema(item_schema)
        for item in value:
            _validate_instance(item, item_schema, schema_path, reference_stack)


def _require_schema(value: object) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise _MalformedSchemaError("schema must be an object")
    return value


def _event_identity(
    event: EventEnvelope | Mapping[str, object],
) -> tuple[str | None, str | None]:
    if isinstance(event, EventEnvelope):
        return _safe_string(event.event_id), _safe_string(event.event_type)
    if isinstance(event, Mapping):
        return _safe_string(event.get("event_id")), _safe_string(event.get("event_type"))
    return None, None


def _safe_string(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _rejected(
    event_id: str | None,
    event_type: str | None,
    reason: str,
) -> EventAcceptanceResult:
    return EventAcceptanceResult(
        event_id=event_id,
        event_type=event_type,
        delivery_state=EventDeliveryState.REJECTED,
        subscribers_notified=(),
        reason=reason,
    )


def _invalid(
    event_type: str | None,
    reason: str,
    *,
    schema_path: Path | None = None,
) -> EventPayloadValidationResult:
    return EventPayloadValidationResult(
        event_type=event_type,
        valid=False,
        reason=reason,
        schema_path=schema_path.as_posix() if schema_path else None,
    )


_TYPE_CHECKS = {
    "object": lambda value: isinstance(value, Mapping),
    "array": lambda value: isinstance(value, list),
    "string": lambda value: isinstance(value, str),
    "boolean": lambda value: isinstance(value, bool),
    "number": lambda value: isinstance(value, (int, float)) and not isinstance(value, bool),
    "integer": lambda value: isinstance(value, int) and not isinstance(value, bool),
    "null": lambda value: value is None,
}
