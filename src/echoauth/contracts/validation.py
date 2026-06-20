"""Repository contract validation harness.

Sprint 1 scope: validate generated repository artifacts without implementing
runtime governance, authorization, policy, audit-chain, or execution behavior.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable, Iterable

YamlParser = Callable[[str], object]
_DEFAULT_YAML_PARSER = object()


class CheckStatus(str, Enum):
    """Validation check status."""

    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"


@dataclass(frozen=True)
class ValidationCheck:
    """Single contract validation check result."""

    name: str
    path: str
    status: CheckStatus
    message: str


@dataclass(frozen=True)
class ValidationReport:
    """Contract validation report."""

    checks: tuple[ValidationCheck, ...]

    @property
    def passed(self) -> bool:
        """Return true when no check failed."""

        return all(check.status is not CheckStatus.FAIL for check in self.checks)

    def failures(self) -> tuple[ValidationCheck, ...]:
        """Return failed checks."""

        return tuple(check for check in self.checks if check.status is CheckStatus.FAIL)


JSON_SCHEMA_GLOBS = ("schemas/*.json", "events/*.json")
YAML_CONTRACT_PATHS = (
    "api/openapi.yaml",
    "contracts/service-contracts.yaml",
    "contracts/integration-contracts.yaml",
    "contracts/recovery-service.yaml",
    "events/event-catalog.yaml",
)
REQUIRED_PATHS = (
    "api/openapi.yaml",
    "contracts/protobuf/echoauth.proto",
    "contracts/service-contracts.yaml",
    "contracts/integration-contracts.yaml",
    "contracts/recovery-service.yaml",
    "events/event-catalog.yaml",
    "events/event-envelope.schema.json",
    "schemas/recovery-request.schema.json",
    "schemas/recovery-result.schema.json",
    "schemas/recovery-review-protocol.schema.json",
    "schemas/governance-runtime-proposal.schema.json",
    "database/schema.sql",
)


def validate_contracts(
    root: str | Path = ".",
    require_optional_tools: bool = False,
    yaml_parser: YamlParser | None | object = _DEFAULT_YAML_PARSER,
) -> ValidationReport:
    """Validate Sprint 1 repository contract artifacts.

    YAML parsing is mandatory and never skipped. Protobuf compiler syntax
    checks remain optional because Sprint 1 only requires deterministic
    protobuf artifact validation when compiler tooling is unavailable.
    """

    root_path = Path(root)
    checks: list[ValidationCheck] = []
    checks.extend(_check_required_paths(root_path, REQUIRED_PATHS))
    checks.extend(_check_json_artifacts(root_path, JSON_SCHEMA_GLOBS))
    checks.append(_check_openapi_structure(root_path / "api/openapi.yaml", root_path))
    checks.extend(_check_yaml_artifacts(root_path, YAML_CONTRACT_PATHS, yaml_parser))
    checks.append(_check_database_schema(root_path / "database/schema.sql", root_path))
    checks.append(_check_protobuf(root_path / "contracts/protobuf/echoauth.proto", root_path, require_optional_tools))
    return ValidationReport(tuple(checks))


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _pass(name: str, path: Path, root: Path, message: str) -> ValidationCheck:
    return ValidationCheck(name, _relative(path, root), CheckStatus.PASS, message)


def _fail(name: str, path: Path, root: Path, message: str) -> ValidationCheck:
    return ValidationCheck(name, _relative(path, root), CheckStatus.FAIL, message)


def _skip(name: str, path: Path, root: Path, message: str) -> ValidationCheck:
    return ValidationCheck(name, _relative(path, root), CheckStatus.SKIP, message)


def _check_required_paths(root: Path, paths: Iterable[str]) -> tuple[ValidationCheck, ...]:
    checks: list[ValidationCheck] = []
    for relative_path in paths:
        path = root / relative_path
        if path.is_file():
            checks.append(_pass("required_path", path, root, "artifact exists"))
        else:
            checks.append(_fail("required_path", path, root, "artifact is missing"))
    return tuple(checks)


def _check_json_artifacts(root: Path, patterns: Iterable[str]) -> tuple[ValidationCheck, ...]:
    checks: list[ValidationCheck] = []
    for pattern in patterns:
        for path in sorted(root.glob(pattern)):
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                checks.append(_fail("json_parse", path, root, f"invalid JSON: {exc.msg}"))
            else:
                checks.append(_pass("json_parse", path, root, "valid JSON"))
    if not checks:
        checks.append(_fail("json_parse", root, root, "no JSON artifacts found"))
    return tuple(checks)


def _check_openapi_structure(path: Path, root: Path) -> ValidationCheck:
    if not path.is_file():
        return _fail("openapi_structure", path, root, "OpenAPI artifact is missing")
    text = path.read_text(encoding="utf-8")
    required_markers = ("openapi:", "paths:", "components:")
    missing = [marker for marker in required_markers if marker not in text]
    if missing:
        return _fail("openapi_structure", path, root, f"missing markers: {', '.join(missing)}")
    return _pass("openapi_structure", path, root, "required OpenAPI markers present")


def _check_yaml_artifacts(
    root: Path,
    paths: Iterable[str],
    yaml_parser: YamlParser | None | object,
) -> tuple[ValidationCheck, ...]:
    parser = _load_yaml_parser() if yaml_parser is _DEFAULT_YAML_PARSER else yaml_parser
    checks: list[ValidationCheck] = []
    for relative_path in paths:
        path = root / relative_path
        if not path.is_file():
            checks.append(_fail("yaml_parse", path, root, "YAML artifact is missing"))
            continue
        if parser is None:
            message = "YAML parser unavailable; install PyYAML or use the built-in Sprint 1 YAML validator"
            checks.append(_fail("yaml_parse", path, root, message))
            continue
        try:
            parser(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - parser-specific exception types vary.
            checks.append(_fail("yaml_parse", path, root, f"invalid YAML: {exc}"))
        else:
            checks.append(_pass("yaml_parse", path, root, "valid YAML"))
    return tuple(checks)


def _load_yaml_parser():
    try:
        import yaml  # type: ignore
    except ModuleNotFoundError:
        return _parse_yaml_subset
    return yaml.safe_load


def _parse_yaml_subset(text: str) -> object:
    """Validate the YAML subset used by EchoAuth repository contracts.

    This parser is intentionally limited to deterministic structural checks for
    repository YAML files. It accepts mappings, list items, inline scalars, and
    inline lists/maps used by the generated contracts.
    """

    stack: list[int] = [-1]
    saw_content = False
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if "\t" in raw_line:
            raise ValueError(f"line {line_number}: tabs are not allowed")
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if indent % 2:
            raise ValueError(f"line {line_number}: indentation must use two-space levels")
        content = raw_line.strip()
        while stack and indent <= stack[-1]:
            stack.pop()
        if content.startswith("- "):
            item = content[2:].strip()
            if not item:
                raise ValueError(f"line {line_number}: list item must not be empty")
            if ":" in item:
                key, value = item.split(":", 1)
                _validate_yaml_key_value(line_number, key, value)
            saw_content = True
            stack.append(indent)
            continue
        if ":" not in content:
            raise ValueError(f"line {line_number}: mapping entry must contain ':'")
        key, value = content.split(":", 1)
        _validate_yaml_key_value(line_number, key, value)
        saw_content = True
        stack.append(indent)
    if not saw_content:
        raise ValueError("YAML document is empty")
    return {}


def _validate_yaml_key_value(line_number: int, key: str, value: str) -> None:
    if not key.strip():
        raise ValueError(f"line {line_number}: mapping key must not be empty")
    stripped_value = value.strip()
    if stripped_value.count("[") != stripped_value.count("]"):
        raise ValueError(f"line {line_number}: inline list brackets are unbalanced")
    if stripped_value.count("{") != stripped_value.count("}"):
        raise ValueError(f"line {line_number}: inline map braces are unbalanced")


def _check_database_schema(path: Path, root: Path) -> ValidationCheck:
    if not path.is_file():
        return _fail("database_schema", path, root, "database schema is missing")
    text = path.read_text(encoding="utf-8")
    if "CREATE TABLE" not in text:
        return _fail("database_schema", path, root, "database schema has no CREATE TABLE statements")
    return _pass("database_schema", path, root, "database schema is readable")


def _check_protobuf(path: Path, root: Path, require_optional_tools: bool) -> ValidationCheck:
    if not path.is_file():
        return _fail("protobuf", path, root, "protobuf artifact is missing")
    text = path.read_text(encoding="utf-8")
    required_markers = ("syntax = \"proto3\";", "package echoauth.v1;")
    missing = [marker for marker in required_markers if marker not in text]
    if missing:
        return _fail("protobuf", path, root, f"missing markers: {', '.join(missing)}")
    message = "protobuf markers present; compiler syntax check not configured"
    if require_optional_tools:
        return _fail("protobuf", path, root, "protobuf compiler unavailable")
    return _skip("protobuf", path, root, message)
