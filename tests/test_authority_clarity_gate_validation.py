"""Authority Clarity Gate validator-only tests."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from echoauth.contracts.authority_clarity_gate_validation import (
    load_authority_clarity_gate_schema,
    validate_authority_clarity_gate_file,
    validate_authority_clarity_gate_record,
)


NON_AUTHORITY_SOURCES = [
    "slack_message",
    "google_drive_file",
    "google_calendar_event",
    "github_notification",
    "codex_message",
    "documentation_only_file",
    "planning_only_file",
    "monitoring_output",
    "notification",
    "file_preview",
]

FORBIDDEN_OUTCOMES = [
    "ignore_and_proceed",
    "click_through_approval",
    "approval_by_notification",
    "approval_by_slack_message",
    "approval_by_google_drive_file",
    "approval_by_calendar_event",
    "approval_by_github_notification",
    "approval_by_codex_message",
    "school_or_clinic_final_authority",
    "caregiver_delegate_scope_expansion_without_parent_or_caregiver_anchor",
    "documentation_only_runtime_authority",
    "monitoring_output_as_authority",
    "silent_fallback_to_ALLOW",
]

NON_IMPLEMENTATION_STATUS = {
    "schema_only": True,
    "implements_validator": False,
    "modifies_ci": False,
    "creates_runtime_behavior": False,
    "creates_enforcement_behavior": False,
    "creates_approval_authority": False,
    "resolves_blockers": False,
    "mutates_registers": False,
    "affects_event_bus_behavior": False,
    "affects_broker_or_trading_paths": False,
    "creates_service": False,
    "creates_agent": False,
    "creates_autonomous_action": False,
    "creates_click_through_override": False,
    "grants_command_execution": False,
}


def _valid_record() -> dict[str, object]:
    return {
        "schema_version": "0.1.0-draft",
        "gate_name": "authority_clarity_gate",
        "gate_state": "HOLD",
        "actor": {
            "role": "parent_caregiver_anchor",
            "actor_reference": "actor-1",
        },
        "authority_source": "parent_caregiver_anchor",
        "delegated_scope": {
            "terms": ["none"],
            "scope_reference": "scope-1",
        },
        "requested_action": {
            "action": "review_candidate",
            "resource_reference": "resource-1",
            "lifecycle_state": "authority_clarity_gate_candidate",
        },
        "evidence": {
            "records": [],
            "evidence_only_phase": True,
        },
        "conflict_status": "none_detected",
        "freshness_status": "current",
        "resolution_path": {
            "selected_path": "none_required",
        },
        "monitoring_observation": {
            "observation_reference": "observation-1",
            "advisory_only": True,
            "creates_authority": False,
            "creates_execution_permission": False,
        },
        "source_of_truth": {
            "code_and_documentation_state": "github_repo",
            "governance_rules": "governance_documents",
            "coordination_only": [
                "slack",
                "google_drive",
                "google_calendar",
                "github_notification",
                "codex_message",
            ],
        },
        "non_authority_sources": list(NON_AUTHORITY_SOURCES),
        "forbidden_outcomes": list(FORBIDDEN_OUTCOMES),
        "non_implementation_status": dict(NON_IMPLEMENTATION_STATUS),
    }


class AuthorityClarityGateValidationTests(unittest.TestCase):
    def test_valid_record_passes(self) -> None:
        report = validate_authority_clarity_gate_record(_valid_record())

        self.assertTrue(report.passed, report.issues)
        self.assertTrue(report.non_authoritative)

    def test_missing_required_field_fails(self) -> None:
        record = _valid_record()
        del record["gate_state"]

        report = validate_authority_clarity_gate_record(record)

        self.assertFalse(report.passed)
        self.assertTrue(
            any(
                issue.location == "$.gate_state"
                and "required field is missing" in issue.message
                for issue in report.issues
            ),
            report.issues,
        )

    def test_wrong_type_fails(self) -> None:
        record = _valid_record()
        record["actor"] = "parent_caregiver_anchor"

        report = validate_authority_clarity_gate_record(record)

        self.assertFalse(report.passed)
        self.assertTrue(
            any(issue.location == "$.actor" and "expected object" in issue.message for issue in report.issues),
            report.issues,
        )

    def test_schema_load_is_read_only(self) -> None:
        schema_path = Path("schemas/authority-clarity-gate.schema.json")
        before = schema_path.read_text(encoding="utf-8")

        schema = load_authority_clarity_gate_schema()

        self.assertEqual(schema["title"], "Authority Clarity Gate Schema-Only Draft")
        self.assertEqual(schema["properties"]["schema_version"]["const"], "0.1.0-draft")
        self.assertIn("non_implementation_status", schema["required"])
        self.assertEqual(schema_path.read_text(encoding="utf-8"), before)

    def test_file_validation_reports_candidate_path(self) -> None:
        with TemporaryDirectory() as tmp:
            candidate = Path(tmp) / "candidate.json"
            candidate.write_text(json.dumps(_valid_record()), encoding="utf-8")

            report = validate_authority_clarity_gate_file(candidate)

        self.assertTrue(report.passed, report.issues)
        self.assertTrue(report.non_authoritative)
        self.assertEqual(report.candidate_path, candidate.as_posix())

    def test_file_validation_missing_file_fails(self) -> None:
        with TemporaryDirectory() as tmp:
            candidate = Path(tmp) / "missing.json"
            report = validate_authority_clarity_gate_file(candidate)

        self.assertFalse(report.passed)
        self.assertTrue(
            any(issue.location == "$" and "candidate file is missing" in issue.message for issue in report.issues),
            report.issues,
        )

    def test_non_authority_boundary(self) -> None:
        report = validate_authority_clarity_gate_record(_valid_record())

        self.assertTrue(report.passed, report.issues)
        self.assertTrue(report.non_authoritative)
        self.assertFalse(hasattr(report, "approval_authority"))
        self.assertFalse(hasattr(report, "runtime_behavior"))
        self.assertFalse(hasattr(report, "enforcement_behavior"))
        self.assertFalse(hasattr(report, "event_bus_behavior"))


if __name__ == "__main__":
    unittest.main()
