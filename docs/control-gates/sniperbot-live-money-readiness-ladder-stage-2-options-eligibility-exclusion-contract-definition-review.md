# SniperBot Live-Money Readiness Ladder Stage 2 Options Eligibility / Exclusion Contract Definition Review

## Status and Boundary

Artifact type: **Contract-Definition Review**

Subject: **Options Eligibility / Exclusion**

Stage: **SniperBot Live-Money Readiness Ladder — Stage 2**

Governing boundary-review commit:
`f13312a2a2f35f874ab1f8d28b8aba75eb250050`.

Starting checkpoint:
`7f9bd718317f2c17d7b7de0099a48815dc799bfe`.

Current readiness: **Contract definition documented; founder decisions not yet
completed.**

This record is descriptive, governance-only, non-runtime, and non-execution.
It grants no permission and authorizes no final vocabulary, schema, Python API,
implementation, tests, evaluator chaining, integration, trading, execution, or
Stage 3 movement.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized.

## Exact Subject Boundary

The proposed subject is one pure descriptive classification of an
Options-related eligibility posture using only caller-supplied evidence. It may
accept supplied Options eligibility, exclusion, restriction, and
evidence-quality facts; optionally accept supplied authority context if later
approved; preserve opaque references; and return one deterministic descriptive
decision.

The future contract must fail closed for contradiction, conflict, incomplete
evidence, governed undefined combinations, and unresolved posture.

An eventual eligible result may mean only:

`eligible for continued governed Stage 2 evaluation`

It must never mean tradeable, approved, safe, recommended, routable,
executable, or authorized for live money. Absence of exclusion must never be
interpreted as approval.

## Explicit Exclusions

The subject excludes:

* asset-class selection or approval;
* ticker, symbol, or underlying selection;
* option-chain lookup or contract discovery;
* call or put selection;
* strike, expiration, moneyness, or option-style selection;
* single-leg, multi-leg, or spread construction;
* quote or pricing analysis;
* Greeks or implied-volatility calculations;
* volume, open-interest, or liquidity analysis;
* strategy selection or signal generation;
* risk, sizing, margin, collateral, assignment, or exercise decisions;
* market-data, broker, Robinhood, exchange, account, wallet, or credential
  access;
* order, routing, transaction, execution, or deployment behavior;
* evaluator orchestration, integration, or Stage 3 movement.

No excluded capability is implied, prepared, partially approved, or made ready
by this contract definition.

## Separation From Adjacent Subjects

### Asset-Class Eligibility / Exclusion

Asset-Class Eligibility / Exclusion may exist as caller-supplied upstream
context only if later approved. This subject must not invoke its evaluator,
inherit permission from its result, or create runtime chaining or orchestration.

### Options Deferral / No-Action

Options Deferral / No-Action remains a separate semantic subject. Deferral
answers whether evaluation pauses or takes no action. Eligibility describes an
eligibility posture. Neither evaluator invokes, overrides, or controls the
other.

### Pure FSM

The pure FSM supplies only a purity and deterministic-classification pattern.
No FSM transition, invocation, state change, or integration is authorized.

### Rollback / No-Action Fallback

Rollback / No-Action Fallback supplies only a governance and fail-closed
reference pattern. No rollback invocation, state change, or behavior is
authorized.

### Stock and Crypto Eligibility / Exclusion

Stock and Crypto Eligibility / Exclusion remain separate later lanes. Stock
follows Options, and Crypto follows Stock. Neither may begin under this record.

## Proposed Request Concepts — Not Approved Fields

The following concepts are proposals for founder decision. They do not define
an exact final request shape.

| Proposed concept | Semantic meaning | Proposed status | Type category | Omission / null | Interpretation | Founder confirmation |
| --- | --- | --- | --- | --- | --- | --- |
| Options request reference | Identifies the caller's Options-related request without identifying or selecting a contract. | Likely required | Non-empty string | Not applicable if required | Opaque and preserved exactly | Required |
| Eligibility evidence present | Caller-supplied assertion that eligibility evidence exists. | Proposed required | Boolean | Not applicable if required | Supplied fact only | Required |
| Eligibility evidence current | Caller-supplied evidence-currentness assertion. | Proposed required | Boolean | Not applicable if required | Supplied fact only | Required |
| Eligibility evidence sufficient | Caller-supplied evidence-sufficiency assertion. | Proposed required | Boolean | Not applicable if required | Supplied fact only | Required |
| Eligibility evidence contradictory | Caller-supplied explicit contradiction assertion. | Proposed required | Boolean | Not applicable if required | Supplied fact only; not inferred | Required |
| Options eligible | Caller-supplied descriptive eligibility posture. | Proposed required | Boolean | Not applicable if required | Supplied fact only; never permission | Required |
| Options excluded | Caller-supplied descriptive exclusion posture. | Proposed required | Boolean | Not applicable if required | Supplied fact only; not runtime blocking | Required |
| Options restricted | Caller-supplied descriptive restriction posture. | Proposed required | Boolean | Not applicable if required | Supplied fact only | Required |
| Eligibility evidence reference | Identifies the supplied eligibility evidence. | Unresolved | Non-empty string | Founder decision required | Opaque and preserved, not looked up | Required |
| Asset-class context | Optional caller-supplied generic asset-class context if approved. | Unresolved | Typed immutable context | Omission versus explicit null unresolved | Supplied context only; no evaluator invocation | Required |
| Authority evidence | Optional contextual EchoAuth evidence if approved. | Proposed optional | Typed immutable structure | Omission-only proposed; explicit null proposed invalid | Contextual only; grants no authority | Required |
| Correlation reference | Caller-supplied traceability reference. | Likely required | Non-empty string | Not applicable if required | Opaque and preserved exactly | Required |
| Upstream decision reference | Optional traceability reference to a supplied upstream decision. | Unresolved | Non-empty string | Omission versus explicit null unresolved | Opaque only; no validation or consumption | Required |

No symbol, ticker, underlying, contract, strike, expiration, Greeks, price,
liquidity, strategy, risk, sizing, order, or execution field is proposed.

## Smallest Proposed Decision Surface

A future closed contract will likely require:

* one immutable request structure;
* one immutable decision structure;
* one optional immutable authority structure if approved;
* a closed outcome vocabulary;
* a closed Options-specific reason vocabulary;
* a closed `RequiredAction` vocabulary;
* a subject-specific emittable-action subset;
* exact reference preservation;
* deterministic first-match precedence;
* explicit undefined-combination handling; and
* a fail-closed unresolved fallback.

### Reusable Only If Explicitly Adopted

The following accepted patterns may be reusable only through explicit founder
adoption: frozen typed structures; the five-value repository
`RequiredAction`; a restricted emittable subset; `Validity`; the six-field
`AuthorityEvidence`; strict non-coercing input boundaries; exact reference
preservation; equal-but-distinct repeated decisions; non-mutation; and no side
effects.

### Options-Specific and Unresolved

The exact outcomes, reason codes, request fields, generic asset-class context,
conflict mappings, governed undefined predicates, first-match order, Python
package, and public exports remain unresolved.

Options Deferral / No-Action outcomes and reason codes cannot be reused because
they classify a different subject.

## Meaningful Conflicts Requiring Founder Decisions

The future founder-decision record must resolve only logically constructible
conflicts, including:

* eligible plus excluded;
* eligible plus restricted;
* excluded plus restricted;
* eligible plus excluded plus restricted;
* contradictory evidence combined with posture facts;
* missing, stale, or insufficient evidence combined with posture facts;
* authority contradiction, ambiguity, invalidity, revocation, staleness, or
  out-of-scope status;
* authority failure combined with posture conflicts;
* all posture flags false after otherwise valid evidence;
* excluded without eligible;
* restricted without eligible; and
* structurally valid combinations intentionally governed as undefined.

The following are not valid collisions: `VALID`, `INVALID`, and `AMBIGUOUS`
simultaneously; one Boolean being both true and false; one field being both
omitted and supplied; or explicit null and a valid typed object simultaneously.
No Cartesian collision matrix is approved.

## Proposed Authority-Evidence Boundary

The accepted six-field structure is the strongest reusable pattern:

1. `validity`
2. `current`
3. `revoked`
4. `contradictory`
5. `in_scope`
6. `evidence_reference`

Explicit founder adoption remains required. The proposed rules are that all six
fields are required when the object is supplied; optionality is represented by
omission only; explicit null and empty objects are rejected; dictionaries and
alternate Deferral-shaped fields are rejected by the typed Python API; the
evidence reference is opaque and non-empty; and authority evidence is contextual
only and cannot grant eligibility or permission.

No Options-specific authority field is currently justified. Whether the
accepted authority subprecedence is inherited remains a founder decision.

## Unresolved Precedence Categories

Deterministic first-match precedence is mandatory, but the exact Options order
remains unresolved. Founder ordering is required for:

1. evidence contradiction;
2. eligible/excluded conflict;
3. eligible/restricted conflict;
4. excluded/restricted conflict, if separately governed;
5. all-three-posture conflict;
6. governed undefined combinations;
7. exclusion;
8. restriction;
9. authority failures;
10. missing evidence;
11. stale evidence;
12. insufficient evidence;
13. eligible posture; and
14. unresolved fallback.

The accepted Asset-Class Eligibility order is a strong reference pattern, not
inherited authority. This record establishes no final precedence.

## Vocabulary Reuse Boundaries

Potentially reusable only if later adopted:

* `Validity.VALID`;
* `Validity.INVALID`;
* `Validity.AMBIGUOUS`;
* `RequiredAction.NONE`;
* `RequiredAction.HUMAN_REVIEW`;
* `RequiredAction.GOVERNANCE_REVIEW`;
* `RequiredAction.FOUNDER_AUTHORITY_REQUIRED`;
* `RequiredAction.RESET_REQUIRED`; and
* generic authority-failure concepts.

Options-specific vocabulary is required for Options eligible, excluded, and
restricted postures; missing, stale, insufficient, and contradictory Options
eligibility evidence; Options posture conflicts; undefined Options
combinations; and unresolved Options eligibility posture.

Generic `ASSET_CLASS_*` reasons would misstate the subject. Options Deferral
reasons would contaminate eligibility with deferral semantics. If a closed
vocabulary is later adopted, aliases, unknown values, and free-text reasons
must be prohibited. This record approves no exact name or count.

## Purity and Prohibited Capabilities

Any future implementation must prohibit filesystem and environment access;
networking; subprocesses; logging; persistence; third-party dependencies;
market-data and option-chain access; pricing; Greeks; implied-volatility
calculations; broker, exchange, Robinhood, account, wallet, or credential
access; contract, strike, expiration, or spread selection; strategy; risk;
sizing; margin; assignment; exercise; orders; transactions; routing;
execution; evaluator orchestration; upstream evaluator invocation; EchoAuth
runtime invocation; mutable global state; input mutation; caching; time
dependence; randomness; nondeterminism; and import-time side effects.

## Required Future Artifact Sequence — Not Authorized

Definitely required:

1. contract-definition documentation;
2. separate founder-decision record;
3. JSON Schema;
4. exact Python API clarification;
5. pure implementation and direct tests;
6. independent implementation-evidence verification;
7. bounded evidence completion if verification finds gaps; and
8. formal implementation-evidence acceptance.

Possibly required: authority-structure clarification, omission-versus-null
clarification, structural clarification, and additional direct-test evidence
completion.

Not justified: evaluator chaining, runtime integration, option-chain work,
pricing work, Stock Eligibility work, Crypto Eligibility work, or Stage 3.

## Founder Decisions Required Before Schema or Implementation

The questions below remain unanswered. Recording them does not resolve them.

### Subject and Authority Boundary

1. Does the subject classify only caller-supplied Options eligibility posture, with no market interpretation?
2. What precisely does an eligible outcome mean: continued governed Stage 2 evaluation only, or another closed non-authorizing meaning?
3. Must the classifier remain independent of Asset-Class Eligibility, Options Deferral, FSM, and Rollback evaluators?
4. Is absence of exclusion expressly prohibited from implying approval?

### Request Inputs

5. What is the exact mandatory opaque Options request reference?
6. Is a separate eligibility-evidence reference required?
7. Which evidence-quality flags are required: presence, currentness, sufficiency, and contradiction?
8. Are `eligible`, `excluded`, and `restricted` the complete posture flags?
9. Is generic asset-class context omitted, or accepted as optional caller-supplied typed context?
10. If generic context exists, must it identify `OPTIONS`, and how are invalid, ambiguous, stale, contradictory, or out-of-scope contexts classified?
11. Is an upstream decision reference allowed for traceability only?
12. Which optional fields use omission only, and is explicit null universally prohibited?
13. Is a mandatory opaque correlation reference required?

### Outcomes

14. Does the lane adopt the generic four-outcome shape—eligible, excluded, restricted, review required—or define another closed Options-specific set?
15. Is every outcome descriptive and non-authorizing?
16. What outcome represents the fail-closed unresolved fallback?

### Reason Codes

17. What are the exact Options-specific eligible, excluded, and restricted reason codes?
18. What are the exact missing, stale, insufficient, and contradictory evidence reasons?
19. What reasons represent eligible/excluded and eligible/restricted conflicts?
20. Is an excluded/restricted collision separately named or governed as undefined?
21. Are authority failures represented by the accepted generic authority reason names?
22. What exact reason represents a governed undefined combination?
23. What exact reason represents unresolved fallback?
24. Are aliases, free text, generic asset-class reasons, and Options Deferral reasons prohibited?

### Required Actions

25. Is the accepted five-value repository `RequiredAction` vocabulary reused unchanged?
26. Which actions may this subject emit?
27. What exact action maps to each outcome and reason?
28. Do `FOUNDER_AUTHORITY_REQUIRED` and `RESET_REQUIRED` remain vocabulary-only and non-emittable?

### Authority Evidence

29. Is the accepted six-field `AuthorityEvidence` structure adopted exactly?
30. Are all six fields mandatory whenever authority evidence is supplied?
31. Is authority evidence optional by omission only, with explicit null prohibited?
32. Are dictionaries and alternate Deferral-shaped authority representations prohibited?
33. Is the accepted authority subprecedence inherited exactly or separately specified?
34. Does valid authority merely permit continued classification without granting eligibility or permission?

### Precedence

35. What is the complete first-match precedence?
36. Do contradiction and posture conflicts precede exclusion and restriction?
37. Does exclusion precede restriction?
38. Where do governed undefined combinations appear?
39. Do posture classifications precede authority failures, or vice versa?
40. What is the order among missing, stale, and insufficient evidence?
41. Where does the eligible branch occur?
42. Is unresolved fallback always last?

### Conflicts and Undefined Combinations

43. What is the mapping for eligible plus excluded?
44. What is the mapping for eligible plus restricted?
45. What is the mapping for excluded plus restricted?
46. What is the mapping when all three posture flags are true?
47. Which structurally valid combinations are expressly governed as undefined?
48. Are excluded-without-eligible and restricted-without-eligible ordinary terminal postures or undefined combinations?
49. How do posture assertions behave when evidence is missing, stale, insufficient, or contradictory?

### References

50. Which request references must be preserved exactly in the decision?
51. Are references opaque non-empty strings with no parsing or lookup?
52. May a decision expose an upstream reference without claiming upstream validation?

### Python API

53. What is the exact package path?
54. What are the exact public enums, frozen dataclasses, constructor, and evaluator symbols?
55. What is the exact `__all__` order?
56. What are the exact dataclass field orders and defaults?
57. Which raw inputs raise `TypeError` versus `ValueError`?
58. Must repeated evaluation return equal but distinct decisions?
59. Must caller objects remain unmodified?

### Purity and Prohibited Capabilities

60. Is the implementation limited to standard-library dataclasses and enums?
61. Are all I/O, environment, network, subprocess, logging, persistence, runtime, and orchestration capabilities prohibited?
62. Are all option-chain, pricing, Greeks, implied-volatility, strategy, risk, sizing, order, and execution capabilities prohibited?
63. Are mutable global state, caching, time dependence, randomness, and import-time behavior prohibited?

### Future Evidence Requirements

64. Which collision cases require direct tests?
65. Which authority-subprecedence combinations require direct tests?
66. Must tests prove strict omission/null and alternate-representation rejection?
67. Must tests prove exact reference preservation, non-mutation, and deterministic repetition?
68. Must tests prove non-emittable actions are never returned?
69. Must validation include schema parse, focused tests, Contract/Authority Clarity checks, import-boundary review, and the canonical full suite?
70. Must independent evidence verification and separate formal acceptance remain mandatory before closure?

## Provisional Future Paths — Not Authorized for Creation

Subject to separate founder authorization and later decisions, repository
conventions support these provisional paths:

* founder-decision record:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-options-eligibility-exclusion-founder-decision-record.md`;
* schema:
  `schemas/sniperbot-options-eligibility-exclusion-decision.schema.json`;
* likely Python package: unresolved because the current `sniperbot.options`
  and `sniperbot.eligibility` conventions do not establish one unambiguous
  location;
* implementation-evidence acceptance:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-options-eligibility-exclusion-implementation-evidence-acceptance.md`.

These paths are proposals only. They create no file, package, schema, API,
implementation, test, integration, or acceptance authority.

## Validation and Stop Conditions

Any later artifact requires its own bounded task order. Future validation is
expected to include schema parsing, focused direct tests, Contract and Authority
Clarity checks, import-boundary review, scope checks, and the canonical full
suite where required. Those checks are not implementation authority.

Work must stop for unresolved vocabulary, precedence, request shape, authority
representation, reference semantics, Python API, unexpected scope, validation
failure, or any request for integration, execution, Stock or Crypto Eligibility,
or Stage 3 movement.

## Readiness Conclusion and Next Founder Decision

The Options Eligibility / Exclusion contract boundary is sufficiently defined
for this documentation record. The 70 founder decisions remain unanswered and
must be resolved separately before schema or implementation work can begin.

This record strengthens the system by isolating a deterministic, fail-closed,
non-authorizing Options eligibility classification surface from option-market
analysis, trading permission, and execution capability.

The exact next founder decision is whether to authorize bounded completion of
the Options Eligibility / Exclusion founder-decision record.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized.
