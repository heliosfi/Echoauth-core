# NODE XNOR → EchoAuth integration evidence reconciliation v0.1

**Disposition: REVIEW HOLD. Evidence inventory only; no merges, deployments, trust enrollment or production edits.**

## Verified CI evidence
| Candidate | What it actually demonstrates | Evidence |
| --- | --- | --- |
| PR #68 | Actual gate with synthetic external coverage injection; test-double behavior only | 27 PASS, run 44150133206 |
| PR #70 | Signed-envelope *structural negative* fixtures; no cryptographic verification | 19 PASS, run 44150542780 |
| PR #72 | Ed25519 verification using publicly embedded test-only seed; no trusted issuer | 20 PASS, run 44151391506 |
| PR #73 | Synthetic checkpoint lineage consistency; no authenticated source | 19 PASS, run 44151846250 |
| PR #74 | Test-only signature + synthetic lineage cross-binding | 12 PASS, run 44152346032 |
| PR #76 | Synthetic resolved-authority and commit-checkpoint binding; inputs not proven resolver-originated | 16 PASS, run 44153005267 |
| PR #78 | Actual gate's resolver selected authority despite caller hint; delegated grantor and missing revocation propagation characterized | 14 PASS (4 new + 10 imported), run 44154115722 |

These are independent CI outcomes, **not** an end-to-end integrated suite or evidence of production authorization safety. Other review candidates (#64–#67, #69, #71, #75, #77) supply relevant cache, trust, mapping and integration design evidence.

## Architectural blockers
1. **Trusted issuer and key registry:** no approved production trust anchors, key scope, lifecycle or authenticated source governance. Public test keys cannot satisfy this.
2. **Authenticated checkpoint lineage:** synthetic parent/sequence checks are not transparency consistency proofs, trusted publication, or cross-client equivocation detection.
3. **Exact authority mapping:** independent provenance mapping between XNOR target/issuer/scope and the *actual gate-selected* EchoAuth authority (including delegated grantor) is unimplemented.
4. **Atomic authorization:** no verified preflight/commit linearization or reliable revocation snapshot binding.
5. **Cache/audit:** current gate's positive decision cache does not bind trusted external checkpoint; audit/cached replay must be addressed before integration.
6. **Runtime provider:** the real gate's resolver request does not forward external revocation records. Synthetic injection is not an authenticated production provider.

## Dependency order — do not skip
A. Approve canonical signed-wire format, signature suite, key enrollment and trust governance.
B. Implement isolated verifier with **independent approved test trust roots** and adversarial vectors; never elevate test result to authority.
C. Prove source checkpoint consistency, freshness, equivocation response and authenticated mapping.
D. Prove exact gate-selected authority binding and delegation scope in isolated gate tests.
E. Specify and test transaction commit, cache invalidation, audit and outage semantics.
F. Seek independent security review and explicit human approval before any production integration or activation.

## Smallest next testable unit
**Test-only provenance capture and mismatch rejection at the real resolver boundary**, with a separate isolated observer that reads actual resolver outputs and compares them to untrusted claimed evidence, without changing the gate's production decision path. Test direct/delegated identity, substitution, missing evidence, and policy denial. This does not itself prove issuer trust.

## Authority boundary
CAPABILITY != AUTHORITY; MATCH != ACCEPTANCE; PASS != PERMISSION; RETURN != REAUTHORIZATION. A green CI run is evidence about its scoped tests only. All draft PRs remain review candidates unless separately approved for merge.
