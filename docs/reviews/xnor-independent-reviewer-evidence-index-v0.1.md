# NODE XNOR — independent reviewer evidence index v0.1

**Status: REVIEW-ONLY INDEX / INDEPENDENT VALIDATION PENDING / PRODUCTION HOLD.**

This is a navigational record for human, academic and AI-assisted reviewers. It does **not** certify the security of the implementation, enroll a key, grant authority, or approve production activation. Links to draft PRs are not files on `main`.

## Suggested reviewer reading order

1. **Authority and governance boundary.** [EchoAuth authorization gate](../../src/echoauth/auth/authorization_gate.py) and [NODE XNOR direct-gate bypass characterization](../../tests/test_xnor_direct_gate_bypass_characterization.py). The direct gate remains callable without mandatory authenticated external NODE XNOR revocation checks; this is a documented gap, not a verified production exploit.
2. **Verified consolidated regression.** [Merged PR #85](https://github.com/heliosfi/Echoauth-core/pull/85), merge `74558d733fb778b313dd590b1e72b731fb7a0eaa`: 294 XNOR review tests and 10 baseline authorization tests passed at that checkpoint.
3. **Mandatory seam negative harness.** [Merged PR #89](https://github.com/heliosfi/Echoauth-core/pull/89), merge `a07821e31c216ad563851d768c8a9c3dafa9cf10`: [synthetic classifier](../../review_candidates/xnor_mandatory_seam_negative_harness.py) and [17 tests](../../tests/test_xnor_mandatory_seam_negative_harness.py). Synthetic `CONTINUE_REVIEW` never means permission.
4. **Public test-key trust boundary.** [Merged PR #91](https://github.com/heliosfi/Echoauth-core/pull/91), merge `73cf93d393f2f7f4a99a76d8fb89d2759f7b3050`: [review classifier](../../review_candidates/xnor_test_key_trust_boundary.py) and [10 tests](../../tests/test_xnor_test_key_trust_boundary.py). Workflow [44179283777](https://github.com/heliosfi/Echoauth-core/actions/runs/44179283777) passed 321 XNOR tests and 10 gate baseline tests; [Authority Clarity Validator 44179285072](https://github.com/heliosfi/Echoauth-core/actions/runs/44179285072) passed. PR discussion records owner-approved **research-evidence preservation**, not independent security validation.
5. **Existing trust specifications on main.** [Authenticated revocation provider contract](xnor-authenticated-revocation-provider-contract-v0.1.md), [cryptographic verifier design](xnor-cryptographic-verifier-design-v0.1.md), [signed lineage to actual authority binding](xnor-signed-lineage-actual-authority-binding-v0.1.md), and [atomic authority-revocation snapshot contract](xnor-atomic-authority-revocation-snapshot-contract-v0.1.md).
6. **Open draft assessments, not on main.** [PR #86 mandatory enforcement seam](https://github.com/heliosfi/Echoauth-core/pull/86), [PR #87 gate entrypoint inventory](https://github.com/heliosfi/Echoauth-core/pull/87), [PR #88 Spine consumer boundary](https://github.com/heliosfi/Echoauth-core/pull/88), and [PR #90 trust readiness register](https://github.com/heliosfi/Echoauth-core/pull/90). These are proposed review artifacts, not merged implementation or approval.

## Explicit boundary ledger

| Evidence question | What is established | What is not established |
| --- | --- | --- |
| Negative contract behavior | Synthetic tests and regression CI pass | Real production revocation enforcement |
| Signature test vector | Deterministic public test-key cryptographic checks | Approved production issuer/key custody, enrollment or authenticated publication |
| Authority binding | Proposed exact gate-selected authority and mapping contracts; synthetic fixtures | End-to-end trusted binding of live resolver, delegated grantor, target and checkpoint |
| Revocation freshness | Synthetic stale/rollback/outage/changed-snapshot rejection | Authenticated monotonic publisher, anti-equivocation, transactional consistency and positive-cache invalidation |
| Entry-point coverage | EchoAuth-local inventory and bounded default-branch cross-repo searches | Exhaustive deployed call graph or exclusive non-bypassable enforcement |
| Academic review | Research may be submitted separately by the owner | IEEE acceptance, external peer review of this implementation or OpenReview validation |
| Governance | Owner-approved merge of test-only research evidence | Independent security signoff, production deployment or execution permission |

## Reviewer verification tasks

- Reproduce CI at the linked merge SHAs and verify that tests are isolated from production gate wiring.
- Inspect trust-root policy, issuer/key custody and approved cryptographic profile; no public fixture key may count as production enrollment.
- Verify checkpoint source authentication, sequence/epoch lineage, fork/rollback handling, freshness and recovery.
- Demonstrate exact gate-selected authority and delegated-grantor mapping with independently sourced provenance.
- Probe direct gate bypass, concurrent revocation, stale positive-cache replay, audit failure and alternate consumer paths.
- Record evidence-backed findings, severity, reviewer identity, commit references and unresolved questions; do not silently convert test PASS to security acceptance.

## Source and access note

This index is in the **EchoAuth repository**. Repository access controls still apply; merging into main does not automatically make private content publicly accessible. Reviewers may need explicit access. This index does not publish or disclose an anonymized IEEE submission or link an anonymous submission to an author identity.

**Current disposition: RESEARCH EVIDENCE PRESERVED — INDEPENDENT VALIDATION PENDING — PRODUCTION HOLD.**

CAPABILITY != AUTHORITY; MATCH != ACCEPTANCE; PASS != PERMISSION; EXECUTION != NEXT-ACTION AUTHORITY; RETURN != REAUTHORIZATION.
