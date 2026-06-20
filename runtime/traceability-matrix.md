# Runtime Traceability Matrix

Freeze timestamp: `2026-06-19T21:12:47Z`

Frozen traceability status: all 16 Sprint 2A-2P foundations have an
implementation evidence file and a dedicated traceability section. Recovery
Eligibility terminates in evidence and audit records; it has no state mutation,
authorization, execution, or `runtime.recovered` edge.

| Specification | Contract | Runtime Interface | Runtime Module | State Machine |
| --- | --- | --- | --- | --- |
| `specs/echoauth-spec.md` | `api/openapi.yaml`; `contracts/service-contracts.yaml`; `contracts/protobuf/echoauth.proto`; `contracts/decision-log.md` | `RuntimeService`; `EchoAuthRuntime`; `EchoAuthRuntimeDependencies` | `src/echoauth/interfaces.py`; `src/echoauth/main.py` | `specs/runtime-state-machine.md` |
| `specs/runtime-state-machine.md`; `specs/authorization-states.md`; Sprint 2L requirements | `contracts/service-contracts.yaml`; `contracts/protobuf/echoauth.proto`; Sprint 2L canonical vocabulary | `RuntimeState`; `RuntimeTransition`; `RuntimeTransitionRequest`; `RuntimeTransitionDecision`; `RuntimeStateEvidence`; `RuntimeStateMachine` | `src/echoauth/runtime/state_models.py`; `src/echoauth/runtime/state_machine.py`; `src/echoauth/runtime/__init__.py` | Versioned 33-edge validation graph over ten Sprint 2L states; no state mutation or persistence |
| Sprint 2G authorization gate; `specs/echoauth-spec.md`; `specs/authorization-states.md` | `api/openapi.yaml`; `contracts/service-contracts.yaml`; `contracts/protobuf/echoauth.proto`; Sprint 2B-2F runtime result models | `AuthorizationRequest`; `AuthorizationDecision`; `AuthorizationGateService` | `src/echoauth/auth/authorization_models.py`; `src/echoauth/auth/authorization_gate.py`; `src/echoauth/auth/state.py` | Gate outcomes: `authorized`, `denied`, `revoked`, `expired`, `conflict`, `invalid_identity`, `invalid_authority`, `invalid_delegation`, `invalid_policy`; no runtime-state transition |
| `specs/identity-resolution.md`; `specs/identity-model.md` | `schemas/common.schema.json`; `api/openapi.yaml`; `contracts/protobuf/echoauth.proto`; `contracts/ambiguities.md`; `contracts/decision-log.md` | `IdentityService`; `RegistryIdentityService`; `CredentialVerifier`; `IdentityRepository`; `IdentityResolutionRequest`; `IdentityVerdict`; `IdentityRecord` | `src/echoauth/identity/models.py`; `src/echoauth/identity/validation.py`; `src/echoauth/identity/repository.py`; `src/echoauth/identity/service.py`; `src/echoauth/interfaces.py`; `src/echoauth/models.py` | `specs/identity-model.md`; `specs/identity-resolution.md` |
| `specs/authority-resolution.md`; `specs/authority-registry.md`; `specs/authority-revocation.md` | `schemas/authority-resolution.schema.json`; `contracts/service-contracts.yaml`; `contracts/protobuf/echoauth.proto`; `contracts/ambiguities.md`; Sprint 2D outcome requirements | `AuthorityResolutionService`; `AuthorityResolutionRequest`; `AuthorityResolutionResult`; `AuthorityScopeMatcher` | `src/echoauth/auth/authority_resolution.py`; `src/echoauth/auth/authority_registry.py`; `src/echoauth/auth/authority.py`; `src/echoauth/models.py` | `authorized`; `denied`; `revoked`; `expired`; `conflict`; `insufficient_authority` |
| `specs/authority-registry.md` | `database/schema.sql`; `contracts/service-contracts.yaml`; Sprint 2C authority category requirements | `AuthorityRepository`; `InMemoryAuthorityRepository`; `AuthorityRecord`; `StoredAuthorityRecord` | `src/echoauth/auth/authority_models.py`; `src/echoauth/auth/authority_validation.py`; `src/echoauth/auth/authority_registry.py`; `src/echoauth/auth/authority.py` | `active` -> `suspended`, `revoked`, or `expired`; `suspended` -> `active` or `revoked` |
| `specs/authority-revocation.md` | `database/schema.sql`; `contracts/service-contracts.yaml` | `RevocationRepository` | `src/echoauth/repositories.py`; `src/echoauth/auth/authority.py` | `specs/runtime-state-machine.md` |
| `specs/delegation-model.md`; `specs/delegation-validation.md` | `api/openapi.yaml`; `contracts/service-contracts.yaml`; `database/schema.sql`; `contracts/ambiguities.md`; `contracts/decision-log.md`; Sprint 2E outcome requirements | `DelegationGrant`; `DelegationRepository`; `InMemoryDelegationRepository`; `DelegationValidationRequest`; `DelegationValidationResult`; `DelegationValidationService`; `DelegationContextMatcher` | `src/echoauth/auth/delegation_models.py`; `src/echoauth/auth/delegation_validation.py`; `src/echoauth/auth/delegation_repository.py`; `src/echoauth/auth/delegation_service.py`; `src/echoauth/auth/permissions.py` | Grant: `issued` -> `active`, `expired`, `revoked`, or `invalid`; validation: `valid`, `expired`, `revoked`, `invalid_grantor`, `invalid_scope`, `invalid_subject`, `conflict` |
| `specs/policy-registry.md`; `specs/policy-evaluation.md`; `specs/policy-engine.md` | `api/openapi.yaml`; `contracts/service-contracts.yaml`; `database/schema.sql`; `contracts/ambiguities.md`; `contracts/decision-log.md`; Sprint 2F outcome requirements | `PolicyRule`; `PolicyRepository`; `InMemoryPolicyRepository`; `PolicyEvaluationRequest`; `PolicyEvaluationResult`; `PolicyEvaluationService`; `PolicyScopeMatcher` | `src/echoauth/policy/models.py`; `src/echoauth/policy/validation.py`; `src/echoauth/policy/repository.py`; `src/echoauth/policy/service.py`; `src/echoauth/policy/evaluation.py` | Policy: `draft` -> `active` or `revoked`; `active` -> `retired`, `revoked`, or `expired`; evaluation: `authorized`, `denied`, `conflict`, `expired`, `revoked`, `invalid_policy` |
| `specs/refusal-engine.md`; `governance/refusal-first.md`; Sprint 2H requirements | `contracts/service-contracts.yaml`; `contracts/ambiguities.md`; Sprint 2G authorization decision model | `RefusalRequest`; `RefusalReason`; `RefusalDecision`; `RefusalService` | `src/echoauth/policy/refusal_models.py`; `src/echoauth/policy/refusal_service.py`; `src/echoauth/policy/refusal.py` | Categories: `invalid_identity`, `invalid_authority`, `invalid_delegation`, `policy_denied`, `revoked`, `expired`, `conflict`, `unavailable_dependency`, `malformed_request`; no runtime-state transition |
| `specs/invariant-validator.md`; `governance/invariants.md`; Sprint 2N implementation boundary | `api/openapi.yaml#/components/schemas/InvariantValidationRequest`; `api/openapi.yaml#/components/schemas/InvariantResult`; `contracts/service-contracts.yaml`; `contracts/ambiguities.md`; `database/schema.sql#invariant_results`; `events/event-catalog.yaml#invariant.result` | `InvariantValidationRequest`; `InvariantResult`; `InvariantRule`; `InvariantSet`; `InvariantService`; `InvariantServiceInterface` | `src/echoauth/governance/invariant_models.py`; `src/echoauth/governance/invariant_service.py`; `src/echoauth/governance/invariants.py`; `src/echoauth/interfaces.py` | Validation outcomes `valid`, `invalid`, `hold`, `halt`; no runtime-state mutation |
| `specs/escalation-engine.md`; Sprint 2I requirements | `contracts/service-contracts.yaml`; `contracts/ambiguities.md`; Sprint 2G authorization decision model; Sprint 2H refusal decision model | `EscalationRequest`; `EscalationReason`; `EscalationDecision`; `EscalationService` | `src/echoauth/governance/escalation_models.py`; `src/echoauth/governance/escalation_service.py`; `src/echoauth/governance/ceg.py` | Foundation emits `opened` or fail-closed `expired`; reviewer notification and resolution transitions deferred |
| `specs/escalation-engine.md`; Sprint 2J requirements | Sprint 2I escalation decision model; `contracts/service-contracts.yaml`; `contracts/ambiguities.md` | `ReviewRequest`; `ReviewOutcome`; `ReviewDecision`; `ReviewerAssignment`; `ReviewService` | `src/echoauth/governance/review_models.py`; `src/echoauth/governance/review_service.py`; `src/echoauth/governance/review.py` | Immutable non-authorizing review record; override, runtime-state, and execution transitions deferred |
| `specs/runtime-envelope.md` | `schemas/runtime-envelope.schema.json`; `contracts/service-contracts.yaml`; `contracts/protobuf/echoauth.proto` | `EnvelopeService`; `RuntimeEnvelope` | `src/echoauth/interfaces.py`; `src/echoauth/models.py` | `specs/runtime-state-machine.md` |
| `specs/execution-token.md` | `schemas/execution-token.schema.json`; `contracts/service-contracts.yaml`; `contracts/protobuf/echoauth.proto` | `TokenService`; `ExecutionToken` | `src/echoauth/execution/controls.py`; `src/echoauth/interfaces.py`; `src/echoauth/models.py` | `specs/runtime-state-machine.md` |
| `specs/execution-claims.md` | `contracts/service-contracts.yaml`; `contracts/ambiguities.md` | `ExecutionClaimService` | `src/echoauth/execution/controls.py`; `src/echoauth/interfaces.py` | `specs/runtime-state-machine.md` |
| `specs/execution-claims.md`; `specs/runtime-halt-model.md`; Sprint 2M requirements | Sprint 2L transition decision; `contracts/service-contracts.yaml`; `contracts/ambiguities.md` | `ExecutionRequest`; `ExecutionDecision`; `ExecutionControl`; `ExecutionEvidence`; `ExecutionConstraint` | `src/echoauth/execution/models.py`; `src/echoauth/execution/service.py`; `src/echoauth/execution/controls.py` | Seven eligibility outcomes only; no execution or state transition |
| `specs/runtime-halt-model.md`; Sprint 2O validation boundary | `contracts/service-contracts.yaml`; `contracts/ambiguities.md`; `events/event-catalog.yaml#runtime.halted` | `HaltRequest`; `HaltDecision`; `HaltDecisionEvidence`; `HaltDecisionService`; `HaltServiceInterface` | `src/echoauth/runtime/halt_models.py`; `src/echoauth/runtime/halt_service.py`; `src/echoauth/runtime/halt.py`; `src/echoauth/interfaces.py` | Evidence outcomes `refused`, `hold`, `halted`, `escalated`; no runtime-state transition or `HaltService.halt()` implementation |
| `specs/runtime-recovery.md`; Sprint 2P validation boundary | `contracts/recovery-service.yaml`; `schemas/recovery-request.schema.json`; `schemas/recovery-result.schema.json`; `schemas/recovery-review-protocol.schema.json`; `contracts/decision-log.md#ADR-0007` | `RecoveryEligibilityRequest`; `RecoveryEligibilityResult`; `RecoveryReviewProtocol`; `RecoveryEligibilityService` | `src/echoauth/runtime/recovery_models.py`; `src/echoauth/runtime/recovery_service.py`; `src/echoauth/runtime/recovery.py` | Entry evidence is limited to `EXECUTION_BLOCKED` and `HALTED`; outcomes are evidence only and perform no transition or mutation |
| `specs/emergency-override-controls.md`; Sprint 2K requirements | `contracts/service-contracts.yaml`; `contracts/ambiguities.md`; Sprint 2G-2J decision models | `OverrideRequest`; `OverrideReason`; `OverrideEvidence`; `OverrideDecision`; `OverrideAuthority`; `OverrideService`; `EmergencyOverrideServiceInterface` | `src/echoauth/governance/override_models.py`; `src/echoauth/governance/override_service.py`; `src/echoauth/governance/override.py`; `src/echoauth/interfaces.py` | Inert `approved`, `denied`, `deferred`, or `expired` record; runtime-state and execution transitions deferred |
| `specs/runtime-session-model.md` | `database/schema.sql`; `contracts/integration-contracts.yaml` | `RuntimeStateRepository`; `RuntimeConfig` | `src/echoauth/repositories.py`; `src/echoauth/config.py` | `specs/runtime-state-machine.md` |
| `specs/audit-record.md`; `specs/audit-chain.md`; `specs/audit-log-spec.md` | `schemas/audit-record.schema.json`; `database/schema.sql`; `events/event-catalog.yaml` | `AuditService`; `AuditRecord`; `AuditLogRepository` | `src/echoauth/audit/logging.py`; `src/echoauth/interfaces.py`; `src/echoauth/models.py`; `src/echoauth/repositories.py` | Not applicable |
| `specs/event-bus.md` | `events/event-envelope.schema.json`; `events/event-catalog.yaml` | `EventBus`; `EventEnvelope` | `src/echoauth/events.py` | Not applicable |
| `specs/notification-contracts.md` | `events/event-catalog.yaml`; `contracts/integration-contracts.yaml` | `NotificationService` | `src/echoauth/interfaces.py` | Not applicable |
| `specs/security-model.md`; `specs/api-spec.md` | `api/openapi.yaml`; `contracts/integration-contracts.yaml` | `RuntimeConfig`; `ContractPaths` | `src/echoauth/config.py` | Not applicable |
| Ambiguity resolution | `contracts/ambiguities.md`; `contracts/ambiguity-resolution-report.md`; `contracts/decision-log.md` | `CanonicalJsonObject`; `StringReferenceList`; `ValidationErrorList` | `schemas/common.schema.json`; `api/openapi.yaml`; `src/echoauth/models.py` | Not applicable |

# Sprint 1 Implementation Traceability

| Sprint 1 Component | Evidence Source | Runtime Artifact | Test Artifact | Contracts Consumed |
| --- | --- | --- | --- | --- |
| Contract validation harness | `runtime/first-engineering-sprint-package.md`; `runtime/sprint-1-execution-board.md`; `runtime/sprint-1-implementation-evidence.md` | `src/echoauth/contracts/__init__.py`; `src/echoauth/contracts/validation.py` | `tests/test_contract_validation.py`; `tests/integration/test_sprint1_contracts.py` | `api/openapi.yaml`; `contracts/service-contracts.yaml`; `contracts/integration-contracts.yaml`; `events/event-catalog.yaml`; `contracts/protobuf/echoauth.proto`; `schemas/*.json`; `events/*.json`; `database/schema.sql` |
| Canonical data utilities | `contracts/ambiguities.md`; `contracts/decision-log.md`; `schemas/common.schema.json` | `src/echoauth/canonical.py` | `tests/test_canonical.py`; `tests/integration/test_sprint1_persistence_events.py` | `schemas/common.schema.json`; `contracts/service-contracts.yaml` |
| Configuration loader | `src/echoauth/config.py`; `contracts/integration-contracts.yaml` | `src/echoauth/config_loader.py` | `tests/test_config_loader.py`; `tests/integration/test_sprint1_contracts.py` | `contracts/integration-contracts.yaml`; `api/openapi.yaml`; `database/schema.sql`; `events/event-catalog.yaml` |
| Repository adapter foundation | `src/echoauth/repositories.py`; `database/schema.sql` | `src/echoauth/persistence/__init__.py`; `src/echoauth/persistence/base.py` | `tests/test_persistence_base.py`; `tests/integration/test_sprint1_persistence_events.py` | `database/schema.sql`; `contracts/integration-contracts.yaml` |
| Event validation foundation | `src/echoauth/events.py`; `events/event-envelope.schema.json`; `events/event-catalog.yaml` | `src/echoauth/events_validation.py` | `tests/test_events_validation.py`; `tests/integration/test_sprint1_persistence_events.py` | `events/event-envelope.schema.json`; `events/event-catalog.yaml` |

# Sprint 2B Implementation Traceability

| Sprint 2B Component | Evidence Source | Runtime Artifact | Test Artifact | Contracts Consumed |
| --- | --- | --- | --- | --- |
| Identity record and lifecycle | `specs/identity-model.md` | `src/echoauth/identity/models.py`; `src/echoauth/identity/validation.py`; `src/echoauth/identity/repository.py` | `tests/test_identity_registry.py` | `schemas/common.schema.json`; `contracts/decision-log.md` |
| Identity resolution | `specs/identity-resolution.md` | `src/echoauth/identity/service.py`; `src/echoauth/interfaces.py`; `src/echoauth/models.py` | `tests/test_identity_resolution.py` | `api/openapi.yaml`; `contracts/service-contracts.yaml`; `contracts/protobuf/echoauth.proto`; `contracts/ambiguities.md` |
| Identity revocation enforcement | `specs/identity-model.md`; `specs/identity-resolution.md` | `src/echoauth/identity/repository.py`; `src/echoauth/identity/service.py` | `tests/test_identity_registry.py`; `tests/test_identity_resolution.py` | `contracts/service-contracts.yaml` |

# Sprint 2C Implementation Traceability

| Sprint 2C Component | Evidence Source | Runtime Artifact | Test Artifact | Contracts Consumed |
| --- | --- | --- | --- | --- |
| Authority record model | `specs/authority-registry.md`; Sprint 2C requirements | `src/echoauth/auth/authority_models.py` | `tests/test_authority_registry.py` | `database/schema.sql`; `contracts/ambiguities.md`; `schemas/common.schema.json` |
| Authority validation and evidence hashing | `specs/authority-registry.md` | `src/echoauth/auth/authority_validation.py` | `tests/test_authority_registry.py` | `contracts/decision-log.md`; `src/echoauth/canonical.py` |
| Authority lifecycle and revocation | `specs/authority-registry.md`; `specs/authority-revocation.md` | `src/echoauth/auth/authority_registry.py` | `tests/test_authority_registry.py` | `contracts/service-contracts.yaml` |
| Authority audit integration | `specs/authority-registry.md`; `specs/audit-record.md`; `specs/audit-chain.md` | `src/echoauth/auth/authority_registry.py`; `src/echoauth/audit/repository.py` | `tests/test_authority_registry.py` | `schemas/audit-record.schema.json`; `events/event-catalog.yaml` |

# Sprint 2D Implementation Traceability

| Sprint 2D Component | Evidence Source | Runtime Artifact | Test Artifact | Contracts Consumed |
| --- | --- | --- | --- | --- |
| Resolution request and result models | `specs/authority-resolution.md`; Sprint 2D requirements | `src/echoauth/models.py`; `src/echoauth/auth/authority_resolution.py` | `tests/test_authority_resolution.py` | `schemas/authority-resolution.schema.json`; `api/openapi.yaml`; `contracts/protobuf/echoauth.proto` |
| Resolution validation | `specs/authority-resolution.md` | `validate_authority_resolution_request` in `src/echoauth/auth/authority_resolution.py` | `tests/test_authority_resolution.py` | `schemas/common.schema.json`; `contracts/ambiguities.md` |
| Registry lookup and lifecycle evaluation | `specs/authority-registry.md` | `AuthorityResolutionService`; `AuthorityRepository.find_by_subject` | `tests/test_authority_resolution.py` | `src/echoauth/auth/authority_registry.py` |
| Revocation and expiration awareness | `specs/authority-revocation.md`; `specs/authority-registry.md` | `src/echoauth/auth/authority_resolution.py` | Revoked, effective-revocation, expired, and malformed-revocation tests | `contracts/service-contracts.yaml`; `contracts/ambiguities.md` |
| Resolution audit integration | `specs/authority-resolution.md`; `specs/audit-record.md`; `specs/audit-chain.md` | `AuthorityResolutionService`; `InMemoryAuditLogRepository` | Valid resolution and deterministic audit-idempotency tests | `schemas/audit-record.schema.json`; `events/event-catalog.yaml` |

# Sprint 2E Implementation Traceability

| Sprint 2E Component | Evidence Source | Runtime Artifact | Test Artifact | Contracts Consumed |
| --- | --- | --- | --- | --- |
| Delegation grant and validation models | `specs/delegation-model.md`; `specs/delegation-validation.md`; Sprint 2E requirements | `src/echoauth/auth/delegation_models.py` | `tests/test_delegation.py` | `api/openapi.yaml`; `database/schema.sql`; `contracts/service-contracts.yaml` |
| Grant validation and evidence hashing | `specs/delegation-model.md` | `src/echoauth/auth/delegation_validation.py` | Grant scope expansion and deterministic validation tests | `contracts/ambiguities.md`; `contracts/decision-log.md`; `src/echoauth/canonical.py` |
| Delegation persistence and lifecycle | `specs/delegation-model.md` | `src/echoauth/auth/delegation_repository.py` | Valid, revoked, expired, and audit-history tests | `database/schema.sql`; `src/echoauth/auth/authority_registry.py` |
| Authority Resolution integration | `specs/delegation-model.md`; `specs/authority-resolution.md` | `InMemoryDelegationRepository`; `AuthorityResolutionResult`; `AuthorityRepository` | Valid grant creation, authority-scope expansion rejection, and revoked-grantor tests | `src/echoauth/auth/authority_resolution.py`; `src/echoauth/auth/authority_registry.py` |
| Runtime delegation validation | `specs/delegation-validation.md` | `src/echoauth/auth/delegation_service.py` | All Sprint 2E outcome tests | `api/openapi.yaml`; `contracts/service-contracts.yaml` |
| Delegation audit integration | `specs/delegation-model.md`; `specs/delegation-validation.md`; `specs/audit-chain.md` | `src/echoauth/auth/delegation_repository.py`; `src/echoauth/auth/delegation_service.py`; `src/echoauth/audit/repository.py` | Audit-history chaining and deterministic audit-idempotency tests | `schemas/audit-record.schema.json`; `events/event-catalog.yaml` |

# Sprint 2F Implementation Traceability

| Sprint 2F Component | Evidence Source | Runtime Artifact | Test Artifact | Contracts Consumed |
| --- | --- | --- | --- | --- |
| Policy rule and evaluation models | `specs/policy-registry.md`; `specs/policy-engine.md`; `specs/policy-evaluation.md`; Sprint 2F requirements | `src/echoauth/policy/models.py` | `tests/test_policy_evaluation.py` | `api/openapi.yaml`; `contracts/service-contracts.yaml`; `contracts/ambiguities.md` |
| Policy validation and hashing | `specs/policy-registry.md`; `specs/policy-engine.md` | `src/echoauth/policy/validation.py` | Policy registration and all evaluation fixtures | `contracts/decision-log.md`; `src/echoauth/canonical.py` |
| Policy repository and lifecycle | `specs/policy-registry.md` | `src/echoauth/policy/repository.py` | Expired and revoked policy tests | `database/schema.sql`; `src/echoauth/audit/repository.py` |
| Deterministic matching and priority | `specs/policy-engine.md`; `specs/policy-evaluation.md` | `src/echoauth/policy/service.py` | Authorized, denied, conflict, priority, invalid-policy, and deterministic tests | `contracts/service-contracts.yaml`; `api/openapi.yaml` |
| Authority and delegation integration | `specs/policy-evaluation.md`; `specs/authority-resolution.md`; `specs/delegation-validation.md` | `PolicyEvaluationService._validate_dependencies` | Direct authority and valid delegation tests | `src/echoauth/auth/authority_resolution.py`; `src/echoauth/auth/delegation_models.py` |
| Policy audit integration | `specs/policy-registry.md`; `specs/policy-evaluation.md`; `specs/audit-chain.md` | `src/echoauth/policy/repository.py`; `src/echoauth/policy/service.py` | Deterministic evaluation and audit-idempotency test | `schemas/audit-record.schema.json`; `events/event-catalog.yaml` |

# Sprint 2G Implementation Traceability

| Sprint 2G Component | Evidence Source | Runtime Artifact | Test Artifact | Contracts Consumed |
| --- | --- | --- | --- | --- |
| Authorization request and decision models | `specs/echoauth-spec.md`; Sprint 2G requirements | `src/echoauth/auth/authorization_gate.py` | `tests/test_authorization_gate.py` | `api/openapi.yaml`; `schemas/common.schema.json`; `contracts/service-contracts.yaml` |
| Identity dependency | `specs/identity-resolution.md`; `specs/echoauth-spec.md` | `AuthorizationGateService`; `RegistryIdentityService` | Successful, delegated-success, and identity-failure tests | `src/echoauth/identity/service.py`; `src/echoauth/models.py` |
| Authority dependency | `specs/authority-resolution.md`; `specs/echoauth-spec.md` | `AuthorizationGateService`; `AuthorityResolutionService` | Successful, delegated-success, authority-failure, revoked, and expired tests | `src/echoauth/auth/authority_resolution.py` |
| Delegation dependency | `specs/delegation-validation.md`; `specs/echoauth-spec.md` | `AuthorizationGateService`; `DelegationValidationService`; `DelegationRepository` | Delegated-success and delegation-failure tests | `src/echoauth/auth/delegation_service.py`; `src/echoauth/auth/delegation_repository.py` |
| Policy dependency | `specs/policy-evaluation.md`; `specs/echoauth-spec.md` | `AuthorizationGateService`; `PolicyEvaluationService` | Successful, denial, conflict, expired, and deterministic tests | `src/echoauth/policy/service.py` |
| Decision evidence and audit | `specs/echoauth-spec.md`; `specs/audit-record.md`; `specs/audit-chain.md` | `AuthorizationDecision`; `AuthorizationGateService._complete` | Evidence-order, component-reference, deterministic-decision, and audit-idempotency assertions | `schemas/audit-record.schema.json`; `events/event-catalog.yaml` |

# Sprint 2H Implementation Traceability

| Sprint 2H Component | Evidence Source | Runtime Artifact | Test Artifact | Contracts Consumed |
| --- | --- | --- | --- | --- |
| Refusal request, reason, and decision models | `specs/refusal-engine.md`; Sprint 2H requirements | `src/echoauth/policy/refusal_models.py` | `tests/test_refusal_service.py` | `contracts/ambiguities.md`; `src/echoauth/auth/authorization_models.py` |
| Versioned refusal mapping | `specs/refusal-engine.md`; `governance/refusal-first.md` | `REFUSAL_MAPPING_VERSION`; `RefusalService`; `_map_authorization_decision` | All category mapping tests | Sprint 2G authorization outcomes |
| Dependency-aware explanation | Sprint 2G evidence packages; `specs/refusal-engine.md` | `refusal_request_from_decision`; `RefusalService.refuse` | Identity, authority, delegation, policy, revoked, expired, and conflict tests | `src/echoauth/auth/authorization_models.py` |
| Structured refusal evidence | `specs/refusal-engine.md`; `contracts/decision-log.md` | `RefusalReason`; redacted evidence package in `RefusalService` | Deterministic evidence assertion | `src/echoauth/canonical.py`; `schemas/common.schema.json` |
| Refusal audit integration | `specs/refusal-engine.md`; `specs/audit-record.md`; `specs/audit-chain.md` | `RefusalService`; `InMemoryAuditLogRepository` | Deterministic refusal and audit-idempotency test | `schemas/audit-record.schema.json`; `events/event-catalog.yaml` |

# Sprint 2I Implementation Traceability

| Sprint 2I Component | Evidence Source | Runtime Artifact | Test Artifact | Contracts Consumed |
| --- | --- | --- | --- | --- |
| Escalation request, reason, and decision models | `specs/escalation-engine.md`; Sprint 2I requirements | `src/echoauth/governance/escalation_models.py` | `tests/test_escalation_service.py` | `contracts/service-contracts.yaml`; `contracts/ambiguities.md` |
| Authorization and refusal integration | Sprint 2G and Sprint 2H runtime decision models | `EscalationService._validate_dependencies` | Refusal, authorized-decision rejection, and mismatched-evidence tests | `src/echoauth/auth/authorization_models.py`; `src/echoauth/policy/refusal_models.py` |
| Deterministic escalation classification | `specs/escalation-engine.md`; Sprint 2I canonical categories | `ESCALATION_MAPPING_VERSION`; `EscalationService`; `_classify` | Conflict, revoked, expired, unavailable-dependency, explicit-route, no-route, and deterministic tests | Sprint 2I requirements |
| Structured escalation evidence | `specs/escalation-engine.md`; `contracts/decision-log.md` | Immutable evidence package in `EscalationService.escalate` | Audit evidence packaging and deterministic tests | `src/echoauth/canonical.py`; `schemas/common.schema.json` |
| Escalation audit integration | `specs/escalation-engine.md`; `specs/audit-record.md`; `specs/audit-chain.md` | `EscalationService`; `InMemoryAuditLogRepository` | Audit-chain evidence and idempotency assertions | `schemas/audit-record.schema.json`; `events/event-catalog.yaml` |

# Sprint 2J Implementation Traceability

| Sprint 2J Component | Evidence Source | Runtime Artifact | Test Artifact | Contracts Consumed |
| --- | --- | --- | --- | --- |
| Review request, outcome, assignment, and decision models | `specs/escalation-engine.md`; Sprint 2J requirements | `src/echoauth/governance/review_models.py` | `tests/test_review_service.py` | Sprint 2I escalation decision model; `contracts/ambiguities.md` |
| Escalation-only integration | `specs/escalation-engine.md`; Sprint 2J constraints | `ReviewService._validate_escalation` | Escalation consumption and evidence tests | `src/echoauth/governance/escalation_models.py` |
| Deterministic reviewer assignment | `specs/escalation-engine.md`; Sprint 2J requirements | `ReviewerAssignment`; `ReviewService._assign_reviewer`; `_validate_assignments` | Configured-order, unresolved, and non-assigned-reviewer tests | Constructor-supplied ordered assignment configuration |
| Review outcome recording | Sprint 2J canonical outcomes | `ReviewOutcome`; `ReviewService.review` | Approval, denial, information-return, delegated-review, and unresolved tests | Sprint 2J requirements |
| Structured review evidence | `specs/escalation-engine.md`; `contracts/decision-log.md` | Immutable evidence package in `ReviewService.review` | Audit evidence and idempotency tests | `src/echoauth/canonical.py`; `schemas/common.schema.json` |
| Review audit integration | `specs/escalation-engine.md`; `specs/audit-record.md`; `specs/audit-chain.md` | `ReviewService`; `InMemoryAuditLogRepository` | Audit-chain evidence and idempotency assertions | `schemas/audit-record.schema.json`; `events/event-catalog.yaml` |

# Sprint 2K Implementation Traceability

| Sprint 2K Component | Evidence Source | Runtime Artifact | Test Artifact | Contracts Consumed |
| --- | --- | --- | --- | --- |
| Override request, reason, evidence, decision, and authority models | `specs/emergency-override-controls.md`; Sprint 2K requirements | `src/echoauth/governance/override_models.py` | `tests/test_override_service.py` | `contracts/service-contracts.yaml`; `contracts/ambiguities.md` |
| Complete upstream evidence consumption | Sprint 2G authorization, Sprint 2H refusal, Sprint 2I escalation, and Sprint 2J review models | `OverrideService._validate_evidence_chain` | Approval fixture, inconsistent-chain rejection, and evidence tests | Runtime decision models from Sprints 2G-2J |
| Explicit override authority validation | `specs/emergency-override-controls.md`; Sprint 2K requirements | `OverrideAuthority`; `_validate_authorities`; `OverrideService._authority_is_valid` | Approval and absent-authority tests | Constructor-supplied authority configuration |
| Deterministic override classification | `specs/emergency-override-controls.md`; Sprint 2K outcomes | `OverrideOutcome`; `_classify`; `OverrideService.decide` | Approval, denial, deferral, expiration, and idempotency tests | Sprint 2J review outcomes |
| Immutable override evidence | `specs/emergency-override-controls.md`; `contracts/decision-log.md` | `OverrideEvidence`; immutable effective scope; evidence hash | Immutable evidence and audit test | `src/echoauth/canonical.py`; `schemas/common.schema.json` |
| Override audit integration | `specs/emergency-override-controls.md`; `specs/audit-record.md`; `specs/audit-chain.md` | `OverrideService`; `InMemoryAuditLogRepository` | Audit-chain evidence and idempotency assertions | `schemas/audit-record.schema.json`; `events/event-catalog.yaml` |

# Sprint 2L Implementation Traceability

| Sprint 2L Component | Evidence Source | Runtime Artifact | Test Artifact | Contracts Consumed |
| --- | --- | --- | --- | --- |
| Runtime state and transition models | `specs/runtime-state-machine.md`; `specs/authorization-states.md`; Sprint 2L vocabulary | `src/echoauth/runtime/state_models.py` | `tests/test_runtime_state_machine.py` | `contracts/service-contracts.yaml`; `contracts/protobuf/echoauth.proto` |
| Explicit versioned state graph | Sprint 2L canonical states; repository runtime transition rules | `RUNTIME_STATE_GRAPH`; `RUNTIME_STATE_GRAPH_VERSION` | Canonical-vocabulary and all-33-edges tests | Sprint 2L requirements; `specs/runtime-state-machine.md` |
| Deterministic fail-closed validation | `specs/runtime-state-machine.md` | `RuntimeStateMachine.validate`; `validate_transition_request` | Valid path, undefined transition, target mismatch, blocked release, and expired-terminal tests | `schemas/common.schema.json`; `src/echoauth/canonical.py` |
| Immutable transition evidence | `specs/runtime-state-machine.md`; `contracts/decision-log.md` | `RuntimeStateEvidence`; evidence hash in `RuntimeTransitionDecision` | Mutation rejection and deterministic evidence assertions | `src/echoauth/canonical.py`; `schemas/common.schema.json` |
| Transition audit integration | `specs/runtime-state-machine.md`; `specs/audit-record.md`; `specs/audit-chain.md` | `RuntimeStateMachine`; `InMemoryAuditLogRepository` | Accepted/rejected audit evidence and idempotency assertions | `schemas/audit-record.schema.json`; `events/event-catalog.yaml` |

# Sprint 2A Implementation Traceability

| Sprint 2A Component | Evidence Source | Runtime Artifact | Test Artifact | Contracts Consumed |
| --- | --- | --- | --- | --- |
| Audit record validation | `specs/audit-record.md`; `specs/audit-log-spec.md` | `src/echoauth/audit/hashing.py`; `AuditRecord` | `tests/test_audit_append.py` | `schemas/audit-record.schema.json` |
| Deterministic event hashing | `specs/audit-chain.md`; `contracts/decision-log.md` | `hash_audit_event`; `AUDIT_HASH_FORMAT` | Stable equivalent-payload hash test | Canonical JSON and SHA-256 contracts |
| Append-only repository and chain sequencing | `specs/audit-chain.md`; `specs/audit-log-spec.md` | `src/echoauth/audit/repository.py`; `InMemoryAuditLogRepository` | Append, previous-hash, conflict, and immutable-storage tests | `database/schema.sql`; `schemas/audit-record.schema.json` |
| Sprint 2A evidence | `runtime/sprint-2a-implementation-evidence.md` | Audit foundation only | 6 focused tests | No signing, external keys, event delivery, or production adapter |

# Sprint 2M Implementation Traceability

| Sprint 2M Component | Evidence Source | Runtime Artifact | Test Artifact | Contracts Consumed |
| --- | --- | --- | --- | --- |
| Execution request, decision, evidence, constraint, and outcome models | `specs/execution-claims.md`; `specs/runtime-halt-model.md`; Sprint 2M requirements | `src/echoauth/execution/models.py` | `tests/test_execution_control.py` | `contracts/service-contracts.yaml`; `contracts/ambiguities.md` |
| Runtime State Machine decision integration | Sprint 2L validation-only contract | `ExecutionControl._validate_runtime_decision` | Direct, override, rejected, blocked, invalid, expired, and halted state tests | `src/echoauth/runtime/state_models.py` |
| Configured execution constraints | Sprint 2M `ExecutionConstraint`; fail-closed requirements | `_validate_constraints`; `_validate_constraint`; `ExecutionControl.validate` | Configured enabled/disabled, expired, evidence-required, and unconfigured tests | Constructor-supplied immutable constraints |
| Deterministic eligibility classification | Sprint 2M canonical outcomes | `ExecutionOutcome`; `_classify`; `ExecutionControl.validate` | All seven outcome tests | Sprint 2M requirements; `specs/runtime-halt-model.md` |
| Authority and governance evidence validation | Sprint 2M requirements; Sprint 2G-2K evidence fields | `_evidence_has`; required-path checks; `ExecutionEvidence` | Missing authority, missing path evidence, and complete override-path tests | Runtime evidence IDs/hashes from Sprints 2G-2K |
| Immutable execution evidence and audit | `specs/audit-record.md`; `specs/audit-chain.md`; Sprint 2M requirements | `ExecutionEvidence`; `ExecutionControl`; `InMemoryAuditLogRepository` | Mutation rejection, audit linkage, and idempotency tests | `src/echoauth/canonical.py`; `schemas/audit-record.schema.json` |

# Sprint 2N Implementation Traceability

| Sprint 2N Component | Evidence Source | Runtime Artifact | Test Artifact | Contracts Consumed |
| --- | --- | --- | --- | --- |
| Invariant request and result models | `specs/invariant-validator.md`; OpenAPI invariant schemas | `src/echoauth/governance/invariant_models.py` | `tests/test_invariant_validator.py` | `api/openapi.yaml`; `contracts/service-contracts.yaml`; `database/schema.sql` |
| Immutable versioned definitions | `specs/invariant-validator.md` deterministic and security requirements | `InvariantRule`; `InvariantSet`; `_validate_sets`; `_definition_hash` | Definition-detachment, duplicate-rule, and stable-order tests | `contracts/ambiguities.md`; `src/echoauth/canonical.py` |
| Deterministic invariant evaluation | `specs/invariant-validator.md` state machine and failure conditions | `InvariantService.validate`; `_evaluate` | Valid, invalid, hold, halt, critical-precedence, missing-fact, unknown-version, and inactive-version tests | Canonical facts contract; configured invariant sets |
| Facts and result hashing | `specs/invariant-validator.md`; `contracts/decision-log.md` | `facts_hash`; `definition_hash`; deterministic result identifier | Equivalent-facts and idempotency tests | `schemas/common.schema.json`; `src/echoauth/canonical.py` |
| Invariant audit integration | `specs/invariant-validator.md`; `specs/audit-record.md`; `specs/audit-chain.md` | `InvariantService`; `InMemoryAuditLogRepository` | Audit result and duplicate-append assertions | `events/event-catalog.yaml#invariant.result`; `schemas/audit-record.schema.json` |

# Sprint 2O Implementation Traceability

| Sprint 2O Component | Evidence Source | Runtime Artifact | Test Artifact | Contracts Consumed |
| --- | --- | --- | --- | --- |
| Halt request, outcome, decision, and evidence models | `specs/runtime-halt-model.md`; Sprint 2O approved causes | `src/echoauth/runtime/halt_models.py` | `tests/test_halt_decision.py` | `contracts/service-contracts.yaml`; `contracts/ambiguities.md` |
| Cause-specific structural validation | `specs/runtime-halt-model.md` validation and failure conditions | `validate_halt_request`; `_validate_cause_evidence` | All cause fixtures and malformed-evidence test | Canonical evidence contract; Sprint 2L-2N evidence field names |
| Deterministic halt classification | `specs/runtime-halt-model.md` state machine and deterministic rules | `HaltDecisionService.decide`; `_classify`; `_CAUSE_CLASSIFICATION` | Missing authority/evidence, invalid state, invariant, dependency, override, execution, and criticality tests | Sprint 2O approved cause list |
| Immutable halt evidence | `specs/runtime-halt-model.md`; `contracts/decision-log.md` | `HaltDecisionEvidence`; canonical source evidence hash | Mutation rejection and equivalent-evidence tests | `src/echoauth/canonical.py`; `schemas/common.schema.json` |
| Halt audit integration | `specs/runtime-halt-model.md`; `specs/audit-record.md`; `specs/audit-chain.md` | `HaltDecisionService`; `InMemoryAuditLogRepository` | Audit linkage and idempotency tests | `schemas/audit-record.schema.json`; event delivery intentionally not implemented |

# Sprint 2P-Prep Contract Traceability

| Contract Component | Evidence Source | Contract Artifact | Validation Artifact | Runtime Effect |
| --- | --- | --- | --- | --- |
| Recovery request and result | `specs/runtime-recovery.md`; ADR-0007 | `schemas/recovery-request.schema.json`; `schemas/recovery-result.schema.json` | `src/echoauth/contracts/validation.py`; `tests/test_contract_validation.py` | None; schemas define evidence only |
| Failure-code policy and guard evidence | Halt, invariant, execution-control, and audit evidence contracts | `contracts/recovery-service.yaml`; `schemas/recovery-request.schema.json#/$defs/GuardEvidence` | Registered YAML and JSON parsing | None; deterministic policy contract only |
| Recovery Review Protocol | Review Decision evidence; explicit recovery authority requirement | `schemas/recovery-review-protocol.schema.json` | JSON contract validation | Separate Recovery protocol; no general Review outcome and no authorization |
| `HOLD` governance proposal | Sprint 2O `hold` outcome; Sprint 2L `EXECUTION_BLOCKED` state | `schemas/governance-runtime-proposal.schema.json` | JSON contract validation | Proposal only; no transition or mutation |
| Recovery vocabulary decision | Sprint 2L; Sprint 2O; Recovery governance review | `contracts/decision-log.md#ADR-0007` | Traceability review | Reconciled before the separate Sprint 2P eligibility-only implementation |

# Sprint 2P Implementation Traceability

| Sprint 2P Component | Evidence Source | Runtime Artifact | Test Artifact | Runtime Effect |
| --- | --- | --- | --- | --- |
| Typed request, result, protocol, state, failure, path, and outcome models | `specs/runtime-recovery.md`; Recovery JSON Schemas | `src/echoauth/runtime/recovery_models.py` | `tests/test_recovery_eligibility.py` | Immutable eligibility artifacts only |
| Failure-code policy validation | `contracts/recovery-service.yaml#/failure_code_policy` | `_FAILURE_POLICY`; `_classify`; `_guards_satisfied` | Entry-state, policy-branch, guard, and halted-default tests | Produces only `revalidation_required`, `rejected`, or `new_request_required` |
| Authority and review evidence binding | `specs/authority-resolution.md`; `schemas/recovery-review-protocol.schema.json` | `_authority_failure`; `_review_failure`; `recovery_review_protocol_hash` | Invalid authority, required/missing protocol, and fully bound protocol tests | Evidence validation only; no authorization or general Review outcome |
| Halt and original-failure preservation | `specs/runtime-halt-model.md`; `specs/audit-record.md`; `specs/audit-chain.md` | `_halt_failure`; `_audit_link_failure` | Audit mismatch and unchanged-source-record tests | Reads source audit evidence; never rewrites it |
| Eligibility audit and idempotency | `contracts/recovery-service.yaml#/required_audit_records` | `RecoveryEligibilityService.validate` | Exact event-type, no-`runtime.recovered`, linkage, and duplicate-call tests | Appends only `recovery.eligibility.requested` and `recovery.eligibility.decided` |
