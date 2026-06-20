# Sprint 2 Kickoff Brief

# Evidence Base

This kickoff brief uses only repository artifacts:

- `runtime/sprint-1-implementation-evidence.md`
- `runtime/implementation-sequencing-report.md`
- `runtime/coverage-report.md`
- `runtime/traceability-matrix.md`
- `contracts/service-contracts.yaml`
- `contracts/integration-contracts.yaml`
- `schemas/audit-record.schema.json`
- `database/schema.sql`
- `events/event-catalog.yaml`
- `events/event-envelope.schema.json`
- `specs/audit-record.md`
- `specs/audit-chain.md`
- `specs/audit-log-spec.md`
- `src/echoauth/audit/logging.py`
- `src/echoauth/interfaces.py`
- `src/echoauth/models.py`
- `src/echoauth/repositories.py`
- Sprint 1 foundations under `src/echoauth/canonical.py`,
  `src/echoauth/persistence/base.py`, and `src/echoauth/events_validation.py`

# 1. First Sprint 2 Component

Audit append adapter.

Evidence:

- `runtime/implementation-sequencing-report.md` lists Sprint 2 Audit as the
  first workstream: "Audit append adapter and audit repository implementation."
- `runtime/coverage-report.md` lists `AuditService`, `AuditRecord`, and
  `AuditLogRepository` as skeleton/interface coverage only.
- `src/echoauth/audit/logging.py` exports the audit interfaces but contains no
  append implementation.

# 2. Purpose

Implement the first real EchoAuth runtime behavior after Sprint 1 foundation
closure: append contract-shaped audit records, persist hash-bound audit fields,
and prepare the audit boundary required by later identity, authority,
delegation, policy, refusal, invariant, runtime state, envelope, token, claim,
halt, and recovery work.

The adapter must not implement identity, authority, delegation, policy,
invariant, runtime envelope, token, execution, emergency override, or
notification behavior.

# 3. Inputs

| Input | Source |
| --- | --- |
| `AuditRecord` | `src/echoauth/models.py`; `schemas/audit-record.schema.json`; `specs/audit-record.md` |
| `event_type` | `schemas/audit-record.schema.json`; `specs/audit-record.md` |
| `actor_id` | `schemas/audit-record.schema.json`; `specs/audit-record.md` |
| `request_id` | `schemas/audit-record.schema.json`; `database/schema.sql` |
| `envelope_id` | `schemas/audit-record.schema.json`; `database/schema.sql` |
| `authority_verdict_id` | `schemas/audit-record.schema.json`; `database/schema.sql` |
| `execution_token_id` | `schemas/audit-record.schema.json`; `database/schema.sql` |
| `state_before` | `schemas/audit-record.schema.json`; `database/schema.sql` |
| `state_after` | `schemas/audit-record.schema.json`; `database/schema.sql` |
| `reason` | `schemas/audit-record.schema.json`; `specs/audit-record.md` |
| `details` | `schemas/audit-record.schema.json`; `contracts/ambiguities.md` |
| `occurred_at` | `schemas/audit-record.schema.json`; `specs/audit-record.md` |

# 4. Outputs

| Output | Source |
| --- | --- |
| `audit_event_id` | `specs/audit-record.md`; `database/schema.sql` |
| `event_hash` | `specs/audit-record.md`; `specs/audit-chain.md`; `database/schema.sql` |
| `previous_hash` | `specs/audit-record.md`; `specs/audit-chain.md`; `database/schema.sql` |
| `storage_state` | `specs/audit-record.md`; `database/schema.sql`; `contracts/service-contracts.yaml#audit_service` |
| persisted audit event row | `database/schema.sql#audit_events` |
| optional `audit.record` event envelope | `events/event-catalog.yaml`; `events/event-envelope.schema.json` |

# 5. Consumed Contracts

| Contract | Use |
| --- | --- |
| `schemas/audit-record.schema.json` | Required input shape for audit records. |
| `contracts/service-contracts.yaml` | Declares `audit_service` input `AuditRecord`, output `AuditRecordResult`, and terminal states `accepted`, `rejected`, `degraded`. |
| `database/schema.sql` | Defines `audit_events` persistence columns. |
| `events/event-catalog.yaml` | Defines `audit.record` payload schema mapping. |
| `events/event-envelope.schema.json` | Defines event envelope shape if audit append emits event bus records. |
| `contracts/ambiguities.md` | Resolves `details` as `CanonicalJsonObject`. |
| `contracts/decision-log.md` | Defines canonical object/list decisions used by Sprint 1 canonical utilities. |
| `specs/audit-record.md` | Defines audit record purpose, inputs, outputs, state machine, validation, failure, security, audit, persistence, and deterministic rules. |
| `specs/audit-chain.md` | Defines hash-chain sequencing and deterministic hashing rules. |
| `specs/audit-log-spec.md` | Defines append-only audit log interface and append outcomes. |

# 6. Produced Contracts

Sprint 2 should produce implementation artifacts, not new governance concepts.
The expected produced implementation contracts are:

| Produced Contract | Expected Location |
| --- | --- |
| Audit append result model or dataclass aligned to `AuditRecordResult`. | `src/echoauth/audit/logging.py` or `src/echoauth/models.py` if promoted to shared model. |
| Audit append adapter class implementing `AuditService.append`. | `src/echoauth/audit/logging.py` or a new audit adapter module. |
| Audit repository implementation using Sprint 1 persistence foundation. | New audit persistence module or `src/echoauth/audit/logging.py`, depending on final implementation design. |
| Audit append tests as executable contract evidence. | `tests/test_audit_logging.py`; `tests/integration/test_sprint2_audit_append.py`. |

# 7. Repository Files To Create

| File | Purpose |
| --- | --- |
| `tests/test_audit_logging.py` | Unit tests for audit record validation, append result shape, canonical hash behavior, and failure conditions. |
| `tests/integration/test_sprint2_audit_append.py` | Integration tests proving audit append consumes Sprint 1 canonical, persistence, and event validation foundations. |
| Optional: `src/echoauth/audit/result.py` | Only if `AuditRecordResult` is separated from `logging.py`; must map to `contracts/service-contracts.yaml`. |
| Optional: `src/echoauth/audit/repository.py` | Only if audit persistence is separated from `logging.py`; must consume `database/schema.sql` and existing repository interfaces. |

# 8. Repository Files To Modify

| File | Modification |
| --- | --- |
| `src/echoauth/audit/logging.py` | Replace interface-only export with audit append adapter surface while preserving exported `AuditService`, `AuditRecord`, and `AuditLogRepository`. |
| `src/echoauth/models.py` | Add `AuditRecordResult` only if shared runtime models require it. |
| `src/echoauth/__init__.py` | Export new audit result/adapter only if it becomes a stable public runtime API. |
| `runtime/coverage-report.md` | Mark audit append adapter implementation coverage after tests pass. |
| `runtime/traceability-matrix.md` | Add Sprint 2 audit append implementation traceability. |
| `runtime/sprint-1-implementation-evidence.md` | Do not modify unless referencing Sprint 1 closure remains necessary; Sprint 2 evidence should be separate. |

# 9. Unit Tests Required

| Test Area | Required Tests |
| --- | --- |
| Required fields | Missing `event_type`, `actor_id`, `reason`, `details`, or `occurred_at` rejects deterministically. |
| Canonical details | `details` must be a canonical JSON object and use Sprint 1 canonical serialization. |
| Event hash | Same audit payload and previous hash produce same hash. |
| Previous hash | Append result includes previous hash value when available. |
| Storage state | Accepted records return `accepted`; invalid records return or raise deterministic `rejected`; storage degradation path is represented without inventing runtime halt behavior. |
| Persistence shape | Stored records include `audit_event_id`, `event_type`, `actor_id`, `reason`, `details_json`, `occurred_at`, `event_hash`, `previous_hash`, and `storage_state`. |
| No cross-service behavior | Audit append tests must not resolve identity, authority, delegation, policy, invariants, tokens, execution, emergency override, or notification delivery. |

# 10. Integration Tests Required

| Integration Test | Required Coverage |
| --- | --- |
| Audit append through persistence foundation | Append an `AuditRecord`, persist it through Sprint 1 repository foundation, and retrieve the stored result. |
| Audit record canonical hash | Verify canonical details serialization participates in stable event hash creation. |
| Audit event catalog mapping | Verify `audit.record` resolves to `../schemas/audit-record.schema.json` using `events/event-catalog.yaml`. |
| Audit append and event envelope validation | If an event envelope is emitted, validate it with `events/event-envelope.schema.json` and `src/echoauth/events_validation.py`. |
| Contract validation still passes | Full Sprint 1 test suite remains green after audit append implementation. |

# 11. Acceptance Criteria

| Criterion | Required Result |
| --- | --- |
| Audit append adapter exists. | `AuditService.append` has a concrete Sprint 2 implementation path without changing unrelated service interfaces. |
| Audit input follows contract. | Input uses `AuditRecord` fields from `schemas/audit-record.schema.json`. |
| Audit output follows contract. | Output includes `audit_event_id`, `event_hash`, `previous_hash`, and `storage_state` aligned to `specs/audit-record.md` and `contracts/service-contracts.yaml`. |
| Canonical hashing is deterministic. | Same canonical audit record and previous hash produce the same event hash. |
| Persistence uses repository evidence. | Stored audit fields align to `database/schema.sql#audit_events`. |
| Event mapping is respected. | `audit.record` uses `events/event-catalog.yaml` and `schemas/audit-record.schema.json`. |
| Sprint 1 remains closed. | Existing 28 Sprint 1 tests still pass. |
| No Sprint 3 or later behavior appears. | No identity, authority, delegation, policy, invariant, envelope, token, execution, emergency override, notification delivery, or runtime orchestrator behavior is implemented. |

# 12. Definition Of Done

Sprint 2 audit append kickoff scope is done when:

- audit append implementation exists and maps to `AuditService.append`,
- all audit append unit tests pass,
- all audit append integration tests pass,
- the full Sprint 1 suite still passes,
- audit append produces contract-shaped results,
- audit records persist fields required by `database/schema.sql`,
- event hash behavior follows canonical deterministic rules from
  `specs/audit-record.md` and `specs/audit-chain.md`,
- `audit.record` event mapping is validated against `events/event-catalog.yaml`,
- traceability and coverage reports are updated,
- and no non-audit Sprint 2 work or later runtime behavior is implemented.
