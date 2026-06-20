# Purpose

Define the session model binding identity, authority checks, envelopes, tokens,
events, and audit records during runtime operation.

# Scope

Applies to user sessions, delegate sessions, service sessions, and execution
sessions.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `session_id` | string | yes | Unique session. |
| `actor_id` | string | yes | Actor bound to session. |
| `actor_type` | enum | yes | Actor type. |
| `identity_verdict_id` | string | yes | Verified identity reference. |
| `started_at` | timestamp | yes | Session start. |
| `expires_at` | timestamp | yes | Session expiration. |
| `device_or_service_id` | string | no | Bound client or service. |
| `risk_level` | enum | yes | Session risk. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `session_state` | enum | `active`, `suspended`, `expired`, `revoked`, `closed`. |
| `bound_requests` | list | Runtime requests in session. |
| `reason` | string | Machine-readable state reason. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `created` | `identity_bound` | `active` |
| `active` | `suspend` | `suspended` |
| `suspended` | `resume` | `active` |
| `active` | `expire` | `expired` |
| `active` | `revoke` | `revoked` |
| `active` | `close` | `closed` |

# Validation Rules

1. Session requires verified identity.
2. Session TTL must not exceed identity verdict TTL.
3. Session actor must match identity verdict actor.
4. High-risk actions may require fresh identity verification.
5. Revoked sessions invalidate active envelopes and tokens.

# Failure Conditions

| Condition | Result |
|---|---|
| Identity mismatch | `revoked` |
| TTL exceeded | `expired` |
| Device mismatch | `suspended` or `revoked` |
| Risk escalation | require fresh identity or `hold` |
| Session store conflict | `hold` |

# Security Requirements

- Session identifiers must be unguessable.
- Session binding must include actor and verifier.
- Session revocation must propagate to envelopes and tokens.
- Session data must not grant authority by itself.

# Audit Requirements

Record session creation, activation, suspension, resume, expiration, revocation,
closure, bound identity, and bound requests.

# Persistence Requirements

- Persist session records and state transitions.
- Index by actor, session state, and expiration.
- Retain closed sessions for audit retention.
- Store session schema version.

# Deterministic Rules

- Session expiration uses UTC.
- Session revocation always supersedes active state.
- Fresh verification requirements must be computed from configured risk table.

# Examples

```json
{
  "session_id": "sess_001",
  "actor_id": "parent_001",
  "session_state": "active"
}
```
