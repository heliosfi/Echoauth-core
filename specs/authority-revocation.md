# Purpose

Define how EchoAuth revokes authority records, delegation grants, identity
verdicts, runtime envelopes, and execution tokens.

# Scope

Applies to all revocable authorization dependencies before, during, and after
execution.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `revocation_id` | string | yes | Unique revocation event. |
| `target_type` | enum | yes | `authority`, `delegation`, `identity`, `envelope`, `token`, `session`. |
| `target_id` | string | yes | Record being revoked. |
| `revoked_by` | string | yes | Actor or component issuing revocation. |
| `reason` | string | yes | Machine-readable reason. |
| `effective_at` | timestamp | yes | Revocation effective time. |
| `scope` | object | no | Partial revocation scope. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `revocation_state` | enum | `accepted`, `rejected`, `propagated`, `completed`. |
| `affected_records` | list | Envelopes, tokens, sessions, and grants invalidated. |
| `reason` | string | Result reason. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `received` | `issuer_valid` | `accepted` |
| `received` | `issuer_invalid` | `rejected` |
| `accepted` | `invalidate_dependents` | `propagated` |
| `propagated` | `audit_written` | `completed` |
| `accepted` | `propagation_failed` | `hold` |

# Validation Rules

1. Revoker must have authority to revoke the target.
2. Target must exist or revocation must be recorded as defensive revocation.
3. `effective_at` must be canonical UTC.
4. Revocation must invalidate dependent active envelopes and tokens.
5. Partial revocation scope must be narrower than or equal to original scope.
6. Revocation cannot be silently deleted.

# Failure Conditions

| Condition | Result |
|---|---|
| Revoker unauthorized | `rejected` |
| Target not found | `accepted` defensive record |
| Dependent invalidation failed | `hold` |
| Audit unavailable | `hold` |
| Partial scope exceeds original | `rejected` |

# Security Requirements

- Revocation must propagate before new execution is allowed.
- Revocation records must be immutable.
- Revoked tokens must be rejected even if otherwise valid.
- Revocation checks must run in every authorization and execution path.

# Audit Requirements

Record revocation issuer, target type, target ID, reason, effective time,
dependent records invalidated, propagation result, and timestamp.

# Persistence Requirements

- Persist revocation records permanently for audit retention.
- Index revocations by `target_id`, `target_type`, and `effective_at`.
- Preserve dependency invalidation records.
- Replicate revocations to all runtime nodes before accepting dependent execution.

# Deterministic Rules

- If revocation effective time is before token use, execution must fail.
- Multiple revocations for same target must sort by `effective_at`, then `revocation_id`.
- Defensive revocation must produce the same inactive result as target revocation.

# Examples

```json
{
  "revocation_id": "rev_001",
  "target_type": "delegation",
  "target_id": "del_school_001",
  "reason": "caregiver_withdrawal",
  "revocation_state": "completed"
}
```
