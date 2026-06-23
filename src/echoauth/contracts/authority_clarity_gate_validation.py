"""Mechanical validation for Authority Clarity Gate candidate records.

This module performs local data-shape checks only. Passing validation does not
grant authority, approve execution, resolve blockers, mutate registers, affect
event-bus behavior, create runtime behavior, or create enforcement behavior.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

AUTHORITY_CLARITY_GATE_SCHEMA_PATH = Path("schemas/authority-clarity-gate.schema.json")


@dataclass(frozen=True)
class AuthorityClarityGateValidationIssue:
    """A mechanical schema-conformance issue."""

    location: str
    message: str


@dataclass(frozen=True)
class AuthorityClarityGateValidationReport:
    """Non-authoritative validation result for an Authority Clarity candidate."""

    schema_path: str
    candidate_path: str | None
    issues: tuple[AuthorityClarityGateValidationIssue, ...]

    @property
    def passed(self) -> bool:
        """Return true when the candidate has no mechanical conformance issues."""

        return not self.issues

    @property
    def non_authoritative(self) -> bool:
        """Always true; this report never grants authority or execution."""

        return True


def load_authority_clarity_gate_schema(
    root: str | Path = ".",
    schema_path: str | Path = AUTHORITY_CLARITY_GATE_SCHEMA_PATH,
) -> Mapping[str, Any]:
    """Load the Authority Clarity Gate schema as reference data only."""

    path = _resolve_path(root, schema_path)
    schema = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(schema, Mapping):
        raise ValueError("Authority Clarity Gate schema must be a JSON object")
    return schema


def validate_authority_clarity_gate_file(
    candidate_path: str | Path,
    *,
    root: str | Path = ".",
    schema_path: str | Path = AUTHORITY_CLARITY_GATE_SCHEMA_PATH,
) -> AuthorityClarityGateValidationReport:
    """Validate a candidate JSON file against the Authority Clarity schema."""

    candidate = _resolve_path(root, candidate_path)
    display_candidate = _display_path(candidate, root)
    schema, schema_issue = _load_schema_for_report(root, schema_path)
    if schema_issue is not None:
        return AuthorityClarityGateValidationReport(
            _display_path(_resolve_path(root, schema_path), root),
            display_candidate,
            (schema_issue,),
        )
    try:
        record = json.loads(candidate.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issue = AuthorityClarityGateValidationIssue("$", "candidate file is missing")
        return AuthorityClarityGateValidationReport(
            _display_path(_resolve_path(root, schema_path), root),
            display_candidate,
            (issue,),
        )
    except json.JSONDecodeError as exc:
        issue = AuthorityClarityGateValidationIssue("$", f"invalid JSON: {exc.msg}")
        return AuthorityClarityGateValidationReport(
            _display_path(_resolve_path(root, schema_path), root),
            display_candidate,
            (issue,),
        )
    return validate_authority_clarity_gate_record(
        record,
        schema=schema,
        schema_path=schema_path,
        candidate_path=display_candidate,
        root=root,
    )


def validate_authority_clarity_gate_record(
    record: object,
    *,
    schema: Mapping[str, Any] | None = None,
    schema_path: str | Path = AUTHORITY_CLARITY_GATE_SCHEMA_PATH,
    candidate_path: str | None = None,
    root: str | Path = ".",
) -> AuthorityClarityGateValidationReport:
    """Validate a candidate record without creating authority or live effects."""

    if schema is None:
        schema, schema_issue = _load_schema_for_report(root, schema_path)
        if schema_issue is not None:
            return AuthorityClarityGateValidationReport(
                _display_path(_resolve_path(root, schema_path), root),
                candidate_path,
                (schema_issue,),
            )
    issues: list[AuthorityClarityGateValidationIssue] = []
    if not isinstance(record, Mapping):
        issues.append(AuthorityClarityGateValidationIssue("$", "candidate must be an object"))
    else:
        _validate_value(record, schema, _defs(schema), "$", issues)
    return AuthorityClarityGateValidationReport(
        _display_path(_resolve_path(root, schema_path), root),
        candidate_path,
        tuple(issues),
    )


def _load_schema_for_report(
    root: str | Path,
    schema_path: str | Path,
) -> tuple[Mapping[str, Any], AuthorityClarityGateValidationIssue | None]:
    try:
        return load_authority_clarity_gate_schema(root, schema_path), None
    except FileNotFoundError:
        issue = AuthorityClarityGateValidationIssue("$", "schema file is missing")
    except json.JSONDecodeError as exc:
        issue = AuthorityClarityGateValidationIssue("$", f"invalid schema JSON: {exc.msg}")
    except ValueError as exc:
        issue = AuthorityClarityGateValidationIssue("$", str(exc))
    return {}, issue


def _validate_value(
    value: object,
    schema: Mapping[str, Any],
    defs: Mapping[str, Any],
    location: str,
    issues: list[AuthorityClarityGateValidationIssue],
) -> None:
    schema = _resolve_schema(schema, defs)
    expected_type = schema.get("type")
    if expected_type is not None and not _type_matches(value, expected_type):
        issues.append(
            AuthorityClarityGateValidationIssue(
                location,
                f"expected {_type_name(expected_type)}",
            )
        )
        return
    if "const" in schema and value != schema["const"]:
        issues.append(
            AuthorityClarityGateValidationIssue(
                location,
                f"expected constant {schema['const']!r}",
            )
        )
    enum = schema.get("enum")
    if isinstance(enum, list) and value not in enum:
        issues.append(AuthorityClarityGateValidationIssue(location, "value is not allowed"))
    if isinstance(value, str):
        _validate_string(value, schema, location, issues)
    if isinstance(value, Mapping):
        _validate_object(value, schema, defs, location, issues)
    if isinstance(value, list):
        _validate_array(value, schema, defs, location, issues)
    for sub_schema in schema.get("allOf", ()):
        if isinstance(sub_schema, Mapping):
            _validate_value(value, sub_schema, defs, location, issues)


def _validate_string(
    value: str,
    schema: Mapping[str, Any],
    location: str,
    issues: list[AuthorityClarityGateValidationIssue],
) -> None:
    min_length = schema.get("minLength")
    if isinstance(min_length, int) and len(value) < min_length:
        issues.append(
            AuthorityClarityGateValidationIssue(
                location,
                f"expected length at least {min_length}",
            )
        )
    if schema.get("format") == "date-time" and not _is_date_time(value):
        issues.append(AuthorityClarityGateValidationIssue(location, "expected date-time string"))


def _validate_object(
    value: Mapping[object, object],
    schema: Mapping[str, Any],
    defs: Mapping[str, Any],
    location: str,
    issues: list[AuthorityClarityGateValidationIssue],
) -> None:
    required = schema.get("required", ())
    if isinstance(required, list):
        for key in required:
            if key not in value:
                issues.append(
                    AuthorityClarityGateValidationIssue(
                        _member_location(location, str(key)),
                        "required field is missing",
                    )
                )
    properties = schema.get("properties", {})
    if not isinstance(properties, Mapping):
        properties = {}
    if schema.get("additionalProperties") is False:
        for key in sorted(str(key) for key in value.keys() if key not in properties):
            issues.append(
                AuthorityClarityGateValidationIssue(
                    _member_location(location, key),
                    "additional property is not allowed",
                )
            )
    for key, sub_schema in properties.items():
        if key in value and isinstance(sub_schema, Mapping):
            _validate_value(value[key], sub_schema, defs, _member_location(location, key), issues)


def _validate_array(
    value: list[object],
    schema: Mapping[str, Any],
    defs: Mapping[str, Any],
    location: str,
    issues: list[AuthorityClarityGateValidationIssue],
) -> None:
    item_schema = schema.get("items")
    if isinstance(item_schema, Mapping):
        for index, item in enumerate(value):
            _validate_value(item, item_schema, defs, f"{location}[{index}]", issues)
    if schema.get("uniqueItems") is True:
        _validate_unique_items(value, location, issues)
    contains = schema.get("contains")
    if isinstance(contains, Mapping) and not any(
        _matches_schema(item, contains, defs, f"{location}[{index}]")
        for index, item in enumerate(value)
    ):
        issues.append(
            AuthorityClarityGateValidationIssue(
                location,
                f"array does not contain required value {_contains_label(contains)}",
            )
        )


def _validate_unique_items(
    value: list[object],
    location: str,
    issues: list[AuthorityClarityGateValidationIssue],
) -> None:
    seen: set[str] = set()
    for item in value:
        marker = _json_marker(item)
        if marker in seen:
            issues.append(AuthorityClarityGateValidationIssue(location, "array items must be unique"))
            return
        seen.add(marker)


def _matches_schema(
    value: object,
    schema: Mapping[str, Any],
    defs: Mapping[str, Any],
    location: str,
) -> bool:
    issues: list[AuthorityClarityGateValidationIssue] = []
    _validate_value(value, schema, defs, location, issues)
    return not issues


def _resolve_schema(schema: Mapping[str, Any], defs: Mapping[str, Any]) -> Mapping[str, Any]:
    ref = schema.get("$ref")
    if isinstance(ref, str) and ref.startswith("#/$defs/"):
        name = ref.removeprefix("#/$defs/")
        resolved = defs.get(name)
        if isinstance(resolved, Mapping):
            return resolved
    return schema


def _defs(schema: Mapping[str, Any]) -> Mapping[str, Any]:
    defs = schema.get("$defs")
    return defs if isinstance(defs, Mapping) else {}


def _type_matches(value: object, expected_type: object) -> bool:
    if expected_type == "object":
        return isinstance(value, Mapping)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "boolean":
        return isinstance(value, bool)
    return True


def _type_name(expected_type: object) -> str:
    return expected_type if isinstance(expected_type, str) else "supported JSON type"


def _member_location(location: str, key: str) -> str:
    return f"{location}.{key}" if location != "$" else f"$.{key}"


def _is_date_time(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def _json_marker(value: object) -> str:
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    except TypeError:
        return repr(value)


def _contains_label(schema: Mapping[str, Any]) -> str:
    if "const" in schema:
        return repr(schema["const"])
    return "matching contains schema"


def _resolve_path(root: str | Path, path: str | Path) -> Path:
    raw_path = Path(path)
    if raw_path.is_absolute():
        return raw_path
    return Path(root) / raw_path


def _display_path(path: Path, root: str | Path) -> str:
    try:
        return path.relative_to(Path(root)).as_posix()
    except ValueError:
        return path.as_posix()
