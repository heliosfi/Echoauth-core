# XNOR → EchoAuth atomic authority/revocation snapshot contract v0.1

**REVIEW-ONLY / ARCHITECTURAL HOLD / NO RUNTIME CHANGE**

## Evidence checkpoint
- PR #61 commit `1e0874570b850e02710670d1457427e38172dd17`, workflow run `44147623749`: 19 tests PASS (10 existing + 9 synthetic), Authority Clarity Validator PASS.
- Current `src/echoauth/auth/authorization_gate.py` on main invokes `AuthorityResolutionService.resolve(AuthorityResolutionRequest(... authority_records=(), policy_version=...))` and does not supply `revocation_records`.
- Delegated requests select `grant.grantor_id` as the authority requester; afterward the gate compares resolved `authority_record_id` against `grant.source_authority_reference`.
- `AuthorizationGateService._complete` computes a decision hash from evidence/outcome/reason and caches by decision hash. Revocation snapshot identity, monotonic checkpoint, and coverage are not currently part of that evidence.
- PR #61's synthetic resolver runs separately from the actual gate; passing its fixture tests does **not** prove the gate selects the same authority or observes the same snapshot.

## Required atomicity invariant
For each request, the authority record actually selected by EchoAuth must be exactly the authority covered by the authenticated revocation snapshot evaluated for that request, under one stable checkpoint and time reference. No authorization may be returned if this binding cannot be established or maintained through final policy decision and audit commit.

## Candidate design for independent review
1. **Single trusted authority-resolution transaction:** the gate supplies the request identity, requester/grantor, subject, action, resource, context, policy version and a trusted checkpoint token to an authority-resolution service. The service resolves the actual authority and obtains its exact-target revocation coverage *within the same bounded evaluation*. Never take the covered authority record ID from caller-controlled parameters.
2. **Immutable decision snapshot:** return selected `authority_record_id`, authority source, subject, effective scope, request binding digest, authenticated mapping digest/version, revocation evidence digest, checkpoint digest/sequence, observed/effective/expires times, provider identity and explicit coverage state. All fields must be authenticated or independently derived; a test boolean is not authentication.
3. **Fail-closed outcomes:** unavailable, missing, ambiguous, stale, rollback, target mismatch, inconsistent checkpoint, unverifiable signature or changed selected authority must produce a non-authorizing outcome with stable reason codes. Effective revocation must produce REVOKED. No default empty revocation feed may mean clear.
4. **Delegation:** grantor authority and `grant.source_authority_reference` must bind to the same snapshot; delegation validation and policy evaluation must consume the same authority verdict. Any post-resolution substitution blocks.
5. **Temporal consistency:** define checkpoint pinning and an expiration/revocation recheck at final decision commit. If snapshot expires or source advances to an incompatible checkpoint before commit, retry with fresh authorization or HOLD. A prior authorized cached decision must not be replayed after a revocation event.
6. **Audit and cache:** include snapshot and mapping digests, selected authority ID, freshness, coverage verdict, and provider identity in canonical decision evidence; ensure audit append succeeds before decision return. Cache key must be revocation-aware or caching of positive decisions must be disabled until monotonic invalidation is proven.
7. **No authority transfer:** revocation evidence can constrain the gate but cannot grant authority, mutate the registry, deploy, execute, or authorize a next action.

## Mandatory negative tests before production wiring
- Provider covers A while actual resolver selects B → no authorization.
- Delegated grantor covered but source authority reference differs → no authorization.
- Authority resolution changes between preflight and commit → no authorization.
- Revocation arrives after positive preflight but before final decision → no authorization.
- Cached positive decision replayed after revocation/checkpoint advance → no authorization.
- Missing/stale/rollback/untrusted/mismatched source, checkpoint or mapping → no authorization.
- Valid coverage plus independent policy denial → DENIED, not authorized.
- Exact verified non-revoked authority plus independent valid identity, delegation and policy → only then may authorize.

## Explicit unresolved decisions
Trusted source and key custody; signature/canonicalization profile; authority mapping and source-of-truth; scope coverage policy; checkpoint sequencing and clock; atomic commit semantics; cache invalidation; approved audit schema; recovery during provider outages.

**Next safe step:** implement a test-only transactional resolver harness that injects checkpoint change between preflight and commit and asserts HOLD; do not modify the production gate until trust and transaction semantics receive independent review.
