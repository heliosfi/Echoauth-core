# Sprint 2I Implementation Evidence

# Scope

Sprint 2I implements only the canonical Escalation Service foundation:

- typed `EscalationRequest`, `EscalationReason`, and `EscalationDecision` artifacts,
- mandatory authorization-decision and refusal-decision evidence linkage,
- versioned deterministic escalation classification,
- seven canonical escalation categories,
- immutable escalation evidence packaging,
- in-process idempotency,
- Sprint 2A audit-chain integration.

The service consumes existing decisions only. It does not invoke authorization
or refusal services, change a denial, assign reviewers, send notifications,
resolve reviews, approve overrides, or permit execution.

# Implementation Evidence

| Component | Runtime Evidence | Test Evidence |
| --- | --- | --- |
| Escalation models | `src/echoauth/governance/escalation_models.py` | All Sprint 2I fixtures and category assertions |
| Authorization and refusal linkage | `EscalationService._validate_dependencies` | Authorized decisions and mismatched refusal evidence are rejected |
| Versioned classification | `ESCALATION_MAPPING_VERSION`; `_classify` | Refusal, conflict, revoked, expired, unavailable-dependency, explicit-route, and no-route tests |
| Structured evidence | `EscalationService.escalate` | Audit evidence test verifies both upstream decision IDs, hashes, and audit references |
| Audit integration | `EscalationService.escalate`; `InMemoryAuditLogRepository` | Repeated escalation is identical and does not duplicate audit evidence |

# Deterministic Processing

- An escalation requires matching immutable authorization and refusal decisions.
- Authorized decisions are rejected and cannot enter escalation.
- Refusal evidence must bind the same authorization decision ID and evidence hash.
- Recoverable or unavailable dependencies produce `system_hold`.
- Malformed refusals, expired deadlines, and explicit absence of a review route
  produce `no_escalation_available`.
- Human, guardian, parent, admin, and clinical review types map through a fixed
  versioned table.
- Every decision has resolution `none`; escalation never authorizes.
- Repeated processing of identical evidence returns the same immutable decision
  without a duplicate audit append.

# Test Evidence

Command:

```text
$env:PYTHONPATH='src'; python -B -m unittest discover -s tests -v
```

Result:

```text
Ran 115 tests in 0.117s

OK
```

The result includes all prior Sprint tests and 11 Sprint 2I escalation tests.

# Deferred Dependencies

- Reviewer registry, reviewer availability, deterministic reviewer selection,
  and authority verification for reviewers.
- Notification delivery and `notified` transition.
- Human review, guardian review, parent review, admin review, and clinical review
  workflows.
- Review resolution, override approval, and return-to-governance validation.
- Runtime authorization changes, execution blocking, tokens, envelopes,
  orchestration, mutation authorization, and override execution.
- Persistent escalation queue and decision repository.
- API, protobuf, database, event-catalog, and integration adapters.

# Contract Ambiguities

| Ambiguity | Sprint 2I handling |
| --- | --- |
| `required_authority_type` is not enumerated by `specs/escalation-engine.md`. | Use only the five review types named by Sprint 2I plus explicit `none`; do not infer review authority from identity, authority registry, or affiliation. |
| The specification requires deterministic reviewer selection but defines no reviewer registry or availability contract. | Classify the required review route only; do not assign `reviewer_id`. |
| The specification state machine includes `notified`, `resolved`, and `cancelled`. | Emit only `opened`, or `expired` for an elapsed deadline; all active workflow transitions remain deferred. |
| No generated escalation schema, protobuf message, API operation, event type, or database table exists. | Use typed in-memory artifacts and append audit evidence; adapters and persistence remain deferred. |
| No contract maps authority-registry categories to guardian, admin, or clinical reviewers. | Require an explicit review type and never derive it from an `AuthorityRecord`. |

# Status

Sprint 2I Escalation Service foundation: complete with documented reviewer,
workflow, persistence, and contract-adapter boundaries.
