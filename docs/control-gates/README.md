# Control Gates

## Purpose

This folder contains planning and readiness documents for future Control Matrix
gates. These documents prepare control-gate work without creating enforcement,
execution, schema, validator, test, CI, or runtime behavior.

## Current Documents

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

## Relationship to Control Matrix

Control gates follow the control-before-capability discipline described in
`../control-matrix.md` and `../../governance/principles.md`.

## Current Status

The files in this folder are documentation-only / planning-only unless a future
task explicitly authorizes schema, validator, test, CI, or runtime enforcement
work.

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
