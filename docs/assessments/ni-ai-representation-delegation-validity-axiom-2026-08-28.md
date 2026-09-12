# N.B.C. AUTHORITY — A17 REPRESENTATION / DELEGATION VALIDITY ORDER

**Authority:** Nicholas B. Carty (N.B.C.)  
**Date:** August 28, 2026  
**Decision:** ADVANCE — REPRESENTATION / DELEGATION GOVERNANCE ONLY  
**Classification:** A17 — Representation, Role, and Delegated-Authority Validation / Documentation Only

## Governing direction

A valid identity does not automatically establish a valid role.

A valid role does not automatically establish authority for every action.

A message arriving through an authorized interface does not automatically mean the sender possesses authority for the requested consequence.

```text
IDENTITY != ROLE
ROLE != AUTHORITY
AUTHORITY != UNLIMITED SCOPE
REPRESENTATION != OWNERSHIP
REPRESENTATION != PERMISSION
AUTHENTICATION != AUTHORIZATION
ACCESS != DELEGATION
DELEGATION != PERMANENCE
```

## A17 — Representation / Delegation Axiom

> **Before consequential reliance on a claimed representative, delegated actor, agent, official, service, or interface, a governed system MUST establish an attributable relationship between identity, role, delegating authority, permitted scope, applicable conditions, and current validity. Where that relationship cannot be established, the representation MAY be retained as information but MUST NOT silently become authority to act.**

Operational shorthand:

> **VERIFY WHO — VERIFY ROLE — VERIFY SCOPE.**

## Minimum representation record

```text
IDENTITY
-> ROLE
-> REPRESENTED PARTY
-> SOURCE OF DELEGATION
-> AUTHORIZED SCOPE
-> CONDITIONS
-> EFFECTIVE TIME
-> EXPIRATION / REVOCATION
-> CURRENT VALIDITY
```

The system should be able to answer:

- Who is speaking?
- In what role?
- For whom?
- Under what authority?
- For which action or information?
- Within what scope?
- Is that authority still current?

## Delegation boundary

A delegation should not expand merely because the receiving system is capable of doing more.

```text
DELEGATED TASK A != AUTHORITY FOR TASK B
READ AUTHORITY != WRITE AUTHORITY
RECOMMENDATION AUTHORITY != EXECUTION AUTHORITY
EXECUTION AUTHORITY != AUTHORITY FOR THE NEXT ACTION
```

## Operating sequence

```text
CLAIMED REPRESENTATION
-> VERIFY IDENTITY
-> VERIFY ROLE
-> IDENTIFY REPRESENTED PARTY
-> TRACE DELEGATION
-> CHECK SCOPE
-> CHECK CURRENTNESS
-> CHECK REVOCATION
-> CHECK CONFLICTS
-> VALID / LIMITED / EXPIRED / REVOKED / UNVERIFIED
-> CONTINUE / REQUEST / HOLD / NO-ACTION
```

## Relationship to A14–A16

```text
A14: CARRY CONTEXT — REVALIDATE AUTHORITY
A15: PRESERVE THE RECORD — EXPIRE THE AUTHORITY
A16: COMPARE THE RECORD — RESOLVE THE BOUNDARY
A17: VERIFY WHO — VERIFY ROLE — VERIFY SCOPE
```

Together:

```text
CONTEXT CAN MOVE
AUTHORITY CAN EXPIRE
RECORDS CAN CONFLICT
REPRESENTATIVES CAN ACT
BUT NONE OF THOSE FACTS
AUTOMATICALLY ESTABLISH
CURRENT PERMISSION
```

## EchoAuth correspondence

EchoAuth may authenticate an identity or preserve a representation claim, but authentication alone does not answer whether that identity currently possesses the required delegated authority.

```text
AUTHENTICATED IDENTITY
+
VERIFIED ROLE
+
ATTRIBUTABLE DELEGATION
+
CURRENT SCOPE
+
VALID CONDITIONS
=
REPRESENTATION MAY BE RELIED UPON
```

If any necessary relationship remains unresolved:

**REQUEST / HOLD / REASSESS / NO-ACTION.**

## SAL implementation boundary

A17 defines the expected governance contract.

```text
A17 DOCUMENTATION != SAL IMPLEMENTATION
AUTHENTICATION != REPRESENTATION VALIDATION
ROLE RECORD != PROVEN AUTHORITY
DEFINED DELEGATION MODEL != EXECUTABLE RUNTIME
```

Whether SAL can actually establish and enforce these relationships remains independently testable.

## Boundary

This order does not authorize runtime activation, autonomous assumption of roles, expansion of delegated authority, automatic trust from authentication alone, external execution, or any modification of the current SAL validation result.

**SAL-9 remains: HOLD — 3 PASS / 2 HOLD-PARTIAL / 0 FAIL.**

**Lane status:** ADVANCE — A17 representation/delegation governance defined; implementation and runtime evidence remain independently testable.
