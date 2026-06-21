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


def _replace_in_section(
    text: str,
    start_heading: str,
    end_heading: str,
    old: str,
    new: str,
    *,
    count: int = 1,
) -> str:
    start = text.index(start_heading)
    end = text.index(end_heading, start + len(start_heading))
    section = text[start:end]
    replaced = section.replace(old, new, count)
    if replaced == section:
        raise AssertionError(f"fixture value not found: {old}")
    return text[:start] + replaced + text[end:]


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

    def test_missing_approval_record_fails_closed(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            (root / "contracts/event-bus-v2-approval-record.md").unlink()
            report = validate_event_bus_v2_contracts(root)

        self.assertIn("missing_artifact", _codes(report))

    def test_missing_or_malformed_authority_intake_schema_fails_closed(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            schema_path = root / "schemas/event-bus-v2-authority-intake.schema.json"
            schema_path.unlink()
            missing_report = validate_event_bus_v2_contracts(root)
            schema_path.write_text("{invalid", encoding="utf-8")
            malformed_report = validate_event_bus_v2_contracts(root)

        self.assertIn("missing_artifact", _codes(missing_report))
        self.assertIn("invalid_json", _codes(malformed_report))

    def test_intake_schema_conformance_cannot_grant_effects(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            schema_path = root / "schemas/event-bus-v2-authority-intake.schema.json"
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            for field in (
                "identity_established",
                "authority_established",
                "approval_granted",
                "blocker_resolved",
                "contains_credentials",
                "contains_secrets",
            ):
                schema["properties"][field]["const"] = True
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            report = validate_event_bus_v2_contracts(root)

        self.assertIn("intake_schema_effect_mismatch", _codes(report))

    def test_intake_contract_remains_unsubmitted_unverified_and_non_runtime(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            contract_path = root / "contracts/event-bus-v2.yaml"
            text = contract_path.read_text(encoding="utf-8")
            text = text.replace("  current_status: NOT_SUBMITTED", "  current_status: SUBMITTED_UNVERIFIED", 1)
            text = text.replace("  establishes_authority: false", "  establishes_authority: true", 1)
            text = text.replace("  grants_approval: false", "  grants_approval: true", 1)
            text = text.replace("  runtime_effect: none", "  runtime_effect: delivery", 1)
            contract_path.write_text(text, encoding="utf-8")
            report = validate_event_bus_v2_contracts(root)

        self.assertIn("intake_contract_boundary_mismatch", _codes(report))

    def test_missing_or_malformed_authority_intake_submission_schema_fails_closed(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            schema_path = root / "schemas/event-bus-v2-authority-intake-submission.schema.json"
            schema_path.unlink()
            missing_report = validate_event_bus_v2_contracts(root)
            schema_path.write_text("{invalid", encoding="utf-8")
            malformed_report = validate_event_bus_v2_contracts(root)

        self.assertIn("missing_artifact", _codes(missing_report))
        self.assertIn("invalid_json", _codes(malformed_report))

    def test_submission_schema_cannot_grant_effects_or_collect_personal_data(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            schema_path = root / "schemas/event-bus-v2-authority-intake-submission.schema.json"
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            for field in (
                "identity_established",
                "authority_established",
                "party_assigned",
                "approval_granted",
                "blocker_resolved",
                "contains_credentials",
                "contains_secrets",
                "contains_unnecessary_personal_data",
            ):
                schema["properties"][field]["const"] = True
            schema["properties"]["personal_name"] = {"type": "string"}
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            report = validate_event_bus_v2_contracts(root)

        codes = _codes(report)
        self.assertIn("submission_schema_effect_mismatch", codes)
        self.assertIn("submission_schema_field_mismatch", codes)

    def test_submission_contract_cannot_infer_authority_assign_or_resolve(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            contract_path = root / "contracts/event-bus-v2.yaml"
            text = contract_path.read_text(encoding="utf-8")
            section_start = text.index("authority_intake_submission:")
            prefix, section = text[:section_start], text[section_start:]
            for old, new in (
                ("  inferred_authority_permitted: false", "  inferred_authority_permitted: true"),
                ("  assigns_party: false", "  assigns_party: true"),
                ("  grants_approval: false", "  grants_approval: true"),
                ("  resolves_blocker: false", "  resolves_blocker: true"),
            ):
                section = section.replace(old, new, 1)
            contract_path.write_text(prefix + section, encoding="utf-8")
            report = validate_event_bus_v2_contracts(root)

        self.assertIn("submission_contract_boundary_mismatch", _codes(report))

    def test_submission_protocol_does_not_change_current_intake_register(self) -> None:
        report = validate_event_bus_v2_contracts(_ROOT)
        approval = (_ROOT / "contracts/event-bus-v2-approval-record.md").read_text(encoding="utf-8")

        self.assertTrue(report.passed, report.failures)
        current_register = approval.split("## Current Authority Intake Register", 1)[1].split(
            "## Approval Readiness", 1
        )[0]
        self.assertEqual(current_register.count("`NOT_SUBMITTED` | `UNRESOLVED`"), 8)
        self.assertNotIn("`SUBMITTED_UNVERIFIED` | `UNRESOLVED`", current_register)

    def test_missing_or_malformed_authority_intake_verification_schema_fails_closed(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            schema_path = root / "schemas/event-bus-v2-authority-intake-verification.schema.json"
            schema_path.unlink()
            missing_report = validate_event_bus_v2_contracts(root)
            schema_path.write_text("{invalid", encoding="utf-8")
            malformed_report = validate_event_bus_v2_contracts(root)

        self.assertIn("missing_artifact", _codes(missing_report))
        self.assertIn("invalid_json", _codes(malformed_report))

    def test_verification_schema_requires_authority_evidence_provenance_and_safe_effects(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            schema_path = root / "schemas/event-bus-v2-authority-intake-verification.schema.json"
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            schema["required"].remove("verifier_authority_evidence_reference")
            schema["properties"]["verified_evidence_references"]["minItems"] = 0
            schema["properties"]["evidence_provenance"]["required"].remove("source_reference")
            schema["properties"]["self_verification_check"]["properties"]["outcome"]["const"] = "SAME"
            for field in (
                "self_verification_detected",
                "inferred_authority",
                "contains_credentials",
                "contains_secrets",
                "contains_excess_personal_data",
                "identity_established",
                "authority_assigned",
                "approval_granted",
                "blocker_resolved",
                "execution_authorized",
            ):
                schema["properties"][field]["const"] = True
            schema["properties"]["personal_name"] = {"type": "string"}
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            report = validate_event_bus_v2_contracts(root)

        codes = _codes(report)
        self.assertIn("verification_schema_required_fields", codes)
        self.assertIn("verification_evidence_reference_mismatch", codes)
        self.assertIn("verification_provenance_mismatch", codes)
        self.assertIn("verification_self_check_mismatch", codes)
        self.assertIn("verification_schema_effect_mismatch", codes)
        self.assertIn("verification_schema_field_mismatch", codes)

    def test_verification_schema_preserves_unverified_state_on_non_verified_outcomes(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            schema_path = root / "schemas/event-bus-v2-authority-intake-verification.schema.json"
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            schema["properties"]["verification_outcome"]["enum"].remove("UNVERIFIABLE")
            schema["allOf"][0]["else"]["properties"]["resulting_intake_status"]["const"] = (
                "VERIFIED_PENDING_GOVERNANCE"
            )
            schema["allOf"][0]["then"]["properties"]["scope_alignment"]["properties"]["outcome"][
                "const"
            ] = "UNVERIFIED"
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            report = validate_event_bus_v2_contracts(root)

        codes = _codes(report)
        self.assertIn("verification_outcome_mismatch", codes)
        self.assertIn("verification_transition_mismatch", codes)

    def test_verification_contract_cannot_assign_approve_resolve_or_mutate_register(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            contract_path = root / "contracts/event-bus-v2.yaml"
            text = contract_path.read_text(encoding="utf-8")
            section_start = text.index("authority_intake_verification:")
            prefix, section = text[:section_start], text[section_start:]
            for old, new in (
                ("  self_verification_permitted: false", "  self_verification_permitted: true"),
                ("  inferred_authority_permitted: false", "  inferred_authority_permitted: true"),
                ("  assigns_authority: false", "  assigns_authority: true"),
                ("  grants_approval: false", "  grants_approval: true"),
                ("  resolves_blocker: false", "  resolves_blocker: true"),
                ("  mutates_current_register: false", "  mutates_current_register: true"),
            ):
                section = section.replace(old, new, 1)
            contract_path.write_text(prefix + section, encoding="utf-8")
            report = validate_event_bus_v2_contracts(root)

        self.assertIn("verification_contract_boundary_mismatch", _codes(report))

    def test_missing_or_duplicate_approval_intake_entry_fails_closed(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            approval_path = root / "contracts/event-bus-v2-approval-record.md"
            text = approval_path.read_text(encoding="utf-8")
            row = "| EVT2-B08 | Causation integrity contract owner | `UNASSIGNED` | `ABSENT` | `NOT_SUBMITTED` | `UNRESOLVED` |\n"
            missing_text = _replace_in_section(
                text,
                "## Current Authority Intake Register",
                "## Approval Readiness",
                row,
                "",
            )
            approval_path.write_text(missing_text, encoding="utf-8")
            missing_report = validate_event_bus_v2_contracts(root)
            approval_path.write_text(
                _replace_in_section(
                    text,
                    "## Current Authority Intake Register",
                    "## Approval Readiness",
                    row,
                    row + row,
                ),
                encoding="utf-8",
            )
            duplicate_report = validate_event_bus_v2_contracts(root)

        self.assertIn("governance_blocker_set_mismatch", _codes(missing_report))
        self.assertIn("governance_blocker_set_mismatch", _codes(duplicate_report))

    def test_approval_record_intake_drift_fails_closed(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            approval_path = root / "contracts/event-bus-v2-approval-record.md"
            text = approval_path.read_text(encoding="utf-8")
            for old, new in (
                ("`UNASSIGNED`", "`party-1`"),
                ("`ABSENT`", "`authority-1`"),
                ("`NOT_SUBMITTED`", "`SUBMITTED_UNVERIFIED`"),
                ("`UNRESOLVED`", "`RESOLVED`"),
            ):
                text = _replace_in_section(
                    text,
                    "## Current Authority Intake Register",
                    "## Approval Readiness",
                    old,
                    new,
                )
            approval_path.write_text(text, encoding="utf-8")
            report = validate_event_bus_v2_contracts(root)

        codes = _codes(report)
        self.assertIn("approval_party_assigned", codes)
        self.assertIn("approval_authority_present", codes)
        self.assertIn("approval_intake_submitted", codes)
        self.assertIn("approval_blocker_resolved", codes)

    def test_empty_blocker_matrix_fails_conformance(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            (root / "contracts/event-bus-v2-blocker-matrix.md").write_text(
                "",
                encoding="utf-8",
            )
            report = validate_event_bus_v2_contracts(root)

        self.assertIn("empty_blocker_matrix", _codes(report))

    def test_blocker_matrix_requires_all_fields_and_unresolved_boundaries(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            _copy_contract_tree(root)
            matrix_path = root / "contracts/event-bus-v2-blocker-matrix.md"
            matrix_path.write_text(
                matrix_path.read_text(encoding="utf-8")
                .replace("- Required evidence:", "- Removed evidence:", 1)
                .replace("- Status: `UNRESOLVED`", "- Status: `RESOLVED`", 1),
                encoding="utf-8",
            )
            report = validate_event_bus_v2_contracts(root)

        self.assertIn("missing_matrix_field", _codes(report))
        self.assertIn("matrix_blocker_resolved", _codes(report))

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
