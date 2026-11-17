# EchoAuth actual-resolver provenance integration checkpoint v0.1

**Disposition: REVIEW HOLD. This is a design and source inspection record, not a production modification.**

## Verified review evidence
- PR #76, commit `2ad19df4287abea887168042b41bc62f9ee2741b`: 16/16 isolated synthetic adapter tests PASS, run `44153005267`, job `134286111978`; Authority Clarity Validator PASS.
- Source inspected: `src/echoauth/auth/authorization_gate.py` on `main` at review time.

## Actual gate provenance and risk
The gate calls `self._authority_service.resolve(AuthorityResolutionRequest(...))` after identity validation, with `requester_id=grant.grantor_id` for delegation, otherwise the request requester. The resolver's response includes `authority_record_id`, `authority_resolution_id`, `outcome`, and `evidence_hash`. The gate independently compares delegated `grant.source_authority_reference` to `authority.authority_record_id`.

The gate's current resolver request passes `authority_records=()` but **does not pass `revocation_records`**. This is a concrete revocation-propagation gap for externally supplied revocation evidence, not proof that the resolver cannot handle revocation.

The gate's `_complete` computes `evidence_hash` and `decision_hash` and returns an existing cached decision for identical hashes before appending a new audit event. The current evidence contains authority outcome/hash/ID, but no authenticated XNOR checkpoint or mapping digest. Therefore an external revocation source cannot be assumed to invalidate cached positive decisions.

## Recommended single authority path
1. Keep existing identity and authority resolution as the sole source of the **actual selected authority**; no caller-supplied authority selection.
2. After successful authority resolution and the existing delegated source-authority equality check, construct an immutable internal `ResolvedAuthorityEvidence` from the actual resolver output and request/delegation context. Include authority record ID, resolution ID, resolver evidence hash, subject/requester/grantor, action, resource, scope, target/mapping digest and provenance.
3. Supply this internal object to a separate revocation-coverage verifier. The verifier must authenticate issuer/key, exact signed payload and source, mapping to the actual authority, checkpoint freshness/consistency, and revocation effective time. Missing data or outage must fail closed. **Never let the caller construct or overwrite internal authority provenance.**
4. Treat `CLEAR_COVERAGE` as a prerequisite to proceeding with the existing delegation and policy checks, not as authorization.
5. Revalidate coverage at the authorization commit linearization point; reject any checkpoint or mapping change between preflight and commit.
6. Incorporate verified checkpoint/mapping/issuer/key evidence into decision and audit hashes. Disable positive cache reuse until cache invalidation against trusted checkpoint state is proven; audit failures must block.
7. Keep independent identity, delegation and policy denial paths intact; coverage verification cannot upgrade their verdicts.

## Evidence needed before code integration
- Trust-anchor enrollment policy and approved key lifecycle (not test keys).
- Exact resolver-selected authority to XNOR target mapping with independent provenance.
- Verified signed checkpoint consistency and anti-rollback semantics.
- Transactional commit/recheck contract, provider outage behavior and audit persistence.
- A full test matrix: caller A vs resolved B, delegated grantor mismatch, signed source mismatch, revoked/stale/partial coverage, checkpoint TOCTOU, cached-positive replay, policy DENY despite CLEAR, and audit failure.
- Independent security review of canonicalization and signature implementation.

## Boundaries
Do not modify `src/echoauth/auth/authorization_gate.py`, enroll keys, mutate real registry, merge draft PRs, deploy or activate on this evidence. Synthetic tests are useful but do not prove authentic source provenance or production readiness.

**Next smallest reviewable step:** a test-only instrumented gate test that captures the actual resolver's `authority_record_id` and demonstrates a caller-provided alternative cannot replace it, without altering production gate logic.
