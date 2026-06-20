"""EchoAuth identity registry and resolution runtime boundary."""

from echoauth.identity.models import (
    CredentialVerification,
    IdentityRecord,
    IdentityState,
    IdentityStatus,
    IdentityVerdictState,
    StoredIdentityRecord,
)
from echoauth.identity.repository import (
    DuplicateIdentityError,
    IdentityNotFoundError,
    IdentityRepository,
    IdentityRepositoryError,
    InMemoryIdentityRepository,
    InvalidIdentityTransitionError,
)
from echoauth.identity.service import (
    CredentialVerifier,
    IdentityProviderUnavailableError,
    RegistryIdentityService,
)
from echoauth.identity.validation import (
    IdentityValidationError,
    identity_evidence_hash,
    identity_record_hash,
    normalize_identity_record,
    validate_resolution_request,
)

__all__ = [
    "CredentialVerification",
    "CredentialVerifier",
    "DuplicateIdentityError",
    "IdentityNotFoundError",
    "IdentityProviderUnavailableError",
    "IdentityRecord",
    "IdentityRepository",
    "IdentityRepositoryError",
    "IdentityState",
    "IdentityStatus",
    "IdentityValidationError",
    "IdentityVerdictState",
    "InMemoryIdentityRepository",
    "InvalidIdentityTransitionError",
    "RegistryIdentityService",
    "StoredIdentityRecord",
    "identity_evidence_hash",
    "identity_record_hash",
    "normalize_identity_record",
    "validate_resolution_request",
]
