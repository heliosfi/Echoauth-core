# Authority Clarity Validator-Only File Scope Proposal

Status: PROPOSAL ONLY -- NOT APPROVED

## Purpose

This proposal identifies candidate file scope for a future separate
validator-only implementation approval.

It supports exact-file approval discipline.

It prevents broad or implicit implementation permission.

No implementation is approved by this proposal.

## Existing Decision-Prep References

Existing decision-prep references:

* `docs/control-gates/authority-clarity-validator-readiness-plan.md`
* `docs/control-gates/authority-clarity-validator-only-approval-gate.md`
* `docs/control-gates/authority-clarity-validator-only-readiness-to-approval-review.md`
* `docs/control-gates/authority-clarity-validator-only-approval-decision-template.md`
* `docs/control-gates/authority-clarity-validator-only-approval-package-manifest.md`
* `schemas/authority-clarity-gate.schema.json`

## Repository Inventory Step

Read-only inventory was performed before drafting this proposal to avoid
inventing repository paths.

Inspection commands were limited to:

* `git status --short`
* directory listings for `src`, `tests`, `schemas`, and `docs/control-gates`
* targeted file-name searches for validator, validation, schema, governance,
  authority-clarity, and control-gates related files

Inventory observations:

* `src` contains `echoauth` and `authority` areas.
* `src/echoauth/contracts` contains existing contract validation modules.
* `src/echoauth/authority/validator.py` exists, but it relates to authority
  validation and is not a default candidate for Authority Clarity schema
  conformance work.
* `schemas/authority-clarity-gate.schema.json` exists as the schema target.
* `tests` contains existing validation and authority tests, but tests remain
  out of scope unless separately approved.
* `docs/control-gates` contains the validator-readiness and decision-prep
  documents listed above.

## Existing Files That May Be Candidates for Future Validator-Only Changes

Existing candidate files:

* `src/echoauth/contracts/__init__.py` - CANDIDATE ONLY -- NOT APPROVED; may be
  considered only if a future approval explicitly permits exporting a new
  validator-only symbol.
* `src/echoauth/contracts/validation.py` - CANDIDATE ONLY -- NOT APPROVED; may
  be considered only if a future approval explicitly permits integration with
  the existing repository contract validation harness.
* `schemas/authority-clarity-gate.schema.json` - CANDIDATE ONLY -- NOT
  APPROVED; candidate schema input/reference only, with no schema mutation
  approved by this proposal.

No existing file is approved for modification by this proposal.

## New Files That May Be Candidates for Future Validator-Only Creation

New candidate files:

* `src/echoauth/contracts/authority_clarity_gate_validation.py` - CANDIDATE
  ONLY -- NOT APPROVED; possible future validator-only module for mechanical
  conformance checking against `schemas/authority-clarity-gate.schema.json`.
* `docs/control-gates/authority-clarity-validator-only-implementation-report.md`
  - CANDIDATE ONLY -- NOT APPROVED; possible future documentation-only report
  if a separately approved validator-only phase requires a bounded completion
  artifact.

No new implementation file is approved for creation by this proposal.

## Forbidden File and Capability Scope

This proposal does not authorize changes to:

* tests
* CI
* runtime behavior
* enforcement behavior
* approval authority
* blocker resolution
* register mutation
* event-bus behavior unless separately and explicitly approved
* broker/trading paths
* services
* agents
* autonomous actions
* click-through overrides
* command execution capability

The following existing areas are not approved by this proposal:

* `tests/`
* CI configuration files
* runtime or execution modules
* event-bus behavior modules
* broker or trading paths
* service or agent code
* approval records
* blocker files
* register files

## Future Approval Requirements

Any future validator-only implementation must require separate explicit user
approval.

The approval must name exact allowed files.

The approval must name exact forbidden files and capabilities.

The approval must preserve HOLD / refusal-first / no-live-effect boundaries.

This file-scope proposal alone grants no permission.
