# Sprint 3W: Dependency Authority-Source Gap Analysis

## Governance Boundary

Sprint 3W is documentation-only and analysis-only. It records authority-source
evidence questions that must be resolved before any dependency contract could
later be considered for approval.

HOLD remains active. `approved: false` remains unchanged.

Sprint 3W does not define a lifecycle node, assignment decision, approval,
`AuthorityRecord`, authority reference grant, mutation proposal, register
mutation, persistence write, audit append, blocker resolution, runtime
execution, resubmission transition, dependency approval, or dependency contract.

## Authority-Source Distinctions

The following terms must remain separate until a future approved contract defines
their relationship:

| Term | Meaning in this analysis | Boundary |
| --- | --- | --- |
| Owner-role placeholder | A named decision discipline or governance role associated with a blocker. | It is not a person, authority source, approval authority, or grant. |
| Accountable party | A future named party that may become responsible for a blocker decision surface. | Naming a party does not approve a contract or prove authority. |
| Approval authority reference | A future evidence reference that may identify the authority relied on for approving a dependency contract. | Referencing authority evidence is not itself approval or an authority grant. |
| Real authority grant | A live authority artifact that could grant permissions only if separately approved by governing contracts. | Sprint 3W does not create, validate, or grant real authority. |

## Open Authority-Source Questions

The following questions remain unresolved and are not answered as approved rules
by Sprint 3W:

| Question | Why it matters |
| --- | --- |
| What evidence can qualify as valid authority source evidence? | Dependency contracts cannot be considered safely without knowing what proves authority. |
| What scope must authority source evidence cover? | An authority source may be valid for one dependency surface but not another. |
| What validity period applies to authority source evidence? | Authority may expire before a future approval discussion occurs. |
| How must expired evidence be represented? | Expired evidence must not be mistaken for current authority. |
| How is inferred authority prohibited? | Role names, context, or prior participation must not imply authority. |
| How is reused authority evidence constrained? | Evidence used for one dependency may not be valid for another dependency. |
| How are conflicting authority sources handled? | Conflicts must not produce implicit approval or blocker resolution. |
| Must authority evidence be independent per dependency? | Shared evidence may create coupling or conflict between unrelated dependency surfaces. |

## Affected Dependencies

Authority-source evidence questions affect every unresolved dependency that may
later be discussed for approval:

| Dependency | Authority-source gap |
| --- | --- |
| Register | Authority to define register read boundaries, freshness treatment, conflict behavior, and non-mutation guarantees remains unresolved. |
| Persistence | Authority to approve storage engine, transaction, uniqueness, migration, and failure rules remains unresolved. |
| Audit append | Authority to approve writer identity, chain selection, append authority, and append-failure behavior remains unresolved. |
| Durable idempotency | Authority to approve durable decision-key scope, duplicate handling, replay limits, and concurrency behavior remains unresolved. |
| Rollback | Authority to approve rollback conditions, responsible party, evidence retention, and failure handling remains unresolved. |
| Replacement | Authority to approve replacement scope, predecessor linkage, conflict handling, and non-inference rules remains unresolved. |
| Revocation | Authority to approve revocation source, timing, scope, evidence binding, and conflict behavior remains unresolved. |

## Risk Analysis

If authority-source evidence remains undefined, future work risks:

| Risk | Why it matters |
| --- | --- |
| Placeholder mistaken for authority | An owner-role placeholder could be treated as if it proves a real approving authority. |
| Accountable party mistaken for approval authority | A named party could be treated as authorized without an explicit authority reference. |
| Authority reference mistaken for grant | Citing authority evidence could be confused with granting authority. |
| Scope mismatch | Authority evidence may not cover the dependency surface being discussed. |
| Expired, reused, or inferred authority | Invalid evidence could appear current, independent, or sufficient. |
| Blocker resolution inferred | Mapping authority-source questions could be mistaken for resolving the blocker itself. |

## Explicit Non-Goals

Sprint 3W does not implement or define:

- authority validation
- dependency approval
- dependency contracts
- workflow
- runtime behavior
- lifecycle node
- assignment decision
- approval
- `AuthorityRecord`
- authority reference grant
- mutation proposal
- register mutation
- persistence write
- audit append
- blocker resolution
- runtime execution
- resubmission transition

Sprint 3W does not change HOLD, does not change `approved: false`, and does not
change any existing contract, schema, validator, test, runtime code, report, or
governance document.
