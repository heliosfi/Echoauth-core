# Codex Three-Rule Repo Protocol

## Purpose

This document defines a compact anti-drift protocol for Codex/repo work. It is intended to keep future task execution inside the named lane, especially when outside pressure, uncertainty, urgency, or low credit could cause scope drift.

## Definitions

Cycle = the repeated repo workflow.
Eco = the affected systems, files, concepts, or project layers.
Habitat = the safe condition that holds the work.
Routine = the exact action allowed by the task order.
Governance = the rule set that blocks, pauses, validates, or authorizes the routine.

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

## Pressure Boundary

Outside pressure, urgency, uncertainty, low credit, time limits, convenience, or obvious next steps do not expand scope.

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
