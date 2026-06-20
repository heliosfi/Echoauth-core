# Purpose

Define the runtime validation interface for checking whether a delegation grant
permits a requested action.

# Scope

Applies whenever `requester_id` is not the controlling authority source.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `validation_id` | string | yes | Unique validation request. |
| `delegation_id` | string | yes | Delegation to validate. |
| `requester_id` | string | yes | Delegate actor. |
| `subject_id` | string | yes | Protected subject. |
| `action` | string | yes | Requested action. |
| `resource` | string | yes | Target resource. |
| `context` | object | yes | Runtime facts. |
| `authority_verdict_id` | string | yes | Grantor authority verdict or source. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `delegation_validation_state` | enum | `valid`, `invalid`, `expired`, `revoked`, `out_of_scope`, `hold`. |
| `effective_scope` | object | Scope allowed for this request. |
| `reason` | string | Machine-readable reason. |
| `evidence_hash` | string | Canonical hash of delegation evidence. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `received` | `load_grant` | `checking_status` |
| `received` | `grant_missing` | `invalid` |
| `checking_status` | `active` | `checking_scope` |
| `checking_status` | `expired` | `expired` |
| `checking_status` | `revoked` | `revoked` |
| `checking_scope` | `scope_match` | `valid` |
| `checking_scope` | `scope_mismatch` | `out_of_scope` |
| `checking_scope` | `evidence_unavailable` | `hold` |

# Validation Rules

1. Delegation must exist.
2. Delegate identity must match `requester_id`.
3. Delegation must be active at evaluation time.
4. Delegation must not be revoked.
5. Grantor must have authority for delegated scope.
6. Action, resource, and context must be inside scope.
7. Delegation evidence must hash deterministically.
8. Delegation validation must not modify delegation state.

# Failure Conditions

| Condition | Result |
|---|---|
| Missing delegation | `invalid` |
| Delegate mismatch | `invalid` |
| Expired grant | `expired` |
| Revoked grant | `revoked` |
| Action/resource mismatch | `out_of_scope` |
| Context mismatch | `out_of_scope` |
| Grantor authority unavailable | `hold` |

# Security Requirements

- Delegation validation must be called before policy permit.
- Validation must reject wildcard scope unless policy permits wildcard grants.
- Delegation chains must have maximum configured depth.
- Delegation grants must not be expanded during validation.

# Audit Requirements

Record validation ID, delegation ID, requester, subject, action, resource,
context hash, grantor reference, result state, and reason.

# Persistence Requirements

- Persist validation results when they influence authorization.
- Cache only within verdict TTL.
- Store evidence hash and delegation version.
- Invalidate cached validation on revocation.

# Deterministic Rules

- Scope matching must use canonical action/resource strings.
- Context predicates must run in stable configured order.
- Missing context required by delegation resolves to `out_of_scope` or `hold`.

# Examples

```json
{
  "delegation_id": "del_school_001",
  "requester_id": "teacher_42",
  "action": "document_observation",
  "delegation_validation_state": "valid"
}
```
