"""Pure, deterministic, fail-closed NI AI transition-envelope validator."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
import re
from types import MappingProxyType
from typing import Any


class ResolvedFactState(str, Enum):
    CONFIRMED = "CONFIRMED"
    REFUTED = "REFUTED"
    UNAVAILABLE = "UNAVAILABLE"
    STALE = "STALE"
    CONTRADICTORY = "CONTRADICTORY"
    UNVERIFIABLE = "UNVERIFIABLE"


class ValidationState(str, Enum):
    CONFORMANT = "CONFORMANT"
    NONCONFORMANT = "NONCONFORMANT"
    INDETERMINATE = "INDETERMINATE"


class Disposition(str, Enum):
    PROCEED = "PROCEED"
    RETURN = "RETURN"
    WAIT = "WAIT"
    STOP = "STOP"
    ESCALATE = "ESCALATE"


class ReasonCode(str, Enum):
    VALIDATION_PASSED = "VALIDATION_PASSED"
    PUBLIC_INPUT_INVALID = "PUBLIC_INPUT_INVALID"
    VALIDATION_CONTEXT_INVALID = "VALIDATION_CONTEXT_INVALID"
    SCHEMA_BINDING_INVALID = "SCHEMA_BINDING_INVALID"
    SCHEMA_INTEGRITY_INVALID = "SCHEMA_INTEGRITY_INVALID"
    SCHEMA_DOCUMENT_INVALID = "SCHEMA_DOCUMENT_INVALID"
    ENVELOPE_SCHEMA_NONCONFORMANT = "ENVELOPE_SCHEMA_NONCONFORMANT"
    CONTRACT_IDENTITY_INVALID = "CONTRACT_IDENTITY_INVALID"
    PARTICIPANT_IDENTITY_INVALID = "PARTICIPANT_IDENTITY_INVALID"
    LINEAGE_INVALID = "LINEAGE_INVALID"
    AUTHORITY_REVOKED = "AUTHORITY_REVOKED"
    AUTHORITY_INVALID = "AUTHORITY_INVALID"
    AUTHORITY_STALE = "AUTHORITY_STALE"
    AUTHORITY_CONTRADICTORY = "AUTHORITY_CONTRADICTORY"
    AUTHORITY_UNVERIFIABLE = "AUTHORITY_UNVERIFIABLE"
    GOVERNING_SOURCE_UNVERIFIABLE = "GOVERNING_SOURCE_UNVERIFIABLE"
    SEMANTIC_AMBIGUITY_DETECTED = "SEMANTIC_AMBIGUITY_DETECTED"
    SEMANTIC_AMBIGUITY_UNRESOLVED = "SEMANTIC_AMBIGUITY_UNRESOLVED"
    POLICY_UNVERIFIABLE = "POLICY_UNVERIFIABLE"
    EVIDENCE_UNVERIFIABLE = "EVIDENCE_UNVERIFIABLE"
    TIME_INVALID = "TIME_INVALID"
    CONSEQUENCE_INVALID = "CONSEQUENCE_INVALID"
    CONFIDENTIALITY_INVALID = "CONFIDENTIALITY_INVALID"
    INTEGRITY_INVALID = "INTEGRITY_INVALID"
    IDEMPOTENCY_ORDERING_INVALID = "IDEMPOTENCY_ORDERING_INVALID"
    LIFECYCLE_INVALID = "LIFECYCLE_INVALID"
    RETURN_PATH_INVALID = "RETURN_PATH_INVALID"
    MATERIAL_CONDITION_UNDEFINED = "MATERIAL_CONDITION_UNDEFINED"


@dataclass(frozen=True)
class EvaluatedCheck:
    precedence_step: int
    check_name: str
    outcome: str
    reason_codes: tuple[ReasonCode, ...]
    evidence_references: tuple[str, ...]


@dataclass(frozen=True)
class TransitionEnvelopeValidationResult:
    validation_id: str
    contract_name: str
    contract_version: str
    transition_id: str
    correlation_id: str
    schema_checkpoint: str
    schema_blob: str
    passage_consumption_reference: str
    passage_exhaustion_reference: str
    evaluated_at_utc: str
    validation_state: ValidationState
    disposition: Disposition
    reason_codes: tuple[ReasonCode, ...]
    evaluated_checks: tuple[EvaluatedCheck, ...]
    evidence_references: tuple[str, ...]
    unresolved_conditions: tuple[str, ...]
    authority_exercised: tuple[str, ...]
    authority_excluded: tuple[str, ...]
    source_provenance: tuple[str, ...]
    continuation_posture: str


_SCHEMA_REPOSITORY = "heliosfi/heliosfi-ni-ai-spine"
_SCHEMA_PATH = "schemas/ni-ai-transition-envelope.schema.json"
_SCHEMA_CHECKPOINT = "6fe29594b4b5c7e4ceea1907c87cc7049e9a0e80"
_SCHEMA_BLOB = "acfe2dc5c4bd722163b123545fbf41a09fa2509d"
_CONTRACT_NAME = "NI AI Transition Envelope"
_CONTRACT_VERSION = "1.0.0"
_CONTEXT_FIELDS = frozenset({
    "schema_document", "schema_repository", "schema_path", "schema_checkpoint",
    "schema_blob", "trusted_evaluation_time_utc", "validation_id",
    "passage_consumption_reference", "passage_exhaustion_reference", "resolved_facts",
})
_FACT_NAMES = (
    "schema_integrity", "issuer_identity", "receiver_identity", "lineage_verifiability",
    "authority_currentness", "authority_attribution", "authority_scope",
    "authority_revocation", "authority_consistency", "authority_evidence_verifiability",
    "governing_source_verifiability", "semantic_correspondence",
    "policy_reference_verifiability", "evidence_reference_verifiability",
    "trusted_time_verifiability", "consequence_reference_verifiability",
    "confidentiality_verifiability", "integrity_proof_verifiability",
    "idempotency_replay_retry_ordering", "lifecycle_separation",
    "return_path_verifiability",
)
_CHECK_NAMES = (
    "PUBLIC_BOUNDARY", "CONTEXT_COMPLETENESS", "SCHEMA_BINDING",
    "SCHEMA_INTEGRITY_DOCUMENT", "ENVELOPE_STRUCTURE",
    "CONTRACT_PARTICIPANT_LINEAGE_IDENTITY", "REVOCATION",
    "AUTHORITY_CONTRADICTION", "AUTHORITY_INVALIDITY", "AUTHORITY_UNAVAILABLE",
    "GOVERNING_SOURCE", "SEMANTIC_CORRESPONDENCE", "POLICY_EVIDENCE",
    "TIME_CONSEQUENCE", "CONFIDENTIALITY_INTEGRITY", "IDEMPOTENCY_ORDERING",
    "LIFECYCLE_RETURN", "OTHER_MATERIAL_CONDITION", "SUCCESS",
)
_EXCLUDED = ("DISPATCH", "PERMISSION_ENFORCEMENT", "EXECUTION", "ACCEPTANCE", "CONTINUATION")
_UNAVAILABLE = {ResolvedFactState.UNAVAILABLE, ResolvedFactState.STALE, ResolvedFactState.UNVERIFIABLE}
_SCHEMA_TYPES = frozenset({"array", "boolean", "integer", "object", "string"})
_SCHEMA_FORMATS = frozenset({"date-time", "uuid"})
_UUID_PATTERN = re.compile(
    r"^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-"
    r"[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$"
)
_RFC3339_UTC_PATTERN = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T"
    r"[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?Z$"
)
_SCHEMA_KEYWORDS = frozenset({
    "$defs", "$id", "$ref", "$schema", "additionalProperties", "allOf", "const",
    "description", "else", "enum", "format", "if", "items", "minItems",
    "minLength", "not", "pattern", "properties", "required", "then", "title",
    "type", "uniqueItems",
})


def _is_deeply_immutable_json(value: object, active: set[int] | None = None) -> bool:
    if value is None or isinstance(value, (str, int, float, bool)):
        return not isinstance(value, float) or value == value and abs(value) != float("inf")
    if active is None:
        active = set()
    identity = id(value)
    if identity in active:
        return False
    active.add(identity)
    try:
        if isinstance(value, MappingProxyType):
            return all(isinstance(k, str) and _is_deeply_immutable_json(v, active) for k, v in value.items())
        if isinstance(value, tuple):
            return all(_is_deeply_immutable_json(v, active) for v in value)
        return False
    finally:
        active.remove(identity)


def _utc(value: object) -> datetime | None:
    if not isinstance(value, str) or _RFC3339_UTC_PATTERN.fullmatch(value) is None:
        return None
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return None
    return parsed if parsed.tzinfo == timezone.utc else None


def _unique_strings(values: Any) -> tuple[str, ...]:
    if not isinstance(values, (tuple, list)):
        return ()
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if isinstance(value, str) and value and value not in seen:
            seen.add(value)
            result.append(value)
    return tuple(result)


def _evidence(envelope: Mapping[str, Any]) -> tuple[str, ...]:
    values: list[str] = []
    governing = envelope.get("governingConditions", {})
    native = envelope.get("nativeResult", {})
    returned = envelope.get("returnedLearning", {})
    for collection in (
        governing.get("requiredEvidence", ()) if isinstance(governing, Mapping) else (),
        native.get("evidenceReferences", ()) if isinstance(native, Mapping) else (),
        returned.get("evidenceReferences", ()) if isinstance(returned, Mapping) else (),
    ):
        for item in collection if isinstance(collection, (tuple, list)) else ():
            if isinstance(item, Mapping):
                values.append(item.get("reference", ""))
    return _unique_strings(values)


def _provenance(envelope: Mapping[str, Any]) -> tuple[str, ...]:
    subject = envelope.get("transitionSubject", {})
    returned = envelope.get("returnedLearning", {})
    values = [_SCHEMA_REPOSITORY, _SCHEMA_PATH, _SCHEMA_CHECKPOINT, _SCHEMA_BLOB]
    if isinstance(subject, Mapping):
        values.append(subject.get("governingSource", ""))
    if isinstance(returned, Mapping):
        values.extend(returned.get("sourceProvenanceReferences", ()))
    return _unique_strings(values)


def _json_equal(left: object, right: object) -> bool:
    """Compare immutable JSON values without representation or ordering assumptions."""
    if isinstance(left, bool) or isinstance(right, bool):
        return isinstance(left, bool) and isinstance(right, bool) and left == right
    if isinstance(left, (int, float)) or isinstance(right, (int, float)):
        return (isinstance(left, (int, float)) and not isinstance(left, bool)
                and isinstance(right, (int, float)) and not isinstance(right, bool)
                and left == right)
    if isinstance(left, Mapping) or isinstance(right, Mapping):
        if not isinstance(left, Mapping) or not isinstance(right, Mapping):
            return False
        return (set(left) == set(right)
                and all(_json_equal(left[key], right[key]) for key in left))
    if isinstance(left, (tuple, list)) or isinstance(right, (tuple, list)):
        if not isinstance(left, (tuple, list)) or not isinstance(right, (tuple, list)):
            return False
        return len(left) == len(right) and all(
            _json_equal(left_item, right_item)
            for left_item, right_item in zip(left, right)
        )
    return type(left) is type(right) and left == right


def _schema_valid(instance: Any, schema: Mapping[str, Any], root: Mapping[str, Any]) -> bool:
    if "$ref" in schema:
        reference = schema["$ref"]
        if not isinstance(reference, str) or not reference.startswith("#/"):
            return False
        target: Any = root
        for part in reference[2:].split("/"):
            if not isinstance(target, Mapping) or part not in target:
                return False
            target = target[part]
        return isinstance(target, Mapping) and _schema_valid(instance, target, root)
    if "allOf" in schema and not all(_schema_valid(instance, item, root) for item in schema["allOf"]):
        return False
    if "if" in schema:
        branch = "then" if _schema_valid(instance, schema["if"], root) else "else"
        if branch in schema and not _schema_valid(instance, schema[branch], root):
            return False
    if "not" in schema and _schema_valid(instance, schema["not"], root):
        return False
    if "const" in schema and not _json_equal(instance, schema["const"]):
        return False
    if "enum" in schema and not any(_json_equal(instance, value)
                                    for value in schema["enum"]):
        return False
    expected = schema.get("type")
    if expected == "object" and not isinstance(instance, Mapping):
        return False
    if expected == "array" and not isinstance(instance, (tuple, list)):
        return False
    if expected == "string" and not isinstance(instance, str):
        return False
    if expected == "boolean" and not isinstance(instance, bool):
        return False
    if expected == "integer" and (not isinstance(instance, int) or isinstance(instance, bool)):
        return False
    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            return False
        if "pattern" in schema and re.search(schema["pattern"], instance) is None:
            return False
        if schema.get("format") == "uuid" and _UUID_PATTERN.fullmatch(instance) is None:
            return False
        if schema.get("format") == "date-time" and _utc(instance) is None:
            return False
    if isinstance(instance, Mapping):
        required = schema.get("required", ())
        if any(key not in instance for key in required):
            return False
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False and any(key not in properties for key in instance):
            return False
        for key, subschema in properties.items():
            if key in instance and not _schema_valid(instance[key], subschema, root):
                return False
    if isinstance(instance, (tuple, list)):
        if len(instance) < schema.get("minItems", 0):
            return False
        if schema.get("uniqueItems"):
            if any(_json_equal(value, prior)
                   for index, value in enumerate(instance)
                   for prior in instance[:index]):
                return False
        if "items" in schema and any(not _schema_valid(value, schema["items"], root) for value in instance):
            return False
    return True


def _schema_document_valid(schema: object) -> bool:
    """Fail closed unless the document is a valid supported Draft 2020-12 schema."""
    if not isinstance(schema, Mapping):
        return False
    root = schema
    active: set[int] = set()

    def unique(values: tuple[Any, ...]) -> bool:
        return all(not any(_json_equal(value, prior) for prior in values[:index])
                   for index, value in enumerate(values))

    def local_reference_exists(reference: object) -> bool:
        if not isinstance(reference, str) or not reference.startswith("#/"):
            return False
        target: object = root
        for encoded in reference[2:].split("/"):
            part = encoded.replace("~1", "/").replace("~0", "~")
            if not isinstance(target, Mapping) or part not in target:
                return False
            target = target[part]
        return isinstance(target, Mapping)

    def valid(candidate: object) -> bool:
        if not isinstance(candidate, Mapping):
            return False
        identity = id(candidate)
        if identity in active:
            return False
        active.add(identity)
        try:
            if any(key not in _SCHEMA_KEYWORDS and not key.startswith("x-")
                   for key in candidate):
                return False
            for key in ("$schema", "$id", "title", "description"):
                if key in candidate and not isinstance(candidate[key], str):
                    return False
            if "$ref" in candidate and not local_reference_exists(candidate["$ref"]):
                return False
            if "type" in candidate and candidate["type"] not in _SCHEMA_TYPES:
                return False
            if "format" in candidate and candidate["format"] not in _SCHEMA_FORMATS:
                return False
            if "pattern" in candidate:
                if not isinstance(candidate["pattern"], str):
                    return False
                try:
                    re.compile(candidate["pattern"])
                except re.error:
                    return False
            for key in ("minLength", "minItems"):
                value = candidate.get(key)
                if key in candidate and (not isinstance(value, int)
                                         or isinstance(value, bool) or value < 0):
                    return False
            for key in ("uniqueItems",):
                if key in candidate and not isinstance(candidate[key], bool):
                    return False
            if "additionalProperties" in candidate:
                additional = candidate["additionalProperties"]
                if not isinstance(additional, bool) and not valid(additional):
                    return False
            if "required" in candidate:
                required = candidate["required"]
                if (not isinstance(required, tuple) or not required
                        or not all(isinstance(item, str) and item for item in required)
                        or len(required) != len(set(required))):
                    return False
            for key in ("properties", "$defs"):
                if key in candidate:
                    members = candidate[key]
                    if (not isinstance(members, Mapping)
                            or not all(isinstance(name, str) and name and valid(member)
                                       for name, member in members.items())):
                        return False
            for key in ("if", "then", "else", "not", "items"):
                if key in candidate and not valid(candidate[key]):
                    return False
            if "allOf" in candidate:
                clauses = candidate["allOf"]
                if not isinstance(clauses, tuple) or not clauses or not all(valid(item) for item in clauses):
                    return False
            if "enum" in candidate:
                values = candidate["enum"]
                if not isinstance(values, tuple) or not values or not unique(values):
                    return False
            return True
        finally:
            active.remove(identity)

    return valid(schema)


def _result(
    envelope: Mapping[str, Any], context: Mapping[str, Any], checks: list[EvaluatedCheck],
    state: ValidationState, disposition: Disposition, reason: ReasonCode,
    unresolved: tuple[str, ...] = (),
) -> TransitionEnvelopeValidationResult:
    def text(source: Mapping[str, Any], key: str) -> str:
        value = source.get(key, "")
        return value if isinstance(value, str) else ""
    continuation = "STOP" if disposition is Disposition.STOP else "WAIT_FOR_SEPARATE_AUTHORITY"
    return TransitionEnvelopeValidationResult(
        text(context, "validation_id"), text(envelope, "contractName"),
        text(envelope, "contractVersion"), text(envelope, "transitionId"),
        text(envelope, "correlationId"), text(context, "schema_checkpoint"),
        text(context, "schema_blob"), text(context, "passage_consumption_reference"),
        text(context, "passage_exhaustion_reference"), text(context, "trusted_evaluation_time_utc"),
        state, disposition, (reason,), tuple(checks), _evidence(envelope), unresolved, (),
        _EXCLUDED, _provenance(envelope), continuation,
    )


def validate_transition_envelope(
    envelope: object,
    validation_context: object,
) -> TransitionEnvelopeValidationResult:
    """Validate one immutable envelope using only immutable caller-supplied facts."""
    safe_envelope = envelope if isinstance(envelope, Mapping) else MappingProxyType({})
    safe_context = validation_context if isinstance(validation_context, Mapping) else MappingProxyType({})
    checks: list[EvaluatedCheck] = []

    def passed(step: int) -> None:
        references: tuple[str, ...] = ()
        if step >= 3:
            context_references = _unique_strings((
                safe_context.get("schema_repository", ""), safe_context.get("schema_path", ""),
                safe_context.get("schema_checkpoint", ""), safe_context.get("schema_blob", ""),
            ))
            references = (_unique_strings((*_evidence(safe_envelope), *context_references))
                          if step >= 5 else context_references)
        checks.append(EvaluatedCheck(step, _CHECK_NAMES[step - 1], "PASSED", (), references))

    def finish(step: int, state: ValidationState, disposition: Disposition,
               reason: ReasonCode, unresolved: tuple[str, ...] = ()) -> TransitionEnvelopeValidationResult:
        outcome = "INDETERMINATE" if state is ValidationState.INDETERMINATE else "FAILED"
        checks.append(EvaluatedCheck(step, _CHECK_NAMES[step - 1], outcome, (reason,), _evidence(safe_envelope)))
        return _result(safe_envelope, safe_context, checks, state, disposition, reason, unresolved)

    if not _is_deeply_immutable_json(envelope) or not _is_deeply_immutable_json(validation_context):
        return finish(1, ValidationState.NONCONFORMANT, Disposition.STOP, ReasonCode.PUBLIC_INPUT_INVALID)
    passed(1)
    if (set(safe_context) != _CONTEXT_FIELDS
            or not all(isinstance(safe_context.get(key), str) and safe_context[key] for key in _CONTEXT_FIELDS - {"schema_document", "resolved_facts"})
            or _utc(safe_context.get("trusted_evaluation_time_utc")) is None
            or not isinstance(safe_context.get("resolved_facts"), Mapping)
            or set(safe_context["resolved_facts"]) != set(_FACT_NAMES)):
        return finish(2, ValidationState.NONCONFORMANT, Disposition.STOP, ReasonCode.VALIDATION_CONTEXT_INVALID)
    try:
        facts = {name: ResolvedFactState(safe_context["resolved_facts"][name]) for name in _FACT_NAMES}
    except (ValueError, TypeError):
        return finish(2, ValidationState.NONCONFORMANT, Disposition.STOP, ReasonCode.VALIDATION_CONTEXT_INVALID)
    passed(2)
    if any((safe_context["schema_repository"] != _SCHEMA_REPOSITORY,
            safe_context["schema_path"] != _SCHEMA_PATH,
            safe_context["schema_checkpoint"] != _SCHEMA_CHECKPOINT,
            safe_context["schema_blob"] != _SCHEMA_BLOB)):
        return finish(3, ValidationState.NONCONFORMANT, Disposition.STOP, ReasonCode.SCHEMA_BINDING_INVALID)
    passed(3)
    schema = safe_context["schema_document"]
    if facts["schema_integrity"] is ResolvedFactState.REFUTED:
        return finish(4, ValidationState.NONCONFORMANT, Disposition.STOP, ReasonCode.SCHEMA_INTEGRITY_INVALID)
    if facts["schema_integrity"] in _UNAVAILABLE or facts["schema_integrity"] is ResolvedFactState.CONTRADICTORY:
        return finish(4, ValidationState.INDETERMINATE, Disposition.WAIT, ReasonCode.SCHEMA_INTEGRITY_INVALID, ("schema_integrity",))
    if (not isinstance(schema, Mapping)
            or schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema"
            or schema.get("title") != _CONTRACT_NAME
            or not isinstance(schema.get("$defs"), Mapping)
            or not _schema_document_valid(schema)):
        return finish(4, ValidationState.NONCONFORMANT, Disposition.STOP, ReasonCode.SCHEMA_DOCUMENT_INVALID)
    passed(4)
    if not _schema_valid(safe_envelope, schema, schema):
        return finish(5, ValidationState.NONCONFORMANT, Disposition.RETURN, ReasonCode.ENVELOPE_SCHEMA_NONCONFORMANT)
    passed(5)
    if safe_envelope.get("contractName") != _CONTRACT_NAME or safe_envelope.get("contractVersion") != _CONTRACT_VERSION:
        return finish(6, ValidationState.NONCONFORMANT, Disposition.STOP, ReasonCode.CONTRACT_IDENTITY_INVALID)
    identity_states = (facts["issuer_identity"], facts["receiver_identity"])
    if ResolvedFactState.CONTRADICTORY in identity_states:
        return finish(6, ValidationState.INDETERMINATE, Disposition.ESCALATE, ReasonCode.PARTICIPANT_IDENTITY_INVALID, ("participant_identity",))
    if ResolvedFactState.REFUTED in identity_states:
        return finish(6, ValidationState.NONCONFORMANT, Disposition.STOP, ReasonCode.PARTICIPANT_IDENTITY_INVALID)
    if any(value in _UNAVAILABLE for value in identity_states):
        return finish(6, ValidationState.INDETERMINATE, Disposition.WAIT, ReasonCode.PARTICIPANT_IDENTITY_INVALID, ("participant_identity",))
    lineage = facts["lineage_verifiability"]
    if lineage is ResolvedFactState.REFUTED:
        return finish(6, ValidationState.NONCONFORMANT, Disposition.STOP, ReasonCode.LINEAGE_INVALID)
    if lineage is ResolvedFactState.CONTRADICTORY:
        return finish(6, ValidationState.INDETERMINATE, Disposition.ESCALATE, ReasonCode.LINEAGE_INVALID, ("lineage_verifiability",))
    if lineage in _UNAVAILABLE:
        return finish(6, ValidationState.INDETERMINATE, Disposition.WAIT, ReasonCode.LINEAGE_INVALID, ("lineage_verifiability",))
    passed(6)
    revocation = facts["authority_revocation"]
    if revocation is ResolvedFactState.CONFIRMED:
        return finish(7, ValidationState.NONCONFORMANT, Disposition.STOP, ReasonCode.AUTHORITY_REVOKED)
    if revocation is ResolvedFactState.CONTRADICTORY:
        return finish(7, ValidationState.INDETERMINATE, Disposition.ESCALATE, ReasonCode.AUTHORITY_CONTRADICTORY, ("authority_revocation",))
    if revocation in _UNAVAILABLE:
        return finish(7, ValidationState.INDETERMINATE, Disposition.WAIT, ReasonCode.AUTHORITY_UNVERIFIABLE, ("authority_revocation",))
    passed(7)
    authority = ("authority_currentness", "authority_attribution", "authority_scope",
                 "authority_consistency", "authority_evidence_verifiability")
    contradictory_authority = (*authority, "governing_source_verifiability")
    if any(facts[name] is ResolvedFactState.CONTRADICTORY for name in contradictory_authority):
        return finish(8, ValidationState.INDETERMINATE, Disposition.ESCALATE,
                      ReasonCode.AUTHORITY_CONTRADICTORY,
                      tuple(name for name in contradictory_authority
                            if facts[name] is ResolvedFactState.CONTRADICTORY))
    passed(8)
    if any(facts[name] is ResolvedFactState.REFUTED for name in authority):
        return finish(9, ValidationState.NONCONFORMANT, Disposition.STOP, ReasonCode.AUTHORITY_INVALID)
    passed(9)
    if facts["authority_currentness"] is ResolvedFactState.STALE:
        return finish(10, ValidationState.INDETERMINATE, Disposition.WAIT, ReasonCode.AUTHORITY_STALE, ("authority_currentness",))
    unavailable_authority = tuple(name for name in authority if facts[name] in _UNAVAILABLE)
    if unavailable_authority:
        return finish(10, ValidationState.INDETERMINATE, Disposition.WAIT, ReasonCode.AUTHORITY_UNVERIFIABLE, unavailable_authority)
    passed(10)
    governing = facts["governing_source_verifiability"]
    if governing is ResolvedFactState.REFUTED:
        return finish(11, ValidationState.NONCONFORMANT, Disposition.RETURN, ReasonCode.GOVERNING_SOURCE_UNVERIFIABLE)
    if governing in _UNAVAILABLE:
        return finish(11, ValidationState.INDETERMINATE, Disposition.WAIT, ReasonCode.GOVERNING_SOURCE_UNVERIFIABLE, ("governing_source_verifiability",))
    passed(11)
    semantic = safe_envelope.get("semanticCorrespondence", {})
    ambiguity = semantic.get("ambiguityState") if isinstance(semantic, Mapping) else None
    if ambiguity == "DETECTED":
        return finish(12, ValidationState.INDETERMINATE, Disposition.ESCALATE, ReasonCode.SEMANTIC_AMBIGUITY_DETECTED, ("semantic_correspondence",))
    if ambiguity == "UNRESOLVED" or facts["semantic_correspondence"] is ResolvedFactState.CONTRADICTORY:
        return finish(12, ValidationState.INDETERMINATE, Disposition.ESCALATE, ReasonCode.SEMANTIC_AMBIGUITY_UNRESOLVED, ("semantic_correspondence",))
    if facts["semantic_correspondence"] is ResolvedFactState.REFUTED:
        return finish(12, ValidationState.NONCONFORMANT, Disposition.RETURN, ReasonCode.SEMANTIC_AMBIGUITY_UNRESOLVED)
    if facts["semantic_correspondence"] in _UNAVAILABLE:
        return finish(12, ValidationState.INDETERMINATE, Disposition.WAIT, ReasonCode.SEMANTIC_AMBIGUITY_UNRESOLVED, ("semantic_correspondence",))
    passed(12)
    for name, reason in (("policy_reference_verifiability", ReasonCode.POLICY_UNVERIFIABLE),
                         ("evidence_reference_verifiability", ReasonCode.EVIDENCE_UNVERIFIABLE)):
        if facts[name] is ResolvedFactState.REFUTED:
            return finish(13, ValidationState.NONCONFORMANT, Disposition.RETURN, reason)
        if facts[name] is ResolvedFactState.CONTRADICTORY:
            return finish(13, ValidationState.INDETERMINATE, Disposition.ESCALATE, reason, (name,))
        if facts[name] in _UNAVAILABLE:
            return finish(13, ValidationState.INDETERMINATE, Disposition.WAIT, reason, (name,))
    passed(13)
    for name, reason in (("trusted_time_verifiability", ReasonCode.TIME_INVALID),
                         ("consequence_reference_verifiability", ReasonCode.CONSEQUENCE_INVALID)):
        if facts[name] is ResolvedFactState.REFUTED:
            return finish(14, ValidationState.NONCONFORMANT, Disposition.RETURN, reason)
        if facts[name] is ResolvedFactState.CONTRADICTORY:
            return finish(14, ValidationState.INDETERMINATE, Disposition.ESCALATE, reason, (name,))
        if facts[name] in _UNAVAILABLE:
            return finish(14, ValidationState.INDETERMINATE, Disposition.WAIT, reason, (name,))
    validity = safe_envelope.get("validityBoundary", {})
    now = _utc(safe_context["trusted_evaluation_time_utc"])
    before = _utc(validity.get("notBefore")) if isinstance(validity, Mapping) else None
    after = _utc(validity.get("notAfter")) if isinstance(validity, Mapping) else None
    if now is None or before is None or after is None or before > after or not before <= now <= after:
        return finish(14, ValidationState.NONCONFORMANT, Disposition.RETURN, ReasonCode.TIME_INVALID)
    passed(14)
    for name, reason in (("confidentiality_verifiability", ReasonCode.CONFIDENTIALITY_INVALID),
                         ("integrity_proof_verifiability", ReasonCode.INTEGRITY_INVALID)):
        if facts[name] is ResolvedFactState.REFUTED:
            return finish(15, ValidationState.NONCONFORMANT, Disposition.STOP, reason)
        if facts[name] is ResolvedFactState.CONTRADICTORY:
            return finish(15, ValidationState.INDETERMINATE, Disposition.ESCALATE, reason, (name,))
        if facts[name] in _UNAVAILABLE:
            return finish(15, ValidationState.INDETERMINATE, Disposition.WAIT, reason, (name,))
    passed(15)
    ordering = facts["idempotency_replay_retry_ordering"]
    if ordering is ResolvedFactState.REFUTED:
        return finish(16, ValidationState.NONCONFORMANT, Disposition.RETURN, ReasonCode.IDEMPOTENCY_ORDERING_INVALID)
    if ordering is ResolvedFactState.CONTRADICTORY:
        return finish(16, ValidationState.INDETERMINATE, Disposition.ESCALATE, ReasonCode.IDEMPOTENCY_ORDERING_INVALID, ("idempotency_replay_retry_ordering",))
    if ordering in _UNAVAILABLE:
        return finish(16, ValidationState.INDETERMINATE, Disposition.WAIT, ReasonCode.IDEMPOTENCY_ORDERING_INVALID, ("idempotency_replay_retry_ordering",))
    passed(16)
    for name, reason in (("lifecycle_separation", ReasonCode.LIFECYCLE_INVALID),
                         ("return_path_verifiability", ReasonCode.RETURN_PATH_INVALID)):
        if facts[name] is ResolvedFactState.REFUTED:
            return finish(17, ValidationState.NONCONFORMANT, Disposition.RETURN, reason)
        if facts[name] is ResolvedFactState.CONTRADICTORY:
            return finish(17, ValidationState.INDETERMINATE, Disposition.ESCALATE, reason, (name,))
        if facts[name] in _UNAVAILABLE:
            return finish(17, ValidationState.INDETERMINATE, Disposition.WAIT, reason, (name,))
    passed(17)
    remaining = tuple(name for name in _FACT_NAMES if facts[name] is not ResolvedFactState.CONFIRMED
                      and not (name == "authority_revocation" and facts[name] is ResolvedFactState.REFUTED))
    if remaining:
        return finish(18, ValidationState.INDETERMINATE, Disposition.WAIT, ReasonCode.MATERIAL_CONDITION_UNDEFINED, remaining)
    passed(18)
    success_evidence = _unique_strings((
        *_evidence(safe_envelope), safe_context["schema_repository"],
        safe_context["schema_path"], safe_context["schema_checkpoint"],
        safe_context["schema_blob"],
    ))
    checks.append(EvaluatedCheck(19, _CHECK_NAMES[18], "PASSED",
                                 (ReasonCode.VALIDATION_PASSED,), success_evidence))
    return _result(safe_envelope, safe_context, checks, ValidationState.CONFORMANT,
                   Disposition.PROCEED, ReasonCode.VALIDATION_PASSED)
