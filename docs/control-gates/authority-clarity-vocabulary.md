# Authority Clarity Vocabulary Plan

## Purpose

This file is planning-only and defines vocabulary candidates for a future
Authority Clarity Gate.

## Relationship to Existing Documents

This vocabulary plan references:

* `docs/control-matrix.md`
* `governance/principles.md`
* `docs/control-gates/README.md`
* `docs/control-gates/authority-clarity-gate-plan.md`
* `docs/control-gates/authority-clarity-enforcement-readiness.md`

## Vocabulary Thesis

A future Authority Clarity Gate cannot be safely implemented until actor roles,
authority sources, delegation scope, conflict states, freshness states, and
allowed outputs are stable and unambiguous.

## Candidate Actor Roles

Planning-only role candidates:

* child
* parent
* caregiver
* caregiver_delegate
* school
* clinical
* system
* unknown_actor

Parent/caregiver authority remains final where applicable, and school/clinical
actors do not become final authority.

## Candidate Authority Sources

Planning-only authority source candidates:

* parent_authority
* caregiver_authority
* delegated_caregiver_scope
* documented_guardian_authority
* no_authority
* unknown_authority
* disputed_authority

Slack messages, Google Drive previews, Google Calendar events, GitHub
notifications, Codex messages, documentation-only files, and planning-only files
are not authority sources.

## Candidate Delegation Scope Terms

Planning-only delegation scope candidates:

* none
* task_scoped
* time_limited
* context_limited
* expired
* exceeded
* disputed
* unknown

## Candidate Conflict States

Planning-only conflict state candidates:

* none
* actor_mismatch
* authority_dispute
* scope_conflict
* stale_evidence
* lifecycle_mismatch
* institutional_overreach
* unresolved_ambiguity

## Candidate Freshness States

Planning-only freshness candidates:

* current
* stale
* expired
* missing_timestamp
* unverifiable
* unknown

## Candidate Gate Outputs

Planning-only future outputs:

* ALLOW
* HOLD
* ESCALATE
* BLOCK
* LOG_ONLY

Missing, stale, conflicting, disputed, unauthorized, or unknown authority must
not resolve to ALLOW.

## Forbidden Vocabulary Drift

Future implementation must not introduce terms that imply:

* child consent where only caregiver/parent authorization exists
* school or clinical final authority
* Slack approval
* Google Drive approval
* GitHub approval
* Codex approval
* documentation-created runtime authority
* approval by notification
* silent fallback to ALLOW

## Open Questions Before Implementation

Planning-only questions:

* Which actor role vocabulary is final?
* Which authority source vocabulary is final?
* What evidence reference format will be used?
* What timestamp/freshness rule will be used?
* Which lifecycle states must be checked?
* Which conflict states require ESCALATE versus BLOCK?
* Which missing-data cases return HOLD versus BLOCK?
* What audit fields are required for rejected decisions?

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
