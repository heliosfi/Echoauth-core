# Sprint 2H Implementation Evidence

# Scope

Sprint 2H implements only the canonical Refusal Service foundation:

- typed `RefusalRequest`, `RefusalReason`, and `RefusalDecision` artifacts,
- versioned deterministic failure mapping,
- dependency-aware refusal classification,
- structured and redacted refusal evidence,
- immutable refusal decisions,
- in-process idempotency,
- Sprint 2A audit-chain integration.

The service does not change, retry, override, or re-evaluate authorization. It
does not implement escalation, review, execution blocking, recovery,
orchestration, envelopes, or mutation authorization.

# Implementation Evidence

| Component | Runtime Evidence | Test Evidence |
| --- | --- | --- |
| Refusal models | `src/echoauth/policy/refusal_models.py` | All Sprint 2H fixtures and category assertions |
| Request construction | `refusal_request_from_decision` | Every test begins with an immutable `AuthorizationDecision` |
| Versioned mapping | `REFUSAL_MAPPING_VERSION`; `_map_authorization_decision` | Identity, authority, delegation, policy, revoked, expired, conflict, and malformed tests |
| Structured evidence | `RefusalService.refuse` | Deterministic test verifies authorization evidence hash linkage |
| Audit integration | `RefusalService.refuse`; `InMemoryAuditLogRepository` | Repeated refusal does not duplicate audit evidence |

# Deterministic Processing

- Authorized decisions cannot produce refusal records.
- Request, authorization decision ID, outcome, failure code, and failure source
  must agree; mismatches map to `malformed_request`.
- Dependency exceptions represented by `*_dependency_failed` reasons map to
  `unavailable_dependency`.
- Identity, authority, delegation, policy denial, revocation, expiration, and
  conflict map through a fixed versioned table.
- Refusal evidence stores hashes and identifiers, not raw authorization
  credentials, payloads, or context.
- The original authorization decision is never mutated.
- Repeated translation of identical evidence returns the same immutable refusal
  and does not duplicate audit evidence.

# Test Evidence

Command:

```text
$env:PYTHONPATH='src'; python -B -m unittest discover -s tests
```

Result:

```text
Ran 104 tests in 0.158s

OK
```

The result includes all prior Sprint tests and 9 Sprint 2H refusal tests.

# Deferred Dependencies

- Runtime-state refusal, hold, halt, revoked, or escalated transitions.
- Escalation and human review.
- Override handling.
- Execution blocking and execution recovery.
- Runtime orchestration and envelopes.
- Persistent refusal storage and signed authorization-decision verification.
- Mutation authorization and API/protobuf adapters.

# Contract Ambiguities

| Ambiguity | Sprint 2H handling |
| --- | --- |
| `specs/refusal-engine.md` outputs runtime states, while Sprint 2H defines explanatory refusal categories. | Produce categories only; do not mutate runtime state. |
| Critical integrity failures map to `halted` in the specification, but `halted` is not a Sprint 2H category. | Gate decisions currently cover pre-execution authorization dependencies; invariant/integrity halt mapping remains deferred. |
| Recovery paths are required but no recovery contract maps individual categories. | Emit `retry_dependency` only for recoverable unavailable dependencies; otherwise emit `none`. |
| No generated refusal API, protobuf message, or database table exists. | Use typed in-memory artifacts and audit evidence; contract/persistence adapters remain deferred. |
| Authorization decisions are typed and hash-bound but not persisted or signed. | Verify all available IDs, outcomes, reasons, and evidence hashes; authenticity hardening remains deferred. |
| Human-readable explanation text is not specified. | Emit machine-readable structured `RefusalReason` only; do not invent prose. |

# Status

Sprint 2H Refusal Service foundation: complete with documented runtime-state
and persistence boundaries.
