# SniperBot Stage 2 Stock Deferral / No-Action Contract Definition Review

## Status and Boundary

Documentation-only / governance-only / contract-definition-only /
stock-specific / non-runtime / non-execution / non-authorizing.

Repository: `heliosfi/Echoauth-core`  
Starting checkpoint: `8f5f91737c58ec3777a4901c383a8dba1440587c`.

This review defines one proposed future contract for classifying externally
supplied stock-lane deferral and no-action facts. It does not create a schema,
implementation, test, approval, eligibility decision, market-data path, signal,
strategy, risk, sizing, order, broker, or execution behavior.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized. The
generic Asset-Class Deferral / No-Action evaluator and its accepted schema,
implementation, tests, and evidence acceptance remain unchanged.

## Exact Subject

The subject is **SniperBot Stage 2 — Stock Deferral / No-Action Decision
Contract**: a descriptive classifier for already supplied facts within an
identified stock lane indicating deferral, no action, missing or deficient
evidence, restriction, or required human/governance review.

It does not determine whether a security is a stock, calculate eligibility,
select a ticker, access prices or market data, calculate signals, authorize
trading, or place or modify an order.

## Separation from the Generic Asset-Class Subject

The generic Asset-Class Deferral / No-Action evaluator classifies externally
supplied asset-class-level facts, including a `STOCK` asset-class value. This
stock-specific subject would classify only externally supplied facts already
within the identified stock lane. Neither classifier calls or automatically
invokes the other; no orchestration or runtime integration is implied.

The generic result is contextual evidence only, never stock permission. Any
dependency ordering is descriptive: stock-lane confirmation and generic
asset-class context may be supplied before classification, but no classifier
executes the other or inherits its authority. Stock-specific semantics must
not be copied from the generic contract unless separately supported by founder
decisions.

## Proposed Immutable Inputs

The smallest future input set to be decided is:

* non-empty opaque stock/security reference;
* externally supplied stock-lane confirmation;
* stock-specific evidence present, current, sufficient, and contradictory
  indicators;
* externally supplied stock deferral condition;
* externally supplied stock no-action condition;
* externally supplied stock restriction, exclusion, or unavailability fact;
* optional contextual generic asset-class decision reference;
* optional contextual bounded EchoAuth authority evidence; and
* mandatory opaque correlation reference.

These are descriptive inputs only. No ticker validation, exchange lookup,
quote retrieval, market-hours logic, price threshold, volume, volatility,
indicator, fundamental, corporate-action, trade, or position fact is in scope.

## Proposed Descriptive Outputs

The smallest future output set is:

* stock-specific classification outcome;
* closed stock-specific reason code;
* RequiredAction;
* opaque stock/security reference; and
* exact correlation reference.

Outputs must not contain stock selection, eligibility approval, signal
direction, entry or exit price, quantity, risk allocation, order instructions,
broker actions, or executable commands.

## Fail-Closed Boundaries

Missing, stale, insufficient, or contradictory stock evidence; simultaneous
deferral and no-action; restriction or exclusion; absent or inconsistent
stock-lane confirmation; generic context not equal to `STOCK`; invalid, stale,
revoked, ambiguous, or out-of-scope authority; unknown raw values; undefined
typed combinations; and all ambiguity must remain non-permission and require
the future founder-defined fail-closed classification. No outcome may become
eligibility, permission, signal, or execution authority.

Externally supplied restriction or exclusion may be consumed only as a
descriptive fact. This subject does not calculate, validate, change, select, or
approve a security. It remains separate from both Stock Eligibility / Exclusion
and generic Asset-Class Eligibility / Exclusion.

## Locked Exclusions

This subject excludes quote retrieval, historical or real-time feeds,
bid/ask, OHLCV, volume, volatility, market or exchange status, corporate
actions, and data-provider integration. It also excludes bullish, bearish,
long, short, buy, sell, hold, or neutral signals; strategy rules; entry/exit;
risk limits; stop loss; take profit; position sizing; portfolio allocation;
backtesting; simulation; broker or Robinhood access; orders; credentials;
deployment; persistence; networking; runtime integration; FSM integration;
rollback/recovery; and execution.

EchoAuth remains the sole permission authority. Authority evidence is
contextual only unless a later founder decision says otherwise. Stock
classification cannot grant, repair, broaden, reinterpret, or bypass authority;
generic asset-class context cannot authorize stock activity or market-data
access.

## Founder Decisions Required Before Schema Definition

The following decisions remain unresolved and are not answered by this review:

1. Outcome vocabulary.
2. Stock-specific reason-code vocabulary.
3. RequiredAction vocabulary and subject-emittable values.
4. Meaning of stock-specific deferral.
5. Meaning of stock-specific no-action.
6. Meaning and treatment of supplied stock restriction or exclusion.
7. Relationship to the generic Asset-Class Deferral evaluator.
8. Whether generic asset-class context is required, optional, or prohibited.
9. Stock-lane confirmation requirements.
10. Deferral versus no-action conflict precedence.
11. Contradiction precedence.
12. Evidence precedence.
13. Authority-evidence treatment and sub-precedence.
14. Unknown and undefined input behavior.
15. Exact future schema, package, implementation, and test paths.
16. Validation and stop conditions.

These decisions must not be inferred from the generic evaluator, historical
records, CI, Slack, or implementation intent.

## Proposed Future File Boundaries

Only if separately approved, a future bounded task may consider one JSON
schema, one pure implementation, one direct test, and one package initializer
only if repository convention requires it. No such files are created or
authorized here.

## Readiness Conclusion

`STOCK DEFERRAL / NO-ACTION CONTRACT READY FOR FOUNDER DECISIONS`

The exact next step is a read-only founder decision sheet. Schema or
implementation must not begin automatically, and no next lane begins
automatically.
