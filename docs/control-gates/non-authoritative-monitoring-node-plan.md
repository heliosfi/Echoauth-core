# Non-Authoritative Monitoring Node Plan

## Purpose

This file is planning-only and describes a future monitoring node that may
observe and report Control Matrix risk conditions without authority or execution
power.

## Relationship to Existing Documents

This monitoring node plan references:

* `docs/control-matrix.md`
* `governance/principles.md`
* `docs/control-gates/README.md`
* `docs/control-gates/authority-clarity-gate-plan.md`
* `docs/control-gates/authority-clarity-enforcement-readiness.md`
* `docs/control-gates/authority-clarity-vocabulary.md`
* `docs/control-gates/authority-clarity-evidence-requirements.md`

## Monitoring Thesis

A monitoring node may detect risk, drift, missing evidence, stale state,
conflict, or forbidden movement, but it must not approve, authorize, mutate,
resolve, execute, or override governance.

## Allowed Future Observations

Planning-only observation candidates:

* missing authority evidence
* stale authority evidence
* conflicting authority evidence
* actor role mismatch
* delegated scope mismatch
* institutional overreach risk
* evidence-only live-effect risk
* documentation-only authority drift
* Slack/Google/GitHub/Codex approval implication risk
* lifecycle mismatch
* forbidden path touched
* unexpected file change
* runtime path touched during documentation-only task

## Allowed Future Outputs

Planning-only output candidates:

* OBSERVE_ONLY
* REPORT_RISK
* RECOMMEND_HOLD
* RECOMMEND_ESCALATE
* RECOMMEND_BLOCK
* LOG_OBSERVATION

These outputs are non-binding and do not create approval, authority, or
execution permission.

## Forbidden Monitoring Node Powers

The monitoring node must not:

* approve authority
* resolve blockers
* mutate registers
* modify schemas
* modify contracts
* modify runtime behavior
* trigger event-bus behavior
* trigger execution
* connect to broker paths
* create trading permission
* override MCG
* open CEG
* override parent/caregiver authority
* convert observations into approvals

## Separation from MCG / CEG / EchoAuth

The monitoring node is not MCG.
The monitoring node is not CEG.
The monitoring node is not EchoAuth.
The monitoring node is not an authority source.
The monitoring node is observation-only unless future bounded tasks separately
define safe reporting behavior.

## Fail-Closed Monitoring Rules

* if monitor cannot determine state => REPORT_RISK / RECOMMEND_HOLD
* if monitor detects conflict => REPORT_RISK / RECOMMEND_ESCALATE
* if monitor detects forbidden path touched => REPORT_RISK / RECOMMEND_BLOCK
* if monitor detects approval implied from Slack, Google, GitHub, Codex, documentation, or planning file => REPORT_RISK / RECOMMEND_HOLD
* if monitor fails or is unavailable => no approval, no execution, no mutation

## Open Questions Before Implementation

Planning-only questions:

* What inputs may a monitoring node observe?
* Where may observations be logged?
* What file paths may be monitored?
* What is the stable risk output vocabulary?
* How are false positives handled?
* How are monitor failures handled?
* What reports are safe to produce?
* Who reviews monitoring reports?
* How is monitoring kept separate from authority?
* How is monitoring kept separate from enforcement?

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
It does not create enforcement behavior.
It does not create a monitoring service.
It does not create an agent.
It does not create autonomous action.
