# Evidence-Bounded Adversarial Evaluation of Implicit Authority Transfer in Agentic AI Governance

> **ANONYMOUS MANUSCRIPT RECONSTRUCTION — ORIGINAL SUBMISSION SOURCE NOT RECOVERED**

**Artifact status:** Reconstructed anonymous review manuscript  
**Reconstruction date:** 2026-09-15  
**Evidence anchor:** Canonical repository checkpoint `627279543f296f3a34615879f0483ca20d778175`  
**External status:** Not submitted, reviewed, accepted, published, or endorsed

## Abstract

Agentic AI systems increasingly combine interpretation, planning, policy evaluation, tool use, and stateful workflows. If these functions are treated as one continuous authority-bearing process, a result produced at one boundary can be mistaken for permission at the next. This paper presents an evidence-bounded governance model in which capability, reasoning, proposal, state assessment, permission, execution eligibility, execution, return, reassessment, and continuation remain separately governed responsibilities. We examine five adversarial cases at concrete repository interfaces: unauthorized state change, stale permission, implied authority transfer, repeated processing and replay, and execution after return. Three cases pass at implemented seams; two remain hold/partial because the legitimate consumers required for full end-to-end evaluation do not exist. The consolidated result is therefore `HOLD — 3 PASS / 2 HOLD-PARTIAL / 0 FAIL`. The contribution is not a claim of a complete safe autonomous runtime. It is a falsifiable governance method: preserve exact evidence, prevent authority inheritance across interfaces, refuse to treat absence as proof, and reopen unresolved tests only when legitimate implementation creates a real evidence surface.

## 1. Research Problem

Modern AI systems can generate plans, rank actions, invoke tools, and interpret returned outputs. These capabilities create a recurring governance hazard: an output that is valid within one responsibility may be treated as authority for a different responsibility. A plan may become a directive, a state label may become permission, an authorization result may be treated as execution, or returned evidence may be reused as authorization for another action.

The research question is:

> How can AI governance architectures prevent authority from expanding implicitly as systems gain planning, reasoning, and tool-use capability?

The proposed answer is responsibility separation with explicit evidence at every consequential crossing. Correspondence between responsibilities is permitted; silent authority inheritance is not.

```text
CAPABILITY != AUTHORITY
REASONING != TRUTH
INFERENCE != EVIDENCE
PLANNING != PERMISSION
PROPOSAL != DIRECTIVE
STATE POSTURE != PERMISSION
PERMISSION != EXECUTION
EXECUTION != AUTHORITY FOR THE NEXT ACTION
RETURN != REAUTHORIZATION
REASSESSMENT != PERMISSION
ABSENCE != PASS
```

## 2. Threat Model

The threat model concerns implicit authority transfer rather than only malicious input. A failure can arise through ordinary composition when adjacent components use similar language but hold different responsibilities.

The assessed hazards are:

1. **Unauthorized state change:** supplied or fabricated state is accepted as governed state.
2. **Stale permission:** earlier authorization survives changed authority or runtime conditions.
3. **Implied authority transfer:** reasoning, proposal, passage, or state posture is interpreted as permission or executable direction.
4. **Repeated processing and replay:** repeated evidence or requests create new authority or duplicate consequential effects.
5. **Execution after return:** a prior execution result, recovery result, or returned validation artifact becomes permission for continuation.

The adversary may be an external caller, a malformed integration, a stale workflow, an over-broad orchestrator, or a well-intentioned component that confuses semantic correspondence with authority equivalence. The system is therefore evaluated against both hostile and accidental boundary collapse.

## 3. Governance Method

The method assigns each stage a bounded responsibility and requires a separately valid transition between stages.

```text
SOURCE
-> BOUNDED INTERPRETATION
-> INERT PROPOSAL OR REPRESENTATION
-> GOVERNED PASSAGE / STATE ASSESSMENT
-> INDEPENDENT PERMISSION EVALUATION
-> EXECUTION ELIGIBILITY
-> SEPARATELY AUTHORIZED EXECUTION
-> INERT RESULT EVIDENCE
-> REASSESSMENT
-> FRESH AUTHORIZATION, HOLD, OR STOP
```

No arrow is assumed merely because both adjacent components exist. The transfer object, producer, consumer, authority treatment, test evidence, and return or termination behavior must be traceable.

### 3.1 Source-first interpretation

Interpretation begins by receiving the source, identifying what is known and uncertain, preserving time and context, distinguishing fact from inference, checking domain authority, and accepting correction. A digital artifact may show an action or reaction without exhausting the responsible human source's prior understanding or purpose.

```text
REACTION != PURPOSE
VISIBILITY != MOTIVATION
OBSERVED RESULT != COMPLETE PRIOR UNDERSTANDING
ASSISTANCE != AUTHORSHIP
CONTRIBUTION != AUTHORITY
FOUNDATION != FINISHED WHOLE
```

This is an interpretive boundary, not a claim that hidden mental states can be technically verified. Human-supplied meaning may clarify the source's own intent; external factual claims remain independently testable.

### 3.2 Evidence classification

Repository artifacts are classified as implemented and tested, implemented but untested, partial, documented only, contract-defined without a consumer, absent, unresolved, or not applicable. A schema, interface, diagram, model, mock, or test fixture is not counted as a runtime consumer merely because it describes the expected relationship.

The method requires:

```text
PRODUCER
-> OUTPUT
-> ACTUAL CALL OR TRANSFER
-> CONSUMER
-> BEHAVIOR
-> TEST EVIDENCE
-> RETURN OR TERMINATION
```

### 3.3 No test-satisfaction build

Missing consumers are preserved as gaps. They are not fabricated or implemented solely to convert a withheld result into a pass. An unresolved adversarial case is reopened only when ordinary, separately authorized development creates the legitimate evidence surface that the test requires.

## 4. Repository Evidence Surface

The assessed repository contains bounded governance-validation machinery for identity, authority, delegation, policy evaluation, authorization, audit, runtime-transition validation, execution eligibility, refusal, escalation, review, override, halt classification, invariant validation, and recovery eligibility.

The strongest implemented execution-facing chain is:

```text
RuntimeTransitionRequest
-> RuntimeStateMachine.validate(...)
-> RuntimeTransitionDecision
-> ExecutionControl.validate(...)
-> ExecutionDecision / ExecutionEvidence
-> AUDIT
-> STOP AT ELIGIBILITY EVIDENCE
```

This chain validates eligibility. It does not dispatch a command, apply or persist the requested state transition, or prove a consequential external effect. The repository also includes recovery-eligibility validation, but no operational recovery consumer is established.

Representative evidence surfaces include:

- `src/echoauth/auth/authorization_gate.py`
- `src/echoauth/runtime/state_machine.py`
- `src/echoauth/runtime/transition_assessment.py`
- `src/echoauth/execution/controls.py`
- `src/echoauth/execution/service.py`
- `src/echoauth/runtime/recovery_service.py`
- `src/hawk/transition_envelope.py`
- `tests/test_runtime_state_machine.py`
- `tests/test_transition_assessment.py`
- `tests/test_execution_control.py`
- `tests/test_recovery_eligibility.py`
- `tests/test_hawk_transition_envelope.py`

These paths identify the review surface; the current reconstruction does not rerun the tests or independently reproduce the historical test baseline.

## 5. Adversarial Evaluation

### 5.1 SAL-11 — Unauthorized state change

**Result: PASS at the tested seam.**

The implemented validators reject attempts to substitute requested or fabricated state for governed runtime state. Validation returns decision evidence rather than applying the transition. This supports a bounded proposition: unauthorized state change is blocked at the tested validation interface.

It does not establish that every future stateful consumer will preserve the same boundary.

### 5.2 SAL-12 — Stale permission

**Result: PASS at the tested seam.**

Authorization freshness and runtime-state currentness are independently checked. Historical permission is not treated as a standing bearer grant after relevant authority or state evidence changes.

This supports stale-permission rejection at implemented interfaces, not durable distributed currentness across a production deployment.

### 5.3 SAL-13 — Implied authority transfer

**Result: HOLD / PARTIAL.**

Implemented state and permission seams reject several forms of authority substitution. The Hawk transition-envelope validator also preserves passage posture without treating `PROCEED` as permission enforcement or execution authority. However, no legitimate production planning/proposal consumer and no complete passage-to-permission-to-execution consumer are established.

The implemented subset may pass while the complete proposition remains untestable. Interface absence is not converted into proof of safety.

### 5.4 SAL-14 — Repeated processing and replay

**Result: PASS at the tested seam.**

At the assessed in-process validation layer, repeated or replayed requests do not create a new authority grant or expand the tested inert effect. This is a bounded replay and idempotency result.

It does not establish exactly-once external effects, durable distributed idempotency, or production message-delivery guarantees.

### 5.5 SAL-15 — Execution after return

**Result: HOLD / PARTIAL.**

Prior eligibility and recovery evidence are rejected as fresh permission at implemented validation seams. Yet the repository does not establish a real executor producing consequential result evidence or a post-execution consumer that reconciles that result and seeks fresh authorization for continuation.

Without that chain, the complete execution-after-return proposition cannot be tested end to end.

## 6. Consolidated Result

| Adversarial case | Result | Bounded interpretation |
| --- | --- | --- |
| SAL-11 — Unauthorized state change | PASS | Rejected at tested validation seam |
| SAL-12 — Stale permission | PASS | Stale authority/state evidence fails closed at tested seam |
| SAL-13 — Implied authority transfer | HOLD / PARTIAL | Implemented subset exists; legitimate end-to-end consumers are absent |
| SAL-14 — Repeated processing and replay | PASS | No new authority at tested in-process validation layer |
| SAL-15 — Execution after return | HOLD / PARTIAL | No real executor and post-execution continuation consumer |

```text
SAL-9 = HOLD — 3 PASS / 2 HOLD-PARTIAL / 0 FAIL
```

The consolidated gate requires five independent passes. Zero failures does not satisfy that rule. The correct conclusion is neither full validation nor system failure; it is a precise hold preserving three bounded passes and two unresolved cases.

## 7. Future Falsification Surfaces

Two contracts describe the minimum future evidence surfaces without establishing that those surfaces currently exist.

SAL-25 preserves the execution-return-reassessment sequence:

```text
EXECUTION RESULT
-> INERT RETURN EVIDENCE
-> REASSESSMENT
-> FULL FRESH VALIDATION
-> NEW CURRENT AUTHORIZATION
-> SEPARATELY BOUNDED EXECUTION
```

SAL-26 preserves the planning side: reasoning terminates in proposal-only evidence carrying an exact candidate action, resource, payload, and context. Proposal acceptance or semantic passage must not become permission, runtime transition, or executable directive by implication.

The highest-value future evaluation is not to build a consumer merely for the test. It is to wait until a legitimate planner or executor is required by ordinary system development, then trace the real producer-consumer chain and attempt to force authority inheritance at every crossing.

## 8. Discussion

### 8.1 Complete and incomplete states may coexist

A component can be complete within its own boundary while the broader runtime remains incomplete. A tested validator may correctly reject stale evidence even though no production orchestrator exists. Treating local completion as global completion creates lifecycle inflation; treating all incomplete integration as component failure discards valid evidence.

### 8.2 Refusal and no-action are valid outputs

HOLD, WAIT, refusal, and no-action are not automatically engineering defects. They may be the correct output when evidence, authority, currentness, or a legitimate consumer is absent. The governance objective is not continuous movement. It is legitimate movement with attributable evidence.

### 8.3 Foundations invite extension without authority transfer

A documented foundation may be questioned, tested, strengthened, or extended by later contributors. Their work should receive its own attribution. Contribution does not erase the originating work, and use of the foundation does not automatically transfer authorship, ownership, or final authority. Conversely, originating authorship does not make later factual or technical claims immune from independent review.

### 8.4 Action and reaction

A reviewer can inspect repository actions and subsequent reactions. That evidence can make a prior understanding materially legible, but it does not prove exhaustive access to motive or lived context. Responsible review therefore separates visible artifact, human-supplied context, bounded inference, and interpretive authority.

## 9. Limitations and Non-Claims

Current evidence does not establish:

- one integrated `NI-AI -> Hawk -> MCG/MPC -> SAI -> EchoAuth -> execution` runtime;
- autonomous command execution or full orchestration;
- a real executor plus post-execution reconciliation consumer;
- durable production persistence;
- durable distributed currentness or idempotency;
- exactly-once external effects;
- external-system or broker action;
- canonical cross-vocabulary state mappings;
- universal AI safety or global robustness;
- production readiness or deployment authorization;
- technical novelty, patentability, or priority;
- external institutional adoption or endorsement;
- independent scientific validation;
- paper submission, review, acceptance, or publication.

The repository previously recorded a historical baseline of 194 passing tests across specified Sprint 1 and Sprint 2 foundation scope. This reconstruction does not independently rerun or reproduce that baseline and therefore does not present it as a new experimental result.

## 10. Related Work — Verification Required

External related-work citations were not verified during this bounded reconstruction. Before submission, a separately authorized research lane should identify current primary sources concerning:

- authorization and least-privilege design;
- reference monitors and policy enforcement points;
- capability-based security;
- agentic AI tool-use governance;
- runtime assurance and safety envelopes;
- provenance, auditability, and accountable AI;
- replay resistance and distributed idempotency;
- human oversight and meaningful control.

No bibliographic placeholder in this section should be converted into a citation without confirming authorship, title, venue, year, identifier, and direct relevance from an authoritative source.

## 11. Conclusion

The evidence supports a bounded governance proposition: several implemented interfaces prevent specific forms of authority inheritance, stale permission reuse, unauthorized state substitution, replay-based amplification, and returned-evidence reuse at the seams tested. The evidence does not support a claim of complete end-to-end autonomous safety because two legitimate consumer chains are absent.

The defensible posture is therefore:

```text
PRESERVE WHAT PASSED
PRESERVE WHAT IS ABSENT
DO NOT BUILD SOLELY TO SATISFY THE TEST
REOPEN WHEN LEGITIMATE DEVELOPMENT CREATES A REAL EVIDENCE SURFACE
```

This posture treats uncertainty as governed state rather than a narrative problem to be hidden. Capability may increase while authority remains explicit, local, current, attributable, and independently reassessed.

## Appendix A — Canonical Repository Evidence

All paths below are relative to the canonical evidence checkpoint identified at the beginning of this reconstruction.

1. `docs/assessments/ni-ai-future-capability-thesis-v1-full-update-2026-08-27.md`
2. `docs/assessments/ni-ai-reviewer-one-page-orientation-2026-08-28.md`
3. `docs/assessments/ni-ai-architecture-evidence-traceability-consumer-gap-map-2026-08-28.md`
4. `docs/assessments/ni-ai-future-capability-thesis-v1-two-page-reviewer-brief.md`
5. `docs/partner/ni-ai-echoauth-independent-review-handoff-packet.md`
6. `runtime/sprint-2a-2p-consolidated-status-report.md`
7. `runtime/traceability-matrix.md`
8. `runtime/deferred-capabilities-register.md`
9. `src/echoauth/auth/authorization_gate.py`
10. `src/echoauth/runtime/state_machine.py`
11. `src/echoauth/runtime/transition_assessment.py`
12. `src/echoauth/execution/controls.py`
13. `src/echoauth/runtime/recovery_service.py`
14. `src/hawk/transition_envelope.py`
15. `tests/test_runtime_state_machine.py`
16. `tests/test_transition_assessment.py`
17. `tests/test_execution_control.py`
18. `tests/test_recovery_eligibility.py`
19. `tests/test_hawk_transition_envelope.py`

## Appendix B — Reconstruction and External-Status Boundary

```text
ORIGINAL MANUSCRIPT SOURCE — NOT RECOVERED
CURRENT DOCUMENT — NEW RECONSTRUCTION
OPENREVIEW PROFILE — ACTIVATED 2026-09-09
PAPER SUBMISSION — NOT ESTABLISHED
OPENREVIEW PAPER OR FORUM ID — NOT ESTABLISHED
EXTERNAL REVIEW — NOT ESTABLISHED
ACCEPTANCE — NOT ESTABLISHED
PUBLICATION — NOT ESTABLISHED
EXTERNAL ENDORSEMENT — NOT ESTABLISHED
COMPLETE INTEGRATED RUNTIME — NOT ESTABLISHED
PRODUCTION READINESS — NOT ESTABLISHED
```

This reconstruction creates no submission, external review, acceptance, publication, endorsement, runtime authority, implementation authority, deployment authority, ownership transfer, or authorship transfer.
