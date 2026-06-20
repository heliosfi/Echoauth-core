# Purpose

Define the append-only audit log interface used to store EchoAuth audit records
and audit-chain events.

# Scope

Applies to every persisted audit event from runtime components.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `append_request_id` | string | yes | Unique append request. |
| `audit_event` | object | yes | Valid audit record. |
| `chain_id` | string | yes | Target audit chain. |
| `expected_previous_hash` | string | no | Optimistic chain guard. |
| `writer_id` | string | yes | Component writing event. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `append_state` | enum | `accepted`, `rejected`, `conflict`, `degraded`. |
| `audit_event_id` | string | Stored event ID. |
| `event_hash` | string | Stored event hash. |
| `chain_position` | integer | Position in chain. |
| `reason` | string | Machine-readable reason. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `received` | `validate_event` | `validated` |
| `received` | `validation_failed` | `rejected` |
| `validated` | `append_success` | `accepted` |
| `validated` | `hash_conflict` | `conflict` |
| `validated` | `storage_degraded` | `degraded` |

# Validation Rules

1. Audit event must satisfy `specs/audit-record.md`.
2. Writer must be registered.
3. Expected previous hash must match current chain tail when supplied.
4. Duplicate event IDs must reject.
5. Audit event hash must be computed by canonical chain rules.

# Failure Conditions

| Condition | Result |
|---|---|
| Invalid event | `rejected` |
| Unknown writer | `rejected` |
| Previous hash conflict | `conflict` |
| Storage unavailable | `degraded` |
| Duplicate event ID | `rejected` |

# Security Requirements

- Audit log storage must be append-only.
- Administrative access must be audited.
- Audit log deletion is prohibited except by retention process.
- Audit data must be protected from runtime actors being audited.

# Audit Requirements

Audit log operations must meta-audit append, reject, conflict, degraded mode,
verification, export, retention, and administrative access.

# Persistence Requirements

- Persist chain tail atomically with event append.
- Replicate according to deployment durability profile.
- Retain event hash, previous hash, writer, schema version, and timestamp.
- Preserve rejected append attempts when possible.

# Deterministic Rules

- Same event payload and previous hash produce same event hash.
- Chain position increases by exactly one per accepted append.
- Conflict resolution never rewrites accepted events.

# Examples

```json
{
  "append_request_id": "append_001",
  "chain_id": "audit_main",
  "append_state": "accepted"
}
```
