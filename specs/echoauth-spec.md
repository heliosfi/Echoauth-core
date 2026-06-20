# Purpose

Define the canonical top-level EchoAuth runtime request contract that binds
identity, authority, delegation, policy, invariants, runtime envelope, execution
token, audit, and terminal outcome.

# Scope

Applies to the complete EchoAuth request lifecycle. Component-specific behavior
is defined in the referenced specifications.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `request_id` | string | yes | Unique EchoAuth request. |
| `requester_id` | string | yes | Actor proposing the action. |
| `subject_id` | string | yes | Protected subject or target identity. |
| `action` | string | yes | Requested operation. |
| `resource` | string | yes | Target resource. |
| `payload` | object | yes | Proposed executable payload. |
| `context` | object | yes | Deterministic runtime facts. |
| `session_id` | string | no | Runtime session reference. |
| `correlation_id` | string | yes | Cross-component correlation ID. |
| `idempotency_key` | string | yes | Duplicate request protection. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `request_state` | enum | Final or current runtime state. |
| `identity_verdict_id` | string | Identity result reference. |
| `authority_verdict_id` | string | Authority result reference. |
| `policy_decision_id` | string | Policy result reference. |
| `invariant_result_id` | string | Invariant result reference. |
| `envelope_id` | string | Runtime envelope reference. |
| `execution_token_id` | string | Execution token reference, when issued. |
| `audit_chain_id` | string | Audit chain used. |
| `reason` | string | Machine-readable result reason. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `new` | `submit` | `proposed` |
| `proposed` | `identity_verified` | `resolving_authority` |
| `resolving_authority` | `authority_valid` | `validating_delegation` |
| `validating_delegation` | `delegation_valid_or_not_required` | `evaluating_policy` |
| `evaluating_policy` | `policy_permit` | `validating_invariants` |
| `validating_invariants` | `invariants_valid` | `creating_envelope` |
| `creating_envelope` | `envelope_created` | `authorized` |
| `authorized` | `token_issued` | `token_issued` |
| `token_issued` | `execution_claimed` | `executing` |
| `executing` | `execution_completed` | `completed` |
| any nonterminal | `refuse` | `refused` |
| any nonterminal | `hold` | `hold` |
| any nonterminal | `halt` | `halted` |
| any nonterminal | `revoke` | `revoked` |

# Validation Rules

1. `request_id`, `correlation_id`, and `idempotency_key` are mandatory.
2. Payload must be canonicalized and hashed before policy or envelope creation.
3. Identity must verify before authority resolution.
4. Authority must resolve before policy permit.
5. Delegation validation is required when requester is not the authority source.
6. Policy and invariant versions must be pinned before envelope creation.
7. Execution requires runtime envelope, execution token, and execution claim.
8. Every terminal outcome must write audit.

# Failure Conditions

| Condition | Result |
|---|---|
| Invalid identity | `refused` |
| Authority missing | `refused` |
| Authority unavailable | `hold` |
| Delegation invalid | `refused` |
| Policy refusal | `refused` |
| Invariant failure | `halted` |
| Audit unavailable | `hold` or `halted` |
| Token failure | `halted` |
| Revocation | `revoked` |

# Security Requirements

- Requests must be idempotent by idempotency key.
- Runtime must fail closed on missing dependencies.
- Interpretation outputs must not authorize execution.
- Payload hash must bind request, envelope, token, and audit.
- Component calls must be authenticated and authorized.

# Audit Requirements

Record request submission, identity verdict, authority verdict, delegation
result, policy decision, invariant result, envelope creation, token issuance,
execution claim, execution result, refusal/hold/halt/revocation, and terminal
state.

# Persistence Requirements

- Persist request record and current state.
- Persist idempotency key and response.
- Persist all component output references.
- Persist payload hash, context hash, and schema version.
- Retain terminal request records for audit retention.

# Deterministic Rules

- Same idempotency key and payload hash returns same request result.
- Component processing order is fixed by the state machine.
- Missing required evidence never produces authorization.
- Terminal states are immutable.

# Examples

```json
{
  "request_id": "req_001",
  "requester_id": "parent_001",
  "subject_id": "child_001",
  "action": "share_record",
  "resource": "therapy_note_001"
}
```
