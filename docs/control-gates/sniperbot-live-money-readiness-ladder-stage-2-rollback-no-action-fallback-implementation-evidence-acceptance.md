# SniperBot Stage 2 Rollback / No-Action Fallback Implementation-Evidence Acceptance

## Acceptance Status and Boundary

`ACCEPT BOUNDED ROLLBACK / NO-ACTION IMPLEMENTATION EVIDENCE`

Repository: `heliosfi/Echoauth-core`  
Current checkpoint: `e9b4dddeca3ab8d1cb0867c53d1c2c2d9bc71a95`

This acceptance covers only the pure Rollback / No-Action Fallback evaluator,
its frozen structures, closed vocabularies, deterministic first-match behavior,
exact correlation preservation, supplied-object non-mutation, and direct tests.
It is not integration authority and creates no rollback, recovery, reset, FSM,
EchoAuth runtime, execution, or Stage 3 authority.

## Accepted Provenance and Files

Implementation commit: `c172aaed8382399c117fe9fc5653ac80b3f63965` (`feat: add
rollback no-action fallback evaluator`).

Test-evidence commit: `e9b4dddeca3ab8d1cb0867c53d1c2c2d9bc71a95` (`test:
complete rollback no-action evidence`).

Accepted implementation files:

* `src/sniperbot/rollback/__init__.py`
* `src/sniperbot/rollback/fallback_decision.py`

Accepted direct test file:

* `tests/test_sniperbot_rollback_no_action_fallback.py`

## Accepted Contract Evidence

Vocabulary counts are exactly: 2 outcomes, 14 full reason codes, 13
subject-emittable reason codes, 5 RequiredAction values, 3 subject-emittable
actions, and 6 descriptive FSM states.

`UNKNOWN_CONDITION` remains vocabulary-only and is not emitted because valid
typed requests are covered deterministically and unknown raw inputs are
rejected before typed construction. `FOUNDER_AUTHORITY_REQUIRED` and
`RESET_REQUIRED` remain vocabulary-only and non-emittable. No aliases, hidden
fallbacks, or free-text replacements exist.

The exact first-match order is:

1. rollback-evidence contradiction;
2. rollback-required and no-action conflict;
3. one of the three closed undefined combinations;
4. supplied authority failure;
5. rollback evidence missing;
6. rollback evidence stale;
7. rollback evidence insufficient;
8. rollback required but unavailable;
9. rollback externally required;
10. explicit no-action;
11. ordinary no-action fallback.

Lower-precedence facts cannot change the selected result. The only undefined
combinations are evidence absent while current, evidence absent while
sufficient, and evidence stale while sufficient.

Authority evidence is optional, contextual, non-authorizing, and EchoAuth-owned.
Its failure order is ambiguous, invalid, revoked, stale, then out of scope. The
evaluator does not call, recreate, repair, reinterpret, broaden, grant, or
bypass EchoAuth authority.

Rollback-required and rollback-available are external descriptive facts only;
availability is not verified, calculated, inspected, or derived. FSM, halt,
failure, recovery, and reset context is opaque and non-decisional. The evaluator
does not execute or orchestrate rollback, mutate FSM state, authorize reset,
perform recovery, restore state, create compensating transactions, or integrate
with runtime systems.

## Test and Validation Evidence

The completed direct tests prove vocabulary parity, non-emission boundaries,
all evaluator branches, collision precedence, authority sub-precedence, all
three undefined combinations, raw enum rejection, contextual non-decision,
correlation preservation, frozen structures, deterministic repetition, and
supplied request/evidence/context non-mutation.

Validation recorded:

* focused tests: 9 passed;
* contract and Authority Clarity tests: 30 passed;
* full suite: 411 passed;
* `git diff --check`: passed;
* prohibited-import and side-effect inspection: passed;
* implementation commit changed only the approved implementation/test files;
* test-evidence commit changed only the approved direct test file.

## Explicit Exclusions and Governance Posture

This acceptance does not authorize rollback or recovery execution, reset
behavior, FSM integration or mutation, EchoAuth runtime integration, market
data, signals, strategy, risk, sizing, simulation, replay/backtesting, brokers,
Robinhood, orders, credentials, deployment, persistence, networking,
execution, another Stage 2 subject, or Stage 3 entry.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized. No
implementation, integration, or neighboring candidate begins automatically.
The next subject requires separate founder selection and a new bounded task
order.
