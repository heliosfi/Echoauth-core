# EchoAuth Runtime

The EchoAuth runtime implements the governance-first execution path described
by the architecture, governance, and specification documents.

Runtime code must enforce the repository's formal rules. It must not treat
documentation as advisory.

## Runtime Responsibilities

The runtime is responsible for:

- receiving proposed actions,
- binding requests to identity,
- resolving authority through governance services,
- validating delegation,
- applying policy,
- validating invariants,
- creating a runtime envelope,
- sequencing execution through CEG,
- refusing unsafe or unauthorized requests,
- and writing audit records.

## Required Runtime Components

### Authorization State Engine

Maintains request lifecycle states from proposal through governance, execution,
refusal, hold, halt, revocation, expiration, escalation, and completion.

### Authority Resolver

Validates parent, caregiver, institutional, delegated, and runtime authority
records.

### Policy Evaluator

Applies deterministic policies and returns structured permit/refuse/hold/halt
results.

### Invariant Validator

Checks non-negotiable governance invariants before execution.

### CEG Execution Governor

Validates execution token, payload hash, nonce, channel, lock, and envelope
state before allowing the executor to run.

### Audit Logger

Records proposal, governance, authorization, envelope, token, execution, and
failure events in an immutable or tamper-evident form.

## Runtime Non-Goals

The runtime must not:

- infer authority,
- expand delegate permissions,
- treat NI-AI interpretation as authorization,
- reuse execution tokens,
- execute outside the runtime envelope,
- bypass audit,
- or continue after hold, halt, refusal, revocation, or expiration.

## Implementation Readiness

Runtime implementations should expose typed interfaces for:

- authorization requests,
- authority verdicts,
- delegate grants,
- invariant results,
- policy decisions,
- runtime envelopes,
- execution tokens,
- CEG state transitions,
- audit events,
- and structured refusal reasons.

## Source Journal Files

- `docs/journal/2026-02-05_(18).html`
- `docs/journal/2026-02-08_(7).html`
- `docs/journal/2026-02-09_(16).html`
- `docs/journal/2026-02-12_(1).html`
- `docs/journal/2026-02-19_(23).html`
- `docs/journal/2026-06-18_(1).html`
