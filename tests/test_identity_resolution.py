"""Sprint 2B identity resolution tests."""

from __future__ import annotations

import unittest
from datetime import datetime, timezone

from echoauth.identity import (
    CredentialVerification,
    CredentialVerifier,
    IdentityProviderUnavailableError,
    IdentityRecord,
    IdentityStatus,
    IdentityVerdictState,
    InMemoryIdentityRepository,
    RegistryIdentityService,
)
from echoauth.models import (
    ActorType,
    AssuranceLevel,
    CanonicalJsonObject,
    IdentityResolutionRequest,
)


class StaticVerifier(CredentialVerifier):
    def __init__(self, verification: CredentialVerification) -> None:
        self.verification = verification
        self.calls = 0

    def verify(
        self,
        record: IdentityRecord,
        credential_set: CanonicalJsonObject,
        context: CanonicalJsonObject,
        session_id: str | None,
    ) -> CredentialVerification:
        self.calls += 1
        return self.verification


class UnavailableVerifier(CredentialVerifier):
    def verify(
        self,
        record: IdentityRecord,
        credential_set: CanonicalJsonObject,
        context: CanonicalJsonObject,
        session_id: str | None,
    ) -> CredentialVerification:
        raise IdentityProviderUnavailableError("offline")


def _record() -> IdentityRecord:
    return IdentityRecord(
        identity_record_id="identity-1",
        actor_id="actor-1",
        actor_type=ActorType.HUMAN,
        status=IdentityStatus.ACTIVE,
        credential_refs=("credential-1",),
        created_at="2026-06-19T12:00:00Z",
        updated_at="2026-06-19T12:00:00Z",
    )


def _request(**overrides: object) -> IdentityResolutionRequest:
    values: dict[str, object] = {
        "identity_request_id": "identity-request-1",
        "actor_id": "actor-1",
        "actor_type": ActorType.HUMAN,
        "credential_set": {"credential_ref": "credential-1", "proof": "proof-1"},
        "context": {"channel": "test"},
        "required_assurance": AssuranceLevel.STANDARD,
    }
    values.update(overrides)
    return IdentityResolutionRequest(**values)  # type: ignore[arg-type]


def _verification(
    *,
    state: IdentityVerdictState = IdentityVerdictState.VERIFIED,
    assurance: AssuranceLevel = AssuranceLevel.STANDARD,
    reason: str = "credentials_verified",
) -> CredentialVerification:
    return CredentialVerification(
        state=state,
        assurance_level=assurance,
        reason=reason,
        verifier_component="test_verifier",
        evidence={"credential_class": "test"},
    )


class IdentityResolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryIdentityRepository()
        self.repository.register(_record())
        self.clock = lambda: datetime(2026, 6, 19, 12, 0, tzinfo=timezone.utc)

    def test_active_identity_resolves_and_is_deterministic(self) -> None:
        verifier = StaticVerifier(_verification())
        service = RegistryIdentityService(self.repository, verifier, clock=self.clock)

        first = service.resolve(_request())
        second = service.resolve(_request())

        self.assertEqual(first.state, IdentityVerdictState.VERIFIED.value)
        self.assertEqual(first, second)
        self.assertEqual(first.expires_at, "2026-06-19T12:05:00Z")
        self.assertEqual(verifier.calls, 2)

    def test_revoked_identity_refuses_without_verifier(self) -> None:
        verifier = StaticVerifier(_verification())
        self.repository.transition(
            "identity-1",
            IdentityStatus.REVOKED,
            updated_at="2026-06-19T12:01:00Z",
        )
        service = RegistryIdentityService(self.repository, verifier, clock=self.clock)

        verdict = service.resolve(_request())

        self.assertEqual(verdict.state, IdentityVerdictState.REFUSED.value)
        self.assertEqual(verdict.reason, "identity_revoked")
        self.assertEqual(verifier.calls, 0)

    def test_wrong_actor_type_conflicts(self) -> None:
        verifier = StaticVerifier(_verification())
        service = RegistryIdentityService(self.repository, verifier, clock=self.clock)

        verdict = service.resolve(_request(actor_type=ActorType.SERVICE))

        self.assertEqual(verdict.state, IdentityVerdictState.CONFLICT.value)
        self.assertEqual(verdict.reason, "actor_type_conflict")

    def test_missing_credentials_refuses(self) -> None:
        verifier = StaticVerifier(_verification())
        service = RegistryIdentityService(self.repository, verifier, clock=self.clock)

        verdict = service.resolve(_request(credential_set={}))

        self.assertEqual(verdict.state, IdentityVerdictState.REFUSED.value)
        self.assertEqual(verdict.reason, "missing_credential")
        self.assertEqual(verifier.calls, 0)

    def test_assurance_below_requirement_refuses(self) -> None:
        verifier = StaticVerifier(_verification(assurance=AssuranceLevel.LOW))
        service = RegistryIdentityService(self.repository, verifier, clock=self.clock)

        verdict = service.resolve(_request(required_assurance=AssuranceLevel.HIGH))

        self.assertEqual(verdict.state, IdentityVerdictState.REFUSED.value)
        self.assertEqual(verdict.reason, "assurance_below_requirement")

    def test_provider_unavailable_holds(self) -> None:
        service = RegistryIdentityService(
            self.repository, UnavailableVerifier(), clock=self.clock
        )

        verdict = service.resolve(_request())

        self.assertEqual(verdict.state, IdentityVerdictState.HOLD.value)
        self.assertEqual(verdict.reason, "identity_provider_unavailable")

    def test_invalid_request_enum_refuses_deterministically(self) -> None:
        verifier = StaticVerifier(_verification())
        service = RegistryIdentityService(self.repository, verifier, clock=self.clock)

        verdict = service.resolve(_request(actor_type="unknown"))

        self.assertEqual(verdict.state, IdentityVerdictState.REFUSED.value)
        self.assertEqual(verdict.reason, "invalid_identity_request")
        self.assertEqual(verifier.calls, 0)


if __name__ == "__main__":
    unittest.main()
