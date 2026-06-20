"""Validation-only event correlation and causation evidence for Sprint 2W."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum

from echoauth.canonical import canonical_sha256
from echoauth.events import EventEnvelope
from echoauth.events_validation import EventValidationError, validate_event_envelope

EVENT_CORRELATION_VERSION = "echoauth.event-correlation.v1"
_CATALOG_ONLY_EVENT_TYPES = frozenset({"runtime.recovered"})


class CausationEvidenceState(str, Enum):
    ABSENT = "absent"
    RESOLVED = "resolved"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True)
class EventCorrelationEvidence:
    """Explicit correlation and causation evidence for one event."""

    event_id: str
    correlation_id: str
    causation_id: str | None
    causation_state: CausationEvidenceState


@dataclass(frozen=True)
class CorrelationGroupEvidence:
    """Deterministic packaging of events sharing an explicit correlation ID."""

    correlation_id: str
    event_ids: tuple[str, ...]


@dataclass(frozen=True)
class EventCorrelationResult:
    """Evidence-only batch result with no tracing or delivery effects."""

    valid: bool
    reason: str
    correlation_groups: tuple[CorrelationGroupEvidence, ...]
    event_evidence: tuple[EventCorrelationEvidence, ...]
    unresolved_causation_ids: tuple[str, ...]
    evidence_hash: str


class EventCorrelationValidator:
    """Validate explicit event relationships without inferring causation."""

    def validate(
        self,
        events: Sequence[EventEnvelope | Mapping[str, object]],
    ) -> EventCorrelationResult:
        if isinstance(events, (str, bytes)) or not isinstance(events, Sequence):
            return _rejected("events_must_be_ordered", ())

        validated: list[dict[str, object]] = []
        event_ids: list[str] = []
        for event in events:
            try:
                data = validate_event_envelope(event)
            except EventValidationError:
                return _rejected("invalid_event_envelope", tuple(event_ids))
            event_id = data["event_id"]
            event_type = data["event_type"]
            correlation_id = data["correlation_id"]
            causation_id = data.get("causation_id")
            if not isinstance(event_id, str) or not event_id:
                return _rejected("malformed_event_id", tuple(event_ids))
            if not isinstance(correlation_id, str) or not correlation_id:
                return _rejected(
                    "malformed_correlation_id",
                    tuple(event_ids + [event_id]),
                )
            if causation_id is not None and (
                not isinstance(causation_id, str) or not causation_id
            ):
                return _rejected(
                    "malformed_causation_id",
                    tuple(event_ids + [event_id]),
                )
            if event_type in _CATALOG_ONLY_EVENT_TYPES:
                return _rejected(
                    "catalog_only_event_type",
                    tuple(event_ids + [event_id]),
                )
            event_ids.append(event_id)
            validated.append(data)

        if len(set(event_ids)) != len(event_ids):
            return _rejected("duplicate_event_id", tuple(event_ids))

        available_ids = frozenset(event_ids)
        groups: dict[str, list[str]] = {}
        evidence: list[EventCorrelationEvidence] = []
        unresolved: set[str] = set()
        for data in validated:
            event_id = str(data["event_id"])
            correlation_id = str(data["correlation_id"])
            causation_id = data.get("causation_id")
            groups.setdefault(correlation_id, []).append(event_id)
            if causation_id is None:
                state = CausationEvidenceState.ABSENT
            elif causation_id == event_id:
                return _rejected("causation_self_reference", tuple(event_ids))
            elif causation_id in available_ids:
                state = CausationEvidenceState.RESOLVED
            else:
                state = CausationEvidenceState.UNRESOLVED
                unresolved.add(str(causation_id))
            evidence.append(
                EventCorrelationEvidence(
                    event_id=event_id,
                    correlation_id=correlation_id,
                    causation_id=str(causation_id) if causation_id is not None else None,
                    causation_state=state,
                )
            )

        correlation_groups = tuple(
            CorrelationGroupEvidence(
                correlation_id=correlation_id,
                event_ids=tuple(sorted(groups[correlation_id])),
            )
            for correlation_id in sorted(groups)
        )
        event_evidence = tuple(sorted(evidence, key=lambda item: item.event_id))
        unresolved_ids = tuple(sorted(unresolved))
        reason = (
            "validated_with_unresolved_causation"
            if unresolved_ids
            else "validated"
        )
        evidence_hash = canonical_sha256(
            {
                "correlation_groups": [
                    {
                        "correlation_id": group.correlation_id,
                        "event_ids": list(group.event_ids),
                    }
                    for group in correlation_groups
                ],
                "event_evidence": [
                    {
                        "causation_id": item.causation_id,
                        "causation_state": item.causation_state.value,
                        "correlation_id": item.correlation_id,
                        "event_id": item.event_id,
                    }
                    for item in event_evidence
                ],
                "format_version": EVENT_CORRELATION_VERSION,
                "reason": reason,
                "unresolved_causation_ids": list(unresolved_ids),
                "valid": True,
            }
        )
        return EventCorrelationResult(
            valid=True,
            reason=reason,
            correlation_groups=correlation_groups,
            event_evidence=event_evidence,
            unresolved_causation_ids=unresolved_ids,
            evidence_hash=evidence_hash,
        )


def _rejected(reason: str, event_ids: tuple[str, ...]) -> EventCorrelationResult:
    evidence_hash = canonical_sha256(
        {
            "event_ids": list(event_ids),
            "format_version": EVENT_CORRELATION_VERSION,
            "reason": reason,
            "valid": False,
        }
    )
    return EventCorrelationResult(
        valid=False,
        reason=reason,
        correlation_groups=(),
        event_evidence=(),
        unresolved_causation_ids=(),
        evidence_hash=evidence_hash,
    )
