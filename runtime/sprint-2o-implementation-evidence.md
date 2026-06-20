# Sprint 2O Implementation Evidence

# Scope

Sprint 2O implements only the validation-only Halt Decision foundation:

- typed `HaltRequest`, `HaltDecision`, `HaltDecisionEvidence`, `HaltCause`,
  `HaltSeverity`, and `HaltOutcome` artifacts,
- deterministic classification of eight explicitly approved safety causes,
- cause-specific structural evidence validation,
- critical-severity halt precedence,
- immutable source-reference and evidence-hash packaging,
- machine-readable reasons and recovery evidence,
- in-process idempotency,
- Sprint 2A audit-chain integration.

The service exposes `decide()`, not `halt()`. It does not implement the abstract
state-mutating `HaltService`, publish `runtime.halted`, mutate Sprint 2L state,
invoke recovery, execute, dispatch, issue tokens, create envelopes, notify,
persist runtime state, orchestrate, or call external systems.

# Deterministic Classification

| Cause | Required Evidence | Outcome |
| --- | --- | --- |
| `missing_authority` | authority check ID, evidence hash, status | `refused` |
| `missing_evidence` | missing-evidence list, source evidence hash | `hold` |
| `invalid_state` | runtime transition decision ID and evidence hash | `halted` |
| `failed_invariant` | invariant result ID, state, and facts hash | `invalid -> refused`; `hold -> hold`; `halt -> halted` |
| `expired_dependency` | dependency ID, hash, `expired` status | `refused` |
| `invalid_dependency` | dependency ID, hash, invalid/revoked/conflict status | `refused` |
| `unresolved_override` | override ID, hash, deferred/unresolved outcome, reviewer | `escalated` |
| `unsafe_execution` | execution decision ID, hash, fail-closed outcome | `halted` |

`critical` severity overrides the cause table and always produces `halted`.
`recovery_allowed` is evidence-only and true only for `hold` and `escalated`.

# Implementation Evidence

| Component | Runtime Evidence | Test Evidence |
| --- | --- | --- |
| Contract-shaped models | `src/echoauth/runtime/halt_models.py` | All Sprint 2O fixtures and outcome assertions |
| Input and cause evidence validation | `validate_halt_request`; `_validate_cause_evidence` | Eight cause paths and malformed unsafe-execution evidence |
| Fixed classification | `_classify`; `_CAUSE_CLASSIFICATION` | Cause outcomes, invariant sub-outcomes, and critical override |
| Immutable evidence | `HaltDecisionEvidence`; canonical hashes and ordered references | Mutation rejection and equivalent-object stability |
| Audit and idempotency | `HaltDecisionService.decide`; `InMemoryAuditLogRepository` | Audit linkage and duplicate-append prevention |

# Test Evidence

Focused command:

```text
$env:PYTHONPATH='src'; python -B -m unittest tests.test_halt_decision -v
```

Focused result:

```text
Ran 14 tests

OK
```

Full-suite command:

```text
$env:PYTHONPATH='src'; python -B -m unittest discover -s tests -v
```

Full-suite result:

```text
Ran 183 tests in 0.370s

OK
```

All existing 169 tests and all 14 Sprint 2O tests pass.

# Deferred Items

- Runtime-state mutation and atomic persistence.
- Implementation of `HaltService.halt()`.
- Runtime halt event publication or notification delivery.
- Halt-to-recovery orchestration and recovery authorization.
- Envelope or token invalidation.
- Execution blocking, dispatch control, or command execution.
- Persistence adapters, decision repositories, signatures, and external source
  verification.
- API, protobuf, JSON Schema, database, event-delivery, and external adapters.
- The `revoked` outcome path, because no approved Sprint 2O cause maps to it.

# Documented Ambiguities

| Ambiguity | Sprint 2O handling |
| --- | --- |
| Halt evidence is a canonical object with no generated cause-specific schemas. | Validate the minimum explicit ID/hash/status fields required for each approved cause; do not infer additional source behavior. |
| `specs/runtime-halt-model.md` includes states absent from Sprint 2L. | Emit evidence-only `HaltOutcome` values and never call the state machine or mutate state. |
| The halt contract includes `revoked`, but the approved Sprint 2O causes do not define a revocation trigger. | Keep `revoked` in the typed contract vocabulary but produce no revocation classification. |
| Referenced source decisions are not persisted or signed. | Validate structure and canonical hashes only; do not claim authenticity or convert evidence into authorization. |
| `runtime.halted` exists in the event catalog, but event delivery is prohibited. | Append `runtime.halt.decision` to the audit chain only; do not publish a runtime event. |
| Recovery eligibility does not define a recovery workflow. | Record a boolean explanation only; do not call recovery or modify runtime state. |

# Status

Sprint 2O Halt Decision foundation: complete as deterministic, auditable,
non-executing evidence. All state mutation and operational effects remain
deferred.
