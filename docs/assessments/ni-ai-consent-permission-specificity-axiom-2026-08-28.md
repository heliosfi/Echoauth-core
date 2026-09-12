# N.B.C. AUTHORITY — A18 CONSENT / PERMISSION SPECIFICITY ORDER

**Authority:** Nicholas B. Carty (N.B.C.)  
**Date:** August 28, 2026  
**Decision:** ADVANCE — CONSENT / PERMISSION SPECIFICITY GOVERNANCE ONLY  
**Classification:** A18 — Consent, Permission, Scope, and Consequence Specificity / Documentation Only

## To whom it may concern — reader-first meaning

The purpose of A18 is simple:

> **A system should do only what was actually authorized, for the purpose and scope that were actually authorized. When permission is unclear, incomplete, expired, withdrawn, or does not cover the consequence being considered, the system should ask, hold, reassess, or take no action rather than silently expanding permission.**

This is not a claim for power over people. It is a restraint on systems.

It does not mean every low-consequence interaction requires a formal contract. It means consequential action must not be justified by ambiguity, technical capability, access, silence, past permission, or a broad interpretation that the evidence does not support.

## Governing direction

Permission is not a general property that automatically follows a person, role, account, session, interface, or prior interaction.

Permission belongs to an attributable boundary.

```text
CAPABILITY != PERMISSION
ACCESS != PERMISSION
AWARENESS != PERMISSION
SILENCE != PERMISSION
PAST PERMISSION != PRESENT PERMISSION
PERMISSION FOR A != PERMISSION FOR B
READ PERMISSION != WRITE PERMISSION
SHARING != TRANSFORMATION
TRANSFORMATION != EXECUTION
AUTHENTICATION != CONSENT
BROAD WORDING != UNLIMITED SCOPE
```

## A18 — Consent / Permission Specificity Axiom

> **Before consequential action, a governed system MUST establish that the applicable permission is attributable, current, sufficiently specific to the actor, action, object or information, purpose, scope, conditions, and consequence under consideration. Permission for one action, purpose, recipient, transformation, or period MUST NOT silently expand into permission for another. Where the permission boundary remains ambiguous or cannot be verified, the system MUST request clarification, hold, reassess, or take no action.**

Operational shorthand:

> **ASK WHAT — FOR WHAT — HOW FAR — UNTIL WHEN.**

## Minimum permission record

```text
WHO GRANTED IT
-> TO WHOM / WHICH SYSTEM
-> FOR WHAT ACTION
-> OVER WHAT INFORMATION / RESOURCE / OBJECT
-> FOR WHAT PURPOSE
-> WITHIN WHAT SCOPE
-> UNDER WHAT CONDITIONS
-> FOR WHICH RECIPIENTS OR INTERFACES
-> WITH WHICH TRANSFORMATIONS, IF ANY
-> EFFECTIVE TIME
-> EXPIRATION / REVOCATION
-> CURRENT VALIDITY
```

Not every domain must encode these fields identically. The required detail should be proportionate to the consequence, while still being sufficient to prevent silent scope expansion.

## Consequence boundary

A system should not infer a more consequential permission from a less consequential one.

```text
VIEW != MODIFY
MODIFY != PUBLISH
PUBLISH != EXECUTE
RECOMMEND != DECIDE
DECIDE != ACT
ONE-TIME PERMISSION != CONTINUING PERMISSION
ONE RECIPIENT != ALL RECIPIENTS
ONE PURPOSE != ALL PURPOSES
```

Where an action would materially increase consequence, exposure, persistence, distribution, or irreversibility, permission should be reassessed at that boundary.

## Operating sequence

```text
PROPOSED CONSEQUENTIAL ACTION
-> IDENTIFY REQUIRED PERMISSION
-> IDENTIFY AUTHORIZED GRANTOR
-> CHECK ACTION
-> CHECK OBJECT / INFORMATION
-> CHECK PURPOSE
-> CHECK SCOPE
-> CHECK CONDITIONS
-> CHECK RECIPIENT / INTERFACE
-> CHECK TRANSFORMATION
-> CHECK TIME / FRESHNESS
-> CHECK REVOCATION
-> CHECK CONFLICTS
-> VALID / LIMITED / EXPIRED / REVOKED / AMBIGUOUS / UNVERIFIED
-> CONTINUE / REQUEST / HOLD / REASSESS / NO-ACTION
```

## Relationship to A14–A17

```text
A14: CARRY CONTEXT — REVALIDATE AUTHORITY
A15: PRESERVE THE RECORD — EXPIRE THE AUTHORITY
A16: COMPARE THE RECORD — RESOLVE THE BOUNDARY
A17: VERIFY WHO — VERIFY ROLE — VERIFY SCOPE
A18: ASK WHAT — FOR WHAT — HOW FAR — UNTIL WHEN
```

Together:

```text
CONTEXT CAN MOVE
AUTHORITY CAN EXPIRE
RECORDS CAN CONFLICT
REPRESENTATION CAN BE VALID OR INVALID
PERMISSION CAN BE SPECIFIC, LIMITED, REVOKED, OR UNRESOLVED

NONE OF THESE
AUTOMATICALLY CREATES
UNLIMITED AUTHORITY TO ACT
```

## EchoAuth correspondence

EchoAuth may preserve permission-related information including:

- who granted permission;
- the authorized recipient, system, or role;
- action and purpose;
- scope and conditions;
- permitted recipients or interfaces;
- authorized transformations;
- timestamps;
- expiration;
- revocation;
- superseding permissions;
- unresolved ambiguity.

EchoAuth should distinguish an information record about permission from a currently valid authorization to act.

```text
PERMISSION RECORD
!=
CURRENT AUTHORIZATION
```

When specificity or current validity cannot be established:

**REQUEST / HOLD / REASSESS / NO-ACTION.**

## Interpretation boundary

A18 is an evidence-bounded system-governance proposition. It does not replace domain-specific legal, medical, contractual, regulatory, cultural, institutional, or other consent requirements. Where another legitimate authority defines a stricter consent standard, the system must remain subject to that boundary.

## SAL implementation boundary

A18 defines expected governance behavior.

```text
A18 DOCUMENTATION != SAL IMPLEMENTATION
PERMISSION MODEL != EXECUTABLE ENFORCEMENT
CONSENT RECORD != PROVEN CURRENT AUTHORIZATION
DEFINED SCOPE CHECK != PROVEN RUNTIME
```

Whether SAL can establish, preserve, reassess, and enforce permission specificity remains independently testable.

## Boundary

This order does not authorize runtime activation, autonomous expansion of permission, external execution, assumption of consent from silence or access, replacement of legitimate domain-specific consent standards, or any modification of the current SAL validation result.

**SAL-9 remains: HOLD — 3 PASS / 2 HOLD-PARTIAL / 0 FAIL.**

**Lane status:** ADVANCE — A18 consent/permission specificity governance defined with reader-first interpretation; implementation and runtime evidence remain independently testable.