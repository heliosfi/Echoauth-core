"""Sprint 3B event-bus v2 contract conformance tests."""

from __future__ import annotations

import json
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from echoauth.contracts.event_bus_v2_validation import (
    EventBusV2ValidationReport,
    validate_event_bus_v2_contracts,
)


_ROOT = Path(__file__).resolve().parents[1]


def _copy_contract_tree(destination: Path) -> None:
    for directory in ("contracts", "events", "schemas", "specs"):
        shutil.copytree(_ROOT / directory, destination / directory)


def _codes(report: EventBusV2ValidationReport) -> set[str]:
    return {failure.code for failure in report.failures}


class EventBusV2ContractValidationTests(unittest.TestCase):
    def test_repository_v2_contracts_conform_and_remain_on_hold(self) -> None:
        report = validate_event_bus_v2_contracts(_ROOT)

        self.assertTrue(report.passed, report.failures)

    def test_missing_required_artifact_fails_closed(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            (root / "events/event-envelope-v2.schema.json").unlink()
            report = validate_event_bus_v2_contracts(root)

        self.assertIn("missing_artifact", _codes(report))

    def test_malformed_yaml_and_json_fail_deterministically(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            (root / "contracts/event-bus-v2.yaml").write_text(
                "version:\n   invalid: indentation\n",
                encoding="utf-8",
            )
            yaml_report = validate_event_bus_v2_contracts(root)
            (root / "contracts/event-bus-v2.yaml").write_text(
                (_ROOT / "contracts/event-bus-v2.yaml").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (root / "schemas/event-bus-runtime-v2.schema.json").write_text(
                "{invalid",
                encoding="utf-8",
            )
            json_report = validate_event_bus_v2_contracts(root)

        self.assertIn("invalid_yaml", _codes(yaml_report))
        self.assertIn("invalid_json", _codes(json_report))

    def test_schema_draft_and_local_reference_failures_are_rejected(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            envelope_path = root / "events/event-envelope-v2.schema.json"
            envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
            envelope["$schema"] = "https://json-schema.org/draft/2019-09/schema"
            envelope["properties"]["event_id"]["$ref"] = "missing.schema.json#/$defs/Id"
            envelope_path.write_text(json.dumps(envelope), encoding="utf-8")
            report = validate_event_bus_v2_contracts(root)

        self.assertIn("schema_draft_mismatch", _codes(report))
        self.assertIn("unresolved_reference", _codes(report))

    def test_schema_identity_and_payload_schema_id_mismatches_fail(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            envelope_path = root / "events/event-envelope-v2.schema.json"
            envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
            envelope["$id"] = "https://echoauth.local/events/wrong.schema.json"
            envelope_path.write_text(json.dumps(envelope), encoding="utf-8")
            catalog_path = root / "events/event-catalog-v2.yaml"
            catalog_text = catalog_path.read_text(encoding="utf-8").replace(
                "https://echoauth.local/schemas/audit-record.schema.json",
                "https://echoauth.local/schemas/wrong.schema.json",
                1,
            )
            catalog_path.write_text(catalog_text, encoding="utf-8")
            report = validate_event_bus_v2_contracts(root)

        self.assertIn("schema_identity_mismatch", _codes(report))
        self.assertIn("payload_schema_id_mismatch", _codes(report))

    def test_duplicate_or_unordered_catalog_entries_fail(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            catalog_path = root / "events/event-catalog-v2.yaml"
            text = catalog_path.read_text(encoding="utf-8")
            text = text.replace("event_type: audit.record", "event_type: runtime.halted", 1)
            catalog_path.write_text(text, encoding="utf-8")
            report = validate_event_bus_v2_contracts(root)

        self.assertIn("duplicate_event_type", _codes(report))
        self.assertIn("nondeterministic_catalog_order", _codes(report))

    def test_incomplete_classification_and_vocabulary_mismatch_fail(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            catalog_path = root / "events/event-catalog-v2.yaml"
            catalog_path.write_text(
                catalog_path.read_text(encoding="utf-8").replace(
                    "confidentiality_class: restricted",
                    "confidentiality_class: unknown",
                    1,
                ),
                encoding="utf-8",
            )
            contract_path = root / "contracts/event-bus-v2.yaml"
            contract_path.write_text(
                contract_path.read_text(encoding="utf-8").replace(
                    "    - sensitive\n    - restricted\n",
                    "    - restricted\n    - sensitive\n",
                    1,
                ),
                encoding="utf-8",
            )
            report = validate_event_bus_v2_contracts(root)

        self.assertIn("incomplete_catalog_classification", _codes(report))
        self.assertIn("vocabulary_mismatch", _codes(report))

    def test_approval_or_hold_changes_fail_closed(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            contract_path = root / "contracts/event-bus-v2.yaml"
            contract_path.write_text(
                contract_path.read_text(encoding="utf-8")
                .replace("status: hold", "status: active", 1)
                .replace("approved: false", "approved: true", 1)
                .replace(
                    "runtime_implementation_permitted: false",
                    "runtime_implementation_permitted: true",
                    1,
                ),
                encoding="utf-8",
            )
            report = validate_event_bus_v2_contracts(root)

        self.assertIn("hold_not_active", _codes(report))
        self.assertIn("approval_must_be_false", _codes(report))
        self.assertIn("runtime_gate_open", _codes(report))

    def test_all_eight_blockers_must_match_across_artifacts(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            contract_path = root / "contracts/event-bus-v2.yaml"
            contract_path.write_text(
                contract_path.read_text(encoding="utf-8").replace(
                    "  - durable_causation_lookup_and_conflict_authority\n",
                    "",
                    1,
                ),
                encoding="utf-8",
            )
            report = validate_event_bus_v2_contracts(root)

        self.assertIn("approval_blocker_mismatch", _codes(report))

    def test_runtime_recovered_must_remain_catalog_only_and_prohibited(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            catalog_path = root / "events/event-catalog-v2.yaml"
            text = catalog_path.read_text(encoding="utf-8")
            marker = "  - event_type: runtime.recovered\n    lifecycle_state: catalog_only"
            text = text.replace(marker, "  - event_type: runtime.recovered\n    lifecycle_state: active")
            catalog_path.write_text(text, encoding="utf-8")
            report = validate_event_bus_v2_contracts(root)

        self.assertIn("runtime_recovered_not_catalog_only", _codes(report))

    def test_validator_exposes_no_runtime_event_bus_behavior(self) -> None:
        for name in (
            "publish",
            "subscribe",
            "route",
            "deliver",
            "retry",
            "dead_letter",
            "persist",
            "replay",
            "sign",
            "append",
            "execute",
        ):
            self.assertFalse(hasattr(validate_event_bus_v2_contracts, name))


if __name__ == "__main__":
    unittest.main()
