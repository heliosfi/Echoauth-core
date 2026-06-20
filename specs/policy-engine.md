# Purpose

Define the deterministic policy engine runtime component.

# Scope

Applies to policy loading, policy evaluation, policy result emission, and policy
failure handling.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `evaluation_id` | string | yes | Unique evaluation. |
| `policy_version` | string | yes | Policy version to evaluate. |
| `policy_type` | enum | yes | Policy type. |
| `facts` | object | yes | Canonical evaluation facts. |
| `authority_verdict_id` | string | no | Authority reference. |
| `delegation_validation_id` | string | no | Delegation reference. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `decision` | enum | `permit`, `refuse`, `hold`, `escalate`. |
| `reason` | string | Machine-readable reason. |
| `matched_rules` | list | Rules evaluated. |
| `failed_rules` | list | Rules preventing permit. |
| `facts_hash` | string | Canonical facts hash. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `received` | `load_policy` | `loaded` |
| `received` | `policy_missing` | `hold` |
| `loaded` | `evaluate` | `evaluating` |
| `evaluating` | `all_required_pass` | `permit` |
| `evaluating` | `rule_refuses` | `refuse` |
| `evaluating` | `evidence_missing` | `hold` |
| `evaluating` | `review_required` | `escalate` |

# Validation Rules

1. Policy version must be active or explicitly replayable.
2. Facts must match policy schema.
3. Rules must execute in deterministic order.
4. Rule evaluation must be side-effect free.
5. Permit requires all required rules to pass.
6. Missing facts must not permit.

# Failure Conditions

| Condition | Result |
|---|---|
| Policy missing | `hold` |
| Facts schema mismatch | `refuse` |
| Rule evaluation error | `refuse` or `hold` |
| Conflicting rule result | `escalate` |
| Policy hash mismatch | `halt` via invariant validator |

# Security Requirements

- Policies cannot grant beyond authority scope.
- Policy artifacts must be hash-verified.
- Policy engine must not execute untrusted dynamic code unless sandboxed.
- Policy results must bind to facts hash and policy version.

# Audit Requirements

Record evaluation ID, policy version, facts hash, matched rules, failed rules,
decision, reason, evaluator, and timestamp.

# Persistence Requirements

- Persist policy decisions used by authorization.
- Store policy artifact hash.
- Retain facts hash and decision reason.
- Cache only by policy version and facts hash.

# Deterministic Rules

- Same policy version and facts hash produce same decision.
- Rule ordering is fixed by policy artifact.
- First-refusal mode terminates at first refusing required rule.

# Examples

```json
{
  "policy_version": "1.0.0",
  "decision": "refuse",
  "reason": "delegation_out_of_scope"
}
```
