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
    "schemas/event-bus-v2-authority-intake.schema.json",
    "schemas/event-bus-v2-authority-intake-submission.schema.json",
    "schemas/event-bus-v2-authority-intake-verification.schema.json",
    "schemas/event-bus-v2-authority-intake-governance-admission.schema.json",
    "schemas/event-bus-v2-authority-intake-governance-review.schema.json",
    "events/event-envelope-v2.schema.json",
    "events/event-catalog-v2.yaml",
    "contracts/event-bus-v2-decision-log.md",
    "contracts/event-bus-v2-approval-record.md",
    "contracts/event-bus-v2-blocker-matrix.md",
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
_BLOCKER_IDS = tuple(f"EVT2-B0{index}" for index in range(1, 9))
_OWNER_ROLES = (
    "Event transport contract owner",
    "Persistence contract owner",
    "Retention and legal-hold contract owner",
    "Cryptographic security contract owner",
    "Data classification contract owner",
    "Subscription governance contract owner",
    "Event audit contract owner",
    "Causation integrity contract owner",
)
_RECOVERED_PROHIBITIONS = (
    "accept",
    "produce",
    "subscribe",
    "publish",
    "replay",
    "emit",
)
_MATRIX_FIELDS = (
    "Status",
    "Owner role placeholder",
    "Accountable party",
    "Authority reference status",
    "Required evidence",
    "Required approval category",
    "Dependent contracts",
    "Dependent runtime capabilities",
    "Upstream dependencies",
    "Downstream dependencies",
    "Resolution criteria",
)
_SPRINT_2J_REVIEW_OUTCOMES = (
    "approved_for_override_review",
    "denied_after_review",
    "returned_for_information",
    "delegated_review_required",
    "guardian_review_required",
    "parent_review_required",
    "clinical_review_required",
    "administrative_review_required",
    "unresolved",
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
    intake_schema = _load_json(
        root_path,
        "schemas/event-bus-v2-authority-intake.schema.json",
        failures,
    )
    submission_schema = _load_json(
        root_path,
        "schemas/event-bus-v2-authority-intake-submission.schema.json",
        failures,
    )
    verification_schema = _load_json(
        root_path,
        "schemas/event-bus-v2-authority-intake-verification.schema.json",
        failures,
    )
    admission_schema = _load_json(
        root_path,
        "schemas/event-bus-v2-authority-intake-governance-admission.schema.json",
        failures,
    )
    governance_review_schema = _load_json(
        root_path,
        "schemas/event-bus-v2-authority-intake-governance-review.schema.json",
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
    assert intake_schema is not None
    assert submission_schema is not None
    assert verification_schema is not None
    assert admission_schema is not None
    assert governance_review_schema is not None
    schemas = (
        runtime_schema,
        envelope_schema,
        intake_schema,
        submission_schema,
        verification_schema,
        admission_schema,
        governance_review_schema,
    )
    _validate_schema_declarations(*schemas, failures)
    _validate_local_references(root_path, *schemas, failures)
    _validate_schema_identity(
        contract,
        catalog,
        envelope_schema,
        intake_schema,
        submission_schema,
        verification_schema,
        admission_schema,
        governance_review_schema,
        failures,
    )
    _validate_catalog(root_path, catalog, runtime_schema, failures)
    _validate_vocabularies(contract, runtime_schema, failures)
    _validate_hold_gate(root_path, contract, catalog, failures)
    _validate_blockers(root_path, contract, catalog, failures)
    _validate_blocker_matrix(root_path, failures)
    _validate_approval_and_intake_records(root_path, failures)
    _validate_authority_intake_contract(contract, intake_schema, failures)
    _validate_authority_intake_submission_contract(contract, submission_schema, failures)
    _validate_authority_intake_verification_contract(contract, verification_schema, failures)
    _validate_authority_intake_governance_admission_contract(
        root_path,
        contract,
        admission_schema,
        failures,
    )
    _validate_authority_intake_governance_review_contract(
        root_path,
        contract,
        governance_review_schema,
        failures,
    )
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
    intake_schema: Mapping[str, Any],
    submission_schema: Mapping[str, Any],
    verification_schema: Mapping[str, Any],
    admission_schema: Mapping[str, Any],
    governance_review_schema: Mapping[str, Any],
    failures: list[EventBusV2ValidationFailure],
) -> None:
    identities: set[str] = set()
    for path, schema in (
        ("schemas/event-bus-runtime-v2.schema.json", runtime_schema),
        ("events/event-envelope-v2.schema.json", envelope_schema),
        ("schemas/event-bus-v2-authority-intake.schema.json", intake_schema),
        ("schemas/event-bus-v2-authority-intake-submission.schema.json", submission_schema),
        ("schemas/event-bus-v2-authority-intake-verification.schema.json", verification_schema),
        ("schemas/event-bus-v2-authority-intake-governance-admission.schema.json", admission_schema),
        ("schemas/event-bus-v2-authority-intake-governance-review.schema.json", governance_review_schema),
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
    intake_schema: Mapping[str, Any],
    submission_schema: Mapping[str, Any],
    verification_schema: Mapping[str, Any],
    admission_schema: Mapping[str, Any],
    governance_review_schema: Mapping[str, Any],
    failures: list[EventBusV2ValidationFailure],
) -> None:
    loaded: dict[Path, Mapping[str, Any]] = {
        (root / "schemas/event-bus-runtime-v2.schema.json").resolve(): runtime_schema,
        (root / "events/event-envelope-v2.schema.json").resolve(): envelope_schema,
        (root / "schemas/event-bus-v2-authority-intake.schema.json").resolve(): intake_schema,
        (root / "schemas/event-bus-v2-authority-intake-submission.schema.json").resolve(): submission_schema,
        (root / "schemas/event-bus-v2-authority-intake-verification.schema.json").resolve(): verification_schema,
        (root / "schemas/event-bus-v2-authority-intake-governance-admission.schema.json").resolve(): admission_schema,
        (root / "schemas/event-bus-v2-authority-intake-governance-review.schema.json").resolve(): governance_review_schema,
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
    visit(root / "schemas/event-bus-v2-authority-intake.schema.json", intake_schema)
    visit(root / "schemas/event-bus-v2-authority-intake-submission.schema.json", submission_schema)
    visit(root / "schemas/event-bus-v2-authority-intake-verification.schema.json", verification_schema)
    visit(root / "schemas/event-bus-v2-authority-intake-governance-admission.schema.json", admission_schema)
    visit(root / "schemas/event-bus-v2-authority-intake-governance-review.schema.json", governance_review_schema)


def _validate_schema_identity(
    contract: Mapping[str, Any],
    catalog: Mapping[str, Any],
    envelope_schema: Mapping[str, Any],
    intake_schema: Mapping[str, Any],
    submission_schema: Mapping[str, Any],
    verification_schema: Mapping[str, Any],
    admission_schema: Mapping[str, Any],
    governance_review_schema: Mapping[str, Any],
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
        ("intake_schema_path", artifacts.get("authority_intake_schema"), "schemas/event-bus-v2-authority-intake.schema.json"),
        (
            "intake_submission_schema_path",
            artifacts.get("authority_intake_submission_schema"),
            "schemas/event-bus-v2-authority-intake-submission.schema.json",
        ),
        (
            "intake_verification_schema_path",
            artifacts.get("authority_intake_verification_schema"),
            "schemas/event-bus-v2-authority-intake-verification.schema.json",
        ),
        (
            "intake_governance_admission_schema_path",
            artifacts.get("authority_intake_governance_admission_schema"),
            "schemas/event-bus-v2-authority-intake-governance-admission.schema.json",
        ),
        (
            "intake_governance_review_schema_path",
            artifacts.get("authority_intake_governance_review_schema"),
            "schemas/event-bus-v2-authority-intake-governance-review.schema.json",
        ),
        ("catalog_envelope", catalog.get("envelope_schema"), "event-envelope-v2.schema.json"),
    )
    for label, actual, required in expected:
        if actual != required:
            _fail(failures, "schema_identity_mismatch", "contracts/event-bus-v2.yaml", label)

    if intake_schema.get("$id") != "https://echoauth.local/schemas/event-bus-v2-authority-intake.schema.json":
        _fail(failures, "schema_identity_mismatch", "schemas/event-bus-v2-authority-intake.schema.json", "$id")
    if submission_schema.get("$id") != "https://echoauth.local/schemas/event-bus-v2-authority-intake-submission.schema.json":
        _fail(
            failures,
            "schema_identity_mismatch",
            "schemas/event-bus-v2-authority-intake-submission.schema.json",
            "$id",
        )
    if verification_schema.get("$id") != "https://echoauth.local/schemas/event-bus-v2-authority-intake-verification.schema.json":
        _fail(
            failures,
            "schema_identity_mismatch",
            "schemas/event-bus-v2-authority-intake-verification.schema.json",
            "$id",
        )
    if admission_schema.get("$id") != "https://echoauth.local/schemas/event-bus-v2-authority-intake-governance-admission.schema.json":
        _fail(
            failures,
            "schema_identity_mismatch",
            "schemas/event-bus-v2-authority-intake-governance-admission.schema.json",
            "$id",
        )
    if governance_review_schema.get("$id") != "https://echoauth.local/schemas/event-bus-v2-authority-intake-governance-review.schema.json":
        _fail(
            failures,
            "schema_identity_mismatch",
            "schemas/event-bus-v2-authority-intake-governance-review.schema.json",
            "$id",
        )


def _validate_authority_intake_contract(
    contract: Mapping[str, Any],
    schema: Mapping[str, Any],
    failures: list[EventBusV2ValidationFailure],
) -> None:
    path = "schemas/event-bus-v2-authority-intake.schema.json"
    properties = _mapping(schema.get("properties"))
    required = schema.get("required")
    expected_required = {
        "intake_schema_version",
        "intake_id",
        "blocker_id",
        "owner_role",
        "intake_status",
        "accountable_party_status",
        "authority_reference_status",
        "contains_credentials",
        "contains_secrets",
        "identity_established",
        "authority_established",
        "approval_granted",
        "blocker_resolved",
    }
    if schema.get("additionalProperties") is not False:
        _fail(failures, "intake_schema_open", path, "additional properties must be prohibited")
    if not _string_sequence(required) or not expected_required.issubset(set(required)):
        _fail(failures, "intake_schema_required_fields", path, "required non-effect fields are missing")
    if _mapping(properties.get("intake_schema_version")).get("const") != "2.0.0":
        _fail(failures, "intake_schema_version_mismatch", path, "intake schema version must be 2.0.0")
    if tuple(_mapping(properties.get("blocker_id")).get("enum", ())) != _BLOCKER_IDS:
        _fail(failures, "intake_schema_blocker_mismatch", path, "all eight blocker IDs are required in order")
    if tuple(_mapping(properties.get("owner_role")).get("enum", ())) != _OWNER_ROLES:
        _fail(failures, "intake_schema_role_mismatch", path, "owner roles must match governance records")
    expected_statuses = (
        "NOT_SUBMITTED",
        "SUBMITTED_UNVERIFIED",
        "VERIFIED_PENDING_GOVERNANCE",
        "ACCEPTED_FOR_REVIEW",
        "REJECTED",
    )
    intake_definitions = _mapping(schema.get("$defs"))
    if tuple(_mapping(intake_definitions.get("IntakeStatus")).get("enum", ())) != expected_statuses:
        _fail(failures, "intake_schema_status_mismatch", path, "canonical intake statuses are required")
    if _mapping(properties.get("intake_status")).get("const") != "NOT_SUBMITTED":
        _fail(failures, "intake_schema_status_mismatch", path, "current intake status must remain NOT_SUBMITTED")
    constants = {
        "accountable_party_status": "UNASSIGNED",
        "authority_reference_status": "ABSENT",
        "contains_credentials": False,
        "contains_secrets": False,
        "identity_established": False,
        "authority_established": False,
        "approval_granted": False,
        "blocker_resolved": False,
    }
    for field, expected in constants.items():
        if _mapping(properties.get(field)).get("const") != expected:
            _fail(failures, "intake_schema_effect_mismatch", path, field)
    intake_contract = _mapping(contract.get("authority_intake"))
    contract_expectations = {
        "schema": "schemas/event-bus-v2-authority-intake.schema.json",
        "validation_effect": "structure_only",
        "current_status": "NOT_SUBMITTED",
        "accountable_party_status": "UNASSIGNED",
        "authority_reference_status": "ABSENT",
        "establishes_identity": False,
        "establishes_authority": False,
        "grants_approval": False,
        "resolves_blocker": False,
        "credentials_permitted": False,
        "secrets_permitted": False,
        "submitted_evidence_status": "unverified",
        "runtime_effect": "none",
    }
    for field, expected in contract_expectations.items():
        if intake_contract.get(field) != expected:
            _fail(failures, "intake_contract_boundary_mismatch", "contracts/event-bus-v2.yaml", field)


def _validate_authority_intake_submission_contract(
    contract: Mapping[str, Any],
    schema: Mapping[str, Any],
    failures: list[EventBusV2ValidationFailure],
) -> None:
    path = "schemas/event-bus-v2-authority-intake-submission.schema.json"
    properties = _mapping(schema.get("properties"))
    expected_fields = {
        "submission_schema_version",
        "intake_id",
        "blocker_id",
        "owner_role",
        "proposed_accountable_party_id",
        "proposed_authority_source",
        "proposed_authority_reference",
        "proposed_authority_scope",
        "submission_evidence_hash",
        "submitted_at",
        "intake_status",
        "submitted_evidence_status",
        "accountable_party_status",
        "authority_reference_status",
        "contains_credentials",
        "contains_secrets",
        "contains_unnecessary_personal_data",
        "identity_established",
        "authority_established",
        "party_assigned",
        "approval_granted",
        "blocker_resolved",
    }
    required = schema.get("required")
    if schema.get("additionalProperties") is not False:
        _fail(failures, "submission_schema_open", path, "additional properties must be prohibited")
    if set(properties) != expected_fields:
        _fail(
            failures,
            "submission_schema_field_mismatch",
            path,
            "only the canonical reference, evidence, status, and effect fields are permitted",
        )
    if not _string_sequence(required) or set(required) != expected_fields:
        _fail(failures, "submission_schema_required_fields", path, "all canonical fields are required")
    if _mapping(properties.get("submission_schema_version")).get("const") != "2.0.0":
        _fail(failures, "submission_schema_version_mismatch", path, "submission schema version must be 2.0.0")
    if tuple(_mapping(properties.get("blocker_id")).get("enum", ())) != _BLOCKER_IDS:
        _fail(failures, "submission_schema_blocker_mismatch", path, "all eight blocker IDs are required in order")
    if tuple(_mapping(properties.get("owner_role")).get("enum", ())) != _OWNER_ROLES:
        _fail(failures, "submission_schema_role_mismatch", path, "owner roles must match governance records")
    constants = {
        "intake_status": "SUBMITTED_UNVERIFIED",
        "submitted_evidence_status": "unverified",
        "accountable_party_status": "UNASSIGNED",
        "authority_reference_status": "ABSENT",
        "contains_credentials": False,
        "contains_secrets": False,
        "contains_unnecessary_personal_data": False,
        "identity_established": False,
        "authority_established": False,
        "party_assigned": False,
        "approval_granted": False,
        "blocker_resolved": False,
    }
    for field, expected in constants.items():
        if _mapping(properties.get(field)).get("const") != expected:
            _fail(failures, "submission_schema_effect_mismatch", path, field)

    submission_contract = _mapping(contract.get("authority_intake_submission"))
    contract_expectations = {
        "schema": path,
        "validation_effect": "structure_only",
        "allowed_status": "SUBMITTED_UNVERIFIED",
        "submitted_evidence_status": "unverified",
        "accountable_party_status": "UNASSIGNED",
        "authority_reference_status": "ABSENT",
        "establishes_identity": False,
        "establishes_authority": False,
        "assigns_party": False,
        "grants_approval": False,
        "resolves_blocker": False,
        "credentials_permitted": False,
        "secrets_permitted": False,
        "unnecessary_personal_data_permitted": False,
        "inferred_authority_permitted": False,
        "runtime_effect": "none",
    }
    for field, expected in contract_expectations.items():
        if submission_contract.get(field) != expected:
            _fail(
                failures,
                "submission_contract_boundary_mismatch",
                "contracts/event-bus-v2.yaml",
                field,
            )


def _validate_authority_intake_verification_contract(
    contract: Mapping[str, Any],
    schema: Mapping[str, Any],
    failures: list[EventBusV2ValidationFailure],
) -> None:
    path = "schemas/event-bus-v2-authority-intake-verification.schema.json"
    properties = _mapping(schema.get("properties"))
    expected_fields = {
        "verification_schema_version",
        "verification_id",
        "intake_id",
        "blocker_id",
        "source_intake_status",
        "subject_party_reference",
        "verifier_party_reference",
        "verifier_authority_evidence_reference",
        "verifier_authority_evidence_hash",
        "verified_evidence_references",
        "submission_evidence_hash",
        "verification_evidence_hash",
        "evidence_provenance",
        "scope_alignment",
        "self_verification_check",
        "verification_outcome",
        "failure_codes",
        "resulting_intake_status",
        "verified_at",
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
    }
    required = schema.get("required")
    if schema.get("additionalProperties") is not False:
        _fail(failures, "verification_schema_open", path, "additional properties must be prohibited")
    if set(properties) != expected_fields:
        _fail(
            failures,
            "verification_schema_field_mismatch",
            path,
            "only canonical verification evidence and effect fields are permitted",
        )
    if not _string_sequence(required) or set(required) != expected_fields:
        _fail(failures, "verification_schema_required_fields", path, "all canonical fields are required")
    if _mapping(properties.get("verification_schema_version")).get("const") != "2.0.0":
        _fail(failures, "verification_schema_version_mismatch", path, "verification schema version must be 2.0.0")
    if tuple(_mapping(properties.get("blocker_id")).get("enum", ())) != _BLOCKER_IDS:
        _fail(failures, "verification_schema_blocker_mismatch", path, "all eight blocker IDs are required in order")

    evidence_references = _mapping(properties.get("verified_evidence_references"))
    if evidence_references.get("minItems") != 1 or evidence_references.get("uniqueItems") is not True:
        _fail(failures, "verification_evidence_reference_mismatch", path, "unique evidence references are required")
    provenance = _mapping(properties.get("evidence_provenance"))
    provenance_required = {"source_category", "source_reference", "evidence_hash", "observed_at"}
    if provenance.get("additionalProperties") is not False or set(provenance.get("required", ())) != provenance_required:
        _fail(failures, "verification_provenance_mismatch", path, "complete closed provenance is required")
    alignment = _mapping(properties.get("scope_alignment"))
    alignment_required = {"blocker_id", "submitted_scope_hash", "verifier_scope_hash", "outcome"}
    if alignment.get("additionalProperties") is not False or set(alignment.get("required", ())) != alignment_required:
        _fail(failures, "verification_scope_mismatch", path, "complete closed scope alignment is required")
    alignment_outcomes = tuple(
        _mapping(_mapping(alignment.get("properties")).get("outcome")).get("enum", ())
    )
    if alignment_outcomes != ("ALIGNED", "MISMATCH", "UNVERIFIED"):
        _fail(failures, "verification_scope_mismatch", path, "canonical scope outcomes are required")
    self_check = _mapping(properties.get("self_verification_check"))
    self_check_required = {
        "subject_party_reference_hash",
        "verifier_party_reference_hash",
        "outcome",
        "evidence_hash",
    }
    self_check_properties = _mapping(self_check.get("properties"))
    if (
        self_check.get("additionalProperties") is not False
        or set(self_check.get("required", ())) != self_check_required
        or _mapping(self_check_properties.get("outcome")).get("const") != "DISTINCT"
    ):
        _fail(
            failures,
            "verification_self_check_mismatch",
            path,
            "hash-bound evidence with a DISTINCT outcome is required",
        )

    expected_outcomes = (
        "VERIFIED",
        "INCOMPLETE",
        "INVALID",
        "CONFLICT",
        "EXPIRED",
        "REVOKED",
        "UNVERIFIABLE",
    )
    if tuple(_mapping(properties.get("verification_outcome")).get("enum", ())) != expected_outcomes:
        _fail(failures, "verification_outcome_mismatch", path, "canonical deterministic outcomes are required")
    constants = {
        "source_intake_status": "SUBMITTED_UNVERIFIED",
        "self_verification_detected": False,
        "inferred_authority": False,
        "contains_credentials": False,
        "contains_secrets": False,
        "contains_excess_personal_data": False,
        "identity_established": False,
        "authority_assigned": False,
        "approval_granted": False,
        "blocker_resolved": False,
        "execution_authorized": False,
    }
    for field, expected in constants.items():
        if _mapping(properties.get(field)).get("const") != expected:
            _fail(failures, "verification_schema_effect_mismatch", path, field)

    all_of = schema.get("allOf")
    rule = _mapping(all_of[0]) if _sequence(all_of) and len(all_of) == 1 else {}
    condition_properties = _mapping(_mapping(rule.get("if")).get("properties"))
    verified_condition = _mapping(condition_properties.get("verification_outcome")).get("const")
    then_properties = _mapping(_mapping(rule.get("then")).get("properties"))
    else_properties = _mapping(_mapping(rule.get("else")).get("properties"))
    verified_status = _mapping(then_properties.get("resulting_intake_status")).get("const")
    verified_failures = _mapping(then_properties.get("failure_codes")).get("maxItems")
    verified_alignment = _mapping(
        _mapping(_mapping(then_properties.get("scope_alignment")).get("properties")).get("outcome")
    ).get("const")
    failure_status = _mapping(else_properties.get("resulting_intake_status")).get("const")
    failure_codes = _mapping(else_properties.get("failure_codes")).get("minItems")
    if (
        verified_condition != "VERIFIED"
        or verified_status != "VERIFIED_PENDING_GOVERNANCE"
        or verified_failures != 0
        or verified_alignment != "ALIGNED"
        or failure_status != "SUBMITTED_UNVERIFIED"
        or failure_codes != 1
    ):
        _fail(
            failures,
            "verification_transition_mismatch",
            path,
            "only complete aligned verification may propose pending governance",
        )

    verification_contract = _mapping(contract.get("authority_intake_verification"))
    contract_expectations = {
        "schema": path,
        "validation_effect": "structure_only",
        "source_status": "SUBMITTED_UNVERIFIED",
        "verified_status": "VERIFIED_PENDING_GOVERNANCE",
        "failure_status": "SUBMITTED_UNVERIFIED",
        "deterministic_outcomes": list(expected_outcomes),
        "verifier_authority_evidence_required": True,
        "evidence_references_required": True,
        "evidence_hashes_required": True,
        "provenance_required": True,
        "scope_alignment_required": True,
        "self_verification_permitted": False,
        "inferred_authority_permitted": False,
        "credentials_permitted": False,
        "secrets_permitted": False,
        "excess_personal_data_permitted": False,
        "establishes_identity": False,
        "assigns_authority": False,
        "grants_approval": False,
        "resolves_blocker": False,
        "authorizes_execution": False,
        "mutates_current_register": False,
        "runtime_effect": "none",
    }
    for field, expected in contract_expectations.items():
        if verification_contract.get(field) != expected:
            _fail(
                failures,
                "verification_contract_boundary_mismatch",
                "contracts/event-bus-v2.yaml",
                field,
            )


def _validate_authority_intake_governance_admission_contract(
    root: Path,
    contract: Mapping[str, Any],
    schema: Mapping[str, Any],
    failures: list[EventBusV2ValidationFailure],
) -> None:
    path = "schemas/event-bus-v2-authority-intake-governance-admission.schema.json"
    properties = _mapping(schema.get("properties"))
    expected_fields = {
        "admission_schema_version",
        "admission_id",
        "intake_id",
        "blocker_id",
        "source_intake_status",
        "verification_record_reference",
        "verification_record_hash",
        "verification_verifier_party_reference_hash",
        "governance_reviewer_party_reference",
        "governance_reviewer_party_reference_hash",
        "governance_reviewer_authority_evidence_reference",
        "governance_reviewer_authority_evidence_hash",
        "evidence_provenance",
        "scope_alignment",
        "reviewer_independence_check",
        "admission_outcome",
        "admission_reason_codes",
        "resulting_intake_status",
        "admitted_at",
        "hold_status",
        "contains_credentials",
        "contains_secrets",
        "contains_excess_personal_data",
        "self_review_detected",
        "verifier_authority_evidence_reused",
        "inferred_governance_authority",
        "identity_established",
        "party_assigned",
        "authority_assigned",
        "authority_reference_granted",
        "approval_granted",
        "contract_approved",
        "blocker_resolved",
        "blockers_resolved",
        "execution_authorized",
        "runtime_enabled",
        "current_register_mutated",
        "runtime_effect",
    }
    required = schema.get("required")
    if schema.get("additionalProperties") is not False:
        _fail(failures, "admission_schema_open", path, "additional properties must be prohibited")
    if set(properties) != expected_fields:
        _fail(
            failures,
            "admission_schema_field_mismatch",
            path,
            "only canonical admission evidence and effect fields are permitted",
        )
    if not _string_sequence(required) or set(required) != expected_fields:
        _fail(failures, "admission_schema_required_fields", path, "all canonical fields are required")
    if _mapping(properties.get("admission_schema_version")).get("const") != "2.0.0":
        _fail(failures, "admission_schema_version_mismatch", path, "admission schema version must be 2.0.0")
    if tuple(_mapping(properties.get("blocker_id")).get("enum", ())) != _BLOCKER_IDS:
        _fail(failures, "admission_schema_blocker_mismatch", path, "all eight blocker IDs are required in order")

    expected_refs = {
        "verification_record_reference": "event-bus-runtime-v2.schema.json#/$defs/NonEmptyString",
        "verification_record_hash": "event-bus-runtime-v2.schema.json#/$defs/Sha256Hex",
        "governance_reviewer_authority_evidence_reference": "event-bus-runtime-v2.schema.json#/$defs/NonEmptyString",
        "governance_reviewer_authority_evidence_hash": "event-bus-runtime-v2.schema.json#/$defs/Sha256Hex",
    }
    for field, expected_ref in expected_refs.items():
        if _mapping(properties.get(field)).get("$ref") != expected_ref:
            _fail(failures, "admission_evidence_reference_mismatch", path, field)

    provenance = _mapping(properties.get("evidence_provenance"))
    provenance_required = {"source_category", "source_reference", "evidence_hash", "observed_at"}
    if provenance.get("additionalProperties") is not False or set(provenance.get("required", ())) != provenance_required:
        _fail(failures, "admission_provenance_mismatch", path, "complete closed provenance is required")
    alignment = _mapping(properties.get("scope_alignment"))
    alignment_required = {"blocker_id", "verified_scope_hash", "reviewer_scope_hash", "outcome"}
    alignment_properties = _mapping(alignment.get("properties"))
    if (
        alignment.get("additionalProperties") is not False
        or set(alignment.get("required", ())) != alignment_required
        or _mapping(alignment_properties.get("outcome")).get("const") != "ALIGNED"
    ):
        _fail(failures, "admission_scope_mismatch", path, "complete aligned scope evidence is required")
    independence = _mapping(properties.get("reviewer_independence_check"))
    independence_required = {
        "verification_verifier_party_reference_hash",
        "governance_reviewer_party_reference_hash",
        "verification_authority_evidence_hash",
        "governance_reviewer_authority_evidence_hash",
        "outcome",
        "evidence_hash",
    }
    independence_properties = _mapping(independence.get("properties"))
    if (
        independence.get("additionalProperties") is not False
        or set(independence.get("required", ())) != independence_required
        or _mapping(independence_properties.get("outcome")).get("const")
        != "DISTINCT_AND_INDEPENDENT"
    ):
        _fail(
            failures,
            "admission_independence_mismatch",
            path,
            "hash-bound distinct reviewer and authority evidence is required",
        )

    expected_outcomes = ("ACCEPTED_FOR_REVIEW", "REJECTED")
    if tuple(_mapping(properties.get("admission_outcome")).get("enum", ())) != expected_outcomes:
        _fail(failures, "admission_outcome_mismatch", path, "only canonical admission outcomes are permitted")
    constants = {
        "source_intake_status": "VERIFIED_PENDING_GOVERNANCE",
        "hold_status": "ACTIVE",
        "contains_credentials": False,
        "contains_secrets": False,
        "contains_excess_personal_data": False,
        "self_review_detected": False,
        "verifier_authority_evidence_reused": False,
        "inferred_governance_authority": False,
        "identity_established": False,
        "party_assigned": False,
        "authority_assigned": False,
        "authority_reference_granted": False,
        "approval_granted": False,
        "contract_approved": False,
        "blocker_resolved": False,
        "blockers_resolved": False,
        "execution_authorized": False,
        "runtime_enabled": False,
        "current_register_mutated": False,
        "runtime_effect": "NONE",
    }
    for field, expected in constants.items():
        if _mapping(properties.get(field)).get("const") != expected:
            _fail(failures, "admission_schema_effect_mismatch", path, field)

    all_of = schema.get("allOf")
    rule = _mapping(all_of[0]) if _sequence(all_of) and len(all_of) == 1 else {}
    condition_properties = _mapping(_mapping(rule.get("if")).get("properties"))
    accepted_condition = _mapping(condition_properties.get("admission_outcome")).get("const")
    then_properties = _mapping(_mapping(rule.get("then")).get("properties"))
    else_properties = _mapping(_mapping(rule.get("else")).get("properties"))
    accepted_status = _mapping(then_properties.get("resulting_intake_status")).get("const")
    accepted_reasons = _mapping(then_properties.get("admission_reason_codes")).get("maxItems")
    rejected_status = _mapping(else_properties.get("resulting_intake_status")).get("const")
    rejected_reasons = _mapping(else_properties.get("admission_reason_codes")).get("minItems")
    if (
        accepted_condition != "ACCEPTED_FOR_REVIEW"
        or accepted_status != "ACCEPTED_FOR_REVIEW"
        or accepted_reasons != 0
        or rejected_status != "REJECTED"
        or rejected_reasons != 1
    ):
        _fail(failures, "admission_transition_mismatch", path, "admission outcomes must map deterministically")

    admission_contract = _mapping(contract.get("authority_intake_governance_admission"))
    contract_expectations = {
        "schema": path,
        "validation_effect": "structure_only",
        "source_status": "VERIFIED_PENDING_GOVERNANCE",
        "deterministic_outcomes": list(expected_outcomes),
        "governance_reviewer_authority_evidence_required": True,
        "verification_record_reference_required": True,
        "verification_record_hash_required": True,
        "provenance_required": True,
        "scope_alignment_required": True,
        "independent_reviewer_evidence_required": True,
        "self_review_permitted": False,
        "verifier_authority_evidence_reuse_permitted": False,
        "inferred_governance_authority_permitted": False,
        "credentials_permitted": False,
        "secrets_permitted": False,
        "excess_personal_data_permitted": False,
        "accepted_for_review_is_approval": False,
        "rejected_is_blocker_resolution": False,
        "assigns_party": False,
        "assigns_authority": False,
        "grants_authority_reference": False,
        "grants_approval": False,
        "resolves_blocker": False,
        "authorizes_execution": False,
        "mutates_current_register": False,
        "runtime_effect": "none",
    }
    for field, expected in contract_expectations.items():
        if admission_contract.get(field) != expected:
            _fail(
                failures,
                "admission_contract_boundary_mismatch",
                "contracts/event-bus-v2.yaml",
                field,
            )

    for document_path in (
        "contracts/event-bus-v2-approval-record.md",
        "contracts/event-bus-v2-decision-log.md",
    ):
        text = (root / document_path).read_text(encoding="utf-8")
        if path not in text:
            _fail(failures, "admission_contract_reference_missing", document_path, path)


def _validate_authority_intake_governance_review_contract(
    root: Path,
    contract: Mapping[str, Any],
    schema: Mapping[str, Any],
    failures: list[EventBusV2ValidationFailure],
) -> None:
    path = "schemas/event-bus-v2-authority-intake-governance-review.schema.json"
    properties = _mapping(schema.get("properties"))
    expected_fields = {
        "review_schema_version",
        "review_id",
        "intake_id",
        "blocker_id",
        "source_intake_status",
        "admission_record_reference",
        "admission_record_hash",
        "admission_reviewer_party_reference_hash",
        "admission_reviewer_authority_evidence_hash",
        "verification_authority_evidence_hash",
        "governance_review_party_reference",
        "governance_review_party_reference_hash",
        "governance_review_authority_evidence_reference",
        "governance_review_authority_evidence_hash",
        "review_evidence_references",
        "review_evidence_hash",
        "evidence_provenance",
        "scope_alignment",
        "reviewer_independence_check",
        "review_outcome",
        "review_reason_codes",
        "resulting_intake_status",
        "reviewed_at",
        "hold_status",
        "contains_credentials",
        "contains_secrets",
        "contains_excess_personal_data",
        "self_review_detected",
        "admission_authority_evidence_reused",
        "verifier_authority_evidence_reused",
        "inferred_governance_authority",
        "identity_established",
        "party_assigned",
        "authority_assigned",
        "authority_reference_granted",
        "approval_granted",
        "contract_approved",
        "blocker_resolved",
        "blockers_resolved",
        "execution_authorized",
        "runtime_enabled",
        "current_register_mutated",
        "runtime_effect",
    }
    required = schema.get("required")
    if schema.get("additionalProperties") is not False:
        _fail(failures, "governance_review_schema_open", path, "additional properties must be prohibited")
    if set(properties) != expected_fields:
        _fail(
            failures,
            "governance_review_schema_field_mismatch",
            path,
            "only canonical review evidence and effect fields are permitted",
        )
    if not _string_sequence(required) or set(required) != expected_fields:
        _fail(failures, "governance_review_schema_required_fields", path, "all canonical fields are required")
    if _mapping(properties.get("review_schema_version")).get("const") != "2.0.0":
        _fail(failures, "governance_review_schema_version_mismatch", path, "review schema version must be 2.0.0")
    if tuple(_mapping(properties.get("blocker_id")).get("enum", ())) != _BLOCKER_IDS:
        _fail(failures, "governance_review_schema_blocker_mismatch", path, "all eight blocker IDs are required in order")

    expected_refs = {
        "admission_record_reference": "event-bus-runtime-v2.schema.json#/$defs/NonEmptyString",
        "admission_record_hash": "event-bus-runtime-v2.schema.json#/$defs/Sha256Hex",
        "governance_review_authority_evidence_reference": "event-bus-runtime-v2.schema.json#/$defs/NonEmptyString",
        "governance_review_authority_evidence_hash": "event-bus-runtime-v2.schema.json#/$defs/Sha256Hex",
    }
    for field, expected_ref in expected_refs.items():
        if _mapping(properties.get(field)).get("$ref") != expected_ref:
            _fail(failures, "governance_review_evidence_reference_mismatch", path, field)
    evidence_references = _mapping(properties.get("review_evidence_references"))
    if evidence_references.get("minItems") != 1 or evidence_references.get("uniqueItems") is not True:
        _fail(failures, "governance_review_evidence_reference_mismatch", path, "review_evidence_references")

    provenance = _mapping(properties.get("evidence_provenance"))
    provenance_required = {"source_category", "source_reference", "evidence_hash", "observed_at"}
    if provenance.get("additionalProperties") is not False or set(provenance.get("required", ())) != provenance_required:
        _fail(failures, "governance_review_provenance_mismatch", path, "complete closed provenance is required")
    alignment = _mapping(properties.get("scope_alignment"))
    alignment_required = {"blocker_id", "admitted_scope_hash", "reviewer_scope_hash", "outcome"}
    alignment_properties = _mapping(alignment.get("properties"))
    if (
        alignment.get("additionalProperties") is not False
        or set(alignment.get("required", ())) != alignment_required
        or _mapping(alignment_properties.get("outcome")).get("const") != "ALIGNED"
    ):
        _fail(failures, "governance_review_scope_mismatch", path, "complete aligned scope evidence is required")

    independence = _mapping(properties.get("reviewer_independence_check"))
    independence_required = {
        "admission_reviewer_party_reference_hash",
        "governance_review_party_reference_hash",
        "verification_authority_evidence_hash",
        "admission_authority_evidence_hash",
        "governance_review_authority_evidence_hash",
        "outcome",
        "evidence_hash",
    }
    independence_properties = _mapping(independence.get("properties"))
    if (
        independence.get("additionalProperties") is not False
        or set(independence.get("required", ())) != independence_required
        or _mapping(independence_properties.get("outcome")).get("const")
        != "DISTINCT_AND_INDEPENDENT"
    ):
        _fail(
            failures,
            "governance_review_independence_mismatch",
            path,
            "reviewer and authority evidence must be distinct from prior-stage evidence",
        )

    expected_outcomes = (
        "FAVORABLE_REVIEW_RECORDED",
        "ADDITIONAL_INFORMATION_REQUIRED",
        "REVIEW_REJECTED",
    )
    actual_outcomes = tuple(_mapping(properties.get("review_outcome")).get("enum", ()))
    if actual_outcomes != expected_outcomes:
        _fail(failures, "governance_review_outcome_mismatch", path, "canonical review outcomes are required")
    if set(actual_outcomes).intersection(_SPRINT_2J_REVIEW_OUTCOMES):
        _fail(failures, "sprint_2j_review_outcome_reuse", path, "escalation-review outcomes are incompatible")
    resulting_states = tuple(
        _mapping(properties.get("resulting_intake_status")).get("enum", ())
    )
    if resulting_states != ("ACCEPTED_FOR_REVIEW", "REJECTED"):
        _fail(
            failures,
            "unsupported_post_review_state",
            path,
            "review may reference only existing accepted or rejected intake states",
        )

    constants = {
        "source_intake_status": "ACCEPTED_FOR_REVIEW",
        "hold_status": "ACTIVE",
        "contains_credentials": False,
        "contains_secrets": False,
        "contains_excess_personal_data": False,
        "self_review_detected": False,
        "admission_authority_evidence_reused": False,
        "verifier_authority_evidence_reused": False,
        "inferred_governance_authority": False,
        "identity_established": False,
        "party_assigned": False,
        "authority_assigned": False,
        "authority_reference_granted": False,
        "approval_granted": False,
        "contract_approved": False,
        "blocker_resolved": False,
        "blockers_resolved": False,
        "execution_authorized": False,
        "runtime_enabled": False,
        "current_register_mutated": False,
        "runtime_effect": "NONE",
    }
    for field, expected in constants.items():
        if _mapping(properties.get(field)).get("const") != expected:
            _fail(failures, "governance_review_schema_effect_mismatch", path, field)

    all_of = schema.get("allOf")
    rules = tuple(_mapping(rule) for rule in all_of) if _sequence(all_of) else ()
    transition_rule = rules[0] if len(rules) == 2 else {}
    reason_rule = rules[1] if len(rules) == 2 else {}
    transition_condition = _mapping(
        _mapping(_mapping(transition_rule.get("if")).get("properties")).get("review_outcome")
    ).get("const")
    transition_then = _mapping(_mapping(transition_rule.get("then")).get("properties"))
    transition_else = _mapping(_mapping(transition_rule.get("else")).get("properties"))
    rejected_status = _mapping(transition_then.get("resulting_intake_status")).get("const")
    retained_status = _mapping(transition_else.get("resulting_intake_status")).get("const")
    reason_condition = _mapping(
        _mapping(_mapping(reason_rule.get("if")).get("properties")).get("review_outcome")
    ).get("const")
    reason_then = _mapping(_mapping(reason_rule.get("then")).get("properties"))
    reason_else = _mapping(_mapping(reason_rule.get("else")).get("properties"))
    favorable_reasons = _mapping(reason_then.get("review_reason_codes")).get("maxItems")
    adverse_reasons = _mapping(reason_else.get("review_reason_codes")).get("minItems")
    if (
        transition_condition != "REVIEW_REJECTED"
        or rejected_status != "REJECTED"
        or retained_status != "ACCEPTED_FOR_REVIEW"
        or reason_condition != "FAVORABLE_REVIEW_RECORDED"
        or favorable_reasons != 0
        or adverse_reasons != 1
    ):
        _fail(
            failures,
            "governance_review_transition_mismatch",
            path,
            "review outcomes must map only to existing intake states",
        )

    review_contract = _mapping(contract.get("authority_intake_governance_review"))
    contract_expectations = {
        "schema": path,
        "validation_effect": "structure_only",
        "source_status": "ACCEPTED_FOR_REVIEW",
        "deterministic_outcomes": list(expected_outcomes),
        "favorable_status": "ACCEPTED_FOR_REVIEW",
        "additional_information_status": "ACCEPTED_FOR_REVIEW",
        "rejected_status": "REJECTED",
        "sprint_2j_outcomes_compatible": False,
        "admission_record_reference_required": True,
        "admission_record_hash_required": True,
        "governance_reviewer_authority_evidence_required": True,
        "provenance_required": True,
        "scope_alignment_required": True,
        "independent_review_evidence_required": True,
        "self_review_permitted": False,
        "admission_authority_evidence_reuse_permitted": False,
        "verifier_authority_evidence_reuse_permitted": False,
        "inferred_governance_authority_permitted": False,
        "credentials_permitted": False,
        "secrets_permitted": False,
        "excess_personal_data_permitted": False,
        "favorable_review_is_approval": False,
        "rejected_review_is_blocker_resolution": False,
        "assigns_party": False,
        "assigns_authority": False,
        "grants_authority_reference": False,
        "grants_approval": False,
        "resolves_blocker": False,
        "authorizes_execution": False,
        "mutates_current_register": False,
        "runtime_effect": "none",
    }
    for field, expected in contract_expectations.items():
        if review_contract.get(field) != expected:
            _fail(
                failures,
                "governance_review_contract_boundary_mismatch",
                "contracts/event-bus-v2.yaml",
                field,
            )

    for document_path in (
        "contracts/event-bus-v2-approval-record.md",
        "contracts/event-bus-v2-decision-log.md",
    ):
        text = (root / document_path).read_text(encoding="utf-8")
        if path not in text:
            _fail(failures, "governance_review_contract_reference_missing", document_path, path)
        for outcome in expected_outcomes:
            if outcome not in text:
                _fail(failures, "governance_review_vocabulary_missing", document_path, outcome)


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


def _validate_blocker_matrix(
    root: Path,
    failures: list[EventBusV2ValidationFailure],
) -> None:
    path = "contracts/event-bus-v2-blocker-matrix.md"
    try:
        text = (root / path).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        _fail(failures, "invalid_blocker_matrix", path, str(exc))
        return
    if not text.strip():
        _fail(failures, "empty_blocker_matrix", path, "blocker matrix must not be empty")
        return
    required_sections = (
        "# Event Bus v2 Blocker Dependency Matrix",
        "## Governance Boundary",
        "## Dependency Summary",
        "## Matrix Disposition",
    )
    for heading in required_sections:
        if heading not in text:
            _fail(failures, "missing_matrix_section", path, heading)

    if "Dependency mapping does not grant approval." not in text:
        _fail(failures, "matrix_approval_boundary_missing", path, "non-approval statement is required")
    if "HOLD remains active" not in text or "approved: false" not in text:
        _fail(failures, "matrix_hold_boundary_missing", path, "HOLD and approved:false boundaries are required")

    sections = _matrix_blocker_sections(text)
    if tuple(sections) != _BLOCKER_IDS:
        _fail(failures, "matrix_blocker_set_mismatch", path, "EVT2-B01 through EVT2-B08 are required exactly once and in order")
        return

    valid_ids = set(_BLOCKER_IDS)
    for blocker_id, section in sections.items():
        fields = _matrix_fields(section)
        for field in _MATRIX_FIELDS:
            value = fields.get(field)
            if not value:
                _fail(failures, "missing_matrix_field", path, f"{blocker_id}:{field}")
        if fields.get("Status") != "`UNRESOLVED`":
            _fail(failures, "matrix_blocker_resolved", path, blocker_id)
        if fields.get("Accountable party") != "`UNASSIGNED`":
            _fail(failures, "matrix_party_assigned", path, blocker_id)
        if fields.get("Authority reference status") != "`ABSENT`":
            _fail(failures, "matrix_authority_present", path, blocker_id)
        for dependency_field in ("Upstream dependencies", "Downstream dependencies"):
            value = fields.get(dependency_field, "")
            references = set(re.findall(r"EVT2-B0[1-8]", value))
            if blocker_id in references:
                _fail(failures, "matrix_self_dependency", path, f"{blocker_id}:{dependency_field}")
            if not references.issubset(valid_ids):
                _fail(failures, "matrix_unknown_dependency", path, f"{blocker_id}:{dependency_field}")


def _validate_approval_and_intake_records(
    root: Path,
    failures: list[EventBusV2ValidationFailure],
) -> None:
    approval_path = "contracts/event-bus-v2-approval-record.md"
    decision_path = "contracts/event-bus-v2-decision-log.md"
    matrix_path = "contracts/event-bus-v2-blocker-matrix.md"
    approval = (root / approval_path).read_text(encoding="utf-8")
    decision = (root / decision_path).read_text(encoding="utf-8")
    matrix = (root / matrix_path).read_text(encoding="utf-8")

    if (
        "Record status: `HOLD`" not in approval
        or "Approval status: `NOT APPROVED`" not in approval
        or "Runtime implementation permitted: `NO`" not in approval
        or "HOLD remains active" not in approval
    ):
        _fail(failures, "approval_record_hold_mismatch", approval_path, "approval record must remain HOLD and not approved")
    if "Approval status: `HOLD`" not in decision or "HOLD remains" not in decision:
        _fail(failures, "decision_log_hold_mismatch", decision_path, "decision log must remain on HOLD")
    if "do not grant approval" not in approval.lower() or "do not grant approval" not in decision.lower():
        _fail(failures, "conformance_nonapproval_missing", approval_path, "conformance must not grant approval")
    if "`approved: true` must remain rejected" not in approval:
        _fail(failures, "approval_rejection_rule_missing", approval_path, "approved:true rejection rule is required")

    approval_blockers = _markdown_table_rows(
        approval,
        "## Blocker Register",
        "## Accountable Authority Intake Structure",
    )
    decision_blockers = _markdown_table_rows(
        decision,
        "## Unresolved Approval Blockers",
        "## Accountable Authority Intake",
    )
    approval_intake = _markdown_table_rows(
        approval,
        "## Current Authority Intake Register",
        "## Approval Readiness",
    )
    decision_intake = _markdown_table_rows(
        decision,
        "## Accountable Authority Intake",
        "## Approval Gate",
    )
    matrix_ids = tuple(_matrix_blocker_sections(matrix))

    _validate_blocker_rows(approval_blockers, approval_path, failures)
    _validate_blocker_rows(decision_blockers, decision_path, failures)
    _validate_intake_rows(approval_intake, approval_path, failures)
    _validate_intake_rows(decision_intake, decision_path, failures)

    sets = (
        tuple(row[0] for row in approval_blockers),
        tuple(row[0] for row in decision_blockers),
        tuple(row[0] for row in approval_intake),
        tuple(row[0] for row in decision_intake),
        matrix_ids,
    )
    if any(blocker_ids != _BLOCKER_IDS for blocker_ids in sets):
        _fail(failures, "governance_blocker_set_mismatch", approval_path, "all governance records must contain EVT2-B01 through EVT2-B08 exactly once and in order")


def _validate_blocker_rows(
    rows: tuple[tuple[str, ...], ...],
    path: str,
    failures: list[EventBusV2ValidationFailure],
) -> None:
    for index, row in enumerate(rows):
        if len(row) < 5:
            _fail(failures, "malformed_blocker_row", path, str(index))
            continue
        blocker_id = row[0]
        if blocker_id not in _BLOCKER_IDS:
            continue
        expected_role = _OWNER_ROLES[_BLOCKER_IDS.index(blocker_id)]
        role = row[3] if len(row) >= 6 else row[2]
        disposition = row[4] if len(row) >= 6 else row[4]
        if role != expected_role:
            _fail(failures, "owner_role_mismatch", path, blocker_id)
        if disposition != "`UNRESOLVED`":
            _fail(failures, "approval_blocker_resolved", path, blocker_id)


def _validate_intake_rows(
    rows: tuple[tuple[str, ...], ...],
    path: str,
    failures: list[EventBusV2ValidationFailure],
) -> None:
    for index, row in enumerate(rows):
        if len(row) != 6:
            _fail(failures, "malformed_intake_row", path, str(index))
            continue
        blocker_id, role, party, authority, intake_status, disposition = row
        if blocker_id not in _BLOCKER_IDS:
            continue
        expected_role = _OWNER_ROLES[_BLOCKER_IDS.index(blocker_id)]
        if role != expected_role:
            _fail(failures, "owner_role_mismatch", path, blocker_id)
        if party != "`UNASSIGNED`":
            _fail(failures, "approval_party_assigned", path, blocker_id)
        if authority != "`ABSENT`":
            _fail(failures, "approval_authority_present", path, blocker_id)
        if intake_status != "`NOT_SUBMITTED`":
            _fail(failures, "approval_intake_submitted", path, blocker_id)
        if disposition != "`UNRESOLVED`":
            _fail(failures, "approval_blocker_resolved", path, blocker_id)


def _markdown_table_rows(
    text: str,
    start_heading: str,
    end_heading: str,
) -> tuple[tuple[str, ...], ...]:
    start = text.find(start_heading)
    end = text.find(end_heading, start + len(start_heading)) if start >= 0 else -1
    if start < 0 or end < 0:
        return ()
    rows: list[tuple[str, ...]] = []
    for raw_line in text[start:end].splitlines():
        if not re.match(r"^\| EVT2-B0[1-8] \|", raw_line):
            continue
        cells = tuple(cell.strip() for cell in raw_line.strip().strip("|").split("|"))
        rows.append(cells)
    return tuple(rows)


def _matrix_blocker_sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^## (EVT2-B0[1-8])\s*$", text, re.MULTILINE))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocker_id = match.group(1)
        if blocker_id in sections:
            return {}
        sections[blocker_id] = text[match.end():end]
    return sections


def _matrix_fields(section: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in section.splitlines():
        if not raw_line.startswith("- ") or ":" not in raw_line:
            continue
        key, value = raw_line[2:].split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


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
