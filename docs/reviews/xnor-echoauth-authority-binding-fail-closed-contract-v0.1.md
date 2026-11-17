# NODE XNOR → EchoAuth authority binding and fail-closed consumer contract v0.1

**Disposition: DESIGN CANDIDATE — REVIEW HOLD. No runtime wiring.**

## Verified source surfaces
- `src/echoauth/auth/authorization_models.py`: `AuthorizationRequest` has no external revocation-evidence field.
- `src/echoauth/auth/authorization_gate.py`: `AuthorizationGateService.authorize` invokes `AuthorityResolutionRequest` without `revocation_records`; it does independently enforce identity, authority, delegation, policy.
- `src/echoauth/auth/authority_resolution.py`: revocation input is accepted as canonical JSON with `revocation_id`, `target_type=authority`, `target_id`, `effective_at`; effective revoked IDs are considered by the resolver.
- `src/echoauth/auth/authority_models.py`: explicit `AuthorityRecord.authority_record_id`, `authority_source_id`, `subject_id`, `scope`, `evidence_hash`, `status`.
- Review-only PRs #52 and #53 demonstrate the gap and synthetic-only evidence classification. Neither implements this mapping.

## Authority-record binding: proposed mandatory checks
1. The evidence producer must supply a cryptographically verified, provenance-bound XNOR target reference. No matching by name, role label, or digest substring.
2. A separately maintained, explicitly authorized mapping record must bind **(XNOR namespace, target digest, role, tier, scope, source identity)** to the exact EchoAuth `authority_record_id`, `authority_source_id`, `subject_id`, and applicable action/resource scope. This mapping record is not created by an XNOR PASS.
3. Require mapping version, immutable mapping digest, trust-anchor reference, effective interval, and accountable human approval provenance. Missing or ambiguous mapping → HOLD.
4. Require independently verified signature, authorized signer, target binding, revocation effective time, checkpoint monotonicity, freshness, and source trust. Unknown, stale, rollback, equivocation, mismatched target, or unverifiable evidence → HOLD/REJECT, never AUTHORIZED.
5. Translate only authenticated and effective revocations into EchoAuth's canonical `revocation_records`. An absence-of-revocation assertion is not an authority grant.
6. Preserve the independent EchoAuth identity → authority → delegation → policy checks; XNOR evidence must not set `AuthorizationOutcome.AUTHORIZED`, issue tokens, change authority status, or authorize execution.
7. Apply revocation checks to the grantor's source authority in delegated requests; the grantor resolution path must not bypass external revocation.

## Integration design decision still open
The current `AuthorizationRequest` lacks a revocation-evidence field. Two possible designs require independent security review:
- **Option A:** trusted revocation-provider dependency injected into the gate, queried after identity and before authority resolution, with required-source failures returning a non-authorizing outcome.
- **Option B:** authenticated, request-bound revocation evidence supplied through a new typed request field and reverified by the gate.

**Recommendation:** Option A, conditional on defining source trust, required-coverage policy, cache/freshness, audit semantics and failure handling. It avoids treating caller-supplied evidence as authoritative. This is a design recommendation, not an approved integration.

## Required synthetic acceptance tests for a future implementation
- valid identity + explicit authority + allowing policy + matching effective revoked target → `REVOKED`, never `AUTHORIZED`
- delegated request + revoked grantor authority → `REVOKED` or non-authorizing fail-closed decision
- required evidence missing/unreachable/stale → non-authorizing HOLD/DENIED/INVALID_AUTHORITY (choose canonical policy explicitly)
- mismatched target/role/tier/scope, ambiguous or unapproved mapping → non-authorizing
- replayed/rolled-back checkpoint or conflicted source → non-authorizing
- verified non-revoked evidence does **not** independently grant permission
- audit includes source/checkpoint/mapping digests and reason codes, without leaking secret material
- no mutation, key activation, execution, continuation, or token issuance from the evidence adapter

## Explicit blockers
Real trust-anchor custody, signer verification, source availability/freshness policy, non-rollback checkpoint, mapping registry approval, cross-repo contract ownership, and complete test evidence are **NOT VERIFIED**. No merge or deployment is authorized by this candidate.
