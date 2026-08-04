# Hawk Canonical Passage Record Contract

## Status

Owner-authoritative, documentation-only workflow contract.

## Authority

Owner-authoritative source and acceptance authority: **Nicholas B. Carty**.

## Purpose

Preserve one stable Hawk passage identity across forward dispatch, downstream handoff, return, consumption, closure, and any later separately authorized reopening.

This contract does not create permission, execution, completion, acceptance, publication, synchronization, runtime authority, or automatic continuation.

## Responsibility boundary

Hawk preserves dispatch readiness, handoff, workflow state, crossing posture, return, consumption, stop state, and next-transition release.

Hawk carries exact identities and authoritative references without creating meaning, evidence acceptance, authority, permission, execution, downstream completion, or owner acceptance.

CEG remains the bounded execution-crossing and sequencing mechanism. EchoAuth remains permission enforcement. Adumetric forms and reassesses. Saloherm preserves separately entrusted completion and reporting. Named acceptance authority performs acceptance.

## Required passage fields

Every passage record must contain:

- `passage_id`;
- origin repository, branch, checkpoint, artifact, and originating responsibility;
- originating package identity;
- destination responsibility, repository habitat, and entry point;
- current Hawk state;
- return identity and return destination;
- exact bounded responsibility;
- permitted and prohibited scope;
- controlling authority identity and lifecycle;
- prerequisites;
- admissible and excluded evidence;
- unresolved conditions;
- stop conditions;
- required return structure;
- passage-specific closed result vocabulary.

## Handoff binding

Every handoff must bind unchanged:

- package identity;
- passage identity;
- origin;
- destination;
- authority;
- scope;
- evidence references;
- unresolved conditions;
- current state;
- return route.

## Referenced records

### EchoAuth reference

Preserve only the authoritative permission record reference, including subject, requested action or resource, policy and invariants, authority and evidence, verdict, applicability, currentness, expiry, limitations, refusal, deferral, revocation, and consumption status.

### CEG reference

Preserve token or crossing identity, authorization-result reference, action or resource match, payload hash, channel state, nonce or replay state, concurrency state, executor identity, audit path, and execution-cycle outcome.

Hawk must not reproduce or reinterpret CEG's verdict.

### Downstream record

Preserve destination identity and entry point, exact scope and prohibitions, completion state, returned artifacts, validation evidence, unresolved conditions, authority limits, result identity, and return destination.

### Return correspondence

Bind passage, package, handoff, destination, returned-result identity, evidence package, result vocabulary, completion state, route, authority-consumption state, and next-question posture.

## Lifecycle

```text
FORMED
-> DISPATCH_READY
-> HANDED_OFF
-> PERMISSION_CONFIRMED
-> CROSSING_CONFIRMED
-> DOWNSTREAM_COMPLETE
-> RETURNED
-> ACCEPTED_FOR_ASSESSMENT
-> CLOSED
```

Guarded non-forward states:

`BLOCKED`, `HOLD`, `DEFERRED`, `REFUSED`, `HALTED`, `REVOKED`.

Every transition must record triggering evidence, responsible authority, prior and resulting state, timestamp or checkpoint, prohibited movement, and required record update.

Missing, stale, duplicated, conflicting, or unverifiable identity must fail closed.

## Result vocabulary rule

Result vocabulary is passage-specific.

Hawk must preserve the vocabulary adopted by the originating package or downstream responsibility and must not impose one universal vocabulary across all passages.

`PASS`, `FAIL`, `BLOCKED`, `ADVANCE`, `FIX`, `WAIT`, `DISPATCHED`, `STOPPED`, or another closed set is valid only when the governing package explicitly adopts it.

## Authority and acceptance

Each passage must name evidence-acceptance and result-acceptance authority.

Hawk may preserve an acceptance reference but may not perform acceptance unless separately authorized.

Hawk releases a next transition only when the returned result reveals an exact next question and separate current authority, requirements, evidence, destination, and stop conditions exist.

## Closure and reopening

Closure consumes and exhausts passage authority.

Reopening requires new evidence and explicit authority and creates a new passage identity linked to the closed predecessor.

## Asset classification

- Formed package: Adumetric-owned origin package; Hawk preserves immutable reference.
- Passage and handoff state: Hawk-owned canonical passage record.
- Authority: governing-authority record reference.
- Evidence: natural evidence-owner reference.
- Permission: EchoAuth authorization reference.
- Execution crossing: CEG crossing record reference.
- Completion or result: downstream result package.
- Acceptance: named acceptance record.

## Prohibitions

Do not:

- collapse Hawk into CEG;
- allow sequencing to create permission;
- allow dispatch to create execution authority;
- allow completion to create acceptance or continuation;
- rewrite a native downstream result;
- reuse an exhausted passage identity;
- reopen without new evidence and explicit authority;
- move repository-owned meaning into EchoAuth or Hawk.

## Result

```text
Canonical Hawk passage identity: PRESERVED
Forward and return lifecycle: PRESERVED
Passage-specific vocabulary: PRESERVED
CEG boundary: PRESERVED
EchoAuth permission boundary: PRESERVED
Architecture change: NONE
```

STOP.
