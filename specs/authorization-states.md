# Purpose

Define the canonical authorization state vocabulary used by EchoAuth runtime
requests, envelopes, refusal handling, recovery, and audit.

# Scope

Applies to every authorization request from proposal through terminal outcome.
`specs/runtime-state-machine.md` defines the full runtime process; this document
defines the authorization state contract used across components.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `request_id` | string | yes | Authorization request identifier. |
| `current_state` | enum | yes | Current authorization state. |
| `transition_event` | enum | yes | Requested state transition event. |
| `actor_id` | string | yes | Actor or component requesting transition. |
| `reason` | string | yes | Machine-readable transition reason. |
| `evidence_hash` | string | yes | Canonical evidence hash for transition. |
| `occurred_at` | timestamp | yes | Transition time in UTC. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `authorization_state` | enum | New authorization state. |
| `transition_id` | string | Unique transition record. |
| `accepted` | boolean | Whether transition was accepted. |
| `terminal` | boolean | Whether state is terminal. |
| `reason` | string | Machine-readable result reason. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `new` | `submit` | `proposed` |
| `proposed` | `begin_governance` | `under_governance` |
| `proposed` | `refuse` | `refused` |
| `under_governance` | `authorize` | `authorized` |
| `under_governance` | `refuse` | `refused` |
| `under_governance` | `hold` | `hold` |
| `under_governance` | `escalate` | `escalated` |
| `authorized` | `begin_execution` | `executing` |
| `authorized` | `revoke` | `revoked` |
| `authorized` | `expire` | `expired` |
| `executing` | `complete` | `completed` |
| `executing` | `halt` | `halted` |
| `executing` | `revoke` | `revoked` |
| `hold` | `resume` | `under_governance` |
| `hold` | `refuse` | `refused` |
| `hold` | `escalate` | `escalated` |
| `escalated` | `resume` | `under_governance` |
| `escalated` | `refuse` | `refused` |

Terminal states: `completed`, `refused`, `halted`, `revoked`, `expired`.

# Validation Rules

1. Only transitions listed in the state table are valid.
2. Terminal states reject all non-audit transitions.
3. `authorized` requires valid identity, authority, policy, and invariant results.
4. `executing` requires a valid runtime envelope and execution token.
5. `completed` requires executor result and audit write.
6. `hold` requires a recoverable missing dependency.
7. `halted` requires integrity, invariant, token, channel, or audit failure evidence.

# Failure Conditions

| Condition | Result |
|---|---|
| Invalid transition | reject transition and audit |
| Missing evidence hash | reject transition |
| Terminal state mutation | reject transition and audit |
| Authorization dependency missing | `hold` or `refused` |
| Integrity failure | `halted` |
| Revocation received | `revoked` |

# Security Requirements

- State transitions must be atomic.
- Transition authority must be checked by component role.
- Terminal states must be immutable.
- Transition evidence must be hash-bound to audit record.
- State changes must not be accepted from unregistered components.

# Audit Requirements

Record request ID, transition ID, previous state, event, next state, actor,
reason, evidence hash, accepted flag, and UTC timestamp.

# Persistence Requirements

- Persist current authorization state.
- Persist append-only transition history.
- Persist rejected transition attempts.
- Index by `request_id`, `authorization_state`, and terminal flag.
- Store state machine version.

# Deterministic Rules

- Same current state and event resolve to the same next state.
- State guards run in stable configured order.
- UTC time is used for expiration and transition ordering.
- Invalid transitions never produce implicit recovery.

# Examples

```json
{
  "request_id": "req_001",
  "current_state": "under_governance",
  "transition_event": "authorize",
  "authorization_state": "authorized"
}
```
