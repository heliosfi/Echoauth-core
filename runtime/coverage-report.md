# Runtime Coverage Report

# Sprint 2A-2P Freeze Snapshot

Freeze timestamp: `2026-06-19T21:12:47Z`

| Measure | Frozen Result |
| --- | --- |
| Sprint foundations | 16 of 16 completed within approved validation and evidence boundaries |
| Full test suite | 194 passed; 0 failed |
| Focused contract tests | 7 passed; 0 failed |
| Contract validation | 31 checks: 30 passed, 1 documented optional protobuf compiler skip, 0 failed |
| Validated implementation contracts | 18: 11 JSON, 5 YAML, 1 protobuf, 1 SQL |
| Sprint evidence files | 16 of 16 present |
| Runtime execution capability | Deferred; no command execution or autonomous orchestration |

Coverage is complete for the approved Sprint 2A-2P foundation scope. It is not
production capability coverage. Operational execution, state mutation, token
issuance, envelope generation, external adapters, and durable persistence
remain outside the frozen baseline.

# Implemented Skeletons

| Component | Skeleton Artifact | Coverage |
| --- | --- | --- |
| Runtime package layout | `src/echoauth/`; `src/echoauth/auth/`; `src/echoauth/policy/`; `src/echoauth/governance/`; `src/echoauth/audit/`; `src/echoauth/execution/` | Package boundaries created without application logic. |
| Canonical models | `src/echoauth/models.py` | Contract dataclasses and enums created for OpenAPI, JSON Schema, and protobuf fields. |
| Runtime service boundary | `src/echoauth/main.py`; `src/echoauth/interfaces.py` | Abstract runtime entrypoint and dependency container created. |
| Runtime State Machine foundation | `src/echoauth/runtime/state_models.py`; `src/echoauth/runtime/state_machine.py`; `src/echoauth/runtime/__init__.py` | Ten canonical Sprint 2L states, ten transition events, 33 explicitly enumerated graph edges, deterministic validation, fail-closed rejection, immutable evidence, rejected-attempt auditing, and in-process idempotency implemented. The service validates proposals only and never reads, mutates, or persists current runtime state. |
| Identity service | `src/echoauth/identity/`; `src/echoauth/interfaces.py`; `src/echoauth/models.py` | Identity record model, deterministic validation and hashing, append-history in-memory registry, status lifecycle, revocation enforcement, provider-neutral verifier boundary, and concrete resolution service implemented. |
| Authority resolution foundation | `src/echoauth/auth/authority_resolution.py`; `src/echoauth/auth/authority.py`; `src/echoauth/models.py` | Deterministic resolution over explicit registry records, lifecycle and effective revocation awareness, expiration checks, provider-neutral scope matching, fail-closed conflicts, audit-chain integration, and idempotent evidence-bound results implemented. Legacy `AuthorityService`/`AuthorityVerdict` contract adaptation remains deferred. |
| Authority registry foundation | `src/echoauth/auth/authority_models.py`; `src/echoauth/auth/authority_validation.py`; `src/echoauth/auth/authority_registry.py` | Explicit authority records, six runtime categories, deterministic evidence hashing, fail-closed validation, append-history lifecycle persistence, revocation, immutable scope evidence, audited retrieval, and Sprint 2A audit-chain integration implemented. |
| Delegation foundation | `src/echoauth/auth/delegation_models.py`; `src/echoauth/auth/delegation_validation.py`; `src/echoauth/auth/delegation_repository.py`; `src/echoauth/auth/delegation_service.py`; `src/echoauth/auth/permissions.py` | Explicit authority-derived grants, deterministic evidence hashing, append-history lifecycle persistence, expiration and revocation, authority-source revalidation, exact action/resource scope enforcement, provider-neutral context matching, chain-metadata preservation with fail-closed validation, and audit-chain integration implemented. |
| Policy Evaluation foundation | `src/echoauth/policy/models.py`; `src/echoauth/policy/validation.py`; `src/echoauth/policy/repository.py`; `src/echoauth/policy/service.py`; `src/echoauth/policy/evaluation.py` | Declarative hash-bound rules, append-history policy repository, lifecycle status, exact action/resource matching, provider-neutral scope evaluation, descending numeric priority, highest-priority conflict detection, authority/delegation dependency gates, fail-closed outcomes, and audit-chain integration implemented. |
| Runtime Authorization Gate foundation | `src/echoauth/auth/authorization_models.py`; `src/echoauth/auth/authorization_gate.py`; `src/echoauth/auth/state.py` | Single fixed-order identity -> authority -> delegation-required-or-not-required -> policy decision boundary, fail-closed outcome propagation, immutable decision evidence packages, deterministic decision IDs, dependency failure handling, and final audit-chain integration implemented. This is not the full runtime orchestrator or runtime-state authorization transition. |
| Refusal Service foundation | `src/echoauth/policy/refusal_models.py`; `src/echoauth/policy/refusal_service.py`; `src/echoauth/policy/refusal.py` | Versioned deterministic translation of immutable gate failures into structured refusal categories, canonical reason records, hashed redacted evidence packages, dependency-aware source classification, recovery metadata, audit-chain integration, and idempotent refusal generation implemented. Refusal never modifies or re-evaluates authorization decisions. |
| Escalation Service foundation | `src/echoauth/governance/escalation_models.py`; `src/echoauth/governance/escalation_service.py`; `src/echoauth/governance/ceg.py` | Deterministic classification from linked authorization and refusal decisions, seven canonical routing outcomes, fail-closed evidence validation, deadline handling, immutable evidence packages, audit-chain integration, and idempotent decision generation implemented. Reviewer lookup, notification, resolution, and authorization changes remain deferred. |
| Review Service foundation | `src/echoauth/governance/review_models.py`; `src/echoauth/governance/review_service.py`; `src/echoauth/governance/review.py` | Deterministic assignment from an ordered local reviewer configuration, explicit reviewer/authority-reference matching, escalation-only input validation, nine canonical non-authorizing outcomes, immutable evidence packaging, audit-chain integration, and idempotent review recording implemented. External discovery, identity verification, authority-status validation, notification, override handling, and authorization effects remain deferred. |
| Invariant Validator foundation | `src/echoauth/governance/invariant_models.py`; `src/echoauth/governance/invariant_service.py`; `src/echoauth/governance/invariants.py` | Contract-shaped request/result models, immutable versioned ordered rule sets, canonical facts and definition hashing, deterministic `valid`/`invalid`/`hold`/`halt` outcomes, fail-closed unknown/inactive/missing-fact handling, fixed criticality precedence, audit integration, and idempotency implemented. Domain invariant fact production and pipeline integration remain deferred. |
| Envelope service | `src/echoauth/interfaces.py`; `src/echoauth/models.py` | Abstract interface and typed envelope model created. |
| Token service | `src/echoauth/execution/controls.py`; `src/echoauth/interfaces.py`; `src/echoauth/models.py` | Abstract interface and typed execution token model created. |
| Execution claim service | `src/echoauth/execution/controls.py`; `src/echoauth/interfaces.py` | Abstract service boundary created. |
| Execution Control foundation | `src/echoauth/execution/models.py`; `src/echoauth/execution/service.py`; `src/echoauth/execution/controls.py` | Typed request, decision, control, evidence, constraint, and seven-outcome artifacts; Sprint 2L decision-only input; configured immutable constraints; deterministic eligibility ordering; fail-closed authority/path evidence checks; immutable evidence; audit integration; and idempotency implemented. `ELIGIBLE` is evidence only and performs no dispatch, issuance, transition, or side effect. |
| Halt Decision foundation | `src/echoauth/runtime/halt_models.py`; `src/echoauth/runtime/halt_service.py`; `src/echoauth/runtime/halt.py`; `src/echoauth/interfaces.py` | Contract-shaped halt request and decision artifacts, eight explicit safety causes, cause-specific evidence validation, deterministic refused/hold/halted/escalated classification, critical-severity precedence, immutable evidence, audit integration, and idempotency implemented. The classifier exposes `decide()` and intentionally does not implement the state-mutating `HaltService.halt()` boundary. |
| Recovery Eligibility foundation | `src/echoauth/runtime/recovery_models.py`; `src/echoauth/runtime/recovery_service.py`; `src/echoauth/runtime/recovery.py` | Contract-backed `EXECUTION_BLOCKED`/`HALTED` eligibility validation, fixed failure-code policy enforcement, explicit Authority Resolution and Recovery Review Protocol evidence binding, changed-evidence checks, source-audit verification, deterministic outcomes, append-only eligibility audit records, and in-process idempotency implemented. No authorization, runtime transition, recovery execution, or state mutation exists. |
| Override Service foundation | `src/echoauth/governance/override_models.py`; `src/echoauth/governance/override_service.py`; `src/echoauth/governance/override.py`; `src/echoauth/interfaces.py` | Typed override request, reason, evidence, decision, and explicit authority artifacts; complete authorization-to-review evidence-chain validation; deterministic approve/deny/defer/expire classification; immutable evidence; audit integration; and idempotent processing implemented. Approval is an inert override record and never authorizes execution. |
| Notification service | `src/echoauth/interfaces.py` | Abstract notification boundary created. |
| Audit service | `src/echoauth/audit/logging.py`; `src/echoauth/interfaces.py`; `src/echoauth/models.py` | Abstract append interface and typed audit record model created. |
| Event bus | `src/echoauth/events.py` | Abstract publish/subscribe interface and event envelope model created. |
| Repository interfaces | `src/echoauth/repositories.py` | Abstract persistence boundaries created for registry, revocation, delegation, policy, runtime state, and audit log storage. |
| Configuration structure | `src/echoauth/config.py` | Contract path and runtime configuration dataclasses created. |
| Dependency graph | `src/echoauth/wiring.py`; `runtime/dependency-graph.md` | Declarative runtime dependency edges created. |
| Traceability matrix | `runtime/traceability-matrix.md` | Specification to contract to runtime mapping created. |
| Sprint 1 contract validation harness | `src/echoauth/contracts/validation.py`; `src/echoauth/contracts/__init__.py` | Repository contract validation implemented without service behavior; YAML validation is mandatory and deterministic for integration and event catalog contracts. |
| Sprint 1 canonical data utilities | `src/echoauth/canonical.py` | Canonical object/list serialization, validation, and hashing implemented for resolved contract types. |
| Sprint 1 configuration loader | `src/echoauth/config_loader.py` | Runtime configuration loading and contract path resolution implemented. |
| Sprint 1 repository foundation | `src/echoauth/persistence/base.py`; `src/echoauth/persistence/__init__.py` | Generic in-memory repository foundation implemented for tests and adapter groundwork. |
| Sprint 1 event validation foundation | `src/echoauth/events_validation.py` | Event envelope validation and catalog mapping implemented without transport behavior. |
| Sprint 1 tests | `tests/test_contract_validation.py`; `tests/test_canonical.py`; `tests/test_config_loader.py`; `tests/test_persistence_base.py`; `tests/test_events_validation.py`; `tests/integration/test_sprint1_contracts.py`; `tests/integration/test_sprint1_persistence_events.py` | Unit and integration test suite implemented; YAML parser available, unavailable, invalid, and valid paths are covered. |
| Sprint 2B identity registry | `src/echoauth/identity/models.py`; `src/echoauth/identity/validation.py`; `src/echoauth/identity/repository.py`; `src/echoauth/identity/service.py` | Identity registration, uniqueness, immutable history, active/suspended/revoked/archived transitions, revocation refusal, assurance enforcement, evidence hashing, and deterministic verdict generation implemented. |
| Sprint 2B tests | `tests/test_identity_registry.py`; `tests/test_identity_resolution.py` | 13 identity tests cover registration, deterministic hashes, lifecycle, revocation, immutability, invalid transitions, verified resolution, conflicts, missing credentials, assurance failure, provider unavailability, and malformed requests. |
| Sprint 2C authority registry tests | `tests/test_authority_registry.py` | 11 tests cover all authority categories, valid and invalid creation, expiration, status transitions, revocation, evidence-hash stability, immutable storage, priority-conflict refusal, audited retrieval, audit failure, and audit-history integrity. |
| Sprint 2D authority resolution tests | `tests/test_authority_resolution.py` | 9 tests cover authorized, denied, revoked, expired, conflict, insufficient-authority, scope mismatch, effective revocation evidence, malformed revocation refusal, deterministic results, and audit idempotency. |
| Sprint 2E delegation tests | `tests/test_delegation.py` | 9 tests cover valid, revoked, expired, invalid-grantor, invalid-scope, invalid-subject, deterministic validation, authority-scope expansion rejection, chain-metadata preservation, fail-closed chain validation, and audit-history integrity. |
| Sprint 2F policy evaluation tests | `tests/test_policy_evaluation.py` | 9 tests cover authorized, denied, conflict, expired, revoked, invalid-policy, deterministic evaluation, priority ordering, delegation integration, and audit idempotency. |
| Sprint 2G authorization gate tests | `tests/test_authorization_gate.py` | 10 full-stack tests cover direct and delegated authorization, identity/authority/delegation failures, policy denial, conflict, revocation, expiration, deterministic decisions, complete dependency references, and audit idempotency. |
| Sprint 2H refusal tests | `tests/test_refusal_service.py` | 9 tests cover identity, authority, delegation, policy-denial, revoked, expired, conflict, malformed-request, deterministic refusal evidence, and audit idempotency. |
| Sprint 2I escalation tests | `tests/test_escalation_service.py` | 11 tests cover refusal, conflict, revocation, expiration, unavailable dependency, every explicit review route, no available route, deterministic classification, audit evidence, authorized-decision rejection, and mismatched-evidence refusal. |
| Sprint 2J review tests | `tests/test_review_service.py` | 10 tests cover escalation consumption, approval-for-override-review, denial, information return, delegated review, unresolved review, configured assignment order, non-assigned reviewer refusal, audit evidence, and idempotent processing. |
| Sprint 2K override tests | `tests/test_override_service.py` | 8 tests cover approval, denial, deferral, expiration, absent authority, inconsistent evidence rejection, immutable audited evidence, and idempotent processing across the complete authorization-to-review chain. |
| Sprint 2L runtime-state tests | `tests/test_runtime_state_machine.py` | 11 tests cover the exact state vocabulary, every one of 33 graph edges, authorization and governance paths, blocked release, undefined transitions, target mismatch, terminal expiration, immutable audit evidence, and idempotency. |
| Sprint 2M execution-control tests | `tests/test_execution_control.py` | 13 tests cover all seven outcomes, direct and override evidence paths, rejected transitions, configured blocking, unconfigured constraints, authority/evidence absence, expiration, immutable audit evidence, and idempotency. |
| Sprint 2N invariant-validator tests | `tests/test_invariant_validator.py` | 12 tests cover all four outcomes, unknown and inactive versions, missing facts, critical precedence, stable evaluation order, canonical facts hashing, immutable definition detachment, invalid configuration, audit evidence, and idempotency. |
| Sprint 2O halt-decision tests | `tests/test_halt_decision.py` | 14 tests cover missing authority/evidence, invalid state, invariant invalid/hold/halt, expired and invalid dependencies, unresolved override, unsafe execution, critical precedence, malformed evidence, immutable audit evidence, and idempotency. |
| Sprint 2P Recovery Eligibility tests | `tests/test_recovery_eligibility.py` | 11 tests cover both entry states, all execution-blocked failure policies, halted new-request handling, unresolved guards, authority and changed-evidence refusal, audit-link integrity, Recovery Review Protocol binding, source-record preservation, eligibility-only audit events, invalid state/failure pairs, and deterministic idempotency. |

# Documented Exceptions

| Exception | Rationale |
| --- | --- |
| Nested business schemas for canonical object fields are not generated. | Existing specifications define `payload`, `context`, `details`, `evidence`, `scope`, `rules`, `facts`, `credential_set`, `context_constraints`, and `effective_scope` as domain-specific canonical JSON objects. |
| Protobuf continues to use `google.protobuf.Struct` for canonical JSON object fields. | Changing to wrapper messages would alter the wire shape without specification authority. |
| Database schema stores canonical JSON as text. | Specifications require deterministic serialization and hashes but do not mandate a database engine or JSON function. |

# Resolved Ambiguities

| Contract Type | Fields |
| --- | --- |
| `CanonicalJsonObject` | `payload`, `context`, `details`, `evidence`, `scope`, `rules`, `facts`, `credential_set`, `context_constraints`, `effective_scope` |
| `StringReferenceList` | `credential_refs`, `role_refs` |
| `ValidationErrorList` | `validation_errors` |

# Missing Dependencies

| Dependency | Required By |
| --- | --- |
| Concrete implementation adapters | All repository, event bus, service, cryptographic, persistence, and API boundaries. |
| Future nested domain schemas, if desired | Domain-specific payload, policy rule, evidence, scope, credential, and fact validation beyond canonical object typing. |
| Concrete credential providers | `CredentialVerifier` is implemented as an identity-only boundary; password, biometric, device, session, and cryptographic provider integrations remain deployment-specific. |
| Authority contract vocabulary alignment | Sprint 2C uses `parent`, `caregiver`, `institution`, `delegated`, `emergency`, and `runtime-service`; older generated contracts use conflicting `court`/`service` and `delegate`/`system` values. Contract regeneration is deferred. |
| Authority mutation authorization | Registry storage operations capture the actor and audit evidence, but administrative/root-authority validation requires the deferred authority decision boundary. The repository must not be exposed directly as a public mutation API. |
| Authority scope semantics | Scope is validated as non-empty canonical JSON and hash-bound. Action/resource matching and institutional, delegated, or emergency precedence are deferred. |
| Authority resolution contract adaptation | Sprint 2D outcomes are `authorized`, `denied`, `revoked`, `expired`, `conflict`, and `insufficient_authority`; generated OpenAPI/protobuf artifacts still expose `valid`, `refused`, `hold`, `conflict`, and `escalate`. |
| Identity verdict status lookup | Authority resolution validates and hash-binds the required identity verdict reference but cannot verify verdict status because no identity-verdict repository contract exists. The reference never grants authority. |
| Delegate identity proof | Delegation validation enforces `requester_id == delegate_id`, but the approved request contract carries no delegate identity-verdict reference. External identity verification remains required before this service is exposed in orchestration. |
| Delegation chain schema | Sprint 2E preserves canonical `chain_metadata` but generated contracts and database schema define no chain fields. Non-empty chain metadata returns `conflict` until bounded chain validation is specified. |
| Delegation persistence alignment | The runtime grant includes `state`, `evidence_hash`, `authority_resolution_id`, and chain metadata; `database/schema.sql#delegations` does not contain all of these fields. Production persistence is deferred. |
| Policy rule schema | Generated contracts define `rules` only as a canonical object. Sprint 2F uses declarative rule fields for action, resource, scope, effect, priority, dates, status, and reason; contract generation remains deferred. |
| Policy priority direction | Specifications require deterministic order but do not define numeric direction. Sprint 2F evaluates the highest numeric priority group first and reports opposing effects in that group as conflict. |
| Upstream result authenticity | Policy evaluation validates typed authority/delegation result references and outcomes, but no persisted verdict-result repository or signature contract exists. |
| Policy persistence alignment | `database/schema.sql` stores policy decisions but defines no policy registry/rule table. Sprint 2F policy artifacts remain in-memory. |
| Gate/runtime-state distinction | Sprint 2G `authorized` means the four gate dependencies passed. Repository runtime specifications reserve runtime state `authorized` for additional invariant checks; no runtime state transition is emitted here. |
| Authorization request contract | Sprint 2G requires requester type, credentials, assurance, and pinned policy version, while `EchoAuthRequest` does not carry all identity inputs. API/protobuf adaptation remains deferred. |
| Authorization idempotency persistence | Decisions are deterministic and cached in-process, but no persistent idempotency/decision repository is implemented. |
| Refusal category/state alignment | Sprint 2H defines explanatory categories, while `specs/refusal-engine.md` defines runtime states `refused`, `hold`, `halted`, `revoked`, and `escalated`. Refusal categories do not perform runtime state transitions. |
| Refusal persistence | Refusal decisions are immutable and cached in-process, but no refusal decision table or repository contract exists. |
| Escalation reviewer registry | `specs/escalation-engine.md` requires deterministic reviewer selection, but no reviewer registry, availability model, or assignment contract exists. Sprint 2I classifies an explicit review type without assigning a reviewer. |
| Escalation persistence and notification | No generated escalation table, API/protobuf model, notification delivery adapter, or review-resolution repository exists. Decisions are immutable and cached in-process; only audit evidence is persisted. |
| Escalation authority vocabulary | The specification names `required_authority_type` but does not enumerate it. Sprint 2I uses only the review routes named in the approved Sprint scope and does not map identity or authority-registry categories into review authority. |
| Review contract artifacts | No standalone review specification, OpenAPI operation, protobuf message, JSON schema, database table, or event schema exists. Sprint 2J is limited to the approved Sprint outcomes, escalation contract, typed in-memory artifacts, and audit evidence. |
| Reviewer trust verification | Ordered reviewer assignments are constructor-supplied and authority-reference-bound, but no contract defines reviewer identity verification, authority lifecycle lookup, signatures, or roster persistence. A recorded review cannot authorize or execute an action. |
| Override contract alignment | `specs/emergency-override-controls.md` defines emergency override fields, while Sprint 2K names a general Override Service and approve/deny/defer/expire outcomes. The runtime uses the emergency evidence fields and Sprint 2K outcomes without adding execution semantics. |
| Override authority trust | Override authorities are explicitly constructor-configured and matched by ID, reference, and declarer. No contract exists for external identity proof, authority lifecycle lookup, signatures, permitted-action registries, or production authority persistence. |
| Override scope semantics | Effective scope is non-empty, canonical, immutable, and hash-bound, but no provider-neutral rule defines how to prove it is narrower than normal authority. An approved record cannot produce execution permission. |
| Runtime state vocabulary alignment | Sprint 2L defines ten states that differ from the older generated `src/echoauth/models.py#RuntimeState` and protobuf vocabulary. The Sprint 2L enum is isolated under `echoauth.runtime`; generated contract replacement is deferred. |
| Runtime transition persistence | The state machine validates and audits transition proposals but intentionally has no current-state repository or mutation method. `allowed` means graph-valid only and does not prove or perform a state change. |
| Runtime transition authority | Actor IDs and evidence are validated and hash-bound, but no component-role registry or transition-authority contract exists. Caller authorization and concurrent-state checks remain deferred. |
| Execution Control contract | No standalone execution-eligibility specification, OpenAPI operation, protobuf message, JSON schema, event, or database table exists. Sprint 2M uses its approved outcomes plus Sprint 2L decisions and repository execution safety requirements. |
| Execution evidence authenticity | Authority and governance evidence require canonical ID/hash pairs and are hash-bound, but no decision repository, signature, or verification-key contract exists. Authenticity hardening remains deferred. |
| Execution eligibility effect | `ELIGIBLE` confirms only that configured prerequisites validated. It does not authorize execution, issue a token, create an envelope, mutate state, claim work, or dispatch a command. |
| Invariant rule schema | The contract defines canonical facts, stable order, fixed criticality, and four outcomes but does not define a domain expression language. Sprint 2N supports only explicitly configured top-level fact equality rules; the twelve governance invariants are not translated into guessed runtime predicates. |
| Invariant fact provenance | Facts are canonicalized and hash-bound, but no contract identifies trusted fact producers or signs fact evidence. The validator cannot infer authority, token, payload, channel, or audit-path truth. |
| Governance package initialization | Importing `echoauth.governance` before `echoauth.auth` exposes a pre-existing eager-import cycle through escalation, policy, and authorization packages. Existing repository import order remains in tests; package-wide lazy-loading refactoring is deferred. |
| Halt outcome vocabulary | `specs/runtime-halt-model.md` includes `refused`, `hold`, `halted`, `revoked`, and `escalated`; Sprint 2L omits `hold` and `revoked`. Sprint 2O emits evidence-only halt outcomes and performs no Sprint 2L transition. |
| Halt evidence schema | The halt specification defines evidence as a canonical JSON object but does not generate cause-specific nested schemas. Sprint 2O requires only explicit source IDs, hashes, statuses, and reviewer references for its eight approved causes. |
| Halt source authenticity | Halt evidence is structurally validated and hash-bound, but no persisted-decision or signature contract authenticates referenced authority, state, invariant, dependency, override, or execution decisions. |
| Recovery authority and review authenticity | Recovery binds typed Authority Resolution, Review Decision, Halt Decision, and audit evidence by ID/hash/reference. No signature, external trust registry, or persisted decision adapter authenticates evidence beyond the supplied in-process artifacts. |
| Recovery operational effects | `REVALIDATION_REQUIRED` is governance eligibility evidence only. Recovery does not invoke validation services, authorize the original action, mutate state, define a destination, issue tokens, create envelopes, emit `runtime.recovered`, or execute work. |

# Final Assessment

Ready for implementation with documented exceptions.

The contract ambiguity items are resolved for interface, schema, serialization,
and persistence boundaries. Implementations can begin against the skeleton, but
must not infer nested business behavior for canonical object fields without a
future specification change.
