# NODE XNOR mandatory enforcement / bypass analysis v0.1

**Disposition: REVIEW HOLD — design and evidence only; no production gate edits, deployment, merge, key enrollment or activation.**

## Verified test evidence
- PR #80 observer: 20 PASS (10 new, 10 imported). Observer mismatch is detected but cannot block the unmodified gate.
- PR #82 facade: 17 PASS (7 new, 10 imported), GitHub Actions run `44155376831`, job `134294577073`; Authority Clarity Validator PASS.
- PR #82's synthetic facade rejects HOLD before calling the real gate, and cannot upgrade independent authority/policy denial. It does **not** prove mandatory enforcement because `AuthorizationGateService.authorize` remains directly callable.

## Actual bypass risk
Any code path that directly invokes `AuthorizationGateService.authorize(request)` bypasses an optional wrapper/facade. The current gate resolves authority without authenticated XNOR revocation records, and its decision evidence/cache does not include a trusted external checkpoint. A green facade test therefore cannot justify production activation.

## Mandatory enforcement design constraints
1. Enforce XNOR revocation *inside the existing gate's trusted authorization path* or through a provably exclusive invocation boundary. An optional wrapper is insufficient.
2. Derive selected authority from the gate's own resolver result; no caller-selected authority ID, caller-supplied `verified` boolean, or arbitrary synthetic observer result.
3. Verify independently approved issuer/key, exact signed scope/target/mapping, authenticated source checkpoint lineage, revocation effective time, and freshness. Fail closed on missing/ambiguous/stale/forked/rolled-back/invalid/outage evidence.
4. Preserve the existing identity → authority → delegation → policy order and independent denials. Revocation CLEAR is not permission.
5. Bind resolver selection, revocation snapshot, delegation/policy, commit and audit in a consistent transaction. If trusted checkpoint changes, invalidate positive cache and re-evaluate or deny.
6. Treat direct internal gate access as a security-critical interface: enumerate all entry points, including tests, services, APIs, jobs and agents; no alternative authorized return path may bypass the mandatory check.
7. Record issuer/key, source/epoch/sequence/digest, mapping provenance, actual resolver authority IDs, and policy/delegation outcome in auditable evidence. Audit failure must block.

## Proposed security review tests
- Direct invocation of gate with revoked XNOR evidence cannot return AUTHORIZED.
- Caller-provided alternative authority ID cannot replace independently selected authority.
- Matching synthetic coverage cannot override policy DENY or identity/delegation failure.
- Revocation becomes effective between preflight and commit; positive cache cannot replay.
- Missing source, invalid signature, unknown key, outage, stale/rollback/fork/partial coverage fail closed.
- Audit failure prevents authorization; no bypass through service/API/job/agent entry points.
- Test-only flags or public test keys are never accepted as production trust.

## Dependency boundary
Do not alter production authorization before approved trust anchors, exact authority mapping, source authentication, atomicity/cache/audit contract and independent review. **Next smallest checkpoint:** test-only direct-gate bypass characterization showing that the optional facade cannot guarantee enforcement, followed by explicit inventory of gate invocation paths.

CAPABILITY != AUTHORITY; PASS != PERMISSION; RETURN != REAUTHORIZATION.
