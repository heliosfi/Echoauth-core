# EchoAuth Governance Principles

EchoAuth is a deterministic authorization framework for environments where
coordination, interpretation, and execution must remain subordinate to human
authority. These principles govern every EchoAuth architecture, runtime, policy,
and implementation artifact.

## 1. Authority Before Execution

No action may execute until a designated authority layer has produced an
explicit authorization result.

Execution components may receive proposals, requests, or interpreted intent, but
they must not treat any of those inputs as permission. Permission is a separate
governance outcome.

## 2. Human Authority Preservation

Human authority remains the final source of approval, denial, escalation, and
accountability.

EchoAuth may structure authority, verify authority, record authority, and enforce
authority boundaries. It must not replace the legally or operationally
responsible human actor with autonomous system discretion.

## 3. Refusal Is Compliant

Refusal to execute is a valid system outcome.

When authority, context, confidence, identity, policy, or runtime integrity is
insufficient, the system must refuse, hold, halt, or escalate according to the
applicable state model. Continuing execution for convenience is non-compliant.

## 4. Separation of Powers

Meaning, judgment, authority, and execution are independent functions.

- NI-AI interprets meaning and context.
- MCG resolves authority and judgment.
- EchoAuth authorizes and enforces the runtime envelope.
- CEG sequences execution after authorization.
- Execution components perform only the authorized action.

No layer may silently absorb the responsibilities of another layer.

## 5. Deterministic Authorization

The same inputs, authority state, policy version, invariant set, and runtime
conditions must produce the same authorization outcome.

Determinism is required for auditability, patent support, developer
implementation, and institutional review.

## 6. Parent-Anchored Authority In Care Contexts

In child, school, clinical, and caregiver settings, parent or legal caregiver
authority is the anchor for authorization unless a formally recognized legal
authority supersedes it.

Teachers, aides, clinicians, and delegates may observe, document, assist, or
execute within a bounded permission. They do not become the authority source
unless explicitly granted that role by the governing authority model.

## 7. No Autonomous Permission Expansion

EchoAuth must never expand its own permissions.

Delegated permissions are bounded by scope, duration, role, context, and source
authority. If a requested action exceeds those bounds, the correct outcome is
refusal, hold, or escalation.

## 8. Auditability

Every authorization decision must be traceable.

Audit records must identify the request, authority source, policy version,
invariant set, decision state, reason, and execution result. Runtime enforcement
must support tamper-evident or immutable audit strategies where required.

## 9. Escalation Integrity

Escalation must preserve authority boundaries.

Escalation is not a shortcut around refusal. It is the process of routing an
unresolved request to the proper authority, reviewer, or safety state.

## 10. Accountability Preservation

Multi-party coordination must not remove accountability from authorized actors.

EchoAuth may support schools, caregivers, clinics, institutions, AI agents, and
runtime services working together, but each decision path must preserve who
proposed, who authorized, who executed, and why.

## Core Statement

Coordination proposes.

Governance permits.

Execution proceeds only after authorization.

## Control Matrix Reference

See `docs/control-matrix.md` for the control-before-capability discipline,
forbidden outcomes, fail-closed defaults, workspace integration boundaries, and
Codex implementation rules that keep control ahead of capability.

## Source Journal Files

- `docs/journal/2026-06-18_(1).html`
- `docs/journal/2026-02-09_(16).html`
- `docs/journal/2026-02-09_(24).html`
- `docs/journal/2026-02-12_(1).html`
- `docs/journal/2026-02-19_(23).html`
