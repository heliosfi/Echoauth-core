# SniperBot Live-Money Readiness Ladder Stage 2 Stock Eligibility / Exclusion Contract-Definition Review

## Status and Boundary

Artifact type: **Contract-Definition Review**

Subject: **Stock Eligibility / Exclusion**

Stage: **SniperBot Live-Money Readiness Ladder - Stage 2**

Governing boundary:
`docs/control-gates/sniperbot-stock-eligibility-exclusion-boundary-review.md`.

Starting checkpoint:
`7ee771ba57a29e706291c44a61401612bc8ba742`.

Current readiness: **Contract-definition decision surface documented; founder
decisions not yet made.**

This record is documentation-only, governance-only, contract-definition-only,
non-runtime, non-execution, and non-authorizing. It defines the boundary of one
possible future Stock Eligibility / Exclusion decision contract. It does not
approve any request shape, evidence model, vocabulary, precedence, authority
representation, schema, Python API, implementation, test, integration, or
acceptance artifact.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized.

## Governing Sequence

The accepted Options Eligibility / Exclusion lane is complete and indexed. The
governing same-family sequence places Stock after Options and Crypto after
Stock. That ordering identifies the subject of this record; it does not grant
implementation authority or authorize Crypto work.

The Stock Eligibility / Exclusion boundary review already establishes that
eligibility is governance analysis rather than stock approval, and exclusion
is governance analysis rather than runtime blocking. This record narrows that
boundary into a complete founder-decision surface without answering it.

## Exact Bounded Subject

The proposed subject is one pure descriptive classification of
caller-supplied Stock eligibility and exclusion facts. Whether it describes an
identified stock lane, an individual caller-supplied security reference, or
another bounded Stock subject remains a founder decision.

A future contract may classify only facts supplied by its caller. It must not:

* discover, choose, rank, recommend, screen, or approve a stock;
* decide whether a symbol represents a supported security;
* retrieve or validate a ticker, exchange, quote, price, volume, spread,
  volatility, corporate action, filing, earnings event, halt, suspension, or
  delisting condition;
* infer eligibility, exclusion, restriction, authority, or evidence quality
  from external systems;
* interpret absence of exclusion as permission; or
* create a trade, order, route, transaction, execution, or runtime action.

Any future eligible result may mean only continued governed Stage 2
consideration under an exact meaning selected by the founder. It must never
mean approved, selected, recommended, safe, tradeable, routable, executable,
or authorized for live money.

## Explicit Non-Authorizing Purpose

The only purpose considered here is deterministic description of supplied
governance posture. Eligibility cannot grant authority. Exclusion cannot
become an executable blocklist, filter, or order-rejection rule. Restriction,
if the founder includes it, cannot become a broker, account, trading, or
execution restriction mechanism.

EchoAuth remains the sole owner of permission authority. No Stock classifier
may create, repair, reinterpret, broaden, bypass, replace, or exercise
authority. Contextual authority evidence, if later approved, may describe
supplied authority posture only.

## Locked Capability Exclusions

This subject excludes:

* asset-class selection and stock selection;
* ticker, symbol, security, exchange, sector, industry, market-cap, screen, and
  watchlist selection;
* market-data, quote, pricing, OHLCV, order-book, bid/ask, volume, liquidity,
  spread, volatility, news, filing, earnings, corporate-action, halt,
  suspension, and delisting access or calculation;
* signals, strategy, forecasting, ranking, scoring, recommendations, entries,
  exits, risk limits, stop loss, take profit, sizing, allocation, margin,
  collateral, buying power, and portfolio behavior;
* broker, Robinhood, exchange, wallet, custody, account, credential, secret,
  subscription, and permission access;
* orders, routing, registration, transactions, execution, deployment,
  networking, persistence, caching, services, workers, schedulers, and runtime
  wiring;
* evaluator invocation, chaining, orchestration, integration, event
  publication, state transition, rollback invocation, or command execution;
* paper trading, simulation, replay, backtesting, live trading, live-money
  behavior, or Stage 3 movement.

No excluded capability is prepared, partially approved, implied, or made
ready by this review.

## Separation From Adjacent Subjects

### Stock Deferral / No-Action

The accepted Stock Deferral / No-Action lane remains unchanged and coexists as
a separate semantic subject. Deferral / No-Action classifies whether supplied
facts require deferral or no action. Stock Eligibility / Exclusion would
describe an eligibility posture only.

Neither subject invokes, overrides, chains to, controls, or inherits
permission from the other. Existing `sniperbot.stock` package exports belong
to the accepted Stock Deferral / No-Action contract. This record does not
modify them, reserve new root exports, or decide how a future eligibility API
would avoid name or export collisions.

### Asset-Class Eligibility / Exclusion

Generic Asset-Class Eligibility / Exclusion may be considered only as
caller-supplied context if a future founder decision approves it. The Stock
subject must not invoke that evaluator, infer Stock identity from it, inherit
its outcome, or convert generic eligibility into stock approval.

### Options Eligibility / Exclusion

The Options lane supplies historical governance evidence only. Its API,
fields, enums, dataclasses, precedence, undefined predicates, authority
representation, mappings, tests, and evidence counts are not Stock decisions.

### Stock Risk and Other Stock Lanes

Stock risk, trade size, position size, max loss, account posture, broker
compatibility, market data, strategy, order routing, and execution remain
separate subjects. Evidence from another lane cannot become Stock eligibility
or exclusion authority.

### Crypto Eligibility / Exclusion

Crypto remains a later separate subject. This record neither opens nor defines
that lane.

## Stock Fact Boundary

The Stock boundary review identifies possible future analysis involving
symbol or ticker relationships, security type, listing venue, sector and
industry, market capitalization, liquidity and volume, spread, volatility,
price range, corporate actions, earnings or news events, halts, suspensions,
delisting, short interest, borrow risk, dividends, splits, watchlists,
screens, account posture, and related evidence.

This record does not adopt any of those as request fields or eligibility
criteria. A founder decision must determine whether each category is:

* prohibited from the contract;
* represented only by an opaque caller-supplied reference;
* represented by a strict caller-supplied descriptive fact;
* represented by a caller-supplied evidence-quality assertion; or
* deferred to a separate subject.

No future classifier may retrieve, calculate, validate, enrich, normalize, or
refresh any such fact.

## Proposed Request Concepts - Not Approved Fields

The labels below identify questions, not final names or fields.

| Concept | Unresolved question | Locked interpretation |
| --- | --- | --- |
| Stock request reference | Is an opaque request reference required, and what strict type and preservation rule applies? | Traceability only |
| Stock subject reference | Is a symbol, ticker, security, or other opaque subject reference required, optional, or prohibited? | Never selection or validation |
| Stock-lane confirmation | Is explicit lane confirmation required, and what closed representation applies? | Never permission |
| Eligibility evidence presence | Must the caller assert that evidence exists? | Supplied fact only |
| Eligibility evidence currentness | Must the caller assert currentness? | No clock or lookup |
| Eligibility evidence sufficiency | Must the caller assert sufficiency? | No internal scoring |
| Eligibility evidence contradiction | Must the caller explicitly identify contradiction? | No inferred contradiction unless founder-defined from supplied fields |
| Eligible posture | Is a supplied eligibility posture represented, and how? | Never authority |
| Excluded posture | Is a supplied exclusion posture represented, and how? | Never runtime blocking |
| Restricted posture | Is a distinct supplied restriction posture represented? | Never an enforcement mechanism |
| Stock evidence reference | Is one opaque evidence reference required? | Preserved, never dereferenced |
| Stock fact categories | Are any caller-supplied listing, sector, capitalization, liquidity, spread, volatility, event, halt, or similar facts allowed? | No retrieval or calculation |
| Generic asset-class context | Is contextual generic evidence required, optional, or prohibited? | No evaluator invocation |
| Upstream decision reference | Is an opaque upstream reference allowed? | Traceability only |
| Authority evidence | Is contextual EchoAuth evidence required, optional, or prohibited? | Cannot grant eligibility |
| Correlation reference | Is a correlation reference required? | Traceability only |

Required versus optional status, exact types, strictness, omission, explicit
null, empty value handling, object identity, normalization, and preservation
remain unresolved for every concept.

## Proposed Decision Surface - Not Approved

A future contract might require an immutable request, an immutable decision,
closed outcome and reason vocabularies, a closed required-action vocabulary,
an exact subject-emittable action subset, reference preservation, deterministic
first-match precedence, explicit governed undefined states, and a fail-closed
fallback.

None of those structures, names, counts, or values is approved here. Whether
authority or generic context requires a separate immutable structure also
remains unresolved.

## Complete Unresolved Founder-Decision Surface

The questions below are complete by decision domain. They are not an inherited
numerical quota, and this review assigns no approved answer.

### Subject and Meaning

* What exact unit is classified: a Stock lane request, an opaque security
  reference, or another bounded subject?
* Must the subject already be identified as Stock, and how is that supplied?
* What exact non-authorizing meaning does eligible have?
* What exact descriptive meaning does excluded have?
* Does restricted exist as a separate posture, and what does it mean?
* Does the contract describe only caller-supplied posture, or may it derive
  limited relationships among supplied typed facts?
* Which interpretations must be expressly prohibited to prevent selection,
  recommendation, trading permission, or execution authority?

### Request Shape and Strict Input Boundary

* What is the exact immutable request structure?
* Which concepts are fields, and what are their exact names?
* Which fields are required, optional, or prohibited?
* What exact types apply to every field?
* Which Boolean facts require strict Boolean types without coercion?
* Are enums accepted only as enum members, only as exact strings, or through
  separate schema and Python boundaries?
* How are unknown keywords, positional arguments, extra object fields,
  alternate representations, subclasses, dictionaries, and lookalike objects
  handled?
* What are the exact non-empty-string, whitespace, normalization, and reference
  preservation rules?
* For every optional field, is omission distinct from explicit null?
* Are empty objects, empty references, and default factories prohibited?
* Are all request fields required to have no defaults, or are any defaults
  justified?

### Stock Subject and Evidence Concepts

* Is a stock, security, symbol, or ticker reference present at all?
* If present, is it opaque and preserved exactly, and which label is correct?
* May a request carry a caller-supplied security-type fact?
* May it carry a caller-supplied exchange or listing-status fact?
* May it carry caller-supplied sector, industry, market-cap, price-range,
  liquidity, volume, spread, or volatility facts?
* May it carry caller-supplied corporate-action, earnings, news-event, halt,
  suspension, delisting, short-interest, borrow-risk, dividend, or split
  facts?
* May it carry caller-supplied watchlist, screen, account-permission, margin,
  collateral, or buying-power facts?
* Which categories belong in other subjects and therefore must be prohibited?
* For every allowed category, is the contract given a fact, a posture, an
  evidence reference, or only an evidence-quality assertion?
* How is the contract prevented from treating supplied market-related facts as
  market-data access, analysis, selection criteria, or trading advice?

### Evidence Quality and References

* Which evidence-quality dimensions exist: presence, currentness,
  sufficiency, contradiction, ambiguity, scope, or others?
* Are evidence-quality dimensions strict Booleans, closed enums, or another
  representation?
* Is currentness supplied by the caller without clock access?
* Is sufficiency supplied by the caller without scoring or policy lookup?
* Is contradiction only an explicit caller fact, or may exact contradictions
  be derived from other supplied fields?
* What evidence reference or references are required?
* Must references be non-empty, opaque, immutable, and preserved exactly?
* What happens when evidence exists but its reference is absent, empty,
  duplicated, mismatched, or contradictory?
* Can evidence be omitted, and how does omission differ from an explicit
  negative evidence assertion?

### Posture Facts

* Which of eligible, excluded, and restricted are represented?
* Are posture facts strict Booleans, a single closed enum, or another exact
  representation?
* Is absence of a posture field permitted?
* What does every all-false, all-omitted, or otherwise unresolved posture
  combination mean?
* May exclusion or restriction be asserted without eligibility?
* Does any supplied posture require a matching evidence reference or
  evidence-quality state?

### Stock-Lane and Generic Context

* Is explicit Stock-lane confirmation required?
* What is its exact closed vocabulary and invalid-input boundary?
* What constitutes missing, negative, contradictory, ambiguous, stale, or
  out-of-scope lane confirmation?
* Is generic Asset-Class context required, optional, or prohibited?
* If generic context is allowed, what exact structure and reference semantics
  apply?
* Must supplied generic context identify Stock, and how are mismatch,
  invalidity, staleness, contradiction, and out-of-scope states classified?
* Is a supplied generic decision reference permitted without a supplied
  generic decision object?
* How is evaluator invocation or inherited authority prohibited?

### Authority Evidence

* Is authority evidence required, optional, or prohibited?
* If allowed, what exact immutable type represents it?
* What exact fields, types, and references are required?
* Does every field lack a default and default factory?
* Which fields, if any, are strict Booleans?
* What closed validity or status vocabulary, if any, is used?
* Is optionality represented by omission only?
* Is explicit null invalid and distinguishable from omission?
* Are dictionaries, alternate objects, Deferral-shaped objects, partial
  objects, empty objects, and lookalikes rejected?
* What exact authority failure states exist?
* What exact subprecedence applies when multiple authority failures collide?
* What mappings connect each authority failure to outcome, reason, and action?
* Where does authority evaluation appear in the overall first-match order?
* How is authority evidence prevented from granting, repairing, broadening,
  reinterpreting, or bypassing Stock eligibility authority?

### Outcomes

* What is the exact closed outcome vocabulary?
* How many outcomes are justified by Stock semantics?
* What does each outcome mean and expressly not mean?
* Is there a distinct unresolved, review, excluded, restricted, or eligible
  outcome?
* Which outcome is the deterministic fail-closed fallback?
* Are aliases, unknown strings, free text, and coercion prohibited?

### Reason Codes

* What is the exact closed Stock-specific reason vocabulary?
* Which reasons represent evidence missing, stale, insufficient,
  contradictory, ambiguous, or otherwise invalid?
* Which reasons represent eligible/excluded/restricted posture and conflicts?
* Which reasons represent Stock-lane and generic-context failures?
* Which reasons represent authority failures?
* Which reasons represent governed undefined states and unresolved fallback?
* Is every reason mapped to exactly one permitted outcome and required action?
* Which generic or neighboring-lane reasons are prohibited because they
  misstate the Stock subject?
* Are aliases, unknown values, free text, and hidden catch-all reasons
  prohibited?

### Required Actions

* What exact closed RequiredAction vocabulary applies?
* Is an existing repository vocabulary reusable only by explicit adoption?
* Which actions are emittable by this subject?
* Which actions must remain unavailable even if present in a shared enum?
* What exact outcome/reason/action mapping applies to every decision path?
* Can any action be mistaken for runtime work, order handling, execution, or
  permission, and how is that prohibited?

### Contradictions and Collisions

* What exact supplied-fact combinations constitute contradiction?
* How are eligible plus excluded, eligible plus restricted, excluded plus
  restricted, and all-three collisions handled?
* How do posture conflicts interact with contradictory, missing, stale, or
  insufficient evidence?
* How do Stock-lane failures interact with posture conflicts?
* How do generic-context failures interact with posture conflicts?
* How do authority failures interact with posture conflicts and evidence
  deficiencies?
* Which collisions are logically constructible in the final typed model?
* Which apparent collisions are impossible and therefore must not be treated
  as required test combinations?

### Governed Undefined States

* Which structurally valid combinations are intentionally undefined?
* Are there one or more exact undefined predicates?
* How are all-false posture, excluded-without-eligible,
  restricted-without-eligible, or other candidate states treated?
* Does a governed undefined state precede ordinary exclusion, restriction,
  authority, or evidence handling?
* What outcome, reason, and action map to each undefined predicate?
* What final fallback covers combinations not otherwise matched?
* How is every typed input combination guaranteed one decision?

### Deterministic Precedence

* What is the exact complete first-match order?
* What is the precedence among contradiction, posture conflicts, governed
  undefined states, lane failures, generic-context failures, exclusion,
  restriction, authority failures, evidence deficiencies, eligibility, and
  fallback?
* Is there separate subprecedence within lane confirmation, generic context,
  authority evidence, evidence quality, and posture conflicts?
* What exact mappings apply at every step?
* How is the ordering proven complete, mutually deterministic, and free of
  accidental fall-through?
* What exhaustive or generated evidence is required to prove precedence?

### Decision Structure and Reference Preservation

* What is the exact immutable decision structure?
* Which references must be returned?
* Must request, subject, evidence, authority, upstream, and correlation
  references be preserved exactly?
* Are optional references omitted or represented explicitly in decisions?
* Must repeated evaluations return equal-but-distinct decision objects?
* Are request or nested evidence objects ever returned by identity, copied, or
  excluded from the decision?

### Schema

* Is a JSON Schema required, and what exact path and identifier apply?
* What schema draft applies?
* What are the exact `required`, `properties`, and
  `additionalProperties` rules for every object?
* How are omission, explicit null, empty strings, strict Booleans, closed
  enums, and nested objects represented?
* Which definitions must have exact parity with Python types?
* Does the schema describe only data shape and avoid implementing precedence
  or runtime behavior?
* What examples, descriptions, and non-authorization language are required?
* What schema/API parity checks are mandatory?

### Python Module, Public API, and Exports

* What exact production module path is appropriate?
* Does implementation belong under `sniperbot.stock` or another bounded
  package?
* How does it coexist with the accepted Stock Deferral / No-Action module?
* Must `src/sniperbot/stock/__init__.py` remain unchanged?
* If package exports are later approved, what exact public symbols and
  `__all__` apply without colliding with existing names?
* Which enums, dataclasses, aliases, constructors, and evaluator functions
  exist?
* Are dataclasses frozen, and do they have slots or other exact structural
  constraints?
* What are the exact function names, positional and keyword boundaries,
  annotations, defaults, and return types?
* Are helper functions public, private, or prohibited?
* What import directions and package-boundary restrictions apply?

### Exceptions and Strict Types

* Which invalid inputs raise `TypeError` and which raise `ValueError`?
* At what boundary are raw strings converted, if conversion is allowed at all?
* Are enum constructors the only raw-string validation boundary?
* How are strict Booleans enforced against integers and other truthy values?
* How are missing fields, extra fields, explicit null, empty references,
  unknown enums, alternate objects, and malformed nested structures rejected?
* Does the evaluator accept only the exact request type?
* Can evaluation itself raise for a well-formed request, or must every
  well-formed request produce a decision?
* Which exception messages or message stability, if any, are contractual?

### Purity, Determinism, and Non-Mutation

* Must evaluation be a total deterministic function over the approved typed
  request space?
* What immutability guarantees apply to requests, nested evidence, and
  decisions?
* What direct evidence proves supplied objects are not mutated?
* What direct evidence proves repeated decisions are equal but distinct?
* How are filesystem, environment, networking, subprocess, logging,
  persistence, caching, time, randomness, mutable globals, and import-time
  side effects prohibited?
* How are market data, broker, wallet, order, registration, runtime,
  integration, orchestration, and evaluator invocation prohibited by imports
  and behavior?
* Are third-party dependencies prohibited?

### Direct Tests

* What exact focused test path is authorized later?
* What public API, `__all__`, enum, dataclass, signature, and exception tests
  are mandatory?
* What omission-versus-null, required-field, no-default, strict-type,
  alternate-object, and lookalike-object tests are mandatory?
* What exact precedence, authority-subprecedence, collision, undefined-state,
  outcome/reason/action mapping, and fallback tests are mandatory?
* What schema/API parity and reference-preservation tests are mandatory?
* What determinism, non-mutation, equal-but-distinct, purity, prohibited
  import, and prohibited capability tests are mandatory?
* Is exhaustive combination testing required, and what exact finite input
  model and expected count apply?
* What evidence closes any direct-test gap found by independent review?

### Validation and Evidence Acceptance

* What documentation and content guards apply at each future step?
* What schema parsing and schema/API parity commands are required?
* What focused, Contract Validation, Authority Clarity, explicit Authority
  Clarity Validator, and canonical-suite commands are required?
* What import-boundary, side-effect, dependency, package, scope, whitespace,
  and `git diff --check` checks are required?
* What exact clean/synchronized repository checks apply before and after
  publication?
* What independent implementation-evidence verification is required?
* If verification finds a gap, what separately authorized bounded evidence
  completion is permitted?
* What exact formal implementation-evidence acceptance artifact is required?
* What commit provenance, test counts, exhaustive counts, and clean-state
  evidence must acceptance record?
* What failures force an immediate stop?

## Explicit No-Inheritance Rule

This record does not adopt from Options Eligibility / Exclusion:

* any Options-specific public symbol or `__all__` entry;
* its nine-symbol API;
* its enum, dataclass, request, decision, or function names;
* its field names, requiredness, defaults, omission/null rules, or strictness;
* its outcome, reason, action, or emittable-action vocabulary;
* its twelve-step precedence;
* its governed undefined predicates;
* its six-field authority structure or authority subprecedence;
* its exception mapping;
* its exhaustive combination count, direct-test count, or evidence count;
* its founder-decision count; or
* its implementation, schema, package, test, or acceptance behavior.

Accepted repository patterns may be cited later as evidence, but Stock may use
one only if a Stock-specific founder decision expressly adopts it. Similarity,
copying convenience, neighboring-lane acceptance, and package proximity are
not authority.

## Required Future Artifact Sequence - Not Authorized

If the founder later chooses to proceed, the governed sequence is expected to
remain:

1. this contract-definition documentation;
2. a separate Stock-specific founder-decision record;
3. a separately authorized JSON Schema;
4. separately authorized exact Python API clarification where needed;
5. a separately authorized pure implementation and direct tests;
6. independent implementation-evidence verification;
7. separately authorized bounded direct-evidence completion if gaps exist; and
8. separately authorized formal implementation-evidence acceptance.

Every step after this record requires its own explicit bounded founder task
order. No step begins automatically.

## Provisional Future Paths - Not Authorized

The following are naming candidates for later founder decision, not approved
files:

* founder-decision record:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-stock-eligibility-exclusion-founder-decision-record.md`;
* schema:
  `schemas/sniperbot-stock-eligibility-exclusion-decision.schema.json`;
* possible production module:
  `src/sniperbot/stock/eligibility_decision.py`;
* possible direct tests:
  `tests/test_sniperbot_stock_eligibility_exclusion.py`; and
* implementation-evidence acceptance:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-stock-eligibility-exclusion-implementation-evidence-acceptance.md`.

The Python package and export path remain especially unresolved because
`sniperbot.stock` already exposes the accepted Stock Deferral / No-Action API.
Listing a candidate path creates no file, reservation, export, or authority.

## Validation and Stop Conditions

This documentation action is valid only if:

* the new contract-definition review and one README traceability entry are the
  only changes;
* the README path is unique and resolves to this file;
* documentation/content guards, Contract Validation, Contract and Authority
  Clarity tests, the Explicit Authority Clarity Validator, and the canonical
  suite pass;
* final newline, whitespace, exact-scope, and `git diff --check` checks pass;
* Stage 2 remains HOLD and Stage 3 remains unentered and unauthorized; and
* the repository finishes clean and synchronized with divergence `0/0`.

Work must stop for any attempt to:

* answer rather than record a founder decision;
* inherit Options-specific API, vocabulary, counts, precedence, authority,
  mappings, tests, or behavior;
* modify or reinterpret Stock Deferral / No-Action;
* create a schema, source module, test, package export, workflow, dependency,
  validator, configuration, runtime hook, or integration surface;
* introduce runtime, orchestration, market-data, broker, wallet, networking,
  persistence, registration, order, trading, execution, or Stage 3 behavior;
* change an unexpected file; or
* proceed after any validation, scope, synchronization, or lock failure.

## Readiness Conclusion and Next Founder Decision

The bounded Stock Eligibility / Exclusion contract-definition surface is now
documented without resolving any Stock semantic choice. It preserves the
accepted Stock Deferral / No-Action lane, rejects inherited Options behavior,
and grants no schema, API, implementation, test, runtime, integration, or
Stage 3 authority.

The exact next founder decision, if any, is whether to authorize bounded
creation of the Stock Eligibility / Exclusion founder-decision record.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized.
