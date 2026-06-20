# Purpose

Define the canonical audit event record emitted by EchoAuth components.

# Scope

Applies to identity, authority, delegation, policy, invariant, envelope, token,
claim, execution, refusal, halt, escalation, recovery, event bus, notification,
and administrative events.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `event_type` | string | yes | Event category. |
| `actor_id` | string | yes | Actor or component causing event. |
| `request_id` | string | no | Related request. |
| `envelope_id` | string | no | Related runtime envelope. |
| `authority_verdict_id` | string | no | Related authority verdict. |
| `execution_token_id` | string | no | Related execution token. |
| `state_before` | string | no | Previous state. |
| `state_after` | string | no | New state. |
| `reason` | string | yes | Machine-readable event reason. |
| `details` | object | yes | Structured event payload. |
| `occurred_at` | timestamp | yes | Event time in UTC. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `audit_event_id` | string | Unique audit event identifier. |
| `event_hash` | string | Canonical hash of event. |
| `previous_hash` | string | Previous chain hash, if hash-chained. |
| `storage_state` | enum | `accepted`, `rejected`, `degraded`. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `created` | `validate` | `validated` |
| `validated` | `seal` | `sealed` |
| `sealed` | `append` | `stored` |
| `created` | `validation_failed` | `rejected` |
| `stored` | `verify_hash` | `verified` |
| `stored` | `hash_mismatch` | `tamper_alert` |

# Validation Rules

1. `event_type`, `actor_id`, `reason`, `details`, and `occurred_at` are mandatory.
2. State transition events must include `state_before` and `state_after`.
3. Token events must include `execution_token_id`.
4. Envelope events must include `envelope_id`.
5. Authority events must include `authority_verdict_id`.
6. Event payload must be canonically serialized before hashing.
7. Stored records must be immutable after sealing.
8. Hash-chain order must be preserved when configured.

# Failure Conditions

| Condition | Result |
|---|---|
| Missing required field | `rejected` |
| Invalid state transition record | `rejected` |
| Serialization failure | `rejected` |
| Hash mismatch | `tamper_alert` |
| Storage unavailable | `degraded` and runtime `hold` or `halted` |
| Attempted mutation | `tamper_alert` |

# Security Requirements

- Use append-only storage where possible.
- Hash or sign audit records.
- Avoid storing raw secrets.
- Preserve correlation identifiers.
- Protect audit logs from actors being audited.
- Treat audit unavailability as a runtime safety condition.

# Audit Requirements

The audit system must emit meta-audit records for accepted records, rejected
records, degraded storage mode, hash verification, hash mismatch, export,
retention action, and administrative access.

# Persistence Requirements

- Persist accepted audit records immutably.
- Persist rejected record metadata when safe.
- Store `event_hash`, `previous_hash`, schema version, writer, and timestamp.
- Retain audit records for configured audit retention.
- Index by request, event type, actor, and occurred time.

# Deterministic Rules

- Same canonical event payload and previous hash produce same event hash.
- Event field ordering must be canonical before hashing.
- Hash-chain position is determined by accepted append order.
- Missing required fields always reject.

# Examples

```json
{
  "event_type": "authorization.refused",
  "actor_id": "policy_engine",
  "request_id": "req_001",
  "reason": "delegation_out_of_scope"
}
```
