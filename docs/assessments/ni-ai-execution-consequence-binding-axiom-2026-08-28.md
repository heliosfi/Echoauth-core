# N.B.C. AUTHORITY — A19 EXECUTION / CONSEQUENCE BINDING ORDER

**Authority:** Nicholas B. Carty (N.B.C.)  
**Date:** August 28, 2026  
**Decision:** ADVANCE — EXECUTION / CONSEQUENCE GOVERNANCE ONLY  
**Classification:** A19 — Pre-Execution Binding, Consequence, and Post-Execution Reassessment / Documentation Only

## Governing direction

A governed system may have valid identity, role, authority, and permission and still not yet have sufficient basis to execute a consequential action.

Permission establishes a boundary within which action may be considered. It does not erase the need to verify that the exact proposed action, current conditions, expected consequence, and execution surface still correspond to that permission.

```text
PERMISSION != EXECUTION
INTENT != EXECUTION
PLAN != EXECUTION
CAPABILITY != EXECUTION AUTHORITY
READY != AUTHORIZED
AUTHORIZED ACTION A != ACTION B
LOW CONSEQUENCE != HIGH CONSEQUENCE
EXECUTION != AUTHORITY FOR THE NEXT ACTION
SUCCESS != REAUTHORIZATION
FAILURE != AUTOMATIC RETRY AUTHORITY
RETURN != REAUTHORIZATION
```

## A19 — Execution / Consequence Binding Axiom

> **Before consequential execution, a governed system MUST bind the proposed action to the currently valid authority, permission, scope, target, execution surface, material conditions, and anticipated consequence. Where that binding cannot be established, or where the proposed execution materially differs from what was authorized, the system MUST request clarification, hold, reassess, or take no action. Completion of one authorized action MUST NOT silently create authority for another action.**

Operational shorthand:

> **BIND BEFORE ACT — RETURN BEFORE CONTINUING.**

## Pre-execution record

Before consequential execution, the system should be able to establish:

```text
AUTHORIZED ACTOR / SYSTEM
-> CURRENT AUTHORITY
-> CURRENT PERMISSION
-> EXACT ACTION
-> EXACT TARGET
-> PURPOSE
-> SCOPE
-> EXECUTION SURFACE
-> MATERIAL CONDITIONS
-> EXPECTED CONSEQUENCE
-> REVERSIBILITY / RECOVERY POSTURE
-> CURRENT CHECKPOINT
-> EXECUTE OR HOLD
```

The necessary detail should be proportionate to the consequence.

A trivial reversible action need not receive the same treatment as an irreversible, externally consequential, financial, legal, safety-sensitive, identity-affecting, or persistent action.

## Consequence escalation boundary

A system MUST NOT silently use permission for a lower-consequence operation to justify a materially higher-consequence operation.

```text
READ != MODIFY
MODIFY != DELETE
DRAFT != SEND
PREVIEW != PUBLISH
SIMULATE != EXECUTE
TEST != PRODUCTION
RECOMMEND != COMMIT
LOCAL EFFECT != EXTERNAL EFFECT
REVERSIBLE != IRREVERSIBLE
```

When consequence increases, the governing boundary must be checked again.

## Final pre-execution check

```text
PROPOSED ACTION
-> VERIFY CURRENT CHECKPOINT
-> VERIFY ACTOR / SYSTEM
-> VERIFY AUTHORITY
-> VERIFY PERMISSION
-> VERIFY ACTION
-> VERIFY TARGET
-> VERIFY SCOPE
-> VERIFY CURRENT CONDITIONS
-> VERIFY EXECUTION SURFACE
-> ASSESS CONSEQUENCE
-> CHECK REVOCATION / CONFLICT
-> VALID / LIMITED / CHANGED / UNRESOLVED
-> EXECUTE / REQUEST / HOLD / NO-ACTION
```

## Execution does not create continuation authority

A completed action produces a result.

That result must return to the governance process before a new consequential action is taken.

```text
AUTHORIZED ACTION
-> EXECUTION
-> RESULT
-> RECORD
-> RETURN
-> REASSESS
-> NEW AUTHORITY / PERMISSION CHECK
-> NEXT ACTION OR STOP
```

Therefore:

```text
EXECUTION
!=
CONTINUING AUTHORITY
```

## Retry boundary

Failure, timeout, incomplete execution, or unexpected output does not automatically authorize repetition.

```text
FAILED ACTION != RETRY AUTHORITY
PARTIAL SUCCESS != EXPANDED AUTHORITY
TIMEOUT != PERMISSION TO BYPASS
ERROR != AUTHORITY TO CHANGE METHOD
```

A retry may be appropriate only where it remains within the established authority, permission, consequence, and retry policy.

## Relationship to A14–A18

```text
A14: CARRY CONTEXT — REVALIDATE AUTHORITY
A15: PRESERVE THE RECORD — EXPIRE THE AUTHORITY
A16: COMPARE THE RECORD — RESOLVE THE BOUNDARY
A17: VERIFY WHO — VERIFY ROLE — VERIFY SCOPE
A18: ASK WHAT — FOR WHAT — HOW FAR — UNTIL WHEN
A19: BIND BEFORE ACT — RETURN BEFORE CONTINUING
```

Together:

```text
CONTEXT
-> CURRENTNESS
-> CONFLICT
-> REPRESENTATION
-> PERMISSION
-> EXECUTION BINDING
-> ACTION OR NO-ACTION
-> RETURN
-> REASSESSMENT
```

## EchoAuth correspondence

EchoAuth may preserve the information necessary to establish whether a proposed action corresponds to current authorization, including:

- authority source;
- permission record;
- exact requested action;
- target;
- purpose and scope;
- execution surface;
- checkpoint;
- relevant state;
- consequence classification;
- revocation or conflict state;
- execution disposition;
- returned result.

The critical distinction remains:

```text
VALID PERMISSION
+
VALID EXECUTION BINDING
=
ACTION MAY PROCEED

VALID PERMISSION ALONE
!=
AUTOMATIC EXECUTION
```

When the execution binding is unresolved:

**REQUEST / HOLD / REASSESS / NO-ACTION.**

## SAL implementation boundary

A19 defines expected system-governance behavior.

```text
A19 DOCUMENTATION != SAL IMPLEMENTATION
DEFINED EXECUTION GATE != EXECUTABLE GATE
PERMISSION RECORD != EXECUTION PROOF
EXPECTED CONSEQUENCE != OBSERVED OUTCOME
RETURN PATH DEFINITION != PROVEN POST-EXECUTION CONSUMER
```

Whether SAL can perform pre-execution binding, enforce consequence boundaries, preserve execution evidence, and require post-execution reassessment remains independently testable.

## Boundary

This order does **not** authorize:

- runtime activation;
- external execution;
- automatic retries;
- autonomous expansion of an authorized action;
- bypass of current permission or authority checks;
- irreversible action merely because capability exists;
- treating successful execution as continuing authorization;
- any change to the current SAL validation result.

**SAL-9 remains: HOLD — 3 PASS / 2 HOLD-PARTIAL / 0 FAIL.**

**Lane status:** **ADVANCE — A19 execution/consequence binding governance defined; implementation and runtime evidence remain independently testable.**