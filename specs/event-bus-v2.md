# Purpose

Define the draft version 2 EchoAuth event-bus contract boundary. This
specification governs event identity, payload classification, subscriptions,
delivery evidence, replay vocabulary, distributed integrity evidence, audit
mapping, and causation evidence without implementing operational behavior.

Contract version: `2.0.0-draft`

Approval state: `HOLD`

**HOLD remains compliant until this contract set is approved.**

# Scope

This specification applies to the versioned successor artifacts:

- `contracts/event-bus-v2.yaml`
- `schemas/event-bus-runtime-v2.schema.json`
- `events/event-envelope-v2.schema.json`
- `events/event-catalog-v2.yaml`
- `contracts/event-bus-v2-decision-log.md`

It does not replace or modify the version 1 event contract. It defines no
runtime publication, routing, delivery, persistence, replay, signing, audit
append, notification, orchestration, authorization, state mutation, execution,
token issuance, or Recovery behavior.

# Inputs

## Event Envelope

| Field | Type | Required | Rule |
| --- | --- | --- | --- |
| `envelope_version` | string | yes | Must equal `2.0`. |
| `event_id` | string | yes | Non-empty identifier; durable uniqueness remains unimplemented. |
| `event_type` | string | yes | Must select exactly one active or catalog-only catalog entry. |
| `producer_id` | string | yes | Must bind to explicit producer evidence. |
| `request_id` | string | no | Request scope; absence creates no request-ordering guarantee. |
| `correlation_id` | string | yes | Explicit correlation evidence; never inferred. |
| `causation_id` | string | no | Explicit causal event reference; absence means no causal evidence. |
| `event_schema_id` | URI | yes | Must equal the v2 envelope schema `$id`. |
| `event_schema_version` | string | yes | Must equal `2.0.0`. |
| `payload_schema_id` | URI | yes | Must match the selected catalog entry. |
| `payload_schema_version` | string | yes | Must match the selected catalog entry. |
| `confidentiality_class` | enum | yes | `public`, `internal`, `sensitive`, or `restricted`. |
| `integrity_class` | enum | yes | `standard` or `high`. |
| `payload` | object | yes | Canonical JSON object selected by `event_type`. |
| `payload_hash` | SHA-256 hex | yes | Canonical payload hash evidence. |
| `occurred_at` | UTC timestamp | yes | Source event time; must end in `Z`. |
| `signature_evidence` | object | conditional | Vocabulary only; required for `high` integrity after trust contracts are approved. |

## Subscription Record

| Field | Type | Required | Rule |
| --- | --- | --- | --- |
| `subscription_id` | string | yes | Stable subscription identifier. |
| `subscription_version` | positive integer | yes | Immutable version of the subscription record. |
| `subscriber_id` | string | yes | Must bind to explicit subscriber authorization evidence. |
| `event_types` | unique list | yes | Exact event-type scope; wildcards are prohibited. |
| `event_schema_versions` | unique list | yes | Exact accepted envelope versions. |
| `authorization_evidence_id` | string | yes | Reference to configured subscriber evidence. |
| `authorization_evidence_hash` | SHA-256 hex | yes | Hash binding for the referenced evidence. |
| `priority` | non-negative integer | yes | Lower numeric value sorts first. |
| `state` | enum | yes | Canonical subscription lifecycle state. |
| `effective_at` | UTC timestamp | yes | Earliest eligibility time. |
| `expires_at` | UTC timestamp | no | Must be later than `effective_at`. |

## Delivery, Dead-Letter, Replay, and Causation Evidence

Canonical shapes are defined in
`schemas/event-bus-runtime-v2.schema.json`. They are evidence contracts only
and grant no authority to perform the represented operation.

# Outputs

| Artifact | Canonical outcomes | Effect |
| --- | --- | --- |
| Event acceptance | `accepted`, `rejected`, `held` | Evidence only. |
| Delivery evidence | `accepted`, `publish_pending`, `published`, `retry_pending`, `dead_lettered`, `rejected`, `held` | Evidence only. |
| Subscription evidence | `proposed`, `active`, `suspended`, `revoked`, `expired`, `retired` | Configuration evidence only. |
| Replay eligibility | `eligible`, `rejected`, `held` | Does not replay an event. |
| Causation evidence | `absent`, `resolved`, `unresolved`, `conflict`, `invalid` | Does not infer or persist causation. |
| Audit mapping | `mapped`, `unmapped`, `held` | Does not append an audit record. |

# State Machine

## Event Delivery Vocabulary

| Current | Evidence event | Next |
| --- | --- | --- |
| `received` | `validation_passed` | `accepted` |
| `received` | `validation_failed` | `rejected` |
| `received` | `required_dependency_unavailable` | `held` |
| `accepted` | `publication_proposed` | `publish_pending` |
| `publish_pending` | `transport_acknowledged` | `published` |
| `publish_pending` | `retryable_failure` | `retry_pending` |
| `retry_pending` | `retry_due` | `publish_pending` |
| `publish_pending` | `non_retryable_failure` | `dead_lettered` |
| `retry_pending` | `retry_exhausted` | `dead_lettered` |

The transitions after `accepted` are vocabulary only. No transition authority,
transport, retry processor, or state mutation is approved by this draft.

## Subscription Lifecycle Vocabulary

| Current | Evidence event | Next |
| --- | --- | --- |
| `proposed` | `approved` | `active` |
| `proposed` | `rejected` | `revoked` |
| `active` | `suspend` | `suspended` |
| `active` | `revoke` | `revoked` |
| `active` | `expire` | `expired` |
| `suspended` | `resume` | `active` |
| `suspended` | `revoke` | `revoked` |
| `suspended` | `expire` | `expired` |
| `revoked` | `retire` | `retired` |
| `expired` | `retire` | `retired` |

Only `active` records within their effective interval are routing candidates.
This rule does not implement registration, discovery, routing, or delivery.

# Validation Rules

1. Every v2 event must carry explicit envelope and payload schema identity.
2. Catalog selection is by exact `event_type`; wildcard selection is prohibited.
3. Envelope confidentiality and integrity classes must equal the catalog entry.
4. Payload hashes use canonical JSON and SHA-256.
5. Payload schemas, including local dependencies, must resolve deterministically.
6. Producers must declare classification; validators must not infer sensitive
   fields from names or values.
7. Raw credentials, bearer secrets, private keys, and executable secret material
   are prohibited in every payload class.
8. `sensitive` and `restricted` payloads fail closed when classification evidence
   is missing or mismatched. Automatic redaction is prohibited by this draft.
9. Subscriber eligibility requires an `active`, unexpired, exact-version record
   and matching hash-bound authorization evidence.
10. Candidate subscription order is priority, subscription version descending,
    then subscription ID. This is a deterministic comparison rule only.
11. Delivery attempts are numbered from one and increase by one within a single
    delivery ID. Durable enforcement remains deferred.
12. Retry requires an explicit retry policy and a retryable failure code.
13. Dead-letter eligibility requires non-retryable failure or retry exhaustion.
14. Replay is prohibited unless the catalog says `authorized_only` and explicit
    replay authority evidence is supplied.
15. Replay eligibility is not permission to publish or deliver.
16. Offsets are opaque, stream-scoped evidence and cannot be compared across
    streams.
17. Missing `causation_id` is valid absent evidence.
18. Self-causation is invalid.
19. A referenced event in the supplied batch is resolved evidence.
20. A referenced event absent from a partial batch is unresolved, not failure.
21. Cross-request causation is prohibited in v2 unless a later approved contract
    explicitly replaces this rule.
22. Cross-batch resolution requires an approved durable causal lookup contract;
    until then it remains unresolved.
23. `runtime.recovered` remains `catalog_only` and cannot be accepted, produced,
    subscribed, published, replayed, or emitted.

# Failure Conditions

| Condition | Result |
| --- | --- |
| Missing or mismatched schema identity | `rejected` |
| Unknown, retired, or disabled event type | `rejected` |
| Missing producer or subscriber evidence | `rejected` |
| Confidentiality or integrity mismatch | `rejected` |
| Prohibited payload content identified by approved schema | `rejected` |
| Required trust, storage, audit, or transport dependency unavailable | `held` |
| Invalid subscription lifecycle or version | `rejected` |
| Retry policy missing for retry request | `held` |
| Replay authority missing or invalid | `rejected` |
| Offset from another stream | `rejected` |
| Self-causation or conflicting causal evidence | `rejected` |
| Causal event absent from a partial batch | `unresolved` evidence |
| `runtime.recovered` operation requested | `rejected` |

# Security Requirements

- Classification is explicit and catalog-bound; it is never inferred.
- Restricted data requires approved encrypted transport and storage profiles
  before operational use.
- High-integrity events require signature evidence after an algorithm registry,
  trust roots, key lifecycle, and verification-failure policy are approved.
- Signature evidence binds the envelope fields enumerated by the contract; it
  cannot authorize an operation or replace producer authorization.
- Replay authority is explicit, scoped, expiring, and hash-bound.
- Subscriber authorization is event-type and schema-version scoped.
- No event evidence can authorize, execute, mutate runtime state, issue tokens,
  or bypass refusal, hold, halt, or revocation.

# Audit Requirements

Acceptance and rejection evidence maps to `AuditRecord` as follows:

| Event evidence | AuditRecord field |
| --- | --- |
| `accepted` | `event_type = event.accepted` |
| `rejected` | `event_type = event.rejected` |
| event `producer_id`, when available | `actor_id` |
| bus component ID when producer is unavailable | `actor_id` |
| event `request_id` | `request_id` |
| acceptance reason | `reason` |
| event IDs, schema identities, classification, payload hash, correlation, causation, and source time | `details` |
| evidence decision time | `occurred_at` |

The mapping must preserve Sprint 2X evidence immutably. A mapping result does not
claim append, chain position, persistence, or audit availability. Audit writer
identity, chain selection, append authority, and append-failure behavior remain
approval blockers.

# Persistence Requirements

This draft defines vocabulary but no persistence adapter:

- Retention classes are `ephemeral`, `operational`, `audit`, and `legal_hold`.
- Replay policies are `prohibited` and `authorized_only`.
- Offsets are opaque strings bound to one stream ID and one event ID.
- Durable event uniqueness, attempt sequencing, subscription version uniqueness,
  transaction isolation, retention durations, deletion authority, legal holds,
  and replay concurrency require future approved deployment contracts.

# Deterministic Rules

- Canonical object serialization and hashing follow the existing common contract.
- Catalog entries sort by event type.
- Subscription candidates sort by priority ascending, subscription version
  descending, then subscription ID ascending.
- Scoped event ordering remains `occurred_at`, then `event_id`.
- Delivery attempts sort by attempt number, then decision timestamp, then
  delivery ID.
- Dead-letter evidence sorts by dead-letter time, then dead-letter ID.
- Replay evidence sorts by source offset only within the same stream; otherwise
  no ordering comparison is permitted.
- Equivalent payload, payload schema identity, and payload schema version produce
  the same payload hash and schema-binding evidence.
- No missing authority, classification, signature, audit, storage, transport, or
  causation evidence resolves positively by default.

# Examples

```json
{
  "envelope_version": "2.0",
  "event_id": "evt_001",
  "event_type": "audit.record",
  "producer_id": "audit-service",
  "request_id": "req_001",
  "correlation_id": "corr_001",
  "event_schema_id": "https://echoauth.local/events/event-envelope-v2.schema.json",
  "event_schema_version": "2.0.0",
  "payload_schema_id": "https://echoauth.local/schemas/audit-record.schema.json",
  "payload_schema_version": "1.0.0",
  "confidentiality_class": "restricted",
  "integrity_class": "high",
  "payload": {
    "event_type": "example",
    "actor_id": "service",
    "reason": "example",
    "details": {},
    "occurred_at": "2026-06-20T12:00:00Z"
  },
  "payload_hash": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "occurred_at": "2026-06-20T12:00:00Z",
  "signature_evidence": {
    "algorithm_id": "unapproved",
    "key_id": "unapproved",
    "signed_fields": ["event_id", "payload_hash"],
    "signature_encoding": "base64url",
    "signature_value": "unapproved",
    "signed_at": "2026-06-20T12:00:00Z"
  }
}
```

# Approval Blockers

The following decisions remain unresolved and prohibit runtime implementation:

1. Transport and broker selection, acknowledgement semantics, and failure codes.
2. Storage engine, transaction isolation, locks, durable offsets, and migrations.
3. Concrete retention durations, deletion authority, and legal-hold ownership.
4. Signature algorithm registry, trust roots, key rotation, revocation, and KMS.
5. Machine-verifiable confidential-field profiles for open canonical payloads.
6. Subscription registrar authority and lifecycle mutation authority.
7. Audit writer identity, chain selection, append authority, and append failures.
8. Durable causal lookup source, retention window, and conflict authority.

Until these blockers are approved in the decision log, all operational event-bus
behavior remains on HOLD.
