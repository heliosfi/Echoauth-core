# NI AI Workflow Relationship Assessment

## Status

Founder-authorized continuation of Workflow Assessment.

Relationship-assessment scope only.

This document does not authorize runtime, implementation, deployment, execution, trading, funding movement, autonomous action, command execution, or capability expansion.

## Purpose

The initial workflow assessment established that the repository already contains a complete governed operating rhythm.

A later review exposed one unsupported inference: the earlier assessment placed CEG beneath Hawk before the original CEG responsibility had been fully tested against repository evidence.

This assessment corrects that drift by asking the narrower question:

> What engineering responsibility was CEG created to preserve, and what relationship can the current evidence legitimately establish among CEG, Hawk, and EchoAuth permission enforcement?

## Evidence inspected

Primary current evidence:

- `governance/ceg.md`
- `docs/control-gates/echoauth-ceg-movement-sequencing-boundary-review.md`
- `architecture/system-overview.md`
- `governance/principles.md`

Primary historical source inspected:

- `archive/journal/2026-02-05_(18).html`

The current `governance/ceg.md` identifies its own source journals, including the historical file above.

## Historical identity established

Repository evidence identifies CEG as:

> **Crossroad Execution Gate**

The historical journal describes CEG as a sealed structural sequencing mechanism that enforces turn-based, authorized execution between subsystems.

It explicitly states that CEG does not generate decisions, goals, interpretations, or authority.

Its purpose includes:

- preventing execution-order drift;
- enabling auditability;
- enabling exact engineering implementation;
- serving as the textual companion to the sealed CEG diagram.

This evidence does not support the phrase `Cognitive Engine Gate` as CEG's canonical historical expansion.

The founder's memory of a four-way movement or crossroad function remains relevant as a clue to the diagrammatic and movement intent, but the repository text currently proves the canonical name `Crossroad Execution Gate`.

## CEG responsibility established

`governance/ceg.md` defines CEG as EchoAuth's structural execution-sequencing mechanism.

Its responsibilities include:

- receiving authorization results;
- issuing or validating single-use execution tokens;
- sequencing execution;
- enforcing one-action boundaries;
- preventing replay;
- validating payload integrity;
- handling channel loss;
- controlling concurrency;
- emitting execution audit events.

Its state model includes:

- `idle`;
- `authorized`;
- `token_issued`;
- `executing`;
- `completed`;
- `refused`;
- `hold`;
- `halted`;
- `revoked`.

Therefore, CEG is more than generic document routing or review-order sequencing.

It preserves a specific execution-crossing responsibility after authorization and before or during bounded execution.

## Relationship to EchoAuth permission enforcement

The evidence supports a clear boundary:

- EchoAuth determines and enforces whether permission exists under authority, policy, identity, and invariants.
- CEG consumes a valid authorization result and governs the structural conditions under which exactly one authorized action may cross into execution.

CEG does not create permission.

EchoAuth permission enforcement does not perform CEG's token, replay, payload, channel, concurrency, and execution-cycle responsibilities.

The legitimate relationship is sequential and bounded:

```text
EchoAuth permission enforcement
-> valid authorization result
-> CEG structural execution crossing
-> bounded authorized action
```

This sequence does not make CEG subordinate in product identity. It establishes the dependency required for CEG's responsibility to become active.

## Relationship to Hawk

Current evidence establishes Hawk as the refined workflow-control responsibility across the NI AI operating rhythm.

Current evidence establishes CEG as a specific structural execution gate with a sealed execution-state contract.

The evidence does not yet justify either of these claims:

- Hawk and CEG are the same thing.
- CEG is merely one generic subcomponent beneath Hawk.

The supported relationship is narrower:

> Hawk names the broader responsibility for preserving workflow state and legitimate movement across the full forward-and-return rhythm, while CEG preserves one specific crossroad: the controlled transition from valid authorization into single-action bounded execution.

This means CEG may participate within the broader workflow controlled by Hawk without losing its own explicit engineering identity.

The relation is responsibility-to-crossing, not replacement or renaming.

## Four-way movement interpretation

No inspected textual source explicitly uses the phrase `four-way movement`.

However, the crossroad identity and state model support a cautious interpretation.

CEG must distinguish multiple legitimate movement outcomes at the execution crossing, including:

- proceed into authorized execution;
- refuse before execution;
- hold pending resolution;
- halt or revoke when integrity fails.

This is not proof of an exact four-arrow diagram, but it is consistent with the founder's recollection that CEG represented directional movement at a crossroad rather than a simple linear pass-through gate.

The repository should not formalize an exact four-way diagram until the sealed diagram or additional source evidence is found.

## Corrected workflow finding

The earlier statement that `CEG expresses only part of Hawk's responsibility` was directionally useful but architecturally premature.

The corrected finding is:

> CEG preserves a specific execution-crossing responsibility. Hawk preserves the broader workflow responsibility across specification, dispatch, return, and transition release. Their relationship is connected but not reducible: CEG is neither proven identical to Hawk nor safely described as merely subordinate to it.

## Responsibility boundaries

### Hawk

Hawk controls workflow across the wider operating rhythm:

- dispatch readiness;
- handoff;
- state carriage;
- return;
- completion-state preservation;
- next-transition release.

Hawk does not create authorization or perform bounded execution.

### EchoAuth permission enforcement

EchoAuth determines whether a requested movement is permitted under explicit authority, policy, identity, and invariants.

Permission is necessary before CEG may sequence execution.

### CEG

CEG governs the structural crossing from authorized state into one bounded execution cycle.

It preserves:

- single-use execution permission;
- exact action and resource match;
- payload integrity;
- channel integrity;
- concurrency integrity;
- replay prevention;
- completion, refusal, hold, halt, and revocation states.

### Saloherm

Saloherm performs the bounded downstream responsibility itself and returns completion state.

CEG may govern the crossing into that bounded work, but CEG is not the downstream performer.

## Workflow relationship conclusion

The workflow relationship is now sufficiently clear to continue without collapsing responsibilities:

```text
Adumetric
specifies the legitimate bounded work

Hawk
controls workflow, handoff, state, and return

EchoAuth
establishes whether movement is permitted

CEG
controls the authorized execution crossing

Saloherm
performs the bounded downstream responsibility and stops
```

These are not five separate systems joined together.

They are distinct engineering responsibilities and mechanisms operating within the one intrinsically governed NI AI system and its EchoAuth environment.

## Preservation rule

Do not rename CEG to Hawk.

Do not reduce CEG to generic sequencing.

Do not expand CEG into authority, interpretation, or workflow ownership.

Do not finalize an exact four-way visual structure until the sealed diagram or equivalent evidence is located.

## Workflow status

Workflow Assessment is now complete enough to proceed.

The remaining unknown is diagrammatic precision, not responsibility ownership.

## Authorized next order

Proceed to Requirements Assessment.

The Requirements Assessment must test whether the repository connects each bounded task to the correct category, specific entity, authoritative source, evidence threshold, and transition requirement before it reaches workflow or execution crossing.
