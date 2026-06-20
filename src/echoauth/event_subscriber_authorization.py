"""Validation-only event subscriber authorization for Sprint 2S.

Configured evidence is local and hash-bound. This module does not register
subscriptions, route events, invoke callbacks, or provide delivery effects.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path

from echoauth.canonical import canonical_sha256
from echoauth.events_validation import load_event_catalog

SUBSCRIBER_AUTHORIZATION_VERSION = "echoauth.event-subscriber-authorization.v1"
_CATALOG_ONLY_EVENT_TYPES = frozenset({"runtime.recovered"})


@dataclass(frozen=True)
class SubscriberAuthorizationEvidence:
    """Explicit configured evidence for one subscriber and its event types."""

    authorization_id: str
    subscriber_id: str
    allowed_event_types: tuple[str, ...]
    evidence_hash: str


@dataclass(frozen=True)
class SubscriberAuthorizationResult:
    """Evidence-only authorization result with no subscription side effects."""

    subscriber_id: str | None
    event_type: str | None
    authorized: bool
    reason: str
    authorization_id: str | None = None
    evidence_hash: str | None = None


class EventSubscriberAuthorizationError(ValueError):
    """Raised when configured subscriber evidence is malformed or ambiguous."""


class EventSubscriberAuthorization:
    """Validate event-type access against explicit configured evidence."""

    def __init__(
        self,
        subscriber_evidence: Sequence[SubscriberAuthorizationEvidence],
        *,
        catalog_path: str | Path = "events/event-catalog.yaml",
    ) -> None:
        catalog = load_event_catalog(catalog_path)
        self._subscribers = _validate_configured_evidence(
            subscriber_evidence,
            catalog,
        )

    def authorize(
        self,
        subscriber_id: object,
        event_type: object,
    ) -> SubscriberAuthorizationResult:
        """Return fail-closed evidence without registering a subscription."""

        if not isinstance(subscriber_id, str) or not subscriber_id:
            return _rejected(None, _safe_string(event_type), "malformed_subscriber")
        if not isinstance(event_type, str) or not event_type:
            return _rejected(subscriber_id, None, "malformed_event_type")
        evidence = self._subscribers.get(subscriber_id)
        if evidence is None:
            return _rejected(subscriber_id, event_type, "unknown_subscriber")
        if event_type not in evidence.allowed_event_types:
            return _rejected(
                subscriber_id,
                event_type,
                "subscriber_event_type_not_authorized",
            )
        return SubscriberAuthorizationResult(
            subscriber_id=subscriber_id,
            event_type=event_type,
            authorized=True,
            reason="authorized",
            authorization_id=evidence.authorization_id,
            evidence_hash=evidence.evidence_hash,
        )


def subscriber_authorization_hash(
    evidence: SubscriberAuthorizationEvidence,
) -> str:
    """Hash canonical subscriber evidence without its supplied evidence hash."""

    payload = asdict(evidence)
    payload.pop("evidence_hash")
    payload["allowed_event_types"] = sorted(evidence.allowed_event_types)
    payload["format_version"] = SUBSCRIBER_AUTHORIZATION_VERSION
    return canonical_sha256(payload)


def _validate_configured_evidence(
    configured: Sequence[SubscriberAuthorizationEvidence],
    catalog: Mapping[str, str],
) -> dict[str, SubscriberAuthorizationEvidence]:
    if isinstance(configured, (str, bytes)) or not isinstance(configured, Sequence):
        raise EventSubscriberAuthorizationError(
            "subscriber evidence must be ordered"
        )
    subscribers: dict[str, SubscriberAuthorizationEvidence] = {}
    authorization_ids: set[str] = set()
    for evidence in configured:
        if not isinstance(evidence, SubscriberAuthorizationEvidence):
            raise EventSubscriberAuthorizationError(
                "configured subscriber evidence must be canonical"
            )
        for field_name in ("authorization_id", "subscriber_id", "evidence_hash"):
            value = getattr(evidence, field_name)
            if not isinstance(value, str) or not value:
                raise EventSubscriberAuthorizationError(
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
            raise EventSubscriberAuthorizationError(
                "allowed_event_types must be a non-empty string tuple"
            )
        if len(set(evidence.allowed_event_types)) != len(
            evidence.allowed_event_types
        ):
            raise EventSubscriberAuthorizationError(
                "allowed_event_types must be unique"
            )
        if any(event_type not in catalog for event_type in evidence.allowed_event_types):
            raise EventSubscriberAuthorizationError(
                "allowed_event_types must exist in the event catalog"
            )
        if _CATALOG_ONLY_EVENT_TYPES.intersection(evidence.allowed_event_types):
            raise EventSubscriberAuthorizationError(
                "catalog-only event types cannot be subscriber-authorized"
            )
        if subscriber_authorization_hash(evidence) != evidence.evidence_hash:
            raise EventSubscriberAuthorizationError(
                "subscriber authorization evidence hash mismatch"
            )
        if evidence.subscriber_id in subscribers:
            raise EventSubscriberAuthorizationError("subscriber_id must be unique")
        if evidence.authorization_id in authorization_ids:
            raise EventSubscriberAuthorizationError(
                "authorization_id must be unique"
            )
        subscribers[evidence.subscriber_id] = evidence
        authorization_ids.add(evidence.authorization_id)
    return subscribers


def _rejected(
    subscriber_id: str | None,
    event_type: str | None,
    reason: str,
) -> SubscriberAuthorizationResult:
    return SubscriberAuthorizationResult(
        subscriber_id=subscriber_id,
        event_type=event_type,
        authorized=False,
        reason=reason,
    )


def _safe_string(value: object) -> str | None:
    return value if isinstance(value, str) and value else None
