# Sprint 1 Execution Board

# Evidence Base

This board uses only:

- `runtime/first-engineering-sprint-package.md`
- `runtime/implementation-sequencing-report.md`
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

# Sprint 1 Kanban Board

| Order | Task | Status | Critical Path | Blockers | Parallelizable Work | Engineering Effort | Test Effort | Completion Evidence | Review Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Create contract validation package and entrypoint. | Complete | Yes | None. | JSON parsing tests can be drafted in parallel. | Medium | Medium | `src/echoauth/contracts/__init__.py`; `src/echoauth/contracts/validation.py`; validation entrypoint runs from repository root. | Code review confirms no service behavior and all checked artifacts come from repository paths. |
| 2 | Validate JSON schema artifacts. | Complete | Yes | Contract validation entrypoint. | OpenAPI, YAML, database, and protobuf checks can be drafted in parallel. | Low | Medium | Validation result covers `schemas/*.schema.json` and `events/event-envelope.schema.json`. | Test review confirms malformed JSON fails deterministically. |
| 3 | Validate OpenAPI structure. | Complete | Yes | Contract validation entrypoint. | JSON/YAML/database checks can proceed in parallel. | Low | Low | Validation checks `api/openapi.yaml` for top-level `openapi`, `paths`, and `components`. | Review confirms no endpoint behavior is implemented. |
| 4 | Validate YAML contract artifacts. | Complete | Yes | YAML parsing dependency or documented local parser fallback. | JSON/OpenAPI/database checks can proceed in parallel. | Medium | Low | Validation covers `contracts/service-contracts.yaml`, `contracts/integration-contracts.yaml`, and `events/event-catalog.yaml`. | Review confirms parser availability or deterministic skip/failure policy is documented in tests. |
| 5 | Validate database schema readability. | Complete | Yes | Contract validation entrypoint. | JSON/OpenAPI/YAML checks can proceed in parallel. | Low | Low | Validation confirms `database/schema.sql` exists and is readable. | Review confirms no database engine-specific behavior beyond existing artifact evidence. |
| 6 | Validate protobuf artifact presence and syntax when tooling is available. | Complete | No | Local protobuf tooling may be absent. | Other validation checks can proceed in parallel. | Low | Low | Validation reports protobuf syntax pass or deterministic tooling-unavailable result. | Review confirms `contracts/protobuf/echoauth.proto` is checked without changing wire contracts. |
| 7 | Add contract validation unit tests. | Complete | Yes | Tasks 1-6. | Canonical/config unit tests can be drafted in parallel. | Low | Medium | `tests/test_contract_validation.py` passes. | Review confirms required artifacts are tested and missing artifacts fail. |
| 8 | Create canonical data utility module. | Complete | Yes | Contract validation package can be incomplete but common schema and ambiguity decisions must be present. | Config loader can proceed in parallel after task 1. | Medium | Medium | `src/echoauth/canonical.py` exists. | Review confirms only `CanonicalJsonObject`, `StringReferenceList`, and `ValidationErrorList` contract handling is implemented. |
| 9 | Implement deterministic canonical JSON serialization. | Complete | Yes | Task 8. | String reference and validation error list validators can proceed in parallel. | Medium | Medium | Equivalent reordered objects serialize identically. | Review confirms no nested business validation is introduced. |
| 10 | Implement stable canonical hashing. | Complete | Yes | Task 9. | List validators and config loader can proceed in parallel. | Low | Medium | Hash fixtures are stable across repeated runs. | Review confirms hash inputs are canonical serialized values. |
| 11 | Implement string reference list validation. | Complete | No | Task 8. | Canonical JSON hashing and validation error list work can proceed in parallel. | Low | Low | `StringReferenceList` accepts ordered strings and rejects unsupported entries. | Review confirms ordering is preserved per `contracts/service-contracts.yaml`. |
| 12 | Implement validation error list validation. | Complete | No | Task 8. | Canonical JSON hashing and string reference work can proceed in parallel. | Low | Low | `ValidationErrorList` accepts ordered strings and rejects unsupported entries. | Review confirms evaluation order preservation is not altered. |
| 13 | Add canonical data unit tests. | Complete | Yes | Tasks 8-12. | Config and event tests can proceed in parallel. | Low | Medium | `tests/test_canonical.py` passes. | Review confirms deterministic fixtures cover object reordering and unsupported types. |
| 14 | Create configuration loader module. | Complete | Yes | Contract path artifacts must exist. | Canonical utilities and validation harness can proceed in parallel. | Low | Low | `src/echoauth/config_loader.py` exists and loads `RuntimeConfig`. | Review confirms `src/echoauth/config.py` dataclass contract is preserved. |
| 15 | Resolve default contract paths from repository root. | Complete | Yes | Task 14. | Repository adapter design can proceed after canonical utilities. | Low | Low | Contract paths resolve for OpenAPI, protobuf, service contracts, integration contracts, database schema, and event catalog. | Review confirms no hard-coded external paths. |
| 16 | Add config loader unit tests. | Complete | Yes | Tasks 14-15. | Persistence and event tests can proceed in parallel. | Low | Low | `tests/test_config_loader.py` passes. | Review confirms missing required fields fail deterministically. |
| 17 | Create persistence package and base adapter. | Complete | Yes | Canonical data utilities and config loader. | Event validation can proceed in parallel. | High | Medium | `src/echoauth/persistence/__init__.py`; `src/echoauth/persistence/base.py` exist. | Review confirms adapter implements repository foundation only. |
| 18 | Implement save/get round trip behavior in test adapter. | Complete | Yes | Task 17. | Event validation can proceed in parallel. | Medium | Medium | Test adapter saves and retrieves contract-shaped records. | Review confirms no service-specific decisions are embedded. |
| 19 | Preserve canonical JSON text at persistence boundary. | Complete | Yes | Tasks 9-10 and 17-18. | Event validation tests can proceed in parallel. | Medium | Medium | Persisted canonical JSON text compares deterministically after retrieval. | Review confirms behavior matches `database/schema.sql` canonical JSON text convention. |
| 20 | Add repository foundation unit tests. | Complete | Yes | Tasks 17-19. | Event unit tests can proceed in parallel. | Low | Medium | `tests/test_persistence_base.py` passes. | Review confirms missing record behavior is deterministic. |
| 21 | Create event validation helper module. | Complete | Yes | Canonical data utilities. | Persistence adapter can proceed in parallel. | Medium | Medium | `src/echoauth/events_validation.py` exists. | Review confirms no event transport implementation is added. |
| 22 | Validate event envelope required fields and canonical payload. | Complete | Yes | Task 21. | Catalog mapping can proceed in parallel. | Medium | Medium | Event envelope validation enforces required fields and canonical object payload. | Review confirms event payload schema is selected by catalog, not inferred. |
| 23 | Map event types to catalog payload schema paths. | Complete | Yes | Task 21. | Event envelope validation can proceed in parallel. | Low | Medium | Event types resolve against `events/event-catalog.yaml`. | Review confirms unknown event types fail deterministically. |
| 24 | Add event validation unit tests. | Complete | Yes | Tasks 21-23. | Persistence tests can proceed in parallel. | Low | Medium | `tests/test_events_validation.py` passes. | Review confirms required fields and catalog mapping are tested. |
| 25 | Add Sprint 1 contract integration test. | Complete | Yes | Tasks 1-16. | Persistence/event integration can proceed after tasks 17-24. | Medium | Medium | `tests/integration/test_sprint1_contracts.py` passes. | Review confirms config-loaded paths feed validation harness. |
| 26 | Add Sprint 1 persistence/event integration test. | Complete | Yes | Tasks 17-24. | Contract integration can proceed in parallel. | Medium | Medium | `tests/integration/test_sprint1_persistence_events.py` passes. | Review confirms persistence and event boundaries work together without service logic. |
| 27 | Run full Sprint 1 test suite and record output. | Complete | Yes | Tasks 1-26. | None. | Low | Medium | Unit and integration test report passes from repository root. | Review confirms Definition of Done in `runtime/first-engineering-sprint-package.md` is satisfied. |

# Critical Path Report

| Critical Path Step | Task Range | Dependency | Downstream Work Unblocked |
| --- | --- | --- | --- |
| Contract validation foundation | 1-7 | None. | Canonical utilities, config loader, integration tests, later API/protobuf/service adapter validation. |
| Canonical data foundation | 8-13 | Contract validation package and resolved ambiguity artifacts. | Persistence JSON text handling, event payload validation, audit, service adapters. |
| Configuration foundation | 14-16 | Contract artifacts and existing `RuntimeConfig`. | Repository adapter setup, validation harness integration, Sprint 2 adapter configuration. |
| Persistence foundation | 17-20 | Canonical data utilities and config loader. | Audit append adapter, authority/delegation/policy/runtime state repositories, event storage. |
| Event foundation | 21-24 | Canonical data utilities and event artifacts. | Audit publication, notification delivery, event-driven integration tests. |
| Sprint 1 integration evidence | 25-27 | All Sprint 1 foundations. | Sprint 2 audit, identity, authority, delegation, policy, refusal, invariant, and runtime state work. |

# Parallel Work Report

# Single Engineer Path

A single engineer should execute the board in strict order. Limited overlap is
available only by drafting tests immediately after each module skeleton exists.

| Sequence | Work |
| --- | --- |
| 1 | Tasks 1-7: contract validation. |
| 2 | Tasks 8-13: canonical data utilities. |
| 3 | Tasks 14-16: configuration loader. |
| 4 | Tasks 17-20: persistence foundation. |
| 5 | Tasks 21-24: event validation foundation. |
| 6 | Tasks 25-27: integration tests and full Sprint 1 evidence. |

# Three-Engineer Path

| Engineer | Primary Work | Parallel Limits |
| --- | --- | --- |
| Engineer A | Tasks 1-7, then Tasks 25 and 27. | Owns validation harness and final test aggregation. |
| Engineer B | Tasks 8-16, then supports Task 25. | Canonical utilities must land before persistence/event validation finalization. |
| Engineer C | Prepares Tasks 17 and 21 in parallel, completes Tasks 18-24 after canonical utilities land, then owns Task 26. | Persistence canonical JSON text and event canonical payload checks depend on Engineer B's canonical utilities. |

| Parallel Window | Work |
| --- | --- |
| Window 1 | Engineer A creates validation harness; Engineer B creates canonical/config skeletons; Engineer C creates persistence/event package skeletons. |
| Window 2 | Engineer A completes validation tests; Engineer B completes canonical/config tests; Engineer C completes persistence/event adapters. |
| Window 3 | Engineer A and B complete contract integration; Engineer C completes persistence/event integration. |
| Window 4 | All engineers review Sprint 1 Definition of Done and test output. |

# Blocker Report

| Blocker | Affected Tasks | Severity | Resolution Path |
| --- | --- | --- | --- |
| YAML parser unavailable in local environment. | 4, 7, 25, 27 | Medium | Use repository-approved test dependency if available; otherwise implement deterministic tooling-unavailable result as required by Sprint 1 acceptance criteria. |
| Protobuf compiler unavailable in local environment. | 6, 7, 25, 27 | Low | Validate protobuf file presence and report syntax check as tooling-unavailable unless repository test dependencies provide a compiler. |
| Canonical JSON behavior not implemented. | 17-24, 26 | High | Complete Tasks 8-13 before persistence/event validation finalization. |
| Configuration path resolution incomplete. | 17, 25, 27 | Medium | Complete Tasks 14-16 before repository integration and contract integration tests. |
| Repository adapter adds service business logic. | 17-20, 26 | High | Review against Sprint 1 rule: no governance, authorization, policy, invariant, execution, token, emergency override, or notification delivery behavior. |
| Event helper implements transport behavior. | 21-24, 26 | Medium | Limit Sprint 1 event work to validation and catalog mapping. |
| Missing test configuration file. | 7, 13, 16, 20, 24-27 | Medium | Add or update only an existing project test configuration if present; otherwise keep tests runnable by direct test command from repository root. |

# Daily Execution Plan

# Single Engineer Plan

| Day | Focus | Tasks | Expected Evidence |
| --- | --- | --- | --- |
| Day 1 | Contract validation package. | 1-6 | Validation module exists and checks repository artifacts. |
| Day 2 | Contract validation tests and canonical utility skeleton. | 7-9 | Contract tests pass; canonical serialization fixtures started. |
| Day 3 | Canonical hashing/list validators and config loader. | 10-16 | Canonical and config unit tests pass. |
| Day 4 | Persistence foundation. | 17-20 | Persistence package and unit tests pass. |
| Day 5 | Event validation foundation. | 21-24 | Event validation helper and unit tests pass. |
| Day 6 | Integration tests. | 25-26 | Contract and persistence/event integration tests pass. |
| Day 7 | Full Sprint 1 verification and review evidence. | 27 | Full test report and Definition of Done evidence complete. |

# Three-Engineer Plan

| Day | Engineer A | Engineer B | Engineer C | Expected Evidence |
| --- | --- | --- | --- | --- |
| Day 1 | Tasks 1-4. | Tasks 8-9. | Tasks 17 and 21 skeletons. | Validation, canonical, persistence, and event module skeletons exist. |
| Day 2 | Tasks 5-7. | Tasks 10-13. | Tasks 18 and 22. | Contract and canonical unit tests pass; persistence/event foundations in progress. |
| Day 3 | Support Task 25 setup. | Tasks 14-16. | Tasks 19-20 and 23-24. | Config, persistence, and event unit tests pass. |
| Day 4 | Task 25. | Review canonical/config integration. | Task 26. | Integration tests pass or expose deterministic blockers. |
| Day 5 | Task 27 and final evidence. | Review Sprint 1 Definition of Done. | Review Sprint 1 Definition of Done. | Full Sprint 1 test report and review evidence complete. |

# Review Evidence Checklist

| Review Area | Required Evidence |
| --- | --- |
| Scope control | Diff shows no governance, authorization, policy, invariant, execution, token, emergency override, or notification delivery behavior. |
| Contract validation | Unit/integration test output shows repository contracts are checked from repository paths. |
| Canonical data | Fixtures show deterministic canonical serialization and stable hashes. |
| Configuration | Tests show contract paths resolve from repository root. |
| Persistence | Tests show save/get round trip and canonical JSON text preservation. |
| Events | Tests show required envelope fields and event catalog mapping. |
| Sprint completion | Full Sprint 1 test output and Definition of Done checklist are attached to review. |
