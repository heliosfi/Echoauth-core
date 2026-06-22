# Authority Clarity Evidence Requirements Plan

## Purpose

This file is planning-only and defines evidence requirements candidates for a
future Authority Clarity Gate.

## Relationship to Existing Documents

This evidence requirements plan references:

* `docs/control-matrix.md`
* `governance/principles.md`
* `docs/control-gates/README.md`
* `docs/control-gates/authority-clarity-gate-plan.md`
* `docs/control-gates/authority-clarity-enforcement-readiness.md`
* `docs/control-gates/authority-clarity-vocabulary.md`

## Evidence Thesis

A future Authority Clarity Gate cannot safely return ALLOW unless the authority
evidence is explicit, current, role-aligned, scope-aligned, conflict-checked,
and traceable.

## Candidate Evidence Fields

Planning-only evidence fields:

* evidence_id
* evidence_type
* authority_source
* actor_role
* subject_role
* requested_action
* authority_scope
* delegated_scope
* lifecycle_state
* conflict_status
* freshness_status
* timestamp
* issuer
* reviewer
* trace_reference

## Candidate Evidence Types

Planning-only evidence type candidates:

* parent_authorization_record
* caregiver_authorization_record
* delegated_scope_record
* guardian_documentation_reference
* lifecycle_state_record
* conflict_review_record
* freshness_check_record
* audit_reference
* no_valid_evidence
* unknown_evidence

## Required Evidence Properties

Future evidence must be:

* explicit
* current
* traceable
* role-aligned
* scope-aligned
* lifecycle-aligned
* conflict-checked
* non-inferred
* non-notification-based

## Invalid Evidence Sources

The following must not count as authority evidence:

* Slack message
* Slack workflow
* Google Drive preview
* Google Calendar event
* GitHub notification
* Codex message
* documentation-only file
* planning-only file
* unreviewed note
* stale record
* conflicting record
* unknown source

## Fail-Closed Evidence Rules

* missing evidence => HOLD
* stale evidence => HOLD
* conflicting evidence => ESCALATE
* evidence source unknown => HOLD
* evidence scope mismatch => BLOCK
* delegate evidence exceeds scope => BLOCK
* school or clinic evidence asserts final authority => BLOCK
* notification-only evidence => HOLD
* documentation-only evidence attempts runtime authority => BLOCK
* evidence-only phase attempts live effect => LOG_ONLY / BLOCK

## Evidence Traceability Requirements

Future implementation must define:

* where evidence is stored
* how evidence is referenced
* how freshness is checked
* how conflicts are identified
* how review state is represented
* how rejected decisions are logged
* how evidence-only records avoid creating live effects

## Open Questions Before Implementation

Planning-only questions:

* What evidence reference format is final?
* Which evidence types are valid?
* Which evidence types are invalid?
* What makes evidence stale?
* What conflict statuses require ESCALATE versus BLOCK?
* Who can review evidence?
* How is delegated scope verified?
* How are evidence-only records prevented from creating authority?
* What audit fields are required for rejected evidence?

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
