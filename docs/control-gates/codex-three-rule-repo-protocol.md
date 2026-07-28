# Codex Three-Rule Repo Protocol

## Purpose

This document defines a compact anti-drift protocol for Codex/repo work. It is intended to keep future task execution inside the named lane, especially when outside pressure, uncertainty, urgency, or low credit could cause scope drift.

This protocol operationalizes the authority boundaries established by `docs/control-gates/stage-governance-authority-lifecycle-doctrine.md`. It does not replace, enlarge, or reinterpret that doctrine.

## Definitions

Cycle = the repeated repo workflow.
Eco = the affected systems, files, concepts, or project layers.
Habitat = the safe condition that holds the work.
Routine = the exact action allowed by the task order.
Governance = the rule set that blocks, pauses, validates, or authorizes the routine.
WAIT = the protected posture required when exact governing authority is absent, exhausted, conflicting, unverifiable, or does not permit the proposed movement.

## Governed Execution Gate

Every governed repository task must pass through this sequence before and during execution:

```text
Anchor
↓
Locate
↓
Determine
↓
Classify
↓
Bound
↓
Decide
↓
Execute or WAIT
↓
Stop
```

### 1. Anchor

Verify the exact governing repository, branch, starting checkpoint, ancestry, named authority, task identity, and applicable governance boundaries.

Conversation, memory, technical expectation, or a nearby repository pattern must not substitute for the authoritative repository state.

### 2. Locate

Locate the last durably proven, accepted, closed, or otherwise governing checkpoint relevant to the exact subject.

A later-looking file, incomplete lane, open stage, or apparent architectural continuation does not displace the last valid governing checkpoint.

### 3. Determine

Determine whether authority for the exact proposed act is:

- explicit and current;
- absent;
- exhausted;
- conflicting;
- stale;
- unverifiable; or
- narrower than the proposed movement.

Capability is not authority. Readiness, evidence, architectural need, technical sequence, prior success, or an obvious next step cannot create authority.

### 4. Classify

Classify the requested activity before acting. Classification may include:

- assessment;
- inspection;
- implementation;
- cleanup;
- verification;
- documentation; or
- governance-changing action.

Classification does not authorize the activity. It identifies which authority and completion boundary must govern it.

### 5. Bound

State the exact permitted and prohibited:

- repository;
- branch;
- checkpoint and ancestry;
- files and paths;
- actions;
- outputs;
- executor;
- verification requirements; and
- stopping condition.

An open stage is a governed habitat, not standing execution permission. Anything outside the exact boundary remains unauthorized.

### 6. Decide

Ask one controlling question:

> Does explicit governing authority permit this exact movement from this exact checkpoint within this exact scope?

Engineering logic may shape how an authorized act is performed. It must not determine whether authority exists.

An identified gap is informational evidence, not a work order. A catalog of gaps is not a work queue. A gap may be inspected, recorded, or reported only within the authority already granted; it may not be selected for implementation without separate explicit authority.

### 7. Execute or WAIT

Execute only when the exact movement is explicitly authorized and all governing conditions are satisfied.

Resolve to WAIT when authority is absent, exhausted, conflicting, stale, unverifiable, or insufficiently bounded. WAIT is a valid protected outcome and is not failure to progress.

### 8. Stop

Stop immediately when:

- the exact bounded result is reached;
- required verification and reporting are complete;
- authority is consumed or exhausted;
- a contradiction or out-of-scope need is discovered; or
- the task resolves to WAIT, FAIL, BLOCKED, refusal, or another protected non-action result.

Completion requires verification and immediate stop. Completion, PASS, acceptance, evidence, or repository cleanliness does not authorize another activity.

## Rule 1. Habitat Before Routine

The safe condition must be defined before any action is allowed.

The lane defines the condition.
The condition defines the allowed action.
The allowed action does not expand the lane.

If the action discovers a need outside the habitat, Codex must stop and report instead of expanding scope.

## Rule 2. Silence Is Not Permission

Anything not named in the task order is outside scope.

Codex must not infer permission from:

- missing prohibitions
- broad wording
- urgency
- low credit
- obvious next steps
- nearby files
- related repo patterns
- prior tasks
- expected future work

If permission is not explicit, it is not granted.

## Rule 3. Stop Outside the Lane

If the work discovers a need outside the named lane, allowed file, or allowed action, Codex must stop and report.

Codex must not continue by:

- creating a second file
- editing README/index files
- changing code
- changing runtime behavior
- adding implementation details
- creating approval records
- creating approval mechanisms
- adding deployment logic
- adding credentials or secrets
- touching trading, broker, order-routing, sizing, or execution capability

## Operating Law

Anchor before movement.

Locate the last governing checkpoint.

Determine authority before interpreting capability.

Classify the act before bounding it.

Bound the exact lane before deciding.

Execute only under explicit authority; otherwise WAIT.

Verify, report, and stop.

Habitat before routine.

The lane defines the condition.
The condition defines the allowed action.
The allowed action does not expand the lane.

Silence is not permission.

Anything not named is outside scope.

If the routine discovers a need outside the habitat, stop and report.

## Non-Authorization Boundary

This protocol is for repo/Codex workflow control only.

It does not authorize:

- runtime behavior
- implementation
- deployment
- trading
- broker access
- credentials
- production activation
- approval records
- approval mechanisms
- execution capability
- live-money readiness
- paper-trading readiness
- simulation readiness
- SniperBot runtime capability
- LocalOps runtime capability
- EchoAuth product/runtime capability
- selection of a repository gap for work
- selection of a later stage or stage subject
- continuation after completion

## Pressure Boundary

Outside pressure, urgency, uncertainty, low credit, time limits, convenience, capability, architectural gaps, technical sequence, prior success, or obvious next steps do not expand scope or create authority.

## Stop Condition

Stop immediately if this requires:

- code changes
- README/index changes
- runtime behavior
- implementation work
- deployment logic
- approval records
- approval mechanisms
- credentials
- trading logic
- broker logic
- execution capability
- any second file
- movement beyond the named checkpoint, subject, or authority
