# NODE XNOR T3 — authenticated checkpoint provenance and freshness assessment v0.1

**DRAFT / REVIEW ONLY / T3 UNVERIFIED / INDEPENDENT VALIDATION PENDING / PRODUCTION HOLD**

This document identifies the evidence required to establish a trustworthy revocation checkpoint publisher, monotonic lineage and freshness. It does not select a publisher, approve a trust root, verify a live checkpoint, or implement a runtime verifier.

## Source evidence and limitations

- [Authenticated provider contract](xnor-authenticated-revocation-provider-contract-v0.1.md) specifies signed source/issuer, checkpoint sequence/digest/epoch, observed/not-before/expiry timestamps and consistency evidence; **no production trust anchor or provider is approved**.
- [Cryptographic verifier design](xnor-cryptographic-verifier-design-v0.1.md) proposes signature, policy, lineage and freshness validation, but remains design-only HOLD.
- [Signed lineage to authority binding](xnor-signed-lineage-actual-authority-binding-v0.1.md) records synthetic public-test-key signature and parent/sequence evidence (PR #74, 12 tests PASS), **not** authenticated publication, non-equivocation or actual gate-selected authority binding.
- [Atomic snapshot contract](xnor-atomic-authority-revocation-snapshot-contract-v0.1.md) specifies one stable authority/revocation decision snapshot and commit-time recheck; the existing gate does not implement this.
- [T1/T2 decision matrix](xnor-t1-t2-trust-policy-decision-matrix-v0.1.md) records the still-unapproved issuer/key and canonical cryptographic choices. [PR #90 T1–T8 register](https://github.com/heliosfi/Echoauth-core/pull/90) remains draft.

## T3 decision and evidence matrix

| ID | Unresolved question | Evidence threshold | Disposition |
| --- | --- | --- | --- |
| T3.1 | Which accountable checkpoint publisher and source identity are authoritative for each namespace/scope? | Independently verified source identity, source-to-scope governance approval, publication endpoint provenance | OPEN |
| T3.2 | How is publication authenticated to the separately approved T1/T2 issuer/key policy? | Signed canonical bytes, approved key provenance, verifier policy binding, no caller-declared trust | OPEN |
| T3.3 | What constitutes a checkpoint identity and unique monotonic order (epoch, sequence, digest, parent)? | Versioned schema, source epoch semantics, signed parent links and durable high-water state | OPEN |
| T3.4 | What proves consistency, detects equivocation/forks and handles gaps, reorgs or rollback? | Independently checkable consistency or transparency evidence, conflicting-witness tests, rollback rejection | OPEN |
| T3.5 | Which trusted clock and time-policy determine freshness, skew, not-before, expiry and maximum age? | Clock provenance, bounded skew/age policy, tests at exact boundaries and after clock jumps | OPEN |
| T3.6 | How is coverage completeness and effective revocation time proven for an exact authority/target/scope? | Authenticated inclusion/non-inclusion or coverage proof, revocation effective-time semantics, partial coverage rejection | OPEN |
| T3.7 | What is the outage, delayed publication, restart, failover and source-key rotation recovery rule? | Recovery runbook, pinned checkpoint continuity, quarantine/hold behavior, anti-rollback persistence tests | OPEN |
| T3.8 | How is one verified checkpoint pinned to the **actual gate-selected** authority through final decision and audit? | T4 independently sourced mapping, T5 atomic recheck/linearization, T6 durable audit, T7 entrypoint coverage | OPEN |

## Threat / negative-test register (not a claim of completed testing)

1. Unauthenticated publisher, valid test-key signature or self-declared trusted registry → HOLD.
2. Valid signature for the wrong source, namespace, authority, scope, epoch or mapping → HOLD.
3. Replayed older sequence, changed parent digest, forked same-sequence checkpoint, missing sequence gap or source epoch rollback → HOLD.
4. Future-dated, not-yet-valid, expired, stale, clock-skew-exceeding or clock-rollback checkpoint → HOLD.
5. Missing/partial non-revocation coverage, revoked at effective boundary, inconsistent inclusion proof → HOLD or verified REVOKED as appropriate; never CLEAR by default.
6. Publisher outage, unverifiable key rotation, cache-only stale positive, lost high-water mark or untrusted failover → HOLD.
7. Valid coverage for a synthetic authority while actual EchoAuth resolver selects another → HOLD.
8. Checkpoint advances incompatibly between preflight and decision commit, or audit append fails → no authorization.

## Proposed independent review procedure

1. Obtain the approved T1 issuer/key custody and T2 cryptographic policy first; **do not treat deterministic test keys as production trust**.
2. Request an attributable, versioned source publication and proof specification with independent publisher provenance. Keep endpoints and identities unspecified until authorized.
3. Independently reproduce canonical signature and lineage verification, including fork/rollback/expiry and scope-substitution negatives, against isolated **test** fixtures.
4. Document a trusted clock, maximum-age and skew policy with reproducible boundary tests.
5. Reconcile T4 mapping to the gate-selected authority and T5/T6 atomicity/audit before proposing production enforcement.
6. Require a separate explicit T8 owner decision for any key enrollment, registry mutation, runtime wiring, deployment or activation.

## Reviewer finding template

- Finding ID / reviewer identity / date:
- Artifact path, version, commit SHA and digest:
- Source publisher provenance and approved scope: **NOT ESTABLISHED**
- Approved T1/T2 trust policy: **NOT ESTABLISHED**
- Lineage and consistency proof: **NOT VERIFIED**
- Trusted clock and freshness evidence: **NOT VERIFIED**
- Actual gate-selected authority binding: **NOT VERIFIED**
- Reproducible tests / negative vectors / limitations:
- Disposition: **T3 UNVERIFIED — HOLD**

**Conclusion:** Synthetic lineage tests and a signed-looking checkpoint do not establish an authenticated, fresh, non-equivocating production revocation source. No code or operational change is authorized.

CAPABILITY != AUTHORITY; CORRESPONDENCE != AUTHORIZATION; PASS != EXECUTION; RETURN != REAUTHORIZATION.
