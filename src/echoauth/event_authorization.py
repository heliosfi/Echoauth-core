"""Validation-only event producer authorization for Sprint 2R.

Configured evidence is local and hash-bound. This module does not authenticate
externally, publish events, authorize subscribers, or provide delivery effects.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path

from echoauth.canonical import canonical_sha256
from echoauth.events import (
    EventAcceptanceResult,
    EventDeliveryState,
    EventEnvelope,
    InProcessEventAcceptance,
)
from echoauth.events_validation import load_event_catalog

PRODUCER_AUTHORIZATION_VERSION = "echoauth.event-producer-authorization.v1"
_CATALOG_ONLY_EVENT_TYPES = frozenset({"runtime.recovered"})


@dataclass(frozen=True)
class ProducerAuthorizationEvidence:
    """Explicit configured evidence for one producer and its event types."""

    authorization_id: str
    producer_id: str
    allowed_event_types: tuple[str, ...]
    evidence_hash: str


class EventProducerAuthorizationError(ValueError):
    """Raised when configured producer evidence is malformed or ambiguous."""


class AuthorizedEventAcceptance:
    """Require producer evidence before Sprint 2Q event acceptance."""

    def __init__(
        self,
        producer_evidence: Sequence[ProducerAuthorizationEvidence],
        *,
        catalog_path: str | Path = "events/event-catalog.yaml",
    ) -> None:
        catalog = load_event_catalog(catalog_path)
        self._producers = _validate_configured_evidence(producer_evidence, catalog)
        self._acceptance = InProcessEventAcceptance(catalog_path)

    def accept(
        self,
        event: EventEnvelope | Mapping[str, object],
    ) -> EventAcceptanceResult:
        """Fail closed unless the producer and event type are explicitly scoped."""

        producer_id, event_type = _event_identity(event)
        evidence = self._producers.get(producer_id) if producer_id else None
        if evidence is None:
            return _rejected(event, "unknown_producer")
        if isinstance(event_type, str) and event_type not in evidence.allowed_event_types:
            return _rejected(event, "producer_event_type_not_authorized")
        return self._acceptance.accept(event)


def producer_authorization_hash(evidence: ProducerAuthorizationEvidence) -> str:
    """Hash canonical producer evidence without its supplied evidence hash."""

    payload = asdict(evidence)
    payload.pop("evidence_hash")
    payload["allowed_event_types"] = sorted(evidence.allowed_event_types)
    payload["format_version"] = PRODUCER_AUTHORIZATION_VERSION
    return canonical_sha256(payload)


def _validate_configured_evidence(
    configured: Sequence[ProducerAuthorizationEvidence],
    catalog: Mapping[str, str],
) -> dict[str, ProducerAuthorizationEvidence]:
    if isinstance(configured, (str, bytes)) or not isinstance(configured, Sequence):
        raise EventProducerAuthorizationError("producer evidence must be ordered")
    producers: dict[str, ProducerAuthorizationEvidence] = {}
    authorization_ids: set[str] = set()
    for evidence in configured:
        if not isinstance(evidence, ProducerAuthorizationEvidence):
            raise EventProducerAuthorizationError(
                "configured producer evidence must be canonical"
            )
        for field_name in ("authorization_id", "producer_id", "evidence_hash"):
            value = getattr(evidence, field_name)
            if not isinstance(value, str) or not value:
                raise EventProducerAuthorizationError(
                    f"{field_name} must be a non-empty string"
                )
        if (
            not isinstance(evidence.allowed_event_types, tuple)
            or not evidence.allowed_event_types
            or any(
                not isinstance(event_type, str) or not event_type
                for event_type in evidence.allowed_event_types
            )
        ):
            raise EventProducerAuthorizationError(
                "allowed_event_types must be a non-empty string tuple"
            )
        if len(set(evidence.allowed_event_types)) != len(
            evidence.allowed_event_types
        ):
            raise EventProducerAuthorizationError(
                "allowed_event_types must be unique"
            )
        if any(event_type not in catalog for event_type in evidence.allowed_event_types):
            raise EventProducerAuthorizationError(
                "allowed_event_types must exist in the event catalog"
            )
        if _CATALOG_ONLY_EVENT_TYPES.intersection(evidence.allowed_event_types):
            raise EventProducerAuthorizationError(
                "catalog-only event types cannot be producer-authorized"
            )
        if producer_authorization_hash(evidence) != evidence.evidence_hash:
            raise EventProducerAuthorizationError(
                "producer authorization evidence hash mismatch"
            )
        if evidence.producer_id in producers:
            raise EventProducerAuthorizationError("producer_id must be unique")
        if evidence.authorization_id in authorization_ids:
            raise EventProducerAuthorizationError(
                "authorization_id must be unique"
            )
        producers[evidence.producer_id] = evidence
        authorization_ids.add(evidence.authorization_id)
    return producers


def _event_identity(
    event: EventEnvelope | Mapping[str, object],
) -> tuple[str | None, object | None]:
    if isinstance(event, EventEnvelope):
        producer_id = event.producer_id
        return (
            producer_id if isinstance(producer_id, str) and producer_id else None,
            event.event_type,
        )
    if isinstance(event, Mapping):
        producer_id = event.get("producer_id")
        return (
            producer_id if isinstance(producer_id, str) and producer_id else None,
            event.get("event_type"),
        )
    return None, None


def _rejected(
    event: EventEnvelope | Mapping[str, object],
    reason: str,
) -> EventAcceptanceResult:
    event_id: str | None = None
    event_type: str | None = None
    if isinstance(event, EventEnvelope):
        event_id = event.event_id if isinstance(event.event_id, str) else None
        event_type = event.event_type if isinstance(event.event_type, str) else None
    elif isinstance(event, Mapping):
        raw_event_id = event.get("event_id")
        raw_event_type = event.get("event_type")
        event_id = raw_event_id if isinstance(raw_event_id, str) else None
        event_type = raw_event_type if isinstance(raw_event_type, str) else None
    return EventAcceptanceResult(
        event_id=event_id,
        event_type=event_type,
        delivery_state=EventDeliveryState.REJECTED,
        subscribers_notified=(),
        reason=reason,
    )
