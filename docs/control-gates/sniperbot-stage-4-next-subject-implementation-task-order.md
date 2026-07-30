# SniperBot Stage 4 Next-Subject Implementation Task Order

## Task-Order Disposition

**AUTHORIZED — SINGLE-USE BOUNDED IMPLEMENTATION LANE MAY BEGIN**

Nicholas B. Carty authorized the **SniperBot Stage 4 Next-Subject Implementation Specification and Task Order Authorization** lane. This record issues the resulting single-use task order for:

> **Deterministic Typed Fixture Scenario Content and Provenance Validator**

This task order is inseparable from:

`docs/control-gates/sniperbot-stage-4-next-subject-implementation-specification.md`

Specification checkpoint:

`8bbe942c40d8d558af0723eb4c1f37024eca1a61`

Specification blob:

`e0fda56c367c41c48c58ca8f117099de2a298624`

If the specification, accepted contract, acceptance record, repository anchors, or this task order is missing, stale, contradictory, moved, revoked, or unverifiable, the implementation lane must remain `WAIT` without mutation.

## Exact Governing Evidence

### SniperBot

- repository: `heliosfi/sniperbot`;
- accepted-contract checkpoint and implementation starting point: `998e2d2e91ecb758e084aad0112fd58608dcdb61`;
- independent contract-acceptance blob: `129d8e2777cac10314103d7c0de747e43afd4b25`;
- exact contract checkpoint: `fb2b26aaad63e17dce7b8b76b0ca92b9b70cd149`;
- exact contract blob: `8fe287db830505dfbc59664ad78dbed60f6baec6`;
- corrected-readiness checkpoint: `05e1137a201ae0c699ea8e28c60f3014dde24f7b`;
- corrected-readiness blob: `df5db9e1d040baf20f42b535744e75d9c7045ce0`;
- accepted Stage 4.1A source blob: `d4a8664cc9ec49b9caffd30157ab6992597fef79`;
- accepted Stage 4.1A test blob: `bfe34ff805e66149dc0de4ee8d9d85ee1efd9804`;
- canonical `main` observed during issuance: `36c34e363619ccf3f859631820dd12ca1bcf5001`.

### Echoauth-core

- repository: `heliosfi/Echoauth-core`;
- task-order branch: `sniperbot-stage-4-next-subject-implementation-task-order`;
- formation checkpoint: `5c6faea46932836fbb8f04d8a1435298ca8a62b2`;
- specification checkpoint: `8bbe942c40d8d558af0723eb4c1f37024eca1a61`;
- specification blob: `e0fda56c367c41c48c58ca8f117099de2a298624`;
- authorized paths in this issuance lane: exactly the specification and this task-order record.

The final task-order commit and blob must be reported after committed-state verification and become the exact governing Echoauth-core evidence for implementation.

## Exact Implementation Branch and Commit

Create the SniperBot branch:

`sniperbot-stage-4-next-subject-implementation`

Create it directly from:

`998e2d2e91ecb758e084aad0112fd58608dcdb61`

Required merge base:

`998e2d2e91ecb758e084aad0112fd58608dcdb61`

Required implementation commit message:

`Implement typed fixture scenario validator`

The result must be exactly one implementation commit ahead of the starting checkpoint. If connector limitations or an incidental technical failure would require multiple implementation commits, stop before mutation and report `BLOCKED`; do not silently weaken the one-commit evidence contract.

## Exact Authorized Paths

Create exactly:

1. `src/sniperbot/simulation/fixture_observation.py`;
2. `tests/test_fixture_observation.py`.

No other path may be created, modified, deleted, renamed, reformatted, regenerated, or re-exported.

Both authorized paths must be absent at the starting checkpoint. Existing Stage 4.1A and package paths must retain their exact blobs.

## Required Pre-Mutation Gate

Before any SniperBot write, prove:

1. the task-order commit and blob are resolved exactly;
2. the specification checkpoint and blob match this order;
3. contract commit `fb2b26aaad63e17dce7b8b76b0ca92b9b70cd149` has blob `8fe287db830505dfbc59664ad78dbed60f6baec6`;
4. acceptance commit `998e2d2e91ecb758e084aad0112fd58608dcdb61` has record blob `129d8e2777cac10314103d7c0de747e43afd4b25`;
5. implementation branch is absent;
6. proposed branch parent and merge base are exact;
7. both authorized output paths are absent;
8. Stage 4.1A source and test blobs are exact;
9. no current governing record revokes or conflicts with the task order;
10. canonical SniperBot and Echoauth-core heads have not moved in a way that invalidates the dual-anchor assessment;
11. one qualifying Python invocation can be selected from the closed candidate list; and
12. the selected invocation can import the accepted Stage 4.1A module and execute its existing test command.

Any failed precondition requires `WAIT` or `BLOCKED` before implementation mutation.

## Closed Python Interpreter Resolution

Evaluate this complete candidate list in order:

1. `python`;
2. `python3`;
3. `py -3`.

The first candidate reporting Python `>=3.11.0,<4.0.0` qualifies and becomes `<PYTHON3>` for the entire lane.

Record:

- complete selected invocation;
- reported version;
- resolved executable path when available; and
- confirmation that the invocation remained unchanged.

If none qualifies, resolution is ambiguous, or invocation identity changes, return `BLOCKED` without further mutation.

## Exact Required Commands

Use the repository root and `PYTHONPATH=src`.

POSIX form:

```text
PYTHONPATH=src <PYTHON3> -m unittest discover -s tests -p "test_simulation_scenario.py" -v
PYTHONPATH=src <PYTHON3> -m unittest discover -s tests -p "test_fixture_observation.py" -v
PYTHONPATH=src <PYTHON3> -m unittest discover -s tests -p "test*.py" -v
```

PowerShell form:

```powershell
$env:PYTHONPATH = "src"
<PYTHON3> -m unittest discover -s tests -p "test_simulation_scenario.py" -v
<PYTHON3> -m unittest discover -s tests -p "test_fixture_observation.py" -v
<PYTHON3> -m unittest discover -s tests -p "test*.py" -v
```

Select only the form native to the execution host. Do not use pytest, tox, nox, a dependency manager, a container, an alternate interpreter, or a different discovery pattern.

## Exact Output Requirements

Required successful counts:

- predecessor command: exactly 26 tests;
- new command: exactly 24 tests;
- combined command: exactly 50 tests.

Each command must exit `0` and end with `OK`. Elapsed time is explicitly variable and excluded from deterministic comparison. No failure, error, skip, expected failure, unexpected success, warning, traceback, or subtest failure is permitted.

The new 24-method inventory and the 67-case ordered negative matrix are frozen verbatim by the inseparable specification. No method, case, order, expected reason, or output count may be added, removed, combined, renamed, reordered, or weakened.

## Required Implementation Behavior

Implement exactly the accepted contract and inseparable specification:

- exact eleven-symbol public surface;
- exact four enum contracts;
- exact six frozen dataclasses;
- exact strict-type and content invariants;
- exact canonical Decimal and compact UTF-8 JSON behavior;
- exact ordered SHA-256 evidence;
- exact Stage 4.1A validation dependency;
- exact global refusal precedence;
- exact observation and field traversal order;
- deterministic immutable accepted and refused decisions;
- total fail-closed behavior for ordinary invalid objects;
- no mutation, shared mutable state, logging, retry, fallback, persistence, or side effect.

Do not inspect historical Stage 4.1B implementation bytes during implementation. The accepted contract already carries every authorized requirement. Historical code is neither needed nor permitted as an implementation source.

## Static Review Requirements

Before commit, inspect both complete new files and prove:

- exact path and public API scope;
- exact imports and no third-party dependency;
- exact enums, field order, annotations, frozen behavior, and signature;
- exact reason and traversal precedence;
- no package re-export;
- no filesystem, environment, credential, network, feed, broker, exchange, wallet, market-data, ingestion, replay, backtest, prediction, signal, strategy, candidate, classification, risk, simulated action, order, fill, execution, position, portfolio, balance, capital, clock, sleep, randomness, logging, persistence, database, service, worker, scheduler, CLI, API, subprocess, deployment, production, communication, or external-integration surface;
- no import-time action or shared mutable runtime state; and
- no Echoauth-core implementation import, copy, or adaptation.

Static checks must distinguish closed-denial vocabulary in accepted Stage 4.1A types from operational interfaces.

## Bounded Correction During Implementation

Before the single commit is created, defects may be corrected only within the two authorized uncommitted files and only to satisfy unchanged contract terms.

No correction may:

- modify or add a third path;
- alter the contract, specification, or task order;
- change the API or test inventory;
- add a dependency, fixture, schema, configuration, or workflow;
- weaken type checks, refusal order, invariants, tests, hashes, or isolation;
- inspect or restore historical implementation bytes;
- alter Echoauth-core; or
- add runtime or external capability.

After the implementation commit exists, this task order is consumed. Any correction then requires separate explicit authority.

## Required Single Commit

After all commands and static checks pass, create exactly one commit:

- parent: `998e2d2e91ecb758e084aad0112fd58608dcdb61`;
- message: `Implement typed fixture scenario validator`;
- changed paths: exactly the two authorized new paths.

Push only the named implementation branch. Do not push or move `main`, merge, rebase, cherry-pick, open a pull request, or synchronize any canonical index.

After push, refetch and prove the committed bytes reproduce the same three successful command outcomes.

## Required Completion Evidence

Report:

- exact SniperBot starting and result commits;
- exact result parent and merge base;
- exact implementation branch;
- exact two-path diff;
- pre-creation absence and resulting blob for each path;
- exact production public, enum, dataclass, field, signature, helper, and import inventories;
- selected interpreter invocation, path, version, and stability;
- exact three commands and complete outputs;
- exact `26`, `24`, and `50` test counts;
- complete 24-method inventory;
- mapping and result for all 67 ordered negative cases;
- deterministic repeated-decision and hash evidence;
- canonical trade, quote, and bar payload/hash evidence;
- static forbidden-surface evidence;
- preservation of Stage 4.1A source/test blobs and both package initializers;
- preservation of inherited governance records;
- final governing Echoauth-core task-order commit and blob;
- evidence Echoauth-core was unchanged during implementation;
- evidence no historical implementation was inspected, copied, restored, merged, or cherry-picked;
- evidence no third path or prohibited surface changed;
- post-push branch/ref equality and clean committed-byte verification; and
- terminal posture `WAIT — IMPLEMENTED, PENDING INDEPENDENT ACCEPTANCE`.

Implementation completion is not acceptance.

## Halt and Failure Conditions

Return `WAIT`, `BLOCKED`, or `FAIL` without unauthorized expansion if:

- any governing identity or ancestry differs;
- either implementation path already exists;
- implementation branch exists with unexpected content;
- a canonical move creates an unresolved dual-anchor conflict;
- a qualifying interpreter or exact command is unavailable;
- any expected test count differs;
- any test or subcase fails;
- a third path, dependency, fixture, schema, configuration, workflow, or contract change appears necessary;
- Stage 4.1A preservation fails;
- deterministic canonicalization or exact refusal behavior cannot be proven;
- historical implementation would need to be inspected or used;
- Echoauth-core would need modification during implementation;
- any runtime, broker, trading, persistence, deployment, production, communication, financial, or external surface becomes necessary; or
- exact one-commit publication cannot be preserved.

A halt does not authorize retry, repair, scope expansion, adjacent work, or another lane.

## Authority Consumption and Acceptance Boundary

This order is single-use. It is consumed by the first implementation mutation or substantive implementation attempt, whether the result is successful, failed, or blocked after mutation.

Successful completion authorizes only the statement:

`IMPLEMENTED — PENDING INDEPENDENT ACCEPTANCE`

Independent implementation acceptance requires a separate reviewer, explicit owner authority, and a new record bound to the exact implementation commit and both resulting blobs.

## Non-Authorization Boundary

This order grants no authority for:

- contract, specification, or task-order correction;
- historical Stage 4.1B restoration or reuse;
- any file outside the two named implementation paths;
- fixture files or external data;
- ingestion, parsing, normalization, replay, backtesting, signals, strategy, candidates, classification, risk, simulated actions, or learning;
- runtime orchestration or simulation activation;
- market-data access, paper or live accounts, brokers, exchanges, wallets, credentials, keys, tokens, orders, fills, execution, positions, portfolios, balances, funding, capital, or financial action;
- database or filesystem persistence;
- deployment, production, customer or administrative communication, external integration, or autonomous action;
- canonical-index synchronization, pull request, merge, or movement of `main`;
- implementation acceptance;
- Stage 4 readiness acceptance or closure; or
- Stage 5 entry.

## Final Task-Order Posture

`AUTHORIZED — ONE BOUNDED TWO-FILE, ONE-COMMIT IMPLEMENTATION ATTEMPT MAY PROCEED; UPON ATTEMPT OR COMPLETION THIS ORDER IS CONSUMED AND THE REPOSITORY MUST RETURN TO WAIT.`
