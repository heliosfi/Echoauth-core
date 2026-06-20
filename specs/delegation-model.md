# Purpose

Define the canonical delegation grant model for actors who may assist, observe,
document, or execute within bounded authority.

# Scope

Applies to caregiver assistants, school staff, clinical staff, runtime services,
institutional delegates, and emergency contacts.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `delegation_id` | string | yes | Unique delegation identifier. |
| `grantor_id` | string | yes | Authority source granting permission. |
| `delegate_id` | string | yes | Actor receiving bounded permission. |
| `subject_id` | string | yes | Protected subject or resource owner. |
| `role` | string | yes | Delegate role label. |
| `allowed_actions` | list | yes | Actions permitted by delegation. |
| `allowed_resources` | list | yes | Resources permitted by delegation. |
| `context_constraints` | object | yes | Location, time, purpose, risk, or environment constraints. |
| `issued_at` | timestamp | yes | Delegation start. |
| `expires_at` | timestamp | yes | Delegation expiration. |
| `revoked_at` | timestamp | no | Revocation time, if revoked. |
| `source_authority_reference` | string | yes | Grantor authority proof. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `delegation_state` | enum | `draft`, `issued`, `active`, `expired`, `revoked`, `out_of_scope`, `invalid`. |
| `effective_scope` | object | Resolved permission bounds. |
| `reason` | string | Machine-readable validation reason. |
| `audit_event_id` | string | Audit record for delegation decision. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `draft` | `grantor_validated` | `issued` |
| `issued` | `activate` | `active` |
| `active` | `request_in_scope` | `active` |
| `active` | `request_out_of_scope` | `out_of_scope` |
| `active` | `expire` | `expired` |
| `active` | `revoke` | `revoked` |
| `issued` | `grantor_invalid` | `invalid` |

# Validation Rules

1. Grantor must be a valid authority source for the delegated subject/action.
2. Delegate identity must be verified.
3. Delegation must specify action and resource scope.
4. Delegation must specify expiration.
5. Delegation must not exceed grantor authority.
6. Delegation must not grant self-expansion unless explicitly permitted.
7. Revoked delegations must fail closed.
8. Role labels must not grant permission without explicit scope.

# Failure Conditions

| Condition | Result |
|---|---|
| Invalid grantor | `invalid` |
| Delegate identity mismatch | `invalid` |
| Expired delegation | `expired` |
| Revoked delegation | `revoked` |
| Action mismatch | `out_of_scope` |
| Resource mismatch | `out_of_scope` |
| Context mismatch | `out_of_scope` |
| Scope exceeds grantor authority | `invalid` |

# Security Requirements

- Delegation cannot override parent/legal caregiver authority unless authority policy permits it.
- Delegation cannot suppress audit.
- Delegation cannot bypass CEG.
- Delegation chains must be bounded and auditable.
- Delegation records must be signed or tamper-evident in distributed deployments.

# Audit Requirements

Record grantor identity, delegate identity, source authority reference, granted
scope, requested action/resource, validation result, revocation status,
expiration status, and reason code.

# Persistence Requirements

- Persist delegation records with immutable history.
- Persist revocation and expiration metadata.
- Index by grantor, delegate, subject, state, and expiration.
- Retain invalid and revoked grants for audit retention.

# Deterministic Rules

- Scope matching uses canonical action and resource strings.
- Expiration uses UTC.
- Same grant, request, and context produce same delegation state.
- Revocation supersedes active and issued states.

# Examples

```json
{
  "delegation_id": "del_school_001",
  "grantor_id": "parent_001",
  "delegate_id": "teacher_42",
  "allowed_actions": ["document_observation"]
}
```
