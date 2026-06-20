# Purpose

Define how EchoAuth routes unresolved or conflicting requests to the correct
authority or reviewer.

# Scope

Applies to authority conflict, missing evidence, policy conflict, emergency
conditions, halted execution, and institutional review.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `escalation_id` | string | yes | Unique escalation request. |
| `request_id` | string | yes | Related runtime request. |
| `trigger_state` | enum | yes | State that caused escalation. |
| `trigger_reason` | string | yes | Machine-readable trigger. |
| `subject_id` | string | yes | Protected subject. |
| `required_authority_type` | enum | yes | Authority needed to resolve. |
| `evidence` | object | yes | Supporting evidence. |
| `deadline_at` | timestamp | no | Required review deadline. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `escalation_state` | enum | `opened`, `notified`, `resolved`, `expired`, `cancelled`. |
| `reviewer_id` | string | Assigned reviewer or authority. |
| `resolution` | enum | `authorize`, `refuse`, `hold`, `halt`, `revoke`, `none`. |
| `reason` | string | Machine-readable result. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `received` | `select_reviewer` | `opened` |
| `opened` | `send_notification` | `notified` |
| `notified` | `reviewer_resolves` | `resolved` |
| `notified` | `deadline_elapsed` | `expired` |
| `opened` | `request_cancelled` | `cancelled` |

# Validation Rules

1. Escalation requires a nonterminal request or halted request eligible for review.
2. Reviewer must match required authority type.
3. Escalation cannot authorize directly without reviewer decision.
4. Evidence hash must be bound to escalation.
5. Deadline expiration must not silently permit execution.

# Failure Conditions

| Condition | Result |
|---|---|
| No reviewer available | `opened` with notification failure |
| Reviewer lacks authority | reject resolution |
| Deadline elapsed | `expired` and hold/refuse request |
| Evidence mismatch | reject resolution |
| Notification unavailable | remain `opened` and audit |

# Security Requirements

- Escalation must preserve authority boundaries.
- Reviewer assignment must be auditable.
- Escalation must not bypass policy or invariants.
- Resolved escalation must return to governance validation before execution.

# Audit Requirements

Record trigger, reviewer selection, notification attempts, evidence hash,
reviewer decision, deadline, expiration, and resulting runtime transition.

# Persistence Requirements

- Persist escalation queue records.
- Persist notification delivery state.
- Persist reviewer decisions immutably.
- Link escalation records to request and audit chain.

# Deterministic Rules

- Reviewer selection must use configured priority order.
- Expired escalations always return non-execution state.
- Same trigger and registry state must select same reviewer.

# Examples

```json
{
  "escalation_id": "esc_001",
  "trigger_reason": "authority_conflict",
  "required_authority_type": "parent",
  "escalation_state": "notified"
}
```
