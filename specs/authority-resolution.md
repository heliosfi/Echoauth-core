# Purpose

Define the interface and rules for resolving whether a request has valid
authority before authorization or execution.

# Scope

Applies to parent, legal caregiver, institutional, delegated, emergency, and
runtime-service authority checks.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `request_id` | string | yes | Request being evaluated. |
| `subject_id` | string | yes | Protected subject or target of action. |
| `requester_id` | string | yes | Actor requesting authorization. |
| `action` | string | yes | Requested operation. |
| `resource` | string | yes | Target resource. |
| `context` | object | yes | Deterministic runtime facts. |
| `identity_verdict_id` | string | yes | Verified identity verdict reference. |
| `authority_records` | list | yes | Candidate authority records. |
| `delegation_records` | list | no | Relevant delegation records. |
| `revocation_records` | list | no | Relevant revocation records. |
| `policy_version` | string | yes | Authority policy version. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `authority_verdict_id` | string | Unique verdict identifier. |
| `request_id` | string | Original request identifier. |
| `state` | enum | `valid`, `refused`, `hold`, `conflict`, `escalate`. |
| `authority_source_id` | string | Controlling authority source, when resolved. |
| `authority_type` | enum | `parent`, `caregiver`, `institution`, `delegate`, `system`, `emergency`. |
| `scope` | object | Authorized action/resource/context bounds. |
| `reason` | string | Machine-readable reason code. |
| `evidence_hash` | string | Canonical hash of evidence used. |
| `expires_at` | timestamp | Verdict expiration. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `received` | `identity_verified` | `checking_records` |
| `received` | `identity_failed` | `refused` |
| `checking_records` | `single_authority_found` | `validating_scope` |
| `checking_records` | `no_authority_found` | `refused` |
| `checking_records` | `authority_unreachable` | `hold` |
| `checking_records` | `conflicting_authority` | `conflict` |
| `validating_scope` | `scope_valid` | `valid` |
| `validating_scope` | `scope_invalid` | `refused` |
| `conflict` | `requires_review` | `escalate` |
| `hold` | `evidence_available` | `checking_records` |

# Validation Rules

1. Requester identity must verify before authority evaluation.
2. Authority records must be active, unexpired, and not revoked.
3. Delegated authority must trace to a valid grantor.
4. Requested action must match authority or delegation scope.
5. Requested resource must match authority or delegation scope.
6. Parent/legal caregiver authority controls child/care contexts unless a valid superseding legal authority is present.
7. Conflicting authority records must not be collapsed unless policy defines precedence.
8. Evidence used for the verdict must be hashable and auditable.

# Failure Conditions

| Condition | Result |
|---|---|
| Identity verification failure | `refused` |
| No authority record | `refused` |
| Authority source unreachable | `hold` |
| Conflicting authority records | `conflict` or `escalate` |
| Expired authority | `refused` |
| Revoked authority | `refused` |
| Scope mismatch | `refused` |
| Delegate grantor invalid | `refused` |
| Evidence integrity failure | `hold` or `refused` |

# Security Requirements

- Never infer authority from role labels alone.
- Never permit execution from interpreted intent.
- Bind verdict to request, action, resource, subject, and evidence hash.
- Treat authority substitution as high severity.
- Expire authority verdicts aggressively in high-risk contexts.

# Audit Requirements

Record all authority records evaluated, identity verdict, delegation chain,
revocation checks, precedence rule, verdict state, reason, evidence hash,
issuing component, and timestamp.

# Persistence Requirements

- Persist authority verdicts used by authorization.
- Store evidence hash and policy version.
- Retain refused, conflict, hold, and escalation verdicts.
- Index by request, subject, requester, authority source, and state.

# Deterministic Rules

- Same authority records, revocations, policy version, and request facts produce same verdict.
- Record ordering is by priority, issued time, then record ID.
- Missing required evidence never resolves to `valid`.

# Examples

```json
{
  "request_id": "req_001",
  "requester_id": "teacher_42",
  "state": "hold",
  "reason": "parent_authority_unreachable"
}
```
