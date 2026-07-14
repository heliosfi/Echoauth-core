# SniperBot Live-Money Readiness Ladder Stage 2 Canonical FSM Re-Gate Founder Decision Record

## Status

Documentation-only / governance-only / founder-decision-record-only.

Founder-authorized record of decisions resolving the identified contract questions for the proposed pure, non-executing SniperBot FSM transition-decision contract.

Current Stage 2 outcome: **HOLD with ESCALATE elements**.

Stage 3 is not entered or authorized.

This record does not authorize implementation, source-code changes, schemas, validators, tests, CI, runtime integration, market data, strategy, signals, risk, sizing, trade cards, simulation, backtesting, broker or Robinhood access, orders, credentials, deployment, database authority, production activation, or execution.

## Decision Authority and Scope

Decision authority: the founder's bounded task order for the **SniperBot FSM Re-Gate Decision Sheet**.

Decision subject: contract-question resolution for the proposed pure, deterministic, side-effect-free, non-executing FSM only.

These decisions resolve neither implementation readiness nor the Stage 2 HOLD. They are not an implementation approval, implementation task order, evidence acceptance for operational readiness, schema-definition task order, or Stage 3 decision.

## Governing Inputs

This record applies the founder decisions to:

1. `sniperbot-live-money-readiness-ladder-stage-2-canonical-fsm-contract-definition-review.md`;
2. `sniperbot-live-money-readiness-ladder-stage-2-authority-resolution-governance-record.md`; and
3. `sniperbot-live-money-readiness-ladder-stage-2-evidence-acceptance-decision-record.md`.

The archive records cited by the contract-definition review remain historical evidence only. This record neither changes nor validates them.

## Founder Decisions

| ID | Founder-selected decision | Contract effect only |
| --- | --- | --- |
| `FSM-01` | `authority-deferred-to-arming` | `PAUSE → READY` must not require authority evidence; authority is considered only at arming. |
| `FSM-02` | `authority-at-arming-only` | Bounded authority evidence is required only before an arming transition. |
| `FSM-03` | `allow-with-valid-authority` | `READY → ARMED_MANUAL` may be considered only with valid authority evidence. It creates no alert, runtime, or implementation permission. |
| `FSM-04` | `retain-but-deny` | `ARMED_AUTO` remains declared vocabulary, but entry into it remains denied pending separate founder authority. |
| `FSM-05` | `in-trade-on-external-confirmed-position` | The requested `IN_TRADE` outcome may be considered only from an externally supplied confirmed-position fact; the FSM may not execute or confirm a fill. |
| `FSM-06` | `exclude-manual-detection` | `ARMED_MANUAL → IN_TRADE` is excluded from the proposed contract. |
| `FSM-07` | `require-in-trade-to-pause` | `IN_TRADE → READY` is not permitted; the archive default `IN_TRADE → PAUSE` is retained. |
| `FSM-08` | `require-position-closed-and-cooldown-facts` | `IN_TRADE → PAUSE` may be considered only when both facts are externally supplied. |
| `FSM-09` | `single-lockout-required-fact` | An externally determined lockout-required fact has precedence over every requested non-lockout transition. |
| `FSM-10` | `external-logging-failure-lockout` | A logging failure may be supplied only as an external lockout-required fact; the FSM performs no log write or recovery action. |
| `FSM-11` | `allow-with-bounded-reset-evidence` | `LOCKOUT → PAUSE` may be considered only with valid bounded reset evidence and required externally supplied reset facts. |
| `FSM-12` | `exact-current-in-scope-non-revoked` | Authority evidence must be exact, current, in scope, and non-revoked. Absent, stale, ambiguous, contradictory, out-of-scope, or revoked evidence is not permission. |
| `FSM-13` | `fsm-output-only` | A denial remains an FSM output only; the FSM creates no durable denial record. |
| `FSM-14` | `required-action-output` | Escalation remains outside the state vocabulary and is represented only by the required next human/governance action output. |
| `FSM-15` | `deny-without-mutation` | An unknown state or undefined transition is denied without state mutation. |
| `FSM-16` | `closed-reason-code-set` | Reason codes must be selected from a future closed, founder-approved set; free-text authority or approval rationale is not permitted. |
| `FSM-17` | `mandatory-opaque-reference` | Every request requires an opaque correlation/reference value; the FSM does not persist, audit, interpret, or generate it. |

## Declared Vocabulary and Contract Separation

The declared state vocabulary remains exactly: `PAUSE`, `READY`, `ARMED_MANUAL`, `ARMED_AUTO`, `IN_TRADE`, and `LOCKOUT`.

No state is added, renamed, normalized, or activated. `START`, trade-card rejection, auto disablement, durable denial, and escalation remain external to the state vocabulary.

The future pure contract remains limited to caller-supplied current state, requested state, transition request, already-determined external facts, bounded authority evidence, and mandatory opaque reference. Its output remains limited to current state, requested state, allowed/denied, closed reason code, and required next human/governance action.

No input or output grants permission, causes state mutation, evaluates a fact, or performs an external action.

## EchoAuth Authority Boundary

EchoAuth remains the sole owner of permission authority. The FSM may consume a bounded EchoAuth authority result as input only. It may not create, reinterpret, replace, refresh, combine, bypass, or override EchoAuth authority or gates.

The selections in `FSM-01`, `FSM-02`, `FSM-03`, `FSM-11`, and `FSM-12` govern only when and how a future pure contract may consider caller-provided authority evidence. They do not authorize EchoAuth contact, a new EchoAuth interface, or runtime integration.

## Boundaries Preserved

The following remain prohibited and unaddressed by this record: market data, strategy, signals, risk, sizing, trade-card generation, simulation, backtesting, broker or Robinhood access, order creation or routing, credentials, deployment, database authority, production activation, execution, autonomous action, schemas, validators, tests, CI, workflows, runtime integration, and EchoAuth runtime changes.

`ARMED_AUTO` is retained solely as declared vocabulary. Its entry remains denied and does not create auto-mode, execution, broker, order, or trading capability.

## Remaining Blockers and Next Founder Decision

The resolved contract questions do not satisfy the remaining Stage 2 HOLD conditions: no implementation task order exists; no operational, implementation, runtime, broker, or execution-prohibition evidence has been accepted for any implementation scope; and no code, schema, test, or runtime work is approved.

No next action is automatically authorized. If the founder chooses to continue, the exact next founder decision is whether to issue a separate bounded task order limited to defining a future FSM schema or interface proposal, with exact allowed files, validation, stop conditions, and continued non-execution boundaries. That decision would not itself authorize implementation.

## Current Determination

This durable record resolves the named founder contract decisions only. Stage 2 remains **HOLD with ESCALATE elements**. Stage 3 remains unentered and unauthorized.
