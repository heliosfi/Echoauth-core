# NODE XNOR trusted checkpoint and authority mapping readiness register v0.1

**REVIEW HOLD.** This is an evidence reconciliation and decision register, not approval of any issuer, key, provider, mapping, runtime integration or deployment.

## Verified available evidence
- `docs/reviews/xnor-authenticated-revocation-provider-contract-v0.1.md` specifies canonical gate-originated request and signed response, exact selected authority binding, freshness, checkpoint lineage, effective revocation, audit and cache constraints. Its own status explicitly says **no trust anchor, runtime wiring or activation**.
- `docs/reviews/xnor-cryptographic-verifier-design-v0.1.md` specifies cryptographic validation and negative cases, but says **design candidate / HOLD** pending human-approved trust governance.
- `docs/reviews/xnor-signed-lineage-actual-authority-binding-v0.1.md` reports public **test-key** synthetic signature and lineage evidence, not production issuer enrollment, source publication or atomic gate binding.
- Merged PR #89 adds a review-only synthetic mandatory seam classifier with 17 tests. The consolidated workflow passed 311 XNOR tests plus 10 baseline gate tests. Its `CONTINUE_REVIEW` result does not grant permission.
- Draft PRs #86–#88 document the mandatory gate seam, entrypoint exposure and Spine consumer boundary. Their draft status does not constitute approval.

## Decision register — independent owner decisions required

| ID | Decision needed | Evidence presently available | Disposition |
| --- | --- | --- | --- |
| T1 | Which issuer(s) and key fingerprints are approved for which scope, including custody, rotation, compromise and revocation | Verifier design and public test-key fixtures only | UNAPPROVED |
| T2 | Which canonical wire format, domain separation, signature/hash algorithms and parser limits are authoritative | Proposed verifier contract | UNAPPROVED |
| T3 | Which authenticated checkpoint publisher, epoch/sequence/consistency proof, anti-rollback state, freshness window and clock are authoritative | Synthetic lineage tests | UNVERIFIED |
| T4 | Which versioned mapping source binds XNOR target/scope to actual gate-selected EchoAuth authority and delegated grantor | Mapping contract and synthetic binding adapters | UNVERIFIED |
| T5 | What is the revocation-vs-authorization linearization point, including concurrent change and cache invalidation | Atomicity/cache design and isolated characterization | UNVERIFIED |
| T6 | Which audit durability, failure and recovery rules govern commit and replay | Gate audit and proposed revocation evidence contracts | UNVERIFIED |
| T7 | Which deployment entrypoints, external consumers, and migration paths are subject to mandatory checks | EchoAuth-local inventory #87, bounded Spine review #88 | INCOMPLETE |
| T8 | Which human authority approves production integration, key enrollment and rollout per repository | Repository authority boundaries documented | NOT GRANTED |

## Minimum evidence to close each decision
- T1/T2: signed-off trust-policy artifact; independent key fingerprint verification, custody and lifecycle test; negative vectors for substitution, unknown key, rotation and downgrade.
- T3: authenticated source publication and consistency/rollback proofs with verified clock/freshness policy; tests for fork, rollback, stale, gap and outage.
- T4: independent source-of-truth mapping, immutable version/digest, real resolver-selected authority and delegated grantor; mismatch tests.
- T5/T6: transactional revocation snapshot specification, linearization and cache strategy, audit durability, concurrent revocation and audit-failure tests.
- T7: complete import/call graph, runtime deployment and external service inventory, exclusive enforcement boundary and migration plan.
- T8: explicit bounded owner approvals for each repository and operational change; CI green is not authority.

## Recommended next review checkpoint
Obtain **T1–T4 decision evidence** and independently validate it before proposing any production verifier. In parallel, a test-only fixture can demonstrate that public test keys, caller-supplied trust flags and a correct-looking signed envelope are insufficient without a trusted issuer registry. Do not edit `src/echoauth/auth/authorization_gate.py`, enroll keys, mutate trust registries, or activate production.

CAPABILITY != AUTHORITY; MATCH != ACCEPTANCE; PASS != PERMISSION; RETURN != REAUTHORIZATION.
