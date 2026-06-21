# Event Bus v2 Approval Readiness Record

Contract version: `2.0.0-draft`

Record status: `HOLD`

Approval status: `NOT APPROVED`

Runtime implementation permitted: `NO`

## Purpose

Track approval readiness for the Event-Bus v2 contract set without granting
approval or introducing runtime behavior. This record preserves the Sprint 3A
contract boundary and the Sprint 3B conformance boundary.

**HOLD remains active and compliant.** Tests, schema validation, conformance
reports, role assignment, and completion of this record do not grant approval.

## Authority Boundary

The owner roles below identify the discipline accountable for proposing a
decision. They do not identify a person, prove identity, establish authority,
or authorize a contract change. A named accountable party and explicit approval
authority reference remain required before any blocker can be resolved.

Every owner role in this record is a placeholder. A placeholder cannot submit,
verify, approve, or reject a decision and cannot be treated as an authority
record.

Coordination proposes. Governance permits. Evidence does not authorize.
Execution remains separate from authorization.

## Blocker Register

| ID | Canonical blocker | Decision category | Accountable owner role | Disposition | Resolution evidence required | Blocked capability |
| --- | --- | --- | --- | --- | --- | --- |
| EVT2-B01 | `transport_and_acknowledgement_contract` | Integration architecture | Event transport contract owner | `UNRESOLVED` | Named accountable party; transport-neutral boundary; acknowledgement states; failure-code registry; retry and dead-letter implications; approval authority reference | Publication, delivery, retry, and dead-letter processing |
| EVT2-B02 | `storage_engine_and_transaction_contract` | Data architecture | Persistence contract owner | `UNRESOLVED` | Named accountable party; engine decision; transaction isolation; locking; migration; uniqueness; offset and concurrency rules; approval authority reference | Persistence, offsets, replay, and concurrent delivery attempts |
| EVT2-B03 | `retention_durations_and_deletion_authority` | Data governance | Retention and legal-hold contract owner | `UNRESOLVED` | Named accountable party; duration table by retention class; deletion authority; legal-hold ownership; jurisdiction review; approval authority reference | Retention enforcement and durable cleanup |
| EVT2-B04 | `signature_algorithm_registry_and_trust_roots` | Security architecture | Cryptographic security contract owner | `UNRESOLVED` | Named accountable party; algorithm registry; signed-field profile; trust roots; rotation; revocation; verification failures; KMS boundary; approval authority reference | Distributed signing and verification |
| EVT2-B05 | `machine_verifiable_confidential_field_profiles` | Data security and privacy | Data classification contract owner | `UNRESOLVED` | Named accountable party; event-type field profiles; prohibited-content representation; schema linkage; deterministic reject rules; privacy review; approval authority reference | Sensitive-content enforcement beyond explicit catalog classification |
| EVT2-B06 | `subscription_registration_and_mutation_authority` | Governance and access control | Subscription governance contract owner | `UNRESOLVED` | Named accountable party; registrar identity requirements; explicit authority source; lifecycle mutation permissions; revocation rules; audit requirements; approval authority reference | Subscription creation, activation, suspension, revocation, and retirement |
| EVT2-B07 | `audit_writer_chain_and_append_failure_contract` | Audit governance | Event audit contract owner | `UNRESOLVED` | Named accountable party; writer identity; chain selection; append authority; failure outcomes; evidence preservation; approval authority reference | Event audit append and chain evidence |
| EVT2-B08 | `durable_causation_lookup_and_conflict_authority` | Event integrity governance | Causation integrity contract owner | `UNRESOLVED` | Named accountable party; lookup source; retention window; request boundary; conflict rules; conflict authority; approval authority reference | Cross-batch causation resolution |

No repository artifact currently supplies the complete resolution evidence for
any blocker. Every disposition therefore remains `UNRESOLVED`.

## Accountable Authority Intake Structure

An authority intake record is governance evidence for review. It is not an
EchoAuth identity verdict, AuthorityRecord, authorization decision, contract
approval, or permission to implement runtime behavior.

Canonical machine-readable structure:
`schemas/event-bus-v2-authority-intake.schema.json`.

Schema conformance validates structure only. It does not verify a submitted
party, establish identity, establish authority, approve a decision, resolve a
blocker, or permit runtime implementation. The schema prohibits credentials and
secrets and requires every effect field to remain false.

The current schema accepts `NOT_SUBMITTED` placeholder records only. The full
intake lifecycle remains defined as vocabulary, but enabling any submitted state
requires an explicit submission protocol. Sprint 3I defines that structure in
`schemas/event-bus-v2-authority-intake-submission.schema.json`. Submission
conformance accepts only `SUBMITTED_UNVERIFIED`; it does not verify or accept
the evidence for governance review.

### Submission Protocol Boundary

The submission schema accepts stable references and hashes only. It prohibits
credentials, secrets, unnecessary personal data, inferred authority, identity
establishment, authority establishment, party assignment, approval, and blocker
resolution. A proposed party or authority reference remains proposed evidence;
the current register remains `UNASSIGNED` and `ABSENT` until a separate,
explicit verification and governance process authorizes a change.

Submission conformance does not update the current intake register. All current
entries therefore remain `NOT_SUBMITTED`, and no Sprint 3I artifact represents
an actual submission.

### Verification Protocol Boundary

Sprint 3J defines structure-only verification evidence in
`schemas/event-bus-v2-authority-intake-verification.schema.json`. Verification
must cite the submitted evidence, its hashes and provenance, the verifier's
authority evidence, and deterministic scope-alignment evidence. The protocol
rejects self-verification and inferred authority.

Only a structurally complete `VERIFIED` result may propose
`VERIFIED_PENDING_GOVERNANCE`. Every incomplete, invalid, conflicting, expired,
revoked, or unverifiable result preserves `SUBMITTED_UNVERIFIED`. Neither result
assigns a party, establishes identity or authority, supplies an accepted
authority reference, approves the contract, resolves a blocker, authorizes
execution, or mutates the current register.

No verification record is instantiated by Sprint 3J. The current register
remains authoritative and unchanged.

### Governance Admission Protocol Boundary

Sprint 3K defines structure-only governance admission evidence in
`schemas/event-bus-v2-authority-intake-governance-admission.schema.json`. The
protocol consumes a referenced, hash-bound verification record and independently
evidenced governance-review authority. It requires aligned scope, provenance,
and hash-bound evidence that the reviewer and reviewer-authority evidence are
distinct from the verification party and verification-authority evidence.

The only admission outcomes are `ACCEPTED_FOR_REVIEW` and `REJECTED`.
`ACCEPTED_FOR_REVIEW` permits governance review only; it is not approval.
`REJECTED` terminates that prospective intake only; it does not resolve the
associated blocker. Neither outcome assigns a party or authority, grants an
authority reference, authorizes execution, enables runtime behavior, or mutates
the current register.

No admission record is instantiated by Sprint 3K. HOLD remains active, and the
current register remains authoritative and unchanged.

### Authority Review Eligibility Protocol Boundary

Sprint 3N defines structure-only authority-review eligibility evidence in
`schemas/event-bus-v2-authority-review-eligibility.schema.json`. The reconciled
outcomes are `ELIGIBLE_FOR_AUTHORITY_REVIEW`,
`ADDITIONAL_EVIDENCE_REQUIRED`, and `INELIGIBLE_FOR_AUTHORITY_REVIEW`.

A favorable review disposition is necessary but not sufficient for eligibility.
`ELIGIBLE_FOR_AUTHORITY_REVIEW` additionally requires independently evidenced
eligibility authority, satisfied eligibility evidence, provenance, and aligned
scope. Missing evidence produces `ADDITIONAL_EVIDENCE_REQUIRED`; invalid or
conflicting evidence fails closed as `INELIGIBLE_FOR_AUTHORITY_REVIEW`.

Eligibility permits review consideration only. It grants no party assignment,
authority, authority reference, blocker resolution, approval, execution, or
runtime effect and cannot bypass the blocker-resolution procedure. No eligibility
record is instantiated by Sprint 3N, and the current register remains unchanged.

### Canonical Lifecycle Reconciliation Boundary

Sprint 3O defines the authoritative phase-qualified lifecycle graph in
`schemas/event-bus-v2-authority-intake-lifecycle-reconciliation.schema.json`.
Each mapping separates `intake_state`, `protocol_phase`, `evidence_outcome`, and
`register_mutation_status`.

The sole live-register mapping is `INTAKE_REGISTER` with `NOT_SUBMITTED` and
`LIVE_REGISTER_UNCHANGED`. Every Sprint 3I-3N mapping is
`PROSPECTIVE_EVIDENCE_ONLY`. Repeated `ACCEPTED_FOR_REVIEW` and `REJECTED`
states are valid only with an explicit protocol phase and evidence outcome.
`GOVERNANCE_REVIEW_COMPLETED` remains unsupported.

Reconciliation preserves all prior protocols and grants no assignment,
authority, authority reference, blocker resolution, approval, execution,
register mutation, or runtime effect. No reconciliation record is instantiated
by Sprint 3O.

### Authority Assignment Review Boundary

Sprint 3P defines structure-only authority-assignment review evidence in
`schemas/event-bus-v2-authority-assignment-review.schema.json`. The phase accepts
only `ELIGIBLE_FOR_AUTHORITY_REVIEW` source evidence and requires the complete
hash-bound evidence chain, blocker-specific scope, independent active reviewer
authority, conflict checks, provenance, and lifecycle-reconciliation evidence.

The outcomes are `CANDIDATE_RECOMMENDED_FOR_ASSIGNMENT_DECISION`,
`ADDITIONAL_ASSIGNMENT_EVIDENCE_REQUIRED`, and
`CANDIDATE_REJECTED_FOR_ASSIGNMENT_DECISION`. Recommendation is not assignment
or authority. Every outcome remains `PROSPECTIVE_EVIDENCE_ONLY` and preserves
the `ACCEPTED_FOR_REVIEW` intake state.

No outcome assigns a party, grants authority or an authority reference, creates
an `AuthorityRecord`, resolves a blocker, approves the contract, authorizes
execution, or mutates the register. No review record is instantiated by Sprint
3P.

### Authority Assignment Decision Boundary

Sprint 3Q defines structure-only authority-assignment decision evidence in
`schemas/event-bus-v2-authority-assignment-decision.schema.json`. The phase
accepts only `CANDIDATE_RECOMMENDED_FOR_ASSIGNMENT_DECISION` source evidence and
requires the complete hash-bound chain, proposed-party authority evidence,
blocker-specific scope, competing-candidate resolution, a clear conflict check,
and independent active decision authority.

The outcomes are `FAVORABLE_ASSIGNMENT_DECISION_RECORDED`,
`ADDITIONAL_ASSIGNMENT_DECISION_EVIDENCE_REQUIRED`, and
`UNFAVORABLE_ASSIGNMENT_DECISION_RECORDED`. A favorable decision is evidence
only; it does not permit assignment application. Every outcome remains
`PROSPECTIVE_EVIDENCE_ONLY` and preserves `ACCEPTED_FOR_REVIEW`.

No outcome assigns a party, grants authority or an authority reference, creates
an `AuthorityRecord`, resolves a blocker, approves the contract, authorizes
execution, or mutates the register. No decision record is instantiated by Sprint
3Q.

### Authority Assignment Application Readiness Boundary

Sprint 3R defines structure-only application-readiness evidence in
`schemas/event-bus-v2-authority-assignment-application-readiness.schema.json`.
The phase accepts only `FAVORABLE_ASSIGNMENT_DECISION_RECORDED` source evidence
and requires the complete chain, proposed-party authority and effective-period
evidence, current register snapshot/version/hash, all dependency contract
references, independent mutation authority, scope, and conflict evidence.

The outcomes are `ASSIGNMENT_APPLICATION_REVIEW_READY`,
`ADDITIONAL_APPLICATION_EVIDENCE_REQUIRED`, and
`ASSIGNMENT_APPLICATION_BLOCKED`. Required failure codes identify unresolved
register, persistence, audit append, idempotency, rollback, mutation-authority,
version, assignment-conflict, authority, and evidence dependencies.

Readiness is not mutation or application permission. No outcome assigns a party,
grants authority or an authority reference, creates an `AuthorityRecord`, writes
persistence, appends audit, resolves a blocker, approves the contract, authorizes
execution, or mutates the register. No readiness record is instantiated by
Sprint 3R.

### Governance Review Protocol Boundary

Sprint 3L defines structure-only governance review evidence in
`schemas/event-bus-v2-authority-intake-governance-review.schema.json`. The
protocol consumes an admitted intake record and requires independently evidenced
reviewer authority, aligned scope, provenance, and evidence hashes distinct from
the verifier and admission reviewer evidence.

The reconciled outcomes are `FAVORABLE_REVIEW_RECORDED`,
`ADDITIONAL_INFORMATION_REQUIRED`, and `REVIEW_REJECTED`. The first two preserve
`ACCEPTED_FOR_REVIEW`; the final outcome maps only to the existing `REJECTED`
intake state. Sprint 2J escalation-review outcomes are incompatible because they
consume escalation decisions and include override-routing semantics.

A favorable review is not authority assignment, blocker resolution, contract
approval, or execution permission. A rejected review does not resolve the
associated blocker. No review record is instantiated by Sprint 3L, and the
current register remains authoritative and unchanged.

### Review Disposition Protocol Boundary

Sprint 3M defines structure-only review disposition evidence in
`schemas/event-bus-v2-authority-intake-review-disposition.schema.json`. The
protocol maps all three Sprint 3L outcomes to evidence-retention dispositions.
The canonical dispositions are `FAVORABLE_REVIEW_EVIDENCE_RETAINED`,
`INFORMATION_REQUEST_EVIDENCE_RETAINED`, and
`REVIEW_REJECTION_EVIDENCE_RETAINED`. The first two preserve
`ACCEPTED_FOR_REVIEW`; the final disposition maps only to the existing
`REJECTED` intake state.

`GOVERNANCE_REVIEW_COMPLETED` is not a canonical Event-Bus v2 state and remains
explicitly unsupported. Disposition requires independently evidenced authority,
provenance, aligned scope, and evidence distinct from verification, admission,
and review authority evidence.

Disposition grants no assignment eligibility, party assignment, authority,
authority reference, blocker resolution, approval, execution permission, or
runtime effect. No disposition record is instantiated by Sprint 3M, and the
current register remains authoritative and unchanged.

| Field | Required | Rule |
| --- | --- | --- |
| `intake_id` | yes after submission | Stable non-empty identifier unique within this approval package. |
| `blocker_id` | yes | Exactly one of `EVT2-B01` through `EVT2-B08`. |
| `proposed_accountable_party_id` | yes after submission | Stable reference only; raw identity credentials and personal data are prohibited. |
| `owner_role` | yes | Must equal the blocker role in the register; matching a role does not establish authority. |
| `proposed_authority_source` | yes after submission | Explicit source category and repository or governance reference; role, title, affiliation, and ownership are insufficient alone. |
| `proposed_authority_reference` | yes after submission | Stable reference to unverified evidence proposed for the complete blocker scope; the accepted authority reference remains absent. |
| `proposed_authority_scope` | yes after submission | Must name the blocker and every decision surface proposed for review. |
| `submission_evidence_hash` | yes after submission | Canonical hash of non-secret, unverified submission evidence. |
| `submitted_at` | yes after submission | UTC timestamp supplied by the intake process. |
| `intake_status` | yes | `NOT_SUBMITTED`, `SUBMITTED_UNVERIFIED`, `VERIFIED_PENDING_GOVERNANCE`, `ACCEPTED_FOR_REVIEW`, or `REJECTED`. |
| `governance_decision_reference` | conditional | Required before a blocker disposition may change; intake acceptance alone is insufficient. |

### Intake State Rules

1. `NOT_SUBMITTED` is the fail-closed default.
2. `SUBMITTED_UNVERIFIED` requires all submission fields and grants no authority.
3. `VERIFIED_PENDING_GOVERNANCE` requires evidence verification but does not
   resolve the blocker or approve the contract.
4. `ACCEPTED_FOR_REVIEW` means only that governance may review the intake. It
   does not mean the blocker decision is accepted.
5. `REJECTED` is terminal for the intake record and leaves the blocker
   `UNRESOLVED`.
6. Missing, conflicting, expired, revoked, or unverifiable authority evidence
   leaves the intake unverified and the blocker unresolved.
7. No intake status permits `approved: true` or runtime implementation.
8. A blocker disposition can change only through the complete resolution
   procedure in this record and an explicit governance decision.

## Current Authority Intake Register

| Blocker | Owner-role placeholder | Accountable party | Authority reference | Intake status | Blocker disposition |
| --- | --- | --- | --- | --- | --- |
| EVT2-B01 | Event transport contract owner | `UNASSIGNED` | `ABSENT` | `NOT_SUBMITTED` | `UNRESOLVED` |
| EVT2-B02 | Persistence contract owner | `UNASSIGNED` | `ABSENT` | `NOT_SUBMITTED` | `UNRESOLVED` |
| EVT2-B03 | Retention and legal-hold contract owner | `UNASSIGNED` | `ABSENT` | `NOT_SUBMITTED` | `UNRESOLVED` |
| EVT2-B04 | Cryptographic security contract owner | `UNASSIGNED` | `ABSENT` | `NOT_SUBMITTED` | `UNRESOLVED` |
| EVT2-B05 | Data classification contract owner | `UNASSIGNED` | `ABSENT` | `NOT_SUBMITTED` | `UNRESOLVED` |
| EVT2-B06 | Subscription governance contract owner | `UNASSIGNED` | `ABSENT` | `NOT_SUBMITTED` | `UNRESOLVED` |
| EVT2-B07 | Event audit contract owner | `UNASSIGNED` | `ABSENT` | `NOT_SUBMITTED` | `UNRESOLVED` |
| EVT2-B08 | Causation integrity contract owner | `UNASSIGNED` | `ABSENT` | `NOT_SUBMITTED` | `UNRESOLVED` |

No accountable authority intake has been submitted. The register records
placeholders only and does not infer authority from those placeholders.

## Approval Readiness

| Gate | Current evidence | Status |
| --- | --- | --- |
| Versioned successor artifacts exist | Sprint 3A v2 specification, contract, schemas, catalog, and decision log | `PASS` |
| Cross-artifact conformance | Sprint 3B conformance validator and focused tests | `PASS` |
| Version 1 preservation | v2 is explicitly non-interchangeable and does not replace v1 | `PASS` |
| Refusal-first preservation | Missing dependencies resolve to rejection or HOLD; no positive inference | `PASS` |
| Blocker ownership categories | Eight accountable discipline roles assigned in this record | `PASS` |
| Accountable authority intake structure | Required fields and fail-closed intake states defined | `PASS` |
| Unverified submission protocol | Structure-only schema; no submissions instantiated | `PASS` |
| Verification evidence protocol | Structure-only schema; no verification instantiated | `PASS` |
| Governance admission protocol | Structure-only schema; no admission instantiated | `PASS` |
| Governance review protocol | Structure-only schema; no review instantiated | `PASS` |
| Review disposition protocol | Structure-only schema; no disposition instantiated | `PASS` |
| Authority review eligibility protocol | Structure-only schema; no eligibility instantiated | `PASS` |
| Canonical lifecycle reconciliation | Phase-qualified evidence graph; live register unchanged | `PASS` |
| Authority assignment review | Structure-only schema; no assignment or review instance | `PASS` |
| Authority assignment decision | Structure-only schema; no assignment or decision instance | `PASS` |
| Assignment application readiness | Structure-only schema; no application or mutation instance | `PASS` |
| Accountable authority intake records | Eight placeholders; no submissions | `BLOCKED` |
| Named accountable parties | No named parties or verified authority references exist | `BLOCKED` |
| Blocker dispositions | Eight of eight remain `UNRESOLVED` | `BLOCKED` |
| Explicit governance approval | No approval decision or authority reference exists | `BLOCKED` |
| Runtime implementation gate | `approved: false`; `runtime_implementation_permitted: false` | `HOLD` |

Overall readiness: `HOLD - NOT APPROVED`.

## Resolution Procedure

A blocker may change from `UNRESOLVED` only when all of the following are
recorded in a future approved contract sprint:

1. A concrete decision that resolves the complete canonical blocker.
2. A named accountable party and an explicit approval authority reference.
3. The affected versioned contract artifacts and deterministic rules.
4. Security, audit, failure, and refusal-first implications.
5. Conformance tests proving cross-artifact consistency and fail-closed handling.
6. An explicit governance disposition recorded in the decision log.

An accepted intake is not a resolved blocker. The governance disposition must
address the blocker decision itself and cite the accepted intake, authority
reference, contract changes, and conformance evidence.

Resolving one blocker does not approve unrelated capabilities or the complete
Event-Bus v2 contract. Partial resolution must retain HOLD for every dependent
runtime behavior.

## Approval Prohibition

`approved: true` must remain rejected by Sprint 3B conformance validation while
any blocker is unresolved, any accountable authority reference is absent, or an
explicit governance approval record is missing. Passing tests or conformance
checks cannot alter this rule and cannot auto-grant approval.

Changing the approval gate requires a separate, explicitly authorized contract
sprint. This Sprint 3C record does not authorize that change.

## Preserved Boundaries

- No runtime event publication, routing, callbacks, or delivery.
- No retry or dead-letter execution.
- No persistence, offsets, retention enforcement, or replay execution.
- No signing, verification, trust-store access, or key management.
- No payload redaction or sensitive-field inference.
- No audit append, chain selection, or persistence claim.
- No cross-batch causation resolution.
- No notification, orchestration, authorization effect, runtime-state mutation,
  execution, token issuance, or runtime recovery behavior.
- `runtime.recovered` remains catalog-only and cannot be accepted, produced,
  subscribed, published, replayed, or emitted.
- Sprint 3A remains a draft contract boundary. Sprint 3B remains a conformance
  boundary. Neither boundary grants operational permission.

## Final Disposition

All eight blockers are `UNRESOLVED`.

Approval remains `NOT APPROVED`.

Runtime implementation remains prohibited.

**HOLD remains active and compliant.**
