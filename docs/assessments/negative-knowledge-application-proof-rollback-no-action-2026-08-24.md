# Negative-Knowledge Application Proof — Rollback / No-Action — 2026-08-24

## Status

OWNER-AUTHORIZED — DOCUMENTATION-ONLY APPLICATION PROOF — NON-RUNTIME

Authority: Nicholas B. Carty (N.B.C.)

Source thesis commit: `8c07cc5cc1ff3bd7bb3a7aac1a0c37f9883ac5e4`

LocalOps: UNCHANGED / OUT OF SCOPE

NI AI Spine: UNCHANGED

Governed Agentic Engineering: UNCHANGED

## Selected historical engineering lane

The strongest application proof is the SniperBot Stage 2 Rollback / No-Action Fallback unknown-condition repair and subsequent bounded implementation.

The relevant lineage is:

```text
1ca0f9af41e82ba5b03d66ffa3be744e4768623c
schema: add rollback no action fallback decision

26b2ef91f48e4e1d9e829470b78f9852b3488027
docs: resolve rollback unknown condition schema boundary

c172aaed8382399c117fe9fc5653ac80b3f63965
feat: add rollback no-action fallback evaluator

e9b4dddeca3ab8d1cb0867c53d1c2c2d9bc71a95
test: complete rollback no-action evidence

d16fc872629aed3f4e5a46a6df58bd55332a27b1
docs: accept rollback no-action implementation evidence
```

## Event

The schema vocabulary contained `UNKNOWN_CONDITION`, creating a possible interpretation that the evaluator might emit that reason for unknown or uncovered inputs.

Implementation-surface verification established a narrower fact: valid typed request combinations were already covered by approved deterministic branches and ordinary fallback. Unknown raw enum values were rejected before typed request construction.

Therefore an emitted `UNKNOWN_CONDITION` branch was not supported by the closed typed input model.

## Original possibility

A plausible but unsupported future path was:

```text
UNKNOWN OR OPAQUE INPUT
-> CONVERT TO UNKNOWN_CONDITION
-> ADD OR USE A GENERIC UNKNOWN-CONDITION BRANCH
```

That path could have been implemented by adding a trigger, fallback branch, opaque-input interpretation, or broader evaluator behavior.

## Demonstrated boundary

The founder decision at `26b2ef91f48e4e1d9e829470b78f9852b3488027` preserved `UNKNOWN_CONDITION` as repository vocabulary while making it non-emittable by this subject.

The evidence-supported boundary was:

```text
UNKNOWN_CONDITION MAY EXIST AS RESERVED VOCABULARY
BUT
THE ROLLBACK / NO-ACTION EVALUATOR MUST NOT EMIT IT
FROM THE CLOSED TYPED REQUEST SPACE
```

The record also preserved that unknown raw enum values are rejected before typed request creation rather than converted into `UNKNOWN_CONDITION`.

## What was preserved as negative knowledge

Do not solve the unsupported gap by:

- inventing a new trigger;
- adding an unknown enum path;
- preserving opaque raw values inside an approved decision;
- interpreting opaque condition or FSM context;
- adding a generic unknown-condition fallback;
- broadening evaluator authority.

This is negative knowledge because the record preserves a demonstrated non-selection: those implementation paths are not valid under the established typed contract and evidence.

## Constraint without prescription

The negative boundary did not dictate the entire later implementation.

Multiple implementation choices still remained, including the internal organization of the pure evaluator, dataclass structure, enum representation, helper structure, validation placement, and direct test organization, provided they remained inside the approved contract.

The boundary constrained one class of invalid behavior while leaving the remaining design space open.

The later implementation at `c172aaed8382399c117fe9fc5653ac80b3f63965` selected one bounded design from that remaining space: the full 14-value `ReasonCode` vocabulary remained present, while a separate `EmittableReasonCode` excluded `UNKNOWN_CONDITION` from evaluator output.

## Verification

The implementation-evidence acceptance at `d16fc872629aed3f4e5a46a6df58bd55332a27b1` records that:

- `UNKNOWN_CONDITION` remains vocabulary-only and is not emitted;
- valid typed requests are deterministically covered;
- unknown raw inputs are rejected before typed construction;
- no hidden fallback or free-text replacement exists;
- focused tests passed: 9;
- contract and Authority Clarity tests passed: 30;
- full suite passed: 411;
- `git diff --check` passed;
- prohibited-import and side-effect inspection passed.

## Thesis test

### A. Was the boundary evidence-based?

PASS.

The boundary followed verification of the closed typed request space and deterministic branch coverage.

### B. Was it conditional rather than universal?

PASS.

`UNKNOWN_CONDITION` was not deleted from all repository vocabulary. It was preserved for traceability and possible future separately governed use, while being non-emittable by this subject.

### C. Did later work avoid rediscovering the same invalid path?

PASS.

The evaluator encoded a separate emittable vocabulary and did not add an unknown-condition branch. Later acceptance explicitly verified non-emission.

### D. Did the negative knowledge constrain rather than dictate?

PASS.

It prohibited unsupported unknown-condition emission but did not prescribe the evaluator's complete implementation structure.

### E. Did authority remain separate from capability?

PASS.

The repair record stated that no implementation was authorized by the schema repair itself. A later separate implementation step produced the evaluator. EchoAuth remained the sole permission authority, and Stage 3 remained unauthorized.

### F. Was the later result verified?

PASS.

Direct tests, contract tests, the full suite, diff validation, and implementation-evidence acceptance were recorded before the lane was accepted.

## Constructive return

The lesson can be returned in this form:

```text
WHAT HAPPENED
A vocabulary item suggested a possible generic unknown-condition output.

WHAT WAS LEARNED
The closed typed request space did not support that output path.

WHAT SHOULD NOT BE REPEATED
Do not manufacture generic fallback behavior merely because vocabulary exists for it.

WHAT REMAINS POSSIBLE
Preserve the reserved vocabulary, implement the bounded deterministic evaluator, and leave future separately governed uses open.

WHAT EVIDENCE IS NEEDED NEXT
A future use of UNKNOWN_CONDITION would require its own explicit trigger, contract, authority, and verification evidence.
```

## Application-proof result

```text
APPLICATION PROOF: PASS
EXAMPLE: SNIPERBOT STAGE 2 ROLLBACK / NO-ACTION UNKNOWN-CONDITION REPAIR
NEGATIVE BOUNDARY: UNKNOWN_CONDITION RESERVED BUT NON-EMITTABLE FOR THIS SUBJECT
FUTURE POSSIBILITY: CONSTRAINED WITHOUT PRESCRIBING THE COMPLETE IMPLEMENTATION
SOURCE THESIS: 8c07cc5cc1ff3bd7bb3a7aac1a0c37f9883ac5e4
RUNTIME CHANGE: NONE
HISTORICAL REWRITE: NONE
NI AI SPINE CHANGE: NONE
GOVERNED-AGENTIC-ENGINEERING CHANGE: NONE
LOCALOPS CHANGE: NONE
RESULT: NEGATIVE-KNOWLEDGE THESIS SUPPORTED BY A PRIOR ENGINEERING LANE
STOP
```
