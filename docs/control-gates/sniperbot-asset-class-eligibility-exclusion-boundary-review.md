# SniperBot Asset-Class Eligibility / Exclusion Boundary Review

## Locked Baseline

Repo: `heliosfi/Echoauth-core`

Branch: `main`

Starting commit: `13ca154c9308ab98e07feb83656b7c337bdf66b9`

State: clean and synchronized with `origin/main`

## Status

DOCUMENTATION ONLY -- GOVERNANCE ONLY --
ELIGIBILITY-EXCLUSION-BOUNDARY-ONLY --
ASSET-CLASS-READINESS-PLANNING-ONLY -- NON-RUNTIME -- NON-EXECUTION --
NOT IMPLEMENTED -- NOT AN IMPLEMENTATION APPROVAL

This file is auditor-facing and founder-facing. It is documentation-only,
governance-only, eligibility-exclusion-boundary-only,
asset-class-readiness-planning-only, non-runtime, and non-execution.

This review defines SniperBot asset-class eligibility and exclusion as
governance boundaries only. Eligibility is not asset approval. Exclusion is
not routing logic. Eligibility/exclusion planning is not asset selection,
trading approval, strategy approval, broker permission, Robinhood
permission, order authority, automation authority, command authority,
execution readiness, or execution capability.

Eligibility/exclusion boundary review is only documentation-only,
governance-only, eligibility-exclusion-boundary-only,
asset-class-readiness-planning-only, non-runtime, and non-execution.

Eligibility/exclusion must not be treated as eligibility runtime, exclusion
runtime, asset-selection logic, asset approval, strategy logic, strategy
runtime, trading logic, broker logic, Robinhood logic, order-routing logic,
CUDA trading behavior, macro/hotkey behavior, audit runtime, traceability
runtime, rollback runtime, autonomous-action runtime, command execution, or
execution capability.

This review does not create asset-class runtime, eligibility runtime,
exclusion runtime, asset-selection logic, position-sizing runtime,
trade-size runtime, broker behavior, Robinhood behavior, SniperBot behavior,
order-routing behavior, paper-trading behavior, simulation behavior,
live-trading behavior, strategy logic, strategy runtime, audit runtime,
traceability runtime, rollback runtime, autonomous-action runtime,
child-safety runtime changes, EchoAuth runtime changes, NI-AI runtime
changes, founder approval runtime, command execution, or execution
capability.

No options lane, stock lane, crypto lane, eligibility lane, exclusion lane,
broker lane, Robinhood lane, SniperBot lane, order-routing lane, automation
lane, simulation lane, paper-trading lane, or live-trading lane is selected
as implementation-ready by this review.

## Scope

This review is:

* documentation-only
* governance-only
* eligibility-exclusion-boundary-only
* asset-class-readiness-planning-only
* non-runtime
* non-execution
* no runtime behavior
* no implementation
* no execution capability

This review may discuss future asset-class eligibility and exclusion
evidence requirements only. It must not define executable eligibility
controls, executable exclusion controls, executable asset-selection
controls, runtime state machines, automation loops, command syntax, API
calls, broker workflows, Robinhood workflows, order workflows, trading
logic, strategy logic, strategy runtime, CUDA trading behavior, audit
runtime, traceability runtime, rollback runtime, autonomous-action runtime,
founder approval runtime, position-sizing runtime, trade-size runtime,
asset-class runtime, eligibility runtime, exclusion runtime, or execution
behavior.

This review preserves no-action posture until a future separately approved
boundary exists. No future task may treat this review as an implementation
plan, runtime specification, eligibility runbook, exclusion runbook,
asset-selection runbook, asset-class runbook, broker workflow, Robinhood
workflow, order workflow, automation workflow, command workflow, strategy
workflow, or execution workflow.

## Purpose

The SniperBot Asset-Class Risk Separation Boundary Review parked future
`asset-class eligibility boundary proposal` and `asset-class exclusion
boundary proposal` work.

SniperBot Live Trading Readiness still lists unresolved options-risk,
stock-risk, crypto-risk, broker-access, Robinhood-access, order-routing, and
latency / CUDA boundaries.

This lane defines how future asset classes may be reviewed as eligible,
excluded, deferred, or no-action without selecting or approving any asset
class.

Eligibility must not mean approval.

Exclusion must not mean routing logic.

Asset-class eligibility/exclusion must not authorize options, stock, crypto,
paper trading, simulation, live trading, broker access, Robinhood access,
order routing, strategy logic, strategy runtime, automation,
implementation, command execution, or execution capability.

This lane records what must be proven later, not what is authorized now.

Eligibility/exclusion boundary comes before execution.

"We don't move until system move." remains the governing posture.

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
* SniperBot Trade-Size Boundary Review
* SniperBot Asset-Class Risk Separation Boundary Review

Those completed lanes do not create live trading, paper trading, simulation,
broker access, Robinhood access, SniperBot behavior, CUDA trading code,
order routing, trade automation, position-sizing runtime, trade-size
runtime, asset-class runtime, eligibility runtime, exclusion runtime,
asset-selection logic, strategy logic, strategy runtime, macro/hotkey
behavior, audit runtime, traceability runtime, rollback runtime,
autonomous-action runtime, child-safety runtime changes, EchoAuth runtime
changes, NI-AI runtime changes, founder approval runtime, command execution,
or execution capability.

This review builds only on their asset-class, trade-size, risk-boundary, and
separation references. It does not create a bridge from eligibility language
or exclusion language to broker, Robinhood, SniperBot, order-routing,
trade-automation, runtime, autonomous action, position sizing, trade sizing,
asset selection, strategy, or execution behavior.

## Required Future Eligibility / Exclusion Categories

Before any future asset-class-specific readiness review can be considered
under a separate bounded task order, a separate future review must define
what eligibility/exclusion posture and future evidence would need to be
recorded, reviewed, and traceable for at least these categories:

* asset-class eligibility taxonomy proposal
* asset-class exclusion taxonomy proposal
* options eligibility / exclusion proposal
* stock eligibility / exclusion proposal
* crypto eligibility / exclusion proposal
* eligibility evidence requirements
* exclusion evidence requirements
* deferred-review category proposal
* no-action category proposal
* asset-class-specific risk evidence relationship proposal
* asset-class-specific trade-size relationship proposal
* asset-class-specific max-loss / daily stop-loss relationship proposal
* asset-class-specific human-confirmation relationship proposal
* asset-class-specific founder-approval relationship proposal
* asset-class-specific audit-log / trade-traceability relationship proposal
* asset-class-specific rollback / no-action fallback relationship proposal
* asset-class-specific no-autonomous-action relationship proposal
* separate approval for any future options review
* separate approval for any future stock review
* separate approval for any future crypto review
* separate approval for paper-trading or simulation review, if ever
  considered later
* separate approval for live-trading review, if ever considered later
* human review before any future movement

Listing those categories does not create eligibility runtime, exclusion
runtime, asset-class runtime, asset-selection logic, position-sizing
runtime, trade-size runtime, schemas, events, records, databases, command
paths, runtime state machines, broker checks, Robinhood checks, order
intents, strategy approvals, trade rationale, governance approvals,
automation, command execution, or execution capability.

Each category would require separate founder-selected review before any
implementation could be considered.

## Required Future Evidence

Before any later eligibility or exclusion mechanism could be considered, a
separate future task would need to propose and review at least the following
evidence:

* asset-class eligibility taxonomy
* asset-class exclusion taxonomy
* eligibility evidence proposal
* exclusion evidence proposal
* options eligibility evidence proposal
* options exclusion evidence proposal
* stock eligibility evidence proposal
* stock exclusion evidence proposal
* crypto eligibility evidence proposal
* crypto exclusion evidence proposal
* asset-class deferral evidence proposal
* asset-class no-action evidence proposal
* account-capital relationship proposal
* maximum exposure relationship proposal
* per-trade cap relationship proposal
* per-day cap relationship proposal
* capital-risk boundary relationship proposal
* trade-size boundary relationship proposal
* asset-class risk separation relationship proposal
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
schemas, validators, tests, CI, eligibility runtime, exclusion runtime,
asset-class runtime, asset-selection logic, trade-size runtime,
position-sizing runtime, runtime sizing logic, event-bus behavior,
monitoring behavior, broker behavior, Robinhood behavior, order-routing
behavior, strategy behavior, strategy runtime, trade automation, audit
runtime, traceability runtime, rollback runtime, autonomous-action runtime,
child-safety runtime changes, EchoAuth runtime changes, NI-AI runtime
changes, founder approval runtime, command execution, or execution
capability.

## Boundary Rules

The following eligibility/exclusion boundary rules remain locked:

* Eligibility must not become asset approval.
* Exclusion must not become routing logic.
* Asset-class eligibility must not become asset selection.
* Asset-class exclusion must not become trading logic.
* Options eligibility must not become options trading approval.
* Stock eligibility must not become stock trading approval.
* Crypto eligibility must not become crypto trading approval.
* Asset-class documentation must not become order authority.
* Eligibility boundaries must not become broker permission.
* Exclusion boundaries must not become Robinhood permission.
* Eligibility/exclusion review must not authorize paper trading, simulation,
  or live trading.
* Eligibility/exclusion review must not create runtime enforcement.
* Eligibility/exclusion review must not create strategy logic.
* Eligibility/exclusion review must not create strategy runtime.
* Eligibility/exclusion review must not create automation.
* Eligibility/exclusion review must not create command execution.
* Ambiguous eligibility authority resolves to no-action, not assumed
  approval.
* Ambiguous exclusion authority resolves to no-action, not assumed approval.
* Incomplete eligibility evidence resolves to no-action, not partial
  execution.
* Incomplete exclusion evidence resolves to no-action, not partial
  execution.
* "We don't move until system move." must remain the governing posture.
* Eligibility language is not readiness approval.
* Exclusion language is not readiness approval.
* Eligibility planning is not implementation approval.
* Exclusion planning is not implementation approval.
* Eligibility planning is not broker permission.
* Exclusion planning is not Robinhood permission.
* Eligibility/exclusion planning is not order authority.
* Eligibility/exclusion planning is not strategy authority.
* Eligibility/exclusion planning is not automation authority.
* Eligibility/exclusion planning is not command authority.
* Eligibility/exclusion planning is not execution authority.
* Eligibility/exclusion planning is not eligibility runtime.
* Eligibility/exclusion planning is not exclusion runtime.
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

* options trading
* stock trading
* crypto trading
* asset selection
* asset approval
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
* asset-class runtime
* eligibility runtime
* exclusion runtime
* asset-selection logic
* strategy logic
* strategy runtime
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

No options trading is authorized by this review.

No stock trading is authorized by this review.

No crypto trading is authorized by this review.

No asset selection is authorized by this review.

No asset approval is created by this review.

No live trading is authorized by this review.

No paper trading is created by this review.

No simulation is created by this review.

No broker access is created by this review.

No Robinhood access or alignment is created by this review.

No SniperBot behavior is created by this review.

No CUDA trading code is created by this review.

No order routing is created by this review.

No trade automation is created by this review.

No position-sizing runtime is created by this review.

No trade-size runtime is created by this review.

No asset-class runtime is created by this review.

No eligibility runtime is created by this review.

No exclusion runtime is created by this review.

No asset-selection logic is created by this review.

No strategy logic is created by this review.

No strategy runtime is created by this review.

No macro/hotkey behavior is created by this review.

No audit runtime is created by this review.

No traceability runtime is created by this review.

No rollback runtime is created by this review.

No autonomous-action runtime is created by this review.

No child-safety runtime changes are created by this review.

No EchoAuth runtime changes are created by this review.

No NI-AI runtime changes are created by this review.

No founder approval runtime is created by this review.

No command execution is created by this review.

No execution capability is created by this review.

## NI-AI Boundary

NI-AI may support coherence, review, refusal, and risk framing.

NI-AI does not approve eligibility.

NI-AI does not approve exclusion.

NI-AI does not select asset classes.

NI-AI does not approve trades.

NI-AI does not size trades.

NI-AI does not place trades.

NI-AI does not generate executable orders.

NI-AI does not connect brokers.

NI-AI does not authorize broker access.

NI-AI does not authorize Robinhood access.

NI-AI does not create trading authority.

NI-AI does not execute trades.

Eligibility language, exclusion language, asset-class language, founder
approval language, EchoAuth / NI-AI output, classification, review, refusal
posture, evidence, PASS state, silence, ambiguity handling, monitoring
output, audit output, checkpointing, parked status, or governance status
must not be treated as trading approval, asset-class approval, asset
eligibility approval, broker access authority, Robinhood authority, order
authority, strategy authority, autonomous-action authority, command
authority, or execution authority.

## Non-Authorization

This review does not authorize:

* implementation
* schema creation
* schema modification
* asset-class eligibility taxonomy creation
* asset-class exclusion taxonomy creation
* eligibility evidence implementation
* exclusion evidence implementation
* options eligibility implementation
* options exclusion implementation
* stock eligibility implementation
* stock exclusion implementation
* crypto eligibility implementation
* crypto exclusion implementation
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
* asset-class implementation
* asset-class runtime
* eligibility implementation
* eligibility runtime
* exclusion implementation
* exclusion runtime
* asset-selection logic
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
* strategy runtime
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
* eligibility readiness
* exclusion readiness
* asset-class readiness
* options readiness
* stock readiness
* crypto readiness
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

Eligibility planning remains separate from asset approval.

Exclusion planning remains separate from routing logic.

Asset-class eligibility remains separate from asset selection.

Asset-class exclusion remains separate from trading logic.

Asset-class language remains separate from trading approval.

Trade-size planning remains separate from position-sizing runtime.

Founder approval planning remains separate from runtime approval systems.

EchoAuth governance remains separate from Trading/Robinhood execution.

NI-AI governance remains separate from Trading/Robinhood execution.

Child-safety governance remains separate from trading governance.

SniperBot readiness language remains separate from SniperBot behavior.

Documentation remains separate from implementation.

Boundary review remains separate from runtime enforcement.

Eligibility/exclusion planning remains separate from runtime behavior.

This review does not bridge eligibility language, exclusion language,
asset-class language, trade-size language, founder approval language,
EchoAuth governance, NI-AI governance, child-safety governance, control
gates, monitoring paths, broker paths, trading paths, Robinhood paths,
macro/hotkey paths, SniperBot paths, CUDA paths, trading-bot paths,
order-routing paths, audit-log paths, traceability paths, rollback paths,
fallback paths, autonomous-action paths, position-sizing paths, trade-size
paths, asset-class paths, eligibility paths, exclusion paths, strategy
paths, command paths, or execution paths.

## Future Movement Boundary

Any future eligibility review, exclusion review, asset-class review,
options-risk review, stock-risk review, crypto-risk review, trade-size
review, position-sizing review, paper-trading, simulation, broker, Robinhood,
order-routing, CUDA, audit-runtime, traceability-runtime, rollback-runtime,
autonomous-action-runtime, founder approval runtime, position-sizing runtime,
trade-size runtime, asset-class runtime, eligibility runtime, exclusion
runtime, child-safety runtime, EchoAuth runtime, NI-AI runtime, strategy,
strategy runtime, or live-trading movement must be separate, explicit,
bounded, and selected by the founder before any implementation discussion
can begin.

Any future eligibility mechanism, exclusion mechanism, asset-class
mechanism, asset-selection mechanism, eligibility taxonomy, exclusion
taxonomy, options eligibility evidence, options exclusion evidence, stock
eligibility evidence, stock exclusion evidence, crypto eligibility evidence,
crypto exclusion evidence, asset-class deferral evidence, asset-class
no-action evidence, account-capital relationship, maximum exposure
relationship, per-trade cap relationship, per-day cap relationship,
capital-risk boundary relationship, trade-size boundary relationship,
asset-class risk separation relationship, max-loss / daily stop-loss
boundary relationship, human-confirmation dependency, founder-approval
dependency, audit-log relationship, rollback/no-action fallback
relationship, no-autonomous-action relationship, failure-mode review,
privacy/security boundary proposal, paper-trading, simulation, market-data,
backtest, strategy, strategy runtime, broker, Robinhood, SniperBot, CUDA,
trading-bot, order-routing, macro/hotkey, autonomous-action,
command-execution, asset-class runtime, eligibility runtime, exclusion
runtime, trade-size runtime, position-sizing runtime, founder approval
runtime, child-safety runtime, EchoAuth runtime, NI-AI runtime, or
execution-related work requires a separate explicit founder-selected bounded
task order and additional safety, risk, broker, execution, eligibility, and
exclusion boundary review before implementation.

No future task may treat this asset-class eligibility / exclusion boundary
review as approval to create eligibility runtime, create exclusion runtime,
create asset-class runtime, create asset-selection logic, create trade-size
runtime, create position-sizing runtime, create automation, create strategy
logic, create strategy runtime, create order intent, create order routing,
create broker interaction, create Robinhood interaction, create paper
trading, create simulation, create a mock broker, connect a broker, connect
Robinhood, create market-data feeds, create backtest logic, create SniperBot
behavior, create CUDA trading behavior, create macro or hotkey behavior,
generate orders, route orders, place orders, approve trades, size trades,
select assets, approve eligibility, approve exclusion, execute, connect to
brokers, log in to Robinhood, align with Robinhood execution, create command
execution, or create execution capability.

## Final Status

Boundary defined.

Asset-class eligibility planning documented.

Asset-class exclusion planning documented.

Eligibility/exclusion boundary documented.

Implementation not authorized.

Runtime not authorized.

Execution not authorized.

README/index update not authorized.

Staging/commit/push not authorized.

Awaiting separate explicit approval for any future index update, staging,
commit, push, implementation, or next lane.
