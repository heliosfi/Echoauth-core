# Purpose

Define the canonical storage and lookup interface for EchoAuth authority
records.

# Scope

Applies to parent, legal caregiver, institutional, delegated-source, emergency,
and runtime-service authority records.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `authority_record_id` | string | yes | Unique authority record. |
| `authority_source_id` | string | yes | Actor or institution holding authority. |
| `subject_id` | string | yes | Subject governed by the authority. |
| `authority_type` | enum | yes | `parent`, `caregiver`, `institution`, `court`, `service`, `emergency`. |
| `scope` | object | yes | Allowed action/resource/context bounds. |
| `priority` | integer | yes | Precedence value within policy. |
| `issued_at` | timestamp | yes | Effective start. |
| `expires_at` | timestamp | no | Effective end. |
| `status` | enum | yes | `active`, `suspended`, `revoked`, `expired`. |
| `source_document_hash` | string | no | Hash of legal or operational source. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `registry_result_id` | string | Unique registry operation result. |
| `state` | enum | `registered`, `updated`, `found`, `not_found`, `rejected`. |
| `authority_record` | object | Canonical record, when returned. |
| `reason` | string | Machine-readable reason. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `draft` | `validate` | `validated` |
| `validated` | `register` | `active` |
| `active` | `suspend` | `suspended` |
| `suspended` | `reactivate` | `active` |
| `active` | `expire` | `expired` |
| `active` | `revoke` | `revoked` |
| `suspended` | `revoke` | `revoked` |

# Validation Rules

1. Authority record IDs must be unique.
2. `authority_source_id`, `subject_id`, `authority_type`, and `scope` are mandatory.
3. Active records must have non-empty scope.
4. `expires_at`, when present, must be later than `issued_at`.
5. Priority conflicts must be resolved by policy before registration.
6. Parent/caregiver records for protected subjects must be marked as human authority.
7. Suspended, revoked, or expired records must not authorize execution.

# Failure Conditions

| Condition | Result |
|---|---|
| Duplicate active record with same priority | `rejected` |
| Missing scope | `rejected` |
| Invalid source document hash | `rejected` |
| Expired record lookup | `not_found` or inactive result |
| Revoked record lookup | inactive result |

# Security Requirements

- Registry writes require administrative or root authority authorization.
- Authority records must be tamper-evident.
- Revoked records must remain queryable for audit.
- Registry lookups must not expose unrelated subject records.
- Priority changes require audit and version bump.

# Audit Requirements

Record create, update, suspend, reactivate, expire, revoke, lookup miss, lookup
hit, priority change, scope change, source document hash, actor, and timestamp.

# Persistence Requirements

- Store all authority records append-only or with immutable history.
- Preserve revoked and expired records for retention period.
- Index by `subject_id`, `authority_source_id`, `authority_type`, and `status`.
- Persist registry schema version.

# Deterministic Rules

- Lookup order must be stable: active records, priority, issued time, record ID.
- Conflicting equal-priority records must return conflict metadata, not arbitrary selection.
- Time comparisons must use UTC.

# Examples

```json
{
  "authority_record_id": "auth_parent_001",
  "authority_source_id": "parent_001",
  "subject_id": "child_001",
  "authority_type": "parent",
  "status": "active"
}
```
