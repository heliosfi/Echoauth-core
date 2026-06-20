# EchoAuth Glossary

## Authority

The recognized source of permission for a request. Authority may be parent,
legal caregiver, institutional, delegated, or system-scoped, but it must be
explicit and auditable.

## Authorization

The EchoAuth decision that an action may or may not execute. Authorization is
bounded by authority, policy, invariants, runtime envelope, action, resource,
payload, and time.

## CEG

Crossroad Execution Gate. The execution sequencing layer that enforces
single-token, single-action, authorized execution after upstream governance
permits the request.

## Delegate

An actor or subsystem granted a bounded permission by a valid authority source.
A delegate may execute or assist inside scope but does not become the authority
source.

## Deterministic Authorization

The requirement that identical inputs, authority records, policy versions,
invariants, and runtime conditions produce identical authorization outcomes.

## EchoAuth

A deterministic authorization and execution-governance framework that ensures
governance precedes execution.

## Execution Token

A single-use permission artifact used by CEG to execute exactly one authorized
action inside a runtime envelope.

## Governance

The process of evaluating authority, policy, invariants, identity, and runtime
conditions before execution.

## Halt

A non-execution state caused by an invariant, integrity, replay, concurrency, or
safety failure. Halt requires audit and review before retry.

## Hold

A non-execution state used when authority, context, identity, channel, or
runtime evidence is unresolved but may become available.

## Identity

The verified relationship between an actor, role, authority record, context, and
permitted action.

## MCG

Melanin Cognitive Governance. The judgment and authority-resolution layer that
identifies the controlling authority source. MCG does not execute actions.

## NI-AI

Natural Intellect - Artificial Intelligence. In the EchoAuth architecture, NI-AI
may interpret meaning, context, intent, and coherence, but it does not authorize
execution.

## Parent-Anchored Authority

The governance model for child, school, clinical, and caregiver contexts in
which parent or legal caregiver authority anchors authorization unless a valid
legal authority supersedes it.

## Refusal

A compliant non-execution outcome. Refusal means the request is denied because
authorization requirements were not satisfied.

## Refusal-First

The enforcement posture that denies execution unless the system can prove the
request is authorized, bounded, auditable, and invariant-compliant.

## Runtime Envelope

The bounded execution context that defines exactly what may execute, under which
authority, with which payload, token, policy, invariant set, channel, and audit
path.

## S23

Envelope governance suite referenced in EchoAuth source material. S23 expresses
authorization and execution constraints as enforceable invariants, generated
tests, boot seals, and runtime tripwires.

## Source Journal Files

- `docs/journal/2026-06-18_(1).html`
- `docs/journal/2026-02-05_(11).html`
- `docs/journal/2026-02-05_(18).html`
- `docs/journal/2026-02-08_(7).html`
- `docs/journal/2026-02-09_(16).html`
- `docs/journal/2026-02-12_(1).html`
- `docs/journal/2026-02-19_(23).html`
