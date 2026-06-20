# Event Bus v2 Decision Log

Contract version: `2.0.0-draft`

Approval status: `HOLD`

This log applies only to the versioned successor artifacts listed in
`specs/event-bus-v2.md`. It does not modify or supersede version 1 contracts.

## Proposed Decisions

| ID | Status | Decision | Repository evidence | Effect after approval |
| --- | --- | --- | --- | --- |
| EVT2-001 | Proposed | Create v2 as a non-interchangeable successor; preserve v1 unchanged. | Sprint 2Y gap report; Sprint 2A-2P freeze change control. | Any v1/v2 adaptation requires a separate explicit contract. |
| EVT2-002 | Proposed | Require envelope and payload schema IDs and versions on every v2 event. | `specs/event-bus.md` requires stored schema version; Sprint 2V binds schema identity and hashes. | Missing or mismatched identity is rejected. |
| EVT2-003 | Proposed | Use `public`, `internal`, `sensitive`, and `restricted` confidentiality classes; prohibit inference and automatic redaction. | `specs/security-model.md`; Sprint 2Y confidentiality gap. | Catalog controls classification; missing or mismatched evidence fails closed. |
| EVT2-004 | Proposed | Define immutable versioned subscriptions with `proposed`, `active`, `suspended`, `revoked`, `expired`, and `retired` states. | `specs/event-bus.md` requires deterministic routing by subscription version; Sprint 2S authorizes but does not register. | Only active, effective, exact-version subscriptions are candidates. |
| EVT2-005 | Proposed | Define delivery evidence states without granting transition authority. | v1 event-bus states; Sprint 2Y delivery gap. | Delivery state vocabulary becomes machine-readable; runtime remains deferred. |
| EVT2-006 | Proposed | Make replay prohibited by default and otherwise authority-evidence gated. | Freeze invariant rejects replay; deferred-capabilities register. | Eligibility evidence never permits publication or delivery. |
| EVT2-007 | Proposed | Define high-integrity signature evidence vocabulary without selecting algorithms or trust roots. | `specs/event-bus.md`; deferred signing and key management. | Distributed signing remains blocked pending cryptographic contracts. |
| EVT2-008 | Proposed | Map acceptance and rejection evidence to audit-record fields without claiming append. | `specs/event-bus.md`; Sprint 2X audit evidence packaging; Sprint 2A audit chain. | Mapping evidence remains distinct from immutable audit append. |
| EVT2-009 | Proposed | Preserve absent and unresolved causation; prohibit self-reference and cross-request causation. | Sprint 2W behavior; Sprint 2Y causation gap. | Cross-batch resolution remains blocked without a durable lookup contract. |
| EVT2-010 | Proposed | Keep `runtime.recovered` catalog-only. | Sprint 2A-2P freeze prohibition; Sprint 2P Recovery eligibility boundary. | Acceptance, production, subscription, publication, replay, and emission remain prohibited. |

No proposed decision is approved merely because it appears in this file.

## Rejected Alternatives

| ID | Alternative | Reason rejected |
| --- | --- | --- |
| EVT2-R01 | Modify v1 artifacts in place. | Violates the frozen baseline and removes explicit compatibility control. |
| EVT2-R02 | Infer confidential fields from names or values. | No authoritative nested payload profiles exist; inference is non-deterministic. |
| EVT2-R03 | Automatically redact payloads. | Redaction changes canonical payload and hash evidence without a transformation contract. |
| EVT2-R04 | Treat subscriber authorization as a subscription. | Authorization evidence does not define registration, lifecycle, priority, or version. |
| EVT2-R05 | Treat delivery eligibility as delivery success. | Evidence cannot claim transport acknowledgement or external effects. |
| EVT2-R06 | Treat replay eligibility as authorization to publish. | Replay is separately governed and prohibited by default. |
| EVT2-R07 | Treat canonical hashes as distributed signatures. | Hashes provide integrity evidence but no signer authenticity or trust chain. |
| EVT2-R08 | Treat Sprint 2X evidence as an appended audit record. | No writer, chain, append authority, or append result is established. |
| EVT2-R09 | Infer cross-batch causation from correlation or time. | Correlation and ordering do not prove causation. |

## Unresolved Approval Blockers

| ID | Required decision | Blocking runtime capability |
| --- | --- | --- |
| EVT2-B01 | Select transport boundary, acknowledgement semantics, and failure-code registry. | Publication, delivery, retry, and dead-letter processing. |
| EVT2-B02 | Select storage engine, transaction isolation, locking, migrations, and durable uniqueness rules. | Persistence, offsets, replay, and concurrent delivery attempts. |
| EVT2-B03 | Approve retention durations, deletion authority, and legal-hold ownership. | Retention enforcement and durable cleanup. |
| EVT2-B04 | Approve signature algorithms, signed-field profile, trust roots, key rotation, revocation, and KMS boundary. | Distributed signing and verification. |
| EVT2-B05 | Define machine-verifiable confidential-field profiles for open canonical payload schemas. | Sensitive-content enforcement beyond explicit catalog classification. |
| EVT2-B06 | Define subscription registrar identity and lifecycle mutation authority. | Subscription creation, activation, suspension, revocation, and retirement. |
| EVT2-B07 | Define audit writer identity, chain selection, append authority, and append-failure outcomes. | Event audit append and chain evidence. |
| EVT2-B08 | Define durable causal lookup source, retention window, and conflict authority. | Cross-batch causation resolution. |

## Approval Gate

Sprint 3A authoring does not approve this contract set. Approval requires:

1. Every proposed decision to be explicitly accepted or revised.
2. Every blocker required by the intended implementation scope to be resolved.
3. Cross-artifact syntax, reference, vocabulary, and state consistency validation.
4. Confirmation that version 1 and Sprint 2A-2P freeze artifacts are unchanged.
5. Confirmation that refusal-first behavior, authority separation, and the
   distinction between evidence, authorization, coordination, and execution are
   preserved.

**HOLD remains compliant until approval is recorded.** No event-bus runtime
implementation is authorized by this decision log.
