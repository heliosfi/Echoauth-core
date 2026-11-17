# NODE XNOR → EchoAuth fail-closed enforcement boundary contract v0.1

**Disposition: REVIEW HOLD. Design only. No production gate changes, merges, deployment or trust enrollment.**

## Evidence
- PR #78: actual gate resolver provenance characterized; 14/14 CI PASS (four new plus ten imported).
- PR #80: actual gate observer; 20/20 CI PASS (ten new plus ten imported), run `44154852594`, job `134292709164`. Authority Clarity Validator PASS.
- PR #80 deliberately shows a crucial gap: when the observer rejects an untrusted claimed authority ID, the unmodified gate can still return AUTHORIZED because the observer is not wired as an enforcement dependency. **This is expected in a test-only observer and is not a secure integrated behavior.**

## Enforcement invariants
1. **Resolver first.** The real gate's independently selected authority record ID and resolution/evidence IDs are authoritative inputs to revocation checks. Caller-selected authority identifiers, XNOR hints, and test observer matches never select or override authority.
2. **Single gate.** The existing identity → authority → delegation → policy gate remains the only authorization decision path. No second authorizer, and no `MATCHED` / `CLEAR` result can produce authorization.
3. **Mandatory fail-closed dependency.** Before the gate can return an AUTHORIZED outcome, require authenticated XNOR coverage for the exact actual authority, grantor, subject, action, resource, scope, mapping digest and checkpoint. Mismatch, missing coverage, revoked evidence, trust failure, stale/rollback/fork, provider outage or ambiguity blocks authorization. A mismatched observation must never be ignored.
4. **Delegation.** Compare against the actual resolver requester (grantor), and independently retain delegation validation and source-authority equality checks.
5. **Trust.** Only independently approved issuer/key registry and authenticated source lineage qualify. A test signature, synthetic digest or caller-provided `verified=True` cannot qualify.
6. **Commit atomicity.** Bind the same authority and revocation snapshot to preflight, policy, commit and audit. If any checkpoint/mapping/revocation changes before commit, deny or restart from fresh evidence, never reuse a prior positive result.
7. **Cache.** Do not reuse positive authorization decisions across changes in trusted checkpoint state; disable positive cache until freshness/invalidation is demonstrated. Audit failures block and cannot silently return cached positives.
8. **Negative authority stays negative.** Identity, authority, delegation or policy denial is never upgraded by a coverage result.
9. **Audit.** Persist trusted issuer/key, source/epoch/sequence/digest, mapping provenance, resolver authority IDs, policy/delegation verdict and decision evidence in a tamper-evident record.

## Proposed review-only sequencing
A. Instrument an isolated **fail-closed gate facade** around a real gate fixture, using a test-only coverage provider. For mismatch/unknown/revoked, it must return a HOLD/blocked *facade result* without calling the real gate; matching synthetic coverage may call the gate but cannot override a denial. This demonstrates composition, not secure runtime integration.
B. Demonstrate actual authority cannot be inferred from caller data: the facade must consume a separately captured resolver output or internal gate-generated evidence; avoid re-resolving independently and accidentally creating TOCTOU.
C. Before production design, settle authenticated trust registry, mapping, atomic snapshot, cache and audit contracts. An external facade alone cannot guarantee the actual gate won't be invoked through a bypass path.
D. Independent review and explicit human authorization for any production gate modification.

## Required negative tests
- Caller A vs resolver B; delegated grantor swap; subject/action/resource/scope mismatch.
- Valid test-key signature but untrusted issuer; missing/expired/forked/rolled-back checkpoint; revocation effective at commit.
- Provider outage/partial coverage; positive cache replay; audit append failure.
- Independent policy DENY even with CLEAR; no alternative call path bypassing mandatory enforcement.

**Next smallest reviewable step:** isolated fail-closed composition tests showing mismatch blocks facade forwarding while matching synthetic evidence cannot override the real gate's policy denial. No production edits.
