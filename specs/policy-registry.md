# Purpose

Define how EchoAuth stores, versions, loads, and validates policy sets used by
policy evaluation.

# Scope

Applies to all authorization, delegation, authority, runtime, emergency, and
notification policies.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `policy_id` | string | yes | Unique policy identifier. |
| `policy_version` | string | yes | Immutable policy version. |
| `policy_type` | enum | yes | `authority`, `delegation`, `runtime`, `security`, `notification`, `emergency`. |
| `rules` | object | yes | Deterministic policy rules. |
| `status` | enum | yes | `draft`, `active`, `retired`, `revoked`. |
| `created_by` | string | yes | Actor creating policy. |
| `effective_at` | timestamp | yes | Activation time. |
| `expires_at` | timestamp | no | Expiration time. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `registry_state` | enum | `registered`, `active`, `retired`, `revoked`, `rejected`, `found`. |
| `policy_hash` | string | Canonical policy hash. |
| `reason` | string | Machine-readable reason. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `draft` | `validate` | `validated` |
| `validated` | `activate` | `active` |
| `active` | `retire` | `retired` |
| `active` | `revoke` | `revoked` |
| `validated` | `reject` | `rejected` |

# Validation Rules

1. Policy ID and version pair must be unique.
2. Active policy rules must be deterministic.
3. Policy rules must not mutate runtime state directly.
4. Active policy must include reason codes for refusal outcomes.
5. `expires_at`, when present, must be later than `effective_at`.
6. Revoked policies must not be selected for new evaluations.

# Failure Conditions

| Condition | Result |
|---|---|
| Duplicate active version | `rejected` |
| Non-deterministic rule | `rejected` |
| Missing reason code | `rejected` |
| Invalid effective period | `rejected` |
| Unknown policy lookup | `not_found` |

# Security Requirements

- Policy activation requires authorized administrative action.
- Policy artifacts must be signed or hash-verified.
- Policy changes require audit and version bump.
- Runtime must pin policy version during evaluation.

# Audit Requirements

Record policy registration, validation, activation, retirement, revocation,
lookup, hash, actor, status, and timestamp.

# Persistence Requirements

- Persist every policy version immutably.
- Index by policy type, status, effective time, and version.
- Retain retired and revoked policies for audit replay.
- Store canonical policy hash.

# Deterministic Rules

- Policy selection uses effective time, policy type, status, then version order.
- Same policy artifact produces same hash.
- Runtime evaluation must use the pinned policy version.

# Examples

```json
{
  "policy_id": "authority_scope",
  "policy_version": "1.0.0",
  "policy_type": "authority",
  "registry_state": "active"
}
```
