# Purpose

Define the canonical identity record model used by EchoAuth identity resolution,
authority resolution, delegation validation, sessions, audit, and notifications.

# Scope

Applies to persisted identity subjects and identity evidence references.
`specs/identity-resolution.md` defines runtime verification; this document
defines the identity data contract.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `identity_record_id` | string | yes | Unique identity record. |
| `actor_id` | string | yes | Canonical actor identifier. |
| `actor_type` | enum | yes | `human`, `delegate`, `institution`, `service`, `executor`, `auditor`. |
| `display_label` | string | no | Human-readable label. |
| `status` | enum | yes | `active`, `suspended`, `revoked`, `archived`. |
| `credential_refs` | list | yes | References to credentials or verifiers. |
| `role_refs` | list | no | Assigned roles. |
| `created_at` | timestamp | yes | Creation time in UTC. |
| `updated_at` | timestamp | yes | Last update time in UTC. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `identity_state` | enum | `registered`, `active`, `suspended`, `revoked`, `archived`, `rejected`. |
| `identity_record` | object | Canonical identity record. |
| `record_hash` | string | Canonical identity record hash. |
| `reason` | string | Machine-readable reason. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `draft` | `register` | `registered` |
| `registered` | `activate` | `active` |
| `active` | `suspend` | `suspended` |
| `suspended` | `reactivate` | `active` |
| `active` | `revoke` | `revoked` |
| `suspended` | `revoke` | `revoked` |
| `revoked` | `archive` | `archived` |
| `active` | `archive` | `archived` |

# Validation Rules

1. `identity_record_id` and `actor_id` must be unique.
2. `actor_type` must be one of the canonical actor types.
3. Active identities require at least one credential reference.
4. Revoked identities must not verify successfully.
5. Service identities require cryptographic credential references.
6. Actor roles must not imply authority without authority records.
7. Identity record hash must use canonical serialization.

# Failure Conditions

| Condition | Result |
|---|---|
| Duplicate actor ID | `rejected` |
| Missing credential references | `rejected` |
| Unknown actor type | `rejected` |
| Revoked identity used | identity resolution `refused` |
| Suspended identity used | identity resolution `hold` or `refused` |
| Record hash mismatch | runtime `halted` |

# Security Requirements

- Store credential references, not raw secrets.
- Protect identity records from unauthorized updates.
- Identity status changes require audit.
- Identity record mutation must invalidate cached identity verdicts.
- Identity records do not grant authority.

# Audit Requirements

Record identity creation, activation, suspension, reactivation, revocation,
archive, credential reference changes, role reference changes, actor, reason,
record hash, and timestamp.

# Persistence Requirements

- Persist identity records with immutable history.
- Index by `actor_id`, `actor_type`, and `status`.
- Retain revoked and archived identities for audit retention.
- Store record schema version and record hash.

# Deterministic Rules

- Same identity record fields produce same record hash.
- Status precedence is `revoked`, `suspended`, `archived`, `active`.
- Credential reference ordering is canonicalized before hashing.

# Examples

```json
{
  "identity_record_id": "id_parent_001",
  "actor_id": "parent_001",
  "actor_type": "human",
  "status": "active"
}
```
