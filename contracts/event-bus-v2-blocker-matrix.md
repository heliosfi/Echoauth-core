# Event Bus v2 Blocker Dependency Matrix

Contract version: `2.0.0-draft`

Matrix status: `HOLD`

Approval status: `NOT APPROVED`

## Governance Boundary

This matrix records dependency evidence for the eight Event-Bus v2 approval
blockers. It does not resolve a blocker, assign a real accountable party,
establish authority, approve a contract, or authorize runtime implementation.

**Dependency mapping does not grant approval.**

All blockers remain `UNRESOLVED`. All accountable parties remain `UNASSIGNED`.
All authority references remain `ABSENT`. `approved: false` remains required.
HOLD remains active and compliant. Missing or unverifiable evidence continues
to fail closed under refusal-first governance.

## Dependency Summary

| Blocker | Status | Owner-role placeholder | Authority reference | Primary blocked capability |
| --- | --- | --- | --- | --- |
| EVT2-B01 | `UNRESOLVED` | Event transport contract owner | `ABSENT` | Publication, delivery, retry, and dead-letter processing |
| EVT2-B02 | `UNRESOLVED` | Persistence contract owner | `ABSENT` | Durable storage, offsets, replay, and delivery concurrency |
| EVT2-B03 | `UNRESOLVED` | Retention and legal-hold contract owner | `ABSENT` | Retention enforcement and durable cleanup |
| EVT2-B04 | `UNRESOLVED` | Cryptographic security contract owner | `ABSENT` | Distributed signing and verification |
| EVT2-B05 | `UNRESOLVED` | Data classification contract owner | `ABSENT` | Machine-verifiable sensitive-content enforcement |
| EVT2-B06 | `UNRESOLVED` | Subscription governance contract owner | `ABSENT` | Subscription lifecycle mutation and routing eligibility |
| EVT2-B07 | `UNRESOLVED` | Event audit contract owner | `ABSENT` | Event audit append and chain evidence |
| EVT2-B08 | `UNRESOLVED` | Causation integrity contract owner | `ABSENT` | Durable cross-batch causation resolution |

The dependency lists below distinguish contract authoring from operational
activation. A blocker may have no prerequisite for drafting while still
depending on other resolved blockers before any runtime capability can activate.

## EVT2-B01

- Status: `UNRESOLVED`
- Owner role placeholder: Event transport contract owner
- Accountable party: `UNASSIGNED`
- Authority reference status: `ABSENT`
- Required evidence: Named accountable party; transport-neutral boundary; acknowledgement states; failure-code registry; retry and dead-letter implications; approval authority reference.
- Required approval category: Integration architecture governance approval.
- Dependent contracts: `contracts/event-bus-v2.yaml`; `specs/event-bus-v2.md`; `schemas/event-bus-runtime-v2.schema.json`; `events/event-catalog-v2.yaml`.
- Dependent runtime capabilities: Publication; delivery; acknowledgement processing; retry scheduling; dead-letter classification.
- Upstream dependencies: No blocker prerequisite for contract drafting; operational activation requires EVT2-B02, EVT2-B04, EVT2-B05, EVT2-B06, and EVT2-B07.
- Downstream dependencies: EVT2-B02 durable delivery records; EVT2-B03 delivery retention; EVT2-B08 delivered-event causal lookup.
- Resolution criteria: Explicit transport and acknowledgement contract; canonical failure codes; retry and dead-letter boundaries; named accountable party; verified authority reference; governance decision reference; updated v2 conformance evidence.

## EVT2-B02

- Status: `UNRESOLVED`
- Owner role placeholder: Persistence contract owner
- Accountable party: `UNASSIGNED`
- Authority reference status: `ABSENT`
- Required evidence: Named accountable party; storage-engine decision; transaction isolation; locking; migrations; durable uniqueness; offset and concurrency rules; approval authority reference.
- Required approval category: Data architecture governance approval.
- Dependent contracts: `contracts/event-bus-v2.yaml`; `schemas/event-bus-runtime-v2.schema.json`; future versioned persistence contract; future versioned database schema.
- Dependent runtime capabilities: Durable events; offsets; delivery attempts; replay records; dead-letter records; causal lookup records.
- Upstream dependencies: No blocker prerequisite for contract drafting; operational activation requires EVT2-B03, EVT2-B04, EVT2-B05, and EVT2-B07.
- Downstream dependencies: EVT2-B01 durable retry and dead-letter behavior; EVT2-B03 retention enforcement; EVT2-B08 durable cross-batch lookup.
- Resolution criteria: Explicit engine and transaction contract; uniqueness and concurrency rules; migration contract; named accountable party; verified authority reference; governance decision reference; updated v2 conformance evidence.

## EVT2-B03

- Status: `UNRESOLVED`
- Owner role placeholder: Retention and legal-hold contract owner
- Accountable party: `UNASSIGNED`
- Authority reference status: `ABSENT`
- Required evidence: Named accountable party; duration table by retention class; deletion authority; legal-hold ownership; jurisdiction review; approval authority reference.
- Required approval category: Data governance and legal retention approval.
- Dependent contracts: `contracts/event-bus-v2.yaml`; `events/event-catalog-v2.yaml`; future versioned retention contract.
- Dependent runtime capabilities: Retention enforcement; deletion; legal hold; dead-letter retention; replay window; causation lookup window.
- Upstream dependencies: Contract drafting requires accountable data-governance and jurisdiction evidence; operational activation requires EVT2-B02, EVT2-B05, and EVT2-B07.
- Downstream dependencies: EVT2-B02 storage lifecycle; EVT2-B08 causal evidence retention.
- Resolution criteria: Approved durations and deletion rules for every retention class; legal-hold authority; named accountable party; verified authority reference; governance decision reference; updated v2 conformance evidence.

## EVT2-B04

- Status: `UNRESOLVED`
- Owner role placeholder: Cryptographic security contract owner
- Accountable party: `UNASSIGNED`
- Authority reference status: `ABSENT`
- Required evidence: Named accountable party; algorithm registry; signed-field profile; trust roots; rotation; revocation; verification failures; KMS boundary; approval authority reference.
- Required approval category: Security architecture and cryptographic governance approval.
- Dependent contracts: `contracts/event-bus-v2.yaml`; `events/event-envelope-v2.schema.json`; `schemas/event-bus-runtime-v2.schema.json`; future versioned trust and key-management contract.
- Dependent runtime capabilities: High-integrity signing; signature verification; trust evaluation; key lifecycle handling.
- Upstream dependencies: No blocker prerequisite for contract drafting; operational key storage may depend on EVT2-B02 and audit evidence may depend on EVT2-B07.
- Downstream dependencies: EVT2-B01 high-integrity transport; EVT2-B02 stored-evidence authenticity; EVT2-B07 audit authenticity; EVT2-B08 causal-evidence authenticity.
- Resolution criteria: Approved algorithms, signed fields, trust roots, key lifecycle, KMS boundary, and fail-closed verification outcomes; named accountable party; verified authority reference; governance decision reference; updated v2 conformance evidence.

## EVT2-B05

- Status: `UNRESOLVED`
- Owner role placeholder: Data classification contract owner
- Accountable party: `UNASSIGNED`
- Authority reference status: `ABSENT`
- Required evidence: Named accountable party; event-type field profiles; prohibited-content representation; schema linkage; deterministic reject rules; privacy review; approval authority reference.
- Required approval category: Data security and privacy governance approval.
- Dependent contracts: `contracts/event-bus-v2.yaml`; `events/event-catalog-v2.yaml`; payload schemas selected by the catalog; future versioned confidentiality-profile contract.
- Dependent runtime capabilities: Machine-verifiable payload classification; prohibited-content rejection; sensitive and restricted payload validation.
- Upstream dependencies: Contract drafting requires authoritative payload-field and privacy evidence; no other blocker may substitute for that evidence.
- Downstream dependencies: EVT2-B01 transport eligibility; EVT2-B02 storage controls; EVT2-B03 retention classification; EVT2-B06 subscription access scope.
- Resolution criteria: Complete machine-verifiable profiles for every applicable event type; deterministic schema linkage and reject outcomes; named accountable party; verified authority reference; privacy governance decision reference; updated v2 conformance evidence.

## EVT2-B06

- Status: `UNRESOLVED`
- Owner role placeholder: Subscription governance contract owner
- Accountable party: `UNASSIGNED`
- Authority reference status: `ABSENT`
- Required evidence: Named accountable party; registrar identity requirements; explicit authority source; lifecycle mutation permissions; revocation rules; audit requirements; approval authority reference.
- Required approval category: Governance and access-control approval.
- Dependent contracts: `contracts/event-bus-v2.yaml`; `schemas/event-bus-runtime-v2.schema.json`; existing subscriber-authorization evidence boundary; future versioned subscription-authority contract.
- Dependent runtime capabilities: Subscription creation; activation; suspension; revocation; expiration; retirement; routing eligibility.
- Upstream dependencies: Contract drafting requires explicit authority-source evidence; operational activation requires EVT2-B04, EVT2-B05, and EVT2-B07.
- Downstream dependencies: EVT2-B01 deterministic subscriber delivery eligibility.
- Resolution criteria: Explicit registrar authority source and scope; lifecycle mutation matrix; revocation and audit rules; named accountable party; verified authority reference; governance decision reference; updated v2 conformance evidence.

## EVT2-B07

- Status: `UNRESOLVED`
- Owner role placeholder: Event audit contract owner
- Accountable party: `UNASSIGNED`
- Authority reference status: `ABSENT`
- Required evidence: Named accountable party; writer identity; chain selection; append authority; failure outcomes; evidence preservation; approval authority reference.
- Required approval category: Audit governance approval.
- Dependent contracts: `contracts/event-bus-v2.yaml`; `schemas/event-bus-runtime-v2.schema.json`; `schemas/audit-record.schema.json`; existing Sprint 2A audit-chain boundary; future versioned event-audit append contract.
- Dependent runtime capabilities: Event audit mapping acceptance; append request eligibility; chain selection; append-failure handling.
- Upstream dependencies: Contract drafting may reference the existing Sprint 2A audit foundation but still requires explicit event-writer and chain authority; operational persistence requires EVT2-B02 and distributed authenticity may require EVT2-B04.
- Downstream dependencies: EVT2-B01 delivery audit; EVT2-B02 persistence audit; EVT2-B03 retention audit; EVT2-B06 subscription mutation audit; EVT2-B08 causation conflict audit.
- Resolution criteria: Explicit writer, chain, and append authority contract; deterministic failure outcomes that preserve refusal-first behavior; named accountable party; verified authority reference; governance decision reference; updated v2 conformance evidence.

## EVT2-B08

- Status: `UNRESOLVED`
- Owner role placeholder: Causation integrity contract owner
- Accountable party: `UNASSIGNED`
- Authority reference status: `ABSENT`
- Required evidence: Named accountable party; durable lookup source; retention window; request boundary; conflict rules; conflict authority; approval authority reference.
- Required approval category: Event integrity governance approval.
- Dependent contracts: `contracts/event-bus-v2.yaml`; `schemas/event-bus-runtime-v2.schema.json`; existing Sprint 2W causation-evidence boundary; future versioned durable-causation contract.
- Dependent runtime capabilities: Cross-batch causal lookup; causal conflict classification; durable resolution evidence.
- Upstream dependencies: Operational activation requires EVT2-B02, EVT2-B03, EVT2-B04, and EVT2-B07.
- Downstream dependencies: No other blocker depends on cross-batch causation for contract drafting; future orchestration remains outside Event-Bus v2 approval.
- Resolution criteria: Explicit lookup, retention, request-boundary, and conflict-authority contract; no inferred causation; named accountable party; verified authority reference; governance decision reference; updated v2 conformance evidence.

## Matrix Disposition

This matrix supplies dependency evidence only. It does not change any intake
status or blocker disposition in `contracts/event-bus-v2-approval-record.md` or
`contracts/event-bus-v2-decision-log.md`.

- Blockers resolved: `0 of 8`
- Accountable parties assigned: `0 of 8`
- Authority references present: `0 of 8`
- Runtime capabilities authorized: `0`
- Approval: `NOT APPROVED`
- HOLD: `ACTIVE`

`runtime.recovered` remains catalog-only. No dependency relationship may be
used to accept, produce, subscribe, publish, replay, or emit it.
