# Purpose

Define the atomic claim process that binds an execution token to one executor
for one authorized action.

# Scope

Applies after token issuance and before command execution.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `claim_id` | string | yes | Unique execution claim. |
| `execution_token_id` | string | yes | Token being claimed. |
| `executor_id` | string | yes | Executor requesting claim. |
| `envelope_id` | string | yes | Runtime envelope. |
| `payload_hash` | string | yes | Payload the executor will run. |
| `claimed_at` | timestamp | yes | Claim time. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `claim_state` | enum | `accepted`, `rejected`, `expired`, `released`, `consumed`. |
| `lease_expires_at` | timestamp | Claim lease expiration. |
| `reason` | string | Machine-readable reason. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `requested` | `token_available` | `accepted` |
| `requested` | `token_unavailable` | `rejected` |
| `accepted` | `begin_execution` | `consumed` |
| `accepted` | `release` | `released` |
| `accepted` | `lease_elapsed` | `expired` |

# Validation Rules

1. Token must exist and be in `issued` state.
2. Token must not already be claimed.
3. Executor identity must be verified.
4. Payload hash must match token and envelope.
5. Claim must be atomic with token state update.
6. Claim lease must have a bounded expiration.

# Failure Conditions

| Condition | Result |
|---|---|
| Token already claimed | `rejected` |
| Token expired | `expired` |
| Payload mismatch | `rejected` and halt |
| Executor unauthorized | `rejected` |
| Atomic write conflict | retry or halt |

# Security Requirements

- Claim operation must be concurrency-safe.
- Executors cannot claim tokens outside their allowed executor role.
- Claims must not be transferable.
- Expired claims must not execute.

# Audit Requirements

Record claim request, token ID, executor ID, envelope ID, payload hash, result,
lease expiration, and reason.

# Persistence Requirements

- Persist claim records atomically with token state.
- Store claim lease expiration.
- Preserve rejected claim attempts.
- Index by token, executor, and envelope.

# Deterministic Rules

- First valid atomic claim wins.
- Concurrent claims resolve by storage lock order, not application preference.
- Expired claims must always reject execution.

# Examples

```json
{
  "claim_id": "claim_001",
  "execution_token_id": "tok_001",
  "executor_id": "exec_a",
  "claim_state": "accepted"
}
```
