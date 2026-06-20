# Sprint 2C Implementation Evidence

# Scope

Sprint 2C implements only the canonical Authority Registry foundation:

- explicit authority record artifacts,
- deterministic authority validation and evidence hashing,
- append-history in-memory authority persistence,
- active, suspended, revoked, and expired lifecycle states,
- authority revocation,
- immutable evidence storage,
- Sprint 2A audit-chain integration.

Authority resolution, delegation, policy, authorization decisions, envelopes,
tokens, execution, institutional override, and runtime orchestration are not
implemented.

# Implementation Evidence

| Component | Runtime Evidence | Test Evidence |
| --- | --- | --- |
| Authority models and categories | `src/echoauth/auth/authority_models.py` | All six categories are registered by `test_valid_authority_creation_supports_all_categories` |
| Validation and evidence integrity | `src/echoauth/auth/authority_validation.py` | Invalid scope, dates, and evidence hashes reject before persistence or audit |
| Deterministic evidence hashing | `src/echoauth/auth/authority_validation.py` | Equivalent canonical scopes produce identical, reproducible hashes |
| Authority repository | `src/echoauth/auth/authority_registry.py` | Creation, retrieval, immutable storage, and duplicate/conflict paths |
| Lifecycle and revocation | `src/echoauth/auth/authority_registry.py` | Suspend, reactivate, expire, revoke, and terminal-state tests |
| Audit integration | `src/echoauth/auth/authority_registry.py`; `src/echoauth/audit/repository.py` | Audit-gated writes, audited retrieval, and previous-hash chain integrity tests |

# Deterministic Rules Implemented

- Authority exists only as an explicit `AuthorityRecord`.
- The registry does not consume or inspect actor type, identity status,
  assurance, request ownership, execution actors, affiliation, credentials, or
  identity verdicts.
- Evidence hashes bind authority record ID, source ID, subject ID, category,
  scope, priority, issue/expiration times, and source-document hash.
- Lifecycle status is excluded from immutable source-evidence hashing; status
  transitions preserve the original evidence hash.
- Scope is detached, recursively immutable, canonically serialized, and
  reproducibly hashed.
- Equal-priority active records for the same subject reject while policy
  resolution is unavailable.
- A failed audit append prevents the authority mutation from becoming visible.

# Test Evidence

Command:

```text
$env:PYTHONPATH='src'; python -B -m unittest discover -s tests
```

Result:

```text
Ran 58 tests in 0.104s

OK
```

The result includes all Sprint 1, Sprint 2A, Sprint 2B, and 11 Sprint 2C tests.

# Deferred Dependencies

- Authority resolution and authority verdict generation.
- Administrative or root-authority mutation authorization. The in-memory
  repository is a storage boundary and must not be exposed as a public write
  service until that decision boundary exists.
- Delegated authority execution and grant-chain validation.
- Policy-based priority and precedence resolution.
- Nested action/resource/context scope matching.
- Institutional override and emergency override behavior.
- Production database persistence and distributed revocation propagation.

# Contract Ambiguities Discovered

| Ambiguity | Sprint 2C handling |
| --- | --- |
| `specs/authority-registry.md` uses `court` and `service`; OpenAPI/common contracts use `delegate` and `system`; Sprint 2C requires `delegated` and `runtime-service`. | Runtime model follows the explicit Sprint 2C category list. Generated contract reconciliation is deferred. |
| Sprint 2C requires `evidence_hash`, while `database/schema.sql#authority_records` defines only optional `source_document_hash`. | In-memory model stores both. Production database mapping is blocked pending schema reconciliation. |
| Authority scope is a canonical object without nested matching rules. | Validate structure, canonical serialization, immutability, and hashing only. No authorization inference is implemented. |
| Registry writes require administrative/root authority, but the authority decision boundary is deferred. | Capture actor and audit evidence; keep repository as an internal persistence boundary and defer public mutation authorization. |
| Audit-record rules refer to `authority_verdict_id` for authority events, but registry events occur before any verdict exists. | Registry audit details bind `authority_record_id` and evidence hash; verdict linkage remains deferred to authority resolution. |

# Status

Sprint 2C Authority Registry foundation: complete with documented contract
reconciliation dependencies.
