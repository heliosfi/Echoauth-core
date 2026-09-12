# N.B.C. AUTHORITY — A16 CONFLICT / SUPERSESSION RESOLUTION ORDER

**Authority:** Nicholas B. Carty (N.B.C.)  
**Date:** August 28, 2026  
**Decision:** ADVANCE — CONFLICT / SUPERSESSION GOVERNANCE ONLY  
**Classification:** A16 — Conflicting Context / Supersession Resolution / Documentation Only

## Governing direction

A governed system may receive multiple records, instructions, checkpoints, permissions, interpretations, or evidence claims that do not agree.

Conflict must not be resolved merely by choosing whichever item is newest, loudest, easiest to execute, or most convenient.

```text
CONFLICT != FAILURE
NEWER != AUTOMATICALLY AUTHORITATIVE
OLDER != AUTOMATICALLY INVALID
MORE DATA != MORE AUTHORITY
REPETITION != PRECEDENCE
ACCESS != PERMISSION
CONVENIENCE != RESOLUTION
AMBIGUITY != EXECUTION AUTHORITY
```

The purpose of conflict handling is to determine which information remains applicable, which authority governs the present boundary, and whether sufficient evidence exists to continue safely.

## A16 — Conflict / Supersession Axiom

> **When two or more inherited records, authorities, permissions, checkpoints, evidence claims, or interpretations conflict, a governed system MUST resolve the conflict through attributable source, applicable authority, scope, freshness, explicit supersession, evidence quality, and current conditions before consequential continuation. If the conflict cannot be resolved at the current boundary, the system MUST preserve the competing records and fail closed rather than silently selecting one.**

Operational shorthand:

> **COMPARE THE RECORD — RESOLVE THE BOUNDARY — DO NOT GUESS.**

## Conflict classes

A conflict may involve:

- two different authorities;
- old and new checkpoints;
- revoked and apparently active permission;
- competing interpretations of the same evidence;
- different scopes applying to the same action;
- contradictory source records;
- stale context versus current state;
- policy versus requested action;
- historical PASS versus new contrary evidence;
- multiple systems claiming responsibility for the same boundary.

## Resolution factors

```text
SOURCE
-> ATTRIBUTION
-> APPLICABLE AUTHORITY
-> SCOPE
-> TIMESTAMP / FRESHNESS
-> EXPLICIT SUPERSESSION
-> REVOCATION STATUS
-> EVIDENCE QUALITY
-> CURRENT CONDITIONS
-> PERMISSION
-> RESOLUTION STATUS
```

No single factor automatically governs every conflict.

A newer record may supersede an older record only when the newer record actually has the authority and scope to do so.

## Resolution outcomes

```text
CURRENT
SUPERSEDED
REVOKED
OUT-OF-SCOPE
CONFLICTED
UNRESOLVED
REQUEST-CLARIFICATION
HOLD
NO-ACTION
```

The losing record does not need to disappear.

It may remain preserved as historical evidence with its prior context and disposition intact.

## Operating sequence

```text
RECEIVE COMPETING CONTEXT
-> PRESERVE BOTH RECORDS
-> ATTRIBUTE EACH SOURCE
-> IDENTIFY THE CONFLICT
-> CHECK AUTHORITY
-> CHECK SCOPE
-> CHECK FRESHNESS
-> CHECK REVOCATION
-> CHECK EXPLICIT SUPERSESSION
-> COMPARE SUPPORTING EVIDENCE
-> DETERMINE CURRENT APPLICABILITY
-> RESOLVE OR MARK UNRESOLVED
-> CONTINUE / REQUEST / HOLD / STOP
```

## No silent precedence

The system MUST NOT assume:

```text
LATEST WINS
HIGHEST VOLUME WINS
MOST RECENT USER WINS
MOST CAPABLE AGENT WINS
MOST CONVENIENT ACTION WINS
AUTOMATION WINS
SYSTEM MEMORY WINS
```

Precedence must come from the governing boundary, not from accidental ordering.

## Relationship to A14 and A15

```text
A14: CARRY CONTEXT — REVALIDATE AUTHORITY
A15: PRESERVE THE RECORD — EXPIRE THE AUTHORITY
A16: COMPARE THE RECORD — RESOLVE THE BOUNDARY
A14 = SAFE CONTINUITY
A15 = SAFE DISCONTINUITY
A16 = SAFE CONFLICT RESOLUTION
```

Together:

```text
CONTEXT MAY CONTINUE
CONTEXT MAY EXPIRE
CONTEXT MAY CONFLICT
AUTHORITY MUST REMAIN ATTRIBUTABLE
UNRESOLVED CONFLICT MUST NOT SILENTLY BECOME ACTION
```

## EchoAuth correspondence

EchoAuth may preserve simultaneous evidence records and their individual provenance, timestamps, permissions, dispositions, revocation states, and supersession relationships.

Where records conflict, EchoAuth should expose the conflict rather than erase it.

```text
RECORD A
+
RECORD B
-> CONFLICT DETECTED
-> AUTHORITY / SCOPE / FRESHNESS CHECK
-> RESOLVED OR UNRESOLVED
```

When the governing relationship cannot be established:

**HOLD / REQUEST / REASSESS / NO-ACTION.**

## SAL implementation boundary

A16 defines expected governance behavior.

```text
A16 DOCUMENTATION != SAL IMPLEMENTATION
CONFLICT RULE != EXECUTABLE RESOLVER
DEFINED PRECEDENCE MODEL != PROVEN RUNTIME
```

Whether SAL can detect, preserve, classify, and correctly resolve these conflicts remains an independent implementation and validation question.

## Boundary

This order does not authorize:

- runtime activation;
- autonomous conflict resolution outside established authority;
- silent deletion of competing records;
- arbitrary precedence;
- automatic supersession based only on time;
- unrestricted execution;
- any change to the existing SAL validation result.

**SAL-9 remains: HOLD — 3 PASS / 2 HOLD-PARTIAL / 0 FAIL.**

**Lane status:** ADVANCE — A16 conflict/supersession governance defined; implementation and runtime evidence remain independently testable.
