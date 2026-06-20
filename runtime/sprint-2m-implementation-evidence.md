# Sprint 2M Implementation Evidence

# Scope

Sprint 2M implements only the Execution Control eligibility foundation:

- typed `ExecutionRequest`, `ExecutionDecision`, `ExecutionControl`,
  `ExecutionEvidence`, `ExecutionConstraint`, and `ExecutionOutcome` artifacts,
- consumption of canonical Sprint 2L `RuntimeTransitionDecision` artifacts,
- constructor-configured immutable execution constraints,
- deterministic eligibility classification across seven canonical outcomes,
- fail-closed authority and governance evidence validation,
- immutable, hash-bound evidence packaging,
- in-process idempotency,
- Sprint 2A audit-chain integration.

An `ELIGIBLE` decision is evidence only. It cannot execute, dispatch, issue,
claim, transition, orchestrate, notify, or access an external system.

# Canonical Outcomes

`ELIGIBLE`, `BLOCKED`, `INVALID_STATE`, `MISSING_AUTHORITY`,
`MISSING_EVIDENCE`, `EXPIRED`, and `HALTED`.

# Deterministic Classification

Evaluation uses this fixed order:

1. A rejected Runtime State Machine decision produces `BLOCKED`.
2. Runtime state `HALTED` produces `HALTED`.
3. Runtime state `EXPIRED`, an elapsed constraint, or a constraint elapsed by
   request time produces `EXPIRED`.
4. A disabled configured constraint or `EXECUTION_BLOCKED` state produces
   `BLOCKED`.
5. Any state other than `READY` produces `INVALID_STATE`.
6. Missing canonical authority reference/hash evidence produces
   `MISSING_AUTHORITY`.
7. Missing refusal, escalation, review, or override ID/hash evidence required by
   the configured constraint produces `MISSING_EVIDENCE`.
8. Only a request passing every prior check produces `ELIGIBLE`.

# Implementation Evidence

| Component | Runtime Evidence | Test Evidence |
| --- | --- | --- |
| Execution models | `src/echoauth/execution/models.py` | All Sprint 2M fixtures and outcome assertions |
| State decision boundary | `ExecutionControl._validate_runtime_decision` | Every test consumes a real Sprint 2L decision; rejected decisions block |
| Configured constraints | `_validate_constraints`; exact configured-object match | Enabled, disabled, expired, all-path, and unconfigured constraint tests |
| Authority and path evidence | `_evidence_has`; fixed required-evidence checks | Missing authority, missing governance evidence, and complete override-path tests |
| Immutable evidence | `ExecutionEvidence`; canonical hashes | Actor, action, resource, runtime decision, constraint, and upstream evidence hash assertions |
| Audit and idempotency | `ExecutionControl.validate`; `InMemoryAuditLogRepository` | Audit event linkage and duplicate-append prevention |

# Test Evidence

Command:

```text
$env:PYTHONPATH='src'; python -B -m unittest discover -s tests
```

Result:

```text
Ran 157 tests in 0.173s

OK
```

The result includes every prior Sprint test and 13 Sprint 2M Execution Control
tests.

# Deferred Dependencies

- Command execution and dispatch.
- Execution token issuance, token claims, and replay protection.
- Runtime envelope creation and validation.
- Runtime-state mutation, orchestration, notifications, providers, and external
  systems.
- Persistent constraint registry, decision repository, and idempotency store.
- Signed or repository-verified authority, refusal, escalation, review,
  override, and runtime-transition decisions.
- API, protobuf, JSON Schema, event, database, and integration adapters.

# Contract Ambiguities

| Ambiguity | Sprint 2M handling |
| --- | --- |
| No standalone Execution Control specification or generated contract exists. | Use only Sprint 2M outcomes, Sprint 2L decisions, and existing execution/halt safety requirements. |
| The Sprint 2L `READY` vocabulary is absent from older generated runtime contracts. | Consume only the typed Sprint 2L decision and require its validated next state to be `READY`. |
| No contract determines whether a request used a direct or override governance path. | Use trusted configured constraints to declare required refusal, escalation, review, and override evidence; never infer a path. |
| Evidence IDs and hashes have no signature or repository-verification contract. | Validate canonical presence and hash-bind all evidence; treat authenticity verification as deferred and keep the decision non-executing. |
| No execution constraint registry contract exists. | Require exact equality with constructor-configured immutable constraints so callers cannot weaken their own requirements. |
| `ELIGIBLE` could be mistaken for execution authorization. | Define it strictly as prerequisite-validation evidence with no token, envelope, state, orchestration, claim, or dispatch effect. |

# Status

Sprint 2M Execution Control foundation: complete as a deterministic,
fail-closed, evidence-only component with no runtime side effects.
