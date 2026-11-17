# NODE XNOR → EchoAuth authenticated revocation provider contract v0.1

**REVIEW-ONLY PROPOSAL — NO TRUST ANCHOR, NO RUNTIME WIRING, NO ACTIVATION**

## Evidence
PR #68 at `67fa049b940b402324c14c0012e30699ae736962`: 27 tests PASS in workflow `44150133206`, Authority Clarity Validator PASS. Synthetic external coverage injection blocks positive cache reuse on HOLD, revocation and outage, but the test double raises exceptions (mapped by the actual gate to INVALID_AUTHORITY) and does not authenticate evidence or bind to the gate-selected authority.

## Provider request (trusted gate-originated)
- Canonical request digest, correlation ID, requester/grantor ID, subject ID, action, resource, policy version.
- Exact **gate-resolved** authority record ID and authority source ID, not a caller-supplied claimed authority.
- Versioned mapping digest and mapping provenance linking XNOR namespace, target fingerprint digest, role/tier/scope/source identity to EchoAuth authority.
- Minimum acceptable monotonic checkpoint sequence and trusted time reference.

## Provider response (canonical, signed, immutable)
- Schema ID/version, issuer/source identity, key identifier and signature algorithm.
- Canonical signed payload bytes (including domain separation), signature and verifier policy version.
- Exact selected authority ID, subject, action/resource scope, source ID, XNOR target fingerprint digest, mapping digest/version.
- Revocation verdict: REVOKED / CLEAR_COVERAGE / HOLD; reason codes, evidence digest and effective time.
- Checkpoint sequence/digest, source epoch, observed-at, not-before, expires-at, consistency proof or authenticated checkpoint lineage.
- Verification status must be derived by a trusted verifier, **never from a boolean supplied by the caller or payload**.

## Validation sequence
1. Establish trusted source/key registry via separate human-governed approval; pin allowed schema, algorithms and issuer scope.
2. Verify canonical encoding, domain separation, signature and key validity/revocation, without accepting an unsigned fallback.
3. Resolve authority independently inside the gate's trusted flow; bind provider response to the *actual* selected authority and delegated grantor.
4. Verify exact target, scope, mapping provenance, checkpoint monotonicity and freshness, with clock-skew rules.
5. Return REVOKED only for verified effective revocation; HOLD for missing, stale, unavailable, ambiguous, untrusted or inconsistent coverage. CLEAR_COVERAGE is **not authorization**.
6. Bind final verified snapshot to authorization evidence and audit; enforce revalidation/linearization and revocation-aware cache policy. Audit failure blocks authorization.

## Negative tests required
- Forged signature, unknown key, wrong issuer, wrong schema/domain, noncanonical bytes.
- Expired key, revoked key, key rollover ambiguity, duplicate source IDs.
- Mismatched authority record, delegated grantor, subject, action, resource, mapping digest, target digest.
- Checkpoint rollback, equivocation, stale timestamp, gap or invalid lineage.
- Provider outage/timeout, absent record, partial coverage, empty default.
- Revocation after preflight, stale positive cache, concurrent snapshot change, audit append failure.
- Verified clear coverage plus independent policy denial must remain DENIED.

## Open security decisions (HOLD)
Trusted issuer and key custody, approved signature/canonicalization profile, checkpoint consistency and transparency mechanism, source-of-truth mapping, delegation semantics, time source, cache invalidation and decision linearization point. No actual keys, signed payloads or provider implementation are authorized by this document.

## Next smallest safe step
Create an isolated **negative-test fixture schema** for signed-envelope validation and exact authority binding; do not wire production gate or assert real signature verification until trusted key governance is approved.
