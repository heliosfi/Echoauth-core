# Purpose

Define the runtime component that validates non-negotiable EchoAuth invariants
before and during execution.

# Scope

Applies to authority, delegation, policy, envelope, token, session, audit,
channel, concurrency, and execution integrity checks.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `validation_id` | string | yes | Unique invariant validation request. |
| `request_id` | string | yes | Runtime request. |
| `envelope_id` | string | no | Runtime envelope. |
| `invariant_version` | string | yes | Invariant set version. |
| `runtime_state` | string | yes | Current runtime state. |
| `facts` | object | yes | Canonical facts to validate. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `invariant_result_id` | string | Unique result identifier. |
| `state` | enum | `valid`, `invalid`, `hold`, `halt`. |
| `failed_invariants` | list | Invariants that failed. |
| `reason` | string | Machine-readable reason. |
| `facts_hash` | string | Canonical facts hash. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `received` | `load_invariants` | `evaluating` |
| `received` | `invariants_missing` | `hold` |
| `evaluating` | `all_pass` | `valid` |
| `evaluating` | `recoverable_missing_fact` | `hold` |
| `evaluating` | `noncritical_failure` | `invalid` |
| `evaluating` | `critical_failure` | `halt` |

# Validation Rules

1. Invariant version must exist and be active.
2. Facts must be canonicalized before evaluation.
3. Invariants must run in stable configured order.
4. Critical invariant failures must halt.
5. Missing required facts must not pass validation.
6. Invariant validation must be side-effect free.

# Failure Conditions

| Condition | Result |
|---|---|
| Unknown invariant version | `hold` |
| Missing required fact | `hold` |
| Single-token violation | `halt` |
| Payload mismatch | `halt` |
| Authority mismatch | `invalid` or `halt` |
| Audit path unavailable | `hold` or `halt` |

# Security Requirements

- Invariant definitions must be immutable for a version.
- Runtime must pin invariant version in the envelope.
- Failed invariants must not be bypassed by policy.
- Validator failures fail closed.

# Audit Requirements

Record invariant version, facts hash, evaluation order, failed invariants,
result state, reason, validator identity, and timestamp.

# Persistence Requirements

- Persist invariant result when used for authorization or execution.
- Persist invariant definition hash.
- Retain failed invariant evidence.
- Invalidate cached results when facts or invariant version changes.

# Deterministic Rules

- Same invariant version and facts hash must produce same result.
- Invariant ordering is fixed by version.
- Criticality mapping is fixed by invariant definition.

# Examples

```json
{
  "validation_id": "inv_001",
  "invariant_version": "1.0.0",
  "state": "valid",
  "failed_invariants": []
}
```
