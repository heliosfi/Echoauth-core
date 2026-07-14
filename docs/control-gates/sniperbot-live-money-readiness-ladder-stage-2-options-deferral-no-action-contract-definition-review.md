# SniperBot Stage 2 Options Deferral / No-Action Contract Definition Review

## Status and Boundary

Documentation-only / governance-only / contract-definition-only /
options-specific / non-runtime / non-execution / non-authorizing.

Repository: `heliosfi/Echoauth-core`
Starting checkpoint: `261600c8e93615b82488b31df6a07d23a9d45588`.

This review defines one proposed future contract for classifying externally
supplied options-lane deferral and no-action facts. It does not create a
schema, implementation, test, approval, eligibility decision, market-data
path, signal, strategy, risk, sizing, order, broker, or execution behavior.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized. The
accepted generic Asset-Class and Stock Deferral / No-Action evaluators remain
unchanged.

## Exact Subject

The subject is **SniperBot Stage 2 - Options Deferral / No-Action Decision
Contract**: a descriptive classifier for already supplied options-specific
facts indicating deferral, no action, missing or deficient evidence,
restriction or exclusion, lane-confirmation failure, incompatible context,
authority-evidence failure, or required human/governance review.

It does not determine whether an instrument is an option, select a contract,
calculate eligibility, inspect an options chain, access pricing or market
data, calculate signals, authorize trading, or place or modify an order.

## Separation from Existing Subjects

This subject is separate from the generic Asset-Class Deferral / No-Action
contract, which classifies asset-class facts, and from the Stock Deferral /
No-Action contract, which classifies facts already within a stock lane. It is
also separate from Options Eligibility / Exclusion. No classifier calls,
invokes, orchestrates, or inherits authority from another classifier.

Options-specific facts must not be copied into generic or stock semantics
without separate founder decisions. A generic context or another result may
be supplied only as opaque contextual evidence; it does not authorize or
select an options subject.

## Proposed Immutable Inputs

The smallest future input set to be decided is:

* a non-empty opaque options reference;
* externally supplied options-lane confirmation;
* options-specific evidence-present, current, sufficient, and contradictory
  indicators;
* externally supplied options deferral and no-action conditions;
* externally supplied restriction or exclusion fact;
* optional generic contextual evidence;
* optional bounded EchoAuth authority evidence; and
* a mandatory opaque correlation reference.

These are descriptive inputs only. No ticker, underlying, call/put,
strike, expiration, premium, Greeks, chain, quote, volatility, lifecycle,
exercise, assignment, position, or market-data field is invented or in scope.

## Proposed Descriptive Outputs

The smallest future output set is an options-specific outcome, closed
reason code, RequiredAction, the opaque options reference, and the exact
correlation reference. Outputs must not contain contract selection,
eligibility approval, signal direction, strategy, pricing, quantity, risk
allocation, order instructions, broker actions, or executable commands.

## Fail-Closed and Authority Boundaries

Unknown values, absent or inconsistent lane confirmation, incompatible
generic context, missing, stale, insufficient, or contradictory evidence,
restriction or exclusion, conflicting deferral and no-action, invalid or
out-of-scope authority evidence, undefined combinations, and all ambiguity
must fail closed under decisions still required below. No result may become
eligibility, permission, signal, or execution authority.

EchoAuth remains the sole permission authority. Authority evidence is
optional contextual input only. This subject must not call EchoAuth,
independently validate, repair, broaden, reinterpret, replace, or bypass
EchoAuth authority.

## Locked Exclusions

This subject excludes options-chain or other market-data access, quote or
pricing logic, exercise, assignment, expiration or lifecycle behavior,
strategy, signals, risk, sizing, portfolio allocation, simulation,
backtesting, broker or Robinhood access, orders, credentials, deployment,
persistence, networking, runtime integration, FSM integration, rollback,
recovery, automation, and execution. It does not calculate eligibility or
asset selection and it does not duplicate Options Eligibility / Exclusion.

## Founder Decisions Required Before Schema Definition

The following exactly seventeen decisions remain unresolved and are not
answered by this review:

1. Outcome vocabulary for the options-specific classifier.
2. Closed options-specific reason-code vocabulary.
3. RequiredAction vocabulary and subject-emittable values.
4. Meaning of an options-specific deferral condition.
5. Meaning of an options-specific no-action condition.
6. Meaning and treatment of supplied options restriction or exclusion.
7. Relationship to the generic Asset-Class Deferral / No-Action contract.
8. Relationship to the Stock Deferral / No-Action contract and other lanes.
9. Whether generic contextual evidence is required, optional, or prohibited.
10. Exact options-lane confirmation requirements.
11. Precedence between explicit deferral and explicit no-action.
12. Contradiction precedence and fail-closed mapping.
13. Evidence-presence, staleness, sufficiency, and deficiency precedence.
14. Optional authority treatment and authority-failure sub-precedence.
15. Unknown and undefined input behavior.
16. Exact future schema, package initializer, implementation, and test paths.
17. Required validation commands and stop conditions.

These decisions must not be inferred from generic or stock evaluators,
archived pseudocode, CI, Slack, logs, or implementation intent. The review
does not answer them and does not authorize their future implementation.

## Proposed Future File Boundaries

Only if separately approved, a future bounded task may consider one options
schema, an initializer only if repository convention requires it, one pure
implementation, and one direct test. Those paths and their exact vocabulary
remain founder decisions. No such files are created or authorized here.

## Validation and Next Step

Validation for this documentation-only lane is limited to confirming that
exactly these two documentation files change, the README entry appears once,
the options subject remains separate from generic and stock subjects, no code
or runtime authority is created, `git diff --check` passes, and the existing
contract and Authority Clarity validation passes.

The exact next step is a read-only Options Deferral / No-Action founder
decision sheet. No schema, implementation, integration, or neighboring lane
begins automatically.

`OPTIONS DEFERRAL / NO-ACTION CONTRACT READY FOR FOUNDER DECISIONS`
