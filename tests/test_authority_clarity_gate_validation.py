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

    def test_required_top_level_fields_fail(self) -> None:
        required_fields = [
            "schema_version",
            "gate_name",
            "actor",
            "authority_source",
            "delegated_scope",
            "requested_action",
            "evidence",
            "conflict_status",
            "freshness_status",
            "resolution_path",
            "monitoring_observation",
            "source_of_truth",
            "non_authority_sources",
            "forbidden_outcomes",
            "non_implementation_status",
        ]

        for field in required_fields:
            with self.subTest(field=field):
                record = _valid_record()
                del record[field]

                report = validate_authority_clarity_gate_record(record)

                self.assertFalse(report.passed)
                self.assertTrue(
                    any(
                        issue.location == f"$.{field}"
                        and "required field is missing" in issue.message
                        for issue in report.issues
                    ),
                    report.issues,
                )
                self.assertTrue(report.non_authoritative)

    def test_wrong_type_fails(self) -> None:
        record = _valid_record()
        record["actor"] = "parent_caregiver_anchor"

        report = validate_authority_clarity_gate_record(record)

        self.assertFalse(report.passed)
        self.assertTrue(
            any(issue.location == "$.actor" and "expected object" in issue.message for issue in report.issues),
            report.issues,
        )

    def test_invalid_gate_state_enum_values_fail(self) -> None:
        for gate_state in ("", "ALLOW", "APPROVED"):
            with self.subTest(gate_state=gate_state):
                record = _valid_record()
                record["gate_state"] = gate_state

                report = validate_authority_clarity_gate_record(record)

                self.assertFalse(report.passed)
                self.assertTrue(
                    any(
                        issue.location == "$.gate_state"
                        and "value is not allowed" in issue.message
                        for issue in report.issues
                    ),
                    report.issues,
                )
                self.assertTrue(report.non_authoritative)

    def test_declared_hold_refuse_escalate_gate_states_pass(self) -> None:
        for gate_state in ("HOLD", "REFUSE", "ESCALATE"):
            with self.subTest(gate_state=gate_state):
                record = _valid_record()
                record["gate_state"] = gate_state

                report = validate_authority_clarity_gate_record(record)

                self.assertTrue(report.passed, report.issues)
                self.assertTrue(report.non_authoritative)

    def test_authority_source_unresolved_states_pass(self) -> None:
        for authority_source in ("missing", "stale", "conflicting", "unauthorized", "unresolved"):
            with self.subTest(authority_source=authority_source):
                record = _valid_record()
                record["authority_source"] = authority_source

                report = validate_authority_clarity_gate_record(record)

                self.assertTrue(report.passed, report.issues)
                self.assertTrue(report.non_authoritative)

    def test_invalid_authority_source_values_fail(self) -> None:
        for authority_source in ("", "slack_message", "approval_by_notification"):
            with self.subTest(authority_source=authority_source):
                record = _valid_record()
                record["authority_source"] = authority_source

                report = validate_authority_clarity_gate_record(record)

                self.assertFalse(report.passed)
                self.assertTrue(
                    any(
                        issue.location == "$.authority_source"
                        and "value is not allowed" in issue.message
                        for issue in report.issues
                    ),
                    report.issues,
                )
                self.assertTrue(report.non_authoritative)

    def test_existing_conflict_status_values_pass(self) -> None:
        conflict_statuses = [
            "none_detected",
            "actor_conflict",
            "authority_source_conflict",
            "delegated_scope_conflict",
            "evidence_conflict",
            "lifecycle_conflict",
            "unresolved_conflict",
            "unknown",
        ]

        for conflict_status in conflict_statuses:
            with self.subTest(conflict_status=conflict_status):
                record = _valid_record()
                record["conflict_status"] = conflict_status

                report = validate_authority_clarity_gate_record(record)

                self.assertTrue(report.passed, report.issues)
                self.assertTrue(report.non_authoritative)

    def test_existing_actor_roles_and_delegation_scope_terms_pass(self) -> None:
        actor_roles = [
            "child",
            "parent_caregiver_anchor",
            "caregiver_delegate",
            "school_actor",
            "clinical_actor",
            "reviewer_auditor",
            "system_observer",
            "monitoring_node",
        ]
        delegation_scope_terms = [
            "none",
            "task_scoped",
            "time_limited",
            "context_limited",
            "expired",
            "exceeded",
            "disputed",
            "unknown",
        ]

        for actor_role in actor_roles:
            with self.subTest(actor_role=actor_role):
                record = _valid_record()
                record["actor"] = {"role": actor_role, "actor_reference": "actor-1"}

                report = validate_authority_clarity_gate_record(record)

                self.assertTrue(report.passed, report.issues)
                self.assertTrue(report.non_authoritative)

        for delegation_scope_term in delegation_scope_terms:
            with self.subTest(delegation_scope_term=delegation_scope_term):
                record = _valid_record()
                record["delegated_scope"] = {
                    "terms": [delegation_scope_term],
                    "scope_reference": "scope-1",
                }

                report = validate_authority_clarity_gate_record(record)

                self.assertTrue(report.passed, report.issues)
                self.assertTrue(report.non_authoritative)

    def test_invalid_actor_role_and_delegation_scope_term_fail(self) -> None:
        record = _valid_record()
        record["actor"] = {"role": "guardian", "actor_reference": "actor-1"}

        report = validate_authority_clarity_gate_record(record)

        self.assertFalse(report.passed)
        self.assertTrue(
            any(issue.location == "$.actor.role" and "value is not allowed" in issue.message for issue in report.issues),
            report.issues,
        )
        self.assertTrue(report.non_authoritative)

        record = _valid_record()
        record["delegated_scope"] = {
            "terms": ["none", "unsupported_scope"],
            "scope_reference": "scope-1",
        }

        report = validate_authority_clarity_gate_record(record)

        self.assertFalse(report.passed)
        self.assertTrue(
            any(
                issue.location == "$.delegated_scope.terms[1]"
                and "value is not allowed" in issue.message
                for issue in report.issues
            ),
            report.issues,
        )
        self.assertTrue(report.non_authoritative)

    def test_schema_load_is_read_only(self) -> None:
        schema_path = Path("schemas/authority-clarity-gate.schema.json")
        before = schema_path.read_text(encoding="utf-8")

        schema = load_authority_clarity_gate_schema()

        self.assertEqual(schema["title"], "Authority Clarity Gate Schema-Only Draft")
        self.assertEqual(schema["properties"]["schema_version"]["const"], "0.1.0-draft")
        self.assertIn("non_implementation_status", schema["required"])
        self.assertEqual(schema_path.read_text(encoding="utf-8"), before)

    def test_non_authority_source_containment_is_required(self) -> None:
        record = _valid_record()
        record["non_authority_sources"] = [
            source for source in NON_AUTHORITY_SOURCES if source != "slack_message"
        ]

        report = validate_authority_clarity_gate_record(record)

        self.assertFalse(report.passed)
        self.assertTrue(
            any(
                issue.location == "$.non_authority_sources"
                and "array does not contain required value 'slack_message'" in issue.message
                for issue in report.issues
            ),
            report.issues,
        )
        self.assertTrue(report.non_authoritative)

    def test_forbidden_outcome_containment_is_required(self) -> None:
        record = _valid_record()
        record["forbidden_outcomes"] = [
            outcome for outcome in FORBIDDEN_OUTCOMES if outcome != "click_through_approval"
        ]

        report = validate_authority_clarity_gate_record(record)

        self.assertFalse(report.passed)
        self.assertTrue(
            any(
                issue.location == "$.forbidden_outcomes"
                and "array does not contain required value 'click_through_approval'" in issue.message
                for issue in report.issues
            ),
            report.issues,
        )
        self.assertTrue(report.non_authoritative)

    def test_non_implementation_flags_must_keep_required_constants(self) -> None:
        record = _valid_record()
        record["non_implementation_status"] = {
            **NON_IMPLEMENTATION_STATUS,
            "creates_runtime_behavior": True,
        }

        report = validate_authority_clarity_gate_record(record)

        self.assertFalse(report.passed)
        self.assertTrue(
            any(
                issue.location == "$.non_implementation_status.creates_runtime_behavior"
                and "expected constant False" in issue.message
                for issue in report.issues
            ),
            report.issues,
        )
        self.assertTrue(report.non_authoritative)

        record = _valid_record()
        status = dict(NON_IMPLEMENTATION_STATUS)
        del status["grants_command_execution"]
        record["non_implementation_status"] = status

        report = validate_authority_clarity_gate_record(record)

        self.assertFalse(report.passed)
        self.assertTrue(
            any(
                issue.location == "$.non_implementation_status.grants_command_execution"
                and "required field is missing" in issue.message
                for issue in report.issues
            ),
            report.issues,
        )
        self.assertTrue(report.non_authoritative)

    def test_additional_properties_report_issue_paths(self) -> None:
        record = _valid_record()
        record["approval_authority"] = True

        report = validate_authority_clarity_gate_record(record)

        self.assertFalse(report.passed)
        self.assertTrue(
            any(
                issue.location == "$.approval_authority"
                and "additional property is not allowed" in issue.message
                for issue in report.issues
            ),
            report.issues,
        )
        self.assertTrue(report.non_authoritative)

    def test_evidence_record_with_existing_schema_fields_passes(self) -> None:
        record = _valid_record()
        record["evidence"] = {
            "records": [
                {
                    "evidence_id": "evidence-1",
                    "evidence_type": "audit_reference",
                    "authority_source": "missing",
                    "actor_role": "caregiver_delegate",
                    "subject_role": "child",
                    "requested_action": "review_candidate",
                    "authority_scope": "task-scoped-review",
                    "delegated_scope": ["unknown"],
                    "lifecycle_state": "pending",
                    "conflict_status": "unresolved_conflict",
                    "freshness_status": "unknown",
                    "timestamp": "2026-06-23T00:00:00Z",
                    "issuer": "issuer-1",
                    "reviewer": "reviewer-1",
                    "trace_reference": "trace-1",
                }
            ],
            "evidence_only_phase": True,
        }

        report = validate_authority_clarity_gate_record(record)

        self.assertTrue(report.passed, report.issues)
        self.assertTrue(report.non_authoritative)

    def test_evidence_record_invalid_timestamp_reports_issue_path(self) -> None:
        record = _valid_record()
        record["evidence"] = {
            "records": [
                {
                    "evidence_id": "evidence-1",
                    "timestamp": "not-a-date",
                    "trace_reference": "trace-1",
                }
            ],
            "evidence_only_phase": True,
        }

        report = validate_authority_clarity_gate_record(record)

        self.assertFalse(report.passed)
        self.assertTrue(
            any(
                issue.location == "$.evidence.records[0].timestamp"
                and "expected date-time string" in issue.message
                for issue in report.issues
            ),
            report.issues,
        )
        self.assertTrue(report.non_authoritative)

    def test_resolution_explanation_packet_with_existing_fields_passes(self) -> None:
        record = _valid_record()
        record["gate_state"] = "ESCALATE"
        record["resolution_path"] = {
            "selected_path": "request_manual_review",
            "explanation_packet": {
                "gate_state": "ESCALATE",
                "reason_code": "unresolved_conflict",
                "conflicting_primitive": "authority_source",
                "freshness_status": "unknown",
                "conflict_status": "authority_source_conflict",
                "actor_role": "reviewer_auditor",
                "authority_source": "conflicting",
                "delegated_scope": ["disputed"],
                "requested_action": "review_candidate",
                "lifecycle_state": "pending",
                "evidence_reference": "evidence-1",
                "trace_reference": "trace-1",
                "timestamp": "2026-06-23T00:00:00Z",
            },
        }

        report = validate_authority_clarity_gate_record(record)

        self.assertTrue(report.passed, report.issues)
        self.assertTrue(report.non_authoritative)

    def test_monitoring_observation_boundary_constants_fail_when_true(self) -> None:
        record = _valid_record()
        record["monitoring_observation"] = {
            "observation_reference": "observation-1",
            "advisory_only": True,
            "creates_authority": True,
            "creates_execution_permission": False,
        }

        report = validate_authority_clarity_gate_record(record)

        self.assertFalse(report.passed)
        self.assertTrue(
            any(
                issue.location == "$.monitoring_observation.creates_authority"
                and "expected constant False" in issue.message
                for issue in report.issues
            ),
            report.issues,
        )
        self.assertTrue(report.non_authoritative)

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
