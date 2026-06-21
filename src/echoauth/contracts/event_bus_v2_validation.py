"""Fail-closed conformance validation for the draft event-bus v2 contracts.

This module validates repository artifacts only. It does not approve contracts
or provide event acceptance, routing, delivery, retry, persistence, replay,
signing, audit append, authorization, orchestration, or execution behavior.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_DRAFT_2020_12 = "https://json-schema.org/draft/2020-12/schema"
_V2_PATHS = (
    "specs/event-bus-v2.md",
    "contracts/event-bus-v2.yaml",
    "schemas/event-bus-runtime-v2.schema.json",
    "events/event-envelope-v2.schema.json",
    "events/event-catalog-v2.yaml",
    "contracts/event-bus-v2-decision-log.md",
)
_BLOCKERS = (
    "transport_and_acknowledgement_contract",
    "storage_engine_and_transaction_contract",
    "retention_durations_and_deletion_authority",
    "signature_algorithm_registry_and_trust_roots",
    "machine_verifiable_confidential_field_profiles",
    "subscription_registration_and_mutation_authority",
    "audit_writer_chain_and_append_failure_contract",
    "durable_causation_lookup_and_conflict_authority",
)
_RECOVERED_PROHIBITIONS = (
    "accept",
    "produce",
    "subscribe",
    "publish",
    "replay",
    "emit",
)


@dataclass(frozen=True)
class EventBusV2ValidationFailure:
    """One deterministic contract-conformance failure."""

    code: str
    path: str
    message: str


@dataclass(frozen=True)
class EventBusV2ValidationReport:
    """Aggregate v2 contract validation result."""

    failures: tuple[EventBusV2ValidationFailure, ...]

    @property
    def passed(self) -> bool:
        return not self.failures


def validate_event_bus_v2_contracts(
    root: str | Path = ".",
) -> EventBusV2ValidationReport:
    """Validate the complete draft v2 artifact set without approving it."""

    root_path = Path(root).resolve()
    failures: list[EventBusV2ValidationFailure] = []
    for relative_path in _V2_PATHS:
        if not (root_path / relative_path).is_file():
            _fail(failures, "missing_artifact", relative_path, "required v2 artifact is missing")
    if failures:
        return EventBusV2ValidationReport(tuple(failures))

    contract = _load_yaml(root_path, "contracts/event-bus-v2.yaml", failures)
    catalog = _load_yaml(root_path, "events/event-catalog-v2.yaml", failures)
    runtime_schema = _load_json(
        root_path,
        "schemas/event-bus-runtime-v2.schema.json",
        failures,
    )
    envelope_schema = _load_json(
        root_path,
        "events/event-envelope-v2.schema.json",
        failures,
    )
    if failures:
        return EventBusV2ValidationReport(tuple(failures))

    assert contract is not None
    assert catalog is not None
    assert runtime_schema is not None
    assert envelope_schema is not None
    _validate_schema_declarations(runtime_schema, envelope_schema, failures)
    _validate_local_references(root_path, runtime_schema, envelope_schema, failures)
    _validate_schema_identity(contract, catalog, envelope_schema, failures)
    _validate_catalog(root_path, catalog, runtime_schema, failures)
    _validate_vocabularies(contract, runtime_schema, failures)
    _validate_hold_gate(root_path, contract, catalog, failures)
    _validate_blockers(root_path, contract, catalog, failures)
    _validate_runtime_recovered(contract, catalog, failures)
    return EventBusV2ValidationReport(tuple(failures))


def _load_json(
    root: Path,
    relative_path: str,
    failures: list[EventBusV2ValidationFailure],
) -> Mapping[str, Any] | None:
    path = root / relative_path
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        _fail(failures, "invalid_json", relative_path, str(exc))
        return None
    if not isinstance(value, Mapping):
        _fail(failures, "invalid_json_root", relative_path, "JSON root must be an object")
        return None
    return value


def _load_yaml(
    root: Path,
    relative_path: str,
    failures: list[EventBusV2ValidationFailure],
) -> Mapping[str, Any] | None:
    try:
        value = _parse_yaml_subset((root / relative_path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        _fail(failures, "invalid_yaml", relative_path, str(exc))
        return None
    if not isinstance(value, Mapping):
        _fail(failures, "invalid_yaml_root", relative_path, "YAML root must be a mapping")
        return None
    return value


def _validate_schema_declarations(
    runtime_schema: Mapping[str, Any],
    envelope_schema: Mapping[str, Any],
    failures: list[EventBusV2ValidationFailure],
) -> None:
    identities: set[str] = set()
    for path, schema in (
        ("schemas/event-bus-runtime-v2.schema.json", runtime_schema),
        ("events/event-envelope-v2.schema.json", envelope_schema),
    ):
        if schema.get("$schema") != _DRAFT_2020_12:
            _fail(failures, "schema_draft_mismatch", path, "Draft 2020-12 declaration is required")
        schema_id = schema.get("$id")
        if not isinstance(schema_id, str) or not schema_id:
            _fail(failures, "missing_schema_id", path, "non-empty $id is required")
        elif schema_id in identities:
            _fail(failures, "duplicate_schema_id", path, "$id must be unique")
        else:
            identities.add(schema_id)


def _validate_local_references(
    root: Path,
    runtime_schema: Mapping[str, Any],
    envelope_schema: Mapping[str, Any],
    failures: list[EventBusV2ValidationFailure],
) -> None:
    loaded: dict[Path, Mapping[str, Any]] = {
        (root / "schemas/event-bus-runtime-v2.schema.json").resolve(): runtime_schema,
        (root / "events/event-envelope-v2.schema.json").resolve(): envelope_schema,
    }
    visited: set[Path] = set()

    def visit(path: Path, document: Mapping[str, Any]) -> None:
        resolved_path = path.resolve()
        if resolved_path in visited:
            return
        visited.add(resolved_path)
        for reference in _references(document):
            file_part, separator, fragment = reference.partition("#")
            if "://" in file_part or (file_part and Path(file_part).is_absolute()):
                _fail(failures, "non_local_reference", _relative(resolved_path, root), reference)
                continue
            target_path = (
                (resolved_path.parent / file_part).resolve()
                if file_part
                else resolved_path
            )
            target = loaded.get(target_path)
            if target is None:
                target = _load_json(root, _relative(target_path, root), failures)
                if target is None:
                    _fail(failures, "unresolved_reference", _relative(resolved_path, root), reference)
                    continue
                loaded[target_path] = target
            if separator and fragment:
                if not fragment.startswith("/") or _json_pointer(target, fragment) is None:
                    _fail(failures, "unresolved_reference", _relative(resolved_path, root), reference)
                    continue
            visit(target_path, target)

    visit(root / "schemas/event-bus-runtime-v2.schema.json", runtime_schema)
    visit(root / "events/event-envelope-v2.schema.json", envelope_schema)


def _validate_schema_identity(
    contract: Mapping[str, Any],
    catalog: Mapping[str, Any],
    envelope_schema: Mapping[str, Any],
    failures: list[EventBusV2ValidationFailure],
) -> None:
    identity = _mapping(contract.get("schema_identity"))
    artifacts = _mapping(contract.get("artifacts"))
    properties = _mapping(envelope_schema.get("properties"))
    event_schema_id = _mapping(properties.get("event_schema_id")).get("const")
    event_schema_version = _mapping(properties.get("event_schema_version")).get("const")
    expected = (
        ("event_schema_id", envelope_schema.get("$id"), identity.get("event_schema_id")),
        ("envelope_schema_id", envelope_schema.get("$id"), event_schema_id),
        ("event_schema_version", identity.get("event_schema_version"), event_schema_version),
        ("envelope_schema_path", artifacts.get("envelope_schema"), "events/event-envelope-v2.schema.json"),
        ("catalog_path", artifacts.get("catalog"), "events/event-catalog-v2.yaml"),
        ("runtime_schema_path", artifacts.get("runtime_vocabulary_schema"), "schemas/event-bus-runtime-v2.schema.json"),
        ("catalog_envelope", catalog.get("envelope_schema"), "event-envelope-v2.schema.json"),
    )
    for label, actual, required in expected:
        if actual != required:
            _fail(failures, "schema_identity_mismatch", "contracts/event-bus-v2.yaml", label)


def _validate_catalog(
    root: Path,
    catalog: Mapping[str, Any],
    runtime_schema: Mapping[str, Any],
    failures: list[EventBusV2ValidationFailure],
) -> None:
    entries = catalog.get("events")
    if not _sequence(entries):
        _fail(failures, "invalid_catalog", "events/event-catalog-v2.yaml", "events must be a non-empty list")
        return
    assert isinstance(entries, Sequence)
    names: list[str] = []
    confidentiality = set(_enum(runtime_schema, "ConfidentialityClass"))
    integrity = set(_enum(runtime_schema, "IntegrityClass"))
    lifecycle = set(_enum(runtime_schema, "CatalogLifecycleState"))
    retention = set(_enum(runtime_schema, "RetentionClass"))
    replay = set(_enum(runtime_schema, "ReplayPolicy"))
    for index, raw_entry in enumerate(entries):
        entry = _mapping(raw_entry)
        event_type = entry.get("event_type")
        if not isinstance(event_type, str) or not event_type:
            _fail(failures, "invalid_event_type", "events/event-catalog-v2.yaml", str(index))
            continue
        names.append(event_type)
        for field, allowed in (
            ("confidentiality_class", confidentiality),
            ("integrity_class", integrity),
            ("lifecycle_state", lifecycle),
            ("retention_class", retention),
            ("replay_policy", replay),
        ):
            if entry.get(field) not in allowed:
                _fail(failures, "incomplete_catalog_classification", "events/event-catalog-v2.yaml", f"{event_type}:{field}")
        schema_path = entry.get("payload_schema")
        schema_id = entry.get("payload_schema_id")
        schema_version = entry.get("payload_schema_version")
        if not isinstance(schema_path, str) or not schema_path:
            _fail(failures, "missing_payload_schema", "events/event-catalog-v2.yaml", event_type)
            continue
        payload_schema = _load_json(
            root,
            _relative((root / "events" / schema_path).resolve(), root),
            failures,
        )
        if payload_schema is not None and payload_schema.get("$id") != schema_id:
            _fail(failures, "payload_schema_id_mismatch", "events/event-catalog-v2.yaml", event_type)
        if not isinstance(schema_version, str) or not schema_version:
            _fail(failures, "missing_payload_schema_version", "events/event-catalog-v2.yaml", event_type)
    if len(names) != len(set(names)):
        _fail(failures, "duplicate_event_type", "events/event-catalog-v2.yaml", "event types must be unique")
    if names != sorted(names):
        _fail(failures, "nondeterministic_catalog_order", "events/event-catalog-v2.yaml", "event types must sort ascending")


def _validate_vocabularies(
    contract: Mapping[str, Any],
    runtime_schema: Mapping[str, Any],
    failures: list[EventBusV2ValidationFailure],
) -> None:
    checks = (
        ("confidentiality", "classes", "ConfidentialityClass"),
        ("integrity", "classes", "IntegrityClass"),
        ("subscriptions", "states", "SubscriptionState"),
        ("delivery", "states", "DeliveryState"),
        ("replay", "policies", "ReplayPolicy"),
        ("retention_and_offsets", "retention_classes", "RetentionClass"),
    )
    for section, field, definition in checks:
        contract_values = _mapping(contract.get(section)).get(field)
        schema_values = _enum(runtime_schema, definition)
        if not _string_sequence(contract_values) or tuple(contract_values) != schema_values:
            _fail(failures, "vocabulary_mismatch", "contracts/event-bus-v2.yaml", f"{section}.{field}")

    causation = _mapping(contract.get("causation"))
    required_causation = {
        causation.get("missing_causation_id"),
        causation.get("self_reference"),
        causation.get("present_in_batch"),
        causation.get("absent_from_partial_batch"),
    }
    if not required_causation.issubset(set(_enum(runtime_schema, "CausationState"))):
        _fail(failures, "vocabulary_mismatch", "contracts/event-bus-v2.yaml", "causation")


def _validate_hold_gate(
    root: Path,
    contract: Mapping[str, Any],
    catalog: Mapping[str, Any],
    failures: list[EventBusV2ValidationFailure],
) -> None:
    approval = _mapping(contract.get("approval"))
    if contract.get("status") != "hold" or catalog.get("status") != "hold":
        _fail(failures, "hold_not_active", "contracts/event-bus-v2.yaml", "contract and catalog must remain on hold")
    if approval.get("approved") is not False:
        _fail(failures, "approval_must_be_false", "contracts/event-bus-v2.yaml", "draft cannot be approved")
    if approval.get("runtime_implementation_permitted") is not False:
        _fail(failures, "runtime_gate_open", "contracts/event-bus-v2.yaml", "runtime implementation must remain prohibited")
    if catalog.get("runtime_implementation_permitted") is not False:
        _fail(failures, "runtime_gate_open", "events/event-catalog-v2.yaml", "runtime implementation must remain prohibited")
    for path in ("specs/event-bus-v2.md", "contracts/event-bus-v2-decision-log.md"):
        text = (root / path).read_text(encoding="utf-8")
        if "HOLD remains compliant" not in text:
            _fail(failures, "missing_hold_statement", path, "explicit HOLD statement is required")


def _validate_blockers(
    root: Path,
    contract: Mapping[str, Any],
    catalog: Mapping[str, Any],
    failures: list[EventBusV2ValidationFailure],
) -> None:
    contract_blockers = contract.get("approval_blockers")
    catalog_blockers = catalog.get("unresolved_dependencies")
    if not _string_sequence(contract_blockers) or tuple(contract_blockers) != _BLOCKERS:
        _fail(failures, "approval_blocker_mismatch", "contracts/event-bus-v2.yaml", "all eight canonical blockers are required in order")
    if not _string_sequence(catalog_blockers) or tuple(catalog_blockers) != _BLOCKERS:
        _fail(failures, "approval_blocker_mismatch", "events/event-catalog-v2.yaml", "catalog blockers must match the contract")
    log_text = (root / "contracts/event-bus-v2-decision-log.md").read_text(encoding="utf-8")
    blocker_ids = tuple(sorted(set(re.findall(r"EVT2-B(?:0[1-8])", log_text))))
    expected_ids = tuple(f"EVT2-B0{index}" for index in range(1, 9))
    if blocker_ids != expected_ids:
        _fail(failures, "decision_log_blocker_mismatch", "contracts/event-bus-v2-decision-log.md", "EVT2-B01 through EVT2-B08 are required")


def _validate_runtime_recovered(
    contract: Mapping[str, Any],
    catalog: Mapping[str, Any],
    failures: list[EventBusV2ValidationFailure],
) -> None:
    entries = catalog.get("events")
    recovered = [
        _mapping(entry)
        for entry in entries
        if _mapping(entry).get("event_type") == "runtime.recovered"
    ] if _sequence(entries) else []
    if len(recovered) != 1 or recovered[0].get("lifecycle_state") != "catalog_only":
        _fail(failures, "runtime_recovered_not_catalog_only", "events/event-catalog-v2.yaml", "runtime.recovered must occur once as catalog_only")
        return
    if tuple(recovered[0].get("prohibited_operations", ())) != _RECOVERED_PROHIBITIONS:
        _fail(failures, "runtime_recovered_prohibitions", "events/event-catalog-v2.yaml", "all operations must remain prohibited")
    contract_recovered = _mapping(_mapping(contract.get("catalog_only_events")).get("runtime.recovered"))
    if tuple(contract_recovered.get("operations_prohibited", ())) != _RECOVERED_PROHIBITIONS:
        _fail(failures, "runtime_recovered_prohibitions", "contracts/event-bus-v2.yaml", "contract prohibitions must match catalog")


def _references(value: object) -> tuple[str, ...]:
    references: list[str] = []
    if isinstance(value, Mapping):
        reference = value.get("$ref")
        if isinstance(reference, str):
            references.append(reference)
        for child in value.values():
            references.extend(_references(child))
    elif isinstance(value, list):
        for child in value:
            references.extend(_references(child))
    return tuple(references)


def _json_pointer(document: object, fragment: str) -> object | None:
    current = document
    for encoded in fragment[1:].split("/"):
        key = encoded.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, Mapping) or key not in current:
            return None
        current = current[key]
    return current


def _enum(schema: Mapping[str, Any], definition: str) -> tuple[str, ...]:
    definitions = _mapping(schema.get("$defs"))
    values = _mapping(definitions.get(definition)).get("enum")
    return tuple(values) if _string_sequence(values) else ()


def _mapping(value: object) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sequence(value: object) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes))


def _string_sequence(value: object) -> bool:
    return _sequence(value) and all(isinstance(item, str) and item for item in value)


def _relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _fail(
    failures: list[EventBusV2ValidationFailure],
    code: str,
    path: str,
    message: str,
) -> None:
    failures.append(EventBusV2ValidationFailure(code, path, message))


@dataclass(frozen=True)
class _YamlLine:
    number: int
    indent: int
    content: str


def _parse_yaml_subset(text: str) -> object:
    """Parse the deterministic YAML subset used by the v2 contract artifacts."""

    lines: list[_YamlLine] = []
    for number, raw in enumerate(text.splitlines(), start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if "\t" in raw:
            raise ValueError(f"line {number}: tabs are prohibited")
        indent = len(raw) - len(raw.lstrip(" "))
        if indent % 2:
            raise ValueError(f"line {number}: indentation must use two spaces")
        content = raw.strip()
        if content.startswith(("---", "...", "&", "*", "!")):
            raise ValueError(f"line {number}: unsupported YAML construct")
        lines.append(_YamlLine(number, indent, content))
    if not lines:
        raise ValueError("YAML document is empty")
    value, index = _parse_yaml_block(lines, 0, lines[0].indent)
    if index != len(lines):
        raise ValueError(f"line {lines[index].number}: unexpected content")
    return value


def _parse_yaml_block(
    lines: Sequence[_YamlLine],
    index: int,
    indent: int,
) -> tuple[object, int]:
    if lines[index].indent != indent:
        raise ValueError(f"line {lines[index].number}: unexpected indentation")
    if lines[index].content.startswith("- "):
        return _parse_yaml_sequence(lines, index, indent)
    return _parse_yaml_mapping(lines, index, indent)


def _parse_yaml_mapping(
    lines: Sequence[_YamlLine],
    index: int,
    indent: int,
) -> tuple[dict[str, object], int]:
    result: dict[str, object] = {}
    while index < len(lines):
        line = lines[index]
        if line.indent < indent or (line.indent == indent and line.content.startswith("- ")):
            break
        if line.indent != indent:
            raise ValueError(f"line {line.number}: unexpected indentation")
        key, raw_value = _yaml_key_value(line)
        if key in result:
            raise ValueError(f"line {line.number}: duplicate key {key}")
        index += 1
        if raw_value:
            result[key] = _yaml_scalar(raw_value, line.number)
        elif index < len(lines) and lines[index].indent > indent:
            if lines[index].indent != indent + 2:
                raise ValueError(f"line {lines[index].number}: indentation skipped a level")
            result[key], index = _parse_yaml_block(lines, index, indent + 2)
        else:
            result[key] = {}
    return result, index


def _parse_yaml_sequence(
    lines: Sequence[_YamlLine],
    index: int,
    indent: int,
) -> tuple[list[object], int]:
    result: list[object] = []
    while index < len(lines):
        line = lines[index]
        if line.indent < indent or line.indent != indent or not line.content.startswith("- "):
            break
        item = line.content[2:].strip()
        if not item:
            raise ValueError(f"line {line.number}: empty sequence item")
        index += 1
        if ":" not in item:
            result.append(_yaml_scalar(item, line.number))
            continue
        key, raw_value = _yaml_key_value(_YamlLine(line.number, indent + 2, item))
        mapping: dict[str, object] = {
            key: _yaml_scalar(raw_value, line.number) if raw_value else {}
        }
        if index < len(lines) and lines[index].indent > indent:
            if lines[index].indent != indent + 2:
                raise ValueError(f"line {lines[index].number}: indentation skipped a level")
            remainder, index = _parse_yaml_mapping(lines, index, indent + 2)
            duplicate = set(mapping).intersection(remainder)
            if duplicate:
                raise ValueError(f"line {line.number}: duplicate key {sorted(duplicate)[0]}")
            mapping.update(remainder)
        result.append(mapping)
    return result, index


def _yaml_key_value(line: _YamlLine) -> tuple[str, str]:
    if ":" not in line.content:
        raise ValueError(f"line {line.number}: mapping entry requires ':'")
    key, value = line.content.split(":", 1)
    key = key.strip()
    if not key:
        raise ValueError(f"line {line.number}: empty mapping key")
    return key, value.strip()


def _yaml_scalar(value: str, line_number: int) -> object:
    if value.startswith("[") or value.startswith("{"):
        try:
            return json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {line_number}: invalid inline value") from exc
    if value.startswith(('"', "'")):
        if len(value) < 2 or value[-1] != value[0]:
            raise ValueError(f"line {line_number}: unterminated quoted scalar")
        if value[0] == '"':
            try:
                return json.loads(value)
            except json.JSONDecodeError as exc:
                raise ValueError(f"line {line_number}: invalid quoted scalar") from exc
        return value[1:-1].replace("''", "'")
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "~"}:
        return None
    if re.fullmatch(r"-?(?:0|[1-9][0-9]*)", value):
        return int(value)
    return value
