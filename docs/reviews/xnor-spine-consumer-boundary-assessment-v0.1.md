# NODE XNOR × NI-AI Spine consumer boundary assessment v0.1

**Disposition: REVIEW HOLD — cross-repository evidence only.** No NI-AI Spine or Governed Agentic Engineering repository changes, runtime wiring, key enrollment, deployment, or activation.

## Repositories and evidence inspected
- `heliosfi/Echoauth-core`: current authorization gate and PRs #85–#87. PR #85 consolidated regression passed 294 XNOR review tests and 10 gate baseline tests; mandatory XNOR enforcement remains absent.
- `heliosfi/heliosfi-ni-ai-spine`: `docs/lineage/echoauth-s-module-to-governance-spine-developmental-trace.md`, `docs/records/founder-authorization.md`, and GitHub default-branch code searches for `AuthorizationGateService`, `EchoAuth`, `XNOR`, `authorization`.
- `heliosfi/governed-agentic-engineering`: `docs/repository-boundaries.md` and corresponding default-branch code searches.

## Grounded findings
1. The Spine developmental trace explicitly requires EchoAuth permission to be non-bypassable, distinguishes S-module condition recognition, S-mode state, MCG/MPC governance, CEG movement sequencing, EchoAuth permission and bounded execution. This is a **governance requirement**, not a runtime integration proof.
2. Search for the exact `AuthorizationGateService` identifier returned no matching file in the NI-AI Spine or Governed Agentic Engineering repositories. Search for `XNOR` returned no NI-AI Spine files and three historical staged-review assessment files in Governed Agentic Engineering. Search results do not prove the absence of aliases, generated code, remote services or deployed consumers.
3. The Spine's `docs/records/founder-authorization.md` explicitly limits the July 29, 2026 authorization to creating the repository and extracting documentation-only foundation; it does not authorize runtime implementation, downstream adoption, deployment or cross-repository mutation.
4. Governed Agentic Engineering `docs/repository-boundaries.md` states that methodology authority does not transfer project implementation authority; cross-project adoption requires separately scoped authority.
5. EchoAuth gate is directly callable without mandatory authenticated external NODE XNOR revocation checks. PR #87 inventories observed EchoAuth-local call sites; external API/agent/job/runtime paths remain unverified.

## Cross-boundary contract required before runtime wiring
- **Spine output:** proposal, scope, state and required permission provenance; never a self-authorizing execution directive.
- **XNOR evidence:** independently authenticated issuer/key, signed checkpoint lineage, effective revocation, freshness and exact authority-target mapping; MATCH is not permission.
- **EchoAuth decision:** independently selected actual authority, mandatory fail-closed revocation evaluation, delegation/policy checks, atomic commit and audit; a CLEAR checkpoint never upgrades DENY.
- **Execution:** separate bounded authorization and per-action continuation checks; RETURN does not reauthorize.
- **Repository authority:** explicit owner approval for each affected project's code changes and any operational deployment.

## Remaining evidence gaps
- Exhaustive cross-repository runtime call graph (imports, aliases, API endpoints, jobs, agent integrations and deployed services).
- Actual NI-AI Spine executable consumer interface, if any; current evidence is predominantly documentary.
- Trust anchors, key governance, checkpoint source, revocation-to-authority mapping, atomicity, cache invalidation and audit guarantees.
- Independent security review and migration/recovery strategy.

## Next bounded step
Construct isolated negative tests for the proposed mandatory boundary in an EchoAuth review-only module, using synthetic providers and explicit non-authorizing outputs. Do not change `src/echoauth/auth/authorization_gate.py` or claim that Spine-to-XNOR runtime wiring exists. If future cross-repo edits are proposed, seek separate scoped authorization first.

CAPABILITY != AUTHORITY; MATCH != ACCEPTANCE; PASS != PERMISSION; RETURN != REAUTHORIZATION.
