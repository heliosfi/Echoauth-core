# SniperBot Live-Money Readiness Ladder Stage 2 Authority-Resolution Governance Record

## Status

Documentation-only / governance-only / authority-resolution-only.

Founder selection is recorded only for the bounded SniperBot Stage 2
authority-resolution governance lane.

Current Stage 2 outcome: **HOLD**.

Stage 3 is not entered or authorized.

This record does not authorize implementation, source-code changes, runtime,
simulation, paper trading, broker access, order routing, credentials, capital
deployment, live trading, or LocalOps work.

## Founder Selection and Lane Boundary

The founder selects **SniperBot** as the active subject for this bounded lane:
SniperBot Stage 2 authority-resolution governance.

LocalOps is outside this lane and receives no selection, authority, or work
scope from this record.

This lane establishes governance documentation needed to resolve the
documented approval and task-order structure gaps. It does not resolve
evidence acceptance, grant an implementation approval, or advance the
live-money readiness ladder.

## Approval Mechanism

The Stage 2 founder-approval mechanism is a human-governance decision format
with exactly these outcomes:

| Outcome | Meaning | Effect on implementation |
| --- | --- | --- |
| `APPROVE` | The founder explicitly approves the exact bounded subject named in a current approval record. | Does not authorize implementation by itself; a separate exact bounded implementation task order is still required. |
| `REJECT` | The founder denies the named subject. | No implementation, runtime, broker, trading, or Stage 3 movement may rely on the rejected subject. |
| `HOLD` | Required authority, evidence, scope, currentness, or task-order conditions are incomplete. | No advancement or implementation is permitted. |
| `ESCALATE` | The named subject requires further human authority review or a separately bounded governance decision. | No automatic advancement or implementation is permitted. |

The mechanism records and verifies a human decision; it does not generate,
infer, or expand approval. Silence, document presence, README indexing,
commits, workflow success, Slack, logs, handoffs, and Codex output are not
mechanism outcomes and cannot substitute for one.

## Durable Approval-Record Format

Any future approval record for this lane must be durable in the repository and
contain all of the following fields:

1. unique record identifier and title;
2. exact subject and requested action;
3. decision outcome (`APPROVE`, `REJECT`, `HOLD`, or `ESCALATE`);
4. named founder or otherwise valid human approving authority;
5. decision timestamp and currentness/revalidation boundary;
6. exact founder task-order reference;
7. evidence references and unresolved-evidence statement, if applicable;
8. explicit allowed scope and explicit exclusions;
9. safety, risk, broker, runtime, execution, and LocalOps boundaries;
10. rejection, hold, escalation, expiration, and revocation handling; and
11. a statement that the record does not itself authorize implementation.

An approval record is valid only for its exact subject, scope, authority, and
currentness window. A format, blank record, historical record, or broad record
does not authorize another action.

## Approval Workflow

Only the founder, or a human authority explicitly designated by a separate
current founder task order, may issue an `APPROVE` or `REJECT` outcome. No
workflow, mechanism, CI result, repository event, or delegated system may
issue approval by inference.

Before a future outcome may be recorded, the workflow requires:

1. a current, explicit, founder-selected bounded task order;
2. the exact subject, allowed files/actions, and prohibited actions;
3. current, task-specific evidence references;
4. scope, exclusion, safety, and risk review;
5. confirmation that no runtime, broker, trading, execution, or LocalOps
   authority is being inferred; and
6. human review of the record and its outcome.

Missing, stale, broad, ambiguous, inherited, revoked, or non-traceable inputs
must result in `HOLD`, `REJECT`, or `ESCALATE`; they must never result in
automatic approval.

## Separate Implementation Task-Order Rule

No code change may begin from this record, an `APPROVE` outcome, or any
approval record alone. A separate implementation task order must be created
and explicitly approved for the exact implementation subject before any code
change is authorized.

That future implementation task order must name the allowed files, allowed
actions, prohibited actions, required validation, unsafe outcomes that must
remain impossible, and the approval record it may rely on. It must not enter
Stage 3 by implication.

## Current Stage 2 Determination

Stage 2 remains **HOLD**. This record does not create a current implementation
task order, approve evidence acceptance, certify readiness, or resolve the
remaining authority decision for a specific implementation subject.

Stage 3 is not entered or authorized. Any future Stage 2 re-gate decision,
evidence-acceptance decision, founder approval for a specific subject, or
implementation task order requires a separate explicit founder-selected
bounded task order.

## Non-Authority Sources

Slack and handoffs are coordination only. CI results, commits, logs, README
entries, workflow output, and Codex output are evidence or traceability only.
None independently creates authority, founder approval, an approval outcome,
evidence acceptance, an implementation task order, or permission to act.

## Closing Boundary

This record is limited to SniperBot Stage 2 authority-resolution governance.
It creates no runtime capability, execution capability, broker access,
trading authority, implementation approval, or LocalOps scope.
