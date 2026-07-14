# SniperBot Live-Money Readiness Ladder Stage 2 Canonical FSM Contract Definition Review

## Status

Documentation-only / governance-only / proposed-contract-definition-only.

Founder-authorized bounded review of a proposed future **pure, non-executing
SniperBot state-transition contract**.

Current Stage 2 outcome: **HOLD with ESCALATE elements**.

Stage 3 is not entered or authorized.

This review does not authorize implementation, source-code changes, runtime,
schemas, validators, tests, CI, workflows, market data, strategy, signals,
risk, sizing, trade cards, simulation, backtesting, broker or Robinhood
access, orders, credentials, deployment, database authority, production
activation, or execution.

## Purpose and Subject Boundary

The proposed subject is one contract only:

> **A pure FSM transition-decision contract that receives already-determined
> facts and produces a transition decision without evaluating or acting on
> those facts.**

This is preparation for a later founder decision. It is not an implementation
subject approval, evidence acceptance, implementation task order, or a
decision to lift the Stage 2 HOLD.

The construction evidence for this proposal is limited to:

1. `archive/journal/2025-12-25_(17).html` — state enum, typed narrative
   structures, gates, and mixed behavior skeleton;
2. `archive/journal/2025-12-25_(19).html` — gate hierarchy and gate outcomes;
3. `archive/journal/2025-12-25_(20).html` — canonical state names and
   transition narrative; and
4. `archive/journal/2025-12-25_(18).html` — linked trade-card and execution
   lifecycle narrative.

The archive is historical evidence only. It is not a validated contract,
implementation, authority source, or permission to act.

## Declared State Vocabulary

The proposed contract preserves the archive's exact declared state names:

| State | Archive meaning retained for traceability | This review does not authorize |
| --- | --- | --- |
| `PAUSE` | Default / no-trade state. | Observation, classification, setup detection, trade-card creation, alerts, or any runtime behavior. |
| `READY` | Preconditions are said to be satisfied for presenting opportunities. | Gate evaluation, signal generation, or opportunity presentation. |
| `ARMED_MANUAL` | Human-authorized alerts, expressly not execution. | Human-authority determination, alerts, or manual-trade detection. |
| `ARMED_AUTO` | Archive-described permissioned execution window. | Auto-mode, execution, broker communication, or order behavior. |
| `IN_TRADE` | Archive-described active position-management state. | Position detection, management, stop/TP behavior, logging, or execution. |
| `LOCKOUT` | Archive-described safety halt. | Kill-switch implementation, logging, alerting, reset execution, or any runtime halt action. |

`START`, trade-card rejection, auto disablement, and escalation are not
declared archive states. This review does not normalize them into states.

## Proposed Pure Contract Shape

### Separation of Concerns

| Contract element | Proposed role | Explicit exclusion |
| --- | --- | --- |
| State | One declared value from the table above. | It is not a runtime mode, permission, command, or execution state. |
| Transition request | A caller-supplied request to consider a named transition. | It does not cause a transition or carry implicit approval. |
| External facts | Caller-supplied, already-determined facts, including any safety, integrity, context, card, position, or reset facts. | No fact is calculated, verified, refreshed, or accepted by this contract. |
| Authority evidence | A bounded, caller-supplied EchoAuth authority result or explicit absence/invalidity indicator. | The contract does not contact EchoAuth, determine permissions, reinterpret an EchoAuth result, or replace an EchoAuth gate. |
| Transition decision | A side-effect-free result for the requested state only. | It does not notify, log, create a card, call a broker, submit an order, manage a position, or change a system state. |
| Reason code | A structured explanation of the decision. | It is not a durable approval, rejection record, escalation record, or audit event. |

### Proposed Input Contract

The later contract may receive only:

1. `current_state` — one declared state;
2. `requested_state` — one declared state;
3. `transition_request` — an externally named request whose semantics must be
   supplied by a future bounded order;
4. `external_facts` — an immutable collection of already-determined facts;
5. `authority_evidence` — an externally produced bounded authority result,
   including explicit invalid, absent, stale, or out-of-scope states; and
6. `request_reference` — an opaque correlation/reference value only.

The contract must not calculate signals, evaluate strategy, determine market
regime, validate a trade card, calculate risk or sizing, determine permissions,
contact EchoAuth, call a broker, place or manage orders, write logs, or perform
any other external action.

### Proposed Output Contract

The later contract's output is limited to:

1. `current_state`;
2. `requested_state`;
3. `allowed` — `true` or `false` only;
4. `reason_code`; and
5. `required_next_human_or_governance_action`, if applicable.

The output is a proposal result, not a state mutation. An `allowed` result
would not grant implementation, runtime, execution, broker, trading, or Stage
3 authority.

## Unresolved Archive Transitions and Required Founder Decisions

No transition below is resolved by this review.

| Archive transition or condition | Preserved contradiction or gap | Required founder decision before any implementation |
| --- | --- | --- |
| `PAUSE → READY` | Page 20 says all gates pass; Page 19 places the human-authority gate among required gates, while arming begins only from `READY`. | Whether authority evidence is required for this transition, which external fact may represent it, and how the ordering avoids a circular prerequisite. |
| `READY → ARMED_MANUAL` | Archive says human arms manual, but defines no authority-result contract. | Exact authority evidence, validity/currentness, and refusal behavior. |
| `READY → ARMED_AUTO` | Archive mixes human arming, auto gates, strategy, risk, daily trade count, and future execution. | Whether this transition is ever in scope, and every required fact without granting auto-mode or execution. |
| `ARMED_AUTO → READY` versus `ARMED_AUTO → IN_TRADE` | Page 20 lists return to `READY` when a trade is executed and also transition to `IN_TRADE` when the bot executes and confirms a fill. | Exclusive event taxonomy and precedence; this review selects neither branch. |
| `ARMED_MANUAL → IN_TRADE` | Described as optional external manual-trade detection without an interface or provenance rule. | Whether the transition exists, the evidence source, and how it cannot imply broker, order, or manual-execution authority. |
| `IN_TRADE → READY` | Allowed only if "explicitly allowed"; the authorizing actor and conditions are absent. | Whether this transition exists and its exact authority/evidence requirements. |
| `ANY → LOCKOUT` | Safety trigger categories are broad and include data, logging, risk, and kill-switch conditions with undefined fact semantics. | Complete trigger taxonomy, precedence, and treatment of contradictory external facts. |
| `LOCKOUT → PAUSE` | Human reset and gate re-pass are required, but reset authority, evidence, and procedure are undefined. | Reset authority, currentness, revocation, and the exact external facts required. |
| Logging failure | Archive requires lockout while the skeleton attempts to log the lockout event. | Failure-safe reporting behavior and whether a missing log fact may be trusted; no logging implementation is proposed. |
| Rejection and escalation | Card rejection is not a state; escalation and durable denial outcomes are absent from the FSM vocabulary. | Whether they remain external governance outcomes, their record owner, and their relationship to a transition denial. |

## EchoAuth Authority Boundary

EchoAuth owns permission authority. A future FSM contract may consume a
bounded, caller-provided EchoAuth authority result only as input evidence. It
may not reproduce, bypass, infer, refresh, combine, reinterpret, or override
EchoAuth gates or permission decisions.

An absent, stale, ambiguous, revoked, contradictory, or out-of-scope authority
result must not be converted into permission. The future founder decision must
specify the resulting reason code and required human/governance action.

## Archive Contradictions Retained

The following are intentionally retained rather than reconciled:

1. gate ordering can make `PAUSE → READY` circular;
2. `ARMED_AUTO` has competing `READY` and `IN_TRADE` outcomes after execution;
3. `ARMED_MANUAL → IN_TRADE` relies on undefined optional detection;
4. `IN_TRADE → READY` relies on unspecified permission;
5. lockout depends on logging even when logging fails;
6. reset authority and reset procedure are not defined;
7. `MCG`, all-gates, confidence thresholds, session bounds, data provenance,
   and rejection output semantics are undefined; and
8. the archive mixes descriptive narrative, pseudocode, strategy, signal,
   risk, sizing, authority, execution, order, and broker concerns.

## Proposed Future Implementation Scope — Non-Authorizing

No current implementation repository, source path, or test path is identified
by this review. This repository contains no active SniperBot package. Naming a
future source, test, schema, validator, or configuration path here would
invent scope and is therefore deliberately not done.

Before a future implementation task order can name files, the founder must
separately decide the implementation repository, exact input/output contract,
all unresolved transition rules, and the authority-result boundary. That later
task order must explicitly name its allowed files, required tests, validation,
and stop conditions.

At minimum, any later bounded task order must prohibit source changes outside
its named files and prohibit market data, strategy, signals, risk, sizing,
trade-card generation, simulation, backtesting, broker or Robinhood access,
orders, credentials, deployment, database authority, production activation,
execution, EchoAuth runtime changes, and all Stage 3 movement unless each is
separately authorized.

## Current Determination

This review defines preparation for one proposed pure FSM
transition-decision contract only. It does not make the archive deterministic,
complete, executable, validated, implementation-ready, or approved.

Stage 2 remains **HOLD with ESCALATE elements**. Stage 3 remains unentered and
unauthorized. A future founder decision must resolve the preserved questions
before any exact bounded implementation task order can be considered.
