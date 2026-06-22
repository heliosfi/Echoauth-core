# Authority Clarity Validator-Only Approval Gate

## Purpose

This file is documentation-only / approval-planning-only.

It defines the explicit approval conditions required before any future
Authority Clarity validator-only implementation work may begin.

This document does not approve validator implementation.
This document does not create validator logic.
This document does not create tests or CI.
This document does not create runtime or enforcement behavior.
This document defines the gate that must be satisfied before a separate future
validator-only task can be authorized.

## Current Locked State

* Repo: `heliosfi/Echoauth-core`
* Branch: `main`
* Latest known commit: `84f8391f3b4eadca4bd9c7389a2164f4d8d9fb42`
* Validator-readiness checkpoint exists and is indexed
* Validator-readiness planning is complete
* Validator implementation remains unauthorized

## Approval Gate Principle

Future validator-only work may begin only after a separate explicit approval.

Approval must be narrow, file-bounded, command-bounded, and reversible.

Approval of validator-only work must not imply tests, CI, runtime, enforcement,
event-bus, broker/trading, service, agent, autonomous action, click-through
override, or command execution capability.

## Required Approval Contents

Any future approval order must define:

* Exact files allowed to be created or modified
* Exact files forbidden to modify
* Allowed commands
* Forbidden commands
* Stop conditions
* Reporting requirements
* Whether tests are allowed or prohibited
* Whether CI changes are allowed or prohibited
* Whether runtime or enforcement behavior is allowed or prohibited

## Allowed Future Validator-Only Scope

Planning assumptions only:

* Mechanical shape checking may be considered later
* Required field checking may be considered later
* Enum/value checking may be considered later
* Non-authority source detection may be considered later
* Forbidden outcome detection may be considered later
* Missing evidence detection may be considered later
* Conflict indication may be considered later
* Review-required reporting may be considered later

This list is not approval to implement.

## Forbidden Future Scope

Forbidden future scope:

* No authority grant
* No execution approval
* No blocker resolution
* No register mutation
* No event-bus transition
* No runtime behavior
* No enforcement behavior
* No broker/trading activation
* No service creation
* No agent creation
* No autonomous action
* No click-through override
* No command execution capability

## Required Stop Conditions

Work must stop if any future task attempts to:

* Combine validator implementation with tests or CI unless explicitly approved
* Treat validation success as authority or execution permission
* Convert ALLOW_CANDIDATE into execution
* Open or alter Crossroad Execution Gate behavior
* Perform MCG judgment
* Authorize EchoAuth decisions
* Resolve blockers
* Mutate registers
* Trigger event-bus behavior
* Touch broker/trading paths
* Create service, agent, autonomous action, click-through override, or command
  execution capability

## Required Reporting Requirements

Any future validator-only task must report:

* Exact files changed
* Exact git status
* Result of `git diff --check`
* Whether tests were run or explicitly not run
* Confirmation no forbidden files were modified
* Confirmation no unauthorized capability was created
* Confirmation nothing was staged, committed, or pushed unless explicitly
  authorized

## Non-Authorization Statement

This file is documentation-only.
This file does not authorize validator implementation.
This file does not authorize tests, CI, runtime, enforcement, approval
authority, blocker resolution, register mutation, event-bus behavior,
broker/trading behavior, service, agent, autonomous action, click-through
override, or command execution capability.
