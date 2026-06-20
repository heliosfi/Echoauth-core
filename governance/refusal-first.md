# Refusal-First Enforcement

EchoAuth uses refusal-first enforcement: execution is denied unless the system
can prove that execution is authorized, bounded, auditable, and inside all
governance invariants.

Refusal-first enforcement is not a failure of the system. It is the system's
primary safety posture.

## Default State

The default authorization state is not permit.

The default state is pending governance. A request becomes executable only after
authority, policy, invariants, identity, and runtime envelope checks succeed.

## Compliant Non-Execution States

EchoAuth recognizes several compliant non-execution states:

- `refused`: the request is not authorized.
- `hold`: execution is paused because required authority, channel, or context
  cannot be verified.
- `halted`: execution stopped because an invariant, integrity condition, or
  safety control failed.
- `revoked`: previously valid authorization was withdrawn or invalidated.
- `escalated`: the request requires review by a designated authority.

## Refusal Triggers

The system must refuse or block execution when:

- authority is missing,
- authority is out of scope,
- delegation is expired,
- identity cannot be verified,
- policy denies the action,
- invariants fail,
- payload integrity fails,
- replay is detected,
- audit path is unavailable,
- channel integrity is uncertain,
- or human authority is ambiguous.

## No Continuity Override

The system must not continue execution merely because:

- an action was previously authorized,
- a user likely intended it,
- the action appears beneficial,
- a delegate is familiar,
- a workflow is urgent,
- or continuity would be more convenient.

Continuity cannot override missing authority.

## Escalation

Escalation is allowed only when it preserves authority boundaries.

Escalation must identify:

- why the request could not proceed,
- which authority must review it,
- what evidence is required,
- and what state the request occupies while waiting.

## Developer Requirement

Implementations must model refusal as a first-class result, not as an exception
path. APIs should return structured refusal reasons suitable for audit,
debugging, regulatory review, and safety testing.

## Source Journal Files

- `docs/journal/2026-06-18_(1).html`
- `docs/journal/2026-02-09_(16).html`
- `docs/journal/2026-02-12_(1).html`
- `docs/journal/2026-02-19_(23).html`
