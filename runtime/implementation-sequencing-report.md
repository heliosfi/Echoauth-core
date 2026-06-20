# Implementation Sequencing Report

# Evidence Base

This report uses only repository artifacts:

- `runtime/final-implementation-readiness-report.md`
- `runtime/final-repository-readiness-assessment.md`
- `runtime/coverage-report.md`
- `runtime/dependency-graph.md`
- `runtime/traceability-matrix.md`
- `contracts/service-contracts.yaml`
- `contracts/integration-contracts.yaml`
- `contracts/ambiguities.md`
- `contracts/decision-log.md`
- `api/openapi.yaml`
- `contracts/protobuf/echoauth.proto`
- `schemas/*.schema.json`
- `events/event-catalog.yaml`
- `events/event-envelope.schema.json`
- `database/schema.sql`
- `src/echoauth/*`

# 1. Exact Component Build Order

| Order | Component | Reason |
| --- | --- | --- |
| 1 | Contract validation harness | All later work consumes OpenAPI, JSON Schema, protobuf, YAML contracts, event schemas, and database schema. |
| 2 | Canonical data utilities | `contracts/service-contracts.yaml` defines `canonical_json_object`, `string_reference_list`, and `validation_error_list`; downstream services depend on canonical serialization and hashing behavior. |
| 3 | Configuration loader | `src/echoauth/config.py` defines contract paths and runtime configuration shape consumed by adapters. |
| 4 | Repository adapters | `database/schema.sql` is required by authority, delegation, policy, runtime state, audit, event, and notification persistence boundaries. |
| 5 | Event bus adapter | `AuditService` and `NotificationService` depend on `EventBus` per `runtime/dependency-graph.md`. |
| 6 | Audit append adapter | Runtime and downstream service work require audit persistence and event emission. |
| 7 | Identity service adapter | First runtime dependency in `contracts/service-contracts.yaml`; required before authority resolution. |
| 8 | Authority registry and revocation repositories | `AuthorityService` consumes authority and revocation storage boundaries. |
| 9 | Authority service adapter | Required before delegation, policy, envelope, and token workflows can be composed. |
| 10 | Delegation repository and service adapter | Required before policy and envelope workflows that reference delegation IDs. |
| 11 | Policy registry and policy service adapter | Required before invariant/envelope authorization progression. |
| 12 | Refusal service adapter | Runtime refusal path must exist before pilot execution paths are exposed. |
| 13 | Invariant service adapter | Required before envelope creation and token issuance. |
| 14 | Escalation and halt service adapters | Required for non-permit terminal and non-terminal control paths. |
| 15 | Runtime envelope service adapter | Produces envelope records consumed by token and claim components. |
| 16 | Execution token service adapter | Produces execution tokens consumed by execution claims. |
| 17 | Execution claim service adapter | Binds executor claims to issued tokens. |
| 18 | Recovery service adapter | Depends on runtime state persistence and halt/refusal states. |
| 19 | Emergency override service adapter | Deferred until core runtime control path and audit/event boundaries exist. |
| 20 | Notification service adapter | Depends on event bus and recipient delivery contracts. |
| 21 | Runtime orchestrator adapter | Composes identity, authority, delegation, policy, invariant, envelope, token, claim, halt, recovery, notification, and audit dependencies. |
| 22 | API adapter | Binds `api/openapi.yaml` operations to runtime/service interfaces. |
| 23 | Protobuf adapter | Binds `contracts/protobuf/echoauth.proto` to runtime models and service interfaces. |
| 24 | End-to-end deterministic processing tests | Verifies state names, terminal states, canonical data handling, idempotency, nonce uniqueness, and audit/event correlation. |

# 2. Critical Path Dependencies

| Critical Path | Dependency Chain |
| --- | --- |
| Runtime request acceptance | Contract validation harness -> canonical data utilities -> configuration loader -> repository adapters -> audit append adapter -> runtime orchestrator adapter -> API adapter |
| Authorization path | Identity service adapter -> authority registry/revocation repositories -> authority service adapter -> delegation service adapter -> policy service adapter -> invariant service adapter |
| Execution path | Authority service adapter -> delegation service adapter -> policy service adapter -> invariant service adapter -> runtime envelope service adapter -> execution token service adapter -> execution claim service adapter |
| Audit and event path | Repository adapters -> event bus adapter -> audit append adapter -> notification service adapter |
| Recovery path | Repository adapters -> runtime state repository -> halt service adapter -> recovery service adapter |

# 3. Highest Leverage Components

| Component | Downstream Work Unblocked |
| --- | --- |
| Contract validation harness | All contract-consuming implementation, tests, API binding, protobuf binding, schema validation. |
| Canonical data utilities | Payload/context/evidence/scope/facts/rules/details hashing and serialization across services. |
| Repository adapters | Authority, delegation, policy, runtime state, audit, event, and notification persistence. |
| Event bus adapter | Audit publication, notification delivery, event-driven integration tests. |
| Audit append adapter | Runtime acceptance, refusal, halt, token, claim, and compliance evidence paths. |
| Authority service adapter | Delegation, policy, envelope, token, execution, and runtime orchestration paths. |
| Runtime envelope service adapter | Token issuance and execution claim flow. |
| Runtime orchestrator adapter | API, protobuf, integration testing, pilot workflows. |

# 4. Parallel Build Groups

| Parallel Group | Components |
| --- | --- |
| Contract tooling | Contract validation harness; protobuf syntax validation; OpenAPI structure validation; JSON Schema validation. |
| Persistence foundations | Repository adapters; canonical JSON text enforcement; database migration/test harness. |
| Integration foundations | Event bus adapter; notification transport shell; API adapter shell; protobuf adapter shell. |
| Independent service shells | Identity service adapter; policy registry adapter; authority registry adapter; revocation repository; delegation repository. |
| Control path shells | Refusal service adapter; halt service adapter; recovery service adapter; emergency override service adapter. |
| Execution shells | Runtime envelope service adapter; execution token service adapter; execution claim service adapter, after authority/policy/invariant interfaces are available. |

# 5. Deferred Components

| Component | Deferral Reason | Resume Condition |
| --- | --- | --- |
| Emergency override service adapter | `runtime/coverage-report.md` lists it as an abstract override boundary; it should follow core audit, event, authority, refusal, halt, and recovery boundaries. | Core runtime control path, audit append, and halt/recovery adapters exist. |
| Notification delivery implementation | `runtime/dependency-graph.md` shows notification depends on event bus; delivery details are integration boundary work. | Event bus adapter and notification contract tests exist. |
| Protobuf adapter | It is not required for HTTP-first runtime pilot unless external protobuf integration is in pilot scope. | Runtime model mapping and canonical `Struct` handling tests exist. |
| Domain-specific nested schema validation | `contracts/ambiguities.md` and `runtime/coverage-report.md` document that nested business schemas are not generated. | Future specifications define nested domain schemas. |
| Production hardening for database-native JSON validation | `database/schema.sql` specifies canonical JSON text but no engine-specific validation function. | Selected database adapter documents engine-specific enforcement. |

# 6. Minimum Viable Runtime

MVR is the smallest implementation that can accept contract-shaped requests,
persist required records, emit audit/event records, and compose runtime service
interfaces without implementing deferred integrations.

| Required Component | Evidence |
| --- | --- |
| Contract validation harness | `api/openapi.yaml`; `schemas/*.json`; `contracts/service-contracts.yaml`; `contracts/integration-contracts.yaml`; `contracts/protobuf/echoauth.proto` |
| Canonical data utilities | `contracts/service-contracts.yaml`; `contracts/ambiguities.md`; `contracts/decision-log.md`; `schemas/common.schema.json` |
| Configuration loader | `src/echoauth/config.py` |
| Repository adapters | `src/echoauth/repositories.py`; `database/schema.sql` |
| Event bus adapter | `src/echoauth/events.py`; `events/event-envelope.schema.json`; `events/event-catalog.yaml` |
| Audit append adapter | `src/echoauth/interfaces.py`; `src/echoauth/audit/logging.py`; `schemas/audit-record.schema.json` |
| Identity, authority, delegation, policy, invariant service adapters | `contracts/service-contracts.yaml`; `src/echoauth/interfaces.py`; `runtime/traceability-matrix.md` |
| Envelope and token adapters | `schemas/runtime-envelope.schema.json`; `schemas/execution-token.schema.json`; `src/echoauth/execution/controls.py` |
| Runtime orchestrator adapter | `src/echoauth/main.py`; `runtime/dependency-graph.md` |

# 7. Minimum Viable Pilot

MVPilot extends MVR with pilot-facing integration surfaces and operational
criteria already reflected in repository artifacts.

| Required Component | Evidence |
| --- | --- |
| MVR components | Section 6. |
| API adapter | `api/openapi.yaml`; `contracts/integration-contracts.yaml` |
| Notification service adapter | `src/echoauth/interfaces.py`; `events/event-catalog.yaml`; `contracts/integration-contracts.yaml` |
| Refusal and halt adapters | `src/echoauth/interfaces.py`; `contracts/service-contracts.yaml`; `runtime/dependency-graph.md` |
| Recovery adapter | `src/echoauth/interfaces.py`; `database/schema.sql`; `runtime/traceability-matrix.md` |
| Pilot test harness | `runtime/final-implementation-readiness-report.md`; `runtime/coverage-report.md` |
| Deterministic processing tests | `specs/runtime-state-machine.md`; `contracts/service-contracts.yaml`; `contracts/decision-log.md` |

# 8. Estimated Engineering Phases

| Phase | Scope | Components | Complexity |
| --- | --- | --- | --- |
| Phase 1 | Contract and validation foundation | Contract validation harness; canonical data utilities; configuration loader | Medium |
| Phase 2 | Persistence and event foundation | Repository adapters; event bus adapter; audit append adapter | High |
| Phase 3 | Core governance service adapters | Identity; authority; delegation; policy; refusal; invariant | High |
| Phase 4 | Runtime execution envelope | Envelope; token; claim; halt; recovery | High |
| Phase 5 | Integration adapters | Runtime orchestrator; API adapter; protobuf adapter; notification adapter | High |
| Phase 6 | Pilot hardening | Deterministic tests; audit/event correlation tests; readiness criteria validation | Medium |

# Component Sequencing Detail

| Component | Purpose | Inputs | Outputs | Contracts Consumed | Contracts Produced | Dependencies | Complexity | Build Priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Contract validation harness | Validate repository contracts before implementation. | OpenAPI, JSON Schemas, protobuf, YAML contracts, database schema. | Validation results. | `api/openapi.yaml`; `schemas/*.json`; `contracts/*.yaml`; `events/*.json`; `events/event-catalog.yaml`; `database/schema.sql`; `contracts/protobuf/echoauth.proto` | Test/validation reports. | None. | Medium | P0 |
| Canonical data utilities | Apply canonical object/list contract handling. | `CanonicalJsonObject`; `StringReferenceList`; `ValidationErrorList`. | Canonical serialized values and hashes. | `schemas/common.schema.json`; `contracts/ambiguities.md`; `contracts/decision-log.md`; `contracts/service-contracts.yaml` | Canonical values for service/repository adapters. | Contract validation harness. | Medium | P0 |
| Configuration loader | Load contract paths and runtime configuration shape. | Contract paths; policy version; invariant version; security profile; audit sink. | Runtime config object. | `src/echoauth/config.py`; `contracts/integration-contracts.yaml` | Runtime configuration instance. | Contract validation harness. | Low | P0 |
| Repository adapters | Persist and retrieve runtime records. | Contract-shaped records. | Stored/retrieved records. | `src/echoauth/repositories.py`; `database/schema.sql`; `contracts/integration-contracts.yaml` | Repository implementations. | Canonical data utilities; configuration loader. | High | P0 |
| Event bus adapter | Publish and subscribe event envelopes. | `EventEnvelope`; event type; subscriber ID. | Delivery state or subscription result. | `src/echoauth/events.py`; `events/event-envelope.schema.json`; `events/event-catalog.yaml` | Event transport implementation. | Canonical data utilities. | Medium | P0 |
| Audit append adapter | Append audit records and persist hash-bound fields. | `AuditRecord`. | `AuditRecordResult`. | `schemas/audit-record.schema.json`; `database/schema.sql`; `events/event-catalog.yaml`; `contracts/service-contracts.yaml` | Audit append implementation. | Repository adapters; event bus adapter. | High | P0 |
| Identity service adapter | Resolve actor identity. | `IdentityResolutionRequest`. | `IdentityVerdict`. | `contracts/service-contracts.yaml`; `api/openapi.yaml`; `contracts/protobuf/echoauth.proto`; `schemas/common.schema.json` | Identity service implementation. | Canonical data utilities; audit append adapter. | Medium | P1 |
| Authority registry repository | Store authority records. | Authority record data. | Authority records. | `database/schema.sql`; `runtime/traceability-matrix.md` | Repository implementation. | Repository adapters. | Medium | P1 |
| Revocation repository | Store authority revocations. | Revocation records. | Revocation records. | `database/schema.sql`; `runtime/traceability-matrix.md` | Repository implementation. | Repository adapters. | Medium | P1 |
| Authority service adapter | Resolve authority verdicts. | `AuthorityResolutionRequest`. | `AuthorityVerdict`. | `schemas/authority-resolution.schema.json`; `contracts/service-contracts.yaml`; `contracts/protobuf/echoauth.proto` | Authority service implementation. | Identity service adapter; authority registry repository; revocation repository; audit append adapter. | High | P1 |
| Delegation repository | Store delegation records. | Delegation records. | Delegation records. | `database/schema.sql`; `runtime/traceability-matrix.md` | Repository implementation. | Repository adapters. | Medium | P1 |
| Delegation service adapter | Validate delegation. | `DelegationValidationRequest`. | `DelegationValidationResult`. | `contracts/service-contracts.yaml`; `contracts/ambiguities.md`; `contracts/decision-log.md` | Delegation service implementation. | Authority service adapter; delegation repository; audit append adapter. | High | P1 |
| Policy registry repository | Store policy records and policy decisions. | Policy artifacts; policy decisions. | Stored policy records and decisions. | `database/schema.sql`; `runtime/traceability-matrix.md` | Repository implementation. | Repository adapters. | Medium | P1 |
| Policy service adapter | Evaluate policy decisions. | `PolicyEvaluationRequest`. | `PolicyDecision`. | `contracts/service-contracts.yaml`; `contracts/ambiguities.md`; `contracts/decision-log.md` | Policy service implementation. | Authority service adapter; delegation service adapter; policy registry repository; audit append adapter. | High | P1 |
| Refusal service adapter | Handle refusal path. | Refusal request object. | Refusal result object. | `contracts/service-contracts.yaml`; `contracts/ambiguities.md`; `runtime/traceability-matrix.md` | Refusal service implementation. | Policy service adapter; audit append adapter. | Medium | P1 |
| Invariant service adapter | Validate invariants. | `InvariantValidationRequest`. | `InvariantResult`. | `contracts/service-contracts.yaml`; `contracts/ambiguities.md`; `database/schema.sql` | Invariant service implementation. | Policy service adapter; audit append adapter. | High | P1 |
| Escalation service adapter | Handle escalation path. | Escalation request object. | Escalation result object. | `contracts/service-contracts.yaml`; `contracts/ambiguities.md`; `runtime/traceability-matrix.md` | Escalation service implementation. | Authority service adapter; policy service adapter; audit append adapter. | Medium | P2 |
| Halt service adapter | Halt runtime requests or sessions. | Halt request object. | Halt result object. | `contracts/service-contracts.yaml`; `events/event-catalog.yaml`; `runtime/traceability-matrix.md` | Halt service implementation. | Audit append adapter; event bus adapter; runtime state repository. | Medium | P2 |
| Runtime state repository | Persist runtime state/session records. | Runtime state records. | Runtime state records. | `database/schema.sql`; `runtime/traceability-matrix.md` | Repository implementation. | Repository adapters. | Medium | P2 |
| Runtime envelope service adapter | Create runtime envelopes. | `RuntimeEnvelope`. | `RuntimeEnvelopeResult`. | `schemas/runtime-envelope.schema.json`; `contracts/service-contracts.yaml`; `contracts/protobuf/echoauth.proto` | Envelope service implementation. | Authority, delegation, policy, invariant services; audit append adapter. | High | P2 |
| Execution token service adapter | Issue execution tokens. | `ExecutionToken`. | `ExecutionTokenResult`. | `schemas/execution-token.schema.json`; `contracts/service-contracts.yaml`; `contracts/protobuf/echoauth.proto` | Token service implementation. | Runtime envelope service adapter; audit append adapter. | High | P2 |
| Execution claim service adapter | Claim execution tokens. | `ExecutionClaim`. | `ExecutionClaimResult`. | `contracts/service-contracts.yaml`; `contracts/ambiguities.md` | Claim service implementation. | Execution token service adapter; audit append adapter. | Medium | P2 |
| Recovery service adapter | Recover from halted/failed runtime states. | Recovery request object. | Recovery result object. | `contracts/service-contracts.yaml`; `database/schema.sql`; `runtime/traceability-matrix.md` | Recovery service implementation. | Halt service adapter; runtime state repository; audit append adapter. | Medium | P2 |
| Emergency override service adapter | Handle emergency override control path. | Override request object. | Override result object. | `contracts/service-contracts.yaml`; `contracts/ambiguities.md`; `runtime/traceability-matrix.md` | Override service implementation. | Core runtime, audit, halt, recovery. | High | P3 |
| Notification service adapter | Send or enqueue notifications. | Notification request object; event envelope. | Notification result object. | `contracts/integration-contracts.yaml`; `events/event-catalog.yaml`; `database/schema.sql` | Notification implementation. | Event bus adapter; repository adapters. | Medium | P3 |
| Runtime orchestrator adapter | Compose runtime services behind `RuntimeService`. | `EchoAuthRequest`. | `EchoAuthResult`. | `contracts/service-contracts.yaml`; `src/echoauth/main.py`; `runtime/dependency-graph.md` | Runtime implementation. | Identity, authority, delegation, policy, invariant, envelope, token, claim, audit; halt/refusal paths. | High | P3 |
| API adapter | Bind OpenAPI operations to runtime/services. | HTTP requests. | HTTP responses. | `api/openapi.yaml`; `contracts/integration-contracts.yaml` | API implementation. | Runtime orchestrator adapter; contract validation harness. | Medium | P3 |
| Protobuf adapter | Bind protobuf messages to runtime models. | Protobuf messages. | Runtime models or protobuf responses. | `contracts/protobuf/echoauth.proto`; `contracts/integration-contracts.yaml`; `src/echoauth/models.py` | Protobuf mapping layer. | Runtime models; canonical data utilities. | Medium | P3 |
| Deterministic processing tests | Verify deterministic contract behavior. | Contract fixtures and runtime adapters. | Test results. | `specs/runtime-state-machine.md`; `contracts/service-contracts.yaml`; `contracts/decision-log.md`; `runtime/traceability-matrix.md` | Test evidence. | MVR components. | Medium | P0 |

# Sprint 1 Plan

| Workstream | Deliverables | Exit Criteria |
| --- | --- | --- |
| Contract validation | Validation harness for JSON Schema, OpenAPI structure, protobuf syntax, YAML syntax, and database schema readability. | Contract checks run locally and fail on schema/contract syntax errors. |
| Canonical data | Canonical object/list helpers for `CanonicalJsonObject`, `StringReferenceList`, and `ValidationErrorList`. | Canonical serialization and hash fixtures pass for representative contract-shaped values. |
| Configuration | Runtime configuration loader based on `src/echoauth/config.py`. | Contract paths resolve and configuration values can be injected into adapters. |
| Persistence foundation | Repository adapter base and schema-backed persistence test harness. | Repository interfaces can persist/retrieve records with canonical JSON text handling. |
| Event foundation | Event bus adapter shell and event envelope validation. | Event envelopes validate against `events/event-envelope.schema.json` and event types map to `events/event-catalog.yaml`. |

# Sprint 2 Plan

| Workstream | Deliverables | Exit Criteria |
| --- | --- | --- |
| Audit | Audit append adapter and audit repository implementation. | `AuditRecord` input persists required fields and emits audit events. |
| Identity and authority | Identity adapter, authority registry repository, revocation repository, authority adapter. | Identity and authority interfaces accept/return contract-shaped records. |
| Delegation and policy | Delegation repository/service, policy registry/service. | Delegation and policy services consume authority outputs and produce contract-shaped decisions. |
| Refusal and invariants | Refusal adapter and invariant adapter. | Non-permit paths and invariant results are contract-shaped and audited. |
| Runtime state | Runtime state repository. | Runtime state records persist with contract state names. |

# Sprint 3 Plan

| Workstream | Deliverables | Exit Criteria |
| --- | --- | --- |
| Envelope and token | Runtime envelope adapter, execution token adapter, execution claim adapter. | Envelope, token, and claim records follow schemas and service terminal states. |
| Halt and recovery | Halt adapter and recovery adapter. | Halt/recovery requests persist state and audit/event evidence. |
| Runtime composition | Runtime orchestrator adapter. | `EchoAuthRuntime` composes injected dependencies without bypassing audit/event boundaries. |
| API integration | OpenAPI operation bindings. | API operations call runtime/service interfaces and return contract-shaped responses. |
| Pilot integration | Notification adapter shell and pilot deterministic tests. | Pilot workflows satisfy MVR and MVPilot readiness criteria. |

# Pilot Readiness Criteria

| Criterion | Evidence Artifact |
| --- | --- |
| MVR components are implemented and tested. | Section 6; `runtime/coverage-report.md`. |
| API adapter exposes OpenAPI operations used by pilot workflows. | `api/openapi.yaml`; `contracts/integration-contracts.yaml`. |
| Audit append and event publication are active for runtime decisions and failures. | `schemas/audit-record.schema.json`; `events/event-catalog.yaml`; `database/schema.sql`. |
| Refusal, halt, and recovery paths exist as contract-shaped service adapters. | `contracts/service-contracts.yaml`; `runtime/dependency-graph.md`. |
| Canonical object/list handling is enforced at boundaries. | `schemas/common.schema.json`; `contracts/ambiguities.md`; `contracts/decision-log.md`. |
| No nested domain behavior is inferred without future specifications. | `runtime/final-repository-readiness-assessment.md`; `runtime/coverage-report.md`. |

# Production Readiness Criteria

| Criterion | Evidence Artifact |
| --- | --- |
| All MVR and MVPilot criteria pass in automated validation. | This report; `runtime/final-implementation-readiness-report.md`. |
| Persistence adapters enforce uniqueness, canonical JSON text, idempotency keys, nonces, and audit/event required fields. | `database/schema.sql`; `contracts/integration-contracts.yaml`. |
| Audit chain behavior is implemented and validated against audit specs and schema contracts. | `specs/audit-chain.md`; `specs/audit-log-spec.md`; `schemas/audit-record.schema.json`; `database/schema.sql`. |
| API, event bus, persistence, and protobuf integration controls are implemented. | `contracts/integration-contracts.yaml`. |
| Runtime dependency graph is implemented with no missing required dependency. | `runtime/dependency-graph.md`; `src/echoauth/wiring.py`. |
| Deterministic processing tests cover state names, terminal states, canonical data, idempotency, nonce uniqueness, and audit/event correlation. | `contracts/service-contracts.yaml`; `runtime/traceability-matrix.md`; `contracts/decision-log.md`. |
| Documented exceptions are either accepted for production scope or resolved by future specification updates. | `runtime/final-repository-readiness-assessment.md`; `contracts/ambiguities.md`. |
