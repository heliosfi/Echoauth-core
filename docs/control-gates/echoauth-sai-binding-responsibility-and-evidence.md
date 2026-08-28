# EchoAuth SAI Binding Responsibility and Evidence

## Status

`INERT CONTRACT IMPLEMENTATION — NO AUTHORIZATION OR RUNTIME ACTIVATION`

Authority: Nicholas B. Carty (N.B.C.), 2026-08-28.

Implementation base: `heliosfi/Echoauth-core` at
`265cfa1617e6daebc9a9212fb0921991c9745750`.

Upstream contract: `heliosfi/heliosfi-ni-ai-spine` at
`f050dc82f20a0866e477cba0e4e74806454f8940`.

This implementation establishes an inert evidence-correspondence surface. It
does not establish an operational MCG, MPC, SAI runtime, permission result,
execution-eligibility result, executor, dispatch path, or external effect.

## Responsibility placement

| Responsibility | Owns | Explicitly does not own |
| --- | --- | --- |
| NI-AI envelope issuer | Upstream transition meaning, state, lineage, governance, validity, and evidence | EchoAuth request meaning, permission, or execution |
| EchoAuth request former | Requester, subject, action, resource, payload, context, credentials, policy, and idempotency | Upstream state meaning or Hawk validation |
| Hawk | Deterministic envelope-validation evidence | Permission, acceptance, dispatch, execution, or continuation |
| SAI binding record former | Exact correspondence formation and hashes | Any source value, translation, authorization, mutation, or execution |
| SAI intake validator | Fail-closed correspondence validation | Authorization-gate invocation or runtime continuation |
| EchoAuth authorization gate | Independent identity, authority, delegation, and policy evaluation | Invocation under this lane |

The binder is implemented in `src/echoauth/sai/binding.py`. The intake
validator is implemented in `src/echoauth/sai/intake.py`. Their immutable
models are in `src/echoauth/sai/models.py`; the closed transport contract is
`schemas/echoauth-sai-binding-record.schema.json`.

## Exact crossing

```text
already formed NI-AI envelope
+ matching immutable Hawk result
+ already formed EchoAuth AuthorizationRequest
+ explicit currentness evidence
-> inert SAI binding record
-> inert intake validation
-> WAIT_FOR_SEPARATE_AUTHORIZATION
```

The record former never calls `AuthorizationGateService.authorize()`. The
intake validator never calls it either. Acceptance states only that exact
evidence is suitable for a later, independently authorized evaluation.

## Current-main Hawk posture reconciliation

Canonical code in `src/hawk/transition_envelope.py` and its tests emit:

```text
WAIT_FOR_SEPARATE_AUTHORITY
```

The later connection-contract document describes the caller posture as:

```text
WAIT_FOR_SEPARATE_PERMISSION_OR_CONTINUATION_AUTHORITY
```

These are not silently collapsed. The binder verifies the exact value emitted
by the implemented Hawk interface. The SAI intake then terminates at its own
exact downstream posture:

```text
WAIT_FOR_SEPARATE_AUTHORIZATION
```

No Hawk source or contract was modified in this lane.

## Field ownership

| Field family | Exact source | Binding rule |
| --- | --- | --- |
| Transition and upstream correlation | NI-AI envelope | Preserve exactly |
| Issuer and participants | NI-AI envelope | Preserve exact identity references |
| State namespace/version/value | Accepted source-vocabulary configuration plus envelope current state | Preserve without translation |
| Governing source and lineage | NI-AI transition subject | Preserve exactly |
| Scope | NI-AI authority binding `exactScope` | Preserve opaque reference |
| Limits | NI-AI governing conditions `permittedScope` | Preserve opaque restrictive reference |
| Validity and revocation | NI-AI validity and authority binding | Shortest validity and fail-closed currentness |
| Hawk evidence | Immutable Hawk result | Hash and preserve; never treat `PROCEED` as permission |
| Request/action/resource | `AuthorizationRequest` | Preserve exactly; never derive from state |
| Payload/context | `AuthorizationRequest` | Store canonical hashes only |
| Credentials and raw payload/context | `AuthorizationRequest` | Never copy into the SAI record |
| Formation/replay/audit evidence | Explicit binder inputs | Bind exact references; never infer first use |

For contract version `1.0.0`, the accepted configuration is locked to upstream
checkpoint `f050dc82f20a0866e477cba0e4e74806454f8940` and transition-envelope
schema blob `acfe2dc5c4bd722163b123545fbf41a09fa2509d`. The Hawk result must bind
that same schema blob while preserving its own historical schema checkpoint.

The upstream envelope has no field named `limits`. The binder does not invent
one. It preserves the upstream `governingConditions.permittedScope` opaque
reference as the restrictive limits reference. Native resolution and meaning
remain upstream.

## Fail-closed behavior

Formation raises only a stable `SaiReason` through `SaiBindingError`. Intake
returns an immutable `SaiIntakeResult`; exceptions become
`INTERNAL_VALIDATION_ERROR`, never acceptance.

Formation or intake refuses missing or unverifiable producers, mutable inputs,
unknown state vocabularies, attempted state translation, mismatched Hawk or
request identities, action/resource substitution, payload/context/hash
substitution, scope or limits absence, stale timing, revocation, supersession,
replay, missing evidence, and missing audit availability.

Intake also revalidates the forming-component identity and version, exact
currentness and replay references, Hawk schema binding, the full upstream
validity interval, the formation time, and the shorter SAI expiry. Recomputing a
record hash cannot bypass those independent correspondence checks.

Record integrity is checked before field-specific intake checks. A party that
alters a record without recomputing its canonical record hash receives an
integrity refusal rather than a more favorable field-specific result.

## Historical invariants reused

The following historical branches supplied adversarial test ideas only:

- `test/sal-13-implied-authority-transfer`;
- `test/sal-15-execution-after-return`;
- `feat/sal-24-validation-only-authorization-execution-handoff`.

No branch was merged, rebased, cherry-picked, revived, or represented as
current implementation. Reused invariants are:

- proposal cannot become permission;
- authorization cannot become execution;
- execution eligibility cannot become completed execution;
- result or return evidence cannot authorize continuation;
- fail-closed evidence outranks readiness, adjacency, or prior success.

## Preserved exclusions

This surface contains no authorization-gate call, token issuance, execution
eligibility invocation, runtime mutation, dispatch, executor, credentials,
broker or account access, paper trading, live trading, or external-system
interaction. Test fixtures prove contract behavior only and are not runtime
producers or permission evidence.

## Review posture

Successful tests support review of this inert boundary only. Review or merge
would not activate it, connect it to authorization, or authorize a later lane.
