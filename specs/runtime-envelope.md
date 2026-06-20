# Purpose

Define the bounded execution container that binds one authorization decision to
one executable action.

# Scope

Applies to every action submitted to EchoAuth for authorization or execution.
The runtime envelope is mandatory for CEG sequencing and executor invocation.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `envelope_id` | string | yes | Unique envelope identifier. |
| `request_id` | string | yes | Authorization request identifier. |
| `subject_id` | string | yes | Protected subject or target identity. |
| `requester_id` | string | yes | Actor proposing the action. |
| `authority_verdict_id` | string | yes | Authority-resolution verdict reference. |
| `delegation_id` | string | no | Delegation reference, when requester is delegated. |
| `action` | string | yes | Requested operation. |
| `resource` | string | yes | Target resource. |
| `payload_hash` | string | yes | Canonical hash of executable payload. |
| `policy_version` | string | yes | Policy set used for evaluation. |
| `invariant_version` | string | yes | Invariant set used for validation. |
| `channel_id` | string | yes | Runtime channel or session identifier. |
| `nonce` | string | yes | Single-use anti-replay value. |
| `expires_at` | timestamp | yes | Envelope expiration. |
| `audit_sink_id` | string | yes | Audit destination. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `envelope_state` | enum | Current envelope state. |
| `execution_token_id` | string | Token reference when issued. |
| `reason` | string | Machine-readable state reason. |
| `validation_errors` | list | Failed validation checks. |
| `audit_event_ids` | list | Audit records emitted for this envelope. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `created` | `submit` | `under_governance` |
| `under_governance` | `authorize` | `authorized` |
| `under_governance` | `refuse` | `refused` |
| `under_governance` | `hold` | `hold` |
| `under_governance` | `escalate` | `escalated` |
| `authorized` | `issue_token` | `token_issued` |
| `authorized` | `expire` | `expired` |
| `authorized` | `revoke` | `revoked` |
| `token_issued` | `begin_execution` | `executing` |
| `token_issued` | `detect_failure` | `halted` |
| `executing` | `complete` | `completed` |
| `executing` | `detect_failure` | `halted` |
| `hold` | `resume_governance` | `under_governance` |
| `escalated` | `resume_governance` | `under_governance` |

# Validation Rules

1. `envelope_id`, `request_id`, and `nonce` must be globally unique.
2. `expires_at` must be later than creation time.
3. `payload_hash` must be computed from canonical payload serialization.
4. `authority_verdict_id` must reference a valid authority verdict.
5. `delegation_id` is required when requester is not the authority source.
6. `policy_version` and `invariant_version` must be known to the runtime.
7. `audit_sink_id` must be reachable before execution.
8. The envelope may issue no more than one execution token.

# Failure Conditions

| Condition | Result |
|---|---|
| Duplicate nonce | `halted` |
| Payload hash mismatch | `halted` |
| Missing authority verdict | `refused` |
| Expired envelope | `expired` |
| Invalid delegation | `refused` |
| Policy mismatch | `refused` |
| Invariant mismatch | `halted` |
| Audit sink unavailable | `hold` or `halted` |
| Channel loss | `hold` |
| Token duplication | `halted` |

# Security Requirements

- Treat envelopes as enforcement state, not log metadata.
- Sign or MAC envelope records in distributed deployments.
- Store envelope state changes append-only.
- Reject envelope mutation after `token_issued` except for terminal transition.
- Bind envelope to requester, authority verdict, payload hash, and channel.

# Audit Requirements

Emit audit records for envelope creation, governance submission, authorization,
refusal, hold, escalation, token issuance, execution start, execution
completion, terminal failure, revocation, expiration, and invalid transitions.

# Persistence Requirements

- Persist envelope records and state transitions.
- Persist nonce and payload hash.
- Persist policy and invariant versions.
- Index by request, envelope state, authority verdict, and expiration.
- Retain terminal envelopes for audit retention.

# Deterministic Rules

- Same request, authority verdict, payload hash, policy version, and invariant version produce same envelope fields except unique IDs.
- Envelope transitions follow the fixed state table.
- Expiration uses UTC.
- Revocation supersedes authorized and token-issued states.

# Examples

```json
{
  "envelope_id": "env_001",
  "request_id": "req_001",
  "envelope_state": "authorized"
}
```
