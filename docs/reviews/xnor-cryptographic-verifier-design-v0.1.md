# NODE XNOR cryptographic verifier — independent review design v0.1

**Disposition: DESIGN CANDIDATE / HOLD. No enrolled keys, cryptographic implementation, runtime wiring, or production authorization.**

## Prior evidence
- EchoAuth PR #70, commit `4a1870ed9131103803c0be447d5aa350c140b87f`: workflow `44150542780` 19/19 negative-fixture tests PASS; Authority Clarity Validator PASS.
- The fixture classifier is intentionally **not a signature verifier**. Every envelope remains HOLD, including structurally plausible examples.

## Proposed verifier input and outputs
Input: immutable exact wire bytes, claimed issuer/key ID/algorithm, domain-separated signed payload, expected gate-resolved authority binding and trusted checkpoint policy. Inputs must be size-bounded and parsed under an approved canonical encoding.

Output is one of:
- `VERIFIED_COVERAGE`: signature and key policy valid, exact authority/target/scope/mapping binding valid, checkpoint lineage/freshness verified, no effective revocation in covered scope. **Not authorization.**
- `VERIFIED_REVOKED`: same trust checks, verified effective revocation. Gate must block.
- `HOLD`: any missing, malformed, unverifiable, ambiguous, stale, inconsistent, unsupported, unavailable, or out-of-scope evidence. No permissive fallback.

Verifier must never return execution authority. A verified coverage result only permits independent authorization checks.

## Decisions requiring explicit human-approved trust governance
1. Allowed cryptographic signature suite and hash suite, security level and canonical serialization profile (including Unicode, numbers, duplicate keys, ordering, normalization, domain separation).
2. Approved issuer identities and per-issuer signing key fingerprints, custody, permitted scopes and key lifecycle (rotation, expiry, compromise/revocation).
3. Authenticated mapping from XNOR namespace, target digest and scope to **actual gate-selected** EchoAuth authority and delegated grantor, with mapping version/digest.
4. Signed checkpoint source, consistency/monotonicity proof, anti-rollback state, maximum age, clock skew and recovery after outage.
5. Where the authorization transaction linearizes relative to revocation changes; positive-cache policy and audit guarantees.

Do not treat public key presence in an untrusted payload as enrollment or proof of trust.

## Validation pipeline (fail closed)
1. Reject oversized/noncanonical/ambiguous envelopes before interpretation.
2. Match schema and domain-separated signed content to approved version.
3. Resolve issuer and key **only from trusted registry**, reject unapproved algorithms, keys, issuers or scope.
4. Verify signature over exact approved canonical bytes using vetted crypto implementation.
5. Verify signed authority, delegated grantor, subject, action, resource, target and mapping against independently resolved gate context.
6. Validate authenticated checkpoint consistency, freshness, revocation effective time, and anti-rollback policy.
7. Persist verified evidence digest and checkpoint reference to decision/audit; recheck atomicity and disable/invalidate positive caching where required.
8. Permit only independent gate checks to determine authorization; audit failure blocks completion.

## Negative acceptance tests (required before production)
- Signature byte mutation, forged signature, unknown issuer/key, algorithm substitution, wrong domain, unsigned downgrade, key rotation/compromise.
- Canonicalization ambiguity: duplicate JSON keys, float/number equivalence, Unicode normalization, reordered fields, trailing data, oversize payload.
- Authority/target/mapping/subject/scope/delegation substitution.
- Checkpoint rollback, equivocation, stale timestamp, invalid consistency proof, revocation at same checkpoint, concurrent change between preflight and commit.
- Missing provider, partial coverage, timeout, audit failure, cache replay, key registry outage.
- CLEAR coverage with policy DENY or invalid identity remains non-authorizing.

## Evidence threshold to advance
A separately approved trust policy and test-only pinned keys, then isolated cryptographic verification against deterministic positive and negative vectors with independent review. Production trust enrollment, registry mutations, and gate integration require separate authority and evidence.

## Current conclusion
**Design-only HOLD.** No real cryptographic verifier has been built or tested by this candidate. PR #70's 19 PASS is structural negative-fixture evidence, not signature authenticity.
