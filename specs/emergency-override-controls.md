# Purpose

Define restricted emergency override handling without allowing uncontrolled
permission expansion.

# Scope

Applies only when configured deployment policy permits emergency action under
defined legal, clinical, safety, or institutional conditions.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `override_id` | string | yes | Unique override request. |
| `request_id` | string | yes | Related runtime request. |
| `declared_by` | string | yes | Actor declaring emergency. |
| `emergency_type` | enum | yes | Configured emergency category. |
| `subject_id` | string | yes | Protected subject. |
| `requested_action` | string | yes | Emergency action. |
| `evidence` | object | yes | Emergency evidence. |
| `expires_at` | timestamp | yes | Override expiration. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `override_state` | enum | `requested`, `approved`, `refused`, `hold`, `expired`, `revoked`. |
| `effective_scope` | object | Emergency scope if approved. |
| `review_required` | boolean | Whether post-action review is mandatory. |
| `reason` | string | Machine-readable reason. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `requested` | `validate_declarer` | `evaluating` |
| `evaluating` | `criteria_met` | `approved` |
| `evaluating` | `criteria_missing` | `hold` |
| `evaluating` | `criteria_failed` | `refused` |
| `approved` | `expire` | `expired` |
| `approved` | `revoke` | `revoked` |

# Validation Rules

1. Emergency override must be enabled by deployment policy.
2. Declarer identity must be verified.
3. Emergency type must be recognized.
4. Requested action must be permitted for emergency scope.
5. Override must have short expiration.
6. Override must require audit and post-action review.
7. Override cannot modify sealed invariants.

# Failure Conditions

| Condition | Result |
|---|---|
| Override disabled | `refused` |
| Declarer unauthorized | `refused` |
| Evidence missing | `hold` |
| Action outside emergency scope | `refused` |
| Expired override | `expired` |
| Audit unavailable | `hold` |

# Security Requirements

- Emergency override must be narrower than normal authority, not broader.
- Override approval must not create standing delegation.
- Override must be time-bound and single-purpose.
- Post-action review must be mandatory for approved emergency actions.

# Audit Requirements

Record declarer, emergency type, evidence hash, requested action, approved
scope, expiration, review requirement, use, revocation, and post-action review.

# Persistence Requirements

- Persist override request and result immutably.
- Link override to all resulting envelopes and tokens.
- Retain emergency evidence hash.
- Persist post-action review outcome.

# Deterministic Rules

- Emergency criteria evaluation must be policy-versioned.
- Same emergency facts and policy version produce same decision.
- Expired override always refuses execution.

# Examples

```json
{
  "override_id": "emg_001",
  "emergency_type": "immediate_safety",
  "override_state": "approved",
  "review_required": true
}
```
