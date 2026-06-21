# Sprint 3U: Register Freshness and Snapshot Evidence Gap Analysis

## Governance Boundary

Sprint 3U is analysis-only. It records freshness questions that must be resolved
before `register_version`, `register_hash`, and `expected_previous_hash`
evidence can be trusted for any future post-review decision or mutation-proposal
discussion.

Sprint 3U does not define a lifecycle node. It does not approve a contract,
authorize assignment, create an `AuthorityRecord`, grant an authority reference,
emit a mutation proposal, mutate the register, write persistence, append audit,
resolve blockers, authorize runtime execution, or define resubmission
transitions.

HOLD remains active. `approved: false` remains unchanged.

## Current Evidence Dependency

Existing Sprint 3R and Sprint 3S artifacts require register snapshot evidence:
`register_version`, `register_hash`, and `expected_previous_hash`.

Current artifacts verify the presence and closed shape of register snapshot
evidence. They do not define freshness semantics, freshness windows, live-register
comparison rules, or re-snapshotting requirements.

`REGISTER_SNAPSHOT_STALE_OR_MISSING` exists as a failure concept for application
review evidence, and `EXPECTED_VERSION_CONFLICT` exists as a readiness failure
concept. No approved freshness rule currently defines when either concept must
apply.

## Freshness Questions To Resolve Later

The following questions remain open. Sprint 3U records them only as future
analysis inputs and does not answer them as approved rules:

| Question | Why it matters |
| --- | --- |
| What event or observation time binds the register snapshot? | Snapshot evidence needs a traceable time basis before freshness can be reasoned about. |
| What maximum age, if any, is permitted for snapshot evidence? | A future rule may need an age limit, but this sprint does not choose one. |
| What makes `expected_previous_hash` stale? | The relationship between expected prior state and later observed state is not yet defined. |
| What happens if the live register changes after review but before future decision discussion? | A future discussion must avoid treating older review evidence as still-current authority. |
| Must freshness be checked at review time, decision time, mutation-proposal time, or all of them? | The check point affects whether later evidence can safely rely on earlier snapshots. |
| Must a later node require re-snapshotting before any decision or mutation proposal? | Re-snapshotting may be required, but no later node or requirement is approved here. |
| Must dependency contract references share the same snapshot time or independent freshness evidence? | Dependency references may age independently from register evidence. |

## Risk Analysis

If register freshness remains undefined, future work risks relying on stale or
misinterpreted evidence:

| Risk | Why it matters |
| --- | --- |
| Stale register evidence mistaken as valid | A snapshot could appear sufficient even after the register changed. |
| Favorable review treated as still-current after register change | `FAVORABLE_APPLICATION_REVIEW_RECORDED` could be misread as remaining current without revalidation. |
| Dependency references appearing current when they are not | Referenced dependency contracts may have changed or expired after the snapshot was recorded. |
| Hash chain mismatch ignored | `expected_previous_hash` could fail to match a later register state without a defined consequence. |
| Future decision or handoff relying on obsolete state | Later analysis could build vocabulary on evidence that no longer reflects the register. |
| Mutation proposal based on outdated register evidence | A proposal could be discussed from stale evidence before a safe re-snapshot rule exists. |

## Future Sprint Candidates

The following are possible future analysis-only sprints. They are not approved
work, and this document does not authorize them:

| Candidate | Analysis purpose |
| --- | --- |
| Register freshness rule vocabulary analysis | Identify vocabulary for snapshot age, observation time, stale evidence, and re-snapshot prerequisites without approving rules. |
| Dependency contract mapping | Map register, persistence, audit append, idempotency, rollback, replacement, and revocation dependencies without resolving them. |
| Post-review handoff vocabulary analysis | Identify language needed to prevent favorable review from becoming automatic decision or mutation authority. |
| Mutation proposal prerequisite analysis | Identify prerequisites for any future mutation-proposal discussion without defining a proposal node. |
| Resubmission vocabulary gap analysis | Identify vocabulary needed for additional-evidence and blocked outcomes without defining transitions. |

## Explicit Non-Goals

Sprint 3U does not implement or define:

- freshness rule
- schema validation
- lifecycle node
- assignment decision
- mutation proposal
- register mutation
- persistence
- audit append
- blocker resolution
- runtime execution
- approval
- resubmission transition

Sprint 3U does not change HOLD, does not change `approved: false`, and does not
change any schema, validator, runtime code, test, v1 contract, frozen report,
coverage report, traceability artifact, deferred capability register,
`contracts/event-bus-v2.yaml`, or existing Sprint 3S or Sprint 3T governance
documentation.
