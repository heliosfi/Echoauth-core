# Purpose

Define how EchoAuth resolves and verifies actor identity before authority,
delegation, policy, or execution processing.

# Scope

Applies to human actors, delegates, institutional users, runtime services,
governance services, execution services, audit services, and notification
services.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `identity_request_id` | string | yes | Unique identity resolution request. |
| `actor_id` | string | yes | Claimed actor identifier. |
| `actor_type` | enum | yes | `human`, `delegate`, `institution`, `service`, `executor`, `auditor`. |
| `subject_id` | string | no | Protected subject related to request. |
| `credential_set` | object | yes | Credentials, signed session, device, biometric, or service proof. |
| `context` | object | yes | Deterministic facts for the identity check. |
| `required_assurance` | enum | yes | `low`, `standard`, `high`, `critical`. |
| `session_id` | string | no | Existing runtime session reference. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `identity_verdict_id` | string | Unique verdict identifier. |
| `state` | enum | `verified`, `refused`, `hold`, `expired`, `conflict`. |
| `resolved_actor_id` | string | Canonical actor identifier. |
| `assurance_level` | enum | Verified assurance level. |
| `evidence_hash` | string | Canonical hash of identity evidence. |
| `expires_at` | timestamp | Identity verdict expiration. |
| `reason` | string | Machine-readable reason. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `received` | `credentials_present` | `validating` |
| `received` | `credentials_missing` | `refused` |
| `validating` | `evidence_verified` | `verified` |
| `validating` | `evidence_incomplete` | `hold` |
| `validating` | `evidence_conflict` | `conflict` |
| `validating` | `evidence_invalid` | `refused` |
| `verified` | `ttl_elapsed` | `expired` |
| `hold` | `evidence_supplied` | `validating` |

# Validation Rules

1. `actor_id`, `actor_type`, `credential_set`, and `required_assurance` are mandatory.
2. Credentials must be validated against the configured identity provider or local verifier.
3. Service identities must use cryptographic credentials.
4. Human identities must meet the required assurance level for the requested action.
5. Session-bound identity must match `session_id`.
6. Identity evidence must be canonicalized before hashing.
7. Expired identity verdicts must not be reused.
8. Identity verification does not imply authority.

# Failure Conditions

| Condition | Result |
|---|---|
| Missing credential | `refused` |
| Invalid credential | `refused` |
| Assurance below requirement | `refused` |
| Conflicting identity evidence | `conflict` |
| Identity provider unavailable | `hold` |
| Expired session | `expired` |
| Actor/session mismatch | `refused` |

# Security Requirements

- Identity verdicts must be bound to actor, context, evidence hash, and TTL.
- Biometric or sensitive evidence must not be stored raw unless explicitly configured.
- Service credentials must be rotatable and revocable.
- Identity provider failures must fail closed.
- Identity verdicts must not be transferable between sessions.

# Audit Requirements

Record `identity_request_id`, `actor_id`, `actor_type`, credential class,
assurance requirement, result state, reason, evidence hash, verifier component,
and timestamp.

# Persistence Requirements

- Persist identity verdicts until their TTL plus audit retention window expires.
- Persist evidence hashes, not raw evidence, by default.
- Persist provider errors as structured audit metadata.
- Identity records must be immutable after verdict emission.

# Deterministic Rules

- Given the same credentials, provider state, assurance requirement, and context,
  the verifier must produce the same state and reason.
- Credential checks must run in stable configured order.
- Missing evidence always resolves to `hold` or `refused`, never `verified`.

# Examples

```json
{
  "identity_request_id": "idreq_001",
  "actor_id": "teacher_42",
  "actor_type": "delegate",
  "required_assurance": "standard",
  "state": "verified",
  "assurance_level": "standard"
}
```
