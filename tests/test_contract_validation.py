"""Sprint 1 contract validation tests."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from echoauth.contracts.validation import CheckStatus, validate_contracts


def _write_minimal_contract_tree(root: Path, yaml_text: str = "version: 1\n") -> None:
    (root / "schemas").mkdir()
    (root / "events").mkdir()
    (root / "api").mkdir()
    (root / "contracts" / "protobuf").mkdir(parents=True)
    (root / "database").mkdir()
    (root / "schemas" / "common.schema.json").write_text(json.dumps({}), encoding="utf-8")
    for schema_name in (
        "recovery-request.schema.json",
        "recovery-result.schema.json",
        "recovery-review-protocol.schema.json",
        "governance-runtime-proposal.schema.json",
    ):
        (root / "schemas" / schema_name).write_text(json.dumps({}), encoding="utf-8")
    (root / "events" / "event-envelope.schema.json").write_text(json.dumps({}), encoding="utf-8")
    (root / "api" / "openapi.yaml").write_text(
        "openapi: 3.1.0\npaths: {}\ncomponents: {}\n",
        encoding="utf-8",
    )
    (root / "contracts" / "service-contracts.yaml").write_text(yaml_text, encoding="utf-8")
    (root / "contracts" / "integration-contracts.yaml").write_text(yaml_text, encoding="utf-8")
    (root / "contracts" / "recovery-service.yaml").write_text(yaml_text, encoding="utf-8")
    (root / "events" / "event-catalog.yaml").write_text(yaml_text, encoding="utf-8")
    (root / "contracts" / "protobuf" / "echoauth.proto").write_text(
        'syntax = "proto3";\npackage echoauth.v1;\n',
        encoding="utf-8",
    )
    (root / "database" / "schema.sql").write_text("CREATE TABLE sample (id TEXT);\n", encoding="utf-8")


class ContractValidationTests(unittest.TestCase):
    def test_repository_contracts_validate_without_failures(self) -> None:
        report = validate_contracts()

        self.assertTrue(report.passed, report.failures())
        self.assertTrue(any(check.name == "json_parse" for check in report.checks))
        self.assertTrue(any(check.name == "openapi_structure" for check in report.checks))
        self.assertTrue(any(check.name == "database_schema" for check in report.checks))
        self.assertTrue(any(check.name == "protobuf" for check in report.checks))

    def test_missing_artifacts_fail_deterministically(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = validate_contracts(root)

        self.assertFalse(report.passed)
        self.assertTrue(report.failures())

    def test_invalid_json_fails_deterministically(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_contract_tree(root)
            (root / "schemas" / "bad.schema.json").write_text("{bad", encoding="utf-8")

            report = validate_contracts(root)

        self.assertFalse(report.passed)
        self.assertTrue(any(check.name == "json_parse" and check.status is CheckStatus.FAIL for check in report.checks))

    def test_yaml_parser_available_validates_yaml(self) -> None:
        calls: list[str] = []

        def parser(text: str) -> object:
            calls.append(text)
            return {}

        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_contract_tree(root)
            report = validate_contracts(root, yaml_parser=parser)

        self.assertTrue(report.passed, report.failures())
        self.assertGreaterEqual(len(calls), 5)
        self.assertTrue(any(check.name == "yaml_parse" and check.status is CheckStatus.PASS for check in report.checks))

    def test_yaml_parser_unavailable_fails_clearly(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_contract_tree(root)
            report = validate_contracts(root, yaml_parser=None)

        self.assertFalse(report.passed)
        self.assertTrue(
            any(
                check.name == "yaml_parse"
                and check.status is CheckStatus.FAIL
                and "YAML parser unavailable" in check.message
                for check in report.checks
            )
        )

    def test_invalid_yaml_fails_deterministically(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_minimal_contract_tree(root, yaml_text="version: [1\n")
            report = validate_contracts(root)

        self.assertFalse(report.passed)
        self.assertTrue(any(check.name == "yaml_parse" and check.status is CheckStatus.FAIL for check in report.checks))

    def test_existing_valid_yaml_passes(self) -> None:
        report = validate_contracts()

        self.assertTrue(report.passed, report.failures())
        self.assertTrue(
            any(
                check.path == "contracts/integration-contracts.yaml"
                and check.name == "yaml_parse"
                and check.status is CheckStatus.PASS
                for check in report.checks
            )
        )
        self.assertTrue(
            any(
                check.path == "events/event-catalog.yaml"
                and check.name == "yaml_parse"
                and check.status is CheckStatus.PASS
                for check in report.checks
            )
        )
        self.assertTrue(
            any(
                check.path == "contracts/recovery-service.yaml"
                and check.name == "yaml_parse"
                and check.status is CheckStatus.PASS
                for check in report.checks
            )
        )
        required_schema_paths = {
            "schemas/recovery-request.schema.json",
            "schemas/recovery-result.schema.json",
            "schemas/recovery-review-protocol.schema.json",
            "schemas/governance-runtime-proposal.schema.json",
        }
        passed_required_paths = {
            check.path
            for check in report.checks
            if check.name == "required_path" and check.status is CheckStatus.PASS
        }
        self.assertTrue(required_schema_paths.issubset(passed_required_paths))


if __name__ == "__main__":
    unittest.main()
