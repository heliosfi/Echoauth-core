# Monitoring Node Technical Boundaries

## Purpose

This file is planning-only and defines technical boundary candidates for a
future non-authoritative monitoring node.

## Relationship to Existing Documents

This technical boundary plan references:

* `docs/control-matrix.md`
* `governance/principles.md`
* `docs/control-gates/README.md`
* `docs/control-gates/non-authoritative-monitoring-node-plan.md`
* `docs/control-gates/authority-clarity-gate-plan.md`
* `docs/control-gates/authority-clarity-enforcement-readiness.md`
* `docs/control-gates/authority-clarity-vocabulary.md`
* `docs/control-gates/authority-clarity-evidence-requirements.md`

## Technical Boundary Thesis

A monitoring node may observe and report risk signals, but must remain
technically unable to approve, authorize, mutate, resolve, execute, open CEG,
act as MCG, act as EchoAuth, create authority, or trigger live effects.

## Candidate Future Inputs

Planning-only input candidates:

* file change metadata
* git status output
* commit metadata
* changed file paths
* documentation-only task scope
* declared allowed files
* declared forbidden files
* authority evidence status
* vocabulary drift indicators
* stale evidence indicators
* conflict indicators
* lifecycle mismatch indicators
* Slack/GitHub/Google/Codex approval implication indicators
* forbidden path touch indicators

These inputs are observation inputs only and do not create authority.

## Candidate Future Outputs

Planning-only output candidates:

* observation_record
* risk_report
* drift_warning
* forbidden_path_warning
* missing_evidence_warning
* stale_evidence_warning
* conflict_warning
* recommended_hold
* recommended_escalate
* recommended_block

All outputs are advisory and non-binding.

## Isolation Requirements

Any future monitoring node must be isolated from:

* approval records
* blocker resolution mechanisms
* register mutation mechanisms
* runtime execution paths
* event-bus mutation paths
* broker adapters
* trading execution paths
* CEG gate-opening mechanisms
* MCG judgment mechanisms
* EchoAuth authorization mechanisms

## Logging Boundaries

Future logs may record observations only.

Future logs must not:

* grant approval
* imply authority
* resolve blockers
* mutate registers
* create execution permission
* create trading permission
* convert recommendation into action
* become evidence of authorization by themselves

## Failure Modes

Planning-only failure modes:

* monitor unavailable
* monitor stale
* monitor conflicting with source of truth
* monitor detects unknown state
* monitor cannot access expected metadata
* monitor reports false positive
* monitor misses a forbidden path touch
* monitor output is misread as approval

## Fail-Closed Behavior

* monitor unavailable => no approval, no execution, no mutation
* monitor uncertain => report risk / recommend HOLD
* monitor detects conflict => report risk / recommend ESCALATE
* monitor detects forbidden path touch => report risk / recommend BLOCK
* monitor output missing => no approval implied
* monitor output misformatted => no approval implied
* monitor output conflicts with governance source => governance source controls

## Source of Truth Hierarchy

* GitHub repo remains source of truth for code and documentation state.
* Governance documents define rules and boundaries.
* Slack remains coordination-only.
* Google Drive and Google Calendar remain coordination/storage only.
* Codex messages are not approval or authority.
* Monitoring outputs are observations only.

## Forbidden Technical Capabilities

The future monitoring node must not have capability to:

* write to approval records
* write to registers
* resolve blockers
* modify schemas
* modify contracts
* modify runtime files
* trigger event-bus behavior
* trigger CEG
* issue MCG judgment
* authorize EchoAuth decisions
* connect to brokers
* place trades
* execute commands that mutate state
* auto-commit
* auto-push
* self-expand permissions
* act autonomously

## Open Technical Questions Before Implementation

Planning-only questions:

* What exact metadata can be observed safely?
* Which paths may be observed?
* Which paths must be forbidden?
* Where can observation logs be stored without creating authority?
* What output vocabulary is final?
* How will false positives be reviewed?
* How will monitor failure be detected?
* How will monitoring remain separate from enforcement?
* How will monitoring remain separate from Codex execution?
* How will monitoring remain separate from Slack coordination?
* Who reviews monitoring reports?

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
It does not grant command execution capability.
