# N.B.C. AUTHORITY — A15 REVOCATION / EXPIRATION OF INHERITED CONTEXT ORDER

**Authority:** Nicholas B. Carty (N.B.C.)  
**Date:** August 28, 2026  
**Decision:** ADVANCE — CONTEXT REVOCATION / FRESHNESS GOVERNANCE ONLY  
**Classification:** A15 — Revocation / Expiration of Inherited Context / Documentation Only

## Governing direction

Context may legitimately persist across sessions, agents, tools, repositories, interfaces, or human handoffs.

Persistence does not make that context permanently valid.

```text
REMEMBERED != CURRENT
PRESERVED != VALID FOREVER
PRIOR PERMISSION != PRESENT PERMISSION
PRIOR PASS != CURRENT PASS
OLD CONTEXT != FALSE CONTEXT
STALE CONTEXT != EXECUTION AUTHORITY
REVOCATION != ERASURE OF HISTORY
EXPIRATION != LOSS OF PROVENANCE
```

The correct system behavior is not to forget history. It is to distinguish historical evidence from currently usable authority-bearing information.

## A15 — Revocation / Expiration Axiom

> **Any context carried across a boundary MUST remain subject to freshness, revocation, scope, source, and current-authority checks before consequential reuse. When the conditions that made prior context valid have expired, changed, been withdrawn, contradicted, or become unverifiable, the context MAY remain preserved as historical evidence but MUST NOT silently continue as current permission or authority.**

Operational shorthand:

> **PRESERVE THE RECORD — EXPIRE THE AUTHORITY.**

## Revocation triggers

A receiving system or participant should reassess inherited context when relevant conditions change, including:

- authority withdrawn or superseded;
- permission expired;
- source corrected prior information;
- scope changed;
- identity or role changed;
- relevant state changed;
- evidence became stale;
- a newer checkpoint superseded the old one;
- a conflict appears between preserved records;
- the current boundary cannot verify whether prior conditions still hold.

## Operating sequence

```text
INHERITED CONTEXT
-> VERIFY SOURCE
-> CHECK CHECKPOINT
-> CHECK FRESHNESS
-> CHECK REVOCATION
-> CHECK CURRENT SCOPE
-> CHECK CURRENT AUTHORITY
-> CHECK CURRENT PERMISSION
-> VALID / EXPIRED / REVOKED / CONFLICTED / UNRESOLVED
-> CONTINUE, REQUEST, HOLD, OR STOP
```

## Historical preservation boundary

Revoking or expiring authority does not require destroying the underlying record.

```text
HISTORY MAY REMAIN
PROVENANCE MAY REMAIN
TIMESTAMP MAY REMAIN
PRIOR DECISION MAY REMAIN
CURRENT AUTHORITY MAY NOT
```

This preserves accountability and replay without allowing history to become permanent permission.

## SAL implementation boundary

A15 defines governance behavior that SAL may later implement or be validated against. The documentation does not establish that SAL already performs this behavior.

```text
GOVERNANCE DEFINITION != IMPLEMENTATION
DESIRED SYSTEM BEHAVIOR != ESTABLISHED RUNTIME BEHAVIOR
DOCUMENTATION != EXECUTION
FUTURE CAPABILITY != CURRENT EVIDENCE
```

Whether SAL conforms to A15 must be established independently through implementation evidence and testing.

## Relationship to A14

```text
A14: CARRY CONTEXT — REVALIDATE AUTHORITY
A15: PRESERVE THE RECORD — EXPIRE THE AUTHORITY
A14 = SAFE CONTINUITY
A15 = SAFE DISCONTINUITY
```

Together they establish that a governed system must know both how to continue and when continuation is no longer justified.

## EchoAuth correspondence

EchoAuth may preserve:

- provenance;
- timestamps;
- evidence lineage;
- previous dispositions;
- responsibility attribution;
- revocation records;
- superseding checkpoints.

But the interface must distinguish:

```text
HISTORICAL RECORD
!=
CURRENT AUTHORIZATION
```

When current authority or meaning cannot be established:

**HOLD / REQUEST / REASSESS / NO-ACTION.**

## Boundary

This order does not authorize runtime activation, autonomous execution, deletion of historical records, silent invalidation of legitimate human authority, automatic revocation without an attributable basis, or any claim that SAL already implements this behavior.

It does not change the broader runtime evidence state.

**SAL-9 remains: HOLD — 3 PASS / 2 HOLD-PARTIAL / 0 FAIL.**

**Lane status:** ADVANCE — A15 governance definition established; SAL implementation remains independently testable; runtime posture unchanged.
