# Authority Clarity Gate Plan

## Purpose

This is a planning-only document for a future testable gate that prevents
EchoAuth / NI-AI decisions from proceeding unless authority is explicit,
current, and valid.

## Relationship to Control Matrix

This plan references `docs/control-matrix.md` and `governance/principles.md`.
It follows the control-before-capability discipline: control gates must be
designed before any capability can rely on authority, approval, execution, or
runtime effects.

## Gate Thesis

A decision cannot proceed unless authority clarity is resolved.

If authority is missing, stale, conflicting, delegated beyond scope, or
ambiguous, the future gate must fail closed.

## Future Inputs

Planned future inputs only:

* actor role
* asserted authority source
* authority scope
* delegated scope, if any
* requested action
* current lifecycle state
* evidence reference
* conflict status
* timestamp or freshness indicator

## Future Allowed Outputs

Planned future outputs only:

* ALLOW
* HOLD
* ESCALATE
* BLOCK
* LOG_ONLY

## Fail-Closed Rules

* missing authority => HOLD
* stale authority => HOLD
* conflicting authority => ESCALATE
* delegate exceeds scope => BLOCK
* school or clinic asserted as final authority => BLOCK
* evidence-only phase attempts live effect => LOG_ONLY / BLOCK
* ambiguity remains unresolved => HOLD

## Forbidden Outcomes

* approval inferred from Slack, Google Drive, Google Calendar, GitHub notification, or Codex message
* school or clinic becoming final authority
* caregiver delegate exceeding task scope
* decision proceeds without parent/caregiver authority clarity
* documentation-only state creating runtime authority
* silent fallback to ALLOW

## Future Test Ideas

Planning-only bullets:

* valid parent authority returns ALLOW
* missing authority returns HOLD
* conflicting authority returns ESCALATE
* delegate over-scope returns BLOCK
* school final-authority assertion returns BLOCK
* stale evidence returns HOLD
* Slack message cannot create approval
* documentation-only file cannot create runtime authority

## Non-Implementation Status

This file is planning-only.
It does not define a schema.
It does not define a contract.
It does not implement a validator.
It does not create runtime behavior.
It does not create approval authority.
It does not resolve blockers.
It does not mutate registers.
It does not affect event-bus behavior.
It does not affect trading or broker paths.
It does not modify CI.
