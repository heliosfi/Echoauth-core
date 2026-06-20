# Sprint 2G Implementation Evidence

# Scope

Sprint 2G implements only the Runtime Authorization Gate foundation:

- typed `AuthorizationRequest` and `AuthorizationDecision` artifacts,
- deterministic input validation,
- fixed identity, authority, delegation, and policy processing order,
- direct and delegated request handling,
- fail-closed dependency and outcome mapping,
- immutable decision evidence packaging,
- deterministic decision identifiers and in-process idempotency,
- final Sprint 2A audit-chain integration.

The gate does not implement invariants, runtime-state transitions, envelopes,
tokens, execution, mutation authorization, override execution, or the broader
runtime orchestrator.

# Implementation Evidence

| Component | Runtime Evidence | Test Evidence |
| --- | --- | --- |
| Request and decision models | `AuthorizationRequest`; `AuthorizationDecision` in `src/echoauth/auth/authorization_gate.py` | All Sprint 2G full-stack fixtures |
| Fixed pipeline | `AuthorizationGateService.authorize` | Direct and delegated successful authorization tests assert all available result references |
| Identity dependency | `RegistryIdentityService.resolve` invocation | Identity-failure and successful tests |
| Authority dependency | `AuthorityResolutionService.resolve` invocation | Authority-failure, revoked, expired, direct, and delegated tests |
| Delegation dependency | Explicit `not_required` evidence for direct requests; `DelegationValidationService.validate` for delegated requests | Delegated success and failure tests |
| Policy dependency | `PolicyEvaluationService.evaluate` invocation | Authorization, denial, conflict, expiration, and deterministic tests |
| Evidence package | `_complete` canonical package and hash | Evaluation-order and stable-decision assertions |
| Audit integration | Final `authorization.decision` append | Repeated decision does not duplicate audit evidence |

# Deterministic Pipeline

1. Validate and canonically hash the request payload and context.
2. Verify requester identity.
3. For direct requests, resolve requester authority. For delegated requests,
   load the explicit grant to identify its grantor, resolve current grantor
   authority, and require the selected authority record to equal the grant
   source.
4. Record delegation as `not_required` for direct requests or validate the
   explicit grant for delegated requests.
5. Evaluate the pinned policy version using validated upstream results.
6. Map the terminal gate outcome, package component evidence, hash the package,
   and append the final audit record.

No later dependency runs after an earlier dependency fails. Dependency errors
map to their corresponding `invalid_*` outcome. Revocation, expiration, and
conflict propagate without being collapsed into generic denial.

# Test Evidence

Command:

```text
$env:PYTHONPATH='src'; python -B -m unittest discover -s tests
```

Result:

```text
Ran 95 tests in 0.145s

OK
```

The result includes every prior Sprint test and 10 Sprint 2G authorization gate
tests.

# Deferred Dependencies

- Invariant validation and runtime-state transition to `authorized`.
- Runtime envelopes, execution tokens, claims, and execution services.
- Broader runtime orchestration, refusal, halt, recovery, and escalation.
- Mutation authorization and institutional/emergency override execution.
- Persistent request, decision, and idempotency repositories.
- API/protobuf adapters and signed dependency-result verification.

# Contract Ambiguities

| Ambiguity | Sprint 2G handling |
| --- | --- |
| Runtime specifications say runtime state `authorized` requires invariants; Sprint 2G ends after policy. | Gate outcome `authorized` is explicitly not a runtime-state transition. Invariants remain mandatory before future execution paths. |
| `EchoAuthRequest` lacks requester actor type, credential set, assurance requirement, and pinned policy version needed by the four dependencies. | Define a gate-specific request model; API/protobuf adaptation remains deferred. |
| Direct requests have no delegation to validate, while the requested pipeline names delegation as mandatory. | Record immutable `delegation: not_required` evidence only when no delegation ID exists; delegated requests always call validation. |
| Delegation validation remains bound to its creation-time authority resolution ID, while the gate resolves fresh authority. | Verify fresh authority selects the grant source, then pass the stored authority resolution reference required by Sprint 2E. |
| A delegated request verifies the delegate identity, not the grantor identity during every gate call. | Grant creation and current explicit authority records establish the grantor source; no identity is inferred as authority. |
| Upstream results are typed and hash-bound but not persisted or signed. | Validate identifiers, outcomes, and cross-component references available in current models; authenticity hardening remains deferred. |
| Audit failure has no valid Sprint 2G outcome. | Raise `AuthorizationGateAuditError`; never return an unaudited authorization decision. |

# Status

Sprint 2G Runtime Authorization Gate foundation: complete with documented
runtime-state and contract adaptation boundaries.
