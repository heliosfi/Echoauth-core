# Control Matrix

## Core Thesis

Control does not mean monitoring behavior.
Control means unsafe state transitions are structurally unreachable by default unless required gates are satisfied.

Awareness is not control.
Documentation is not control.
Control begins when the system cannot move forward unless the required gate is satisfied.

The implementation path is:

awareness → structure → enforcement → proof

## Global Rule

Implement control before capability.

Do not add execution paths, approval paths, assignment paths, blocker-resolution paths, register mutations, broker connections, or live effects unless the corresponding control gate exists, is schema-defined, validator-enforced, test-covered, and CI-checked.

Every unresolved condition must fail closed.

No silent approval.
No inferred authority.
No hidden mutation.
No live execution by implication.
No successful default on missing data.

## EchoAuth / NI-AI Control Matrix

EchoAuth / NI-AI controls protect:

* parent/caregiver authority
* refusal
* child safety
* evidence integrity
* delegation scope
* lifecycle state
* uncertainty escalation
* auditability

Required fail-closed behavior:

* no authority clarity => HOLD
* no evidence => HOLD
* conflict detected => ESCALATE
* invalid transition => BLOCK
* child safety ambiguity => REFUSE or HOLD
* evidence-only phase => LOG_ONLY, no live effect

Forbidden outcomes:

* approval without parent/caregiver authority
* execution during ambiguity
* delegated caregiver exceeding scope
* school or clinic becoming final authority
* child refusal being overridden by convenience
* evidence-only phase creating live effects
* register mutation without approved transition
* silent blocker resolution
* runtime action from documentation-only state
* approval inferred from Slack, calendar, Drive, or notification activity

## Sniper Bot Control Matrix

Sniper Bot controls protect:

* execution mode
* signal validity
* market-data integrity
* risk limits
* manual approval
* kill-switch availability
* broker isolation
* auditability
* stop conditions

Required fail-closed behavior:

* no valid signal => NO_TRADE
* stale or conflicting data => NO_TRADE
* risk limit exceeded => BLOCK
* no manual approval for live mode => REQUIRES_MANUAL_APPROVAL
* kill switch unavailable => BLOCK
* broker not explicitly permitted => BLOCK
* execution uncertainty => HALT or LOG_ONLY

Forbidden outcomes:

* live order without explicit live mode
* live order without manual approval
* trade without stop condition
* trade above risk limit
* broker connection from dry-run code path
* execution when kill switch is unavailable
* trade on stale or conflicting market data
* silent failure treated as permission
* Slack notification treated as trading approval

## Separation Rule

EchoAuth / NI-AI and Sniper Bot may share the control pattern, but they must not share domain logic.

EchoAuth is care-governance and child-safety oriented.
Sniper Bot is trading-risk and execution-control oriented.

Do not merge care-governance logic with trading-execution logic.
Reuse the control pattern, not the domain rules.

## Workspace Integration Rule

Slack is coordination-only.
Google Drive may store and surface work.
Google Calendar may coordinate time and reminders.
GitHub remains the source of truth for code and governance artifacts.
Codex may propose or implement bounded repo changes only when scope is explicit.

No Slack message, app, workflow, notification, file preview, or calendar event creates:

* approval
* authority
* execution permission
* register mutation
* blocker resolution
* governance override
* broker connection
* trading permission

## Codex Implementation Rule

For every future Codex task, the task must answer:

1. What files may change?
2. What files must not change?
3. What tests must pass?
4. What unsafe outcome must remain impossible?

If any answer is missing, the task must remain HOLD / documentation-only.

## Current Status

This document is specification-only.
It does not create approval.
It does not resolve blockers.
It does not authorize runtime implementation.
It does not modify schemas.
It does not modify contracts.
It does not create broker access.
It does not create trading permission.
It does not alter any frozen governance artifact.
