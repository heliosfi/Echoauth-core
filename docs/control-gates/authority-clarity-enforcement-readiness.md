# Authority Clarity Enforcement Readiness Checklist

## Purpose

This checklist is planning-only. It defines readiness requirements that must be
met before future enforcement work may begin for the Authority Clarity Gate.

## Relationship to Existing Documents

This checklist references:

* `docs/control-matrix.md`
* `governance/principles.md`
* `docs/control-gates/authority-clarity-gate-plan.md`

## Readiness Thesis

Future enforcement must not begin until the gate's inputs, outputs, fail-closed
behavior, forbidden outcomes, tests, audit expectations, and non-authority
boundaries are explicitly defined.

## Required Before Schema Work

The following requirements must be clarified before any schema is created:

* authoritative actor roles
* allowed authority sources
* delegated authority scope
* evidence reference format
* conflict status vocabulary
* lifecycle state dependency
* freshness/staleness criteria
* allowed output vocabulary

## Required Before Validator Work

The following requirements must be clarified before any validator is created:

* missing authority behavior
* stale authority behavior
* conflicting authority behavior
* delegate over-scope behavior
* school/clinic final-authority rejection behavior
* evidence-only live-effect rejection behavior
* ambiguity handling behavior
* logging expectations for rejected decisions

## Required Before Test Work

Planned future test categories:

* valid authority
* missing authority
* stale authority
* conflicting authority
* delegate exceeds scope
* institutional actor incorrectly claims final authority
* evidence-only phase attempts live effect
* Slack/Google/GitHub/Codex message attempts to imply approval
* documentation-only file attempts to imply runtime authority
* unknown input fails closed

## Required Before CI Work

Readiness requirements before CI can enforce the gate:

* stable schema location
* stable validator location
* stable test location
* forbidden-path checks
* fail-closed regression tests
* documentation traceability requirement
* no live-effect assertion requirement

## Explicit Non-Authority Boundaries

None of the following may create approval or authority:

* Slack message
* Slack workflow
* Google Drive file preview
* Google Calendar event
* GitHub notification
* Codex message
* documentation-only file
* planning-only file

## Stop Conditions

The following conditions require HOLD before implementation:

* unclear actor role vocabulary
* unclear authority source vocabulary
* unclear conflict vocabulary
* unresolved parent/caregiver final authority rule
* unclear delegated scope behavior
* uncertain lifecycle state dependency
* unclear evidence freshness rule
* any proposed runtime behavior without tests
* any proposed schema without fail-closed outputs

## Non-Implementation Status

This file is planning-only.
It does not define a schema.
It does not define a contract.
It does not implement a validator.
It does not create tests.
It does not modify CI.
It does not create runtime behavior.
It does not create approval authority.
It does not resolve blockers.
It does not mutate registers.
It does not affect event-bus behavior.
It does not affect trading or broker paths.
