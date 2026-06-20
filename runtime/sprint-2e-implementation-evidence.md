# Sprint 2E Implementation Evidence

# Scope

Sprint 2E implements only the canonical Delegation foundation:

- explicit `DelegationGrant` artifacts,
- request and result models,
- deterministic grant and validation evidence hashing,
- authority-gated grant creation,
- append-history in-memory persistence,
- issued, active, expired, revoked, and invalid lifecycle support,
- expiration and revocation enforcement,
- continuing authority-source validation,
- explicit action/resource scope enforcement,
- provider-neutral context matching,
- chain-metadata preservation with fail-closed chain handling,
- Sprint 2A audit-chain integration.

Policy, precedence, institutional or emergency overrides, execution
authorization, tokens, envelopes, mutation authorization, and orchestration are
not implemented.

# Implementation Evidence

| Component | Runtime Evidence | Test Evidence |
| --- | --- | --- |
| Delegation models | `src/echoauth/auth/delegation_models.py` | All Sprint 2E fixtures use typed grant, request, and result models |
| Grant validation and hashing | `src/echoauth/auth/delegation_validation.py` | Scope expansion rejection and deterministic result tests |
| Repository and lifecycle | `src/echoauth/auth/delegation_repository.py` | Issuance, activation, revocation, expiration, and immutable audit history tests |
| Authority integration | `InMemoryDelegationRepository._validate_grantor`; `DelegationValidationService._grantor_is_current` | Valid authority-derived grant and revoked-grantor tests |
| Runtime validation | `src/echoauth/auth/delegation_service.py` | Valid, expired, revoked, invalid-grantor, invalid-scope, invalid-subject, and conflict tests |
| Audit integration | Delegation repository and validation service | Hash-chained history and repeated-validation audit idempotency |

# Deterministic Processing

- A grant is created only from an `authorized` Sprint 2D result whose source,
  authority record, resolution ID, and subject registry record match.
- Every proposed action/resource pair must fit the authority result scope.
- Grant actions and resources are canonicalized into sorted, unique tuples.
- Grant evidence binds grantor, delegate, subject, role, scope, dates, authority
  references, and chain metadata independently of mutable lifecycle state.
- Validation checks subject, delegate, authority reference, revocation,
  expiration, active state, current grantor authority, action, resource, and
  context in stable order.
- Revocation supersedes active state.
- Non-empty chain metadata is preserved but resolves to `conflict` because
  delegation-chain validation remains unspecified.
- Repeated validation of identical evidence returns the cached immutable result
  without duplicating audit evidence.

# Test Evidence

Command:

```text
$env:PYTHONPATH='src'; python -B -m unittest discover -s tests
```

Result:

```text
Ran 76 tests in 0.108s

OK
```

The result includes all prior Sprint tests and 9 Sprint 2E delegation tests.

# Deferred Dependencies

- Policy evaluation and policy precedence.
- Bounded multi-hop delegation-chain validation.
- Institutional and emergency override logic.
- Delegate identity-verdict lookup.
- Mutation authorization.
- Execution authorization, tokens, envelopes, services, and orchestration.
- Production database persistence and distributed revocation propagation.
- API and protobuf runtime adapters.

# Contract Ambiguities

| Ambiguity | Sprint 2E handling |
| --- | --- |
| Generated contracts use `invalid`, `out_of_scope`, and `hold`; Sprint 2E requires `invalid_grantor`, `invalid_scope`, `invalid_subject`, and `conflict`. | Runtime result uses the explicit Sprint 2E outcomes. Contract adaptation remains deferred. |
| Delegate identity must verify, but `DelegationValidationRequest` contains no identity-verdict reference. | Enforce exact requester/delegate match; document external identity verification as a prerequisite. No authority is inferred from identity. |
| Delegation chains must be bounded, but no generated chain fields or maximum depth exist. | Preserve canonical `chain_metadata`; any non-empty chain returns `conflict`. |
| Context constraints are canonical objects without predicate semantics. | Require an injected `DelegationContextMatcher`; ambiguity returns `conflict`. |
| Wildcard scope requires policy, but policy is deferred. | No wildcard expansion is implemented; action and resource strings match exactly. |
| Runtime grants require `state`, `evidence_hash`, `authority_resolution_id`, and chain metadata, while the database table lacks these fields. | Use in-memory persistence only; production mapping remains blocked. |
| The specification names `authority_verdict_id`, while Sprint 2D produces `authority_resolution_id`. | Sprint 2E binds the request field to the stored Sprint 2D resolution identifier without changing generated contracts. |

# Status

Sprint 2E Delegation foundation: complete with documented contract adaptation
dependencies.
