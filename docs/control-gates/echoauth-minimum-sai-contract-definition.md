# EchoAuth Minimum SAI Contract Definition

## Status and authority

`DOCUMENTATION-ONLY — CONTRACT DEFINITION`

Repository: `heliosfi/Echoauth-core`

Repository checkpoint assessed:
`6ecf52283f64d095f233d968e15d34f0bc8ca476`

Authority: Nicholas B. Carty (N.B.C.), 2026-08-26.

This lane is limited to defining and validating one minimum State
Authorization Interface (SAI) contract. It creates no runtime code, schema,
test, API, wiring, state mutation, token, execution, deployment, or
external-system action.

## Purpose

Define the smallest evidence-bounded contract by which a future MCG / MPC
state-governance decision could be presented to EchoAuth for independent
permission evaluation without transferring reasoning, amplifying authority,
or treating state as permission or execution.

This document defines a future interface boundary. It does not establish that
the interface exists or works.

## Evidence basis

The definition is bounded by:

- `docs/assessments/ni-ai-future-capability-thesis-2026-08-25.md`;
- `docs/assessments/ni-ai-future-capability-thesis-2026-08-25-acceptance.md`;
- `docs/control-gates/echoauth-authority-mode-spine-review.md`;
- `docs/control-gates/echoauth-s-mode-transition-requirements-review.md`;
- `docs/control-gates/echoauth-s-module-mcg-integration-boundary-review.md`;
- `archive/journal/2025-12-12_Section_2.html`;
- `archive/journal/2025-12-12_Section_10_hand_off_pack.html`;
- `src/echoauth/runtime/state_models.py`;
- `src/echoauth/runtime/state_machine.py`;
- `src/echoauth/runtime/transition_assessment.py`;
- `src/echoauth/models.py`;
- `specs/runtime-state-machine.md`;
- `specs/authority-resolution.md`; and
- `specs/runtime-envelope.md`.

The historical record identifies SAI as one-way `MCG -> EchoAuth`, carrying
state and boundary parameters while excluding reasoning, interpretation, and
logic. Current code supplies validation-only runtime transition machinery and
separate authority, envelope, audit, and lifecycle contracts. No executable
SAI-equivalent or authorized cross-vocabulary mapping is present.

## Governing separation

```text
NI-AI / SCI supplies structured understanding
-> MCG / MPC determines a bounded state posture
-> SAI carries that state posture without commands or reasoning
-> EchoAuth independently evaluates permission
-> any later execution remains separately bounded and authorized
```

The following invariants are mandatory:

```text
UNDERSTANDING != AUTHORITY
STATE != INTENT
STATE POSTURE != PERMISSION
PERMISSION != EXECUTION
EXECUTION != AUTHORITY FOR THE NEXT ACTION
```

SAI is a carriage and validation boundary. It is not a reasoning component,
authority resolver, permission engine, state machine, execution sequencer, or
executor.

## Direction and parties

| Role | Minimum responsibility |
|---|---|
| Producer | A separately established MCG / MPC governance component emits one bounded state decision. |
| Interface | SAI preserves, validates, and conveys the decision without semantic expansion. |
| Consumer | EchoAuth independently evaluates identity, authority, delegation, policy, invariants, scope, and currentness before any permission result. |

No NI-AI output, S-module output, CEG signal, caller request, historical note,
or SAI payload may impersonate the MCG / MPC producer.

## Minimum input record

Any future SAI input must contain all of the following information. Field names
and serialization remain unresolved until a separately authorized schema lane.

| Information | Minimum requirement |
|---|---|
| Contract identity | Contract name and explicit version. |
| Decision identity | Globally unique SAI decision identifier and source MCG / MPC decision identifier. |
| Source identity | Identified producing component and its version; the source must be independently trusted rather than accepted from an unverified label. |
| Request binding | Request identifier, canonical request hash, and correlation identifier where the surrounding request contract uses one. The associated EchoAuth request, not SAI, owns requester and subject identity data. |
| Requested boundary | Exact action and resource; neither may be wildcarded, inferred, substituted, or broadened by SAI. |
| Payload binding | Canonical payload hash, or an explicit declaration that no payload exists. Raw executable payload is outside this contract. |
| State declaration | One state value plus its exact vocabulary namespace and version. |
| Scope | Machine-verifiable action, resource, context, channel, and delegation bounds applicable to the state declaration. |
| Limits | Quantitative, qualitative, frequency, duration, and other applicable ceilings. Absence must never mean unbounded. |
| Time | UTC `issued_at`, `effective_at`, and `expires_at` values with `issued_at <= effective_at < expires_at`. |
| Replay binding | A unique nonce or equivalent single-use reference plus an idempotency key. |
| Governance continuity | Source state-governance policy version, source-decision revocation or supersession status, and any prior-state reference required to interpret currentness. These are not EchoAuth identity or authority verdicts. |
| Evidence continuity | Canonical evidence hash and immutable evidence references sufficient for independent verification. Reasoning content is excluded. |
| Audit continuity | Source audit event or chain reference and intended EchoAuth audit sink reference. |

Every boundary field must be explicit. Missing, empty, unparsable, unknown,
unverifiable, expired, revoked, contradictory, or out-of-scope information is
fail-closed.

## Minimum output record

SAI may return only an interface-validation result. The minimum result carries:

| Information | Minimum requirement |
|---|---|
| Result identity | Unique result identifier bound to the SAI decision and request. |
| Acceptance flag | Boolean stating whether the record is valid for submission to independent EchoAuth permission evaluation. `true` is not permission. |
| Preserved state | The exact received state value, vocabulary namespace, and version; no translated state unless a separately approved mapping exists. |
| Preserved bounds | Exact accepted scope, limits, action, resource, payload hash, and expiration. |
| Reason | Stable machine-readable validation reason. It must describe interface validity, not issue a command. |
| Evidence binding | Canonical hash of the validated SAI record and source evidence hash. |
| Validation time | UTC validation timestamp. |
| Audit reference | Append-only audit event reference recording acceptance or refusal. |

An accepted output means only:

```text
SAI RECORD VALID FOR INDEPENDENT ECHOAUTH EVALUATION
```

It does not mean `AUTHORIZED`, `READY`, `ALLOW`, `EXECUTE`, token eligibility,
or execution eligibility.

## State-vocabulary reconciliation boundary

The repository contains multiple state vocabularies with different meanings:

| Vocabulary | Established meaning | Contract treatment |
|---|---|---|
| Historical `OBSERVE / CONFIRM / EXECUTE` | MCG state language carried historically through SAI. | Historical evidence only; no current runtime mapping is established. `EXECUTE` is not an EchoAuth permission or command. |
| `S0-S5` | Authority-state classifications governed by explicit transition requirements. | Must remain namespaced; no mapping to runtime state, permission, or execution may be inferred. |
| `echoauth.runtime-state.v1` | Ten-state, validation-only transition graph in `src/echoauth/runtime/state_models.py`. | May be validated only through its canonical graph; it is not an S-mode mapping and validation does not apply state. |
| `specs/runtime-state-machine.md` / `src/echoauth/models.py` | Separate eighteen-state request lifecycle vocabulary. | Must remain namespaced and distinct from `echoauth.runtime-state.v1` and S-modes. |

The minimum reconciliation rule is **preservation without translation**:

1. The producer declares exactly one vocabulary namespace, version, and value.
2. SAI verifies that all three are recognized as one exact tuple.
3. SAI returns the same tuple unchanged.
4. EchoAuth may consume it only if EchoAuth has a separately reviewed,
   explicitly authorized mapping for that exact source and target vocabulary.
5. If no such mapping exists, the result is refused or held with no movement.

Label similarity, ordering, historical sequence, numeric proximity, shared
words such as `authorized`, `execute`, `ready`, or `halted`, and favorable
interpretation are not mappings.

The exact mapping among these vocabularies remains unresolved. This document
does not choose one.

## Freshness and expiration

1. All time values must be timezone-aware UTC.
2. Validation must occur no earlier than `effective_at` and strictly before
   `expires_at`.
3. The source decision, source governance policy, evidence, and any prior-state
   reference must all be current at validation time. EchoAuth separately checks
   identity, authority, delegation, policy, and invariants.
4. The shortest applicable expiration governs.
5. Expiration before or during downstream evaluation invalidates the SAI
   result; it may not be silently renewed or continued.
6. Reassessment requires a new or explicitly revalidated source decision,
   new freshness checks, and a distinct audit event.

Clock source, clock-skew tolerance, and distributed currentness verification
are unresolved implementation questions.

## Replay and idempotence

1. A nonce is single-use for one source decision, request, action, resource,
   payload hash, scope, and time window.
2. Reprocessing an identical record may return the same bounded validation
   result; it must not extend time, scope, limits, authority, or state.
3. Reuse of a nonce with any changed field is a conflict and fails closed.
4. Reuse of an expired, revoked, superseded, or consumed decision fails closed.
5. Missing replay evidence or unavailable replay state cannot be treated as
   first use.

## Revocation, conflict, and supersession

Source-decision revocation is checked before SAI acceptance. EchoAuth
separately checks authority and delegation revocation before any later
permission decision. Either kind of revocation supersedes prior acceptance at
its respective boundary.

The result fails closed when:

- a source decision or source governance-policy reference is revoked, expired,
  superseded, or unverifiable;
- two current records disagree about source, state, scope, action, resource,
  payload hash, limits, time, evidence, or authority;
- evidence hashes, versions, identifiers, or audit lineage do not match;
- precedence is absent or ambiguous; or
- the producer and EchoAuth cannot establish the same canonical record.

SAI must not select a favorable record, merge conflicting scope, discard a
restrictive limit, or resolve an authority dispute. Conflict resolution returns
to governance through a separately authorized path.

## Prohibited transformations

SAI must never:

- carry or reconstruct reasoning, interpretation, recommendations, urgency,
  hidden logic, natural-language commands, or executable payloads;
- convert intent, confidence, capability, explanation, or an S-module output
  into state or authority;
- infer a state, namespace, source, scope, limit, identity, delegation,
  currentness, or authority field;
- map between vocabularies without a separately authorized exact mapping;
- translate `OBSERVE`, `CONFIRM`, `EXECUTE`, an S-mode, `AUTHORIZED`, or
  `READY` into permission or execution eligibility;
- broaden, normalize away, repair, fill, merge, default, or silently drop a
  restriction;
- replace EchoAuth identity, authority, delegation, policy, invariant,
  envelope, revocation, or audit checks;
- treat MCG / MPC state as an order to act;
- mutate or persist runtime state;
- create a runtime envelope, issue or claim an execution token, dispatch an
  action, call an external system, or manufacture authorization; or
- treat prior acceptance as authority for a later action.

## Fail-closed outcomes

| Condition | Required outcome |
|---|---|
| Complete, canonical, current, conflict-free record in a recognized namespace | `accepted = true` only for independent EchoAuth evaluation. |
| Missing, malformed, unknown, unverifiable, mismatched, expired, revoked, replayed, or conflicting information | `accepted = false`; no state movement or permission evaluation based on that record. |
| Required mapping absent or ambiguous | `accepted = false` or non-advancing hold; no translation and no movement. |
| Audit write or audit sink unavailable | `accepted = false` or non-advancing hold. |
| Currentness, revocation, replay, authority, or evidence check unavailable | `accepted = false` or non-advancing hold. |

Whether a future implementation distinguishes refusal from hold is unresolved.
Both outcomes prohibit progression. No error, timeout, exception, fallback, or
partial result may become acceptance.

## Verification criteria for a future implementation

A later implementation cannot claim conformance until independent evidence
demonstrates all of the following:

1. Exact required-field, canonicalization, namespace, and version validation.
2. Preservation of state and every boundary without semantic expansion.
3. Rejection of unknown or ambiguous vocabulary and every unapproved mapping.
4. Independent EchoAuth evaluation after SAI acceptance.
5. No path from SAI acceptance directly to permission, state application,
   envelope creation, token issuance, dispatch, or execution.
6. Freshness, earliest-expiration, revocation, supersession, conflict, replay,
   and idempotence behavior under deterministic clocks.
7. Fail-closed behavior for unavailable dependencies, malformed inputs,
   exceptions, timeouts, races, storage conflicts, and audit failures.
8. Tamper-evident binding of the associated request identity, action,
   resource, payload hash, state, scope, limits, time, policy, invariants,
   authority, evidence, and audit lineage.
9. Adversarial resistance to authority leakage, evidence substitution,
   confused-deputy behavior, namespace confusion, downgrade or upgrade by
   translation, scope widening, expiration extension, and replay.
10. Audit coverage for accepted, refused, held, conflicting, expired, revoked,
    replayed, superseded, and unverifiable records.
11. No regression of the existing validation-only runtime transition boundary.
12. Separate explicit authorization for any schema, code, tests, API, runtime,
    integration, deployment, or execution work.

These criteria are requirements, not evidence that they have been satisfied.

## Evidence-bounded determination

### Supported

- Historical SAI is a one-way `MCG -> EchoAuth` state-and-boundary interface.
- Historical SAI excludes reasoning, interpretation, and logic.
- Existing governance separates understanding, state, authority posture,
  permission, execution, and reassessment.
- Existing runtime transition assessment is fail-closed, audited,
  idempotent, validation-only, and non-mutating within its tested boundary.

### Unresolved connections

- The exact relationship among historical `OBSERVE / CONFIRM / EXECUTE`,
  `S0-S5`, `echoauth.runtime-state.v1`, and the eighteen-state request
  lifecycle.
- The canonical producer identity and trust-verification mechanism for a
  future MCG / MPC decision.
- Concrete field names, serialization, signatures or MACs, storage,
  transport, clock policy, reason-code vocabulary, and refuse-versus-hold
  behavior.
- Integrated and adversarial proof across SAI and EchoAuth.

### Not established

- A current executable SAI-equivalent.
- Any cross-vocabulary mapping.
- MCG / MPC runtime authority or S-mode runtime behavior.
- Permission, state mutation, envelope creation, token issuance, execution,
  deployment, production readiness, or external-system authority.

## Stop boundary

This definition stops at the minimum documentation contract and its
documentation validation. Completion, review, commit, merge, or acceptance of
this document does not authorize a schema, code, tests, API, runtime wiring,
state change, token, execution, deployment, external-system access, or a next
lane.

## Final status

`MINIMUM SAI CONTRACT — DEFINED FOR REVIEW`

`CURRENT EXECUTABLE SAI — NOT ESTABLISHED`

`CROSS-VOCABULARY MAPPING — UNRESOLVED`

`IMPLEMENTATION AUTHORITY — NOT CREATED`
