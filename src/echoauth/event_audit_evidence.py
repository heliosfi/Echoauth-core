"""Validation-only event audit evidence packaging for Sprint 2X."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from echoauth.canonical import canonical_sha256
from echoauth.events import (
    EventAcceptanceResult,
    EventDeliveryState,
    EventEnvelope,
)

EVENT_AUDIT_EVIDENCE_VERSION = "echoauth.event-audit-evidence.v1"
_EVIDENCE_STATES = frozenset(
    {EventDeliveryState.ACCEPTED, EventDeliveryState.REJECTED}
)


@dataclass(frozen=True)
class EventAuditEvidence:
    """Immutable evidence of event acceptance or rejection.

    This artifact does not represent an appended audit record, persistence,
    delivery, replay, signing, or authorization.
    """

    event_id: str | None
    event_type: str | None
    producer_id: str | None
    correlation_id: str | None
    occurred_at: str | None
    delivery_state: EventDeliveryState
    reason: str
    payload_hash: str | None
    evidence_hash: str


class EventAuditEvidenceError(ValueError):
    """Raised when acceptance evidence cannot be bound safely."""


class EventAuditEvidencePackager:
    """Package deterministic evidence without causing operational effects."""

    def package(
        self,
        event: EventEnvelope | Mapping[str, object],
        acceptance: EventAcceptanceResult,
    ) -> EventAuditEvidence:
        """Bind available event metadata to an acceptance or rejection result."""

        if not isinstance(acceptance, EventAcceptanceResult):
            raise EventAuditEvidenceError("invalid_acceptance_result")
        if acceptance.delivery_state not in _EVIDENCE_STATES:
            raise EventAuditEvidenceError("unsupported_delivery_state")
        if not isinstance(acceptance.reason, str) or not acceptance.reason:
            raise EventAuditEvidenceError("invalid_acceptance_reason")

        fields = _available_fields(event)
        event_id = _bind_identifier(
            fields["event_id"],
            acceptance.event_id,
            "event_id",
        )
        event_type = _bind_identifier(
            fields["event_type"],
            acceptance.event_type,
            "event_type",
        )
        if acceptance.delivery_state is EventDeliveryState.ACCEPTED:
            required = (
                event_id,
                event_type,
                fields["producer_id"],
                fields["correlation_id"],
                fields["occurred_at"],
            )
            if any(value is None for value in required):
                raise EventAuditEvidenceError("incomplete_accepted_event_evidence")

        material = {
            "delivery_state": acceptance.delivery_state.value,
            "event_id": event_id,
            "event_type": event_type,
            "format_version": EVENT_AUDIT_EVIDENCE_VERSION,
            "occurred_at": fields["occurred_at"],
            "payload_hash": _optional_string(acceptance.payload_hash),
            "producer_id": fields["producer_id"],
            "correlation_id": fields["correlation_id"],
            "reason": acceptance.reason,
        }
        return EventAuditEvidence(
            event_id=event_id,
            event_type=event_type,
            producer_id=fields["producer_id"],
            correlation_id=fields["correlation_id"],
            occurred_at=fields["occurred_at"],
            delivery_state=acceptance.delivery_state,
            reason=acceptance.reason,
            payload_hash=_optional_string(acceptance.payload_hash),
            evidence_hash=canonical_sha256(material),
        )


def _available_fields(
    event: EventEnvelope | Mapping[str, object],
) -> dict[str, str | None]:
    if isinstance(event, EventEnvelope):
        return {
            "event_id": _optional_string(event.event_id),
            "event_type": _optional_string(event.event_type),
            "producer_id": _optional_string(event.producer_id),
            "correlation_id": _optional_string(event.correlation_id),
            "occurred_at": _optional_string(event.occurred_at),
        }
    if isinstance(event, Mapping):
        return {
            field: _optional_string(event.get(field))
            for field in (
                "event_id",
                "event_type",
                "producer_id",
                "correlation_id",
                "occurred_at",
            )
        }
    raise EventAuditEvidenceError("invalid_event_candidate")


def _bind_identifier(
    event_value: str | None,
    result_value: object,
    field: str,
) -> str | None:
    result = _optional_string(result_value)
    if event_value is not None and result is not None and event_value != result:
        raise EventAuditEvidenceError(f"{field}_mismatch")
    return result if result is not None else event_value


def _optional_string(value: object) -> str | None:
    return value if isinstance(value, str) and value else None
