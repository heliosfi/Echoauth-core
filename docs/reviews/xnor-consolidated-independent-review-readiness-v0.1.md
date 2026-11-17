# NODE XNOR × EchoAuth — consolidated independent-review readiness assessment v0.1

**REVIEW-ONLY / NO INDEPENDENT SECURITY SIGNOFF / PRODUCTION HOLD**

## Executive finding

The repository provides reproducible **synthetic negative-boundary evidence**, documentation of authority invariants and a navigable reviewer index. It does **not** yet demonstrate a trusted production checkpoint source, a complete exact gate-selected authority binding, non-bypassable enforcement, or independent security validation. Documentation readiness must not be conflated with runtime security readiness.

## Evidence a reviewer can inspect now

1. [Reviewer evidence index](xnor-independent-reviewer-evidence-index-v0.1.md), merged [PR #92](https://github.com/heliosfi/Echoauth-core/pull/92), commit `f9498ce68623e843cd4550ff92aa7f6bbefe738f`.
2. [T1/T2 decision matrix](xnor-t1-t2-trust-policy-decision-matrix-v0.1.md), merged [PR #93](https://github.com/heliosfi/Echoauth-core/pull/93), commit `78f5307636986da8da0c037f8ec89f786c119948`.
3. [T3 provenance/freshness assessment](xnor-t3-checkpoint-provenance-freshness-assessment-v0.1.md), merged [PR #94](https://github.com/heliosfi/Echoauth-core/pull/94), commit `77c7c1fee9342fb130187d1e344e8c9e4cd17be7`.
4. [PR #91](https://github.com/heliosfi/Echoauth-core/pull/91), merge `73cf93d393f2f7f4a99a76d8fb89d2759f7b3050`: public deterministic test-key and caller-supplied trust negative-boundary fixture; CI 321 XNOR tests and 10 authorization baseline tests PASS, Authority Clarity PASS. **Not** production issuer/key validation.
5. [PR #89](https://github.com/heliosfi/Echoauth-core/pull/89): 17 synthetic mandatory-seam negative tests, not runtime enforcement.
6. [Actual authorization gate](../../src/echoauth/auth/authorization_gate.py): identity → authority → delegation → policy; direct `authorize` method has no mandatory authenticated NODE XNOR revocation provider integration in the inspected main-branch code.
7. [Draft T1–T8 readiness register, PR #90](https://github.com/heliosfi/Echoauth-core/pull/90) and [draft entrypoint inventory, PR #87](https://github.com/heliosfi/Echoauth-core/pull/87), [draft Spine consumer review, PR #88](https://github.com/heliosfi/Echoauth-core/pull/88): scoped assessments, not independently validated deployment inventories.

## Gate-by-gate evidence and closure criteria

| Gate | Verifiable now | Unproven / required next evidence | Disposition |
| --- | --- | --- | --- |
| **T1 issuer/key trust** | Public test-key signatures and explicit non-trust boundary | Approved issuer identity, out-of-band fingerprints, custody, lifecycle, scope, trusted registry provenance; independent challenge of substitution/compromise | UNAPPROVED |
| **T2 crypto profile** | Proposed canonical verification pipeline and adversarial test plan | Human-approved canonical wire bytes, domain separation, signature/hash suites, parser limits, independent cryptographic vectors and review | UNAPPROVED |
| **T3 checkpoint provenance/freshness** | Synthetic sequence/parent-link evidence and documented requirements | Authenticated publisher, consistency/non-equivocation proof, trusted clock, high-water rollback state, freshness policy, coverage completeness | UNVERIFIED |
| **T4 authority mapping** | Synthetic exact-binding adapters and written contract | Independent source-of-truth mapping to actual gate-selected authority, delegated grantor, subject/action/resource/scope; live mismatch negatives | UNVERIFIED |
| **T5 atomicity/cache** | Snapshot contract and synthetic preflight/commit negatives | Demonstrated revocation linearization, commit-time recheck, concurrent revocation, positive-cache invalidation under actual gate | UNVERIFIED |
| **T6 audit durability** | Proposed audit evidence binding and fail-closed rules | Durable audit append/recovery tests with real checkpoint identity, crash/replay/failure handling and independent integrity review | UNVERIFIED |
| **T7 non-bypassable coverage** | EchoAuth-local gate entrypoint inventory and bounded Spine searches | Exhaustive runtime imports/call graph, external consumers, exclusive enforcement proof, migration and deployment inventory | INCOMPLETE |
| **T8 human authorization** | Explicit owner approval for merging review-only research/documentation | Separately scoped approvals for key enrollment, runtime changes, deployment and activation after required reviews | NOT GRANTED |

## Highest-priority reviewer questions

1. Can an attacker bypass the optional XNOR review facade and call `AuthorizationGateService.authorize` directly? Demonstrate from an actual reachable entrypoint, not just a theoretical import.
2. Can a caller supply an apparently trusted registry or a valid **test-key** signature and trick any path into granting trust? Verify all downstream consumers.
3. What independent authority proves the selected authority and delegated grantor correspond to the checkpoint's target and scope?
4. How are fork, rollback, stale checkpoint, revocation during decision, positive cache replay and audit failure blocked in the real authorization path?
5. Which controls remain fail-closed when issuer keys, registry, publisher or audit service are unavailable?

## Smallest evidence-producing next step

**One bounded, non-production, read-only cross-repository entrypoint trace**: identify actual call sites and service boundaries reaching `AuthorizationGateService.authorize` in EchoAuth and NI-AI Spine, capture file/commit references, and classify each path as *mandatory authenticated revocation enforcement demonstrated*, *bypass exposure*, or *unknown*. Do not claim completeness without deployment/runtime evidence. This directly addresses T7 and informs T4/T5 before further synthetic fixtures.

## Reviewer handoff / independence

A reviewer should receive the commit-pinned source index, CI run links, unresolved decisions, threat questions and explicit HOLD boundaries. A review performed by the author or an AI assistant is **not independent human security validation**. Academic paper submission, OpenReview availability and GitHub CI do not constitute production security approval. Repository visibility and access control may limit external reviewer access. Avoid disclosing identity links that could compromise an anonymized paper review.

**Disposition: DOCUMENTATION READY FOR EXTERNAL INSPECTION; SECURITY VALIDATION PENDING; T1–T8 OPEN; PRODUCTION HOLD.**

CAPABILITY != AUTHORITY; PLANNING != PERMISSION; PASS != EXECUTION; RETURN != REAUTHORIZATION.
