"""Authority resolution interface exports.

Specification: specs/authority-resolution.md
Contracts: schemas/authority-resolution.schema.json,
contracts/service-contracts.yaml#authority_resolver
State machine: specs/runtime-state-machine.md
"""

from echoauth.interfaces import AuthorityService
from echoauth.models import AuthorityResolutionRequest, AuthorityVerdict
from echoauth.repositories import AuthorityRegistryRepository, RevocationRepository
from echoauth.auth.authority_models import (
    AuthorityHistoryEntry,
    AuthorityRecord,
    AuthorityRegistryState,
    AuthorityStatus,
    AuthorityType,
    StoredAuthorityRecord,
)
from echoauth.auth.authority_registry import (
    AuthorityAuditError,
    AuthorityNotFoundError,
    AuthorityRepository,
    AuthorityRepositoryError,
    DuplicateAuthorityError,
    InMemoryAuthorityRepository,
    InvalidAuthorityTransitionError,
)
from echoauth.auth.authority_validation import (
    AuthorityValidationError,
    authority_evidence_hash,
    build_authority_record,
    validate_authority_record,
)
from echoauth.auth.authority_resolution import (
    AuthorityResolutionAuditError,
    AuthorityResolutionOutcome,
    AuthorityResolutionResult,
    AuthorityResolutionService,
    AuthorityResolutionValidationError,
    AuthorityScopeMatcher,
    ScopeMatchResult,
    authority_resolution_evidence_hash,
    validate_authority_resolution_request,
)

__all__ = [
    "AuthorityRegistryRepository",
    "AuthorityAuditError",
    "AuthorityHistoryEntry",
    "AuthorityNotFoundError",
    "AuthorityRecord",
    "AuthorityRepository",
    "AuthorityRepositoryError",
    "AuthorityRegistryState",
    "AuthorityResolutionRequest",
    "AuthorityResolutionAuditError",
    "AuthorityResolutionOutcome",
    "AuthorityResolutionResult",
    "AuthorityResolutionService",
    "AuthorityResolutionValidationError",
    "AuthorityScopeMatcher",
    "AuthorityService",
    "AuthorityStatus",
    "AuthorityType",
    "AuthorityVerdict",
    "AuthorityValidationError",
    "DuplicateAuthorityError",
    "InMemoryAuthorityRepository",
    "InvalidAuthorityTransitionError",
    "RevocationRepository",
    "StoredAuthorityRecord",
    "ScopeMatchResult",
    "authority_evidence_hash",
    "authority_resolution_evidence_hash",
    "build_authority_record",
    "validate_authority_record",
    "validate_authority_resolution_request",
]
