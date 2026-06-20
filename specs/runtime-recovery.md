# 1. Recovery Purpose

Recovery determines whether a request stopped in `EXECUTION_BLOCKED` or
`HALTED` is eligible to enter a new validation cycle. It preserves the original
failure and audit evidence, requires explicit recovery authority, and identifies
the validations that must be rerun.

Recovery is governance-only and eligibility-only. It does not restore
authorization, mutate runtime state, or resume execution.

# 2. Recovery Boundaries

- The only Recovery entry states are `EXECUTION_BLOCKED` and `HALTED`.
- Governance `HOLD` is not a Recovery entry state. It may produce a separate,
  evidence-only proposal for `EXECUTION_BLOCKED`; that proposal is not a state
  transition or mutation.
- Recovery consumes immutable references to the original failure and Halt
  Decision.
- Recovery evaluates eligibility for revalidation only.
- Recovery never changes the original request, decision, audit record, token,
  envelope, or runtime state.
- Recovery never treats elapsed time, service restoration, review evidence, or
  changed evidence as implicit authorization.
- An eligible result must return to the normal identity, authority, delegation,
  policy, invariant, and audit validation sequence.
- Recovery from `HALTED` defaults to `new_request_required`. Revalidation is
  possible only when a separate, active Recovery Review Protocol permits it.

# 3. Recovery Inputs

The canonical request schema is `schemas/recovery-request.schema.json`.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `recovery_id` | string | yes | Unique recovery eligibility request. |
| `request_id` | string | yes | Original affected request. |
| `source_state` | enum | yes | `execution_blocked` or `halted`. |
| `failure_code` | enum | yes | Canonical original failure classification. |
| `requested_recovery_path` | enum | yes | `revalidate_request` or `create_new_request`. |
| `recovery_actor_id` | string | yes | Actor requesting evaluation; identity grants no authority. |
| `recovery_authority_reference` | string | yes | Explicit authority source applicable to Recovery. |
| `authority_resolution_id` | string | yes | Authority Resolution result supporting the request. |
| `authority_evidence_hash` | string | yes | Hash of current authority evidence. |
| `halt_decision_id` | string | yes | Preserved Halt Decision reference. |
| `halt_decision_evidence_hash` | string | yes | Hash of preserved Halt evidence. |
| `original_failure_evidence_hash` | string | yes | Hash of immutable original failure evidence. |
| `original_failure_audit_event_id` | string | yes | Audit reference for the original failure. |
| `changed_evidence_reference` | string | yes | Stable reference to evidence changed since failure. |
| `changed_evidence_hash` | string | yes | Canonical hash of changed evidence. |
| `recovery_policy_version` | string | yes | Pinned policy used for classification. |
| `guard_evidence` | object | yes | Failure-code-specific evidence defined by the request schema. |
| `recovery_review_protocol` | object | conditional | Required for `HALTED` revalidation; defined by its separate schema. |
| `invalidated_token_refs` | list[string] | yes | Tokens that remain unusable; may be empty. |
| `requested_at` | UTC timestamp | yes | Recovery eligibility request time. |

# 4. Recovery Outputs

The canonical result schema is `schemas/recovery-result.schema.json`.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `recovery_decision_id` | string | yes | Deterministic eligibility decision identifier. |
| `recovery_id` | string | yes | Related Recovery request. |
| `request_id` | string | yes | Original affected request. |
| `source_state` | enum | yes | Preserved entry state. |
| `outcome` | enum | yes | `revalidation_required`, `rejected`, or `new_request_required`. |
| `reason` | string | yes | Machine-readable decision reason. |
| `required_validations` | ordered list[enum] | yes | Validations required before any later authorization. |
| `evidence_hash` | string | yes | Canonical hash of the eligibility evidence package. |
| `decided_at` | UTC timestamp | yes | Decision time. |
| `audit_event_id` | string | yes | Audit record for the eligibility decision. |
| `recovery_allowed` | boolean | no | Deprecated compatibility-only field. Consumers must ignore it and use `outcome`. |

No output grants authorization, execution permission, a destination state, or
permission to mutate runtime state.

# 5. Recovery Evidence Requirements

1. Evidence must bind the Recovery request to the original request, failure
   code, failure evidence hash, failure audit event, and Halt Decision.
2. Changed evidence must have a stable reference and canonical hash distinct
   from the evidence that caused the original failure.
3. `guard_evidence` must contain every field required for its source-state and
   failure-code policy row in `contracts/recovery-service.yaml`.
4. Recovery Review Protocol evidence is separate from a general Review outcome
   and must conform to `schemas/recovery-review-protocol.schema.json`.
5. Authority evidence must be current and must not be inferred from identity,
   role, ownership, affiliation, or prior authorization.
6. Used, expired, revoked, invalid, or previously claimed token references
   remain invalid and may never be recovered.
7. Evidence packages contain hashes and stable references, not raw credentials,
   secrets, or executable payloads.
8. Missing, malformed, conflicting, unverifiable, or unchanged evidence fails
   closed.
9. Original failure and Halt audit records remain unchanged.

# 6. Recovery Authority Requirements

- Recovery requires an explicit authority source applicable to Recovery.
- `authority_resolution_id` and its evidence hash must bind the authority result
  used for the request.
- Verified identity attributes the actor but grants no authority.
- Authority must be current, in scope, unexpired, and unrevoked.
- Revalidation from `HALTED` additionally requires a separate active Recovery
  Review Protocol and its bound Review Decision evidence.
- The Recovery Review Protocol does not add a general Review outcome and does
  not authorize the original action.
- Override evidence does not independently grant Recovery authority.
- Ambiguous, conflicting, missing, or invalid authority produces `rejected`.

# 7. Recovery State Vocabulary

| Term | Classification | Recovery Meaning |
| --- | --- | --- |
| `EXECUTION_BLOCKED` | Sprint 2L runtime state | Recoverable entry state; eligibility evaluation may be requested. |
| `HALTED` | Sprint 2L runtime state | Safety or integrity entry state; a new request is required by default. |
| `HOLD` | governance outcome | Not an entry state. It may produce a proposal-only `EXECUTION_BLOCKED` artifact. |
| `revalidation_required` | Recovery outcome | Full validation may be requested; no runtime state changes. |
| `rejected` | Recovery outcome | Eligibility failed closed. |
| `new_request_required` | Recovery outcome | Original request cannot be reused. |

Recovery defines no destination runtime state. The `HOLD` to
`EXECUTION_BLOCKED` mapping is represented only by
`schemas/governance-runtime-proposal.schema.json`. A future state change would
require separate canonical transition processing outside Recovery.

# 8. Recovery Outcomes

| Outcome | Meaning |
| --- | --- |
| `revalidation_required` | Eligibility passed; the complete ordered governance validation sequence must run again. |
| `rejected` | Recovery evidence, authority, policy, audit linkage, or changed condition failed closed. |
| `new_request_required` | The original request cannot be reused; a new request and fresh evidence are mandatory. |

Deterministic precedence and failure-code guards are defined in
`contracts/recovery-service.yaml`. No new general Review outcome is defined.

# 9. Recovery Non-Goals

Recovery does not:

- authorize or reauthorize an action,
- infer authority from identity,
- reverse refusal, halt, revocation, or expiration,
- approve or execute an override,
- perform general review or escalation,
- mutate runtime state or execute transition logic,
- define or create destination runtime states,
- resume or dispatch execution,
- issue, restore, revalidate, or reuse tokens,
- create or modify runtime envelopes,
- orchestrate validation services,
- publish notifications or runtime events,
- call adapters, providers, or external systems,
- persist records or implement storage adapters,
- repair or rewrite the original audit chain.

# 10. Difference From Other Governance Components

| Component | Distinction From Recovery |
| --- | --- |
| Authorization | Authorization determines permission. Recovery determines only eligibility to request fresh validation. |
| Review | General Review assesses escalation evidence. Recovery uses a separate Recovery Review Protocol without adding a general Review outcome. |
| Escalation | Escalation routes unresolved outcomes. Recovery classifies eligibility after processing stopped. |
| Override | Override records an exceptional governance decision. It does not independently grant Recovery authority. |
| Halt | Halt classifies why processing must stop. Recovery preserves that decision and never cancels or rewrites it. |

Contract artifacts: `contracts/recovery-service.yaml`,
`schemas/recovery-request.schema.json`, `schemas/recovery-result.schema.json`,
`schemas/recovery-review-protocol.schema.json`, and
`schemas/governance-runtime-proposal.schema.json`.
