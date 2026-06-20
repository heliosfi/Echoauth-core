"""Validation-only event payload-to-schema binding for Sprint 2V."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from echoauth.canonical import canonical_sha256
from echoauth.event_payload_validation import EventPayloadSchemaValidator
from echoauth.events_validation import EventValidationError, resolve_payload_schema_path

_DRAFT_2020_12 = "https://json-schema.org/draft/2020-12/schema"


@dataclass(frozen=True)
class SchemaDependencyEvidence:
    """Canonical evidence for one local referenced schema document."""

    schema_id: str
    schema_hash: str


@dataclass(frozen=True)
class EventSchemaEvidence:
    """Root schema identity and deterministic transitive dependency evidence."""

    schema_id: str
    schema_hash: str
    dependencies: tuple[SchemaDependencyEvidence, ...]


@dataclass(frozen=True)
class EventSchemaBindingResult:
    """Evidence-only payload/schema binding result."""

    event_type: str | None
    valid: bool
    reason: str
    payload_hash: str | None = None
    schema_evidence: EventSchemaEvidence | None = None
    binding_hash: str | None = None


class EventSchemaBindingError(ValueError):
    """Raised when selected schema evidence cannot be resolved safely."""


class EventSchemaBindingValidator:
    """Bind validated payload evidence to explicit selected-schema evidence."""

    def __init__(
        self,
        catalog_path: str | Path = "events/event-catalog.yaml",
    ) -> None:
        self._catalog_path = Path(catalog_path).resolve()
        self._payload_validator = EventPayloadSchemaValidator(self._catalog_path)

    def schema_evidence(self, event_type: str) -> EventSchemaEvidence:
        """Resolve deterministic root and local dependency fingerprints."""

        try:
            root_path = resolve_payload_schema_path(event_type, self._catalog_path)
        except EventValidationError as exc:
            raise EventSchemaBindingError("unknown_event_type") from exc
        documents = _collect_schema_documents(root_path)
        root_document = documents[root_path.resolve()]
        root_id = _schema_id(root_document)
        identities: dict[str, Path] = {}
        for path, document in documents.items():
            schema_id = _schema_id(document)
            previous = identities.get(schema_id)
            if previous is not None and previous != path:
                raise EventSchemaBindingError("ambiguous_schema_binding")
            identities[schema_id] = path
        dependencies = tuple(
            sorted(
                (
                    SchemaDependencyEvidence(
                        schema_id=_schema_id(document),
                        schema_hash=canonical_sha256(document),
                    )
                    for path, document in documents.items()
                    if path != root_path.resolve()
                ),
                key=lambda item: (item.schema_id, item.schema_hash),
            )
        )
        return EventSchemaEvidence(
            schema_id=root_id,
            schema_hash=canonical_sha256(root_document),
            dependencies=dependencies,
        )

    def validate(
        self,
        event_type: object,
        payload: object,
        expected_schema: EventSchemaEvidence | None,
    ) -> EventSchemaBindingResult:
        """Validate a payload and bind it to exactly matching schema evidence."""

        if not isinstance(event_type, str) or not event_type:
            return _rejected(None, "malformed_event_type")
        if expected_schema is None:
            return _rejected(event_type, "missing_schema_binding")
        if not isinstance(expected_schema, EventSchemaEvidence):
            return _rejected(event_type, "malformed_schema_binding")
        payload_result = self._payload_validator.validate(event_type, payload)
        if not payload_result.valid:
            return _rejected(event_type, payload_result.reason)
        try:
            actual_schema = self.schema_evidence(event_type)
        except EventSchemaBindingError as exc:
            return _rejected(event_type, str(exc))
        if expected_schema != actual_schema:
            return _rejected(event_type, "schema_binding_mismatch")
        binding_hash = canonical_sha256(
            {
                "event_type": event_type,
                "payload_hash": payload_result.payload_hash,
                "schema_evidence": asdict(actual_schema),
            }
        )
        return EventSchemaBindingResult(
            event_type=event_type,
            valid=True,
            reason="bound",
            payload_hash=payload_result.payload_hash,
            schema_evidence=actual_schema,
            binding_hash=binding_hash,
        )


def _collect_schema_documents(root_path: Path) -> dict[Path, Mapping[str, Any]]:
    root = root_path.resolve()
    documents: dict[Path, Mapping[str, Any]] = {}
    visiting: set[Path] = set()

    def visit(path: Path) -> None:
        resolved = path.resolve()
        if resolved in documents:
            return
        if resolved in visiting:
            return
        visiting.add(resolved)
        document = _load_schema(resolved)
        documents[resolved] = document
        for reference in _references(document):
            dependency_path, fragment = _resolve_reference_target(
                reference,
                resolved,
            )
            dependency_document = (
                document
                if dependency_path == resolved
                else _load_schema(dependency_path)
            )
            if fragment:
                _resolve_json_pointer(dependency_document, fragment)
            if dependency_path != resolved:
                visit(dependency_path)
        visiting.remove(resolved)

    visit(root)
    return documents


def _load_schema(path: Path) -> Mapping[str, Any]:
    if not path.is_file():
        raise EventSchemaBindingError("schema_not_found")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise EventSchemaBindingError("malformed_schema") from exc
    if not isinstance(value, Mapping):
        raise EventSchemaBindingError("malformed_schema")
    if value.get("$schema") != _DRAFT_2020_12:
        raise EventSchemaBindingError("malformed_schema")
    _schema_id(value)
    return value


def _schema_id(schema: Mapping[str, Any]) -> str:
    schema_id = schema.get("$id")
    if not isinstance(schema_id, str) or not schema_id:
        raise EventSchemaBindingError("missing_schema_id")
    return schema_id


def _references(value: object) -> tuple[str, ...]:
    references: list[str] = []

    def collect(current: object) -> None:
        if isinstance(current, Mapping):
            reference = current.get("$ref")
            if reference is not None:
                if not isinstance(reference, str) or not reference:
                    raise EventSchemaBindingError("malformed_schema")
                references.append(reference)
            for key in sorted(current):
                collect(current[key])
        elif isinstance(current, list):
            for item in current:
                collect(item)

    collect(value)
    return tuple(sorted(set(references)))


def _resolve_reference_target(reference: str, source_path: Path) -> tuple[Path, str]:
    file_part, separator, fragment = reference.partition("#")
    if file_part:
        reference_path = Path(file_part)
        if reference_path.is_absolute() or "://" in file_part:
            raise EventSchemaBindingError("unresolved_schema_reference")
        target_path = (source_path.parent / reference_path).resolve()
    else:
        target_path = source_path.resolve()
    if separator and fragment and not fragment.startswith("/"):
        raise EventSchemaBindingError("unresolved_schema_reference")
    return target_path, fragment


def _resolve_json_pointer(root: object, fragment: str) -> object:
    current = root
    for encoded_part in fragment[1:].split("/"):
        part = encoded_part.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, Mapping) or part not in current:
            raise EventSchemaBindingError("unresolved_schema_reference")
        current = current[part]
    return current


def _rejected(event_type: str | None, reason: str) -> EventSchemaBindingResult:
    return EventSchemaBindingResult(
        event_type=event_type,
        valid=False,
        reason=reason,
    )
