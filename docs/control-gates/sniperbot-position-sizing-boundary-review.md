# SniperBot Position Sizing Boundary Review

## Status

DOCUMENTATION ONLY -- GOVERNANCE ONLY -- POSITION-SIZING BOUNDARY ONLY --
NON-RUNTIME -- NON-EXECUTION -- NOT IMPLEMENTED -- NOT AN IMPLEMENTATION
APPROVAL

This file is auditor-facing and founder-facing. It is documentation-only,
governance-only, position-sizing boundary-only, non-runtime, and
non-execution.

This review defines future position-sizing readiness boundaries for
SniperBot. It does not create, approve, enable, prepare, or make ready
position-sizing runtime, position-size calculation, quantity calculation,
share quantity calculation, contract quantity calculation, crypto quantity
calculation, buying-power allocation, capital allocation, exposure
allocation, risk-to-position-sizing handoff,
position-sizing-to-trade-size handoff, position-sizing-to-order-routing
handoff, position-sizing-to-routing handoff, position-sizing approval,
position-sizing rejection, account-balance reads, broker balance reads,
Robinhood balance reads, buying-power reads, margin calculation, leverage
calculation, trade sizing, risk runtime, strategy runtime, market-data
runtime, tick-processing runtime, signal runtime, replay/backtest runtime,
order routing, order submission, order cancellation, broker routing,
Robinhood routing, exchange routing, paper-trading behavior, simulation
behavior, live-trading behavior, automated execution, command execution, or
execution capability.

No position-sizing lane, position-size calculation lane, quantity
calculation lane, share quantity lane, contract quantity lane, crypto
quantity lane, buying-power lane, capital-allocation lane,
exposure-allocation lane, risk-to-position-sizing lane,
position-sizing-to-trade-size lane, position-sizing-to-order-routing lane,
position-sizing-to-routing lane, position-sizing approval lane,
position-sizing rejection lane, account-balance lane, broker-balance lane,
Robinhood-balance lane, buying-power-read lane, margin lane, leverage lane,
trade-size lane, risk-runtime lane, strategy-runtime lane, market-data lane,
tick-processing lane, signal lane, replay/backtest lane, order-routing lane,
broker lane, Robinhood lane, exchange lane, paper-trading lane, simulation
lane, live-trading lane, SniperBot lane, command lane, or automation lane is
selected as implementation-ready by this review.

No position-size calculator, quantity calculator, share calculator, contract
calculator, crypto quantity calculator, buying-power allocator, capital
allocator, exposure allocator, risk-to-position-sizing handoff,
position-sizing-to-trade-size handoff, position-sizing-to-order-routing
handoff, position-sizing-to-routing handoff, position-sizing approval,
position-sizing rejection, account-balance read, broker balance read,
Robinhood balance read, buying-power read, margin calculator, leverage
calculator, trade-size mechanism, risk runtime, strategy runtime,
market-data runtime, tick-processing runtime, signal runtime, replay,
backtest, order-routing, broker, Robinhood, exchange, paper-trading,
simulation, live-trading, SniperBot, command, or execution behavior becomes
approved, eligible, configured, calculated, allocated, read, gated,
approved, rejected, queued, dispatched, handed off, routed, submitted,
cancelled, automated, activated, or ready through this review.

## Purpose

This review records the governance boundary for any possible future
SniperBot position-sizing readiness work. It exists to keep quantity
pressure, exposure allocation, capital-to-position conversion,
risk-to-position-sizing handoff, position-sizing-to-trade-size handoff, and
position-sizing-to-routing or position-sizing-to-order-routing authority
from being inferred from risk runtime, strategy runtime, signal runtime,
market data / tick processing, broker access, Robinhood access, order
routing, paper-trading, simulation, live-trading readiness, or any prior
SniperBot boundary document.

The purpose is boundary definition only. Position-sizing analysis is not
position sizing. Position-size analysis is not position-size calculation.
Quantity analysis is not quantity calculation. Share analysis is not share
quantity calculation. Contract analysis is not contract quantity
calculation. Crypto quantity analysis is not crypto quantity calculation.
Buying-power analysis is not buying-power allocation. Capital analysis is
not capital allocation. Exposure analysis is not exposure allocation.
Margin analysis is not margin calculation. Leverage analysis is not leverage
calculation. Documentation is not execution.

Position-sizing boundary mapping is not risk authority, trade-size
authority, order authority, broker authority, Robinhood authority, trading
authority, or execution authority. Risk-to-position-sizing analysis is not
risk-to-position-sizing handoff. Position-sizing-to-trade-size analysis is
not position-sizing-to-trade-size handoff. Position-sizing-to-routing
analysis is not position-sizing-to-routing handoff or
position-sizing-to-order-routing handoff.

Position-sizing-pipeline analysis is not position-sizing-pipeline
implementation. Position-size calculator analysis is not calculator
implementation. Quantity calculator analysis is not calculator
implementation. Quantity analysis is not quantity-calculation
implementation. Buying-power analysis is not account-balance access.
Buying-power analysis is not buying-power-read implementation or
buying-power-allocation implementation. Exposure-allocation analysis is not
exposure-allocation implementation.
Margin analysis is not margin implementation. Leverage analysis is not
leverage implementation. Trade-size analysis is not trade sizing. Routing
analysis is not routing implementation.

This review does not activate position-sizing runtime, a position-size
calculator, quantity calculator, share quantity calculator, contract
quantity calculator, crypto quantity calculator, buying-power allocator,
capital allocator, exposure allocator, margin calculator, leverage
calculator, position-sizing gate, position-sizing queue,
position-sizing dispatcher, runtime sizing pipeline,
risk-to-position-sizing handoff, position-sizing-to-trade-size handoff,
position-sizing-to-routing handoff, position-sizing-to-order-routing
handoff, trade-size path, market-data runtime, tick-processing runtime,
signal runtime, strategy runtime, risk runtime, replay path, backtest path,
order-routing path, broker route, Robinhood route, exchange route,
paper-trading path, simulation path, live-trading path, or execution path.

This review also does not authorize configuration work, environment-variable
work, API-key work, market-data integration, tick-processing integration,
signal integration, strategy integration, risk integration, replay
integration, backtest integration, account-balance integration,
broker-balance integration, Robinhood-balance integration,
position-size calculation work, quantity calculation work, share quantity
work, contract quantity work, crypto quantity work, buying-power work,
buying-power-read work, capital-allocation work, exposure-allocation work,
margin work, leverage work, position-sizing gate work, position-sizing queue work,
position-sizing dispatcher work, risk-to-position-sizing integration,
position-sizing-to-trade-size integration,
position-sizing-to-routing integration, position-sizing-to-order-routing
integration, trade-sizing integration, order-routing integration, latency / CUDA integration,
position-sizing-pipeline implementation, position-size calculator
implementation, quantity calculator implementation,
quantity-calculation implementation, buying-power-read implementation,
buying-power allocator implementation, exposure-allocation implementation,
exposure allocator implementation, margin calculator implementation,
leverage calculator implementation, trade-sizing implementation, routing
implementation, runtime behavior, feature-flag work, dry-run work,
mock-sizing work, sandbox-sizing work, or any preparatory technical step
that could become position-sizing activation.

Any future position-sizing capability, if ever considered, must require a
separate explicit founder-selected bounded task order, separate review
evidence, and separate approval before implementation could be discussed.

## Boundary Statement

Position sizing is a sizing-governance and execution-adjacent boundary. It
is separate from risk runtime, trade sizing, order routing, paper trading,
simulation, and live trading, and it must not inherit permission from those
boundaries.

The risk-runtime, strategy-runtime, signal-runtime, market-data /
tick-processing, broker-access, Robinhood-access, and order-routing
boundaries are prerequisite reference points only. They are not parent
approvals, partial approvals, implied approvals, inherited approvals,
technical readiness markers, risk-readiness approvals, strategy-readiness
approvals, data-readiness approvals, broker-readiness approvals,
order-routing approvals, position-sizing approvals, trade-size approvals,
runtime behavior approvals, or activation bridges for position-sizing work.

Position sizing is execution-adjacent because quantity decisions can
transform risk output into capital pressure, exposure pressure,
buying-power pressure, trade-size pressure, route pressure, or no-action
posture. Position sizing can touch symbols, asset classes, strategy outputs,
risk decisions, risk scores, exposure, buying power, account state, broker
state, Robinhood state, margin assumptions, leverage assumptions, protected
funds, trade-size assumptions, route pressure, audit evidence,
traceability, and possible future execution paths. That adjacency is the
reason this review must remain governance-only and non-execution.

This review defines position sizing as a future governance question only. It
does not define position sizing as a calculator task, quantity task, account
balance task, buying-power task, exposure-allocation task, capital-allocation
task, margin task, leverage task, position-sizing approval task,
position-sizing rejection task, handoff task, trade-size task, risk-runtime
task, strategy-runtime task, signal-runtime task, market-data task,
tick-processing task, replay task, backtest task, order-routing task, broker
task, Robinhood task, exchange task, paper-trading task, simulation task,
live-trading task, or runtime enablement task.

Prior SniperBot boundary reviews remain locked. Completing live-trading
readiness, broker access, Robinhood access, order routing, latency / CUDA,
market-data / tick-processing, signal runtime, strategy runtime, risk
runtime, paper-trading / simulation, capital-risk, max-loss / daily
stop-loss, trade-size, asset-class risk separation, eligibility/exclusion,
deferral/no-action, kill-switch, human-confirmation, audit-log,
rollback/no-action, no-autonomous-action, no-child-safety crossover, or
founder-approval reviews does not authorize position-sizing runtime,
position-size calculation, quantity calculation, share quantity calculation,
contract quantity calculation, crypto quantity calculation,
buying-power allocation, capital allocation, exposure allocation,
risk-to-position-sizing handoff, position-sizing-to-trade-size handoff,
position-sizing-to-routing handoff, position-sizing-to-order-routing
handoff, account-balance reads, broker balance reads, Robinhood balance
reads, buying-power reads, margin calculation, leverage calculation, trade
sizing, routing decisions, runtime behavior, or execution behavior.

Position sizing must not be inherited from:

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
* risk-runtime review
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

Position-sizing readiness requires its own explicit boundary before any
future position-sizing runtime, position-size calculator, quantity
calculator, share quantity calculator, contract quantity calculator, crypto
quantity calculator, buying-power allocator, capital allocator, exposure
allocator, margin calculator, leverage calculator, position-sizing gate,
position-sizing queue, position-sizing dispatcher, runtime sizing pipeline,
risk-to-position-sizing handoff, position-sizing-to-trade-size handoff,
position-sizing-to-routing handoff, position-sizing-to-order-routing
handoff, trade-size input, order-routing input, paper path, simulation path,
live path, or execution-adjacent behavior can be considered.

## Why Position Sizing Is Not Trading Approval

Position sizing is separate from risk runtime, trade sizing, order routing,
paper trading, simulation, and live trading.

A risk-runtime boundary may define future risk decisions, risk scoring,
risk approvals, risk rejections, exposure checks, and
risk-to-position-sizing handoff questions. A trade-size boundary may define
future trade-size evidence, caps, floors, and trade-size planning questions.
Neither boundary creates position-sizing approval, position-size
calculation approval, quantity calculation approval, buying-power approval,
capital-allocation approval, exposure-allocation approval, margin approval,
leverage approval, trade-sizing approval, routing-decision approval,
paper-trading approval, simulation approval, live-trading approval, or
execution approval.

Completing risk-runtime, strategy-runtime, signal-runtime, market-data /
tick-processing, latency / CUDA, broker-access, Robinhood-access, and
order-routing boundaries does not authorize:

* position-sizing runtime
* position-size calculation
* quantity calculation
* share quantity calculation
* contract quantity calculation
* crypto quantity calculation
* buying-power allocation
* capital allocation
* exposure allocation
* risk-to-position-sizing handoff
* position-sizing-to-trade-size handoff
* position-sizing-to-routing handoff
* position-sizing-to-order-routing handoff
* position-sizing approval
* position-sizing rejection
* account-balance reads
* broker balance reads
* Robinhood balance reads
* buying-power reads
* margin calculation
* leverage calculation
* trade sizing
* risk runtime
* strategy runtime
* market-data runtime
* tick-processing runtime
* signal runtime
* replay/backtest runtime
* CUDA sizing processing
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

Position-sizing work can become execution-adjacent before any order or trade
exists. A position-size calculator, quantity calculator, account-balance
read, buying-power allocator, exposure allocator, leverage calculator,
margin calculator, position-sizing gate, position-sizing queue,
position-sizing dispatcher, runtime sizing pipeline,
risk-to-position-sizing handoff, position-sizing-to-trade-size handoff, or
position-sizing-to-routing handoff or position-sizing-to-order-routing
handoff can still create authority, traceability, auditability, safety,
determinism, no-action, rollback, and execution-adjacent questions.

Position-sizing work must not be treated as:

* a configuration switch
* an environment-variable addition
* a sizing-engine addition
* a sizing library setup
* a position-size calculator
* a quantity calculator
* a share quantity calculator
* a contract quantity calculator
* a crypto quantity calculator
* an account-balance read
* a broker balance read
* a Robinhood balance read
* a buying-power allocator
* a capital allocator
* an exposure allocator
* a leverage calculator
* a margin calculator
* a position-sizing gate
* a position-sizing queue
* a position-sizing dispatcher
* a risk-to-position-sizing bridge
* a position-sizing-to-trade-size bridge
* a position-sizing-to-routing bridge
* a position-sizing-to-order-routing bridge
* a runtime sizing pipeline
* a trade-size prerequisite
* an order-routing prerequisite
* a routing implementation
* a broker-runtime prerequisite
* a Robinhood-runtime prerequisite
* a market-data runtime prerequisite
* a signal-runtime prerequisite
* a strategy-runtime prerequisite
* a risk-runtime prerequisite
* a CUDA runtime prerequisite
* a paper-trading shortcut
* a simulation shortcut
* a live-trading shortcut
* an execution shortcut

## Non-Authorization Statement

This review does not authorize, approve, enable, prepare, make ready, or
partially approve any of the following:

* position-sizing runtime
* position-size calculation
* quantity calculation
* share quantity calculation
* contract quantity calculation
* crypto quantity calculation
* buying-power allocation
* capital allocation
* exposure allocation
* risk-to-position-sizing handoff
* position-sizing-to-trade-size handoff
* position-sizing-to-routing handoff
* position-sizing-to-order-routing handoff
* position-sizing approval
* position-sizing rejection
* position-size calculators
* quantity calculators
* share quantity calculators
* contract quantity calculators
* crypto quantity calculators
* account-balance reads
* broker balance reads
* Robinhood balance reads
* buying-power reads
* buying-power allocators
* capital allocators
* exposure allocators
* margin calculation
* margin calculators
* leverage calculation
* leverage calculators
* position-sizing gates
* position-sizing queues
* position-sizing dispatchers
* runtime sizing pipelines
* position-sizing-pipeline implementation
* quantity-calculation implementation
* buying-power implementation
* exposure implementation
* trade sizing
* trade-size calculators
* trade-sizing implementation
* risk runtime
* strategy runtime
* market-data runtime
* tick-processing runtime
* signal runtime
* replay/backtest runtime
* CUDA sizing processing
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
deployment approval, testing approval, position-sizing approval,
position-sizing-runtime approval, position-size calculation approval,
quantity calculation approval, share quantity approval, contract quantity
approval, crypto quantity approval, buying-power approval,
buying-power-read approval, capital-allocation approval,
exposure-allocation approval, risk-to-position-sizing approval,
position-sizing-to-trade-size approval, position-sizing-to-routing approval,
position-sizing-to-order-routing approval, account-balance approval,
broker-balance approval, Robinhood-balance approval, margin approval,
leverage approval, trade-size approval, risk approval, strategy approval,
market-data approval, tick-processing approval, signal approval, replay
approval, backtest approval, CUDA approval, latency approval, order-routing
approval, broker approval, Robinhood approval, exchange approval, trading
approval, or execution approval.

It does not create position-sizing-pipeline implementation approval,
position-size calculator implementation approval, quantity calculator
implementation approval, account-balance integration approval,
broker-balance integration approval, Robinhood-balance integration approval,
quantity-calculation implementation approval, buying-power-read
implementation approval, buying-power allocator implementation approval,
exposure-allocation implementation approval, exposure allocator
implementation approval, margin implementation approval, margin calculator
implementation approval, leverage implementation approval, leverage
calculator implementation approval, position-sizing gate implementation
approval, position-sizing queue implementation approval,
position-sizing dispatcher implementation approval, trade-sizing
implementation approval, position-sizing-to-routing implementation
approval, routing implementation approval, runtime-behavior approval, or
activation approval.

Analysis remains analysis. Position-sizing boundary review remains review.
Boundary language remains boundary language. No sizing pipeline,
position-size calculator, quantity calculator, account-balance read,
buying-power read, buying-power allocator, exposure allocation, exposure
allocator, margin implementation, margin calculator, leverage
implementation, leverage calculator, position-sizing gate, queue,
dispatcher, handoff, trade sizing, routing, runtime, activation, or
execution behavior is created by this file.

## Position-Sizing Risk Surfaces

Future position-sizing work, if ever separately approved for analysis in a
later lane, would require governance attention to risk surfaces including:

* separation between risk decisions, position sizing, trade sizing, routing
  decisions, and execution
* position-sizing assumptions, sizing formulas, and parameter governance
* quantity calculation, false precision, rounding, and unit conversion
* share quantity, contract quantity, and crypto quantity differences
* options-specific, stock-specific, crypto-specific, and asset-class sizing
  differences
* buying-power interpretation and accidental account-access authority
* account-balance reads, broker balance reads, and Robinhood balance reads
* capital-to-position conversion and protected-funds boundaries
* exposure allocation and accidental capital-allocation authority
* margin calculation and leverage calculation pressure
* risk-to-position-sizing handoff and accidental quantity creation
* position-sizing-to-trade-size handoff and accidental trade-size pressure
* position-sizing-to-routing and position-sizing-to-order-routing handoff and
  accidental routing pressure
* position-sizing gates, queues, dispatchers, and backpressure
* position state, account state, duplicate intent, repeated intent, and stale
  intent
* market-data / tick-processing coupling and accidental data-runtime
  assumptions
* signal-runtime coupling and accidental signal-to-sizing activation
* strategy-runtime coupling and accidental strategy-to-sizing activation
* risk-runtime coupling and accidental risk-to-sizing activation
* latency / CUDA coupling and accidental optimized sizing paths
* replay/backtest coupling and false readiness from historical evidence
* paper-trading, simulation, and live-trading confusion
* audit-log timing, traceability, and evidence preservation
* rollback timing, no-action fallback, and fail-closed behavior
* command-execution adjacency and automation pressure

Listing these risk surfaces does not approve any sizing control, runtime
control, position-size calculator, quantity calculator, account-balance
read, buying-power allocator, exposure allocator, margin calculator,
leverage calculator, risk-to-position-sizing handoff,
position-sizing-to-trade-size handoff, position-sizing-to-routing handoff,
position-sizing-to-order-routing handoff, trade sizing, routing
implementation, route, trade, paper path, simulation path, live path,
command path, runtime behavior, or execution behavior.

## Required Future Approval Gates

Before any future position-sizing implementation could be considered, later
separate lanes would need explicit founder-selected approval for each
relevant layer, including at minimum:

* position-sizing scope definition
* risk-runtime separation review
* strategy-runtime separation review
* signal-runtime separation review
* market-data / tick-processing separation review
* replay/backtest-separation review
* position-sizing formula and parameter review
* quantity-calculation taxonomy review
* share quantity separation review
* contract quantity separation review
* crypto quantity separation review
* buying-power boundary review
* account-balance read non-authorization review
* broker balance read non-authorization review
* Robinhood balance read non-authorization review
* capital-to-position conversion review
* exposure-allocation separation review
* margin calculation separation review
* leverage calculation separation review
* protected-funds separation review
* risk-to-position-sizing handoff review
* position-sizing-to-trade-size handoff review
* position-sizing-to-routing handoff review
* position-sizing-to-order-routing handoff review
* position-sizing-pipeline implementation non-authorization review
* quantity-calculation implementation non-authorization review
* buying-power implementation non-authorization review
* exposure implementation non-authorization review
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
* adding position-sizing runtime
* adding position-size calculation
* adding quantity calculation
* adding share quantity calculation
* adding contract quantity calculation
* adding crypto quantity calculation
* adding buying-power allocation
* adding capital allocation
* adding exposure allocation
* adding risk-to-position-sizing handoff
* adding position-sizing-to-trade-size handoff
* adding position-sizing-to-routing handoff
* adding position-sizing-to-order-routing handoff
* adding position-sizing approval
* adding position-sizing rejection
* adding position-size calculators
* adding quantity calculators
* adding share quantity calculators
* adding contract quantity calculators
* adding crypto quantity calculators
* adding account-balance reads
* adding broker balance reads
* adding Robinhood balance reads
* adding buying-power reads
* adding buying-power allocators
* adding capital allocators
* adding exposure allocators
* adding margin calculation
* adding margin calculators
* adding leverage calculation
* adding leverage calculators
* adding position-sizing gates
* adding position-sizing queues
* adding position-sizing dispatchers
* adding runtime sizing pipelines
* adding position-sizing-pipeline implementation
* adding quantity-calculation implementation
* adding buying-power implementation
* adding exposure implementation
* adding trade sizing
* adding trade-size calculators
* adding trade-sizing implementation
* adding risk runtime
* adding strategy runtime
* adding market-data runtime
* adding quote-feed runtime
* adding option-chain runtime
* adding tick-processing runtime
* adding data-ingestion runtime
* adding signal runtime
* adding replay/backtest runtime
* adding CUDA sizing processing
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
paths, mock sizing engines, sandbox sizing engines, recorded quantity
decisions, replay paths, backtest paths, position-size calculator paths,
quantity-calculation paths, buying-power paths, exposure-allocation paths,
margin paths, leverage paths, position-sizing gate paths,
position-sizing queue paths, position-sizing dispatcher paths,
risk-to-position-sizing adapters, position-sizing-to-routing adapters,
trade-size adapters, routing adapters, or position-sizing pipelines that
could later be used as activation bridges.

## Governance Conclusion

The SniperBot position sizing boundary remains documentation-only and
governance-only. It records that position sizing, quantity pressure,
exposure allocation, risk-to-position-sizing handoff,
capital-to-position conversion, position-to-trade-size separation, and
position-sizing-to-routing separation are execution-adjacent safety and
authority questions, not implementation tasks.

Risk runtime, strategy runtime, signal runtime, market data / tick
processing, broker access, Robinhood access, order routing, trade-size
planning, paper-trading, simulation, and live-trading readiness do not
create inherited position-sizing approval. Position-sizing review does not
create risk approval, strategy approval, market-data approval,
account-balance approval, broker-balance approval, Robinhood-balance
approval, buying-power approval, exposure-allocation approval, margin
approval, leverage approval, trade-size approval, order-routing approval,
broker approval, Robinhood approval, exchange approval, paper-trading
approval, simulation approval, live-trading approval, command-execution
approval, or execution capability.

Safety and authority boundaries come before execution. Position-sizing
boundary analysis remains separate from activation. Any future
position-sizing movement must occur only through later, explicit,
founder-selected, separately approved governance lanes before implementation
could even be considered.
