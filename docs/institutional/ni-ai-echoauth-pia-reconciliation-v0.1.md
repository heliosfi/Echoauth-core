# NI-AI / EchoAuth PIA Current-State Reconciliation v0.1

**Authority:** Nicholas B. Carty (N.B.C.)  
**Decision:** ADVANCE — DOCUMENTATION-ONLY PIA RECONCILIATION  
**Repository:** `heliosfi/Echoauth-core`  
**Canonical reconciliation baseline:** `main@f7398b8fa24e0a2d515ce26ad7446dbc9ec8ac56`  
**Runtime effect:** NONE  
**External authority created:** NONE  
**Privacy compliance or certification created:** NONE  
**Consent authority created:** NONE  
**Production-data processing established:** NONE  
**Existing governance dispositions changed:** NONE

## 1. Purpose and provenance

This document reconciles the historical November 2025 NI-AI / EchoAuth Privacy Impact Assessment (PIA) material against current repository evidence without promoting historical assumptions about collection, personal information, storage, retention, sharing, privacy controls, deployment, legal applicability, or regulatory status into present facts.

Historical source lineage is preserved in `archive/journal/2025-11-21_Pia.html` and in the broader institutional-pack lineage already reconciled by `docs/institutional/ni-ai-government-pack-reconciliation-v0.1.md`.

The historical PIA material is treated only as design and assessment lineage. Its presence does not establish present data collection, actual user records, production processing, durable storage, external disclosure, consent, deployment, privacy compliance, legal sufficiency, or system authorization.

This reconciliation does not rewrite, replace, delete, or validate the historical journal.

## 2. Evidence-classification vocabulary

Only the following classifications are used:

- **CURRENTLY ESTABLISHED** — a present repository-level fact or governing rule is directly evidenced at the stated baseline.
- **DOCUMENTED / SPECIFIED** — a current specification, schema, interface, or governance artifact defines a field, boundary, or requirement; implementation is not established by documentation alone.
- **IMPLEMENTED** — current source artifacts implement bounded handling or processing at a repository seam.
- **VERIFIED** — current repository evidence records successful bounded tests for the stated implementation. This does not establish production operation, real-user processing, independent privacy audit, legal compliance, or external certification.
- **PARTIALLY SUPPORTED** — current repository evidence corresponds to part of the historical concept, but the historical or privacy claim is broader than what is established.
- **HISTORICAL PROPOSAL** — the concept is preserved from historical material without sufficient current evidence to promote it.
- **NOT ESTABLISHED** — current inspected repository evidence does not establish the claim.
- **HOLD** — the claim or boundary remains intentionally unresolved pending appropriate evidence.

Classification applies only to the exact bounded statement where it appears. No classification may be generalized into a broader privacy program, production environment, legal determination, or external compliance claim.

## 3. Current evidence inspected

This reconciliation is grounded in current repository evidence at the stated baseline, including:

- `docs/institutional/ni-ai-echoauth-ssp-reconciliation-v0.1.md`
- `docs/institutional/ni-ai-government-pack-reconciliation-v0.1.md`
- `runtime/traceability-matrix.md`
- `runtime/sprint-1-implementation-evidence.md`
- `runtime/sprint-2d-implementation-evidence.md`
- `runtime/sprint-2i-implementation-evidence.md`
- `runtime/sprint-2m-implementation-evidence.md`
- `src/echoauth/identity/models.py`
- `src/echoauth/auth/authority_models.py`
- `src/echoauth/auth/delegation_models.py`
- `src/echoauth/auth/authorization_models.py`
- `src/echoauth/policy/models.py`
- `src/echoauth/policy/refusal_models.py`
- `src/echoauth/governance/escalation_models.py`
- `src/echoauth/governance/review_models.py`
- `src/echoauth/governance/override_models.py`
- `src/echoauth/execution/models.py`
- `src/echoauth/models.py`
- `src/echoauth/audit/logging.py`
- `src/echoauth/config.py`
- current schema, event, database, persistence, and contract artifacts referenced by the runtime traceability matrix.

Repository models and schemas establish technical shapes. Implemented services establish bounded handling. In-memory repositories and local tests establish repository-local behavior. None of those facts alone establish actual production collection or real-user processing.

## 4. Three-layer data-evidence rule

Every data-related claim in this reconciliation must distinguish the following layers:

```text
DEFINED FIELD
!=
IMPLEMENTED PROCESSING
!=
ACTUAL PRODUCTION COLLECTION
```

A field can exist without a service processing it. A service can process a test or caller-supplied object without proving a production system collects corresponding information from real users. A persistence schema or repository interface can exist without proving durable production storage.

## 5. Current data-inventory correspondence

| Data / artifact category | Current repository representation | Evidence classification | Implemented processing | Actual production collection |
| --- | --- | --- | --- | --- |
| Identity identifiers | `IdentityRecord` defines `identity_record_id`, `actor_id`, `actor_type`, status, credential references, timestamps, optional display label, and role references. | **DOCUMENTED / SPECIFIED** for fields; bounded identity registry/resolution support is **IMPLEMENTED** elsewhere in current runtime evidence. | Bounded identity handling exists at repository seams. | **NOT ESTABLISHED** |
| Credential references / verification evidence | Identity models define `credential_refs`; credential verification artifacts carry verdict, assurance level, reason, verifier component, and evidence object. | **PARTIALLY SUPPORTED** | Bounded verification interfaces and test implementations exist. | **NOT ESTABLISHED** as collection of production credentials or external identity-provider data. |
| Authority records | `AuthorityRecord` defines authority record/source IDs, `subject_id`, authority type, scope, priority, issue/expiry times, evidence hash, status, and optional source-document hash. | **IMPLEMENTED** at bounded authority-registry/resolution seams; Sprint 2D evidence is **VERIFIED** locally. | Deterministic authority resolution is test-backed. | **NOT ESTABLISHED** |
| Parent / caregiver / institutional authority categories | Current authority model includes parent, caregiver, institution, delegated, emergency, and runtime-service categories. | **DOCUMENTED / SPECIFIED** as categories; bounded authority handling is **IMPLEMENTED**. | Category-bearing authority records can be processed. | **NOT ESTABLISHED** as real parent, caregiver, school, clinical, or institutional records. |
| Delegation records | `DelegationGrant` defines grantor, delegate, subject, role, actions, resources, context constraints, issue/expiry/revocation information, authority references, chain metadata, and evidence hash. | **IMPLEMENTED** as bounded repository/runtime artifacts. | Delegation validation can process canonical grant/request artifacts. | **NOT ESTABLISHED** |
| Policy records | `PolicyRule` defines policy/rule IDs, type, effect, actions, resources, scope, priority, reason, status, creator, effective/expiry times, and policy hash. | **IMPLEMENTED** as bounded declarative policy artifacts. | Policy evaluation can process canonical policy artifacts. | **NOT ESTABLISHED** |
| Authorization requests | `AuthorizationRequest` defines requester and subject identifiers, action, resource, credential set, required assurance, payload, context, policy version, correlation ID, idempotency key, and optional delegation/session references. | **IMPLEMENTED** as a bounded authorization data shape. | Authorization gate processing exists at repository seams. | **NOT ESTABLISHED** as production collection from users or connected systems. |
| Authorization decisions | `AuthorizationDecision` defines outcome, reason, evidence/evidence hash, decision time, upstream decision references, and audit reference. | **IMPLEMENTED** | Current authorization processing can produce bounded decision artifacts. | **NOT ESTABLISHED** as production decision history. |
| Refusal evidence | Refusal models define request/failure metadata, severity, recoverability, authorization linkage, reason category, evidence, timestamps, and audit reference. | **IMPLEMENTED** | Bounded refusal handling exists. | **NOT ESTABLISHED** |
| Escalation evidence | Escalation models define request/subject IDs, trigger state/reason, required review type, evidence, authorization/refusal linkage, deadlines, category, resolution, timestamps, and audit reference. | **IMPLEMENTED**; Sprint 2I classification/evidence behavior is **VERIFIED** locally. | Bounded escalation classification and evidence packaging exist. | **NOT ESTABLISHED** as an operational human-review workflow or production case record. |
| Review evidence | Review models define reviewer route/ID, authority and delegation references, policy/refusal evidence, audit references, requested/outcome state, reasons, timestamps, and evidence hash. | **IMPLEMENTED** as non-authorizing review artifacts. | Bounded review-record handling exists. | **NOT ESTABLISHED** as real reviewer identity or institutional review data. |
| Override evidence | Override models define subject, declarant, emergency type, requested action, authority references, policy version, expiry, effective scope, upstream evidence hashes, audit references, and decision metadata. | **IMPLEMENTED** as bounded non-executing override artifacts. | Bounded override decision handling exists. | **NOT ESTABLISHED** as production emergency-event or authority data. |
| Audit records | `AuditRecord` defines event type, actor ID, reason, details object, occurrence time, optional request/envelope/authority/token references, and before/after state. | **IMPLEMENTED** at bounded audit seams. | In-process audit append/hash-chain behavior exists and is test-backed in current implementation evidence. | **NOT ESTABLISHED** as durable production audit storage or real-user audit history. |
| Runtime-state evidence | Runtime traceability defines state-transition and recovery/halt evidence artifacts and references. | **IMPLEMENTED** at bounded runtime-state seams. | Bounded state validation/evidence handling exists. | **NOT ESTABLISHED** as production session telemetry. |
| Execution-eligibility evidence | `ExecutionRequest` / `ExecutionEvidence` define actor/action/resource, authority/refusal/escalation/review/override evidence references/hashes, runtime decision reference, audit references, constraints, request time, and decision metadata. | **VERIFIED** for the bounded Sprint 2M non-executing eligibility foundation. | Evidence-only eligibility processing exists. | **NOT ESTABLISHED** as production execution or external-system activity. |
| Configuration values | `RuntimeConfig` defines contract paths, policy/invariant versions, security profile ID, and audit sink ID. | **IMPLEMENTED** as bounded configuration shape / loader evidence. | Configuration loading and validation have repository-local test evidence. | **NOT ESTABLISHED** as deployed environment configuration. |
| Event / database / persistence artifacts | Contracts and schemas define event envelopes, database tables, and repository boundaries; Sprint 1 evidence records in-memory persistence and contract validation. | **DOCUMENTED / SPECIFIED** for schemas; selected repository foundations are **IMPLEMENTED** / **VERIFIED** locally. | In-memory and contract-level persistence/event handling exists. | **NOT ESTABLISHED** as durable production database, event transport, or external storage. |

## 6. Historical personal-data claims

Historical or surrounding PIA-era material may refer to data categories that sound personal, sensitive, biometric, behavioral, clinical, educational, or otherwise regulated. This reconciliation does not promote any such category into a current production fact merely because it appeared in a journal, historical diagram, proposed system description, schema, model name, fixture, or example.

The following present-state classifications apply unless separate evidence establishes otherwise:

| Historical or sensitive-data category | Current disposition |
| --- | --- |
| Names or direct personal identifiers | **NOT ESTABLISHED** as production collection. Current repository fields include technical actor/subject/requester identifiers and an optional identity display label; those definitions do not prove real-world collection. |
| Authentication information | **PARTIALLY SUPPORTED** as technical credential references / verification evidence; production credential collection, secret storage, external IdP integration, and authentication-data retention are **NOT ESTABLISHED**. |
| Behavioral information | **NOT ESTABLISHED** as production collection or profiling. |
| Emotional-state / emotional-signature information | **NOT ESTABLISHED**. Historical terminology is not mapped onto current runtime artifacts. |
| Cognitive-rhythm information | **NOT ESTABLISHED**. |
| Device signatures / device fingerprinting | **NOT ESTABLISHED**. |
| Interaction metadata | **PARTIALLY SUPPORTED** as repository-defined request IDs, timestamps, correlation IDs, actions, resources, outcomes, evidence hashes, and audit metadata; actual production interaction collection is **NOT ESTABLISHED**. |
| Child information | **NOT ESTABLISHED** as production collection. Authority vocabulary such as parent/guardian/caregiver does not itself establish child records. |
| Caregiver information | **NOT ESTABLISHED** as production collection. Current authority categories and reviewer routes are technical categories, not evidence of real caregiver records. |
| School / educational information | **NOT ESTABLISHED**. |
| Clinical information | **NOT ESTABLISHED**. A `clinical` review route label does not establish medical data processing, clinical workflow deployment, or healthcare compliance. |
| Medical / health information | **NOT ESTABLISHED**. |
| Financial information | **NOT ESTABLISHED**. |
| Social Security numbers / government identifiers | **NOT ESTABLISHED**. |
| Precise or coarse location information | **NOT ESTABLISHED**. |
| Biometric information | **NOT ESTABLISHED**. |
| Other sensitive or regulated information | **HOLD** until a specific current field, collection source, purpose, flow, persistence mechanism, and evidence basis are identified. |

## 7. Collection and purpose

A repository field, schema, interface, model, test fixture, historical journal statement, or example is not proof that a live system collects corresponding information.

Where current code defines data-bearing artifacts, their evidence-bounded technical purposes are limited to current governance/runtime functions such as identity resolution, authority resolution, delegation validation, policy evaluation, authorization decisions, refusal, escalation, review, override evidence, audit linkage, runtime-state validation, and execution eligibility.

Those technical purposes do not establish:

- a production collection source;
- a live end-user interface collecting the field;
- a third-party data feed;
- background tracking;
- behavioral or emotional profiling;
- biometric capture;
- clinical intake;
- school-record intake;
- government-record intake;
- marketing or advertising use;
- secondary-use analytics;
- model training on production user data.

All such claims are **NOT ESTABLISHED** unless separately evidenced.

## 8. Storage and persistence

Current repository evidence distinguishes multiple layers that must not be collapsed:

| Storage layer | Current disposition |
| --- | --- |
| In-memory repositories / test adapters | **IMPLEMENTED** and locally test-backed for bounded repository behavior. |
| Database schema definitions | **DOCUMENTED / SPECIFIED**. Schema existence does not prove a live database. |
| Persistence interfaces / adapters | **IMPLEMENTED** for bounded repository abstractions where current evidence identifies them. |
| Durable production storage | **NOT ESTABLISHED**. |
| Encrypted production storage | **NOT ESTABLISHED**. |
| External cloud storage | **NOT ESTABLISHED**. |
| Production backup / replica storage | **NOT ESTABLISHED**. |

The merged SSP reconciliation already withholds claims of durable encrypted storage, cloud deployment, production backups, and externally immutable logging. This PIA reconciliation does not change those dispositions.

## 9. Retention and deletion

Current inspected evidence does not establish an institutionally governed production retention/deletion schedule for user or operational data.

Accordingly:

- retention duration: **NOT ESTABLISHED**;
- user-record deletion workflow: **NOT ESTABLISHED**;
- legal hold policy: **NOT ESTABLISHED**;
- archive duration: **NOT ESTABLISHED**;
- backup retention: **NOT ESTABLISHED**;
- lifecycle disposal / secure destruction: **NOT ESTABLISHED**;
- verified deletion from production replicas or backups: **NOT ESTABLISHED**.

Lifecycle states inside individual technical models, such as `archived`, `revoked`, `expired`, or repository-history entries, do not by themselves establish privacy-record retention or deletion policy.

## 10. Access, authority, and consent

Current EchoAuth architecture preserves separate concepts for identity, authority, authorization, data-bearing evidence, runtime eligibility, and execution.

That separation supports bounded governance correspondence but does not create privacy consent.

```text
IDENTITY != AUTHORITY
AUTHORITY != AUTHORIZATION
AUTHORIZATION != DATA ACCESS POLICY
AUTHORIZATION != CONSENT
PERMISSION != EXECUTION
```

Current authority controls may help constrain who can produce or consume governance artifacts at bounded seams. They must not be generalized into a complete privacy access-control program, consent-management system, legal representative determination, or data-subject-rights workflow.

**Consent collection, consent withdrawal, consent provenance, purpose-specific consent, parental consent, guardian consent, and consent-to-secondary-use are NOT ESTABLISHED unless separately implemented and evidenced.**

## 11. Sharing and external disclosure

No production sharing or disclosure is inferred from repository architecture, historical journals, field names, reviewer categories, or integration contracts.

Current inspected evidence does not establish production disclosure of user or system data to:

- schools or educational institutions;
- clinics, hospitals, clinicians, or health systems;
- government agencies;
- cloud providers as deployed processors;
- third-party AI systems;
- external institutions;
- vendors, subprocessors, or data brokers;
- advertisers or marketing systems.

The existence of contract, event, API, or notification interfaces is **DOCUMENTED / SPECIFIED** or **IMPLEMENTED** only at the exact bounded seam supported by repository evidence. It is not proof of an active external transfer.

Production sharing / disclosure status: **NOT ESTABLISHED**.

## 12. Privacy / security relationship

The merged SSP reconciliation may be used as evidence for bounded security/governance implementation facts, but security and privacy claims remain distinct.

```text
SECURITY CONTROL != PRIVACY COMPLIANCE
AUTHORIZATION CONTROL != CONSENT
AUDITABILITY != LAWFULNESS
DATA MINIMIZATION CLAIM != VERIFIED MINIMIZATION
SECURE STORAGE CLAIM != VERIFIED RETENTION OR DELETION
```

A security control can exist without establishing purpose limitation, notice, consent, retention, deletion, access rights, legal basis, cross-border transfer status, or regulatory applicability.

## 13. Regulatory and legal status

This reconciliation does not establish, imply, certify, or determine applicability or compliance for:

- the U.S. Privacy Act;
- the E-Government Act;
- HIPAA;
- COPPA;
- FERPA;
- GDPR;
- CCPA / CPRA;
- the NIST Privacy Framework;
- state privacy statutes;
- federal agency privacy requirements;
- clinical, educational, child-safety, biometric, financial, or other sector-specific privacy law.

Repository terminology, technical controls, historical PIA formatting, or data-field definitions are not legal determinations.

Any future legal/applicability determination requires a separate authorized lane and appropriate evidence and expertise.

## 14. Institutional evidence rules

```text
HISTORICAL DATA CLAIM != CURRENT DATA INVENTORY
SCHEMA FIELD != COLLECTED DATA
CODE SUPPORT != PRODUCTION PROCESSING
TEST DATA != REAL USER DATA
DOCUMENTED RETENTION != VERIFIED RETENTION
AUTHORIZATION != CONSENT
PRIVACY MAPPING != LEGAL COMPLIANCE
PIA DOCUMENT != PRIVACY CERTIFICATION OR SYSTEM AUTHORIZATION
```

Additional existing rules remain in force:

```text
HISTORICAL DESIGN != CURRENT IMPLEMENTATION
DOCUMENTED CONTROL != IMPLEMENTED CONTROL
IMPLEMENTED CONTROL != VERIFIED CONTROL
PROPOSED INTEGRATION != DEPLOYED INTEGRATION
INFERENCE != EVIDENCE
CAPABILITY != AUTHORITY
```

## 15. Existing governance posture preserved

The existing independent-review posture remains unchanged:

```text
SAL-11 = PASS
SAL-12 = PASS
SAL-13 = HOLD / PARTIAL
SAL-14 = PASS
SAL-15 = HOLD / PARTIAL
SAL-9  = HOLD — 3 PASS / 2 HOLD-PARTIAL / 0 FAIL
```

This PIA reconciliation does not advance, reduce, reinterpret, or close any existing HOLD or deferred runtime boundary.

In particular:

```text
PIA RECONCILIATION != SAL-9 ADVANCE
PIA RECONCILIATION != PRODUCTION DATA INVENTORY
PIA RECONCILIATION != PRIVACY COMPLIANCE
PIA RECONCILIATION != CONSENT AUTHORITY
PIA RECONCILIATION != DEPLOYMENT
```

## 16. Non-authorized actions

This reconciliation does not authorize:

- runtime-code modification;
- test modification;
- schema or database modification;
- configuration or dependency modification;
- authorization-logic modification;
- consent logic;
- deletion or retention implementation;
- privacy-control implementation;
- collection or inspection of actual user records merely to complete documentation;
- inference of deployment from schemas, fixtures, models, examples, or journals;
- legal or regulatory compliance claims;
- historical-journal modification;
- combination with AI Assurance or DFD reconciliation without a separate N.B.C. decision.

## 17. Verification conditions for this change

This change remains within authority only if:

1. exactly one new documentation file changes;
2. no runtime, tests, schemas, database structures, configuration, dependencies, authorization logic, or historical journals change;
3. every present-state data-processing claim is supported by current repository evidence;
4. historical collection, storage, retention, sharing, and sensitive-data claims remain historical or **NOT ESTABLISHED** unless independently supported;
5. no production-data claim is inferred from code, schemas, models, tests, or repository structure alone;
6. no privacy compliance, certification, legal determination, consent authority, production deployment, or external authority is created;
7. `SAL-9 = HOLD — 3 PASS / 2 HOLD-PARTIAL / 0 FAIL` remains unchanged.

## Target review disposition

```text
PASS — PIA CURRENT STATE RECONCILED /
DATA AND PRIVACY CLAIMS EVIDENCE-BOUNDED /
NO PRIVACY COMPLIANCE, PRODUCTION-DATA PROCESSING, CONSENT AUTHORITY,
DEPLOYMENT, OR EXTERNAL AUTHORITY ESTABLISHED
```

That target disposition is not self-executing. Separate independent review and a separate N.B.C. merge decision are required before merge.