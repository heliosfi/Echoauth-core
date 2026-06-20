# First Engineering Sprint Package

# Evidence Base

This work package is derived from:

- `runtime/implementation-sequencing-report.md`
- `runtime/final-implementation-readiness-report.md`
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
- `src/echoauth/config.py`
- `src/echoauth/repositories.py`
- `src/echoauth/events.py`

# 1. Sprint Objective

Establish the implementation foundation required before EchoAuth runtime
services are built:

- validate generated contracts,
- implement canonical data handling,
- load runtime configuration,
- create persistence foundation adapters,
- create event bus foundation adapters,
- and add tests that prevent downstream services from consuming invalid
  contracts or non-canonical data.

Sprint 1 must not implement governance decisions, authorization behavior,
policy behavior, audit-chain behavior, execution behavior, or nested
domain-specific business validation.

# 2. Deliverables

| Deliverable | Description | Evidence Source |
| --- | --- | --- |
| Contract validation harness | Validates JSON Schemas, OpenAPI structure, protobuf syntax, YAML syntax, event schemas, and database schema readability. | `runtime/implementation-sequencing-report.md`; `api/openapi.yaml`; `schemas/*.json`; `contracts/*.yaml`; `events/*.json`; `database/schema.sql`; `contracts/protobuf/echoauth.proto` |
| Canonical data utilities | Provides canonical handling for `CanonicalJsonObject`, `StringReferenceList`, and `ValidationErrorList`. | `contracts/service-contracts.yaml`; `contracts/ambiguities.md`; `contracts/decision-log.md`; `schemas/common.schema.json` |
| Configuration loader | Loads `RuntimeConfig` and contract paths from repository-defined structure. | `src/echoauth/config.py`; `contracts/integration-contracts.yaml` |
| Repository adapter foundation | Provides concrete base persistence adapter behavior for repository interfaces without service business logic. | `src/echoauth/repositories.py`; `database/schema.sql`; `contracts/integration-contracts.yaml` |
| Event bus adapter foundation | Provides event envelope validation and event type catalog mapping. | `src/echoauth/events.py`; `events/event-envelope.schema.json`; `events/event-catalog.yaml` |
| Sprint 1 test suite | Unit and integration tests for all Sprint 1 deliverables. | `runtime/implementation-sequencing-report.md` |

# 3. Acceptance Criteria

| Criterion | Required Result |
| --- | --- |
| Contract validation harness exists. | One command validates JSON Schema files, OpenAPI structure, YAML files, protobuf syntax when tooling is available, event schemas, and database schema readability. |
| Canonical data helpers exist. | Helpers accept only contract-supported data classes: canonical JSON objects, string reference lists, and validation error lists. |
| Canonical serialization is deterministic. | Reordered equivalent JSON objects produce the same canonical representation and hash. |
| Runtime config can be loaded. | Contract paths resolve relative to repository root and required runtime configuration fields are present. |
| Repository foundation can persist and retrieve records. | Concrete test adapter stores and retrieves contract-shaped records while preserving canonical JSON text. |
| Event foundation validates envelopes. | Event envelopes validate required fields and event types map to `events/event-catalog.yaml`. |
| No governance behavior is added. | Sprint 1 code does not permit, refuse, authorize, delegate, evaluate policy, validate invariants, issue tokens, or execute commands. |

# 4. Repository Files To Create

| File | Purpose |
| --- | --- |
| `src/echoauth/contracts/__init__.py` | Contract validation package export. |
| `src/echoauth/contracts/validation.py` | Contract validation harness. |
| `src/echoauth/canonical.py` | Canonical object/list serialization and hashing utilities. |
| `src/echoauth/config_loader.py` | Runtime configuration loading helper based on `RuntimeConfig`. |
| `src/echoauth/persistence/__init__.py` | Persistence adapter package export. |
| `src/echoauth/persistence/base.py` | Concrete repository adapter foundation. |
| `src/echoauth/events_validation.py` | Event envelope and catalog validation helpers. |
| `tests/test_contract_validation.py` | Unit tests for contract validation harness. |
| `tests/test_canonical.py` | Unit tests for canonical data utilities. |
| `tests/test_config_loader.py` | Unit tests for configuration loading. |
| `tests/test_persistence_base.py` | Unit tests for repository adapter foundation. |
| `tests/test_events_validation.py` | Unit tests for event validation helpers. |
| `tests/integration/test_sprint1_contracts.py` | Integration tests over repository contract artifacts. |
| `tests/integration/test_sprint1_persistence_events.py` | Integration tests covering persistence and event foundations together. |

# 5. Repository Files To Modify

| File | Modification |
| --- | --- |
| `src/echoauth/__init__.py` | Export Sprint 1 foundation modules only if they are stable public runtime APIs. |
| `src/echoauth/config.py` | Add loader-facing helpers only if they preserve the existing dataclass contract. |
| `src/echoauth/repositories.py` | Add no business logic; modify only if abstract base interfaces require minor typing alignment. |
| `src/echoauth/events.py` | Add no transport behavior; modify only if event validation helpers need shared types. |
| `pyproject.toml` or existing test configuration file, if present | Register test paths and dependencies if the repository already uses project-level test configuration. |

# 6. Unit Tests Required

| Test Area | Required Tests |
| --- | --- |
| Contract validation | JSON files parse; required schema files exist; OpenAPI file exists and has top-level `openapi`, `paths`, and `components`; service and integration contract files exist; event catalog and event envelope exist; database schema file exists. |
| Canonical JSON object | Equivalent objects with different key order serialize identically; non-object values are rejected for canonical object helpers; hash output is stable. |
| String reference list | Ordered string reference lists validate; empty or non-string entries fail if helper enforces contract type. |
| Validation error list | Ordered validation error lists validate; non-string entries fail if helper enforces contract type. |
| Configuration loader | Default contract paths resolve; required runtime fields are loaded; missing required fields fail deterministically. |
| Repository foundation | Save/get round trip; missing record handling is deterministic; canonical JSON text is preserved. |
| Event validation | Required envelope fields are enforced; event types resolve against catalog; event payload remains canonical JSON object. |

# 7. Integration Tests Required

| Integration Test | Required Coverage |
| --- | --- |
| Repository artifact validation | Validate all Sprint 1 contract artifacts from repository paths. |
| Canonical data through persistence | Canonical object is serialized, persisted through repository foundation, retrieved, and compared deterministically. |
| Event catalog and envelope | Event envelope validates and event type resolves to the catalog payload schema path. |
| Configuration to validation | Runtime config contract paths feed the validation harness. |
| Persistence and event boundary | Repository foundation and event validation can be used together without service business logic. |

# 8. Expected Outputs

| Output | Description |
| --- | --- |
| Validation command output | Pass/fail report for contract artifacts. |
| Canonical hash fixtures | Stable fixtures proving deterministic serialization and hashing. |
| Config loader result | Runtime configuration object with resolved contract paths. |
| Persistence test records | Test-only records proving repository foundation behavior. |
| Event validation results | Pass/fail results for event envelope and catalog mapping. |
| Test report | Unit and integration test results for Sprint 1 scope. |

# 9. Definition Of Done

Sprint 1 is done when:

- all files listed in "Repository Files To Create" either exist or are
  explicitly documented as unnecessary because equivalent repository files
  already exist,
- all Sprint 1 unit tests pass,
- all Sprint 1 integration tests pass,
- contract validation runs from repository root,
- canonical data helpers are deterministic,
- repository foundation preserves canonical JSON text,
- event validation maps envelopes to the catalog,
- no Sprint 1 code implements governance, authorization, policy, invariant,
  execution, token, emergency override, or notification delivery behavior,
- and the final Sprint 1 result can unblock Sprint 2 audit, identity,
  authority, delegation, policy, refusal, invariant, and runtime state work.

# Sprint 1 Component Work Packages

# Component 1: Contract Validation Harness

| Field | Detail |
| --- | --- |
| Purpose | Validate repository contracts before downstream implementation consumes them. |
| Task breakdown | Create validation module; parse JSON schemas; check OpenAPI structure; check YAML files; check event schema and catalog presence; check database schema readability; check protobuf file presence and syntax when local tooling is available; expose a single testable entrypoint. |
| Estimated effort | Medium. |
| Dependencies | None. |
| Completion criteria | Validation harness runs from repository root and fails deterministically on missing or malformed contract artifacts. |

# Component 2: Canonical Data Utilities

| Field | Detail |
| --- | --- |
| Purpose | Implement contract-level handling for `CanonicalJsonObject`, `StringReferenceList`, and `ValidationErrorList`. |
| Task breakdown | Create canonical serialization helper; create stable hash helper; validate canonical JSON object inputs; validate string reference lists; validate validation error lists; add fixtures proving deterministic output. |
| Estimated effort | Medium. |
| Dependencies | Contract validation harness; `schemas/common.schema.json`; `contracts/ambiguities.md`; `contracts/decision-log.md`. |
| Completion criteria | Equivalent canonical objects produce identical serialized output and hashes; unsupported input types fail deterministically. |

# Component 3: Configuration Loader

| Field | Detail |
| --- | --- |
| Purpose | Load runtime configuration and contract paths required by adapters. |
| Task breakdown | Create loader module; resolve `ContractPaths`; load required runtime fields; validate path existence; expose deterministic failure for missing required configuration; test default path resolution. |
| Estimated effort | Low. |
| Dependencies | Contract validation harness; `src/echoauth/config.py`; `contracts/integration-contracts.yaml`. |
| Completion criteria | Runtime configuration loads with resolved repository contract paths and fails when required fields are absent. |

# Component 4: Repository Adapter Foundation

| Field | Detail |
| --- | --- |
| Purpose | Provide the persistence foundation used by authority, delegation, policy, runtime state, audit, event, and notification adapters. |
| Task breakdown | Create persistence package; implement concrete base adapter suitable for tests; preserve repository interface contract; support save/get; enforce deterministic missing-record behavior; preserve canonical JSON text at persistence boundary; add persistence tests. |
| Estimated effort | High. |
| Dependencies | Canonical data utilities; configuration loader; `src/echoauth/repositories.py`; `database/schema.sql`; `contracts/integration-contracts.yaml`. |
| Completion criteria | Test adapter persists and retrieves contract-shaped records without adding service business logic. |

# Component 5: Event Bus Adapter Foundation

| Field | Detail |
| --- | --- |
| Purpose | Provide event envelope validation and catalog mapping used by audit and notification work. |
| Task breakdown | Create event validation module; validate required envelope fields; validate canonical JSON payload type; load event catalog; map event type to payload schema path; add event validation tests. |
| Estimated effort | Medium. |
| Dependencies | Canonical data utilities; `src/echoauth/events.py`; `events/event-envelope.schema.json`; `events/event-catalog.yaml`. |
| Completion criteria | Event envelopes validate against required fields and event types resolve to catalog entries. |

# Component 6: Sprint 1 Integration Test Harness

| Field | Detail |
| --- | --- |
| Purpose | Prove Sprint 1 foundations work together before Sprint 2 service adapters begin. |
| Task breakdown | Add integration test directory; validate all contract paths through loaded config; persist canonical test record; validate an event envelope using catalog mapping; run tests from repository root. |
| Estimated effort | Medium. |
| Dependencies | Contract validation harness; canonical data utilities; configuration loader; repository adapter foundation; event validation foundation. |
| Completion criteria | Sprint 1 integration tests pass and produce evidence that Sprint 2 can consume configuration, canonical data, persistence, and event foundations. |
