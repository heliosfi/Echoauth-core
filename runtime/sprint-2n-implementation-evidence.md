# Sprint 2N Implementation Evidence

# Selected Gap

The Invariant Validator was the next smallest contract-backed Sprint 2 gap:

- `specs/invariant-validator.md` defines its complete request/result shape,
  outcome state machine, validation rules, audit requirements, and deterministic
  requirements.
- OpenAPI defines `InvariantValidationRequest` and `InvariantResult`.
- `contracts/service-contracts.yaml` defines the service boundary.
- `database/schema.sql` defines the future result persistence shape.
- `events/event-catalog.yaml` defines `invariant.result`.
- Runtime coverage previously contained only an abstract interface.

Halt/recovery and runtime-state persistence were not selected because they
require state mutation or adapters. Envelopes, tokens, claims, notifications,
and orchestration remain outside the permitted boundary.

# Implemented Scope

- Typed invariant request, result, state, rule, and versioned-set artifacts.
- Immutable, detached, ordered rule definitions.
- Active and inactive invariant versions.
- Canonical facts hashing and versioned definition hashing.
- Deterministic top-level fact equality checks.
- Fixed outcome precedence: `halt`, then `invalid`, then `hold`, then `valid`.
- Fail-closed unknown/inactive versions and missing required facts.
- Stable failed-invariant and evaluation ordering.
- Sprint 2A audit-chain integration and in-process idempotency.

The service is side-effect free except for required audit append. It does not
authorize, execute, mutate state, create envelopes, issue tokens, notify, or
call external systems.

# Deterministic Rules

1. The request pins one invariant version and supplies canonical facts.
2. Unknown or inactive versions return `hold`.
3. Rules run in their immutable configured tuple order.
4. A missing configured fact records that invariant and returns at least
   `hold`.
5. Canonical expected and actual values are compared by stable hashes.
6. Any configured critical mismatch returns `halt`.
7. Otherwise, any noncritical mismatch returns `invalid`.
8. Otherwise, missing facts return `hold`.
9. Only complete matching facts return `valid`.
10. Results bind request, version, runtime state, envelope reference, facts,
    definition, failure order, and validator version.

# Test Evidence

Command:

```text
$env:PYTHONPATH='src'; python -B -m unittest discover -s tests -v
```

Result:

```text
Ran 169 tests in 0.182s

OK
```

The result includes all prior tests and 12 focused Sprint 2N tests.

# Deferred Items

- Translation of the twelve governance invariants into runtime predicates.
- Trusted fact producers and provenance/signature validation.
- Authority, delegation, policy, payload, token, nonce, channel, audit-path,
  separation-of-powers, and refusal-safety fact adapters.
- Integration into Authorization Gate, Runtime State Machine, Execution Control,
  envelopes, tokens, claims, halt, recovery, or orchestration.
- Persistent invariant definition/result repositories and cache invalidation
  across processes.
- API, protobuf, JSON Schema, database, event publication, and external adapters.
- Notifications, execution, state mutation, and provider calls.

# Documented Ambiguities

| Ambiguity | Sprint 2N handling |
| --- | --- |
| The contract requires immutable ordered definitions but defines no invariant expression language. | Support only configured top-level fact equality checks; do not invent domain predicates or nested path semantics. |
| `governance/invariants.md` names twelve invariants but does not define canonical runtime fact schemas for them. | Preserve them as documentation; do not claim they are implemented. |
| Authority mismatch and audit unavailability may be `invalid` or `halt`, and audit unavailability may also be `hold`. | Require each configured rule to declare `invalid` or `halt`; missing facts always hold. No category-specific mapping is inferred. |
| Fact provenance and result authenticity are unspecified. | Canonicalize and hash facts/results only; do not convert supplied facts into authorization. |
| Database persistence is specified but persistence adapters are prohibited in this sprint. | Produce immutable in-memory results and audit records only. |
| `echoauth.governance` has a pre-existing eager-import cycle when imported before `echoauth.auth`. | Preserve the established import order in focused tests; defer package-wide lazy-loading changes as unrelated refactoring. |

# Status

Sprint 2N Invariant Validator foundation: complete within the contract-backed,
validation-only boundary. Domain invariant implementation remains explicitly
deferred.
