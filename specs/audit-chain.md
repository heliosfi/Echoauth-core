# Purpose

Define tamper-evident sequencing for EchoAuth audit records.

# Scope

Applies to all audit events emitted by identity, authority, delegation, policy,
invariant, envelope, token, execution, recovery, notification, and event bus
components.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `audit_event_id` | string | yes | Event identifier. |
| `event_payload` | object | yes | Canonical audit payload. |
| `previous_hash` | string | no | Previous chain hash. |
| `chain_id` | string | yes | Audit chain identifier. |
| `occurred_at` | timestamp | yes | Event time. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `event_hash` | string | Hash of canonical payload plus previous hash. |
| `chain_position` | integer | Event position in chain. |
| `chain_state` | enum | `accepted`, `rejected`, `verified`, `broken`. |
| `reason` | string | Machine-readable reason. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `received` | `canonicalize` | `canonicalized` |
| `canonicalized` | `hash` | `hashed` |
| `hashed` | `append` | `accepted` |
| `accepted` | `verify` | `verified` |
| any | `hash_mismatch` | `broken` |
| any | `validation_failure` | `rejected` |

# Validation Rules

1. Event payload must pass audit-record validation.
2. Canonical serialization must be stable.
3. `previous_hash` must equal last accepted event hash for the chain.
4. Chain position must increase by one.
5. Accepted audit events must be immutable.
6. Broken chains must trigger runtime safety notification.

# Failure Conditions

| Condition | Result |
|---|---|
| Previous hash mismatch | `broken` |
| Invalid payload | `rejected` |
| Duplicate event ID | `rejected` |
| Append conflict | retry or `broken` |
| Storage unavailable | runtime `hold` or `halted` |

# Security Requirements

- Use cryptographic hash function approved by deployment profile.
- Protect chain storage from mutation.
- Rotate chains only through configured checkpoint protocol.
- Do not store raw secrets in payload.

# Audit Requirements

Audit chain operations must emit meta-audit events for append, verify, mismatch,
checkpoint, rotation, export, and administrative access.

# Persistence Requirements

- Persist `chain_id`, `chain_position`, `previous_hash`, and `event_hash`.
- Store chain checkpoints.
- Retain broken-chain evidence.
- Replicate audit chain according to deployment durability requirements.

# Deterministic Rules

- Canonical serialization must sort object keys.
- Hash input format must be versioned.
- Same event payload and previous hash produce same event hash.

# Examples

```json
{
  "chain_id": "audit_main",
  "audit_event_id": "evt_001",
  "previous_hash": null,
  "chain_state": "accepted"
}
```
