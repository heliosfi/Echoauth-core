# NODE XNOR mandatory gate seam — implementation review v0.1

**Disposition: REVIEW HOLD.** This is a non-executable design candidate. No production gate edits, trusted-key enrollment, runtime integration, deployment, or activation.

## Verified current seam (main, after PR #85)

In `src/echoauth/auth/authorization_gate.py`, `AuthorizationGateService.authorize` runs identity, authority, delegation, policy and `_complete`. Authority selection uses `authority_requester = grant.grantor_id` for delegated requests and `AuthorityResolutionService.resolve(AuthorityResolutionRequest(... authority_records=(), policy_version=...))`. No authenticated external XNOR revocation evidence is supplied in that request. The delegated path compares `authority.authority_record_id` with `grant.source_authority_reference`. The existing decision evidence includes authority resolution ID, record ID and evidence hash, but not a trusted external revocation checkpoint. `_complete` uses an evidence-derived decision hash as cache key.

PR #84 demonstrates that direct `authorize` calls do not consult optional XNOR facades. PR #85's consolidated regression passes 294 XNOR review tests and 10 baseline authorization-gate tests. Neither fact establishes mandatory production enforcement.

## Proposed mandatory seam (not implemented)

1. Preserve existing identity resolution and independently selected authority resolution. Never select authority using caller `context` hints or XNOR-supplied claims.
2. After successful authority resolution and before any AUTHORIZED outcome, require a trusted revocation verifier bound to the **actual** `authority_record_id`, requester/grantor, subject, action, resource and delegation source reference.
3. The verifier must authenticate issuer/key from independently approved trust anchors; signed payload and source/checkpoint lineage; exact target/scope mapping; effective revocation time; freshness and monotonicity. Synthetic `MATCHED_FOR_REVIEW` is not authorization.
4. Missing/invalid/stale/forked/rolled-back/ambiguous/outage evidence yields HOLD/DENY, never an authorized return. CLEAR merely allows continuation to independent delegation and policy evaluation.
5. Capture one consistent trusted snapshot across authority selection, revocation, delegation/policy, final commit, audit and cache. If the snapshot changes before commit, retry from a new authenticated snapshot or deny. A cached positive decision cannot survive an effective revocation or checkpoint change.
6. Bind to audit evidence: issuer and key reference, checkpoint source/epoch/sequence/digest, authority mapping digest, selected authority ID, effective-time evaluation, delegation and policy outcomes. Audit append failure must not authorize.
7. Enforce inside `AuthorizationGateService.authorize` or prove that a single exclusive invocation boundary prevents all direct bypasses. Do not introduce a permissive optional fallback.

## Review-only negative test acceptance matrix

| Case | Required result |
| --- | --- |
| Direct gate call with authenticated effective revocation | Not AUTHORIZED |
| Caller supplies a different authority ID in context | Resolver-selected authority remains authoritative |
| Missing provider, unknown issuer/key, invalid signature | HOLD/DENY |
| Stale, rollback, fork, source mismatch, partial coverage | HOLD/DENY |
| Revocation between preflight and decision commit | No positive cache replay or authorization |
| Revocation checkpoint changes after prior positive decision | Cache invalidated or re-evaluated |
| XNOR CLEAR but policy or identity denies | Existing denial preserved |
| Delegated authority source mismatch | Existing denial preserved |
| Audit append fails | Not AUTHORIZED |
| Optional facade bypass via direct `authorize` | Mandatory gate still checks |
| Test-only keys/fixtures offered as production trust | Rejected |

## Independent prerequisites before any implementation merge

- Approved trusted issuer/key enrollment and rotation/revocation process
- Verified external checkpoint source, signed lineage and rollback defense
- Independently specified authority-target/scope mapping and provenance
- Atomic authorization/commit, cache invalidation and audit durability design
- Inventory of direct and indirect authorization entry points across services, APIs, jobs and agents
- Explicit human review of production fail-closed behavior, recovery and migration strategy

## Next reviewable step

Enumerate all callers of `AuthorizationGateService.authorize` and `AuthorizationGateService` construction across the repository and dependent services. Then build **test-only** negative fixtures for the proposed mandatory seam, without changing the real gate. Only after the trust and atomicity prerequisites are independently verified should a separately authorized implementation PR be considered.

**Governance:** CAPABILITY != AUTHORITY; MATCH != ACCEPTANCE; PASS != PERMISSION; EXECUTION != NEXT-ACTION AUTHORITY; RETURN != REAUTHORIZATION.
