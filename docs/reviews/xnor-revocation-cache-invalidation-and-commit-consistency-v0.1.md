# XNOR / EchoAuth revocation-aware cache and commit consistency review v0.1

**REVIEW ONLY — NO PRODUCTION CHANGE — HOLD**

## Verified evidence
- PR #63 synthetic transactional snapshot harness: 14/14 PASS, run 44148501915, commit 647987ac06e32a35e05864a0c6b249a9df8b92d4.
- Main `src/echoauth/auth/authorization_gate.py`: `AuthorizationGateService._complete` builds `evidence_package`, derives `evidence_hash` and `decision_hash`, then looks up `self._cache[decision_hash]` under an RLock; a cache hit returns the prior decision. Cache identity does not currently contain a trusted revocation checkpoint or source freshness guarantee.
- `authorize` obtains `now` before identity, authority, delegation and policy checks; `_complete` appends an audit record for cache misses. No trusted external revocation snapshot is currently part of this transaction.

## Critical distinctions
- The current cache is keyed by a hash of decision evidence, outcome and reason, **not solely by request ID**. Do not claim it always replays a previous authorization after revocation: that depends on evidence and outcome staying identical.
- Nevertheless, if revocation changes outside the evidence considered by the gate, the cache cannot by itself detect that change. A repeated positive evaluation may return an old cached decision while the external revocation state differs.
- Even a cache miss cannot guarantee safety if revocation changes after the final snapshot check but before decision/audit commit.
- An RLock around `_complete` only serializes the local cache/audit section; it does not establish atomicity with an external revocation source.

## Proposed security invariant
No cached or newly computed AUTHORIZED decision may be returned unless the *actual selected authority*, exact subject/scope and trusted revocation coverage are bound to a valid monotonic checkpoint at a defined decision linearization point. If the system cannot establish that guarantee, it must return a non-authorizing outcome.

## Review options
A. Disable positive-decision caching for externally revocable authority until a trusted checkpoint invalidation protocol is verified. This is the safer interim default.
B. Later permit checkpoint-keyed positive caching only if source updates, monotonic sequencing, freshness, invalidation, and audit binding have independent tests and review. Checkpoint digest in a cache key alone is insufficient.
C. Revalidation at decision commit requires an authenticated source and a documented consistency/linearization contract; repeated reads alone cannot eliminate all races.

## Required negative tests
1. Positive decision at checkpoint 5; revocation at checkpoint 6; identical request must not return AUTHORIZED from cache.
2. Checkpoint advance without revocation must invalidate or require fresh evaluation, not reuse a stale positive decision.
3. Revocation after preflight but before audit append blocks authorization.
4. Provider outage during commit blocks authorization even if cache contains prior positive result.
5. A forged or rollback checkpoint cannot be used as cache key to reauthorize.
6. Different authority record, grantor, subject, action or resource cannot reuse coverage or positive decision.
7. Repeated HOLD/REVOKED decisions do not silently become AUTHORIZED through idempotency/retry.
8. Audit evidence binds actual authority, checkpoint, mapping and final non-authorizing reason; audit failure cannot return an authorization.

## Remaining independent review
Trusted source identity and key custody, canonical signed snapshot format, checkpoint consistency model, authority selection atomicity, delegation semantics, cache invalidation protocol, and linearization point. No real keys or runtime trust have been demonstrated.

## Next smallest reviewable implementation
A standalone **synthetic positive-cache replay harness** that demonstrates checkpoint-5 authorization candidate cannot be reused after checkpoint-6 revocation or provider outage. Keep it isolated from production gate and do not merge without review.
