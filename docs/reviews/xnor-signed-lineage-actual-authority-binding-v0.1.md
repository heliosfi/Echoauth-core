# NODE XNOR signed lineage → EchoAuth authority binding — review checkpoint v0.1

**REVIEW ONLY — NO PRODUCTION INTEGRATION OR AUTHORITY GRANT**

## Evidence
- PR #74 commit `3104b4e184e6e964296a3fdf0cd8a20b4a21558a`, run `44152346032`: 12/12 tests PASS; Authority Clarity Validator PASS.
- Combined harness verifies a **public test-key** signature and synthetic checkpoint parent/sequence relationships. It binds signed checkpoint source/epoch/sequence/digest to a synthetic candidate.
- This does not prove authenticated source publication, exact EchoAuth gate-selected authority identity, transactional consistency, or production key trust.

## Binding must originate from actual gate state
The authority ID cannot be a caller-selected ID. At authorization evaluation, record:
1. Independently resolved authority record ID, authority source, subject, scope, version, and authority verdict.
2. For delegation, independently resolved grantor and source authority record; delegation ID, delegate, allowed scope, effective status and expiry.
3. Requested action/resource, policy version, identity verdict, correlation/idempotency IDs and canonical request digest.
4. XNOR namespace, target fingerprint digest, mapping source/provenance, mapping version/digest.
5. Signed checkpoint issuer/key ID, source epoch, sequence/digest, coverage scope, effective revocation time, observed/expiry times and authenticated consistency proof.
6. Immutable evidence digest tied to the **same** decision/audit and a documented revocation linearization point.

## Mandatory ordering
- Identity and authority resolution establish the *candidate* actual authority; they do not authorize.
- Independently verify trust policy and cryptographic source of revocation evidence.
- Compare exact signed mapping/target/authority/delegated grantor against resolved authority; mismatches HOLD.
- Check checkpoint freshness, lineage and effective revocation; REVOKED blocks, unknown/partial/stale/outage HOLD.
- Check policy and delegation independently. CLEAR coverage never overrides denial.
- Recheck or lock checkpoint consistency at commit; cached positive results must not bypass revocation revalidation.
- Audit verified snapshot reference and decision; audit failure blocks completion.

## Required negative tests
- Caller supplies A while gate resolves B; signed proof for A must not clear B.
- Direct authority matches but delegated grantor/source authority differs.
- Correct authority but wrong subject/action/resource/target/mapping digest.
- Signature valid under public test key but issuer not in approved registry.
- Checkpoint changes between preflight and commit; replay old positive cache.
- Revocation effective at same checkpoint, missing/partial coverage, expired proof, audit failure.
- Conflicting checkpoint source epochs or equivocation across concurrent requests.

## Review disposition
**HOLD** until authenticated issuer/key governance, independently verified source mapping, exact gate-selected authority binding, atomic revocation checkpoint semantics, cache invalidation and audit tests are demonstrated. Do not merge, enroll keys, update production gate or claim deployment from this document.

## Next bounded implementation
A **test-only authority-binding adapter** that receives an independently resolved authority object and a synthetic signed-lineage result, rejects mismatch and never returns authorization. Avoid production edits until trust policy and transactional semantics are approved.
