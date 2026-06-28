# SniperBot Risk Runtime Boundary Review

## Status

DOCUMENTATION ONLY -- GOVERNANCE ONLY -- RISK-RUNTIME BOUNDARY ONLY --
NON-RUNTIME -- NON-EXECUTION -- NOT IMPLEMENTED -- NOT AN IMPLEMENTATION
APPROVAL

This file is auditor-facing and founder-facing. It is documentation-only,
governance-only, risk-runtime boundary-only, non-runtime, and
non-execution.

This review defines future risk-runtime readiness boundaries for SniperBot.
It does not create, approve, enable, prepare, or make ready risk runtime,
risk activation, risk scoring, risk decisioning, risk approval, risk
rejection, strategy-to-risk handoff, risk-to-position-sizing handoff,
risk-to-trade-sizing handoff, risk-to-routing handoff,
risk-to-order-routing handoff, exposure calculation runtime,
capital-allocation runtime, loss-limit enforcement runtime, stop-loss
runtime, daily stop-loss runtime, position sizing, trade sizing,
market-data runtime, tick-processing runtime, signal runtime, strategy
runtime, replay/backtest runtime, order routing, order submission, order
cancellation, broker routing, Robinhood routing, exchange routing,
paper-trading behavior, simulation behavior, live-trading behavior,
automated execution, command execution, or execution capability.

No risk lane, risk-runtime lane, risk-activation lane, risk-scoring lane,
risk-decision lane, risk-approval lane, risk-rejection lane,
strategy-to-risk lane, risk-to-position-sizing lane, risk-to-trade-sizing
lane, risk-to-routing lane, risk-to-order-routing lane,
exposure-calculation lane, capital-allocation lane, loss-limit lane,
stop-loss lane, daily-stop lane, position-sizing lane, trade-size lane,
market-data lane, tick-processing lane, signal lane, strategy lane,
replay/backtest lane, order-routing lane, broker lane, Robinhood lane,
exchange lane, paper-trading lane, simulation lane, live-trading lane,
SniperBot lane, command lane, or automation lane is selected as
implementation-ready by this review.

No risk engine, risk runtime, risk activation, risk scorer, risk gate,
risk decision, risk approval, risk rejection, exposure calculator, capital
allocator, loss-limit enforcer, stop-loss enforcer, daily stop-loss enforcer,
position-size calculator, trade-size calculator, strategy-to-risk handoff,
risk-to-position-sizing handoff, risk-to-trade-sizing handoff,
risk-to-routing handoff, risk-to-order-routing handoff, market-data,
tick-processing, signal, strategy, replay, backtest, order-routing, broker,
Robinhood, exchange, paper-trading, simulation, live-trading, SniperBot,
command, or execution behavior becomes approved, eligible, configured,
scored, decided, approved, rejected, calculated, enforced, queued,
dispatched, handed off, routed, submitted, cancelled, automated, activated,
or ready through this review.

## Purpose

This review records the governance boundary for any possible future
SniperBot risk-runtime readiness work. It exists to keep risk decisioning,
risk scoring, exposure checks, capital-allocation checks, loss-limit checks,
stop-loss checks, daily stop-loss checks, strategy-to-risk handoff,
risk-to-position-sizing handoff, risk-to-trade-sizing handoff, and
risk-to-routing or risk-to-order-routing authority from being inferred from
strategy runtime, signal runtime, market data / tick processing, latency /
CUDA, broker access, Robinhood access, order routing, paper-trading,
simulation, live-trading readiness, or any prior SniperBot boundary
document.

The purpose is boundary definition only. Risk analysis is not risk
activation. Risk-runtime analysis is not risk runtime. Risk-scoring analysis
is not risk scoring. Risk-decision analysis is not risk decisioning.
Risk-approval analysis is not risk approval. Risk-rejection analysis is not
risk rejection. Exposure analysis is not exposure calculation runtime.
Capital-allocation analysis is not capital-allocation runtime. Loss-limit
analysis is not loss-limit enforcement. Stop-loss analysis is not stop-loss
runtime. Daily stop-loss analysis is not daily stop-loss runtime.
Documentation is not execution.

Risk-boundary mapping is not strategy authority, position-sizing authority,
trade-sizing authority, order authority, broker authority, Robinhood
authority, trading authority, or execution authority. Strategy-to-risk
analysis is not strategy-to-risk handoff. Risk-to-position-sizing analysis
is not risk-to-position-sizing handoff. Risk-to-trade-sizing analysis is not
risk-to-trade-sizing handoff. Risk-to-routing analysis is not
risk-to-routing handoff or risk-to-order-routing handoff.

Risk-pipeline analysis is not risk-pipeline implementation. Risk-engine
analysis is not risk-engine implementation. Risk-scorer analysis is not
risk-scorer implementation. Risk-gate analysis is not risk-gate
implementation. Risk-decision analysis is not risk-decision implementation.
Risk-approval analysis is not risk-approval implementation. Risk-rejection
analysis is not risk-rejection implementation. Exposure-check analysis is
not exposure-calculator implementation. Loss-limit analysis is not
loss-limit enforcement runtime. Position-size analysis is not position
sizing. Trade-size analysis is not trade sizing. Routing analysis is not
routing implementation.

This review does not activate a risk runtime, risk engine, risk scorer,
risk gate, risk approval path, risk rejection path, exposure calculator,
capital-allocation path, loss-limit enforcer, stop-loss enforcer, daily
stop-loss enforcer, position-size calculator, trade-size calculator,
strategy-to-risk handoff, risk-to-position-sizing handoff,
risk-to-trade-sizing handoff, risk-to-routing handoff,
risk-to-order-routing handoff, market-data runtime, tick-processing runtime,
signal runtime, strategy runtime, replay path, backtest path,
order-routing path, broker route, Robinhood route, exchange route,
paper-trading path, simulation path, live-trading path, or execution path.

This review also does not authorize configuration work, environment-variable
work, API-key work, market-data integration, tick-processing integration,
signal integration, strategy integration, replay integration, backtest
integration, risk-engine work, risk-scoring work, risk-decision work,
risk-approval work, risk-rejection work, exposure-calculation work,
capital-allocation work, loss-limit work, stop-loss work, daily-stop work,
position-size work, trade-size work, risk-queue work, risk-dispatcher work,
strategy-to-risk integration, risk-to-position-sizing integration,
risk-to-trade-sizing integration, risk-to-routing integration,
risk-to-order-routing integration, order-routing integration, latency / CUDA
integration, risk-pipeline implementation, risk-engine implementation,
risk-scorer implementation, risk-gate implementation,
risk-decision implementation, risk-approval implementation,
risk-rejection implementation, exposure-calculator implementation,
capital-allocation implementation, loss-limit enforcement implementation,
stop-loss implementation, daily stop-loss implementation, position-sizing
implementation, trade-sizing implementation, routing implementation,
runtime behavior, feature-flag work, dry-run work, mock-risk work,
sandbox-risk work, or any preparatory technical step that could become
risk-runtime activation.

Any future risk-runtime capability, if ever considered, must require a
separate explicit founder-selected bounded task order, separate review
evidence, and separate approval before implementation could be discussed.

## Boundary Statement

Risk runtime is a risk-governance and execution-adjacent boundary. It is
separate from strategy runtime, signal runtime, market data / tick
processing, position sizing, trade sizing, order routing, paper trading,
simulation, and live trading, and it must not inherit permission from those
boundaries.

The strategy-runtime, signal-runtime, market-data / tick-processing,
latency / CUDA, broker-access, Robinhood-access, and order-routing
boundaries are prerequisite reference points only. They are not parent
approvals, partial approvals, implied approvals, inherited approvals,
technical readiness markers, strategy-readiness approvals, signal-readiness
approvals, data-readiness approvals, broker-readiness approvals,
order-routing approvals, risk-runtime approvals, risk-scoring approvals,
risk-decision approvals, position-sizing approvals, trade-size approvals,
runtime behavior approvals, or activation bridges for risk-runtime work.

Risk runtime is execution-adjacent because risk decisions can transform
strategy intent into approval, rejection, sizing pressure, routing pressure,
or no-action posture. Risk scoring can touch symbols, asset classes,
strategy outputs, signal state, indicator outputs, exposure, capital
availability, loss limits, stop-loss state, daily stop state, account state,
position state, trade-size assumptions, route pressure, audit evidence,
traceability, and possible future execution paths. That adjacency is the
reason this review must remain governance-only and non-execution.

This review defines risk runtime as a future governance question only. It
does not define risk runtime as a risk-engine task, risk-scoring task,
risk-decision task, risk-approval task, risk-rejection task, exposure
calculation task, capital-allocation task, loss-limit task, stop-loss task,
daily-stop task, position-sizing task, trade-size task, handoff task,
market-data task, tick-processing task, signal-runtime task,
strategy-runtime task, replay task, backtest task, order-routing task,
broker task, Robinhood task, exchange task, paper-trading task, simulation
task, live-trading task, or runtime enablement task.

Prior SniperBot boundary reviews remain locked. Completing live-trading
readiness, broker access, Robinhood access, order routing, latency / CUDA,
market-data / tick-processing, signal runtime, strategy runtime,
paper-trading / simulation, capital-risk, max-loss / daily stop-loss,
trade-size, asset-class risk separation, eligibility/exclusion,
deferral/no-action, kill-switch, human-confirmation, audit-log,
rollback/no-action, no-autonomous-action, no-child-safety crossover, or
founder-approval reviews does not authorize risk runtime, risk activation,
risk scoring, risk decisioning, risk approval, risk rejection, risk engines,
risk gates, exposure calculation runtime, capital-allocation runtime,
loss-limit enforcement runtime, stop-loss runtime, daily stop-loss runtime,
strategy-to-risk handoffs, risk-to-position-sizing handoffs,
risk-to-trade-sizing handoffs, risk-to-routing handoffs,
risk-to-order-routing handoffs, position sizing, trade sizing, routing
decisions, runtime behavior, or execution behavior.

Risk runtime must not be inherited from:

* EchoAuth governance
* NI-AI governance
* broker/trading separation review
* live-trading readiness review
* broker-access review
* Robinhood-access review
* order-routing review
* latency / CUDA review
* market-data / tick-processing review
* signal-runtime review
* strategy-runtime review
* paper-trading / simulation review
* capital-risk review
* max-loss / daily stop-loss review
* trade-size review
* asset-class risk separation review
* options risk review
* stock risk review
* crypto risk review
* asset-class eligibility / exclusion review
* options eligibility / exclusion review
* stock eligibility / exclusion review
* crypto eligibility / exclusion review
* asset-class deferral / no-action review
* options deferral / no-action review
* stock deferral / no-action review
* crypto deferral / no-action review
* kill-switch review
* human-confirmation review
* audit-log / trade-traceability review
* rollback / no-action fallback review
* no-autonomous-action review
* no child-safety governance crossover review
* founder approval review
* README/index inclusion
* clean git status
* committed, pushed, indexed, verified, or parked status

Risk-runtime readiness requires its own explicit boundary before any future
risk runtime, risk activation, risk engine, risk scorer, risk gate, risk
decision, risk approval, risk rejection, exposure calculator,
capital-allocation path, loss-limit path, stop-loss path, daily-stop path,
strategy-to-risk handoff, risk-to-position-sizing handoff,
risk-to-trade-sizing handoff, risk-to-routing handoff,
risk-to-order-routing handoff, position-size input, trade-size input,
order-routing input, paper path, simulation path, live path, or
execution-adjacent behavior can be considered.

## Why Risk Runtime Is Not Trading Approval

Risk runtime is separate from strategy runtime, signal runtime, market data
/ tick processing, position sizing, trade sizing, order routing, paper
trading, simulation, and live trading.

A strategy-runtime boundary may define future trade-intent, strategy
selection, strategy scoring, and strategy-to-risk handoff questions. A
signal-runtime boundary may define future signal generation, indicator
evaluation, confidence scoring, and signal handoff questions. A market-data
/ tick-processing boundary may define future feed, quote, option-chain,
tick-processing, stale-data, and replay questions. None of those boundaries
creates risk approval, risk-activation approval, risk-scoring approval,
risk-decision approval, risk-approval path approval, risk-rejection path
approval, exposure-calculation approval, capital-allocation approval,
loss-limit approval, stop-loss approval, daily stop-loss approval,
position-sizing approval, trade-sizing approval, routing-decision approval,
paper-trading approval, simulation approval, live-trading approval, or
execution approval.

Completing strategy-runtime, signal-runtime, market-data / tick-processing,
latency / CUDA, broker-access, Robinhood-access, and order-routing
boundaries does not authorize:

* risk runtime
* risk activation
* risk scoring
* risk decisioning
* risk approval
* risk rejection
* risk engines
* risk scorers
* risk gates
* risk approval paths
* risk rejection paths
* strategy-to-risk handoff
* risk-to-position-sizing handoff
* risk-to-trade-sizing handoff
* risk-to-routing handoff
* risk-to-order-routing handoff
* exposure calculation runtime
* capital-allocation runtime
* loss-limit enforcement runtime
* stop-loss runtime
* daily stop-loss runtime
* position sizing
* trade sizing
* market-data runtime
* tick-processing runtime
* signal runtime
* strategy runtime
* replay/backtest runtime
* CUDA risk processing
* latency optimization
* order routing
* order submission
* order cancellation
* broker routing
* Robinhood routing
* exchange routing
* paper trading
* simulation
* live trading
* automated execution
* command execution
* execution capability

Risk work can become execution-adjacent before any order or trade exists. A
risk engine, risk scorer, risk gate, approval path, rejection path, exposure
calculator, loss-limit enforcer, stop-loss enforcer, daily stop-loss
enforcer, position-size calculator, trade-size calculator,
strategy-to-risk handoff, risk-to-position-sizing handoff,
risk-to-trade-sizing handoff, risk-to-routing handoff, or
risk-to-order-routing handoff can still create authority, traceability,
auditability, safety, determinism, no-action, rollback, and
execution-adjacent questions.

Risk-runtime work must not be treated as:

* a configuration switch
* an environment-variable addition
* a risk-engine addition
* a risk library setup
* a risk scorer
* a risk gate
* a risk approval path
* a risk rejection path
* an exposure calculator
* a capital-allocation calculator
* a loss-limit enforcer
* a stop-loss enforcer
* a daily stop-loss enforcer
* a position-size calculator
* a trade-size calculator
* a strategy-to-risk bridge
* a risk-to-position-sizing bridge
* a risk-to-trade-sizing bridge
* a risk-to-routing bridge
* a risk-to-order-routing bridge
* a risk-pipeline implementation
* a position-sizing prerequisite
* a trade-size prerequisite
* an order-routing prerequisite
* a routing implementation
* a market-data runtime prerequisite
* a signal-runtime prerequisite
* a strategy-runtime prerequisite
* a CUDA runtime prerequisite
* a paper-trading shortcut
* a simulation shortcut
* a live-trading shortcut
* an execution shortcut

## Non-Authorization Statement

This review does not authorize, approve, enable, prepare, make ready, or
partially approve any of the following:

* risk runtime
* risk activation
* risk scoring
* risk decisioning
* risk approval
* risk rejection
* risk engines
* risk scorers
* risk gates
* risk approval paths
* risk rejection paths
* risk-pipeline implementation
* risk-decision implementation
* risk-approval implementation
* risk-rejection implementation
* strategy-to-risk handoff
* risk-to-position-sizing handoff
* risk-to-trade-sizing handoff
* risk-to-routing handoff
* risk-to-order-routing handoff
* exposure calculation runtime
* exposure calculators
* capital-allocation runtime
* capital-allocation calculators
* loss-limit enforcement runtime
* loss-limit enforcement
* stop-loss runtime
* stop-loss enforcement
* daily stop-loss runtime
* daily stop-loss enforcement
* position sizing
* position-size calculators
* position-sizing implementation
* trade sizing
* trade-size calculators
* trade-sizing implementation
* market-data runtime
* tick-processing runtime
* signal runtime
* strategy runtime
* replay/backtest runtime
* CUDA risk processing
* latency optimization
* order routing
* order creation
* order submission
* order cancellation
* order modification
* broker routing
* Robinhood routing
* exchange routing
* routing API calls
* paper trading
* simulation
* live trading
* automated execution
* SniperBot behavior
* command execution
* execution capability

This review does not create implementation approval, readiness approval,
deployment approval, testing approval, risk approval, risk-runtime approval,
risk-activation approval, risk-scoring approval, risk-decision approval,
risk-approval-path approval, risk-rejection-path approval, exposure approval,
capital-allocation approval, loss-limit approval, stop-loss approval, daily
stop-loss approval, strategy-to-risk approval, risk-to-position-sizing
approval, risk-to-trade-sizing approval, risk-to-routing approval,
risk-to-order-routing approval, market-data approval, tick-processing
approval, signal approval, strategy approval, replay approval, backtest
approval, position-sizing approval, trade-size approval, CUDA approval,
latency approval, order-routing approval, broker approval, Robinhood
approval, exchange approval, trading approval, or execution approval.

It does not create risk-pipeline implementation approval, risk-engine
implementation approval, risk-scorer implementation approval, risk-gate
implementation approval, risk-decision implementation approval,
risk-approval implementation approval, risk-rejection implementation
approval, exposure-calculator implementation approval, capital-allocation
implementation approval, loss-limit enforcement implementation approval,
stop-loss implementation approval, daily stop-loss implementation approval,
position-sizing implementation approval, trade-sizing implementation
approval, risk-to-routing implementation approval, routing implementation
approval, runtime-behavior approval, or activation approval.

Analysis remains analysis. Risk-boundary review remains review. Boundary
language remains boundary language. No risk pipeline, risk engine, risk
scorer, risk gate, risk-decision implementation, approval path, rejection
path, exposure calculation, capital allocation, loss-limit enforcement,
stop-loss enforcement, daily stop-loss enforcement, sizing, routing,
runtime, activation, or execution behavior is created by this file.

## Risk-Runtime Risk Surfaces

Future risk-runtime work, if ever separately approved for analysis in a
later lane, would require governance attention to risk surfaces including:

* separation between strategies, risk decisions, sizing decisions, routing
  decisions, and execution
* risk-engine inventory, risk assumptions, and risk parameter governance
* risk scoring, risk thresholds, false precision, and score interpretation
* risk approval paths and pressure toward action
* risk rejection paths, no-action posture, and fail-closed behavior
* exposure calculation and accidental capital-allocation authority
* capital-allocation checks and protected-funds boundaries
* loss-limit, stop-loss, and daily stop-loss coupling
* max-loss / daily stop-loss evidence leakage into runtime behavior
* strategy-to-risk handoff and accidental risk-decision creation
* risk-to-position-sizing handoff and accidental sizing pressure
* risk-to-trade-sizing handoff and accidental trade-size pressure
* risk-to-routing and risk-to-order-routing handoff and accidental
  execution-adjacent routing
* options-specific, stock-specific, crypto-specific, and asset-class risk
  differences
* position state, account state, duplicate intent, repeated intent, and stale
  intent
* market-data / tick-processing coupling and accidental data-runtime
  assumptions
* signal-runtime coupling and accidental signal-to-risk activation
* strategy-runtime coupling and accidental strategy-to-risk activation
* latency / CUDA coupling and accidental optimized risk-runtime paths
* replay/backtest coupling and false readiness from historical evidence
* paper-trading, simulation, and live-trading confusion
* audit-log timing, traceability, and evidence preservation
* rollback timing, no-action fallback, and fail-closed behavior
* command-execution adjacency and automation pressure

Listing these risk surfaces does not approve any risk control, runtime
control, risk engine, risk scorer, risk gate, approval path, rejection path,
exposure calculator, capital allocator, loss-limit enforcer, stop-loss
enforcer, daily stop-loss enforcer, strategy-to-risk handoff,
risk-to-position-sizing handoff, risk-to-trade-sizing handoff,
risk-to-routing handoff, risk-to-order-routing handoff, position sizing,
trade sizing, sizing implementation, routing implementation, route, trade,
paper path, simulation path, live path, command path, runtime behavior, or
execution behavior.

## Required Future Approval Gates

Before any future risk-runtime implementation could be considered, later
separate lanes would need explicit founder-selected approval for each
relevant layer, including at minimum:

* risk-runtime scope definition
* strategy-runtime separation review
* signal-runtime separation review
* market-data / tick-processing separation review
* replay/backtest-separation review
* risk-engine inventory and risk-family review
* risk-scoring and threshold review
* risk-decision taxonomy review
* risk-approval path review
* risk-rejection and no-action path review
* exposure-calculation separation review
* capital-allocation separation review
* protected-funds separation review
* loss-limit enforcement separation review
* stop-loss runtime separation review
* daily stop-loss runtime separation review
* max-loss / daily stop-loss boundary inheritance review
* strategy-to-risk handoff review
* risk-to-position-sizing handoff review
* risk-to-trade-sizing handoff review
* risk-to-routing handoff review
* risk-to-order-routing handoff review
* risk-pipeline implementation non-authorization review
* risk-decision implementation non-authorization review
* position-sizing separation review
* trade-size separation review
* order-routing separation review
* latency / CUDA separation review
* audit-log and traceability review
* rollback and no-action fallback timing review
* paper-trading / simulation separation review
* live-trading non-authorization review
* deployment and operations review
* explicit founder approval before any implementation task

Each future gate must be separate, explicit, and bounded. A future gate must
not be inferred from this review, from README/index inclusion, from a clean
git state, from committed status, from pushed status, or from any completed
SniperBot boundary document.

## Explicitly Out of Scope

The following are explicitly out of scope for this review:

* modifying runtime code
* adding risk runtime
* adding risk activation
* adding risk scoring
* adding risk decisioning
* adding risk approval
* adding risk rejection
* adding risk engines
* adding risk scorers
* adding risk gates
* adding risk approval paths
* adding risk rejection paths
* adding risk-pipeline implementation
* adding risk-decision implementation
* adding risk-approval implementation
* adding risk-rejection implementation
* adding strategy-to-risk handoff
* adding risk-to-position-sizing handoff
* adding risk-to-trade-sizing handoff
* adding risk-to-routing handoff
* adding risk-to-order-routing handoff
* adding exposure calculation runtime
* adding exposure calculators
* adding capital-allocation runtime
* adding capital-allocation calculators
* adding loss-limit enforcement runtime
* adding loss-limit enforcement
* adding stop-loss runtime
* adding stop-loss enforcement
* adding daily stop-loss runtime
* adding daily stop-loss enforcement
* adding position sizing
* adding position-size calculators
* adding position-sizing implementation
* adding trade sizing
* adding trade-size calculators
* adding trade-sizing implementation
* adding market-data runtime
* adding quote-feed runtime
* adding option-chain runtime
* adding tick-processing runtime
* adding data-ingestion runtime
* adding signal runtime
* adding strategy runtime
* adding replay/backtest runtime
* adding CUDA risk processing
* adding CUDA code
* adding GPU kernels
* adding latency optimization
* adding order-routing logic
* adding routing implementation
* adding order submission logic
* adding order cancellation logic
* adding order modification logic
* adding broker routing
* adding Robinhood routing
* adding exchange routing
* adding API key or secret handling
* adding credential storage or retrieval
* adding OAuth, login, session, cookie, or browser automation behavior
* adding wallet or custody behavior
* adding paper trading
* adding simulation
* adding live trading
* adding automated execution
* adding SniperBot behavior
* adding command execution
* adding execution capability
* modifying tests
* modifying CI
* modifying README/index entries

This review does not approve preparatory scaffolding, feature flags, dry-run
paths, mock risk engines, sandbox risk engines, recorded risk decisions,
replay paths, backtest paths, risk-engine paths, risk-scoring paths,
risk-gate paths, risk-decision paths, approval paths, rejection paths,
exposure-calculation paths, capital-allocation paths, loss-limit paths,
stop-loss paths, daily-stop paths, strategy-to-risk adapters,
risk-to-routing adapters, sizing adapters, routing adapters, or risk
pipelines that could later be used as activation bridges.

## Governance Conclusion

The SniperBot risk runtime boundary remains documentation-only and
governance-only. It records that risk runtime, risk decisioning,
risk scoring, exposure checks, capital-allocation checks, loss-limit checks,
stop-loss checks, daily stop-loss checks, strategy-to-risk handoff,
risk-to-position-sizing handoff, risk-to-trade-sizing handoff, and
risk-to-routing and risk-to-order-routing handoff are execution-adjacent
safety and authority questions, not implementation tasks.

Strategy runtime, signal runtime, market data / tick processing, latency /
CUDA, broker access, Robinhood access, order routing, paper-trading,
simulation, and live-trading readiness do not create inherited
risk-runtime approval. Risk-runtime review does not create market-data
approval, signal approval, strategy approval, position-sizing approval,
trade-size approval, order-routing approval, broker approval, Robinhood
approval, exchange approval, paper-trading approval, simulation approval,
live-trading approval, command-execution approval, or execution capability.

Safety and authority boundaries come before execution. Risk-boundary
analysis remains separate from activation. Any future risk-runtime movement
must occur only through later, explicit, founder-selected, separately
approved governance lanes before implementation could even be considered.
