# SniperBot Stage 2 Repository-Boundary and Disposition Decision

## Status and Boundary

Status: **FOUNDER DECISION — RETAIN THROUGH STAGE 2 CLOSURE**

Mode: documentation-only, architectural-boundary-decision-only,
non-implementation, non-migration, non-execution, fail-closed.

This record decides the repository boundary and the sequence for disposition
of the failed SniperBot Stage 2 Advancement Gate findings. It does not accept
Stage 2 evidence, certify or close Stage 2, change the Advancement Gate result,
create an implementation task order, create a repository, migrate files, enter
Stage 3, or authorize operative capability.

The Advancement Gate remains **FAIL**. Stage 2 remains **HOLD**. Stage 3
remains unentered and unauthorized.

## Decision Identity

- Repository: `heliosfi/Echoauth-core`
- Authoritative starting checkpoint:
  `69e5952319f1c0fed81744401482d8fcb3cfcd00`
- Decision identity:
  `SNIPERBOT-STAGE2-REPOSITORY-BOUNDARY-DISPOSITION-69E5952`
- Decision title: SniperBot Stage 2 Repository-Boundary and Disposition
  Decision
- Founder: Nicholas B. Carty
- Advancement Gate determination addressed: `FAIL`
- Final repository-boundary disposition:
  **RETAIN THROUGH STAGE 2 CLOSURE**

## Starting-State Verification

At the start of this decision lane:

- branch `main`, local `HEAD`, and `origin/main` all resolved to
  `69e5952319f1c0fed81744401482d8fcb3cfcd00`;
- divergence was `0/0`;
- the working tree and index were clean;
- no Git lock existed; and
- no newer synchronized checkpoint existed after one refresh of `origin`.

Commit `69e5952319f1c0fed81744401482d8fcb3cfcd00` added only
`docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-advancement-gate-reevaluation-task-order.md`
and directly followed
`e96dcbbe8b37e565bbff69aa1352915b3ab927df`.

The one-time task order produced one read-only `FAIL` determination and is
consumed. The task order authorized a reported determination, not creation or
mutation of a repository record. Its published text therefore remains
immutable and no standalone gate-determination file was created. This record
does not replay that task, rewrite its historical status text, or perform
another Advancement Gate evaluation.

## Unresolved Advancement Gate Findings

The consumed re-evaluation identified these unresolved dependencies:

1. `H5` — no exact implementation task order exists.
2. `H7` — documentation-only sources do not authorize advancement.
3. `H8` — documentation coverage is not overall evidence acceptance or
   certification.
4. `E1` — lane evidence exists, but overall Stage 2 evidence acceptance has
   not occurred.
5. `E2` — traceability does not settle advancement authority.
6. Indexing discrepancy — the re-evaluation authority chain and task order
   are not indexed in the canonical indexes, and no standalone path exists for
   the read-only `FAIL` determination.

These findings remain unresolved for the Advancement Gate until the separate
future lanes defined below are completed. This decision classifies their
proper disposition; it does not itself resolve the gate or convert `FAIL` to
another result.

## Evidence Examined

### Repository Purpose and Governing Architecture

- `README.md` — identifies Echoauth-core as a deterministic governance and
  authorization framework and preserves the current Stage 2 `HOLD` posture.
- `architecture/system-overview.md` — defines EchoAuth as the authorization
  and enforcement framework in which governance precedes execution.
- `governance/principles.md` — requires authority before execution,
  separation of powers, deterministic authorization, and no autonomous
  permission expansion.
- `governance/authority-model.md` — requires explicit, bounded, auditable
  authority and rejects inferred or expanded permission.

### Stage and Advancement Boundaries

- `docs/control-gates/sniperbot-live-money-readiness-ladder-non-authorization-boundary-review.md`
  at `303adcfaf53c17f21b3d794f1b2baec33ccbf315` — defines the staged ladder,
  makes each stage separately governed, and defines Stage 3 as implementation
  task-order requirements rather than implementation authority.
- `docs/control-gates/sniperbot-live-money-readiness-advancement-gate-non-authorization-boundary-review.md`
  at `6d529ef0ea0138bccb789628511db155ced17338` — requires explicit authority,
  evidence acceptance, currentness, and task-specific boundaries before
  movement, while prohibiting README entries and documentation presence from
  acting as authority.
- `docs/control-gates/sniperbot-live-money-readiness-evidence-requirements-non-authorization-boundary-review.md`
  at `f70298cffbb922b53884069a7681ba07edc816ca` — requires evidence acceptance
  to occur through a separate founder-authorized bounded process.
- `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-advancement-gate-decision-review.md`
  at `2491ad62ecd9a5c365d9b8e404862c7c1666308b` — records the historical
  `HOLD` posture with `ESCALATE` elements and the locked separation between
  coverage, currentness, certification, advancement, and activation.
- `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-evidence-acceptance-decision-record.md`
  at `be9bdc736c9f3452059aa968c914b8bdf6db69f7` — records the existing overall
  Stage 2 evidence decision as `HOLD`.
- `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-authority-resolution-governance-record.md`
  at `d930618add0009120cc2b3c007406e1e90b494c4` — establishes that an exact
  implementation task order is required before a future code change and
  cannot be inferred from another record.
- `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-founder-approval-artifact-requirements-currentness-validation-review.md`
  at `c3fade3c8e268a898a0fbf85dab3ca2f20726274` — accepts bounded documentary
  currentness without treating currentness as certification or advancement.

### Construction and Evidence State

- `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-post-construction-accumulated-evidence-coverage-sufficiency-review.md`
  at `fc0daf5d70b0cad40d476bb0582ccf3f4f4667d1` — records coverage and
  sufficiency `PASS` for all ten evaluator lanes and all 108 required category
  positions, but explicitly excludes overall Stage 2 acceptance and
  completion certification.
- `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-post-construction-cross-file-semantic-consistency-review.md`
  at `8e7eda217a37c26855f9e2e1a0b63e11aaf36423` — preserves the historical
  semantic findings that drove the later bounded repair sequence.
- `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-canonical-fsm-post-repair-implementation-evidence-acceptance.md`
  at `ac1cb28b656f2bcef415025f416bfaeee80dfeff` — accepts the repaired Canonical
  FSM, closes the null-authority discrepancy, and records zero remaining
  substantive Canonical FSM discrepancies.
- `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-crypto-deferral-no-action-post-repair-implementation-evidence-acceptance.md`
  at `7e814861b252449866046e7598af490e831a4698` — accepts the strict-reference
  repair and its direct evidence without closing Stage 2.
- The remaining eight lane-level implementation-evidence acceptances indexed
  by `docs/control-gates/README.md` — preserve the accepted Rollback,
  Asset-Class, Options, Stock, and Crypto evaluator evidence that completes
  the ten-lane construction set.
- `src/sniperbot/`, the ten SniperBot schemas in `schemas/`, and the ten
  focused SniperBot test modules in `tests/` — establish that the current
  Stage 2 implementation record is physically and historically contained in
  Echoauth-core.

### Re-evaluation Authority Chain and Traceability

- Founder approval artifact at
  `d8ba64728bdde235dccc7777ceeaec249d19965d`.
- Approval record at
  `97708c57dce0d5c8bce05a5a6ccfbe8ee1851ea8`.
- Approval mechanism at
  `f5af8c5c1cbfb0cd121b8fe655aed7d04b49aeac`.
- Approval workflow at
  `a8fb2c1d92e8ec3d5adbe1a7b56bfcae29abc0bc`.
- Workflow-execution record at
  `e96dcbbe8b37e565bbff69aa1352915b3ab927df`.
- Re-evaluation task order at
  `69e5952319f1c0fed81744401482d8fcb3cfcd00`.
- `README.md` and `docs/control-gates/README.md`, both last synchronized for
  this subject at `a3b6ddf15cbdb66d2add15d0caf6ce0fd97d36ad`.

All cited paths and commits resolve at the starting checkpoint. No existing
repository artifact defines or authorizes migration to a dedicated SniperBot
repository.

## Current Architectural Relationship

EchoAuth is the larger deterministic governance and authority system.
SniperBot is a governed domain system whose current Stage 2 contracts,
founder decisions, schemas, pure evaluators, direct tests, independent
evidence, acceptances, and control-gate history reside in Echoauth-core.

That containment does not collapse the two systems into one architectural
identity. EchoAuth supplies governance and authority boundaries. SniperBot
supplies a domain-specific decision surface that remains subordinate to those
boundaries. A future dedicated SniperBot repository, if later created, will
remain governed by EchoAuth and will not become an independent source of
authority merely because its code is stored separately.

The separate Governed Agentic Engineering methodology repository is not part
of this decision lane. It remains parked until separately activated and must
not be modified, relied on as operative authority, or collapsed into either
EchoAuth or SniperBot by this decision.

## Repository-Boundary Decision

The founder selects:

**RETAIN THROUGH STAGE 2 CLOSURE**

Echoauth-core must remain the sole authoritative repository for the complete
SniperBot Stage 2 record through:

1. independent Stage-2-wide evidence review;
2. formal Stage-2-wide evidence acceptance;
3. separate Stage 2 completion certification;
4. canonical index synchronization;
5. a separate current closure-authority process; and
6. formal Stage 2 closure.

No dedicated SniperBot repository may be planned as an operative migration,
created, initialized, populated, or used for later implementation before
formal Stage 2 closure. Repository separation occurs **after Stage 2
closure**, never by inference from this decision.

### Rationale

- Every governing Stage 2 artifact, implementation blob, schema, test, repair,
  and acceptance currently belongs to one verifiable Echoauth-core lineage.
- No repository-controlled migration or separation authority currently exists.
- Moving the active record before acceptance and closure would split the
  evidence baseline, complicate currentness, and risk obscuring provenance.
- EchoAuth's authority-before-execution, separation-of-powers, and
  non-expansion rules favor completing the current governance chain before a
  new storage boundary is introduced.
- Retention through closure preserves auditability without granting any new
  implementation, runtime, execution, or repository-creation authority.

## Implementation-Task-Order Disposition — H5

### Current Need

No additional Stage 2 implementation is established as necessary by the
current synchronized evidence. The ten evaluator lanes have lane-level
acceptance, the Canonical FSM repair chain is accepted with zero substantive
discrepancies, and the Crypto Deferral strict-reference repair chain is
accepted. No legitimate remaining code, schema, API, test, package, runtime,
or integration repair lane is authorized or identified.

### Meaning of the Missing Order

The separate implementation-task-order rule controls a future code change. It
does not supply provenance for completed work and cannot be applied backward
to turn prior founder-bounded construction into a newly authorized task.

Accordingly:

- the missing implementation task order does not identify a current Stage 2
  implementation dependency;
- it must not be represented as an order for work already completed;
- creating it now for completed implementation would be prohibited
  retroactive authorization;
- it is historically inapplicable to the documentation-only acceptance,
  certification, indexing, and closure sequence;
- it remains prospectively required before any genuine future code change;
  and
- its absence must be disposed of expressly by the later Stage-2-wide review
  and closure-authority process rather than ignored, backfilled, or silently
  waived.

No future implementation task order is created or waived by this record. If
new substantive implementation evidence later appears necessary before Stage
2 closure, the process must fail closed, return Stage 2 to the applicable
finding, and obtain a new founder boundary decision and a separate exact
implementation task order. This record cannot authorize that exception.

After Stage 2 closure, any legitimate later SniperBot implementation task
order belongs in the separately authorized dedicated SniperBot repository,
must cite the preserved Echoauth-core lineage, and requires its own future
stage authorization. Until that repository and stage exist, no repository is
authorized for future SniperBot implementation.

## Disposition of Every Failed Gate Finding

| Finding | Governed disposition | Exact later dependency |
| --- | --- | --- |
| `H5` — absent implementation task order | No current implementation lane exists. Retroactive creation is prohibited. The requirement is prospectively valid but historically inapplicable to completed construction and documentation-only closure work. | The Stage-2-wide independent review must verify no implementation remains and accept this disposition; the closure-authority process must expressly preserve it. Any later code change requires a new exact task order in the future authorized repository. |
| `H7` — documentation does not authorize advancement | Preserved. Documentation, acceptance, certification, and indexes remain evidence or governance records, not closure authority. | A separate current founder closure-authority chain and exact closure task order must authorize only the final Stage 2 closure evaluation and record. |
| `H8` — coverage is not overall acceptance | Preserved. The ten-lane `PASS` for coverage and sufficiency is an input, not Stage-2-wide acceptance or certification. | A separate independent Stage-2-wide acceptance review, formal evidence-acceptance artifact, and separate completion-certification artifact are required. |
| `E1` — lane evidence exists without overall acceptance | Preserved. Lane-level acceptance cannot be aggregated by inference. | The exact next bounded evidence lane is the independent Stage-2-wide evidence consolidation and acceptance review defined below. |
| `E2` — traceability does not settle advancement authority | Preserved. Complete lineage and clean indexes do not close Stage 2. | After evidence acceptance, certification, and index synchronization, complete the separate closure-authority process before formal closure. |
| Indexing discrepancy | The authority chain and task order are valid but absent from both current indexes. The read-only `FAIL` determination has no standalone artifact because its consumed order did not authorize one. | A later documentation-only synchronization lane must update both indexes, truthfully record the consumed `FAIL`, and use this disposition record as the durable repository reference without inventing a nonexistent result path. |

## Stage-2-Wide Evidence Acceptance Requirement

The exact next evidence dependency is a separate founder-authorized,
read-only **Stage-2-wide evidence consolidation and independent acceptance
review**. It must:

- derive its criteria from the repository's evidence-requirements and
  Advancement Gate boundaries;
- inspect all ten current lane-level acceptances and their exact current
  implementation, schema, API, and test blobs;
- include the Canonical FSM and Crypto Deferral post-repair acceptance chains;
- verify currentness, provenance, coverage, sufficiency, cross-file semantic
  consistency, package boundaries, prohibited-capability absence, and no
  unresolved substantive discrepancy;
- independently verify that the `H5` disposition above does not conceal a
  remaining implementation need;
- distinguish lane acceptance from overall Stage 2 acceptance and completion
  certification; and
- return only a review outcome and proposed acceptance scope, without
  publishing acceptance, certifying completion, changing an index, closing
  Stage 2, or authorizing Stage 3.

If that review passes, a separate founder-authorized artifact must formally
accept the Stage-2-wide evidence. Evidence acceptance must remain separate
from founder approval, implementation task orders, certification,
advancement, activation, runtime, and execution.

After formal evidence acceptance, a separate founder-authorized Stage 2
completion-certification review and artifact must determine whether the
accepted evidence is sufficient to certify completion of the bounded Stage 2
construction record. Certification is not closure or advancement.

## Closure and Advancement Authority Requirement

Stage 2 may close only after the acceptance, certification, and indexing
dependencies above are complete and current.

The exact later authority dependency is a separate task-specific founder
closure-authority process for the sole subject of formal SniperBot Stage 2
closure. That process must preserve the repository's established separation
of:

1. founder approval artifact;
2. durable approval record;
3. fail-closed approval mechanism;
4. genuine human-review workflow and execution record;
5. exact single-use, read-only closure task order; and
6. final closure evaluation and closure record.

Each component requires its own explicit bounded authorization and publication
boundary where the controlling repository rules require separation. The
closure task must revalidate every prior artifact, all revocation and
currentness conditions, the `H5` disposition, and the then-current indexes.

Only the final authorized closure evaluation may change the Stage 2 posture
or supersede the current Advancement Gate `FAIL`. It must use a closed,
repository-governed result vocabulary and must fail closed on any missing,
stale, conflicting, revoked, unindexed, or unaccepted dependency.

Even a successful Stage 2 closure does not enter or authorize Stage 3. Stage
3 requires a later, separate, explicit founder authorization after repository
separation and lineage initialization are complete.

## Canonical Indexing Requirement

Indexing remains traceability only and grants no authority.

### `docs/control-gates/README.md`

A later README-only synchronization lane must add canonical, unique,
resolvable entries for:

1. the founder approval artifact;
2. the approval record;
3. the approval mechanism;
4. the approval workflow;
5. the workflow-execution record;
6. the consumed re-evaluation task order;
7. the read-only `FAIL` determination, recorded truthfully through this
   disposition record because no standalone result artifact was authorized;
8. this repository-boundary and disposition decision;
9. the later Stage-2-wide evidence acceptance; and
10. the later Stage 2 completion certification.

The index entry for the task order must not retain the misleading implication
that it remains unused. The historical task-order file itself must remain
unchanged; the index must state that its single use is consumed and returned
`FAIL`.

### `README.md`

The root status summary must be updated in the same separately authorized
documentation synchronization lane to identify:

- the current authoritative Stage 2 checkpoint;
- the current Stage-2-wide acceptance and certification status;
- the consumed `FAIL` re-evaluation and this disposition record;
- Echoauth-core's retained authority through Stage 2 closure;
- the current `HOLD` posture and closure dependency; and
- Stage 3's unentered and unauthorized posture.

The root README need not duplicate the entire control-gate catalog, but it
must link to the canonical control-gates index and current controlling
artifacts without presenting traceability as authority.

No index is modified by this decision.

## Historical-Lineage Preservation

If a dedicated SniperBot repository is later created, the following rules are
mandatory:

- Echoauth-core's published Git history, tags, branches, documents, schemas,
  source, tests, and acceptance records must not be deleted or rewritten.
- Published commits must retain their original hashes and must not be
  represented as if they originated in the new repository.
- Files must not be moved, copied, squashed, filtered, or renamed in a way
  that obscures their Echoauth-core provenance.
- Echoauth-core remains the canonical historical and governance authority for
  the complete Stage 2 record after separation.
- The new repository must begin with a lineage manifest identifying
  `heliosfi/Echoauth-core`, the exact closed Stage 2 checkpoint, the exact
  closure artifact, every imported path and blob hash, and the method used to
  preserve or reference history.
- Any later code transfer requires separate authorization after repository
  creation and must record source path, source commit, source blob, target
  path, and target blob.
- The new repository must not claim independent origin, inherited Stage 3
  authority, implementation authority, deployment authority, or live-money
  authority.
- EchoAuth governance and SniperBot domain logic must remain architecturally
  distinct even where the future SniperBot repository cites or consumes
  EchoAuth governance contracts.
- The Governed Agentic Engineering methodology repository remains separate
  and parked until independently activated.

## Exact Future Bounded-Lane Sequence

Every lane below requires a new explicit founder-selected bounded order. No
lane authorizes the next merely by completing successfully.

1. **Repository-boundary and Stage 2 disposition decision.** Publish only
   this record. Stop after synchronization. This lane authorizes no follow-on
   action.
2. **Independent Stage-2-wide evidence consolidation and acceptance review.**
   Perform read-only review only. Stop after reporting `PASS`, `FAIL`, or
   `BLOCKED` and, on `PASS`, the exact proposed acceptance scope.
3. **Formal Stage-2-wide evidence acceptance.** Create and publish only the
   acceptance artifact supported by a passing independent review. Stop before
   certification or indexing.
4. **Stage 2 completion certification.** Independently review and, only under
   separate publication authority, publish the completion-certification
   artifact. Stop before indexing or closure authority.
5. **Canonical README and control-gate index synchronization.** Update only
   the minimum existing indexes described above. Stop after publication;
   indexing is not authority.
6. **Stage 2 closure-authority process.** Establish the separate,
   task-specific, fail-closed closure authority chain and exact one-time
   closure task order through separately bounded publications. Stop before
   executing the closure task.
7. **Formal Stage 2 closure.** Execute only the authorized read-only closure
   task, publish the result only if separately authorized, and stop. A
   successful result closes Stage 2 but does not enter Stage 3.
8. **Closure traceability synchronization.** Index the closure result under a
   separate documentation-only authorization. Stop before repository
   separation planning.
9. **Dedicated SniperBot repository-separation plan.** Define lineage,
   ownership, governance references, allowed initial files, prohibited
   transfers, validation, and rollback boundaries. Create no repository and
   move or copy no files.
10. **Dedicated SniperBot repository creation and lineage initialization.**
    Under separate authority, create only the repository and its approved
    provenance/governance initialization. Do not import implementation or
    begin a future stage unless separately authorized.
11. **Future SniperBot stage authorization.** Only after the dedicated
    repository and lineage are independently verified may a separate founder
    process select a future stage and, if implementation is requested, issue
    a current exact implementation task order in that repository.

Any failed, blocked, stale, revoked, conflicting, or incomplete lane halts the
sequence. No later lane may be started to work around an earlier result.

## Stage Posture

- Advancement Gate: **FAIL**
- Stage 2: **HOLD**
- Stage 2 closure: not authorized and not performed
- Stage 3: **UNENTERED AND UNAUTHORIZED**
- Dedicated SniperBot repository: not authorized and not created
- Future implementation: not authorized

## Explicit Non-Authorization Boundaries

This decision does not create, grant, imply, validate, approve, certify, or
authorize:

- a SniperBot repository or migration;
- moving, copying, deleting, renaming, squashing, filtering, or rewriting
  files or history;
- an implementation task order or retroactive implementation authority;
- implementation, remediation, source, schema, API, evaluator, test, package,
  validator, workflow, dependency, or configuration changes;
- Stage-2-wide evidence acceptance or completion certification;
- closure authority, Stage 2 closure, an Advancement Gate rerun, or a changed
  gate result;
- Stage 3 entry or any future stage;
- integration, orchestration, persistence, networking, registration, runtime,
  monitoring, deployment, or activation;
- market-data, signal, strategy, risk, sizing, allocation, broker, exchange,
  wallet, custody, credential, routing, order, paper-trading, simulation,
  execution, capital, or live-money capability; or
- any change to the Governed Agentic Engineering methodology repository.

Documentation is not authority. Evidence acceptance is not certification.
Certification is not closure. Closure is not Stage 3 entry. Repository
separation is not implementation authorization.

## Closing Decision

The governed repository boundary is **RETAIN THROUGH STAGE 2 CLOSURE**.

Echoauth-core remains the sole authority for the complete SniperBot Stage 2
record until a separately authorized formal closure succeeds. Repository
separation may be planned only after that closure and may be executed only
under another separate authorization that preserves the full Echoauth-core
lineage.

The exact next dependency after publication of this decision is a separate
founder-authorized, read-only Stage-2-wide evidence consolidation and
independent acceptance review. That next dependency is not executed or
authorized by this record.

Exact next bounded lane: **Stage-2-wide evidence consolidation and independent
acceptance review**.

- Repository created: **NO**.
- Files moved or copied: **NO**.
- Implementation task order created: **NO**.
- Advancement Gate rerun: **NO**.

The Advancement Gate remains **FAIL**. Stage 2 remains **HOLD**. Stage 3
remains **UNENTERED AND UNAUTHORIZED**.
