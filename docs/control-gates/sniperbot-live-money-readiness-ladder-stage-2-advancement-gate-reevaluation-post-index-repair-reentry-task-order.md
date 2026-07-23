# SniperBot Stage 2 Advancement Gate Post-Index-Repair Re-entry Read-Only Re-evaluation Task Order

## Status and Boundary

**ISSUED -- NOT EXECUTED -- READ-ONLY RE-EVALUATION ONLY -- SINGLE USE --
FAIL CLOSED -- NON-REPLAYABLE -- DOCUMENTATION ONLY -- GOVERNANCE ONLY -- NO
STAGE 3 AUTHORITY -- NO IMPLEMENTATION AUTHORITY -- NO RUNTIME AUTHORITY**

This task order authorizes exactly one later read-only Advancement Gate
re-evaluation by a genuinely fresh independent Codex session. It does not
authorize this publishing session to execute the re-evaluation.

## Task-Order Identity

- Task-order identity:
  `SNIPERBOT-STAGE2-ADVANCEMENT-GATE-POST-INDEX-REPAIR-REENTRY-TASK-ORDER-c65571f0a834519be63d391e492d464f903d2f3c`
- Task-order path:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-advancement-gate-reevaluation-post-index-repair-reentry-task-order.md`
- Direct founder authorization record:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-advancement-gate-reevaluation-post-index-repair-reentry-founder-authorization-record.md`
- Direct founder authorization identity:
  `SNIPERBOT-STAGE2-ADVANCEMENT-GATE-POST-INDEX-REPAIR-REENTRY-FOUNDER-AUTHORIZATION-c65571f0a834519be63d391e492d464f903d2f3c`
- Repository: `heliosfi/Echoauth-core`
- Branch: `main`
- Authoritative starting checkpoint:
  `c65571f0a834519be63d391e492d464f903d2f3c`
- Canonical-index repair publication checkpoint:
  `c65571f0a834519be63d391e492d464f903d2f3c`

## Publication-Checkpoint Binding

This order is bound to the final publication checkpoint created by the lane
that first publishes this task order and its companion founder authorization
record to `origin/main`.

Because a file cannot contain its own future commit SHA without changing that
SHA, the final publication checkpoint is defined as the exact commit SHA that
first adds both authorized records to `main` and is later verified by local
`HEAD`, local `origin/main`, and live remote `main`. The executing session must
resolve and report that exact SHA before evaluation. If that checkpoint cannot
be established, differs across local or remote references, or is not clean and
synchronized, the required result is `BLOCKED`.

## Fresh-Session Independence

The executing evaluator must be a genuinely fresh independent Codex session.
Execution is prohibited for any session that participated in:

- drafting either post-index-repair re-entry document;
- reviewing either document;
- recording the founder authorization;
- publishing the documents;
- staging, committing, pushing, or synchronizing the publication;
- this construction lane; or
- any action that could reasonably compromise independent re-evaluation.

If independence cannot be affirmatively established, the required result is
`BLOCKED`.

## Mandatory Execution-Time Preconditions

Before substantive evaluation, the fresh independent evaluator must verify:

1. repository identity is exactly `heliosfi/Echoauth-core`;
2. branch identity is exactly `main`;
3. local `HEAD`, local `origin/main`, and live remote `main` all equal the final
   publication checkpoint;
4. divergence is `0/0`;
5. the index and worktree are clean;
6. no tracked or untracked changes exist;
7. no Git lock files exist;
8. this task-order identity and path are exact;
9. the direct founder authorization identity and path are exact;
10. the direct founder authorization is current, applicable, unrevoked,
    unsuperseded, conflict-free, and ambiguity-free;
11. the canonical-index repair checkpoint is present in the governing lineage;
12. all relied-on evidence is current, applicable, traceable, and provenance
    complete;
13. all governing lineage references are present and internally consistent;
14. no revocation, supersession, conflict, ambiguity, or intervening authority
    defect exists; and
15. this task order has not already been consumed.

Any missing, stale, conflicting, ambiguous, untraceable, altered, revoked,
superseded, or unverifiable prerequisite requires `BLOCKED`.

## Governing Lineage to Re-check

The evaluator must re-check the complete governing lineage, including at
minimum:

- Canonical Advancement Gate:
  `docs/control-gates/sniperbot-live-money-readiness-advancement-gate-non-authorization-boundary-review.md`
- Original gate decision:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-advancement-gate-decision-review.md`
- Repository-boundary and disposition decision:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-repository-boundary-and-disposition-decision.md`
- Stage-2-wide evidence acceptance:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-wide-evidence-acceptance.md`
- Stage 2 completion certification:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-completion-certification.md`
- Stage 2 formal closure:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-formal-closure-record.md`
- Post-closure authority review:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-post-closure-authority-review.md`
- Post-closure evidence-integrity audit:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-post-closure-evidence-integrity-audit.md`
- Re-evaluation readiness review:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-advancement-gate-reevaluation-readiness-review.md`
- Original task order:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-advancement-gate-reevaluation-task-order.md`
- Original disposition:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-repository-boundary-and-disposition-decision.md`
- Renewal founder authorization:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-advancement-gate-reevaluation-renewal-founder-authorization-record.md`
- Renewed task order:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-advancement-gate-reevaluation-renewed-task-order.md`
- Second-renewal founder authorization:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-advancement-gate-reevaluation-second-renewal-founder-authorization-record.md`
- Second-renewed task order:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-advancement-gate-reevaluation-second-renewed-task-order.md`
- Second-renewed blocked disposition:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-advancement-gate-reevaluation-second-renewed-blocked-disposition-record.md`
- Prior gate-reentry founder authorization:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-advancement-gate-reevaluation-gate-reentry-founder-authorization-record.md`
- Fresh-reentry task order:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-advancement-gate-reevaluation-fresh-reentry-task-order.md`
- Fresh-reentry substantive `FAIL` disposition:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-advancement-gate-reevaluation-fresh-reentry-fail-disposition-record.md`
- Canonical indexes repaired at the starting checkpoint:
  `README.md` and `docs/control-gates/README.md`

The evaluator must also preserve every current Stage 3, implementation,
runtime, deployment, trading, live-execution, broker, Robinhood, funding,
autonomous-action, and command-execution non-authorization boundary recorded in
the governing lineage and canonical indexes.

## Permitted Evaluation Only

If and only if every execution-time precondition passes, the evaluator may
perform one read-only re-evaluation of the Advancement Gate against the current
governing lineage and evidence. The evaluator must not repair evidence, modify
indexes, create artifacts, run implementation, alter schemas, alter validators,
alter tests, alter CI, change runtime behavior, or take any follow-on action.

## Closed Result Vocabulary

The evaluator must issue exactly one of:

- `PASS`
- `FAIL`
- `BLOCKED`

No other result label is permitted.

`PASS` may be issued only if the fresh evaluator independently verifies that
all gate requirements, lineage requirements, evidence requirements, currentness
requirements, and authority requirements are satisfied.

`FAIL` may be issued only if substantive evaluation validly completes and one
or more substantive gate requirements remain unmet.

`BLOCKED` must be issued if any prerequisite involving independence, authority,
checkpoint synchronization, cleanliness, currentness, provenance, traceability,
applicability, revocation, supersession, conflict, ambiguity, or lineage cannot
be verified.

## Single-Use and Expiry

This order is single-use, fail-closed, non-transferable, non-expandable,
non-replayable, and non-renewable in place. It expires immediately after one
valid `PASS`, `FAIL`, or `BLOCKED` determination; attempted execution by a
disqualified session; founder revocation; superseding authority; identity or
scope mismatch; or alteration of its vocabulary, boundaries, or lineage.

Expiration creates no replacement authority.

## Explicit Non-Authorization

This task order does not authorize:

- Stage 3 entry, planning, construction, implementation, or execution;
- source-code, schema, API, evaluator, test, CI, dependency, configuration,
  LocalOps, Event Bus, runtime, or deployment changes;
- implementation task orders, approval records, approval mechanisms, approval
  workflows, broker access, market-data access, Robinhood access, order
  routing, paper trading, simulation runtime, live trading, funding movement,
  capital movement, operational activity, autonomous action, or command
  execution;
- repository mutation during execution;
- repair, reinterpretation, reversal, cure, or replacement of any prior
  consumed determination except by the single permitted read-only result; or
- follow-on authority by inference.

Even a later `PASS` does not itself authorize Stage 3, implementation, runtime
activation, deployment, trading, funding, or live execution. Any such movement
would require separate explicit founder authority outside this order.

## Preserved Posture

- Stage 2: **FORMALLY CLOSED**
- Canonical indexing dependency: **REPAIRED**
- Previous fresh-reentry task order: **CONSUMED -- EXPIRED**
- Previous determination: **FAIL -- SUBSTANTIVE**
- New task order: **ISSUED -- NOT EXECUTED**
- Advancement Gate: **AWAITING NEW RE-EVALUATION**
- Stage 3: **UNENTERED AND UNAUTHORIZED**
- Implementation authority: **NONE**
- Runtime authority: **NONE**
- Deployment authority: **NONE**
- Trading authority: **NONE**
- Live-execution authority: **NONE**
