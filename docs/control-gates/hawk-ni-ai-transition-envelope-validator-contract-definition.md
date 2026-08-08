# Hawk NI AI Transition-Envelope Validator Contract Definition

## Status

Owner-authorized contract definition. Documentation only. No implementation.

Owner-authoritative source and acceptance authority: **Nicholas B. Carty**.

## Authority and checkpoints

This contract definition is anchored to:

- `heliosfi/Echoauth-core` canonical checkpoint `d2307b3de7282de4da0eb5fdc34372f68876e6ef`;
- `heliosfi/heliosfi-ni-ai-spine` canonical checkpoint `6fe29594b4b5c7e4ceea1907c87cc7049e9a0e80`;
- `docs/assessments/ni-ai-spine-api-boundary-contract-assessment.md`;
- `schemas/ni-ai-transition-envelope.schema.json`;
- `docs/assessments/hawk-ni-ai-connection-correspondence-assessment.md`;
- `docs/acceptance-records/hawk-ni-ai-connection-correspondence-acceptance.md`;
- `docs/control-gates/hawk-three-agent-cross-repository-passage-contract.md`;
- `docs/control-gates/hawk-canonical-passage-record-contract.md`;
- `docs/assessments/ni-ai-responsibility-map.md`;
- `docs/assessments/ni-ai-workflow-assessment.md`;
- `docs/assessments/ni-ai-spine-integration-review.md`.

## Purpose

Define the smallest future coded surface through which Hawk may validate and carry one `NI AI Transition Envelope` without changing its meaning, creating permission, dispatching work, or absorbing another responsibility.

The validator is a pure contract-conformance and supplied-fact evaluation boundary. It is not a workflow engine, schema owner, authority resolver, policy engine, evidence resolver, permission service, execution crossing, completion agent, acceptance mechanism, or transport.

## Rightful habitat and proposed surface

```text
Repository: heliosfi/Echoauth-core
Package: src/hawk/
Module: src/hawk/transition_envelope.py
Public function:
  validate_transition_envelope(
      envelope,
      validation_context,
  ) -> TransitionEnvelopeValidationResult
```

The proposed package is top-level `src/hawk/`, not `src/echoauth/hawk/`. This preserves Hawk as the broader workflow-carriage responsibility while leaving EchoAuth permission enforcement separate. Repository placement preserves the demonstrated Hawk footprint; it does not make EchoAuth the owner of Hawk or transfer the Spine into EchoAuth.

No source file, package initializer, test, schema copy, dependency, or runtime wiring is authorized by this document.

## Purity and determinism

The future validator must:

- be deterministic for equal inputs;
- have no filesystem, repository, network, clock, environment, credential, process, logging, database, queue, transport, or external-service access;
- perform no dispatch, execution, mutation, persistence, publication, synchronization, acceptance, or continuation;
- treat both inputs as immutable and never mutate or retain caller-owned objects;
- return a new immutable result instance for every evaluation;
- preserve input identifiers and references exactly;
- use only the supplied envelope, supplied validation context, and implementation-embedded closed contract logic;
- fail closed when any material fact is absent, malformed, stale, contradictory, unsupported, or unverifiable.

Equality of repeated results is required. Object identity reuse is prohibited.

## Input 1 — transition envelope

`envelope` represents exactly one candidate `NI AI Transition Envelope`.

The accepted NI AI Spine schema remains the authoritative structural definition. Hawk may validate against the supplied canonical schema document, but it may not copy, rewrite, relax, extend, or become the source of that schema.

The validator must preserve without reinterpretation:

- contract name and version;
- transition and correlation identifiers;
- issuer and participant identities;
- creation and validity boundaries;
- subject, current authoritative state, lineage, governing source, and proposed destination;
- semantic correspondence and ambiguity state;
- authority binding;
- governing conditions and transition factors;
- consequence;
- idempotency, replay, retry, and ordering evidence;
- confidentiality and integrity evidence;
- separate lifecycle records;
- native result;
- returned learning and source provenance.

The input may be represented by an immutable mapping-compatible value. Mutable, cyclic, non-JSON, or unsupported values are invalid at the public boundary.

## Input 2 — validation context

`validation_context` is one immutable value with exactly these fields:

1. `schema_document` — the complete immutable Draft 2020-12 schema document supplied by the caller;
2. `schema_repository` — exactly `heliosfi/heliosfi-ni-ai-spine`;
3. `schema_path` — exactly `schemas/ni-ai-transition-envelope.schema.json`;
4. `schema_checkpoint` — exactly `6fe29594b4b5c7e4ceea1907c87cc7049e9a0e80` for contract version `1.0.0` unless a later separately accepted contract changes the binding;
5. `schema_blob` — immutable Git blob identity of the supplied schema document;
6. `trusted_evaluation_time_utc` — explicit UTC evaluation time supplied from outside the validator;
7. `validation_id` — an opaque immutable identifier supplied by the caller; the validator must not generate randomness;
8. `resolved_facts` — the complete closed fact set defined below.

Unknown context fields are rejected. Missing context fields fail closed. The validator must not obtain or refresh any context value itself.

## Schema-loading boundary

The caller owns retrieval and integrity verification of the canonical schema document.

The validator receives the schema document and its repository, path, checkpoint, and blob identities. It verifies their exact contract binding and validates the envelope against the supplied document. It does not:

- fetch a schema;
- read a repository or filesystem;
- select a newer checkpoint;
- follow a branch name;
- trust an unbound schema merely because it self-validates;
- infer authority from schema validity.

Schema identity or integrity mismatch returns `STOP` with the applicable closed reason code.

## Closed resolved-fact state

Every externally resolved fact uses exactly one value:

`CONFIRMED | REFUTED | UNAVAILABLE | STALE | CONTRADICTORY | UNVERIFIABLE`

The required closed fact set is:

1. `schema_integrity`;
2. `issuer_identity`;
3. `receiver_identity`;
4. `authority_currentness`;
5. `authority_attribution`;
6. `authority_scope`;
7. `authority_revocation`;
8. `authority_consistency`;
9. `authority_evidence_verifiability`;
10. `governing_source_verifiability`;
11. `semantic_correspondence`;
12. `policy_reference_verifiability`;
13. `evidence_reference_verifiability`;
14. `trusted_time_verifiability`;
15. `consequence_reference_verifiability`;
16. `confidentiality_verifiability`;
17. `integrity_proof_verifiability`;
18. `idempotency_replay_retry_ordering`;
19. `lifecycle_separation`;
20. `return_path_verifiability`.

All twenty facts are required. The fact values report externally established evidence only. They do not authorize action and do not replace the exact evidence references carried by the envelope.

`authority_revocation = CONFIRMED` means revocation is confirmed and therefore authority is unavailable. For all other facts, `CONFIRMED` means the named condition is satisfied.

## Closed validation states

The validation result uses exactly one state:

`CONFORMANT | NONCONFORMANT | INDETERMINATE`

- `CONFORMANT` means every required structural and supplied-fact check passed.
- `NONCONFORMANT` means a definite contract contradiction or invalid value exists.
- `INDETERMINATE` means a required material condition cannot currently be established.

Validation state is not authority, permission, acceptance, dispatch, execution, completion, or continuation.

## Closed workflow dispositions

The validator returns exactly one cross-domain disposition:

`PROCEED | RETURN | WAIT | STOP | ESCALATE`

- `PROCEED` means only that the envelope is conformant for possible separately governed movement.
- `RETURN` means the candidate envelope has a bounded correctable contract defect and must return to its source responsibility.
- `WAIT` means required current evidence or a material externally resolved fact is unavailable, stale, or unverifiable.
- `STOP` means the governing schema binding, identity, authority lifecycle, confidentiality, integrity, or public input boundary is invalid in a way that prohibits this crossing.
- `ESCALATE` means a material contradiction or unresolved semantic or authority conflict requires the named governing authority.

No disposition dispatches work or creates permission. Native downstream result vocabularies remain passage-specific and must not be replaced by these validator dispositions.

## Closed reason-code vocabulary

Every result contains one or more reason codes from this exact set:

1. `VALIDATION_PASSED`;
2. `PUBLIC_INPUT_INVALID`;
3. `VALIDATION_CONTEXT_INVALID`;
4. `SCHEMA_BINDING_INVALID`;
5. `SCHEMA_INTEGRITY_INVALID`;
6. `SCHEMA_DOCUMENT_INVALID`;
7. `ENVELOPE_SCHEMA_NONCONFORMANT`;
8. `CONTRACT_IDENTITY_INVALID`;
9. `PARTICIPANT_IDENTITY_INVALID`;
10. `LINEAGE_INVALID`;
11. `AUTHORITY_REVOKED`;
12. `AUTHORITY_INVALID`;
13. `AUTHORITY_STALE`;
14. `AUTHORITY_CONTRADICTORY`;
15. `AUTHORITY_UNVERIFIABLE`;
16. `GOVERNING_SOURCE_UNVERIFIABLE`;
17. `SEMANTIC_AMBIGUITY_DETECTED`;
18. `SEMANTIC_AMBIGUITY_UNRESOLVED`;
19. `POLICY_UNVERIFIABLE`;
20. `EVIDENCE_UNVERIFIABLE`;
21. `TIME_INVALID`;
22. `CONSEQUENCE_INVALID`;
23. `CONFIDENTIALITY_INVALID`;
24. `INTEGRITY_INVALID`;
25. `IDEMPOTENCY_ORDERING_INVALID`;
26. `LIFECYCLE_INVALID`;
27. `RETURN_PATH_INVALID`;
28. `MATERIAL_CONDITION_UNDEFINED`.

Unknown reason codes are prohibited. `VALIDATION_PASSED` must appear alone.

## Deterministic first-match precedence

The future validator evaluates in this exact order and stops disposition selection at the first matching step. It may continue collecting only subordinate evidence within that already selected step; it may not allow a later check to weaken the selected disposition.

1. **Public boundary:** unsupported, mutable, cyclic, non-JSON, or malformed public inputs → `NONCONFORMANT / STOP / PUBLIC_INPUT_INVALID`.
2. **Context completeness:** missing or unknown context fields, invalid trusted time, incomplete fact set, or invalid fact value → `NONCONFORMANT / STOP / VALIDATION_CONTEXT_INVALID`.
3. **Schema binding:** wrong repository, path, checkpoint, blob binding, schema identity, or contract-version binding → `NONCONFORMANT / STOP / SCHEMA_BINDING_INVALID`.
4. **Schema integrity/document:** refuted schema integrity or invalid Draft 2020-12 schema document → `NONCONFORMANT / STOP / SCHEMA_INTEGRITY_INVALID` or `SCHEMA_DOCUMENT_INVALID`.
5. **Envelope structure:** schema nonconformance or unknown field/value → `NONCONFORMANT / RETURN / ENVELOPE_SCHEMA_NONCONFORMANT`.
6. **Contract, participant, and lineage identity:** definite identity or lineage contradiction → `NONCONFORMANT / STOP` with the applicable identity or lineage reason.
7. **Revocation:** confirmed authority revocation → `NONCONFORMANT / STOP / AUTHORITY_REVOKED`.
8. **Authority contradiction:** contradictory authority state, attribution, scope, governing source, permitted transition, or evidence → `INDETERMINATE / ESCALATE / AUTHORITY_CONTRADICTORY`.
9. **Authority invalidity:** refuted authority currentness, attribution, scope, or evidence → `NONCONFORMANT / STOP / AUTHORITY_INVALID`.
10. **Authority unavailable:** stale authority → `INDETERMINATE / WAIT / AUTHORITY_STALE`; unavailable or unverifiable authority evidence → `INDETERMINATE / WAIT / AUTHORITY_UNVERIFIABLE`.
11. **Governing source:** unavailable, stale, or unverifiable governing source → `INDETERMINATE / WAIT / GOVERNING_SOURCE_UNVERIFIABLE`.
12. **Semantic correspondence:** `DETECTED` → `INDETERMINATE / ESCALATE / SEMANTIC_AMBIGUITY_DETECTED`; `UNRESOLVED` → `INDETERMINATE / ESCALATE / SEMANTIC_AMBIGUITY_UNRESOLVED`; any contradiction between the envelope and supplied semantic fact uses the same precedence.
13. **Policy and evidence:** unavailable, stale, or unverifiable required policy or evidence reference → `INDETERMINATE / WAIT` with `POLICY_UNVERIFIABLE` or `EVIDENCE_UNVERIFIABLE`; a definite invalid reference → `NONCONFORMANT / RETURN`.
14. **Time and consequence:** invalid validity interval, timeout disposition, trusted-time relationship, severity, or domain-native consequence reference → `NONCONFORMANT / RETURN` with `TIME_INVALID` or `CONSEQUENCE_INVALID`; unavailable external verification → `INDETERMINATE / WAIT`.
15. **Confidentiality and integrity:** refuted confidentiality or integrity requirement → `NONCONFORMANT / STOP` with the applicable reason; unavailable or unverifiable proof → `INDETERMINATE / WAIT`.
16. **Idempotency and ordering:** invalid duplicate, replay, retry, or ordering state → `NONCONFORMANT / RETURN / IDEMPOTENCY_ORDERING_INVALID`; unavailable verification → `INDETERMINATE / WAIT`.
17. **Lifecycle and return:** collapsed lifecycle states, inferred acceptance or continuation, invalid return evidence, or invalid source preservation → `NONCONFORMANT / RETURN` with `LIFECYCLE_INVALID` or `RETURN_PATH_INVALID`.
18. **Other material condition:** any remaining required material condition that is undefined, invalid, contradictory, stale, insufficient, or unverifiable → `INDETERMINATE / WAIT / MATERIAL_CONDITION_UNDEFINED`; it cannot produce `PROCEED`.
19. **Success:** every required check confirmed → `CONFORMANT / PROCEED / VALIDATION_PASSED`.

No readiness, capability, prior success, adjacency, clean state, accepted evidence, silence, or schema validity may skip a precedence step or create `PROCEED`.

## Exact validation responsibilities

### Structural schema conformance

Hawk validates the candidate envelope against the exact supplied and checkpoint-bound schema. This establishes structural conformance only.

### Governing-condition validation

Hawk evaluates the envelope's closed material-condition status, factor completeness, timing, consequence, idempotency, lifecycle, and return requirements against supplied facts. It does not resolve those external facts itself.

### Authority verification

Hawk verifies that all eleven authority-binding fields exist, structurally conform, match the supplied authority facts, remain current and unrevoked, and preserve exact scope and governing source. Hawk does not originate founder authority or perform EchoAuth permission enforcement.

### Semantic-correspondence validation

Hawk verifies the closed ambiguity state, governing meaning source, one-lane invariant, correspondence evidence, and supplied semantic fact. It does not invent, select, transform, or repair meaning.

### Workflow disposition

Hawk returns one closed disposition under the precedence above. The disposition describes validator posture only.

### Downstream permission enforcement

EchoAuth remains the separate authority, identity, policy, invariant, resource, payload, time, and runtime permission-enforcement responsibility. A Hawk `PROCEED` does not predetermine an EchoAuth verdict.

### Execution

CEG remains the authorized execution-crossing and sequencing mechanism where applicable. The validator cannot issue or claim a token, enter an execution cycle, call an executor, or perform work.

### Evidence return

Hawk returns one immutable validation result with exact source identities and evaluated evidence. It does not write a passage record, acceptance record, repository file, log, or external message.

### Founder acceptance

Nicholas B. Carty remains acceptance authority. Validation evidence may be presented for acceptance but cannot create it.

## Exact immutable result

`TransitionEnvelopeValidationResult` contains exactly:

1. `validation_id`;
2. `contract_name`;
3. `contract_version`;
4. `transition_id`;
5. `correlation_id`;
6. `schema_checkpoint`;
7. `schema_blob`;
8. `evaluated_at_utc`;
9. `validation_state`;
10. `disposition`;
11. `reason_codes`;
12. `evaluated_checks`;
13. `evidence_references`;
14. `unresolved_conditions`;
15. `authority_exercised`;
16. `authority_excluded`;
17. `source_provenance`;
18. `continuation_posture`.

The result is frozen and deeply immutable. `validation_id` is supplied through the validation context and preserved exactly. The validator must not generate randomness or derive a replacement identity.

The validator preserves all input identifiers exactly. `reason_codes`, checks, references, conditions, authority fields, and provenance use immutable tuples in deterministic order.

`continuation_posture` is always `WAIT_FOR_SEPARATE_AUTHORITY` or `STOP`. It is never automatic continuation.

## Evidence-return requirements

The result must make it possible to reconstruct:

- the exact envelope identity evaluated;
- the exact schema repository, path, checkpoint, and blob;
- the trusted supplied evaluation time;
- every precedence step evaluated before the selected disposition;
- the supplied fact state supporting every material check;
- every evidence and governing-source reference used;
- the exact reason for refusal, return, wait, stop, escalation, or conformance;
- unresolved conditions;
- authority exercised and explicitly excluded;
- preservation of source provenance;
- the non-automatic continuation posture.

Evidence return does not create a repository record, acceptance, dispatch, or another lane.

## Required implementation evidence

Any later implementation order must require direct tests for:

- exact public API and exact export set;
- frozen and deeply immutable input/context/result models;
- exact fields and rejection of unknown or missing fields;
- schema checkpoint and blob binding;
- all closed fact states, validation states, dispositions, and reason codes;
- every first-match precedence branch;
- every missing, invalid, stale, contradictory, unavailable, unsupported, and unverifiable material condition;
- `PROCEED` only on complete conformance;
- `VALIDATION_PASSED` only and alone on success;
- structural conformance without authority inference;
- semantic ambiguity and one-lane behavior;
- synchronous timeout and asynchronous completion-reference behavior;
- authority revocation, contradiction, invalidity, staleness, and unverifiability collisions;
- policy, evidence, consequence, confidentiality, integrity, idempotency, lifecycle, and return collisions;
- exact identifier and reference preservation;
- non-mutation of both inputs;
- equal but distinct repeated results;
- deterministic ordering of all tuple fields;
- no production imports or capabilities that expose clock, randomness, filesystem, network, repository, subprocess, environment, credentials, persistence, dispatch, execution, permission enforcement, or logging;
- full-suite non-regression.

Positive, negative, collision, immutability, determinism, repeated-evaluation, boundary, and prohibited-capability evidence are mandatory.

## Stop conditions

The validator stops after returning one immutable result.

It must not:

- dispatch or route work;
- mutate the envelope or context;
- write or update a Hawk passage record;
- create authority, permission, acceptance, publication, synchronization, closure, or continuation;
- invoke EchoAuth, CEG, Adumetric, Saloherm, an agent, or an external system;
- perform downstream completion;
- select a transport or consumer beyond this separately accepted Hawk validation responsibility;
- alter the Spine contract or schema;
- authorize another lane.

## Responsibility preservation

```text
Adumetric: forms meaning and the exact bounded responsibility
Hawk validator: validates and returns one workflow disposition
EchoAuth: separately enforces permission
CEG: separately protects an authorized execution crossing
Saloherm: separately completes, reports, and stops
N.B.C.: aligns owner intent and returned evidence
Nicholas B. Carty: performs founder acceptance
NI AI Spine: preserves the consumer-neutral governing contract and schema
```

Hawk does not own or replace the Spine. Repository placement does not collapse these responsibilities.

## Contract result

```text
Repository habitat: heliosfi/Echoauth-core
Future package: src/hawk/
Future module: src/hawk/transition_envelope.py
Public function: LOCKED
Inputs: 2 LOCKED
Validation-context fields: 8 LOCKED
Result: 1 IMMUTABLE RESULT LOCKED
Resolved fact states: 6 CLOSED VALUES
Required resolved facts: 20
Validation states: 3 CLOSED VALUES
Workflow dispositions: 5 CLOSED VALUES
Reason codes: 28 CLOSED VALUES
First-match precedence: 19 STEPS LOCKED
Pure and deterministic: REQUIRED
Fail closed: REQUIRED
Dispatch and execution: PROHIBITED
Permission enforcement: SEPARATE
Founder acceptance: SEPARATE
Implementation: NOT AUTHORIZED
```

## Current posture

`HAWK VALIDATOR CONTRACT PROPOSED -> WAIT FOR INDEPENDENT CONTRACT VERIFICATION`

STOP.
