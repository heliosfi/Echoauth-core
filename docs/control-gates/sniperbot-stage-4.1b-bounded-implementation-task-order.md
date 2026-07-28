# Stage 4.1B Bounded Implementation Task Order

## Status

FOUNDER-AUTHORIZED BOUNDED IMPLEMENTATION ORDER -- STAGE 4 -- SIMULATION ONLY

## Authority

Founder Nicholas B. Carty authorized continuation through completion of the Stage 4.1B governed lane.

This task order releases implementation authority only for the exact repository, paths, behavior, tests, and boundaries stated below.

## Governing Inputs

Implementation must conform to:

1. `sniperbot-stage-4.1b-multi-variant-observation-contract-specification.md`
2. `sniperbot-stage-4.1b-multi-variant-observation-contract-independent-acceptance.md`
3. `sniperbot-stage-4.1b-observation-implementation-specification.md`
4. the accepted Stage 4.1A scenario-envelope implementation and acceptance record.

Any contradiction, missing prerequisite, path conflict, or required scope expansion requires refusal and return to WAIT.

## Authorized Repository

`heliosfi/SniperBot`

## Authorized Base

The implementation must begin from the current accepted default-branch lineage containing Stage 4.1A commit:

`085cd82742a93f0a631cb2185d868f719ddd84f5`

Later unrelated default-branch commits are permitted only when they do not contradict this order.

## Authorized Paths

Create exactly:

- `src/sniperbot/simulation/observation.py`
- `tests/test_simulation_observation.py`

No existing file may be modified under this task order.

## Authorized Behavior

Implement the closed multi-variant, caller-supplied, deterministic observation-content validator defined by the governing specification.

The implementation may:

- consume `SimulationObservationReference` from Stage 4.1A;
- represent the four closed payload variants;
- validate strict types and semantic constraints;
- canonicalize payload content deterministically;
- calculate and compare SHA-256 payload digests;
- return immutable accepted or refused decisions;
- run entirely in memory and without side effects.

## Required Validation

The implementer must run the repository's accepted Python test command and record:

- Python interpreter and version;
- exact command;
- total passed, failed, skipped, and errored tests;
- implementation commit SHA;
- changed-path list.

At minimum, all pre-existing tests and all Stage 4.1B tests must pass.

## Locked Prohibitions

This order does not authorize:

- modification of `scenario.py`, package `__init__.py` files, existing tests, workflows, configuration, or documentation in SniperBot;
- filesystem, fixture, environment, clock, randomness, logging, persistence, network, HTTP, websocket, subprocess, database, provider, adapter, ingestion, polling, or replay behavior;
- signals, strategies, confidence, ranking, risk, candidate intent, simulated actions, outcomes, orders, fills, brokers, accounts, capital, credentials, secrets, runtime orchestration, deployment, or live behavior;
- Stage 4 closure or Stage 5 entry.

## Completion State

Successful implementation results only in:

`IMPLEMENTED -- PENDING INDEPENDENT ACCEPTANCE`

Implementation does not self-accept and does not authorize the next subject.

## Refusal Conditions

Stop without mutation if:

- either authorized path already exists;
- the accepted Stage 4.1A reference type is absent or incompatible;
- implementation requires an existing-file modification;
- the specification cannot be implemented without broadening scope;
- validation cannot be executed or produces a failure that cannot be corrected within the two authorized paths.

## Post-Implementation Rule

After implementation and evidence capture, an independent acceptance record must inspect contract fidelity, changed paths, tests, deterministic behavior, boundary preservation, and repository lineage.

Until that acceptance is complete:

- Stage 4 remains OPEN;
- Stage 5 remains NONE;
- no additional implementation lane is implied;
- posture is WAIT.
