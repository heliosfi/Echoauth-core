# SniperBot Crypto Risk Boundary Review

## Locked Baseline

Repo: `heliosfi/Echoauth-core`

Branch: `main`

Starting commit: `f9ac2a22379555b1bc3d425233ae5042a3c0ec14`

State: clean and synchronized with `origin/main`

## Status

DOCUMENTATION ONLY -- GOVERNANCE ONLY -- CRYPTO-RISK-BOUNDARY-ONLY --
CRYPTO-RISK-PLANNING-ONLY -- NON-RUNTIME -- NON-EXECUTION -- NOT
IMPLEMENTED -- NOT AN IMPLEMENTATION APPROVAL

This file is auditor-facing and founder-facing. It is documentation-only,
governance-only, crypto-risk-boundary-only, crypto-risk-planning-only,
non-runtime, and non-execution.

This review defines a SniperBot crypto-risk boundary for future analysis
only. It does not create crypto readiness, crypto approval, crypto trading
approval, broker approval, exchange approval, wallet approval, strategy
approval, order authority, automation authority, command authority,
execution readiness, deployment permission, or execution capability.

This review is not a readiness assessment. It does not certify that any
crypto risk surface is understood, controlled, bounded, mitigated, tested,
implemented, deployable, or safe for use.

Crypto Risk had not been created before this lane. This file creates only a
governance boundary document. It does not create runtime crypto risk
controls, runtime trading controls, executable risk scoring, schemas,
events, records, databases, commands, services, broker connections,
exchange connections, wallet integrations, custody workflows, order paths,
strategy paths, automation paths, or execution paths.

No future reader, system, agent, workflow, or trading-adjacent task may
reinterpret this review as crypto activation, crypto implementation
approval, crypto strategy approval, crypto asset approval, broker
permission, exchange permission, wallet permission, order authority,
position-sizing authority, leverage authority, margin authority, liquidation
control authority, command authority, deployment authority, or execution
authority.

Documentation is not execution.

Boundary review is not activation.

## Purpose

The purpose of this review is to define the boundary around future
SniperBot crypto-risk analysis without approving or enabling any crypto
capability.

The SniperBot Asset-Class Risk Separation Boundary Review named crypto-risk
as a future unresolved asset-specific risk boundary. The SniperBot Crypto
Deferral / No-Action Boundary Review parked crypto no-action posture, but
did not authorize crypto risk approval, crypto eligibility, crypto strategy,
exchange connectivity, wallet/custody handling, order submission, automated
execution, or crypto trading.

This lane records what must remain separated before any future crypto work
could be considered. It does not approve what comes next.

SniperBot must not treat crypto as merely another asset-class switch. Crypto
risk requires separate governance because the risk surface is structurally
different from stocks and cannot be inherited from stock-risk, options-risk,
trade-size, max-loss, or capital-risk documents.

This review preserves the EchoAuth / NI-AI governance principle that safety
and authority boundaries come before execution.

Nothing in this review may be used as inherited permission from stock-risk,
options-risk, asset-class risk separation, trade-size, max-loss,
capital-risk, broker/trading, paper-trading, simulation, or live-trading
lanes.

## Boundary Statement

This review is a boundary document only.

It may identify crypto-specific risk surfaces that a later separately
approved lane would need to analyze. It must not define executable crypto
controls, runtime risk checks, trading logic, exchange workflows, wallet
workflows, custody workflows, broker workflows, order-routing workflows,
strategy workflows, automation workflows, liquidation workflows, position
sizing, trade sizing, token selection, stablecoin handling, DeFi
interaction, smart-contract interaction, market-making, arbitrage, or
execution behavior.

Analysis and activation are separate.

Analysis in this document means governance review, vocabulary boundaries,
and future evidence categories.

Activation would mean implementation, runtime behavior, executable controls,
credentials, connectivity, order authority, trading authorization, automated
execution, custody handling, deployment permission, or production use.

This review permits analysis only. It does not permit activation.

Analysis language in this file must not be converted into configuration,
feature flags, runtime checks, control logic, prompts, tools, schemas,
tests, CI checks, market-data workflows, trading workflows, exchange
workflows, wallet workflows, custody workflows, or implementation tasks
without a later separate explicit approval gate.

Ambiguous crypto authority resolves to no-action, not assumed approval.

Incomplete crypto evidence resolves to no-action, not partial execution.

"We don't move until system move." remains the governing posture.

## Why Crypto Risk Is Not Stock Risk

Crypto risk is structurally different from stock risk and must not be
treated as a simple asset-class extension.

Crypto markets can trade 24/7, including weekends, holidays, and overnight
periods when human monitoring, banking rails, liquidity, and operational
support may be reduced.

Crypto liquidity is fragmented across exchanges, venues, regions, trading
pairs, on-chain pools, stablecoin rails, and market-maker relationships.
Venue-specific depth, spreads, fees, outages, withdrawal limits, and market
integrity conditions can materially change execution risk.

Crypto liquidity gaps can appear suddenly. A token that appears liquid under
normal conditions may become thin, halted, delisted, depegged, restricted,
or unavailable during stress.

Crypto introduces custody and wallet risk. Private keys, wallet approvals,
withdrawal addresses, custody arrangements, exchange account security,
deposit/withdrawal latency, account freezes, and irreversible transfers are
not stock-risk equivalents.

Crypto can introduce liquidation risk through leverage, margin, perpetuals,
borrowed collateral, volatile collateral values, and venue-specific margin
rules. Liquidation mechanics are not equivalent to stock stop-loss behavior.

Crypto has token-specific risk. Issuer concentration, protocol changes,
token unlocks, mint/burn mechanics, bridge exposure, governance changes,
oracle failures, smart-contract defects, and chain-specific failures can
change the risk profile independently of price action.

Crypto has stablecoin risk. Peg stability, issuer solvency, reserve quality,
redemption access, banking relationships, jurisdictional treatment, and
venue support can affect trading and custody assumptions.

Crypto carries regulatory uncertainty. Jurisdiction, asset classification,
exchange availability, tax treatment, compliance obligations, sanctions
screening, and platform restrictions may change without matching stock
market processes.

Because of these differences, stock-risk boundaries, stock-risk evidence,
stock execution assumptions, broker assumptions, market-hours assumptions,
and conventional position-sizing assumptions must not be reused as crypto
approval.

Treating crypto as a simple asset-class switch would collapse distinct risk
surfaces into an execution assumption. That posture is prohibited by this
review.

## Non-Authorization Statement

This review does not approve, authorize, enable, imply, or prepare:

* crypto trading
* crypto strategy execution
* exchange connectivity
* broker approval
* exchange approval
* broker/exchange approval
* order submission
* automated execution
* wallet handling
* custody handling
* private-key handling
* deposit or withdrawal handling
* leverage behavior
* margin behavior
* liquidation-risk controls
* position sizing
* trade sizing
* stablecoin handling
* token selection
* token approval
* market-making
* arbitrage
* DeFi interaction
* smart-contract interaction
* on-chain transaction behavior
* runtime trading changes
* broker integration
* exchange integration
* API key or secrets logic
* order-routing logic
* SniperBot runtime behavior
* EchoAuth runtime behavior
* NI-AI runtime behavior
* command execution
* deployment permission
* execution capability

No credential, API key, exchange account, broker account, wallet, private
key, custody path, deposit path, withdrawal path, order path, quote path,
trade path, strategy path, runtime path, automation path, command path, or
deployment path is created or implied.

No future task may cite this review as proof that crypto trading is ready,
safe, approved, partially approved, pre-approved, conditionally approved, or
awaiting only technical implementation.

## Crypto-Specific Risk Surfaces

Any future crypto capability, if ever separately approved for analysis,
would require explicit review of at least these risk surfaces:

* 24/7 market monitoring and no-action posture
* exchange fragmentation and venue-specific risk
* liquidity gaps, spread expansion, and slippage risk
* exchange outages, delistings, restrictions, and withdrawal limits
* custody, wallet, private-key, and transfer risk
* irreversible transaction and mistaken-address risk
* leverage, margin, collateral, and liquidation risk
* token-specific issuer, protocol, unlock, oracle, and bridge risk
* stablecoin peg, issuer, redemption, reserve, and venue-support risk
* regulatory, jurisdictional, sanctions, and platform-policy uncertainty
* market manipulation, wash trading, and unreliable volume risk
* chain congestion, network fees, finality, and settlement timing risk
* DeFi, smart-contract, approval, bridge, and oracle risk
* security risk around API keys, wallet approvals, secrets, and account
  takeover
* tax, reporting, auditability, and traceability requirements

Listing these risk surfaces is analysis only. It is not a runtime
specification, control design, implementation plan, approval checklist,
trading checklist, exchange checklist, custody checklist, order checklist,
or deployment checklist.

These surfaces are not acceptance criteria for activation. Satisfying,
discussing, or documenting any one surface would not authorize crypto
trading, exchange connectivity, wallet/custody handling, order submission,
position sizing, leverage, margin, liquidation controls, stablecoin
handling, token selection, market-making, arbitrage, DeFi interaction,
smart-contract interaction, or runtime trading changes.

## Required Future Approval Gates

Any future crypto work, if ever considered, must be handled in later
separate lanes with explicit approval for each layer.

At minimum, separate explicit approval would be required before any future
work on:

* crypto-risk taxonomy
* crypto evidence requirements
* crypto eligibility / exclusion
* token selection
* stablecoin handling
* exchange or broker selection
* exchange connectivity
* broker connectivity
* API key, secrets, and credential handling
* wallet and custody handling
* deposit and withdrawal handling
* market-data access
* quote handling
* order-routing design
* order submission
* trade-size and position-size logic
* leverage, margin, collateral, or liquidation controls
* DeFi or smart-contract interaction
* market-making or arbitrage
* paper-trading or simulation
* audit-log and traceability behavior
* human confirmation
* founder approval
* kill-switch and rollback behavior
* live-trading readiness
* deployment

Each future gate would require its own bounded task order, founder-selected
scope, review evidence, explicit non-authorization language where
applicable, and separate approval before implementation could be discussed.

No listed gate is approved by this review.

Future approval gates must be explicit, separate, and layer-specific. They
must not be inferred from this boundary review, bundled into a general
crypto approval, or satisfied by asset-class switch wording.

## Explicitly Out of Scope

The following are explicitly out of scope for this review:

* runtime code changes
* tests
* CI changes
* trading logic
* broker integration
* exchange integration
* API key or secrets logic
* order-routing logic
* order submission
* position-sizing runtime
* trade-size runtime
* wallet or custody logic
* asset-class runtime behavior
* crypto strategy logic
* crypto execution logic
* market-making logic
* arbitrage logic
* DeFi logic
* smart-contract logic
* stablecoin handling logic
* token-selection logic
* leverage or margin behavior
* liquidation-risk controls
* live trading
* paper trading
* simulation
* deployment
* README/index updates
* staging
* commit
* push

This file must not be used as a runbook, implementation plan, activation
plan, readiness approval, runtime specification, deployment checklist,
broker workflow, exchange workflow, wallet workflow, custody workflow,
order workflow, strategy workflow, automation workflow, or execution
workflow.

This file must also not be used to request, store, validate, rotate, or
operate broker credentials, exchange credentials, API keys, secrets, wallet
keys, wallet approvals, custody accounts, deposit addresses, withdrawal
addresses, or trading permissions.

## Governance Conclusion

The SniperBot crypto-risk boundary is defined as documentation-only,
governance-only, non-runtime, and non-execution.

Crypto risk is not stock risk. Crypto must not be treated as merely another
asset-class switch. Future crypto capability, if ever considered, requires
later separate approval gates for each layer before implementation can be
discussed.

This review preserves the EchoAuth / NI-AI principle that safety and
authority boundaries come before execution.

Analysis remains separated from activation.

No crypto readiness, crypto approval, broker approval, exchange approval,
wallet approval, custody approval, strategy approval, order authority,
position-sizing authority, trading authority, automation authority,
deployment permission, or execution capability is created by this review.

The only authorized outcome of this lane is a stronger written boundary:
analysis remains analysis, activation remains unapproved, and any future
crypto movement requires a later explicit approval gate before work begins.

Final status:

* Boundary defined
* Crypto-risk planning documented
* Crypto-specific risk surfaces documented as analysis only
* Implementation not authorized
* Runtime not authorized
* Execution not authorized
* README/index update not authorized
* Staging/commit/push not authorized
* Awaiting separate explicit approval for any future index update, staging,
  commit, push, implementation, or next lane
