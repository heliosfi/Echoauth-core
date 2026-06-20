# CEG Governance Specification

CEG, the Crossroad Execution Gate, is EchoAuth's structural execution sequencing
mechanism.

CEG enforces the rule that only authorized actions may execute, and that each
authorized action executes inside a bounded runtime envelope.

## Scope

CEG is responsible for:

- receiving authorization results,
- issuing or validating execution tokens,
- sequencing execution,
- enforcing single-action boundaries,
- preventing replay,
- validating payload integrity,
- handling channel loss,
- controlling concurrency,
- and emitting execution audit events.

CEG is not responsible for:

- resolving authority,
- interpreting meaning,
- deciding policy,
- granting delegation,
- or expanding permissions.

## Core Contract

CEG may execute only when all of the following are true:

1. A valid upstream authorization result exists.
2. The authorization result matches the requested action and resource.
3. A single execution token is available.
4. The payload hash matches the authorized payload.
5. The execution channel is valid.
6. No conflicting execution lock exists.
7. No invariant violation is detected.

If any condition fails, CEG must refuse, hold, or halt.

## Execution Token

An execution token is a single-use, exclusive permission to execute exactly one
authorized action.

Execution tokens must include:

- token identifier,
- request identifier,
- authorized action,
- authorized resource,
- authority verdict reference,
- payload hash,
- expiration,
- nonce,
- issuing component,
- and audit metadata.

## CEG States

- `idle`: no execution is in progress.
- `authorized`: a valid authorization result has been received.
- `token_issued`: a single execution token exists.
- `executing`: the authorized action is being performed.
- `completed`: execution completed inside the envelope.
- `refused`: execution was denied before token use.
- `hold`: execution is paused pending authority/channel/context resolution.
- `halted`: execution stopped due to conflict, integrity failure, or invariant
  violation.
- `revoked`: authorization or token was invalidated before completion.

## Required Failure Handling

- Replay or nonce reuse: halt.
- Authority substitution: refuse or halt.
- Payload drift: halt.
- Channel loss: hold.
- Concurrency lock conflict: hold or halt.
- Token duplication: halt and invalidate tokens.
- Expired authorization: refuse.
- Missing audit path: halt.

## Audit Requirements

CEG must record:

- authorization result consumed,
- token issuance,
- token use,
- payload hash,
- channel state,
- lock state,
- execution start,
- execution completion,
- refusal/hold/halt/revocation reason,
- and downstream executor identity.

## Source Journal Files

- `docs/journal/2026-02-05_(18).html`
- `docs/journal/2026-02-08_(7).html`
- `docs/journal/2026-02-09_(16).html`
- `docs/journal/2026-02-19_(23).html`
