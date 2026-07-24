# Implementation Task Order 4.1A — Deterministic Simulation Scenario Envelope and Isolation Validator

## Authority

This task order is durably issued by Founder Order 10G as a governing artifact. Founder Order 10G does not authorize execution of this task order.

Implementation may begin only under a later, separate Founder Order.

The complete technical requirements are fixed by:

`Implementation_Specification_4.1A-SPEC.md`

This task order and the specification are inseparable. If either document is missing, incomplete, contradictory, or stale, refuse before mutation.

## Exact Subject

Implement:

**Deterministic Simulation Scenario Envelope and Isolation Validator**

The component must provide a deterministic, immutable, caller-supplied, in-memory scenario boundary for simulation-only use.

It must validate isolation and input integrity without activating simulation, reading external data, or causing external effects.

## Exact Repository and Branch

Repository:

`heliosfi/SniperBot`

Branch:

`main`

Exact starting checkpoint:

`a9614e0e83fee9453d4c161b915a7b0327f79ea9`

## Exact Governing Repository

Repository:

`heliosfi/Echoauth-core`

Branch:

`main`

Exact governing checkpoint:

`ecb5e55aeddaa388689dbc2b5100f9994d92c64b`

Echoauth-core must remain unchanged.

## Exact Authorized Paths

Create exactly these four paths:

1. `src/sniperbot/__init__.py`
2. `src/sniperbot/simulation/__init__.py`
3. `src/sniperbot/simulation/scenario.py`
4. `tests/test_simulation_scenario.py`

No other path may be created, modified, renamed, or deleted.

The two `__init__.py` files must contain no re-export, registration, startup logic, runtime behavior, or side effect.

## Exact Public Module

`sniperbot.simulation.scenario`

No package-root re-export is authorized.

## Required Pre-Mutation Checks

Before creating or modifying anything, verify:

1. both repositories are on `main`;
2. both repositories match the exact checkpoints above;
3. local `HEAD`, tracked `origin/main`, and live remote `main` agree;
4. divergence is `0/0`;
5. both worktrees are clean;
6. untracked-file count is zero;
7. Git lock-file count is zero;
8. all four authorized output paths are absent;
9. all governing records remain current and unrevoked;
10. a qualifying `<PYTHON3>` invocation can be selected under the required interpreter-resolution procedure and can run the exact validation command.

If any check fails, refuse and stop.

## Required Implementation

Implement the API and behavior defined in `Implementation_Specification_4.1A-SPEC.md`.

The implementation must:

- use only caller-supplied in-memory values;
- remain deterministic and pure;
- return immutable decisions;
- enforce exact refusal precedence;
- create stable SHA-256 fingerprints only for accepted requests;
- perform no I/O;
- use no external dependency;
- activate no runtime;
- cause no external action.

## Required Python Interpreter Resolution

Before any future implementation mutation, evaluate the following complete closed candidate list in the listed order:

1. `python`
2. `python3`
3. `py -3`

A candidate qualifies only if it reports Python 3.11 or later and lower than Python 4.0.

Select the first qualifying candidate and bind its complete invocation to the logical token `<PYTHON3>`.

Use the same selected invocation for every Python command throughout the future implementation lane. Record the selected invocation, resolved executable identity where available, and reported Python version as completion evidence.

If no candidate qualifies, a version mismatch occurs, or the interpreter invocation drifts, classify the future implementation lane as **BLOCKED** and halt without implementation mutation.

## Exact Validation Command

Run from the SniperBot repository root in PowerShell:

```powershell
$env:PYTHONPATH = "src"
<PYTHON3> -m unittest discover -s tests -p "test_simulation_scenario.py" -v
```

No interpreter outside the complete closed candidate list, dependency manager, test runner, environment, or alternate command is authorized.

## Required Static Review

Inspect the complete four-path diff and confirm:

- exact public API;
- exact enum vocabulary;
- frozen dataclasses;
- exact field order and defaults;
- exact refusal precedence;
- deterministic canonical fingerprinting;
- no forbidden imports;
- no forbidden fields;
- no filesystem, environment, live clock, network, subprocess, socket, broker, account, credential, order, fill, capital, deployment, persistence, logging, or runtime surface.

## Bounded Defect Correction

Defects may be corrected only when all corrections remain within the same four authorized paths and the unchanged specification.

No correction may:

- add a path;
- add a dependency;
- expand the API;
- change the subject;
- weaken refusal;
- introduce external capability;
- alter Echoauth-core.

## Required Commit

Create one commit with exact parent:

`a9614e0e83fee9453d4c161b915a7b0327f79ea9`

Commit message:

`Implement deterministic simulation scenario envelope`

The commit must contain exactly the four authorized new paths.

## Publication Sequence

After all tests and scans pass:

1. inspect the final diff;
2. commit once;
3. push `main`;
4. fetch the remote state;
5. verify local `HEAD`, tracked `origin/main`, and live remote `main` equality;
6. verify divergence `0/0`;
7. verify clean worktree;
8. verify zero untracked files;
9. verify zero Git locks;
10. report completion evidence;
11. stop.

## Refusal and Halt Conditions

Refuse or halt if:

- either checkpoint differs;
- either repository is dirty, divergent, stale, or locked;
- any authorized path already exists;
- any fifth path becomes necessary;
- any additional schema, fixture, dependency, manifest, config, workflow, documentation, or runtime path becomes necessary;
- any Echoauth-core copy, adaptation, reconstruction, import, or transfer becomes necessary;
- a third-party dependency is required;
- exact deterministic behavior cannot be proven;
- exact refusal precedence cannot be proven;
- no listed interpreter candidate qualifies or a Python version mismatch occurs;
- the selected interpreter invocation drifts during the lane;
- the exact validation command cannot run;
- any required test or static scan fails and cannot be corrected within the four-path lane;
- an unexpected change appears;
- publication would exceed the task boundary.

No refusal or failure authorizes repair, retry, expansion, or adjacent work.

## Required Completion Evidence

Report:

- exact starting commit;
- exact resulting commit;
- exact parent relation;
- exact four-path inventory;
- blob SHA for each path;
- exact validation command;
- selected `<PYTHON3>` invocation, resolved executable identity where available, and reported Python version;
- full test summary and total test count;
- mapping of tests to required validation and refusal conditions;
- deterministic fingerprint evidence;
- static forbidden-surface scan result;
- evidence Echoauth-core remained unchanged;
- evidence no artifact was copied or transferred;
- evidence no schema, fixture, dependency, config, CI, runtime, broker, credential, order, fill, capital, deployment, or operational path changed;
- local, tracked, and live remote equality;
- divergence `0/0`;
- clean worktree;
- zero untracked files;
- zero Git locks.

## Final Posture

Upon successful completion:

- subject: **IMPLEMENTED — PENDING INDEPENDENT ACCEPTANCE**
- task-order authority: **CONSUMED AND EXHAUSTED**
- Stage 4: **ENTERED**
- ordinary bounded Stage 4 authority: **ACTIVE**
- simulation activation: **NONE**
- implementation acceptance: **NOT PERFORMED**
- Stage 4 readiness acceptance: **NOT AUTHORIZED**
- Stage 5 authority: **NONE**

Stop.
