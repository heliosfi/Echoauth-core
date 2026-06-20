# Sprint 2D Implementation Evidence

# Scope

Sprint 2D implements only the canonical Authority Resolution foundation:

- existing contract-shaped `AuthorityResolutionRequest` inputs,
- immutable `AuthorityResolutionResult` outputs,
- deterministic validation and evidence hashing,
- explicit Authority Registry lookup,
- lifecycle, expiration, and revocation awareness,
- provider-neutral scope matching,
- fail-closed conflict handling,
- Sprint 2A audit-chain integration.

Policy, delegation chains, mutation authorization, institutional or emergency
override logic, envelopes, tokens, execution, and runtime orchestration are not
implemented.

# Implementation Evidence

| Component | Runtime Evidence | Test Evidence |
| --- | --- | --- |
| Request model | `AuthorityResolutionRequest` in `src/echoauth/models.py` | All Sprint 2D tests use the approved request fields |
| Result model and outcomes | `AuthorityResolutionResult`; `AuthorityResolutionOutcome` in `src/echoauth/auth/authority_resolution.py` | Authorized, denied, revoked, expired, conflict, and insufficient-authority assertions |
| Resolution validation | `validate_authority_resolution_request` | Malformed revocation evidence denies deterministically |
| Registry lookup | `AuthorityRepository.find_by_subject`; `AuthorityResolutionService` | Valid, conflict, insufficient, and mismatch tests |
| Revocation awareness | `AuthorityResolutionService`; `_effective_revoked_record_ids` | Persisted revocation and request revocation-record tests |
| Expiration awareness | `AuthorityResolutionService`; `_is_expired` | Effective expiration test |
| Scope boundary | `AuthorityScopeMatcher`; `ScopeMatchResult` | Test-only exact matcher proves match/mismatch without production scope invention |
| Audit integration | `AuthorityResolutionService`; `InMemoryAuditLogRepository` | Resolution audit append and repeated-resolution idempotency tests |

# Deterministic Processing

- Only repository-backed `AuthorityRecord` artifacts can authorize.
- Candidate records must match both subject and authority source/requester.
- Revoked, expired, and suspended records never authorize.
- Effective authority revocation records override active registry status.
- Delegated and emergency records return `insufficient_authority` because their
  validation paths are deferred.
- Multiple applicable records return `conflict`; priority direction and policy
  precedence are not inferred.
- Canonical evidence binds request facts, identity-verdict reference, policy
  version, ordered authority record evidence, revocations, and resolution time.
- Repeated resolution of the same evidence returns the cached immutable result
  and does not duplicate audit evidence.

# Test Evidence

Command:

```text
$env:PYTHONPATH='src'; python -B -m unittest discover -s tests
```

Result:

```text
Ran 67 tests in 0.110s

OK
```

The result includes all prior Sprint tests and 9 Sprint 2D authority resolution
tests.

# Deferred Dependencies

- Policy evaluation and priority precedence.
- Delegation-chain and delegated-grant validation.
- Institutional and emergency override behavior.
- Mutation authorization.
- Envelope creation, execution tokens, execution services, and orchestration.
- Production persistence and distributed revocation propagation.
- Legacy OpenAPI/protobuf authority-verdict adapter.

# Contract Ambiguities

| Ambiguity | Sprint 2D handling |
| --- | --- |
| Specifications/generated contracts use `valid`, `refused`, `hold`, `conflict`, and `escalate`; Sprint 2D requires `authorized`, `denied`, `revoked`, `expired`, `conflict`, and `insufficient_authority`. | Runtime result uses the explicit Sprint 2D outcomes. Contract regeneration/adaptation remains deferred. |
| Scope is a canonical object without action/resource comparison semantics. | Resolution requires an injected `AuthorityScopeMatcher`; ambiguous scope denies. |
| Priority ordering does not define whether larger or smaller values win and policy is deferred. | Multiple applicable records return `conflict`; no record is selected by inferred precedence. |
| `identity_verdict_id` is required, but no verdict lookup repository is contracted. | Validate and hash-bind the reference only. It never creates authority. |
| Request contracts carry caller-supplied `authority_records`, while Sprint 2D requires registry lookup. | Resolver ignores caller-supplied authority candidates and uses only repository records. |
| Revocation records have no generated nested schema. | Validate the minimum fields defined by `specs/authority-revocation.md`; malformed evidence denies. |

# Status

Sprint 2D Authority Resolution foundation: complete with documented contract
adaptation dependencies.
