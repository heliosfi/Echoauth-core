# Purpose

Define the single-use token that allows CEG to execute exactly one authorized
action inside a runtime envelope.

# Scope

Applies after authorization and before executor invocation.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `execution_token_id` | string | yes | Unique token identifier. |
| `envelope_id` | string | yes | Runtime envelope reference. |
| `request_id` | string | yes | Authorization request reference. |
| `authority_verdict_id` | string | yes | Authority verdict reference. |
| `action` | string | yes | Authorized action. |
| `resource` | string | yes | Authorized resource. |
| `payload_hash` | string | yes | Authorized payload hash. |
| `nonce` | string | yes | Single-use anti-replay value. |
| `issued_at` | timestamp | yes | Token issue time. |
| `expires_at` | timestamp | yes | Token expiration. |
| `issuer_id` | string | yes | CEG or runtime issuer. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `token_state` | enum | `issued`, `claimed`, `used`, `expired`, `revoked`, `invalid`. |
| `claim_id` | string | Execution claim reference. |
| `reason` | string | Machine-readable state reason. |
| `audit_event_id` | string | Audit record for token event. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `issued` | `claim` | `claimed` |
| `issued` | `expire` | `expired` |
| `issued` | `revoke` | `revoked` |
| `claimed` | `execute` | `used` |
| `claimed` | `payload_mismatch` | `invalid` |
| `claimed` | `concurrency_conflict` | `invalid` |
| `claimed` | `channel_loss` | `revoked` |

# Validation Rules

1. Token must reference an authorized runtime envelope.
2. Token must be unique per envelope.
3. Token nonce must not have been used before.
4. Token action/resource must match envelope action/resource.
5. Token payload hash must match envelope payload hash.
6. Token must be unexpired at claim and execution.
7. Token may be claimed once.
8. Token must be consumed when execution begins.

# Failure Conditions

| Condition | Result |
|---|---|
| Duplicate token for envelope | `invalid` |
| Reused nonce | `invalid` |
| Payload mismatch | `invalid` |
| Action/resource mismatch | `invalid` |
| Expired token | `expired` |
| Revoked authorization | `revoked` |
| Second claim attempt | `invalid` |
| Missing audit path | `invalid` |

# Security Requirements

- Tokens must be cryptographically random or signed.
- Tokens must not be reusable across requests.
- Tokens must not be logged as bearer secrets.
- Token validation must be atomic with execution lock acquisition.
- Token invalidation must propagate to all executors.

# Audit Requirements

Record token issuance, claim, consumption, expiration, revocation, invalidation,
nonce, envelope reference, executor identity, and payload hash.

# Persistence Requirements

- Persist token state and transitions.
- Persist nonce use.
- Index by envelope, request, token state, and expiration.
- Retain invalid and rejected token use attempts.

# Deterministic Rules

- Same envelope may issue at most one active token.
- Revocation supersedes issued and claimed states.
- Expired tokens always reject claim and execution.
- Atomic claim ordering determines the winning executor.

# Examples

```json
{
  "execution_token_id": "tok_001",
  "envelope_id": "env_001",
  "token_state": "issued"
}
```
