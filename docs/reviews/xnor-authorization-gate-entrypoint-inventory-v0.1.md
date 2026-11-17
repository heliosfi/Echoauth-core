# EchoAuth authorization-gate entrypoint inventory — NODE XNOR v0.1

**Disposition: REVIEW HOLD.** Static GitHub default-branch search and selected file inspection only; no production changes. Search coverage is not a complete whole-organization runtime call graph.

## Verified source and exports
- `src/echoauth/auth/authorization_gate.py`: public `AuthorizationGateService.authorize(request)` performs identity → authority → delegation → policy → `_complete`. Its authority-resolution request currently omits authenticated external XNOR revocation records. No mandatory XNOR check is called.
- `src/echoauth/auth/state.py`: re-exports `AuthorizationGateService` and `AuthorizationRequest`.
- `src/echoauth/auth/__init__.py`: re-exports the gate again through the public `echoauth.auth` interface. **Export visibility is not proof of runtime invocation.**
- `tests/test_authorization_gate.py`: constructs the gate fixture and calls `self.gate.authorize` directly, including positive authorization tests.

## Observed call sites and their significance
| Surface | Observed role | Review implication |
| --- | --- | --- |
| `tests/test_authorization_gate.py` | Direct gate construction and invocation | Demonstrates direct callable API; tests do not establish production entrypoint |
| `tests/test_xnor_direct_gate_bypass_characterization.py` | Direct call without mandatory XNOR; untrusted context hint ignored | Verified review characterization of optional-facade bypass |
| `tests/test_xnor_external_coverage_gate_review.py` | Calls real gate with synthetic resolver test double | Test-only injection; not authenticated provider |
| `tests/test_xnor_synthetic_gate_demonstration.py` | Injects synthetic revocation forwarder and calls gate | Demonstration only |
| `tests/test_xnor_real_gate_cache_characterization.py` | Direct gate calls around revocation/cache conditions | Characterizes existing cache gap |
| `tests/test_xnor_real_resolver_provenance.py` | Spies on real authority resolver during gate call | Resolver evidence observation, not mandatory enforcement |
| `tests/test_xnor_revocation_propagation_review.py` | Direct call with recording authority resolver | Characterizes missing external propagation |
| `tests/test_xnor_resolver_evidence_observer.py` | Direct gate call with observer | Observer cannot deny |
| `review_candidates/xnor_fail_closed_facade.py` | `evaluate_facade` optionally calls `gate.authorize(request)` | Optional facade can be bypassed by a direct gate caller |
| `docs/control-gates/echoauth-sai-binding-responsibility-and-evidence.md` | Explicitly says SAI record former/intake validator do not call gate | Documentation claim; not runtime call-graph proof |

GitHub code search for `AuthorizationGateService(`, `AuthorizationGateService`, `.authorize(`, and `authorization_gate` found these surfaces. Other `.authorize(` occurrences belong to distinct `EventSubscriberAuthorization` and must not be conflated with `AuthorizationGateService`.

## What remains unverified
1. Exhaustive repository-wide static analysis of aliases, dynamic imports, dependency injection, reflection, wrappers and alternative authorization outcomes.
2. External consumer repositories: NI-AI Spine, agent runtimes, API services, jobs, queue consumers, and deployed applications. No claim of complete cross-repo inventory.
3. Production deployment topology and whether a gateway or exclusive service boundary exists.
4. Runtime configuration, secrets, trusted issuer enrollment, and actual provider provenance.
5. All possible bypasses through other authorization implementations or cached decision consumers.

## Decision and next checkpoint
**Confirmed risk:** `AuthorizationGateService.authorize` is a public, directly callable method and lacks a mandatory authenticated external XNOR revocation check. A review-only facade is not an exclusive enforcement boundary.

**Do not** equate code-search absence with proof that no callers exist. Next: perform a cross-repository consumer inventory and build a test-only mandatory-seam negative harness. Before any production gate edit, require trusted issuer/source and authority mapping approval, atomic commit/cache/audit semantics, and explicit authorization.

CAPABILITY != AUTHORITY; MATCH != ACCEPTANCE; PASS != PERMISSION; RETURN != REAUTHORIZATION.
