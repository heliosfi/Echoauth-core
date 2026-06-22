# Authority Clarity Resolution Path Plan

## Purpose

This file is planning-only and defines future resolution-path candidates for
Authority Clarity Gate outcomes such as HOLD, ESCALATE, BLOCK, REFUSE, and
LOG_ONLY.

## Relationship to Existing Documents

This resolution path plan references:

* `docs/control-matrix.md`
* `governance/principles.md`
* `docs/control-gates/README.md`
* `docs/control-gates/authority-clarity-gate-plan.md`
* `docs/control-gates/authority-clarity-enforcement-readiness.md`
* `docs/control-gates/authority-clarity-vocabulary.md`
* `docs/control-gates/authority-clarity-evidence-requirements.md`
* `docs/control-gates/non-authoritative-monitoring-node-plan.md`
* `docs/control-gates/monitoring-node-technical-boundaries.md`

## Resolution Thesis

The gate must fail closed technically, but resolve clearly for the human
authority anchor.

Fail-closed must not mean fail-silent. A stopped decision must expose why it
stopped and what bounded, authorized next steps are available without allowing
click-through override or unsafe bypass.

## Human Authority Anchor

The human authority anchor is the parent/caregiver or explicitly authorized
reviewer responsible for resolving authority ambiguity.

* school and clinical actors do not become final authority
* Slack, Google Drive, Google Calendar, GitHub, Codex, documentation-only files,
  planning-only files, monitoring outputs, and notifications do not become
  authority anchors
* human resolution must feed back into the Authority Clarity Gate rather than
  bypass it

## Resolution-Eligible States

Planning-only states that may require a resolution path:

* HOLD
* ESCALATE
* BLOCK
* REFUSE
* LOG_ONLY

Resolution eligibility does not imply permission to proceed.

## Visibility Invariant

Future stopped decisions should expose a structured explanation packet for the
authorized human authority anchor.

Candidate explanation fields:

* gate_state
* reason_code
* missing_primitive
* conflicting_primitive
* stale_field
* freshness_status
* conflict_status
* actor_role
* authority_source
* delegated_scope
* requested_action
* lifecycle_state
* evidence_reference
* trace_reference
* timestamp

This packet is explanatory only and does not create approval, authority, or
execution permission.

## Bounded Remediation Paths

Planning-only remediation path candidates:

* provide_missing_evidence
* refresh_stale_evidence
* resolve_actor_mismatch
* clarify_delegated_scope
* escalate_to_parent_or_caregiver_anchor
* confirm_block
* abort_request
* leave_in_hold
* request_manual_review

No remediation path may provide a click-through override.

## Forbidden Resolution Paths

Future resolution mechanisms must not allow:

* ignore_and_proceed
* click_through_approval
* approval_by_notification
* approval_by_slack_message
* approval_by_google_drive_file
* approval_by_calendar_event
* approval_by_github_notification
* approval_by_codex_message
* school_or_clinic_final_authority
* caregiver_delegate_scope_expansion_without_parent_or_caregiver_anchor
* documentation_only_runtime_authority
* monitoring_output_as_authority
* silent_fallback_to_ALLOW

## Feedback Into Gate

Resolution data must be treated as candidate input back into the Authority
Clarity Gate. It must not bypass the gate.

If supplied resolution data is missing, stale, conflicting, unauthorized, or
scope-mismatched, the gate must remain HOLD, ESCALATE, BLOCK, REFUSE, or
LOG_ONLY as appropriate.

## Anti-Bypass Design Goal

The resolution path should reduce human workaround behavior by making stopped
decisions legible, routed, and bounded while preserving refusal-first and
fail-closed behavior.

## Routing Boundaries

Planning-only routing candidates:

* parent/caregiver anchor for authority ambiguity
* reviewer/auditor for documentation or trace review
* system log for observation-only records
* no routing to non-authoritative actors as final decision-makers

Routing is not approval.

## Open Questions Before Implementation

Planning-only questions:

* Who qualifies as the human authority anchor in each lifecycle context?
* What explanation fields are required?
* Which stopped states require routing?
* Which stopped states require only logging?
* Which conflicts require ESCALATE versus BLOCK?
* What evidence can the human anchor provide?
* How is click-through override prevented?
* How is human resolution fed back into the gate?
* How are rejected resolutions logged?
* How is alert fatigue avoided?
* How is bypass behavior detected without creating monitoring authority?

## Non-Implementation Status

This file is planning-only.
It does not define a schema.
It does not define a contract.
It does not implement a validator.
It does not create tests.
It does not modify CI.
It does not create runtime behavior.
It does not create approval authority.
It does not create click-through override.
It does not resolve blockers.
It does not mutate registers.
It does not affect event-bus behavior.
It does not affect trading or broker paths.
It does not create enforcement behavior.
It does not create a monitoring service.
It does not create an agent.
It does not create autonomous action.
It does not grant command execution capability.
