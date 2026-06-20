# Purpose

Define halt, hold, refusal, revocation, and escalation behavior for runtime
safety failures.

# Scope

Applies to all runtime components that can block, stop, or escalate execution.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `halt_event_id` | string | yes | Unique halt or safety event identifier. |
| `request_id` | string | yes | Related request. |
| `envelope_id` | string | no | Runtime envelope reference. |
| `execution_token_id` | string | no | Token reference. |
| `detected_by` | string | yes | Component that detected failure. |
| `failure_type` | enum | yes | Failure category. |
| `severity` | enum | yes | `low`, `medium`, `high`, `critical`. |
| `state_before` | string | yes | Previous runtime state. |
| `evidence` | object | yes | Evidence supporting halt/hold/refusal. |
| `occurred_at` | timestamp | yes | Detection time in UTC. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `runtime_state` | enum | `refused`, `hold`, `halted`, `revoked`, `escalated`. |
| `reason` | string | Machine-readable reason. |
| `recovery_allowed` | boolean | Whether processing may resume. |
| `required_reviewer` | string | Authority/reviewer needed for escalation. |
| `audit_event_id` | string | Audit event reference. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `under_governance` | `authority_missing` | `refused` |
| `under_governance` | `evidence_unavailable` | `hold` |
| `authorized` | `revocation_received` | `revoked` |
| `authorized` | `token_failure` | `halted` |
| `token_issued` | `replay_detected` | `halted` |
| `token_issued` | `channel_loss` | `hold` |
| `executing` | `payload_drift` | `halted` |
| `executing` | `concurrency_conflict` | `halted` |
| `hold` | `evidence_resolved` | `under_governance` |
| `halted` | `review_required` | `escalated` |

# Validation Rules

1. Halt events must include failure type, severity, detector, and evidence.
2. Critical failures must transition to `halted`.
3. Authority absence must not transition to `authorized`.
4. Channel loss before execution may transition to `hold`.
5. Integrity failure during or after token issuance must transition to `halted`.
6. Revocation must invalidate active envelopes and tokens.
7. Recovery from `hold` requires revalidation.
8. Recovery from `halted` requires a new request or explicit review protocol.

# Failure Conditions

| Condition | Result |
|---|---|
| Missing authority | `refused` |
| Authority unreachable | `hold` |
| Replay | `halted` |
| Payload drift | `halted` |
| Token duplication | `halted` |
| Concurrency conflict | `halted` |
| Revocation | `revoked` |
| Policy conflict | `escalated` |
| Audit unavailable | `hold` or `halted` |
| Detector failure | `halted` |

# Security Requirements

- Halt decisions must be fail-closed.
- Halt events must be immutable once emitted.
- Resuming from hold must rerun authority, policy, invariant, and envelope validation.
- Halted execution must not be resumed with the same token.
- Critical halt events must notify audit and authority channels.

# Audit Requirements

Record triggering condition, detector component, prior state, resulting state,
severity, evidence hash, invalidated envelope/token identifiers, reviewer or
escalation target, recovery eligibility, and timestamp.

# Persistence Requirements

- Persist halt events immutably.
- Link halt events to request, envelope, token, and audit chain.
- Persist invalidated dependent records.
- Retain detector evidence hash.
- Index by request, failure type, severity, and runtime state.

# Deterministic Rules

- Same failure type, severity, state, and recovery policy produce same runtime state.
- Criticality mapping is fixed by runtime halt policy.
- Revocation supersedes hold and authorized states.
- Halted tokens cannot become valid again.

# Examples

```json
{
  "halt_event_id": "halt_001",
  "failure_type": "payload_drift",
  "severity": "critical",
  "runtime_state": "halted"
}
```
