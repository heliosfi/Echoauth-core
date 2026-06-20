# Purpose

Define cross-cutting security requirements for EchoAuth runtime implementation.

# Scope

Applies to identity, authority, delegation, policy, invariants, envelopes,
tokens, execution, audit, event bus, notifications, storage, and recovery.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `security_profile_id` | string | yes | Deployment security profile. |
| `component_id` | string | yes | Runtime component. |
| `operation` | string | yes | Operation being secured. |
| `data_classification` | enum | yes | `public`, `internal`, `sensitive`, `restricted`. |
| `risk_level` | enum | yes | `low`, `standard`, `high`, `critical`. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `security_decision` | enum | `allow`, `refuse`, `hold`, `halt`. |
| `required_controls` | list | Controls that must be enforced. |
| `reason` | string | Machine-readable reason. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `received` | `load_profile` | `evaluating` |
| `received` | `profile_missing` | `hold` |
| `evaluating` | `controls_satisfied` | `allow` |
| `evaluating` | `controls_missing` | `refuse` |
| `evaluating` | `integrity_failure` | `halt` |

# Validation Rules

1. Security profile must be active.
2. Component must be registered.
3. Operation must declare data classification.
4. Required controls must match risk level.
5. Restricted data requires encrypted transport and storage.
6. Critical operations require audit availability.

# Failure Conditions

| Condition | Result |
|---|---|
| Missing security profile | `hold` |
| Unknown component | `refuse` |
| Missing required control | `refuse` |
| Integrity failure | `halt` |
| Audit unavailable for critical operation | `halt` |

# Security Requirements

- Authenticate all components.
- Authorize all operations.
- Encrypt sensitive and restricted data in transit.
- Encrypt restricted data at rest.
- Use least privilege for service accounts.
- Rotate secrets.
- Reject replay.
- Protect audit chain integrity.

# Audit Requirements

Record security profile, component, operation, data classification, risk level,
decision, required controls, missing controls, and timestamp.

# Persistence Requirements

- Persist security profiles immutably by version.
- Persist security decisions affecting authorization.
- Store control evidence hashes.
- Retain denied and halted operation records.

# Deterministic Rules

- Same profile, component, operation, classification, and risk produce same decision.
- Control evaluation order is fixed by security profile.
- Missing control evidence never resolves to allow.

# Examples

```json
{
  "component_id": "ceg",
  "operation": "token.claim",
  "security_decision": "allow"
}
```
