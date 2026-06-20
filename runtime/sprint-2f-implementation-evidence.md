# Sprint 2F Implementation Evidence

# Scope

Sprint 2F implements only the canonical Policy Evaluation foundation:

- declarative `PolicyRule` artifacts,
- typed evaluation requests and results,
- deterministic policy hashing and validation,
- append-history in-memory policy persistence,
- policy lifecycle and effective-period handling,
- exact action and resource matching,
- provider-neutral canonical scope matching,
- deterministic descending numeric priority evaluation,
- highest-priority conflict detection,
- authority and optional delegation dependency gates,
- fail-closed outcomes,
- Sprint 2A audit-chain integration.

Execution authorization, tokens, envelopes, orchestration, mutation
authorization, and institutional or emergency overrides are not implemented.

# Implementation Evidence

| Component | Runtime Evidence | Test Evidence |
| --- | --- | --- |
| Policy models | `src/echoauth/policy/models.py` | All Sprint 2F typed rule/request/result fixtures |
| Validation and policy hashing | `src/echoauth/policy/validation.py` | Valid repository registration across all evaluation tests |
| Policy repository | `src/echoauth/policy/repository.py` | Revoked/expired lifecycle tests and audit registration evidence |
| Deterministic evaluator | `src/echoauth/policy/service.py` | Authorized, denied, conflict, invalid-policy, priority, and repeated-evaluation tests |
| Authority integration | `PolicyEvaluationService._validate_dependencies` | Direct authority-backed policy evaluation tests |
| Delegation integration | `PolicyEvaluationService._validate_dependencies` | Valid delegation upstream-evidence test |
| Audit integration | Policy repository and service | Audit append on registration/status/evaluation and cache-based idempotency |

# Deterministic Processing

- Policy evaluation cannot proceed unless the authority result identifier and
  request identifier match and the authority outcome is `authorized`.
- Direct requests require the requester to equal the authority source.
- Delegated requests require a matching `valid` delegation result.
- Revoked and expired upstream evidence propagates to policy outcomes.
- Action and resource strings match exactly; wildcard expansion is absent.
- Scope matching uses an injected deterministic matcher; ambiguity conflicts.
- Rules are stored in descending numeric priority order.
- Only the highest applicable priority group controls the decision.
- Opposing effects in that group return `conflict`.
- Missing versions and invalid requests return `invalid_policy`; missing active
  matches deny.
- Repeated evaluation of identical evidence returns an immutable cached result
  without duplicating audit evidence.

# Test Evidence

Command:

```text
$env:PYTHONPATH='src'; python -B -m unittest discover -s tests
```

Result:

```text
Ran 85 tests in 0.161s

OK
```

The result includes all prior Sprint tests and 9 Sprint 2F policy tests.

# Deferred Dependencies

- Execution authorization, tokens, envelopes, and runtime orchestration.
- Mutation authorization and signed policy distribution.
- Institutional and emergency override behavior.
- Production policy registry and decision persistence.
- API/protobuf adapters and generated rule schemas.
- Persisted or signed authority/delegation result verification.

# Contract Ambiguities

| Ambiguity | Sprint 2F handling |
| --- | --- |
| Generated contracts use `permit`, `refuse`, `hold`, and `escalate`; Sprint 2F requires `authorized`, `denied`, `conflict`, `expired`, `revoked`, and `invalid_policy`. | Runtime result uses Sprint 2F outcomes. Contract adaptation remains deferred. |
| Policy registry defines `rules` as an unstructured canonical object. | Runtime uses declarative rule fields required by Sprint 2F; arbitrary executable policy code is not supported. |
| Numeric priority direction is unspecified. | Runtime treats larger integers as higher priority and documents this choice. |
| First-refusal mode is described but no configuration contract exists. | Evaluate the highest-priority group; an unopposed deny denies, while opposing effects conflict. |
| `PolicyEvaluationRequest` has no policy type. | Evaluate all registered rules pinned to the requested version. |
| Authority results do not expose action/resource/subject fields and are not persisted or signed. | Validate result ID, request ID, source for direct requests, outcome, and evidence hash presence; deeper authenticity remains deferred. |
| Delegation requests reference a delegation ID but not a validation-result ID. | Require a typed result with the same delegation ID and `valid` outcome. |
| Database schema contains policy decisions but no policy artifact table. | Use in-memory policy persistence only. |

# Status

Sprint 2F Policy Evaluation foundation: complete with documented contract
adaptation dependencies.
