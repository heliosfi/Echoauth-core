# Purpose

Define canonical EchoAuth runtime API contracts for identity, authority,
delegation, policy, invariants, envelopes, tokens, execution, audit,
escalation, and notifications.

# Scope

Applies to internal service APIs and external integration boundaries. Transport
may be HTTP, RPC, message bus, or in-process calls, but contract semantics must
remain stable.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `api_request_id` | string | yes | Unique API request. |
| `operation` | string | yes | API operation name. |
| `actor_id` | string | yes | Caller identity. |
| `session_id` | string | no | Runtime session. |
| `correlation_id` | string | yes | Cross-service correlation ID. |
| `idempotency_key` | string | yes | Duplicate request protection. |
| `payload` | object | yes | Operation-specific payload. |
| `payload_hash` | string | yes | Canonical payload hash. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `api_response_id` | string | Unique response. |
| `status` | enum | `accepted`, `rejected`, `refused`, `hold`, `halted`, `error`. |
| `result` | object | Operation-specific output. |
| `reason` | string | Machine-readable reason. |
| `audit_event_id` | string | Audit reference. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `received` | `authenticate` | `authenticated` |
| `received` | `authentication_failed` | `rejected` |
| `authenticated` | `validate_schema` | `validated` |
| `validated` | `dispatch` | `processing` |
| `processing` | `operation_complete` | `completed` |
| `processing` | `operation_refused` | `refused` |
| `processing` | `operation_hold` | `hold` |
| `processing` | `operation_halt` | `halted` |

# Validation Rules

1. API request ID and idempotency key are mandatory.
2. Payload must validate against operation schema.
3. Payload hash must match canonical payload.
4. Caller must be authenticated before dispatch.
5. Caller must be authorized for the operation.
6. Mutating operations must be idempotent by idempotency key.
7. All API outcomes must include a reason code.

# Failure Conditions

| Condition | Result |
|---|---|
| Authentication failure | `rejected` |
| Authorization failure | `refused` |
| Schema mismatch | `rejected` |
| Payload hash mismatch | `halted` |
| Duplicate idempotency key | return original result |
| Downstream hold | `hold` |
| Downstream halt | `halted` |

# Security Requirements

- Authenticate every API caller.
- Authorize every operation.
- Use replay protection for mutating calls.
- Bind request to payload hash and correlation ID.
- Do not expose sensitive evidence in error responses.

# Audit Requirements

Record API operation, caller, session, correlation ID, idempotency key, payload
hash, status, reason, downstream references, and timestamp.

# Persistence Requirements

- Persist idempotency records for configured TTL.
- Persist request/response audit metadata.
- Persist schema version used.
- Retain rejected mutating calls for audit.

# Deterministic Rules

- Same idempotency key and payload hash returns same response.
- Schema validation order is stable.
- Operation dispatch maps deterministically by operation name and version.

# Examples

```json
{
  "operation": "authority.resolve",
  "idempotency_key": "idem_001",
  "status": "accepted"
}
```
