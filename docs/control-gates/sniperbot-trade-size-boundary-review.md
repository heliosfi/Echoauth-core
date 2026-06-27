# SniperBot Trade-Size Boundary Review

## Locked Baseline

Repo: `heliosfi/Echoauth-core`

Branch: `main`

Starting commit: `68af9876fa157ec82abe675324b5bf8ea9a1d8ec`

State: clean and synchronized with `origin/main`

## Status

DOCUMENTATION ONLY -- GOVERNANCE ONLY -- RISK-BOUNDARY-ONLY --
TRADE-SIZE-PLANNING-ONLY -- NON-RUNTIME -- NON-EXECUTION -- NOT
IMPLEMENTED -- NOT AN IMPLEMENTATION APPROVAL

This file is auditor-facing and founder-facing. It is documentation-only,
governance-only, risk-boundary-only, trade-size-planning-only, non-runtime,
and non-execution.

This review defines the SniperBot trade-size boundary required before any
future trading-adjacent readiness review can be considered under a separate
bounded task order.

This review defines trade-size as a governance risk boundary only. It is not
trading approval, order authority, position-sizing logic, broker permission,
Robinhood permission, strategy authority, automation authority, command
authority, execution readiness, or execution capability.

This review does not create position-sizing runtime, trade-size runtime,
broker behavior, Robinhood behavior, SniperBot behavior, order-routing
behavior, paper-trading behavior, simulation behavior, live-trading
behavior, audit runtime, traceability runtime, rollback runtime,
autonomous-action runtime, child-safety runtime changes, EchoAuth runtime
changes, NI-AI runtime changes, founder approval runtime, command execution,
or execution capability.

No trade-size lane, position-sizing lane, broker lane, Robinhood lane,
SniperBot lane, order-routing lane, automation lane, simulation lane,
paper-trading lane, or live-trading lane is selected as
implementation-ready by this review.

## Scope

This review is:

* documentation-only
* governance-only
* risk-boundary-only
* trade-size-planning-only
* non-runtime
* non-execution
* no runtime behavior
* no implementation
* no execution capability

This review may discuss future trade-size evidence requirements only. It
must not define executable position-sizing controls, executable trade-size
controls, runtime state machines, automation loops, command syntax, API
calls, broker workflows, Robinhood workflows, order workflows, trading
logic, strategy logic, CUDA trading behavior, audit runtime, traceability
runtime, rollback runtime, autonomous-action runtime, founder approval
runtime, position-sizing runtime, trade-size runtime, or execution behavior.

This review preserves no-action posture until a future separately approved
boundary exists. No future task may treat this review as an implementation
plan, runtime specification, position-sizing runbook, trade-size runbook,
broker workflow, Robinhood workflow, order workflow, automation workflow,
command workflow, or execution workflow.

## Purpose

Trade-size is listed as an unresolved future readiness boundary in SniperBot
live-trading readiness governance.

The capital-risk review also references maximum trade-size boundary needs.

Trade-size must be bounded, documented, and reviewed before any future
trading-adjacent readiness can be considered.

Trade-size language must not be treated as trading approval, broker
approval, Robinhood approval, order-routing approval, strategy approval,
automation approval, command approval, implementation approval, or execution
approval.

Trade-size in this review is governance posture, future evidence planning,
and risk-boundary review only. It is non-runtime and non-execution.

Trade-size is not position-sizing logic, trading approval, implementation
approval, broker permission, Robinhood permission, order authority, strategy
authority, automation authority, command authority, execution readiness,
execution capability, position-sizing runtime, or trade-size runtime.

This lane records what must be proven later, not what is authorized now.

Trade-size boundary comes before execution.

"We don't move until system move."

Documentation is not execution.

## Relationship to Completed Lanes

The following SniperBot readiness boundary lanes are complete, indexed,
verified, and parked as documentation-only / governance-only / non-execution
boundary reviews:

* Broker/Trading Boundary Review
* SniperBot Live Trading Readiness Boundary Review
* SniperBot Capital Risk Limit Boundary Review
* SniperBot Max Loss / Daily Stop-Loss Boundary Review
* SniperBot Paper-Trading / Simulation Boundary Review
* SniperBot Kill-Switch Boundary Review
* SniperBot Human Confirmation Boundary Review
* SniperBot Audit Log / Trade Traceability Boundary Review
* SniperBot Rollback / No-Action Fallback Boundary Review
* SniperBot No-Autonomous-Action Boundary Review
* SniperBot No Child-Safety Governance Crossover Boundary Review
* SniperBot Founder Approval Boundary Review

Those completed lanes do not create live trading, paper trading, simulation,
broker access, Robinhood access, SniperBot behavior, CUDA trading code,
order routing, trade automation, position-sizing runtime, trade-size
runtime, macro/hotkey behavior, audit runtime, traceability runtime,
rollback runtime, autonomous-action runtime, child-safety runtime changes,
EchoAuth runtime changes, NI-AI runtime changes, founder approval runtime,
command execution, or execution capability.

This review builds only on their trade-size and risk-boundary references. It
does not create a bridge from trade-size language to broker, Robinhood,
SniperBot, order-routing, trade-automation, runtime, autonomous action,
position sizing, trade sizing, or execution behavior.

## Required Future Trade-Size Categories

Before any future trading-adjacent readiness review can be considered under
a separate bounded task order, a separate future review must define what
trade-size posture and future evidence would need to be recorded, reviewed,
and traceable for at least these categories:

* maximum trade-size proposal
* minimum trade-size / no-trade floor proposal
* account-size relationship proposal
* capital-risk relationship proposal
* max-loss / daily stop-loss relationship proposal
* human-confirmation relationship proposal
* audit-log / trade-traceability relationship proposal
* rollback / no-action fallback relationship proposal
* no-autonomous-action relationship proposal
* founder-approval relationship proposal
* asset-class separation for options, stock, and crypto, without authorizing
  any asset class
* separate approval for paper-trading or simulation review, if ever
  considered later
* separate approval for live-trading review, if ever considered later
* human review before any future movement

Listing those categories does not create trade-size runtime,
position-sizing runtime, schemas, events, records, databases, command paths,
runtime state machines, broker checks, Robinhood checks, order intents,
strategy approvals, trade rationale, governance approvals, automation,
command execution, or execution capability.

Each category would require separate founder-selected review before any
implementation could be considered.

## Required Future Evidence

Before any later trade-size mechanism could be considered, a separate future
task would need to propose and review at least the following evidence:

* trade-size taxonomy proposal
* account-capital relationship proposal
* maximum exposure proposal
* per-trade cap proposal
* per-day cap relationship proposal
* capital-risk boundary relationship proposal
* max-loss / daily stop-loss boundary relationship proposal
* human-confirmation dependency proposal
* founder-approval dependency proposal
* audit-log relationship proposal
* rollback/no-action fallback relationship proposal
* no-autonomous-action relationship proposal
* failure-mode review
* privacy/security boundary proposal
* separation from broker/order execution paths
* separation from runtime automation paths
* separation from EchoAuth / NI-AI child-safety runtime paths

These future evidence items are planning topics only. They do not create
schemas, validators, tests, CI, trade-size runtime, position-sizing runtime,
runtime sizing logic, event-bus behavior, monitoring behavior, broker
behavior, Robinhood behavior, order-routing behavior, strategy behavior,
trade automation, audit runtime, traceability runtime, rollback runtime,
autonomous-action runtime, child-safety runtime changes, EchoAuth runtime
changes, NI-AI runtime changes, founder approval runtime, command execution,
or execution capability.

## Boundary Rules

The following trade-size boundary rules remain locked:

* Trade-size review must not become position-sizing logic.
* Trade-size documentation must not become order authority.
* Trade-size limits must not become broker permission.
* Trade-size limits must not become Robinhood permission.
* Trade-size discussion must not become trading approval.
* Trade-size review must not authorize options, stock, crypto, paper
  trading, simulation, or live trading.
* Trade-size review must not create runtime enforcement.
* Trade-size review must not create automation.
* Trade-size review must not create command execution.
* Ambiguous trade-size authority resolves to no-action, not assumed
  approval.
* Incomplete trade-size evidence resolves to no-action, not partial
  execution.
* "We don't move until system move" must remain the governing posture.
* Trade-size language is not readiness approval.
* Trade-size planning is not implementation approval.
* Trade-size planning is not broker permission.
* Trade-size planning is not Robinhood permission.
* Trade-size planning is not order authority.
* Trade-size planning is not strategy authority.
* Trade-size planning is not automation authority.
* Trade-size planning is not command authority.
* Trade-size planning is not execution authority.
* Trade-size planning is not position-sizing runtime.
* Documentation is not execution.
* PASS is not permission.
* Silence is not consent.
* Ambiguity remains non-permission.
* EchoAuth governance and Trading/Robinhood execution remain separate
  domains.
* SniperBot cannot inherit authority from EchoAuth governance.
* SniperBot cannot inherit authority from NI-AI governance.

This review does not add, change, rank, resolve, reinterpret, or implement
those rules.

## Explicit Non-Authorization

This file does not authorize:

* live trading
* paper trading
* simulation
* broker access
* Robinhood access
* SniperBot behavior
* CUDA trading code
* order routing
* trade automation
* position-sizing runtime
* trade-size runtime
* macro/hotkey behavior
* audit runtime
* traceability runtime
* rollback runtime
* autonomous-action runtime
* child-safety runtime changes
* EchoAuth runtime changes
* NI-AI runtime changes
* founder approval runtime
* command execution
* execution capability

No live trading is authorized by this review.

No paper trading is created by this review.

No simulation is created by this review.

No broker access is created by this review.

No Robinhood access or alignment is created by this review.

No SniperBot behavior is created by this review.

No CUDA trading code is created by this review.

No order routing is created by this review.

No order placement is created by this review.

No order intent is created by this review.

No strategy authority is created by this review.

No trade automation is created by this review.

No position-sizing runtime is created by this review.

No trade-size runtime is created by this review.

No macro/hotkey behavior is created by this review.

No audit runtime is created by this review.

No traceability runtime is created by this review.

No rollback runtime is created by this review.

No autonomous-action runtime is created by this review.

No child-safety runtime changes are created by this review.

No EchoAuth runtime changes are created by this review.

No NI-AI runtime changes are created by this review.

No founder approval runtime is created by this review.

No runtime behavior is created by this review.

No command execution is created by this review.

No execution capability is created by this review.

No schema is created by this review.

No trade-size taxonomy is created by this review.

No account-capital relationship is created by this review.

No maximum exposure calculation is created by this review.

No per-trade cap is created by this review.

No per-day cap is created by this review.

No asset-class authorization is created by this review.

No options authorization is created by this review.

No stock authorization is created by this review.

No crypto authorization is created by this review.

No human-confirmation dependency is created by this review.

No founder-approval dependency is created by this review.

No audit-log runtime relationship is created by this review.

No rollback/no-action fallback runtime relationship is created by this
review.

No no-autonomous-action runtime relationship is created by this review.

No failure-mode implementation is created by this review.

No privacy/security implementation is created by this review.

No broker/order execution path is created by this review.

No runtime automation path is created by this review.

No EchoAuth / NI-AI child-safety runtime path is modified by this review.

This review does not create implementation, schema, validator, test, CI,
runtime, enforcement, event-bus, register mutation, blocker resolution,
monitoring service behavior, monitoring agent behavior, broker/trading
behavior, Robinhood execution alignment, autonomous action, command
execution, or execution capability.

## Founder / Risk Boundary

Founder approval may support governance selection, bounded review, and
documentation-only task authorization.

Founder approval in this context does not approve trade size, position
sizing, trading, broker access, Robinhood access, order routing, automation,
runtime behavior, command execution, or execution capability.

Trade-size language may support future risk review only. It is not a trade
instruction, order instruction, position-size instruction, strategy
instruction, broker instruction, Robinhood instruction, runtime instruction,
command instruction, or execution instruction.

EchoAuth does not size trades.

EchoAuth does not approve trades.

EchoAuth does not generate executable orders.

EchoAuth does not connect brokers.

EchoAuth does not authorize broker access.

EchoAuth does not authorize Robinhood access.

EchoAuth does not create trading authority.

EchoAuth does not execute trades.

NI-AI does not size trades.

NI-AI does not approve trades.

NI-AI does not generate executable orders.

NI-AI does not connect brokers.

NI-AI does not authorize broker access.

NI-AI does not authorize Robinhood access.

NI-AI does not create trading authority.

NI-AI does not execute trades.

Trade-size language, founder approval language, EchoAuth / NI-AI output,
classification, review, refusal posture, evidence, PASS state, silence,
ambiguity handling, monitoring output, audit output, checkpointing, parked
status, or governance status must not be treated as trading approval, broker
access authority, Robinhood authority, order authority, position-sizing
authority, strategy authority, autonomous-action authority, command
authority, or execution authority.

## Non-Authorization

This review does not authorize:

* implementation
* schema creation
* schema modification
* trade-size taxonomy creation
* account-capital relationship implementation
* maximum exposure implementation
* per-trade cap implementation
* per-day cap implementation
* validator work
* tests
* CI
* runtime behavior
* enforcement behavior
* approval authority
* permission
* blocker resolution
* register mutation
* event-bus behavior
* monitoring service behavior
* monitoring agent behavior
* service behavior
* agent behavior
* trade-size implementation
* trade-size runtime
* position-sizing implementation
* position-sizing runtime
* child-safety runtime changes
* EchoAuth runtime changes
* NI-AI runtime changes
* founder approval runtime
* human-confirmation dependency implementation
* founder-approval dependency implementation
* audit-log relationship implementation
* rollback/no-action fallback relationship implementation
* no-autonomous-action relationship implementation
* failure-mode implementation
* privacy/security implementation
* broker/order execution path
* runtime automation path
* capital allocation
* capital approval
* trading-account connection
* paper account
* simulated account
* paper trading
* simulation
* mock broker
* broker API logic
* broker connection
* broker access
* broker/trading behavior
* Robinhood connection
* Robinhood login
* Robinhood access
* Robinhood alignment
* Robinhood scraping
* Robinhood automation
* Robinhood execution alignment
* market-data feed
* recorded-data feed
* backtest logic
* strategy engine
* trading strategy logic
* trading permission
* trading execution
* live trading
* order-routing logic
* order-routing path
* order placement
* order confirmation
* order intent generation
* trade decision generation
* trade automation
* options execution
* stock execution
* crypto execution
* options authorization
* stock authorization
* crypto authorization
* CUDA trading code
* trading-bot behavior
* SniperBot runtime behavior
* macro/hotkey automation
* autonomous action
* autonomous trading behavior
* audit runtime
* traceability runtime
* rollback runtime
* autonomous-action runtime
* command execution
* command-execution capability
* execution capability
* trade-size readiness
* position-sizing readiness
* simulation readiness
* paper-trading readiness
* broker readiness
* trading readiness
* live-trading readiness
* execution readiness
* automation readiness
* an approval path
* an unblock path
* implied execution permission

## Separation Wall

Trade-size planning remains separate from position-sizing runtime.

Trade-size language remains separate from trading approval.

Founder approval planning remains separate from runtime approval systems.

EchoAuth governance remains separate from Trading/Robinhood execution.

NI-AI governance remains separate from Trading/Robinhood execution.

Child-safety governance remains separate from trading governance.

SniperBot readiness language remains separate from SniperBot behavior.

Documentation remains separate from implementation.

Boundary review remains separate from runtime enforcement.

Risk-boundary planning remains separate from runtime behavior.

This review does not bridge trade-size language, founder approval language,
EchoAuth governance, NI-AI governance, child-safety governance, control
gates, monitoring paths, broker paths, trading paths, Robinhood paths,
macro/hotkey paths, SniperBot paths, CUDA paths, trading-bot paths,
order-routing paths, audit-log paths, traceability paths, rollback paths,
fallback paths, autonomous-action paths, position-sizing paths, trade-size
paths, command paths, or execution paths.

## Future Movement Boundary

Any future trade-size review, position-sizing review, paper-trading,
simulation, broker, Robinhood, order-routing, CUDA, audit-runtime,
traceability-runtime, rollback-runtime, autonomous-action-runtime, founder
approval runtime, position-sizing runtime, trade-size runtime, child-safety
runtime, EchoAuth runtime, NI-AI runtime, or live-trading movement must be
separate, explicit, bounded, and selected by the founder before any
implementation discussion can begin.

Any future trade-size mechanism, position-sizing mechanism, trade-size
taxonomy, account-capital relationship, maximum exposure proposal,
per-trade cap proposal, per-day cap relationship, capital-risk boundary
relationship, max-loss / daily stop-loss boundary relationship,
human-confirmation dependency, founder-approval dependency, audit-log
relationship, rollback/no-action fallback relationship, no-autonomous-action
relationship, failure-mode review, privacy/security boundary proposal,
paper-trading, simulation, market-data, backtest, strategy, broker,
Robinhood, SniperBot, CUDA, trading-bot, order-routing, macro/hotkey,
autonomous-action, command-execution, trade-size runtime, position-sizing
runtime, founder approval runtime, child-safety runtime, EchoAuth runtime,
NI-AI runtime, or execution-related work requires a separate explicit
founder-selected bounded task order and additional safety, risk, broker,
execution, and trade-size boundary review before implementation.

No future task may treat this trade-size boundary review as approval to
create trade-size runtime, create position-sizing runtime, create automation,
create order intent, create order routing, create broker interaction, create
Robinhood interaction, create paper trading, create simulation, create a
mock broker, connect a broker, connect Robinhood, create market-data feeds,
create backtest logic, create strategy logic, create SniperBot behavior,
create CUDA trading behavior, create macro or hotkey behavior, generate
orders, route orders, place orders, approve trades, size trades, execute,
connect to brokers, log in to Robinhood, align with Robinhood execution,
create command execution, or create execution capability.

## Final Status

Boundary defined.

Trade-size planning documented.

Risk boundary documented.

Implementation not authorized.

Runtime not authorized.

Execution not authorized.

README/index update not authorized.

Staging/commit/push not authorized.

Awaiting separate explicit approval for any future index update, staging,
commit, push, implementation, or next lane.
