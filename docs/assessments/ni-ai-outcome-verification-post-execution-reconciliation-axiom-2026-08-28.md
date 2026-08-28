# N.B.C. AUTHORITY — A20 OUTCOME VERIFICATION / POST-EXECUTION RECONCILIATION ORDER

**Authority:** Nicholas B. Carty (N.B.C.)  
**Date:** August 28, 2026  
**Decision:** ADVANCE — OUTCOME VERIFICATION / RECONCILIATION GOVERNANCE ONLY  
**Classification:** A20 — Observed Outcome, Authorized Expectation, and Post-Execution Reconciliation / Documentation Only

## Governing direction

Execution creates an event.

It does not prove that the intended, authorized, or expected result actually occurred.

```text
EXECUTED != VERIFIED
RETURNED != CORRECT
NO ERROR != VERIFIED SUCCESS
EXPECTED OUTCOME != OBSERVED OUTCOME
COMPLETION != CONFORMANCE
SIDE EFFECT != AUTHORIZED EFFECT
PARTIAL SUCCESS != FULL SUCCESS
SUCCESS SIGNAL != VERIFIED RESULT
OBSERVED RESULT != NEW AUTHORITY
RESULT != REAUTHORIZATION
```

A governed system must distinguish between what was supposed to happen and what evidence shows actually happened.

## A20 — Outcome Verification / Reconciliation Axiom

> **After consequential execution, a governed system MUST preserve and evaluate the observed result against the authorized action, target, scope, material conditions, expected consequence, and applicable success criteria before treating the action as successfully completed or allowing its result to support consequential continuation. Any material discrepancy, unexpected effect, unverifiable outcome, incomplete evidence, or scope deviation MUST be surfaced for reassessment rather than silently normalized into success.**

Operational shorthand:

> **OBSERVE WHAT HAPPENED — COMPARE WHAT WAS AUTHORIZED — RECONCILE BEFORE CONTINUING.**

## Minimum reconciliation record

```text
EXECUTION IDENTITY
-> AUTHORIZED ACTION
-> AUTHORIZED TARGET
-> AUTHORIZED SCOPE
-> EXPECTED OUTCOME
-> OBSERVED OUTCOME
-> OBSERVED SIDE EFFECTS
-> EVIDENCE / PROVENANCE
-> COMPLETION STATE
-> DISCREPANCIES
-> CURRENT CONSEQUENCE
-> RECONCILIATION STATUS
```

## Outcome classifications

A returned result should be capable of being classified as:

```text
VERIFIED-AS-EXPECTED
VERIFIED-WITHIN-BOUNDS
PARTIAL
DIVERGENT
UNEXPECTED-SIDE-EFFECT
FAILED
INDETERMINATE
UNVERIFIABLE
CONFLICTED
```

A label of success should require evidence supporting the relevant success condition.

## No silent normalization

The system MUST NOT assume:

```text
HTTP 200 = BUSINESS SUCCESS
PROCESS EXIT = CORRECT RESULT
MESSAGE SENT = MESSAGE RECEIVED
WRITE COMPLETED = INTENDED STATE ACHIEVED
NO EXCEPTION = NO SIDE EFFECT
PARTIAL MATCH = FULL CONFORMANCE
EXPECTED VALUE = OBSERVED VALUE
```

Technical completion and governed success are different questions.

## Discrepancy boundary

Where the observed result materially differs from the authorized expectation:

```text
DISCREPANCY
-> PRESERVE EVIDENCE
-> IDENTIFY DIFFERENCE
-> ASSESS CONSEQUENCE
-> CHECK WHETHER AUTHORIZED BOUNDS WERE EXCEEDED
-> CHECK REVERSIBILITY / RECOVERY
-> RETURN TO GOVERNANCE
-> REASSESS
```

The system must not hide, overwrite, repair, retry, or reinterpret the discrepancy merely to produce a favorable result.

## Retry and remediation boundary

```text
BAD RESULT != RETRY AUTHORITY
PARTIAL RESULT != COMPLETION
UNEXPECTED EFFECT != AUTHORITY TO REPAIR
REMEDIATION != ORIGINAL EXECUTION
ROLLBACK != AUTOMATIC PERMISSION
```

A corrective action, retry, rollback, or remediation is itself an action and must remain subject to the applicable governance boundary.

## Operating sequence

```text
EXECUTION
-> RESULT
-> PRESERVE RESULT
-> COLLECT OBSERVABLE EVIDENCE
-> COMPARE AGAINST AUTHORIZED ACTION
-> COMPARE AGAINST TARGET
-> COMPARE AGAINST SCOPE
-> COMPARE AGAINST EXPECTED CONSEQUENCE
-> IDENTIFY DISCREPANCIES
-> CLASSIFY OUTCOME
-> RECORD
-> RETURN
-> REASSESS
-> CLOSE / REQUEST / HOLD / REMEDIATE / STOP
```

## Relationship to A14–A19

```text
A14: CARRY CONTEXT — REVALIDATE AUTHORITY
A15: PRESERVE THE RECORD — EXPIRE THE AUTHORITY
A16: COMPARE THE RECORD — RESOLVE THE BOUNDARY
A17: VERIFY WHO — VERIFY ROLE — VERIFY SCOPE
A18: ASK WHAT — FOR WHAT — HOW FAR — UNTIL WHEN
A19: BIND BEFORE ACT — RETURN BEFORE CONTINUING
A20: OBSERVE — COMPARE — RECONCILE
```

The governed sequence now becomes:

```text
CONTEXT
-> CURRENTNESS
-> CONFLICT
-> REPRESENTATION
-> PERMISSION
-> EXECUTION BINDING
-> EXECUTION
-> OBSERVATION
-> OUTCOME VERIFICATION
-> RECONCILIATION
-> REASSESSMENT
```

## EchoAuth correspondence

EchoAuth may preserve:

- execution identity;
- governing checkpoint;
- authorized action and target;
- scope and consequence boundary;
- execution disposition;
- returned result;
- observed state;
- evidence references;
- discrepancy classification;
- rollback or remediation status;
- final reconciliation disposition.

The critical distinction is:

```text
EXECUTION RESULT
!=
VERIFIED GOVERNED OUTCOME
```

When the outcome cannot be reconciled:

**REQUEST / HOLD / REASSESS / NO-ACTION.**

## SAL implementation boundary

A20 defines expected system-governance behavior.

```text
A20 DOCUMENTATION != SAL IMPLEMENTATION
RETURNED RESULT != VERIFIED RESULT
DEFINED RECONCILIATION != EXECUTABLE RECONCILER
OUTCOME LABEL != OBSERVED EVIDENCE
AUDIT RECORD != PROVEN POST-EXECUTION CONSUMER
```

Whether SAL can independently observe, compare, classify, preserve, and reconcile post-execution results remains an implementation and validation question.

## Boundary

This order does **not** authorize:

- runtime activation;
- external execution;
- automatic retries;
- autonomous remediation;
- silent rollback;
- reinterpretation of discrepancies as success;
- continuation from an unverified outcome;
- treating audit presence as proof of correctness;
- any change to the existing SAL validation result.

**SAL-9 remains: HOLD — 3 PASS / 2 HOLD-PARTIAL / 0 FAIL.**

**Lane status:** **ADVANCE — A20 outcome-verification and post-execution reconciliation governance defined; implementation and runtime evidence remain independently testable.**