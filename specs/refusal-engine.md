# Purpose

Define the component that converts failed validation, missing authority, policy
denial, or invariant failure into structured non-execution outcomes.

# Scope

Applies to all pre-execution and runtime checks that produce refusal, hold,
halt, revocation, or escalation.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `refusal_request_id` | string | yes | Unique refusal evaluation. |
| `request_id` | string | yes | Related request. |
| `failure_source` | enum | yes | `identity`, `authority`, `delegation`, `policy`, `invariant`, `runtime`, `audit`. |
| `failure_code` | string | yes | Machine-readable failure. |
| `severity` | enum | yes | `low`, `medium`, `high`, `critical`. |
| `recoverable` | boolean | yes | Whether recovery may be attempted. |
| `evidence` | object | yes | Failure evidence. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `refusal_state` | enum | `refused`, `hold`, `halted`, `revoked`, `escalated`. |
| `reason` | string | Canonical reason code. |
| `recovery_path` | string | Required recovery or review path. |
| `audit_event_id` | string | Audit reference. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `received` | `recoverable_missing_evidence` | `hold` |
| `received` | `nonrecoverable_denial` | `refused` |
| `received` | `integrity_failure` | `halted` |
| `received` | `revocation_event` | `revoked` |
| `received` | `review_required` | `escalated` |

# Validation Rules

1. Failure source and code are mandatory.
2. Critical integrity failures must map to `halted`.
3. Missing authority maps to `refused` unless policy defines reachable authority as `hold`.
4. Missing evidence maps to `hold` only when recoverable is true.
5. Revocation events map to `revoked`.
6. Refusal output must include recovery path or `none`.

# Failure Conditions

| Condition | Result |
|---|---|
| Unknown failure code | `halted` |
| Missing evidence hash | `halted` |
| Refusal engine unavailable | fail closed to `halted` |
| Conflicting refusal mappings | `escalated` |

# Security Requirements

- Refusal engine decisions must not be overridden by executor.
- Failure code mapping must be versioned.
- Refusal outputs must be immutable once emitted.
- Refusal must not disclose sensitive evidence beyond configured audience.

# Audit Requirements

Record failure source, code, severity, recoverability, mapped state, recovery
path, evidence hash, mapping version, and timestamp.

# Persistence Requirements

- Persist refusal decisions with request state.
- Store mapping version used.
- Retain refusal records for audit retention.
- Index by request, failure source, and refusal state.

# Deterministic Rules

- Same failure source/code/severity/recoverability must map to same state.
- Mapping table order must be stable.
- Unknown critical failures always halt.

# Examples

```json
{
  "failure_source": "authority",
  "failure_code": "scope_mismatch",
  "refusal_state": "refused"
}
```
