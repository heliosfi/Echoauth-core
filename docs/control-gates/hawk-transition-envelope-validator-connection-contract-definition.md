# Hawk Transition-Envelope Validator Connection Contract Definition

## Status and anchors

This document defines one documentation-only caller-to-validator boundary. It does not instantiate, register, authorize, or implement a caller, adapter, runtime connection, permission gate, dispatcher, executor, acceptance mechanism, or continuation mechanism.

The definition is anchored to:

- EchoAuth canonical checkpoint `d1154d3d45a79b1d4e60b75d878804554f691cbb`;
- the accepted Hawk validator contract at `docs/control-gates/hawk-ni-ai-transition-envelope-validator-contract-definition.md`;
- the canonical validator at `src/hawk/transition_envelope.py`;
- NI AI Spine checkpoint `6fe29594b4b5c7e4ceea1907c87cc7049e9a0e80`;
- canonical schema blob `acfe2dc5c4bd722163b123545fbf41a09fa2509d`.

No coded connection is authorized. A future source adapter may be proposed only if separately accepted evidence proves that direct assembly of the two immutable validator inputs is insufficient.

## One connection boundary

The sole defined caller role is `Hawk Passage Validation Caller`.

The role describes a possible future responsibility. The role does not identify an existing EchoAuth runtime, create an identity, grant authority, register a component, authorize invocation, or select an implementation habitat. No current EchoAuth, CEG, Adumetric, Saloherm, permission, queue, transport, or runtime component inherits this role by capability, readiness, adjacency, prior success, accepted evidence, or repository location.

The boundary, if separately authorized later, would perform exactly one synchronous call:

```text
validate_transition_envelope(envelope, validation_context) -> TransitionEnvelopeValidationResult
```

It would supply one already formed immutable `NI AI Transition Envelope`, one complete immutable ten-field validation context, and receive one newly created immutable twenty-field result. It would not alter any input or interpret, rewrite, persist, publish, dispatch, execute, accept, or continue the result.

## Caller authority evidence

Before any invocation, an external authority-verification responsibility must verify one closed eleven-field `CallerAuthorityEvidence` family:

1. `authoritySubject` — the exact one-envelope validation passage;
2. `authorizedActor` — the stable identity proposed to act as the `Hawk Passage Validation Caller`;
3. `currentAuthoritativeState` — the caller's current state at evaluation;
4. `issuer` — Nicholas B. Carty or a separately founder-accepted delegated issuer;
5. `audience` — the exact validator connection boundary;
6. `exactScope` — one envelope, one context, one invocation, and one unchanged result return;
7. `governingSource` — the accepted caller-authority record;
8. `permittedTransition` — exactly `INVOKE_HAWK_TRANSITION_ENVELOPE_VALIDATOR_ONCE`;
9. `validityInterval` — explicit trusted UTC `notBefore` and `notAfter` boundaries;
10. `revocationStateOrReference` — an externally verifiable current revocation state or reference;
11. `independentlyVerifiableEvidenceReference` — an attributable, integrity-bound evidence reference.

All eleven fields are required, attributable, current, scoped, audience-bound, independently verifiable, and fail-closed. Missing, malformed, stale, expired, revoked, contradictory, insufficient, unsupported, or unverifiable caller evidence prohibits invocation. The validator does not verify this caller authority and the connection boundary does not create or repair it.

## Envelope input

The sole envelope input is an already formed, deeply immutable `NI AI Transition Envelope`. Its authoritative source is the native formation responsibility represented by its issuer, submitting actor, transition subject, governing source, and lineage evidence. Adumetric formation remains separate where applicable.

The caller may receive and preserve the envelope but may not:

- form or complete it;
- infer missing values;
- repair schema or meaning;
- change identity, correlation, lineage, authority, evidence, disposition, consequence, lifecycle, or return data;
- treat receipt, schema validity, or readiness as authority.

If source identity, immutability, completeness, lineage, or governing meaning cannot be verified, no invocation occurs.

## Exact ten-field validation-context mapping

The validation context is assembled outside Hawk. It contains exactly the following fields and sources:

| Field | Exact value or authoritative source |
| --- | --- |
| `schema_document` | Complete deeply immutable schema document retrieved externally from the NI AI Spine and verified before delivery. |
| `schema_repository` | Exact constant `heliosfi/heliosfi-ni-ai-spine`. |
| `schema_path` | Exact constant `schemas/ni-ai-transition-envelope.schema.json`. |
| `schema_checkpoint` | Exact constant `6fe29594b4b5c7e4ceea1907c87cc7049e9a0e80`. |
| `schema_blob` | Exact constant `acfe2dc5c4bd722163b123545fbf41a09fa2509d`. |
| `trusted_evaluation_time_utc` | One externally supplied, trusted, extended UTC timestamp from the caller-authority-approved time source. |
| `validation_id` | One non-empty opaque identifier issued by the authorized passage responsibility and preserved exactly. |
| `passage_consumption_reference` | One non-empty opaque reference issued by the external passage-consumption authority and preserved exactly. |
| `passage_exhaustion_reference` | One non-empty opaque reference issued by the external passage-exhaustion authority and preserved exactly. |
| `resolved_facts` | One deeply immutable mapping containing exactly the twenty-one externally resolved facts below. |

No field may be defaulted, inferred, fetched, refreshed, repaired, or derived by Hawk. Unknown or additional context fields are prohibited.

## Schema acquisition and integrity boundary

The future authorized caller, or a separately authorized schema-acquisition responsibility acting before it, must retrieve the schema outside Hawk. That responsibility must verify repository, path, checkpoint, blob identity, document integrity, and Draft 2020-12 identity before producing the immutable context.

Hawk receives the schema document and identities as data. Hawk receives no filesystem, repository, network, environment, credential, cache, package-registry, or external-service access. Retrieval success does not create caller authority or permission to act.

## Exact twenty-one resolved facts

Each fact is externally resolved to exactly `CONFIRMED`, `REFUTED`, `UNAVAILABLE`, `STALE`, `CONTRADICTORY`, or `UNVERIFIABLE`. The source must be native to the responsibility named below and must provide an attributable evidence reference. Hawk may validate the supplied state but may not discover, infer, refresh, reconcile, or repair it.

| Fact | Native authoritative evidence owner and source requirement |
| --- | --- |
| `schema_integrity` | The external schema-acquisition and integrity-verification responsibility, bound to the exact Spine checkpoint and blob. |
| `issuer_identity` | The issuer's native identity authority and current identity evidence. |
| `receiver_identity` | The intended receiver's native identity authority and current identity evidence. |
| `lineage_verifiability` | The transition subject's native lineage owner and current checkpoint evidence. |
| `authority_currentness` | The authority issuer and governing source identified by the envelope authority binding. |
| `authority_attribution` | The native authority issuer's attributable evidence for subject, actor, issuer, and audience. |
| `authority_scope` | The governing authority source for exact scope and permitted transition. |
| `authority_revocation` | The native revocation authority or the source identified by `revocationStateOrReference`. |
| `authority_consistency` | The governing authority source comparing all eleven authority-binding fields without creating authority. |
| `authority_evidence_verifiability` | The issuer of `independentlyVerifiableEvidenceReference` and its integrity-verification responsibility. |
| `governing_source_verifiability` | The native owner of the governing source referenced by both transition subject and authority binding. |
| `semantic_correspondence` | The source-meaning authority and correspondence evidence identified by the envelope. |
| `policy_reference_verifiability` | Each native policy issuer for the required policy references. |
| `evidence_reference_verifiability` | Each evidence issuer and integrity source for required evidence references. |
| `trusted_time_verifiability` | The caller-authority-approved time source used for the supplied evaluation time and validity comparison. |
| `consequence_reference_verifiability` | The domain-native consequence authority identified by the envelope. |
| `confidentiality_verifiability` | The native disclosure, audience, and redaction policy authority. |
| `integrity_proof_verifiability` | The native integrity-proof mechanism and proof issuer. |
| `idempotency_replay_retry_ordering` | The external passage and ordering authority governing the supplied idempotency and ordering evidence. |
| `lifecycle_separation` | The native owners of the ten separately evidenced lifecycle records. |
| `return_path_verifiability` | The external passage-return authority governing result destination, source preservation, and continuation posture. |

A fact without its native evidence source is not `CONFIRMED`. EchoAuth permission enforcement may later evaluate its own authority and policy evidence, but it does not become the source of unrelated Hawk resolved facts.

## Passage references

The passage-consumption and passage-exhaustion references are issued, owned, consumed, exhausted, advanced, and audited only by an external canonical passage responsibility. The caller supplies both non-empty opaque references. Hawk preserves them exactly in the result and does not interpret or update passage state.

Presence of either reference does not prove authority, consumption, exhaustion, permission, execution, acceptance, or continuation. Missing, contradictory, reused outside its authorized idempotency boundary, or unverifiable passage references prohibit invocation.

## Result and evidence-return boundary

The sole result is the existing immutable `TransitionEnvelopeValidationResult` with exactly twenty fields:

1. `validation_id`;
2. `contract_name`;
3. `contract_version`;
4. `transition_id`;
5. `correlation_id`;
6. `schema_checkpoint`;
7. `schema_blob`;
8. `passage_consumption_reference`;
9. `passage_exhaustion_reference`;
10. `evaluated_at_utc`;
11. `validation_state`;
12. `disposition`;
13. `reason_codes`;
14. `evaluated_checks`;
15. `evidence_references`;
16. `unresolved_conditions`;
17. `authority_exercised`;
18. `authority_excluded`;
19. `source_provenance`;
20. `continuation_posture`.

The exact result recipient is the separately authorized invoking `Hawk Passage Validation Caller`. The call returns the result directly and synchronously. The connection boundary does not log, persist, publish, mutate, interpret, or forward it. Presentation to a passage record, permission gate, founder acceptance boundary, or other recipient requires separate authority outside this contract.

## Deterministic disposition handling

The caller must preserve the returned result unchanged and apply exactly one connection posture:

| Hawk disposition | Required caller posture |
| --- | --- |
| `PROCEED` | Return the result and stop at `WAIT_FOR_SEPARATE_PERMISSION_OR_CONTINUATION_AUTHORITY`. It is validation conformance only. |
| `RETURN` | Return the result to the separately authorized source-correction boundary and stop. No automatic retry or repair. |
| `WAIT` | Return the result, preserve all evidence, and stop until the identified condition changes under separate authority. |
| `STOP` | Return the result and terminate the invocation attempt. No retry, dispatch, execution, or continuation. |
| `ESCALATE` | Return the result to the separately authorized founder or authority-resolution boundary and stop. |

`PROCEED` never means permission, dispatch, execution, acceptance, publication, synchronization, continuation, completion, or success. No disposition authorizes another invocation or lane.

## Responsibility separation

- The NI AI Spine remains the governing contract and schema authority.
- The source or Adumetric responsibility forms the envelope where applicable.
- Hawk validates one supplied envelope and context only.
- EchoAuth remains the separate downstream permission-enforcement responsibility.
- CEG remains the separate execution-crossing and sequencing responsibility.
- Saloherm remains the separate completion responsibility.
- Nicholas B. Carty remains founder acceptance authority.
- Passage ownership, result recording, and lifecycle advancement remain external.

No responsibility is inherited across these boundaries.

## Invocation mode

Only direct synchronous invocation is defined. The envelope's `SYNCHRONOUS` or `ASYNCHRONOUS` timing mode describes the governed transition represented by the envelope; it does not select or authorize the validator invocation mechanism.

No queue, callback, worker, event bus, transport, asynchronous adapter, retry loop, scheduler, or background process is defined. Any future asynchronous delivery mechanism requires a separate assessment, contract, authority, implementation, verification, and acceptance lane.

## Closed connection errors and stop conditions

The pre-invocation connection error vocabulary is exactly:

1. `CALLER_AUTHORITY_MISSING`;
2. `CALLER_AUTHORITY_INVALID`;
3. `CALLER_AUTHORITY_STALE`;
4. `CALLER_AUTHORITY_REVOKED`;
5. `CALLER_AUTHORITY_CONTRADICTORY`;
6. `CALLER_AUTHORITY_UNVERIFIABLE`;
7. `ENVELOPE_SOURCE_UNVERIFIABLE`;
8. `CONTEXT_SOURCE_INCOMPLETE`;
9. `SCHEMA_BINDING_UNVERIFIABLE`;
10. `RESOLVED_FACT_SOURCE_UNVERIFIABLE`;
11. `PASSAGE_REFERENCE_UNVERIFIABLE`;
12. `RESULT_RECIPIENT_UNVERIFIABLE`.

Errors 1, 2, 4, and 7 produce `STOP`. Errors 3, 6, 8, 9, 10, 11, and 12 produce `WAIT`. Error 5 produces `ESCALATE`. These are connection postures only and are not Hawk dispositions. A pre-invocation error means the validator is not called and no validator result is fabricated.

Invocation also stops before the call when inputs are mutable, caller scope covers more than one envelope or invocation, the result recipient is not exact, evidence disclosure exceeds the authorized audience, a hidden dependency is required, or any responsibility boundary would be crossed.

## Future implementation test contract

Any future coded connection requires separate authorization and must prove, at minimum:

### Positive tests

- one exact authorized caller, immutable envelope, complete context, verified schema, twenty-one sourced facts, and two passage references produce exactly one synchronous validator call;
- the exact immutable result is returned unchanged to the exact caller;
- equal inputs produce equal connection behavior without sharing mutable state.

### Negative and boundary tests

- every closed connection error prevents invocation and produces its exact posture;
- missing, stale, revoked, contradictory, insufficient, or unverifiable caller evidence prevents invocation;
- missing or unknown context fields, wrong schema identities, mutable inputs, unverifiable facts, or invalid passage references prevent invocation;
- an unknown disposition, error, field, caller, recipient, resolver, or dependency fails closed.

### Collision tests

- caller-authority contradiction outranks stale or incomplete lower conditions;
- revocation and invalid authority outrank readiness, schema validity, or prior success;
- schema-binding failure, unresolved facts, and passage-reference failure cannot be weakened by a valid envelope;
- `STOP` and `ESCALATE` cannot be weakened by later evidence.

### Preservation tests

- caller, envelope, context, schema, facts, passage references, and result are never mutated or retained;
- correlation, lineage, semantic meaning, authority evidence, confidentiality, integrity, idempotency, and evidence ordering are preserved exactly;
- no logging, persistence, filesystem, repository, network, clock, randomness, credentials, processes, queues, transports, dispatch, execution, permission enforcement, acceptance, or continuation capability exists;
- synchronous invocation remains the sole call form;
- Hawk, EchoAuth, CEG, Adumetric, Saloherm, Spine, passage, and founder responsibilities remain separate.

## Current stop state

The `Hawk Passage Validation Caller` is defined but not instantiated or authorized. Its implementation habitat remains unselected. No source adapter has been proven necessary. No coded connection, runtime wiring, integration, deployment, dispatch, execution, or continuation is authorized.

The state after this proposed contract is:

`HAWK CONNECTION CONTRACT PROPOSED — WAIT FOR INDEPENDENT CONTRACT VERIFICATION`
