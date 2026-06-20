"""Identity resolution service for the Sprint 2B registry foundation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from datetime import datetime, timedelta, timezone

from echoauth.canonical import canonical_sha256
from echoauth.identity.models import (
    CredentialVerification,
    IdentityRecord,
    IdentityStatus,
    IdentityVerdictState,
)
from echoauth.identity.repository import IdentityNotFoundError, IdentityRepository
from echoauth.identity.validation import (
    IdentityValidationError,
    identity_evidence_hash,
    validate_resolution_request,
)
from echoauth.interfaces import IdentityService
from echoauth.models import (
    AssuranceLevel,
    CanonicalJsonObject,
    IdentityResolutionRequest,
    IdentityVerdict,
)


class IdentityProviderUnavailableError(RuntimeError):
    """Raised by a verifier when its identity provider is unavailable."""


class CredentialVerifier(ABC):
    """Provider-neutral credential verification boundary."""

    @abstractmethod
    def verify(
        self,
        record: IdentityRecord,
        credential_set: CanonicalJsonObject,
        context: CanonicalJsonObject,
        session_id: str | None,
    ) -> CredentialVerification:
        """Verify credentials without granting authority."""


_ASSURANCE_RANK = {
    AssuranceLevel.LOW: 0,
    AssuranceLevel.STANDARD: 1,
    AssuranceLevel.HIGH: 2,
    AssuranceLevel.CRITICAL: 3,
}


class RegistryIdentityService(IdentityService):
    """Resolve identities against a registry and injected credential verifier."""

    def __init__(
        self,
        repository: IdentityRepository,
        verifier: CredentialVerifier,
        *,
        verdict_ttl: timedelta = timedelta(minutes=5),
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if verdict_ttl <= timedelta(0):
            raise ValueError("verdict_ttl must be positive")
        self._repository = repository
        self._verifier = verifier
        self._verdict_ttl = verdict_ttl
        self._clock = clock or (lambda: datetime.now(timezone.utc))

    def resolve(self, request: IdentityResolutionRequest) -> IdentityVerdict:
        """Return a deterministic, fail-closed identity verdict."""

        try:
            validate_resolution_request(request)
        except IdentityValidationError:
            return self._verdict(
                request,
                IdentityVerdictState.REFUSED,
                AssuranceLevel.LOW,
                "invalid_identity_request",
                record_hash=None,
            )

        try:
            stored = self._repository.get_by_actor(request.actor_id)
        except IdentityNotFoundError:
            return self._verdict(
                request,
                IdentityVerdictState.REFUSED,
                AssuranceLevel.LOW,
                "identity_not_found",
                record_hash=None,
            )

        record = stored.identity_record
        if record.actor_type is not request.actor_type:
            return self._verdict(
                request,
                IdentityVerdictState.CONFLICT,
                AssuranceLevel.LOW,
                "actor_type_conflict",
                record_hash=stored.record_hash,
            )
        if record.status is IdentityStatus.REVOKED:
            return self._verdict(
                request,
                IdentityVerdictState.REFUSED,
                AssuranceLevel.LOW,
                "identity_revoked",
                record_hash=stored.record_hash,
            )
        if record.status is IdentityStatus.SUSPENDED:
            return self._verdict(
                request,
                IdentityVerdictState.REFUSED,
                AssuranceLevel.LOW,
                "identity_suspended",
                record_hash=stored.record_hash,
            )
        if record.status is IdentityStatus.ARCHIVED:
            return self._verdict(
                request,
                IdentityVerdictState.REFUSED,
                AssuranceLevel.LOW,
                "identity_archived",
                record_hash=stored.record_hash,
            )
        if not request.credential_set:
            return self._verdict(
                request,
                IdentityVerdictState.REFUSED,
                AssuranceLevel.LOW,
                "missing_credential",
                record_hash=stored.record_hash,
            )

        try:
            verification = self._verifier.verify(
                record,
                request.credential_set,
                request.context,
                request.session_id,
            )
        except IdentityProviderUnavailableError:
            return self._verdict(
                request,
                IdentityVerdictState.HOLD,
                AssuranceLevel.LOW,
                "identity_provider_unavailable",
                record_hash=stored.record_hash,
            )

        if verification.state is IdentityVerdictState.VERIFIED and (
            _ASSURANCE_RANK[verification.assurance_level]
            < _ASSURANCE_RANK[request.required_assurance]
        ):
            return self._verdict(
                request,
                IdentityVerdictState.REFUSED,
                verification.assurance_level,
                "assurance_below_requirement",
                record_hash=stored.record_hash,
                verification_evidence=verification.evidence,
            )
        return self._verdict(
            request,
            verification.state,
            verification.assurance_level,
            verification.reason,
            record_hash=stored.record_hash,
            verification_evidence=verification.evidence,
        )

    def _verdict(
        self,
        request: IdentityResolutionRequest,
        state: IdentityVerdictState,
        assurance: AssuranceLevel,
        reason: str,
        *,
        record_hash: str | None,
        verification_evidence: CanonicalJsonObject | None = None,
    ) -> IdentityVerdict:
        evidence_hash = identity_evidence_hash(
            request,
            record_hash=record_hash,
            verification_evidence=verification_evidence,
        )
        verdict_hash = canonical_sha256(
            {
                "evidence_hash": evidence_hash,
                "identity_request_id": request.identity_request_id,
                "reason": reason,
                "state": state.value,
            }
        )
        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise ValueError("identity service clock must return a timezone-aware datetime")
        expires_at = (now.astimezone(timezone.utc) + self._verdict_ttl).isoformat().replace(
            "+00:00", "Z"
        )
        return IdentityVerdict(
            identity_verdict_id=f"idv_{verdict_hash}",
            state=state.value,
            resolved_actor_id=request.actor_id,
            assurance_level=assurance,
            evidence_hash=evidence_hash,
            expires_at=expires_at,
            reason=reason,
        )
