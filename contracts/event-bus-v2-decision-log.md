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

The accountable owner roles identify decision disciplines only. They do not
identify a person, establish authority, or resolve a blocker. Canonical tracking
details are recorded in `contracts/event-bus-v2-approval-record.md`.

| ID | Required decision | Decision category | Accountable owner role | Disposition | Blocking runtime capability |
| --- | --- | --- | --- | --- | --- |
| EVT2-B01 | Select transport boundary, acknowledgement semantics, and failure-code registry. | Integration architecture | Event transport contract owner | `UNRESOLVED` | Publication, delivery, retry, and dead-letter processing. |
| EVT2-B02 | Select storage engine, transaction isolation, locking, migrations, and durable uniqueness rules. | Data architecture | Persistence contract owner | `UNRESOLVED` | Persistence, offsets, replay, and concurrent delivery attempts. |
| EVT2-B03 | Approve retention durations, deletion authority, and legal-hold ownership. | Data governance | Retention and legal-hold contract owner | `UNRESOLVED` | Retention enforcement and durable cleanup. |
| EVT2-B04 | Approve signature algorithms, signed-field profile, trust roots, key rotation, revocation, and KMS boundary. | Security architecture | Cryptographic security contract owner | `UNRESOLVED` | Distributed signing and verification. |
| EVT2-B05 | Define machine-verifiable confidential-field profiles for open canonical payload schemas. | Data security and privacy | Data classification contract owner | `UNRESOLVED` | Sensitive-content enforcement beyond explicit catalog classification. |
| EVT2-B06 | Define subscription registrar identity and lifecycle mutation authority. | Governance and access control | Subscription governance contract owner | `UNRESOLVED` | Subscription creation, activation, suspension, revocation, and retirement. |
| EVT2-B07 | Define audit writer identity, chain selection, append authority, and append-failure outcomes. | Audit governance | Event audit contract owner | `UNRESOLVED` | Event audit append and chain evidence. |
| EVT2-B08 | Define durable causal lookup source, retention window, and conflict authority. | Event integrity governance | Causation integrity contract owner | `UNRESOLVED` | Cross-batch causation resolution. |

Conformance and tests provide evidence only. They do not grant approval. All
eight blockers remain unresolved, `approved: true` must remain rejected, and
HOLD remains active.

## Accountable Authority Intake

Owner roles are placeholders for accountable disciplines. They are not named
parties, verified identities, AuthorityRecords, or approval authorities. Intake
requirements and state rules are canonical in
`contracts/event-bus-v2-approval-record.md`.

| Blocker | Owner-role placeholder | Accountable party | Authority reference | Intake status | Disposition |
| --- | --- | --- | --- | --- | --- |
| EVT2-B01 | Event transport contract owner | `UNASSIGNED` | `ABSENT` | `NOT_SUBMITTED` | `UNRESOLVED` |
| EVT2-B02 | Persistence contract owner | `UNASSIGNED` | `ABSENT` | `NOT_SUBMITTED` | `UNRESOLVED` |
| EVT2-B03 | Retention and legal-hold contract owner | `UNASSIGNED` | `ABSENT` | `NOT_SUBMITTED` | `UNRESOLVED` |
| EVT2-B04 | Cryptographic security contract owner | `UNASSIGNED` | `ABSENT` | `NOT_SUBMITTED` | `UNRESOLVED` |
| EVT2-B05 | Data classification contract owner | `UNASSIGNED` | `ABSENT` | `NOT_SUBMITTED` | `UNRESOLVED` |
| EVT2-B06 | Subscription governance contract owner | `UNASSIGNED` | `ABSENT` | `NOT_SUBMITTED` | `UNRESOLVED` |
| EVT2-B07 | Event audit contract owner | `UNASSIGNED` | `ABSENT` | `NOT_SUBMITTED` | `UNRESOLVED` |
| EVT2-B08 | Causation integrity contract owner | `UNASSIGNED` | `ABSENT` | `NOT_SUBMITTED` | `UNRESOLVED` |

No intake has been submitted. No accountable party or authority reference may
be inferred from a role label, repository authorship, affiliation, ownership,
or conformance result. Intake acceptance, when it occurs, will permit governance
review only; it will not resolve a blocker or approve runtime implementation.

Sprint 3I defines the machine-readable structure for a future
`SUBMITTED_UNVERIFIED` intake in
`schemas/event-bus-v2-authority-intake-submission.schema.json`. Schema
conformance records neither a submission nor a verified identity, authority,
assignment, approval, or blocker disposition. Credentials, secrets, unnecessary
personal data, and inferred authority are prohibited. The register above remains
the authoritative current state.

Sprint 3J defines a machine-readable verification-evidence protocol in
`schemas/event-bus-v2-authority-intake-verification.schema.json`. A conforming
`VERIFIED` result may propose `VERIFIED_PENDING_GOVERNANCE` only; it is not an
assignment, accepted authority reference, approval, blocker resolution, or
runtime permission. Every non-verified deterministic outcome preserves
`SUBMITTED_UNVERIFIED`. No verification instance or register mutation is
recorded by this decision log.

Sprint 3K defines governance-admission evidence in
`schemas/event-bus-v2-authority-intake-governance-admission.schema.json`.
Admission requires independently evidenced governance-review authority and
permits only `ACCEPTED_FOR_REVIEW` or `REJECTED`. Admission is not governance
approval: neither outcome assigns authority, grants an authority reference,
resolves a blocker, authorizes execution, enables runtime behavior, or mutates
the current register. No admission instance is recorded by this decision log.

Sprint 3L reconciles a separate governance-review vocabulary for admitted
authority intake evidence: `FAVORABLE_REVIEW_RECORDED`,
`ADDITIONAL_INFORMATION_REQUIRED`, and `REVIEW_REJECTED`. The contract is
machine-readable in
`schemas/event-bus-v2-authority-intake-governance-review.schema.json`.
Sprint 2J escalation-review outcomes are explicitly incompatible with this
protocol. Favorable review is not approval, rejected review is not blocker
resolution, and no review instance or register mutation is recorded here.

Sprint 3M reconciles evidence-only review dispositions:
`FAVORABLE_REVIEW_EVIDENCE_RETAINED`,
`INFORMATION_REQUEST_EVIDENCE_RETAINED`, and
`REVIEW_REJECTION_EVIDENCE_RETAINED`. Their machine-readable contract is
`schemas/event-bus-v2-authority-intake-review-disposition.schema.json`.
`GOVERNANCE_REVIEW_COMPLETED` remains unsupported. Disposition does not grant
assignment eligibility, authority, approval, blocker resolution, execution, or
register mutation, and no disposition instance is recorded here.

Sprint 3N reconciles authority-review eligibility outcomes:
`ELIGIBLE_FOR_AUTHORITY_REVIEW`, `ADDITIONAL_EVIDENCE_REQUIRED`, and
`INELIGIBLE_FOR_AUTHORITY_REVIEW`. Their machine-readable contract is
`schemas/event-bus-v2-authority-review-eligibility.schema.json`. A favorable
disposition alone is insufficient; independent eligibility evidence is required.
Eligibility permits review consideration only and grants no assignment,
authority, authority reference, approval, blocker resolution, execution, or
register mutation. No eligibility instance is recorded here.

Sprint 3O reconciles the authority-intake lifecycle in
`schemas/event-bus-v2-authority-intake-lifecycle-reconciliation.schema.json`.
The graph separates intake state, protocol phase, evidence outcome, and register
mutation status. Duplicate `ACCEPTED_FOR_REVIEW` and `REJECTED` uses require an
explicit phase. Only `INTAKE_REGISTER / NOT_SUBMITTED` describes the live
register; every Sprint 3I-3N mapping is prospective evidence.
`GOVERNANCE_REVIEW_COMPLETED` remains unsupported, and reconciliation grants no
governance or runtime effect.

Sprint 3P adds the prospective `AUTHORITY_ASSIGNMENT_REVIEW` phase through
`schemas/event-bus-v2-authority-assignment-review.schema.json`. Its canonical
outcomes are `CANDIDATE_RECOMMENDED_FOR_ASSIGNMENT_DECISION`,
`ADDITIONAL_ASSIGNMENT_EVIDENCE_REQUIRED`, and
`CANDIDATE_REJECTED_FOR_ASSIGNMENT_DECISION`. Recommendation is not assignment,
authority, approval, blocker resolution, execution permission, or register
mutation. No assignment-review instance is recorded here.

Sprint 3Q adds the prospective `AUTHORITY_ASSIGNMENT_DECISION` phase through
`schemas/event-bus-v2-authority-assignment-decision.schema.json`. Its outcomes
are `FAVORABLE_ASSIGNMENT_DECISION_RECORDED`,
`ADDITIONAL_ASSIGNMENT_DECISION_EVIDENCE_REQUIRED`, and
`UNFAVORABLE_ASSIGNMENT_DECISION_RECORDED`. Favorable decision evidence is not
assignment application, authority, approval, blocker resolution, execution
permission, or register mutation. No assignment-decision instance is recorded.

Sprint 3R adds the prospective `AUTHORITY_ASSIGNMENT_APPLICATION_READINESS`
phase through
`schemas/event-bus-v2-authority-assignment-application-readiness.schema.json`.
Its outcomes are `ASSIGNMENT_APPLICATION_REVIEW_READY`,
`ADDITIONAL_APPLICATION_EVIDENCE_REQUIRED`, and
`ASSIGNMENT_APPLICATION_BLOCKED`. Readiness remains evidence-only and permits no
assignment application, persistence write, audit append, approval, execution,
or register mutation. No readiness instance is recorded here.

## Approval Gate

Sprint 3A authoring, Sprint 3B conformance, and Sprint 3C readiness tracking do
not approve this contract set. Approval requires:

1. Every proposed decision to be explicitly accepted or revised.
2. Every blocker required by the intended implementation scope to be resolved.
3. Cross-artifact syntax, reference, vocabulary, and state consistency validation.
4. Confirmation that version 1 and Sprint 2A-2P freeze artifacts are unchanged.
5. Confirmation that refusal-first behavior, authority separation, and the
   distinction between evidence, authorization, coordination, and execution are
   preserved.

**HOLD remains compliant until approval is recorded.** No event-bus runtime
implementation is authorized by this decision log.
