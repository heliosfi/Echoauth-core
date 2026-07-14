# SniperBot Stage 2 Rollback / No-Action Fallback Unknown-Condition Founder Decision Record

## Status and Boundary

Documentation-only / governance-only / schema-consistency-only /
founder-decision-record-only / non-runtime / non-execution / non-authorizing.

Starting checkpoint: `1ca0f9af41e82ba5b03d66ffa3be744e4768623c` (`schema: add
rollback no action fallback decision`).

The implementation-surface verification found that `UNKNOWN_CONDITION` is not
deterministically reachable from the closed typed request. All valid typed
combinations are covered by the approved first-match branches and ordinary
fallback. No new trigger, field, interpretation, or capability is authorized.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized. EchoAuth
remains the sole permission authority.

## Founder Decision

`UNKNOWN_CONDITION_VOCABULARY_ONLY_NON_EMITTABLE`

The full repository reason-code vocabulary remains exactly 14 values. The
subject-emittable vocabulary is exactly 13 values; `UNKNOWN_CONDITION` is
reserved for traceability and future separately governed use only. The
classifier must never emit it.

Unknown raw enum values continue to be rejected before typed request creation.
The classifier must not convert unknown input into `UNKNOWN_CONDITION`, add an
unknown enum, retain opaque values in an approved decision, interpret opaque
condition or FSM context, or add a fallback branch. Ordinary valid fallback
remains `NO_ACTION / NO_ACTION_REQUIRED / NONE`.

## Schema Responsibility

The schema preserves the full 14-value `ReasonCode` vocabulary and defines a
separate 13-value `SubjectEmittableReasonCode` used by emitted decisions.
`UNKNOWN_CONDITION` therefore remains documented repository vocabulary while
being impossible as a valid emitted decision reason. Cross-object and
procedural behavior remains evaluator-owned; no implementation is authorized.

No outcome, reason code, RequiredAction, state, authority meaning, request
field, precedence, mapping, rollback behavior, recovery behavior, reset,
integration, or runtime capability is changed.

## Validation and Stop Conditions

Validate JSON parsing and Draft 2020-12 structure; counts of 14 full and 13
emittable reasons, 2 outcomes, 5 RequiredAction values, and 3 emittable
actions; rejection of `UNKNOWN_CONDITION` in `Decision.reason_code`; ordinary
fallback; file scope; index uniqueness; `git diff --check`; contract and
Authority Clarity tests; and the full suite. Stop on any need for a new field,
trigger, vocabulary, interpretation, mapping, precedence, implementation,
workflow, dependency, or unrelated change.

Future Python implementation and tests remain separately unauthorized. The
exact next founder decision is to authorize a separate read-only post-repair
implementation-readiness verification.
