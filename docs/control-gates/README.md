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
* `authority-clarity-conformance-expansion-plan.md` - auditor-facing candidate
  future Authority Clarity validator conformance scenarios before any test
  implementation; includes authority-source gaps, conflicting claims,
  delegation ambiguity, incomplete evidence chains, malformed escalation paths,
  unresolved uncertainty, HOLD / REFUSE / ESCALATE classification candidates,
  and audit evidence preservation expectations.
* `authority-clarity-compatibility-assessment.md` - read-only compatibility
  assessment after Authority Clarity validator conformance test expansion;
  records 23 Authority Clarity tests OK, 7 contract validation tests OK,
  full-suite command identified but not run, and nearby contract validation
  boundaries not disturbed.
* `authority-clarity-full-suite-proof.md` - read-only full-suite discovery
  proof after Authority Clarity conformance expansion and compatibility
  assessment indexing; records `python -m unittest discover -s tests`,
  `Ran 383 tests in 20.856s`, `OK`, clean final tree, and proof-only
  non-runtime boundary.
* `authority-clarity-full-suite-traceability-review.md` - documentation-only
  traceability review confirming the full-suite proof artifact is indexed, the
  compatibility assessment and full-suite proof form a coherent proof trail,
  and no schema, validator, test, CI, runtime, enforcement, approval, register,
  event-bus, broker/trading, service, agent, autonomous, click-through, or
  command-execution expansion is authorized.
* `authority-clarity-audit-evidence-mapping.md` - documentation-only mapping
  of the existing Authority Clarity governance/proof spine into
  auditor-facing evidence categories, including operating law, audit evidence
  expectations, schema, validator, tests, CI proof, compatibility proof,
  full-suite proof, traceability proof, and non-authorization boundaries,
  without creating audit storage, runtime logging, enforcement, approval, or
  new capability.
* `authority-clarity-closure-review.md` - documentation-only Authority Clarity
  phase closure record confirming the evidence chain is complete for this
  phase, proof artifacts are indexed, no unresolved gaps remain before
  closure, and the recommended next category is documentation-only Next
  Control Gate Selection.
* `next-control-gate-selection-review.md` - documentation-only review artifact
  for selecting the next bounded control-gate step after Authority Clarity
  closure; records Delegation Boundary Gate as the recommended next
  documentation-only gate planning category without approving implementation or
  capability expansion.
* `delegation-boundary-gate.md` - documentation-only planning artifact for
  future Delegation Boundary Gate evaluation; preserves parent/caregiver final
  authority and treats delegation as bounded, task-scoped, revocable,
  evidence-dependent, and non-transferable without approving implementation or
  capability expansion.
* `delegation-boundary-schema-readiness-plan.md` - documentation-only
  schema-readiness planning artifact for determining what must be true before
  any future Delegation Boundary schema-only draft could be considered; it does
  not approve schema creation, schema modification, validator work, tests, CI,
  runtime, enforcement, approval authority, blocker resolution, register
  mutation, event-bus behavior, or execution capability.
* `delegation-boundary-schema-only-approval-gate.md` - documentation-only
  approval-boundary artifact for any possible future Delegation Boundary
  schema-only draft; records schema work as not approved and prevents movement
  from readiness planning into schema drafting without explicit separate
  approval.

## Relationship to Control Matrix

Control gates follow the control-before-capability discipline described in
`../control-matrix.md` and `../../governance/principles.md`.

## Current Governance Chain

Authority Clarity currently follows:

`operating law -> documents -> schema -> validator -> tests -> CI proof -> audit evidence -> conformance expansion planning -> expanded conformance tests -> compatibility assessment -> full-suite proof -> full-suite traceability review -> audit evidence mapping -> closure review`

* Operating law: `authority-clarity-operating-law.md`
* Documents: this control-gates folder.
* Schema: `../../schemas/authority-clarity-gate.schema.json`
* Validator: `../../src/echoauth/contracts/authority_clarity_gate_validation.py`
* Tests: `../../tests/test_authority_clarity_gate_validation.py`
* CI: `../../.github/workflows/authority-clarity-validator.yml`
* Audit evidence: `authority-clarity-audit-evidence-model.md`
* Conformance expansion planning:
  `authority-clarity-conformance-expansion-plan.md`
* Expanded conformance tests:
  `../../tests/test_authority_clarity_gate_validation.py`
* Compatibility assessment:
  `authority-clarity-compatibility-assessment.md`
* Full-suite proof: `authority-clarity-full-suite-proof.md`
* Full-suite traceability review:
  `authority-clarity-full-suite-traceability-review.md`
* Audit evidence mapping:
  `authority-clarity-audit-evidence-mapping.md`
* Closure review: `authority-clarity-closure-review.md`

## Current Status

The files in this folder are documentation-only unless a bounded task
separately authorizes schema, validator, test, CI, or runtime enforcement work.
The separately approved Authority Clarity validator, validator-only tests, and
minimal validator-only CI workflow are listed above for traceability, along
with the documentation-only audit evidence model and conformance expansion
planning artifact. The compatibility assessment records read-only confirmation
that expanded Authority Clarity tests did not disturb nearby contract
validation boundaries. The full-suite proof records read-only discovery proof
without creating runtime approval. The full-suite traceability review confirms
the proof checkpoint is indexed and discoverable without authorizing capability
expansion. The audit evidence mapping records the auditor-facing evidence
chain without creating audit storage, runtime logging, enforcement, approval,
or new capability. The closure review records documentation-only phase closure
and points the next phase toward documentation-only Next Control Gate
Selection before implementation planning. The next control gate selection
review records Delegation Boundary Gate as the recommended next bounded
documentation-only step without implementation approval or capability
expansion. The Delegation Boundary Gate planning artifact records future
delegation-boundary evaluation concepts while preserving parent/caregiver
final authority and non-transferable delegated scope. The Delegation Boundary
schema-readiness plan records documentation-only readiness thresholds before
any future schema-only draft could be considered, without approving schema or
implementation work. The Delegation Boundary schema-only approval gate records
that schema work remains not approved and requires explicit separate approval
before any schema drafting may begin.

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
