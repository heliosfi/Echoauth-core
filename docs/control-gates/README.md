# Control Gates

## Purpose

This folder contains planning, readiness, approval-boundary, and report
documents for Control Matrix gates. These documents preserve the governance
record without creating enforcement, execution, approval authority, runtime
behavior, broker/trading paths, service behavior, or agent behavior.

## Current Documents

* `authority-clarity-operating-law.md` - Authority Clarity operating law and
  vulnerability-first governance principle anchor; states that power must kneel
  to responsibility before it moves and traces the principle through documents,
  schema, validator, tests, CI, future runtime gates, and audit logs.
* `authority-clarity-gate-plan.md` - planning document for a future Authority
  Clarity Gate that would prevent EchoAuth / NI-AI decisions from proceeding
  unless authority is explicit, current, and valid.
* `authority-clarity-enforcement-readiness.md` - readiness checklist describing
  what must exist before future schema, validator, test, CI, or runtime
  enforcement work may begin for the Authority Clarity Gate.
* `authority-clarity-vocabulary.md` - planning document for candidate actor
  roles, authority sources, delegation scope terms, conflict states, freshness
  states, and gate outputs.
* `authority-clarity-evidence-requirements.md` - planning document for candidate
  evidence fields, evidence types, evidence properties, invalid evidence
  sources, and fail-closed evidence rules.
* `non-authoritative-monitoring-node-plan.md` - planning document for a future
  observation-only monitoring node that may report risk without authority,
  enforcement, execution, service, agent, or autonomous-action behavior.
* `monitoring-node-technical-boundaries.md` - planning document for future
  monitoring-node observation inputs, advisory outputs, isolation, logging,
  failure modes, and forbidden technical capabilities.
* `authority-clarity-resolution-path-plan.md` - planning document for
  resolution paths for HOLD, ESCALATE, BLOCK, REFUSE, and LOG_ONLY outcomes so
  fail-closed behavior does not become fail-silent.
* `authority-clarity-validator-readiness-plan.md` - validator-readiness
  planning only; it does not authorize validator implementation, and preserves
  future validation as separately approved mechanical conformance checking only.
* `authority-clarity-validator-readiness-checkpoint.md` - checkpoint-only
  phase-closure document confirming validator-readiness planning is complete,
  validator implementation remains unauthorized, and any future validator-only
  work requires separate explicit approval.
* `authority-clarity-validator-only-approval-gate.md` - approval-planning-only
  document that does not authorize validator implementation; future
  validator-only work requires separate explicit approval that is narrow,
  file-bounded, command-bounded, reversible, and includes stop conditions.
* `authority-clarity-validator-only-readiness-to-approval-review.md` -
  documentation-only / review-only decision-prep for a separate validator-only
  approval decision; it does not authorize validator implementation.
* `authority-clarity-validator-only-approval-decision-template.md` -
  documentation-only / decision-prep-only template with status
  PENDING -- NOT APPROVED; it does not authorize validator implementation.
* `authority-clarity-validator-only-approval-package-manifest.md` -
  documentation-only / decision-prep-only package manifest with status
  DECISION-PREP ONLY -- NOT APPROVED; it does not authorize validator
  implementation.
* `authority-clarity-validator-only-file-scope-proposal.md` -
  documentation-only / proposal-only file-scope proposal with status PROPOSAL
  ONLY -- NOT APPROVED; it does not authorize validator implementation.
* `authority-clarity-validator-only-implementation-approval-request-draft.md` -
  documentation-only / request-draft-only approval request draft with status
  REQUEST DRAFT ONLY -- NOT APPROVED; it does not authorize validator
  implementation.
* `authority-clarity-validator-only-approval-boundary-checkpoint.md` -
  documentation-only / boundary-checkpoint-only marker with status BOUNDARY
  CHECKPOINT -- NOT APPROVED; it does not authorize validator implementation.
* `authority-clarity-validator-only-implementation-report.md` - report
  document for the separately approved validator-only implementation; it does
  not authorize additional validator, runtime, enforcement, approval, broker,
  trading, service, agent, autonomous-action, click-through, or command
  execution capability.
* `authority-clarity-validator-ci-planning.md` - CI-planning-only document
  recording validated local commands and future CI boundaries; it does not
  authorize CI changes.
* `authority-clarity-validator-ci-design-plan.md` - CI-design-planning-only
  document for a minimal future validator-only workflow; it does not create or
  authorize CI.
* `authority-clarity-validator-ci-approval-boundary-checkpoint.md` -
  approval-boundary-only checkpoint documenting the boundary before separately
  approved minimal validator-only CI creation; it does not authorize additional
  CI changes.
* `authority-clarity-audit-evidence-model.md` - auditor-facing evidence
  expectations for Authority Clarity validation; preserves proof after
  validation without creating runtime, enforcement, approval, register,
  event-bus, broker/trading, service, agent, autonomous, click-through, or
  command-execution capability.

## Relationship to Control Matrix

Control gates follow the control-before-capability discipline described in
`../control-matrix.md` and `../../governance/principles.md`.

## Current Governance Chain

Authority Clarity currently follows:

`operating law -> documents -> schema -> validator -> tests -> CI proof -> audit evidence`

* Operating law: `authority-clarity-operating-law.md`
* Documents: this control-gates folder.
* Schema: `../../schemas/authority-clarity-gate.schema.json`
* Validator: `../../src/echoauth/contracts/authority_clarity_gate_validation.py`
* Tests: `../../tests/test_authority_clarity_gate_validation.py`
* CI: `../../.github/workflows/authority-clarity-validator.yml`
* Audit evidence: `authority-clarity-audit-evidence-model.md`

## Current Status

The files in this folder are documentation-only unless a bounded task
separately authorizes schema, validator, test, CI, or runtime enforcement work.
The separately approved Authority Clarity validator, validator-only tests, and
minimal validator-only CI workflow are listed above for traceability, along
with the documentation-only audit evidence model.

## Boundary

This folder does not create:

* approval
* authority
* runtime behavior
* enforcement behavior
* blocker resolution
* register mutation
* event-bus behavior
* broker access
* trading permission
* CI behavior

## Future Movement Rule

Future control-gate implementation must proceed only in separate, bounded tasks,
and only after required inputs, outputs, fail-closed behavior, forbidden
outcomes, tests, audit expectations, and non-authority boundaries are defined.
