# NI AI Future Capability Thesis v1 — Two-Page Reviewer Brief

**Prepared under N.B.C. authority — Nicholas B. Carty**

**Review status:** Prepared for possible independent technical/safety review. No external receipt, assignment, endorsement, acceptance, or organizational commitment is established.

**Frozen thesis checkpoint:** SAL-28

**Primary canonical repository checkpoint:** `heliosfi/Echoauth-core@72b6ea04594b16f1386816a9d729f51d0f8a0807`

## Research question

**How can AI governance architectures prevent authority from expanding implicitly as systems gain planning, reasoning, and tool-use capability?**

## Bounded thesis

The thesis proposes that increasingly capable AI systems may be governed through separately bounded, evidence-linked responsibilities in which understanding, planning, workflow passage, state assessment, permission, execution, return, and reassessment correspond without automatically transferring authority.

The central discipline is:

```text
CAPABILITY != AUTHORITY
PLANNING != PERMISSION
PROPOSAL != DIRECTIVE
STATE POSTURE != PERMISSION
PERMISSION != EXECUTION
EXECUTION != NEXT-ACTION AUTHORITY
RETURN != REAUTHORIZATION
REASSESSMENT != PERMISSION
```

This is not a claim that the current repository implements a complete safe autonomous runtime. It is a narrower claim about authority separation at tested boundaries and about contracts required for currently absent boundaries.

## Architecture

```text
UNDERSTANDING / PLANNING
-> INERT PROPOSAL OR STRUCTURED EVIDENCE
-> GOVERNED PASSAGE / STATE ASSESSMENT
-> INDEPENDENT PERMISSION EVALUATION
-> SEPARATELY BOUNDED EXECUTION
-> EVIDENCE RETURN
-> REASSESSMENT
```

Each crossing must establish only the authority native to that interface. A successful prior crossing must not create authority for the next one.

The NI AI Transition Envelope and Hawk validator preserve semantic/workflow passage while explicitly excluding permission enforcement and execution. Hawk `PROCEED` is passage posture only. The minimum SAI contract likewise carries state posture toward independent EchoAuth evaluation without carrying reasoning, commands, or executable payloads.

## Evidence currently supporting the thesis

Canonical repository evidence includes validation-only runtime transition assessment, authorization models/gates, Execution Control as eligibility-only evidence, Recovery as non-authorizing evidence, audit contracts, and explicit deferred-capability records.

Supplemental open/unmerged PRs provide focused adversarial/currentness evidence. They are **not canonical integration**.

The current adversarial framework is:

| Case | Result |
| --- | --- |
| Unauthorized state change | **PASS** |
| Stale permission | **PASS** |
| Implied authority transfer | **HOLD / PARTIAL** |
| Repeated processing and replay | **PASS** |
| Execution after return | **HOLD / PARTIAL** |

Therefore: **SAL-9 = HOLD — 3 PASS / 2 HOLD-PARTIAL / 0 FAIL.**

The absence of a FAIL does not satisfy the framework's all-five-PASS advance rule.

## What the PASS results currently establish

At the tested seams, state evidence cannot substitute for permission; historical authorization is not treated as a standing bearer grant; permission for one action/resource cannot silently authorize another; stale runtime-state evidence is independently rejected; replay/idempotency does not expand authority at the tested in-process validation layer; and Recovery/returned eligibility evidence does not itself restore permission.

These results support authority non-inheritance at specific interfaces. They do not establish end-to-end autonomous safety.

## Why two cases remain HOLD

**Implied authority transfer:** the implemented subset passes, but the repository has no real command execution/return consumer and no concrete planning-proposal consumer. Interface absence is preserved as unresolved rather than counted as PASS.

**Execution after return:** returned validation/recovery evidence is rejected as permission at the implemented seam, but no real executor and post-execution continuation/reassessment consumer exists.

SAL-25 now defines a future non-authorizing execution-result → return → reassessment contract. SAL-26 defines a future inert PlanningProposal → governance contract. Those documents specify what a legitimate future consumer must prove; they do not establish that such consumers currently exist.

## Important limitations

The evidence does not establish a complete NI AI → Hawk → MCG/MPC → SAI → EchoAuth → execution runtime, production readiness, autonomous command execution, full orchestration, durable distributed currentness/idempotency, exactly-once external effects, external-system or broker action, canonical cross-vocabulary state mappings, universal safety, technical novelty, patentability, external endorsement, or deployment authorization.

Open PR evidence must remain distinguishable from canonical `main`.

## Questions for the reviewer

Please focus on falsification and boundary accuracy:

1. Are any claims stronger than the cited evidence supports?
2. Are capability, proposal, state posture, permission, execution, return, and reassessment separated in a technically meaningful way?
3. Does the framework correctly refuse to count absent consumers as PASS?
4. What important implicit-authority-transfer failure mode is missing?
5. Are authorization freshness and runtime-state currentness sufficiently separated?
6. Are SAL-25 and SAL-26 adequate minimum contracts for future real consumers?
7. Where could semantic correspondence or state-vocabulary mapping accidentally become authority translation?
8. What single future implementation/test would best falsify or strengthen the thesis?

## Requested reviewer classification

For each material claim, please classify it as:

`SUPPORTED / PARTIALLY SUPPORTED / NOT SUPPORTED / INDETERMINATE`

and identify the evidence relied upon, missing/contradictory evidence, required correction, and highest-value next test.

An overall review may conclude:

```text
A. THESIS CLAIM SUPPORTED WITHIN STATED BOUNDARIES
B. PARTIALLY SUPPORTED — NARROWING REQUIRED
C. INDETERMINATE — ADDITIONAL EVIDENCE REQUIRED
D. NOT SUPPORTED BY CURRENT EVIDENCE
```

No such response should be interpreted as deployment authorization, organizational endorsement, or commercial commitment unless separately and explicitly established.
