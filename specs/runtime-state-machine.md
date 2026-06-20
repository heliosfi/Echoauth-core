# Purpose

Define the canonical EchoAuth runtime state machine for request processing from
proposal through terminal outcome.

# Scope

Applies to every runtime request, including authority checks, policy checks,
invariant validation, execution-token issuance, execution, recovery, and audit.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `request_id` | string | yes | Runtime request identifier. |
| `current_state` | enum | yes | Current runtime state. |
| `event_type` | enum | yes | Transition event. |
| `actor_id` | string | yes | Actor or component requesting transition. |
| `evidence` | object | yes | Transition evidence. |
| `occurred_at` | timestamp | yes | Event time. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `next_state` | enum | Resulting state. |
| `transition_id` | string | Unique transition record. |
| `accepted` | boolean | Whether transition was accepted. |
| `reason` | string | Machine-readable result. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `new` | `submit` | `proposed` |
| `proposed` | `begin_governance` | `under_governance` |
| `under_governance` | `identity_verified` | `resolving_authority` |
| `resolving_authority` | `authority_valid` | `evaluating_policy` |
| `evaluating_policy` | `policy_permit` | `validating_invariants` |
| `validating_invariants` | `invariants_valid` | `authorized` |
| `authorized` | `issue_token` | `token_issued` |
| `token_issued` | `claim_token` | `executing` |
| `executing` | `complete` | `completed` |
| any nonterminal | `refuse` | `refused` |
| any nonterminal | `hold` | `hold` |
| any nonterminal | `halt` | `halted` |
| any nonterminal | `revoke` | `revoked` |
| any nonterminal | `expire` | `expired` |
| `hold` | `resume` | `under_governance` |
| `halted` | `escalate` | `escalated` |

# Validation Rules

1. Transitions must be in the allowed transition table.
2. Terminal states must reject non-audit transitions.
3. `executing` requires a valid execution claim.
4. `authorized` requires identity, authority, policy, and invariants to pass.
5. `completed` requires executor result and audit write.
6. Transition evidence must be immutable after acceptance.

# Failure Conditions

| Condition | Result |
|---|---|
| Unknown current state | reject transition |
| Invalid transition | reject and audit |
| Missing evidence | reject or hold |
| Terminal state mutation | reject and audit |
| Concurrent transition conflict | halt or retry with lock |

# Security Requirements

- State transitions must be atomic.
- Only authorized components may emit transition events.
- Transition records must be tamper-evident.
- Runtime state must fail closed on lock or storage conflict.

# Audit Requirements

Record transition ID, request ID, previous state, event, next state, actor,
accepted flag, reason, evidence hash, and timestamp.

# Persistence Requirements

- Persist every accepted and rejected transition.
- Store current state and append-only transition history.
- Use optimistic or pessimistic concurrency control.
- Persist state schema version.

# Deterministic Rules

- Same current state and event must produce same next state.
- Transition guards must run in configured stable order.
- Tie-breaking for concurrent transitions must use timestamp then transition ID.

# Examples

```json
{
  "request_id": "req_001",
  "current_state": "authorized",
  "event_type": "issue_token",
  "next_state": "token_issued"
}
```
