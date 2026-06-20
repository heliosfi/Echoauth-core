# Purpose

Define deterministic policy evaluation for EchoAuth authorization decisions.

# Scope

Applies after identity and authority inputs are available and before runtime
execution-token issuance.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `policy_evaluation_id` | string | yes | Policy evaluation identifier. |
| `request_id` | string | yes | Authorization request. |
| `subject_id` | string | yes | Protected subject or target. |
| `requester_id` | string | yes | Actor requesting action. |
| `authority_verdict_id` | string | yes | Authority verdict reference. |
| `delegation_id` | string | no | Delegation reference. |
| `action` | string | yes | Requested action. |
| `resource` | string | yes | Target resource. |
| `context` | object | yes | Deterministic facts. |
| `policy_version` | string | yes | Policy set version. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `policy_decision_id` | string | Unique policy result identifier. |
| `decision` | enum | `permit`, `refuse`, `hold`, `escalate`. |
| `reason` | string | Machine-readable reason. |
| `matched_policies` | list | Policies evaluated. |
| `failed_policies` | list | Policies that blocked permit. |
| `evidence_hash` | string | Canonical context/evidence hash. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `received` | `load_policy_set` | `evaluating` |
| `received` | `policy_set_missing` | `hold` |
| `evaluating` | `policy_permits` | `permit` |
| `evaluating` | `policy_refuses` | `refuse` |
| `evaluating` | `policy_requires_more_evidence` | `hold` |
| `evaluating` | `policy_requires_review` | `escalate` |

# Validation Rules

1. Policy set version must be loaded and immutable during evaluation.
2. Input context must be canonicalized before evaluation.
3. Policies must execute in deterministic order.
4. First refusal may terminate evaluation when refusal-first mode is active.
5. Permit requires all required policies to pass.
6. Missing required evidence returns `hold`, not permit.
7. Policy output must include a reason code.
8. Policy evaluation must not modify authority verdicts or runtime envelopes.

# Failure Conditions

| Condition | Result |
|---|---|
| Missing policy version | `hold` |
| Unknown policy | `hold` |
| Required evidence missing | `hold` |
| Policy runtime error | `refuse` or `hold` |
| Policy conflict | `escalate` |
| Context hash mismatch | `refuse` |
| Authority verdict mismatch | `refuse` |

# Security Requirements

- Policy evaluation must be side-effect free.
- Policy code or rules must be versioned.
- Policy inputs must not contain unaudited mutable references.
- Policy decisions must be bound to evidence hash and policy version.
- Policies must not grant permissions beyond authority scope.

# Audit Requirements

Record policy version, evaluation order, policy inputs hash, matched policies,
failed policies, decision, reason, authority verdict reference, and evaluator
component identity.

# Persistence Requirements

- Persist policy decisions used by authorization.
- Persist evidence hash and policy version.
- Retain refused, hold, and escalation decisions.
- Cache only by policy version and evidence hash.

# Deterministic Rules

- Same policy version and evidence hash produce same decision.
- Policy ordering is fixed by policy registry.
- Missing required evidence never permits.
- First-refusal mode terminates at the first refusing required policy.

# Examples

```json
{
  "policy_evaluation_id": "peval_001",
  "policy_version": "1.0.0",
  "decision": "permit"
}
```
