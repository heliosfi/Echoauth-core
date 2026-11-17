# EchoAuth actual decision cache versus XNOR synthetic replay — characterization v0.1

**REVIEW ONLY / NO PRODUCTION CODE MODIFICATION / PRODUCTION HOLD**

## Verified evidence
- PR #65 commit `69ca6d232fd95756a7de9b4d0256ebe81f2bf1b1`: XNOR Synthetic Cache Replay Review run `44149369910` PASS, 15 tests; Authority Clarity Validator PASS.
- Inspected `src/echoauth/auth/authorization_gate.py` on `main`. `_complete` computes `evidence_package` from accumulated identity/authority/delegation/policy evidence plus correlation, idempotency and request IDs. `evidence_hash=canonical_sha256(evidence_package)`; `decision_hash=canonical_sha256({evidence_hash,outcome,reason})`.
- Under `self._lock`, `_cache.get(decision_hash)` returns an existing decision **without another audit append**. Otherwise the gate appends an audit event, creates an `AuthorizationDecision`, and caches it under `decision_hash`.
- Current gate's `AuthorityResolutionRequest` omits `revocation_records`, so external XNOR revocation coverage is not part of the authority evidence. The lock does not cover an external trusted revocation checkpoint.

## Precise interpretation
- This is a **decision-hash cache**, not a general request-ID cache. Reusing a decision requires the same canonical evidence, outcome and reason.
- PR #65's isolated cache simulator is intentionally stricter: it never returns a cached positive authorization, but it does **not** execute the real gate's cache path.
- Neither PR #65's PASS nor a stable `decision_hash` establishes revocation-aware invalidation, freshness, or external source consistency.
- A future XNOR integration must avoid stale positive decisions after revocation even when the existing identity, authority and policy evidence remain unchanged.

## Next bounded verification candidate
Add a **test-only characterization of the actual `AuthorizationGateService._complete` cache path**, using existing gate fixtures and synthetic evidence. Test whether identical evidence returns a cached decision, whether a changed synthetic revocation checkpoint in evidence changes the decision hash, and whether an unchanged evidence package can still return the same cached positive decision. Tests must distinguish observed current behavior from desired security behavior; never mark an existing vulnerability as an authorization success criterion.

## Required controls before production
1. Authenticated exact-authority revocation snapshot in the actual gate decision evidence.
2. Monotonic checkpoint and source freshness verified at a documented linearization point.
3. Positive-cache disablement or independently verified invalidation on revocation, rollback, expiry and provider failure.
4. No reuse of a prior positive decision without new authorization and audit semantics.
5. Independent review of delegation, audit, idempotency, time and source trust.

## Disposition
Documented implementation gap. No production code edits, real keys, registry changes, merge, or activation. Independent security review pending.
