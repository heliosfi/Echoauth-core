# Sprint 2P Recovery Eligibility Evidence Report

Freeze timestamp: `2026-06-19T21:12:47Z`

Freeze status: complete and included in the Sprint 2A-2P baseline.

# Scope

Sprint 2P implements validation-only Recovery Eligibility:

- typed request, result, state, failure-code, outcome, path, and Recovery Review
  Protocol artifacts,
- `EXECUTION_BLOCKED` and `HALTED` entry-state enforcement,
- the canonical failure-code policy and guard-field table,
- explicit Authority Resolution, Halt Decision, Review Decision, and review
  authority evidence binding,
- changed-evidence reference and hash validation,
- original-failure and Halt audit-chain linkage verification,
- deterministic evidence hashing and in-process idempotency,
- `recovery.eligibility.requested` and `recovery.eligibility.decided` audit
  records only.

# Outcome Boundary

The service emits only `REVALIDATION_REQUIRED`, `REJECTED`, or
`NEW_REQUEST_REQUIRED`. These outcomes are evidence and do not authorize the
original action, grant execution permission, identify a destination state, or
perform a runtime transition.

# Implementation Evidence

| Component | Runtime Evidence | Test Evidence |
| --- | --- | --- |
| Contract-shaped models | `src/echoauth/runtime/recovery_models.py` | Both canonical source states and all three outcomes |
| Request and failure-policy validation | `validate_recovery_request`; `_FAILURE_POLICY`; `_guards_satisfied` | Valid policy branches, invalid state/failure pair, and unresolved guard |
| Explicit authority binding | `_authority_failure` | Revoked and mismatched authority fail closed |
| Recovery Review Protocol binding | `_review_failure`; `recovery_review_protocol_hash` | Bound active protocol passes; absent required protocol requires a new request |
| Changed and source evidence validation | `_halt_failure`; `_audit_link_failure` | Equal changed hash and mismatched source audit hash fail closed |
| Audit and idempotency | `RecoveryEligibilityService.validate` | Exact eligibility events, unchanged source records, no `runtime.recovered`, and duplicate-call stability |

# Test Evidence

Focused command:

```text
$env:PYTHONPATH='src'; python -B -m unittest tests.test_recovery_eligibility -v
```

Focused result:

```text
Ran 11 tests

OK
```

Full-suite command:

```text
$env:PYTHONPATH='src'; python -B -m unittest discover -s tests -v
```

Full-suite result:

```text
Ran 194 tests

OK
```

# Deferred Items

- Recovery execution, orchestration, and automatic revalidation.
- Runtime-state mutation, transition requests, and destination states.
- Authorization or reauthorization of the original action.
- Token, envelope, notification, event delivery, adapter, and external-system
  behavior.
- Persistence beyond Sprint 2A append-only audit evidence.
- Signature, external trust-registry, and persisted-decision authenticity.
- Processing of the proposal-only `HOLD` to `EXECUTION_BLOCKED` contract.
- Emission of `runtime.recovered`.

# Contract Boundary

`recovery_allowed` is not present in runtime results. The deprecated schema
field is compatibility-only and is never treated as permission. Invalidated
token references are hash-bound evidence and are never restored or reused.

# Status

Sprint 2P Recovery Eligibility validation is complete as deterministic,
auditable, non-authorizing evidence. Operational Recovery remains deferred.
