# Sprint 2Y Event Contract Gap Report

## Status

Sprint 2Y is a contract-reconciliation checkpoint. It adds no runtime behavior.
The verified entry baseline is 254 passing tests, zero failures, and unchanged
Sprint 2A-2P freeze artifacts.

**HOLD is compliant.** Event-bus runtime coding must not proceed until approved,
versioned contracts resolve the gaps in this report.

## Completed Validation Foundations

| Sprint | Foundation | Implemented boundary |
| --- | --- | --- |
| 2Q | Event acceptance | Validates event envelope structure and catalog membership; emits accepted or rejected evidence only. |
| 2R | Producer authorization | Requires explicit, hash-bound, event-type-scoped producer evidence. |
| 2S | Subscriber authorization | Requires explicit, hash-bound, event-type-scoped subscriber evidence without registering subscriptions. |
| 2T | Payload schema validation | Validates payloads against the schema selected by `event_type`, including deterministic local reference resolution. |
| 2U | Event ordering | Validates deterministic per-request ordering by `occurred_at`, then `event_id`; unscoped events receive no ordering guarantee. |
| 2V | Schema binding | Binds payload hashes to schema identifiers, schema hashes, and deterministic local dependency fingerprints. |
| 2W | Correlation and causation | Validates explicit correlation and causation evidence without inferring missing causal relationships. |
| 2X | Audit evidence packaging | Packages immutable, deterministic acceptance or rejection evidence without claiming audit append or persistence. |

These foundations are validation-only. They do not publish, route, deliver,
persist, replay, sign, authorize operations, orchestrate services, or execute
commands. `runtime.recovered` remains catalog-only.

## Blocking Contract Gaps

| Gap | Missing decision | Why implementation is blocked |
| --- | --- | --- |
| Payload confidentiality | Define sensitive-field classification, prohibited content, redaction responsibility, and reject-versus-redact outcomes by event type. | Runtime code cannot infer secrets or safely transform canonical payloads. |
| Schema versioning | Define the canonical event schema-version field, compatibility rules, version selection, retirement, and mismatch outcomes. | Schema `$id` and hashes provide evidence but do not define deployment compatibility or migration behavior. |
| Subscription model | Define subscription identifiers, versions, lifecycle states, event-type scope, precedence, and authorization binding. | Deterministic routing by event type and subscription version cannot be implemented from subscriber authorization evidence alone. |
| Delivery semantics | Define transport boundary, delivery guarantees, acknowledgement, retry limits, timeout behavior, and `published` transition authority. | Publishing and delivery outcomes would otherwise depend on invented broker behavior. |
| Dead-letter handling | Define eligibility, record shape, retry exhaustion, access controls, retention, and reprocessing rules. | The `dead_lettered` state exists without an operational contract. |
| Persistence and replay | Define which events are durable, retention, indexing, replay authorization, replay ordering, offsets, and duplicate handling. | Durable uniqueness and replay require transactional storage and concurrency guarantees. |
| Distributed authenticity | Identify high-integrity event types and define signature format, signed fields, trust roots, key rotation, revocation, and verification failures. | Canonical hashes do not establish cross-process authenticity. |
| Audit append integration | Define the mapping from Sprint 2X evidence to `AuditRecord`, audit writer identity, chain selection, event identifiers, and append-failure outcomes. | Evidence packaging cannot truthfully claim an immutable audit append. |
| Cross-batch causation | Define resolution scope, retention window, cross-request rules, conflict handling, and authoritative lookup source. | Sprint 2W must leave absent causal events unresolved and cannot infer causation. |

## Why Runtime Coding Is Unsafe

Implementing beyond Sprint 2X would require selecting behavior not fixed by the
repository contracts. Such code could expose sensitive payloads, claim delivery
without defined guarantees, route through unversioned subscriptions, accept
unauthenticated distributed evidence, rewrite unresolved causation as fact, or
claim durable audit and replay properties that do not exist. Each outcome would
weaken fail-closed and refusal-first governance.

## Deferred Runtime Behaviors

- Event publication, transport, routing, callbacks, and subscriber delivery.
- Delivery acknowledgements, retries, timeouts, and dead-letter processing.
- Event persistence, durable offsets, retention, replay, and reprocessing.
- Durable event-ID uniqueness and concurrency guarantees.
- Secret inference, payload redaction, or payload transformation.
- Event signing, verification, trust-store access, and key management.
- Cross-batch or cross-request causation inference.
- Audit append, chain-position claims, and audit persistence.
- Notification delivery, orchestration, authorization effects, state mutation,
  execution, token issuance, and runtime recovery emission.

## Required Versioned Contract Decisions

Before runtime work resumes, an approved contract revision must specify:

1. Event confidentiality classifications and deterministic handling outcomes.
2. Event schema-version identity, selection, compatibility, and retirement.
3. Versioned subscription records, lifecycle, authorization binding, and routing.
4. Transport-neutral delivery states, acknowledgements, retries, and failures.
5. Dead-letter record, access, retention, and reprocessing semantics.
6. Durable storage, uniqueness, ordering, replay, and concurrency boundaries.
7. High-integrity event classification and cryptographic verification contracts.
8. Event-audit evidence mapping, append authority, chain selection, and failure
   behavior.
9. Cross-batch causation resolution and conflict rules.

Future contracts must preserve the separation between validation, coordination,
governance, authorization, and execution. Until every behavior being implemented
has an approved deterministic contract, Sprint 2Y remains on HOLD.
