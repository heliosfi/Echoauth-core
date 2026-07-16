# SniperBot Live-Money Readiness Ladder Stage 2 Stock Eligibility / Exclusion Founder-Decision Record

## Status and Boundary

Artifact type: **Founder-Decision Record**

Subject: **Stock Eligibility / Exclusion**

Stage: **SniperBot Live-Money Readiness Ladder - Stage 2**

Contract-definition review and starting checkpoint:
`59a57194112a7af5a745d9243bcf058b8d724fbc`.

Current posture: **All 20 Stock decision domains resolved; schema and
implementation not authorized.**

This record is documentation-only, governance-only,
founder-decision-record-only, non-runtime, non-execution, and
non-authorizing. It selects the exact future Stock Eligibility / Exclusion
contract semantics. It does not create or authorize a schema, Python module,
test, package export, dependency, workflow, validator, runtime hook,
integration surface, or acceptance artifact.

The selections below are made independently for Stock. Where a label or
pattern resembles an accepted neighboring lane, this record expressly adopts
it for the Stock subject on its own merits. Similarity is not inherited
authority, and no Options-specific symbol, count, vocabulary, precedence,
authority shape, or behavior applies unless selected here.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized.

## Decision 01 - Stock Subject and Non-Authorizing Meaning

The future contract classifies one caller-supplied opaque `stock_reference`
already presented within the Stock lane. The classifier does not determine
whether the reference identifies a stock, security, ticker, symbol, exchange
listing, or supported instrument. It never parses, normalizes, resolves,
validates, looks up, ranks, selects, or recommends the reference.

The exact posture meanings are:

* `ELIGIBLE`: the supplied Stock posture may continue only to further
  governed Stage 2 consideration. It is not approval, selection, safety,
  suitability, tradeability, routability, order authority, or execution
  authority.
* `EXCLUDED`: the caller supplied an exclusion posture. It is descriptive and
  is not a runtime blocklist, filter, rejection rule, or enforcement action.
* `RESTRICTED`: the caller supplied a restriction posture requiring human
  review. It is descriptive and is not a broker, account, trading, order, or
  execution restriction mechanism.
* `REVIEW_REQUIRED`: supplied facts do not support a terminal eligible,
  excluded, or restricted classification under the exact first-match order.

Absence of exclusion or restriction is never permission. The subject derives
only the deterministic relationships expressly recorded below among supplied
typed facts.

## Decision 02 - Exact Request Shape and Strict Boundary

The exact future immutable request type is `StockEligibilityRequest` with
fields in this order:

| Order | Field | Exact Python type | Default | Meaning |
| ---: | --- | --- | --- | --- |
| 1 | `stock_reference` | `str` | none | Opaque caller-identified Stock subject |
| 2 | `eligibility_evidence_present` | `bool` | none | Caller assertion that eligibility evidence exists |
| 3 | `eligibility_evidence_current` | `bool` | none | Caller assertion of currentness |
| 4 | `eligibility_evidence_sufficient` | `bool` | none | Caller assertion of sufficiency |
| 5 | `eligibility_evidence_contradictory` | `bool` | none | Caller assertion of contradiction |
| 6 | `stock_eligible` | `bool` | none | Supplied eligible posture |
| 7 | `stock_excluded` | `bool` | none | Supplied excluded posture |
| 8 | `stock_restricted` | `bool` | none | Supplied restricted posture |
| 9 | `eligibility_evidence_reference` | `str` | none | Opaque evidence reference |
| 10 | `correlation_reference` | `str` | none | Opaque traceability reference |
| 11 | `stock_lane_confirmation` | `StockLaneConfirmation | None` | `None` | Supplied Stock-lane confirmation; `None` means missing |
| 12 | `generic_asset_class_context` | `GenericAssetClassContext | None` | `None` | Optional generic context |
| 13 | `authority_evidence` | `AuthorityEvidence | None` | `None` | Optional contextual authority evidence |

The first ten fields are required and have no default. Only the final three
fields have the exact default `None`. No field has a default factory.

Runtime type rules are exact:

* every Boolean field requires `type(value) is bool`; integers and truthy or
  falsey substitutes are rejected;
* every enum field requires the exact enum type;
* nested objects require their exact dataclass type; dictionaries, subclasses,
  lookalikes, partial objects, and alternate representations are rejected;
* references require `type(value) is str`, at least one non-whitespace
  character, and exact preservation;
* references are never stripped, normalized, parsed, dereferenced, or looked
  up;
* missing required keywords and unexpected keywords raise `TypeError`;
* positional construction through `create_request` is unavailable because the
  function accepts keyword arguments only.

Omission and null rules are:

* omitted `stock_lane_confirmation` and explicit
  `stock_lane_confirmation=None` both mean missing lane confirmation;
* `generic_asset_class_context` and `authority_evidence` are optional by
  omission through `create_request`;
* explicit `generic_asset_class_context=None` and
  `authority_evidence=None` through `create_request` are rejected with
  `TypeError`;
* their dataclass defaults remain `None` to represent the already-constructed
  absence state;
* the future JSON Schema omits optional generic and authority properties
  rather than accepting JSON `null`;
* empty objects and empty or whitespace-only references are invalid.

No request field is added for an upstream decision, market snapshot, quote,
price, volume, spread, volatility, event, account, broker, order, or
execution fact.

## Decision 03 - Permitted Caller-Supplied Stock Evidence and Context

The request permits only:

* one opaque `stock_reference`;
* four caller-supplied eligibility-evidence quality Booleans;
* three caller-supplied posture Booleans;
* one opaque eligibility-evidence reference;
* one opaque correlation reference;
* optional Stock-lane confirmation;
* optional generic Asset-Class context; and
* optional contextual authority evidence.

The request expressly prohibits fields for:

* security type, ticker validation, symbol resolution, exchange, listing
  status, sector, industry, market capitalization, or price range;
* quote, OHLCV, order-book, bid/ask, volume, liquidity, spread, volatility, or
  market status;
* corporate action, filing, earnings, news event, halt, suspension, delisting,
  short interest, borrow risk, dividend, or split;
* watchlist, screen, ranking, score, signal, strategy, recommendation, entry,
  exit, risk, sizing, allocation, margin, collateral, buying power, or
  position;
* account permission, market-data subscription, broker, Robinhood, exchange,
  wallet, credential, order, route, transaction, execution, or runtime state.

Those facts belong to other separately governed subjects. The classifier may
not retrieve, calculate, infer, validate, enrich, refresh, or reinterpret
them.

## Decision 04 - Evidence Quality, Contradiction, and References

The exact evidence-quality dimensions are the four strict Booleans:

1. `eligibility_evidence_present`
2. `eligibility_evidence_current`
3. `eligibility_evidence_sufficient`
4. `eligibility_evidence_contradictory`

Currentness and sufficiency are supplied facts. The evaluator has no clock,
policy lookup, scoring logic, or external validation. Only
`eligibility_evidence_contradictory is True` establishes the highest-level
eligibility-evidence contradiction. No other contradiction is inferred except
the exact posture conflicts and undefined predicates separately recorded
below.

`eligibility_evidence_reference` is mandatory, non-empty,
non-whitespace-only, opaque, immutable, and preserved exactly in every
decision. Evidence absence does not permit omission of its reference; the
reference identifies the caller's evidence record or absence assertion.

The exact evidence-defect mappings, when no higher branch wins, are:

| Condition | Outcome | ReasonCode | RequiredAction |
| --- | --- | --- | --- |
| Evidence absent | `REVIEW_REQUIRED` | `STOCK_ELIGIBILITY_EVIDENCE_MISSING` | `HUMAN_REVIEW` |
| Evidence not current | `REVIEW_REQUIRED` | `STOCK_ELIGIBILITY_EVIDENCE_STALE` | `HUMAN_REVIEW` |
| Evidence insufficient | `REVIEW_REQUIRED` | `STOCK_ELIGIBILITY_EVIDENCE_INSUFFICIENT` | `HUMAN_REVIEW` |
| Evidence contradictory | `REVIEW_REQUIRED` | `STOCK_ELIGIBILITY_EVIDENCE_CONTRADICTORY` | `HUMAN_REVIEW` |

## Decision 05 - Posture Representation and Constructible Combinations

Eligible, excluded, and restricted are represented by the three strict
Booleans `stock_eligible`, `stock_excluded`, and `stock_restricted`. All eight
Boolean combinations are structurally constructible.

The posture results are:

* eligible only: `ELIGIBLE / STOCK_ELIGIBLE / NONE` after all higher and
  evidence-defect branches pass;
* excluded only: `EXCLUDED / STOCK_EXCLUDED / NONE`;
* restricted only: `RESTRICTED / STOCK_RESTRICTED / HUMAN_REVIEW`;
* excluded plus restricted with eligible false: exclusion wins;
* eligible plus excluded: governed conflict;
* eligible plus restricted with excluded false: governed conflict;
* all three true: eligible/excluded conflict wins;
* all three false: final unresolved fallback after all higher branches pass.

Excluded without eligible and restricted without eligible are ordinary
terminal postures, not undefined states. A posture does not require a separate
posture-specific reference beyond `eligibility_evidence_reference`.

## Decision 06 - Stock-Lane and Generic Asset-Class Context

### Stock-lane confirmation

The exact closed `StockLaneConfirmation` vocabulary is:

1. `CONFIRMED`
2. `NOT_CONFIRMED`
3. `CONTRADICTORY`

Missing lane confirmation is represented by `None`. It is never inferred from
`stock_reference`, generic context, a package path, or other data.

The exact lane mappings are:

| Condition | Outcome | ReasonCode | RequiredAction |
| --- | --- | --- | --- |
| Missing | `REVIEW_REQUIRED` | `STOCK_LANE_CONFIRMATION_MISSING` | `GOVERNANCE_REVIEW` |
| `CONTRADICTORY` | `REVIEW_REQUIRED` | `STOCK_LANE_CONTRADICTORY` | `GOVERNANCE_REVIEW` |
| `NOT_CONFIRMED` | `REVIEW_REQUIRED` | `STOCK_LANE_NOT_CONFIRMED` | `GOVERNANCE_REVIEW` |
| `CONFIRMED` | continue | none | none |

### Generic Asset-Class context

Generic context is optional by omission and contextual only. The exact frozen
`GenericAssetClassContext` fields, in order, are:

1. `asset_class: AssetClass`
2. `validity: Validity`
3. `current: bool`
4. `contradictory: bool`
5. `in_scope: bool`
6. `context_reference: str`

All six fields are required, have no defaults or default factories, and use
the same exact strict runtime and reference rules as the request.

The independently selected `AssetClass` vocabulary is:

* `STOCK`
* `OPTIONS`
* `CRYPTO`

The independently selected `Validity` vocabulary is:

* `VALID`
* `INVALID`
* `AMBIGUOUS`

Generic context subprecedence is exactly:

1. contradictory;
2. ambiguous;
3. invalid;
4. asset class other than `STOCK`;
5. stale;
6. out of scope.

The exact generic mappings are:

| Condition | Outcome | ReasonCode | RequiredAction |
| --- | --- | --- | --- |
| Contradictory | `REVIEW_REQUIRED` | `GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY` | `GOVERNANCE_REVIEW` |
| Ambiguous or invalid | `REVIEW_REQUIRED` | `GENERIC_ASSET_CLASS_CONTEXT_INVALID` | `GOVERNANCE_REVIEW` |
| Asset class is not `STOCK` | `REVIEW_REQUIRED` | `GENERIC_ASSET_CLASS_NOT_STOCK` | `GOVERNANCE_REVIEW` |
| Stale | `REVIEW_REQUIRED` | `GENERIC_ASSET_CLASS_CONTEXT_STALE` | `GOVERNANCE_REVIEW` |
| Out of scope | `REVIEW_REQUIRED` | `GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE` | `GOVERNANCE_REVIEW` |
| Fully valid Stock context | continue | none | none |

Absent generic context also continues. Neither absence nor valid context
grants eligibility. No generic evaluator is invoked, and no generic outcome is
consumed.

## Decision 07 - Authority Evidence and Subprecedence

Stock independently selects contextual authority evidence because it permits a
closed fail-closed description of supplied EchoAuth posture. The selection is
Stock-specific and does not inherit Options authority.

The exact frozen `AuthorityEvidence` fields, in order, are:

1. `validity: Validity`
2. `current: bool`
3. `revoked: bool`
4. `contradictory: bool`
5. `in_scope: bool`
6. `evidence_reference: str`

All six fields are required and have no defaults or default factories. The
four Boolean fields require exact `bool`. `validity` requires the exact
`Validity` enum. `evidence_reference` is non-empty, non-whitespace-only,
opaque, and preserved inside the supplied frozen object without lookup or
normalization.

The typed boundary rejects dictionaries, empty objects, partial objects,
arbitrary objects, subclasses, lookalikes, alternate objects, and
Deferral-shaped objects using `currentness`, `revocation`, `scope`, or other
field names.

Authority is optional by omission through `create_request`. Explicit
`authority_evidence=None` through `create_request` is rejected. Absent
authority and fully valid authority both allow evaluation to continue; neither
grants eligibility or permission.

The exact authority subprecedence is:

1. contradictory;
2. ambiguous;
3. invalid;
4. revoked;
5. stale;
6. out of scope.

Authority mappings are:

| Condition | Outcome | ReasonCode | RequiredAction |
| --- | --- | --- | --- |
| Contradictory, ambiguous, or invalid | `REVIEW_REQUIRED` | `AUTHORITY_EVIDENCE_INVALID` | `GOVERNANCE_REVIEW` |
| Revoked | `REVIEW_REQUIRED` | `AUTHORITY_EVIDENCE_REVOKED` | `GOVERNANCE_REVIEW` |
| Stale | `REVIEW_REQUIRED` | `AUTHORITY_EVIDENCE_STALE` | `GOVERNANCE_REVIEW` |
| Out of scope | `REVIEW_REQUIRED` | `AUTHORITY_EVIDENCE_OUT_OF_SCOPE` | `GOVERNANCE_REVIEW` |
| Fully valid | continue | none | none |

EchoAuth is never called. Evidence cannot create, repair, reinterpret, broaden,
bypass, replace, or exercise authority.

## Decision 08 - Closed Outcomes

The exact closed `Outcome` vocabulary contains four Stock-selected values:

1. `ELIGIBLE`
2. `EXCLUDED`
3. `RESTRICTED`
4. `REVIEW_REQUIRED`

`REVIEW_REQUIRED` is the fail-closed outcome for contradiction, conflict,
undefined state, lane failure, generic-context failure, authority failure,
evidence deficiency, and unresolved fallback. No alias, unknown value,
free-text outcome, `ALLOW`, `DENY`, trade direction, or execution outcome is
authorized.

## Decision 09 - Closed Stock Reason Codes

The exact closed `ReasonCode` vocabulary contains 23 values:

1. `STOCK_ELIGIBLE`
2. `STOCK_EXCLUDED`
3. `STOCK_RESTRICTED`
4. `STOCK_ELIGIBILITY_EVIDENCE_MISSING`
5. `STOCK_ELIGIBILITY_EVIDENCE_STALE`
6. `STOCK_ELIGIBILITY_EVIDENCE_INSUFFICIENT`
7. `STOCK_ELIGIBILITY_EVIDENCE_CONTRADICTORY`
8. `STOCK_ELIGIBLE_EXCLUDED_CONFLICT`
9. `STOCK_ELIGIBLE_RESTRICTED_CONFLICT`
10. `STOCK_LANE_CONFIRMATION_MISSING`
11. `STOCK_LANE_NOT_CONFIRMED`
12. `STOCK_LANE_CONTRADICTORY`
13. `GENERIC_ASSET_CLASS_CONTEXT_INVALID`
14. `GENERIC_ASSET_CLASS_CONTEXT_STALE`
15. `GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY`
16. `GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE`
17. `GENERIC_ASSET_CLASS_NOT_STOCK`
18. `AUTHORITY_EVIDENCE_INVALID`
19. `AUTHORITY_EVIDENCE_STALE`
20. `AUTHORITY_EVIDENCE_REVOKED`
21. `AUTHORITY_EVIDENCE_OUT_OF_SCOPE`
22. `UNDEFINED_INPUT_COMBINATION`
23. `STOCK_ELIGIBILITY_UNRESOLVED`

These labels are selected expressly for Stock. Options-specific posture or
evidence reasons, generic `ASSET_CLASS_*` posture reasons, Deferral /
No-Action reasons, aliases, unknown values, free text, and hidden catch-all
reasons are prohibited.

Every reason maps to exactly one outcome and action under the branch table
below. Ambiguous and invalid validity values intentionally share their
corresponding `*_INVALID` reason; they remain distinct conditions in
subprecedence evidence.

## Decision 10 - Required Actions and Emittable Subset

Stock independently selects the exact closed `RequiredAction` vocabulary:

1. `NONE`
2. `HUMAN_REVIEW`
3. `GOVERNANCE_REVIEW`
4. `FOUNDER_AUTHORITY_REQUIRED`
5. `RESET_REQUIRED`

Only these three values are emittable:

1. `NONE`
2. `HUMAN_REVIEW`
3. `GOVERNANCE_REVIEW`

`FOUNDER_AUTHORITY_REQUIRED` and `RESET_REQUIRED` remain vocabulary-only.
`Decision` rejects either with `ValueError`. No public
`EmittableAction` or `EmittableReasonCode` symbol is authorized.

No action creates runtime work, founder approval, permission, market-data
access, broker activity, order handling, or execution.

## Decision 11 - Contradictions and Constructible Collisions

The exact posture-conflict mappings are:

| Collision | Outcome | ReasonCode | RequiredAction |
| --- | --- | --- | --- |
| Eligible and excluded | `REVIEW_REQUIRED` | `STOCK_ELIGIBLE_EXCLUDED_CONFLICT` | `GOVERNANCE_REVIEW` |
| Eligible and restricted, with excluded false | `RESTRICTED` | `STOCK_ELIGIBLE_RESTRICTED_CONFLICT` | `HUMAN_REVIEW` |
| Excluded and restricted, with eligible false | `EXCLUDED` | `STOCK_EXCLUDED` | `NONE` |
| Eligible, excluded, and restricted | `REVIEW_REQUIRED` | `STOCK_ELIGIBLE_EXCLUDED_CONFLICT` | `GOVERNANCE_REVIEW` |

Eligibility-evidence contradiction precedes every posture collision. The
eligible/excluded conflict precedes the eligible/restricted conflict.
Eligible/excluded therefore wins the all-three collision. Exclusion precedes
restriction for the excluded/restricted pair.

Only logically constructible collisions require evidence. A single Boolean
cannot be both true and false; `VALID`, `INVALID`, and `AMBIGUOUS` cannot
coexist in one enum field; omitted and supplied cannot coexist; and null and a
typed object cannot coexist in one field.

Lane confirmation has one enum value or `None`, so lane failures do not
collide with one another. Generic and authority objects can contain multiple
independent failure facts, and their separately recorded subprecedence governs
those collisions.

## Decision 12 - Governed Undefined States and Fallback

Exactly three evidence-quality predicates are governed as undefined:

1. `not eligibility_evidence_present and eligibility_evidence_current`
2. `not eligibility_evidence_present and eligibility_evidence_sufficient`
3. `not eligibility_evidence_current and eligibility_evidence_sufficient`

If any predicate is true after higher contradiction and posture-conflict
branches, the exact mapping is:

* Outcome: `REVIEW_REQUIRED`
* ReasonCode: `UNDEFINED_INPUT_COMBINATION`
* RequiredAction: `GOVERNANCE_REVIEW`

No fourth undefined predicate is selected. Excluded-without-eligible and
restricted-without-eligible are ordinary postures.

The final fallback applies only after all other branches pass and
`stock_eligible is False`. It maps to:

* Outcome: `REVIEW_REQUIRED`
* ReasonCode: `STOCK_ELIGIBILITY_UNRESOLVED`
* RequiredAction: `GOVERNANCE_REVIEW`

Every well-formed typed request therefore produces exactly one decision.

## Decision 13 - Complete Deterministic First-Match Precedence

The exact Stock first-match order has 16 top-level steps:

| Precedence | Trigger | Outcome | ReasonCode | RequiredAction |
| ---: | --- | --- | --- | --- |
| 1 | Eligibility evidence contradictory | `REVIEW_REQUIRED` | `STOCK_ELIGIBILITY_EVIDENCE_CONTRADICTORY` | `HUMAN_REVIEW` |
| 2 | Eligible and excluded | `REVIEW_REQUIRED` | `STOCK_ELIGIBLE_EXCLUDED_CONFLICT` | `GOVERNANCE_REVIEW` |
| 3 | Eligible and restricted | `RESTRICTED` | `STOCK_ELIGIBLE_RESTRICTED_CONFLICT` | `HUMAN_REVIEW` |
| 4 | Any governed undefined predicate | `REVIEW_REQUIRED` | `UNDEFINED_INPUT_COMBINATION` | `GOVERNANCE_REVIEW` |
| 5 | Stock-lane confirmation missing | `REVIEW_REQUIRED` | `STOCK_LANE_CONFIRMATION_MISSING` | `GOVERNANCE_REVIEW` |
| 6 | Stock-lane confirmation contradictory | `REVIEW_REQUIRED` | `STOCK_LANE_CONTRADICTORY` | `GOVERNANCE_REVIEW` |
| 7 | Stock lane not confirmed | `REVIEW_REQUIRED` | `STOCK_LANE_NOT_CONFIRMED` | `GOVERNANCE_REVIEW` |
| 8 | Generic Asset-Class context failure | `REVIEW_REQUIRED` | Exact generic reason | `GOVERNANCE_REVIEW` |
| 9 | Stock excluded | `EXCLUDED` | `STOCK_EXCLUDED` | `NONE` |
| 10 | Stock restricted | `RESTRICTED` | `STOCK_RESTRICTED` | `HUMAN_REVIEW` |
| 11 | Authority failure | `REVIEW_REQUIRED` | Exact authority reason | `GOVERNANCE_REVIEW` |
| 12 | Eligibility evidence missing | `REVIEW_REQUIRED` | `STOCK_ELIGIBILITY_EVIDENCE_MISSING` | `HUMAN_REVIEW` |
| 13 | Eligibility evidence stale | `REVIEW_REQUIRED` | `STOCK_ELIGIBILITY_EVIDENCE_STALE` | `HUMAN_REVIEW` |
| 14 | Eligibility evidence insufficient | `REVIEW_REQUIRED` | `STOCK_ELIGIBILITY_EVIDENCE_INSUFFICIENT` | `HUMAN_REVIEW` |
| 15 | Stock eligible | `ELIGIBLE` | `STOCK_ELIGIBLE` | `NONE` |
| 16 | Otherwise unresolved | `REVIEW_REQUIRED` | `STOCK_ELIGIBILITY_UNRESOLVED` | `GOVERNANCE_REVIEW` |

Step 8 uses the six-step generic subprecedence in Decision 06. Step 11 uses
the six-step authority subprecedence in Decision 07. Evidence-quality
precedence at steps 12 through 14 is missing, then stale, then insufficient.

Exclusion and restriction intentionally precede authority and ordinary
evidence deficiencies because they are terminal caller-supplied governance
postures. They do not override contradiction, conflicts, undefined states, or
lane and generic-context failures.

This 16-step order is selected independently for Stock and does not inherit
the Options order.

## Decision 14 - Immutable Decision and Reference Preservation

The exact future frozen `Decision` fields, in order, are:

1. `outcome: Outcome`
2. `reason_code: ReasonCode`
3. `required_action: RequiredAction`
4. `stock_reference: str`
5. `eligibility_evidence_reference: str`
6. `correlation_reference: str`

All six fields are required and have no defaults or default factories.
`Decision` accepts only exact enum types and the emittable action subset.

Every decision preserves `stock_reference`,
`eligibility_evidence_reference`, and `correlation_reference` exactly.
Generic-context and authority evidence references remain inside their
caller-supplied input objects; they are not copied into the decision. No
upstream decision reference exists.

Evaluation never returns the request or a nested input object by identity.
Repeated evaluation of the same request produces decisions that are equal by
value and distinct by object identity.

## Decision 15 - Future JSON Schema and Parity

The exact future schema path is:

`schemas/sniperbot-stock-eligibility-exclusion-decision.schema.json`

The schema must use JSON Schema draft 2020-12 and an exact repository-local
`$id` derived from that filename. Its root object requires exactly `request`
and `decision` and sets `additionalProperties: false`.

Every object definition sets `additionalProperties: false`. Required arrays,
property order, enum values, reference patterns, and object shapes must match
this record exactly.

The request schema requires the first ten request fields. These properties are
optional:

* `stock_lane_confirmation`, represented by the closed enum or JSON `null`;
* `generic_asset_class_context`, represented only by its object and never
  JSON `null`; and
* `authority_evidence`, represented only by its object and never JSON `null`.

Omitted and explicit-null lane confirmation both represent the missing lane
state. Generic context and authority evidence use omission only.

References require a string with at least one non-whitespace character and
are not normalized. Booleans use JSON Boolean types. Closed enum values have
no aliases.

The schema describes data shape only. It must not encode evaluator
precedence, market interpretation, selection, authority creation, integration,
or execution behavior.

Schema/API parity must prove:

* every closed vocabulary and exact order;
* request, nested-context, authority, and decision fields;
* requiredness, defaults, omission, null, and additional-property behavior;
* exact reference constraints;
* strict Boolean and nested-object boundaries;
* emittable RequiredAction restriction; and
* preservation of the accepted Stock Deferral schema and API.

This record does not authorize creating the schema.

## Decision 16 - Future Python Module, API, and Package Coexistence

The exact future production module is:

`sniperbot.stock.eligibility_decision`

The exact source path is:

`src/sniperbot/stock/eligibility_decision.py`

The exact public API contains 12 symbols in this exact `__all__` order:

1. `AssetClass`
2. `AuthorityEvidence`
3. `Decision`
4. `GenericAssetClassContext`
5. `Outcome`
6. `ReasonCode`
7. `RequiredAction`
8. `StockEligibilityRequest`
9. `StockLaneConfirmation`
10. `Validity`
11. `create_request`
12. `evaluate`

No alias, `EmittableAction`, `EmittableReasonCode`, helper, or additional
public symbol is authorized.

The six exact string enums are:

1. `AssetClass`
2. `Outcome`
3. `ReasonCode`
4. `RequiredAction`
5. `StockLaneConfirmation`
6. `Validity`

The four exact frozen dataclasses are:

1. `GenericAssetClassContext`
2. `AuthorityEvidence`
3. `StockEligibilityRequest`
4. `Decision`

No `slots` requirement is selected. No mutable dataclass, named tuple,
dictionary contract, inheritance hierarchy, protocol, or third-party model is
authorized.

The public functions are exactly:

```python
def create_request(**values: object) -> StockEligibilityRequest:
```

```python
def evaluate(request: StockEligibilityRequest) -> Decision:
```

`create_request` performs strict typed construction without coercion or
evaluation. `evaluate` accepts only
`type(request) is StockEligibilityRequest`.

The existing `src/sniperbot/stock/__init__.py` remains unchanged. The new
symbols are not re-exported at `sniperbot.stock` because its accepted generic
names belong to Stock Deferral / No-Action and would collide. Callers must use
the eligibility submodule explicitly. Stock Deferral source, schema, tests,
exports, behavior, and acceptance remain unchanged.

Production imports are limited to:

```python
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
```

No import from Stock Deferral, Asset-Class Eligibility, Options Eligibility,
EchoAuth runtime, or any other evaluator is authorized.

This record defines a future API contract only. It does not authorize the
module or any package change.

## Decision 17 - Exceptions and Strict Runtime Types

`TypeError` is required for:

* wrong runtime types;
* raw strings supplied where exact enums are required;
* integers or other values supplied for Boolean fields;
* dictionaries, subclasses, lookalikes, partial objects, and alternate nested
  representations;
* Deferral-shaped authority or context objects;
* explicit `generic_asset_class_context=None` or
  `authority_evidence=None` through `create_request`;
* missing required request keywords;
* unexpected request keywords;
* positional arguments to `create_request`; and
* any evaluation input whose exact type is not `StockEligibilityRequest`.

`ValueError` is required for:

* empty or whitespace-only required references;
* a `Decision` containing `FOUNDER_AUTHORITY_REQUIRED` or
  `RESET_REQUIRED`;
* correctly typed values violating an exact closed decision-only boundary;
  and
* unknown raw values passed to an enum constructor at the enum-construction
  boundary.

`stock_lane_confirmation=None` is valid and means missing confirmation.
Well-formed `StockEligibilityRequest` evaluation does not raise; it always
returns one `Decision`. No custom exception, `AssertionError` validation,
implicit conversion, normalization, warning, logging fallback, or silent
repair is authorized. Exception message text is not contractual, but exception
type and triggering boundary are contractual.

## Decision 18 - Purity, Determinism, Non-Mutation, and Prohibited Capabilities

Evaluation is a total deterministic function over the approved typed request
space. Requests, nested contexts, authority evidence, and decisions are
frozen. Evaluation does not mutate caller-owned objects, references, globals,
or any accepted Stock Deferral object.

The future module prohibits:

* filesystem and environment access;
* networking, sockets, HTTP, subprocesses, and inter-process communication;
* logging, telemetry, persistence, databases, files, queues, caches, and
  registration;
* time, clocks, randomness, nondeterminism, mutable global state, memoization,
  and import-time side effects;
* services, workers, schedulers, event publication, runtime invocation,
  evaluator chaining, orchestration, integration, FSM transitions, rollback,
  and EchoAuth runtime calls;
* market data, quotes, OHLCV, prices, order books, bid/ask, volume, liquidity,
  spread, volatility, news, filings, events, halts, suspensions, and
  corporate-action access;
* ticker validation, symbol resolution, security selection, screen, watchlist,
  ranking, recommendation, signals, strategy, risk, sizing, allocation,
  margin, collateral, buying power, and portfolio behavior;
* broker, Robinhood, exchange, account, wallet, custody, credential, secret,
  subscription, order, route, transaction, trading, execution, deployment,
  or live-money behavior;
* third-party dependencies.

Only the three standard-library imports selected in Decision 16 are permitted.

## Decision 19 - Direct-Test and Exhaustive-Evidence Requirements

The exact future direct-test path is:

`tests/test_sniperbot_stock_eligibility_exclusion.py`

Focused direct tests must prove:

* exact 12-symbol public API and `__all__` order;
* all six closed enums and exact values;
* all four frozen dataclasses, field order, annotations, defaults, absence of
  default factories, equality, and immutability;
* exact function signatures;
* all strict Boolean, enum, reference, nested-object, omission, explicit-null,
  missing-keyword, extra-keyword, alternate-object, subclass, lookalike, and
  Deferral-shaped rejection boundaries;
* all 16 top-level precedence branches independently;
* exact outcome/reason/action mapping for every branch;
* all eight posture combinations and all-three precedence;
* all three governed undefined predicates and final fallback independently;
* all Stock-lane states and generic-context states;
* generic-context six-step subprecedence with all 14 logically possible
  pairwise collision witnesses;
* authority six-step subprecedence with all 14 logically possible pairwise
  collision witnesses;
* independent out-of-scope generic and authority outcomes;
* absence and fully valid generic and authority context continuing without
  granting eligibility;
* `FOUNDER_AUTHORITY_REQUIRED` and `RESET_REQUIRED` never emitted and rejected
  by `Decision`;
* exact decision reference preservation;
* generic-context and authority-reference non-mutation;
* request and caller-object non-mutation;
* equal-by-value but distinct repeated decisions;
* schema/API parity;
* package-root exports unchanged;
* production import restrictions and absence of prohibited capabilities.

The exhaustive deterministic audit uses this exact finite representative
model:

* 16 combinations of the four eligibility-evidence Booleans;
* 8 combinations of the three posture Booleans;
* 4 lane states: missing, confirmed, not confirmed, contradictory;
* 8 generic-context representatives: absent, fully valid, contradictory,
  ambiguous, invalid, non-Stock, stale, out of scope; and
* 8 authority representatives: absent, fully valid, contradictory, ambiguous,
  invalid, revoked, stale, out of scope.

The required audit total is:

`16 x 8 x 4 x 8 x 8 = 32,768 combinations`

All 32,768 combinations must produce the exact result predicted by an
independent oracle. Multi-failure generic and authority collision witnesses
are tested separately because the representative audit states isolate one
failure at a time.

If independent verification finds missing direct evidence, only a separate
founder-authorized bounded test-evidence completion may close the gap.

## Decision 20 - Validation, Independent Verification, Acceptance, and Stops

Every future schema, implementation, evidence-completion, and acceptance step
requires its own explicit bounded founder task order.

Future validation must include, as applicable:

* documentation and content guards;
* JSON Schema draft validation and parse;
* exact schema/API structural and vocabulary parity;
* focused Stock Eligibility / Exclusion direct tests;
* Contract Validation;
* Contract and Authority Clarity tests;
* Explicit Authority Clarity Validator;
* canonical full suite;
* exact public API, package-boundary, import, dependency, side-effect, and
  prohibited-capability scans;
* exact changed-file and commit-scope review;
* final newline, whitespace, and `git diff --check`;
* clean synchronized repository state, zero locks, and divergence `0/0`
  before and after publication.

After implementation, an independent read-only implementation-evidence review
must verify the contract, schema, production module, direct tests, exhaustive
audit, purity, non-mutation, package coexistence, and capability restrictions.
Implementation alone is not acceptance.

If independent review identifies an evidence gap, the gap must be named
exactly and closed only through a separate bounded founder authorization.

Formal implementation-evidence acceptance requires its own separately
authorized documentation artifact recording:

* contract-definition, founder-decision, schema, implementation, and any
  direct-test evidence-completion commit provenance;
* exact implementation and test scope;
* focused, governing-validator, exhaustive-audit, and canonical-suite results;
* independent verification findings and closure of any evidence gap;
* clean synchronized repository evidence; and
* explicit non-authorization of runtime, integration, orchestration,
  market-data, broker, wallet, networking, persistence, registration, order,
  execution, and Stage 3.

Work must stop on:

* an unresolved or contradictory contract selection;
* vocabulary, fields, defaults, null handling, precedence, mappings,
  authority, API, exceptions, or evidence behavior not stated here;
* implicit inheritance from Options or another lane;
* any modification to accepted Stock Deferral / No-Action;
* schema/API drift or package-root export expansion;
* failed test, validation, parity, scope, whitespace, import, purity, or
  prohibited-capability check;
* unexpected files, dependencies, workflows, configuration, validators,
  archives, or generated artifacts;
* evaluator invocation, integration, orchestration, market-data, broker,
  wallet, networking, persistence, registration, order, trading, execution,
  runtime, deployment, or Stage 3 movement.

## Exact Closed Vocabularies

### AssetClass - 3

* `STOCK`
* `OPTIONS`
* `CRYPTO`

### StockLaneConfirmation - 3

* `CONFIRMED`
* `NOT_CONFIRMED`
* `CONTRADICTORY`

### Validity - 3

* `VALID`
* `INVALID`
* `AMBIGUOUS`

### Outcome - 4

* `ELIGIBLE`
* `EXCLUDED`
* `RESTRICTED`
* `REVIEW_REQUIRED`

### ReasonCode - 23

* `STOCK_ELIGIBLE`
* `STOCK_EXCLUDED`
* `STOCK_RESTRICTED`
* `STOCK_ELIGIBILITY_EVIDENCE_MISSING`
* `STOCK_ELIGIBILITY_EVIDENCE_STALE`
* `STOCK_ELIGIBILITY_EVIDENCE_INSUFFICIENT`
* `STOCK_ELIGIBILITY_EVIDENCE_CONTRADICTORY`
* `STOCK_ELIGIBLE_EXCLUDED_CONFLICT`
* `STOCK_ELIGIBLE_RESTRICTED_CONFLICT`
* `STOCK_LANE_CONFIRMATION_MISSING`
* `STOCK_LANE_NOT_CONFIRMED`
* `STOCK_LANE_CONTRADICTORY`
* `GENERIC_ASSET_CLASS_CONTEXT_INVALID`
* `GENERIC_ASSET_CLASS_CONTEXT_STALE`
* `GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY`
* `GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE`
* `GENERIC_ASSET_CLASS_NOT_STOCK`
* `AUTHORITY_EVIDENCE_INVALID`
* `AUTHORITY_EVIDENCE_STALE`
* `AUTHORITY_EVIDENCE_REVOKED`
* `AUTHORITY_EVIDENCE_OUT_OF_SCOPE`
* `UNDEFINED_INPUT_COMBINATION`
* `STOCK_ELIGIBILITY_UNRESOLVED`

### RequiredAction - 5

* `NONE`
* `HUMAN_REVIEW`
* `GOVERNANCE_REVIEW`
* `FOUNDER_AUTHORITY_REQUIRED`
* `RESET_REQUIRED`

### Emittable RequiredAction subset - 3

* `NONE`
* `HUMAN_REVIEW`
* `GOVERNANCE_REVIEW`

## Future Governed Paths - Not Authorized for Creation

### Schema

`schemas/sniperbot-stock-eligibility-exclusion-decision.schema.json`

### Production module

`src/sniperbot/stock/eligibility_decision.py`

### Direct tests

`tests/test_sniperbot_stock_eligibility_exclusion.py`

### Implementation-evidence acceptance

`docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-stock-eligibility-exclusion-implementation-evidence-acceptance.md`

The existing `src/sniperbot/stock/__init__.py` is not a future changed path
under this contract. Every listed future artifact requires separate founder
authorization.

## Decision Boundary and Next Founder Decision

These 20 Stock-specific decisions close the founder-decision surface only.
They establish the exact future descriptive contract, closed vocabularies,
request and decision structures, 16-step precedence, generic and authority
subprecedence, 12-symbol submodule API, purity constraints, exhaustive
32,768-combination evidence requirement, governed paths, and stopping
conditions.

This record creates no schema, source, test, package export, dependency,
workflow, validator, runtime, integration, orchestration, market-data, broker,
wallet, networking, persistence, registration, order, trading, execution,
deployment, live-money, or Stage 3 authority.

The exact next founder decision, if any, is whether to authorize a separate
bounded schema-only task order for the Stock Eligibility / Exclusion contract.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized.
