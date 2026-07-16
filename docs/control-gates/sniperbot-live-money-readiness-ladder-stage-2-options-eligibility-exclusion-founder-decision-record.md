# SniperBot Live-Money Readiness Ladder Stage 2 Options Eligibility / Exclusion Founder Decision Record

## Status and Boundary

Subject: **Options Eligibility / Exclusion**

Stage: **SniperBot Live-Money Readiness Ladder — Stage 2**

Artifact: **Founder-Decision Record**

Governing contract checkpoint:
`854f4f85e2b5bd5ca0cce91cfbe2b08a54ed56dd`.

Governing boundary-review commit:
`f13312a2a2f35f874ab1f8d28b8aba75eb250050`.

Founder decisions completed: **70 of 70**.

Current posture: **Decisions recorded; schema and implementation not
authorized.**

Every result governed here is descriptive. No result grants trading authority,
permission, market access, order authority, execution authority, or live-money
authority. This documentation-only record authorizes no schema, source, tests,
implementation, evaluator orchestration, integration, market data, option-chain
access, pricing, strategy, risk, sizing, orders, execution, neighboring lane, or
Stage 3 movement.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized.
## Founder decisions

### A. Subject and authority boundary

#### Decision 1

The subject classifies only caller-supplied Options eligibility facts.

It performs no independent market, contract, security, or instrument interpretation.

#### Decision 2

`ELIGIBLE` means only:

`eligible for continued governed Stage 2 evaluation`

It does not mean:

* tradeable;
* approved;
* safe;
* recommended;
* routable;
* executable;
* authorized for live money.

#### Decision 3

The classifier remains completely independent of:

* Asset-Class Eligibility / Exclusion;
* Options Deferral / No-Action;
* the pure FSM evaluator;
* Rollback / No-Action Fallback;
* Stock Eligibility / Exclusion;
* Crypto Eligibility / Exclusion.

It invokes none of them.

#### Decision 4

Absence of exclusion must never be interpreted as approval, permission, eligibility, or authority.

### B. Exact request inputs

#### Decision 5

The mandatory Options request reference is:

`options_reference`

It is a non-empty opaque string.

#### Decision 6

A separate eligibility-evidence reference is mandatory:

`eligibility_evidence_reference`

It is a non-empty opaque string.

#### Decision 7

The following evidence-quality fields are all required strict Booleans:

* `eligibility_evidence_present`
* `eligibility_evidence_current`
* `eligibility_evidence_sufficient`
* `eligibility_evidence_contradictory`

No truthy or falsy coercion is allowed.

#### Decision 8

The complete Options posture fields are:

* `options_eligible`
* `options_excluded`
* `options_restricted`

All three are required strict Booleans.

No additional posture flag is authorized.

#### Decision 9

Generic asset-class context is omitted from the request.

The Options classifier does not consume an Asset-Class Eligibility decision or context object.

#### Decision 10

Because generic asset-class context is omitted, no generic-context validation, interpretation, or mapping exists in this lane.

#### Decision 11

An upstream decision reference is not part of the request or decision.

No upstream decision consumption or traceability field is authorized.

#### Decision 12

The only optional structured request field is:

`authority_evidence`

Its absence is represented by omission only through the public constructor.

Explicit `None` supplied through the public constructor is rejected.

#### Decision 13

A mandatory correlation reference is required:

`correlation_reference`

It is a non-empty opaque string preserved exactly.

### C. Outcomes

#### Decision 14

The closed outcome vocabulary is exactly:

* `ELIGIBLE`
* `EXCLUDED`
* `RESTRICTED`
* `REVIEW_REQUIRED`

#### Decision 15

Every outcome is descriptive and non-authorizing.

#### Decision 16

The fail-closed unresolved fallback outcome is:

`REVIEW_REQUIRED`

### D. Reason codes

#### Decision 17

The exact terminal posture reasons are:

* `OPTIONS_ELIGIBLE`
* `OPTIONS_EXCLUDED`
* `OPTIONS_RESTRICTED`

#### Decision 18

The exact evidence-quality reasons are:

* `OPTIONS_ELIGIBILITY_EVIDENCE_MISSING`
* `OPTIONS_ELIGIBILITY_EVIDENCE_STALE`
* `OPTIONS_ELIGIBILITY_EVIDENCE_INSUFFICIENT`
* `OPTIONS_ELIGIBILITY_EVIDENCE_CONTRADICTORY`

#### Decision 19

The exact eligible-conflict reasons are:

* `OPTIONS_ELIGIBLE_EXCLUDED_CONFLICT`
* `OPTIONS_ELIGIBLE_RESTRICTED_CONFLICT`

#### Decision 20

Excluded plus restricted is not assigned a separate conflict reason.

When `options_eligible` is false and both exclusion and restriction are true, exclusion wins through normal precedence:

`EXCLUDED / OPTIONS_EXCLUDED / NONE`

When all three posture facts are true, the eligible/excluded conflict wins.

#### Decision 21

The exact authority-failure reasons are reused unchanged:

* `AUTHORITY_EVIDENCE_INVALID`
* `AUTHORITY_EVIDENCE_STALE`
* `AUTHORITY_EVIDENCE_REVOKED`
* `AUTHORITY_EVIDENCE_OUT_OF_SCOPE`

Contradictory, ambiguous, and invalid authority states all use:

`AUTHORITY_EVIDENCE_INVALID`

#### Decision 22

The governed undefined-combination reason is:

`UNDEFINED_INPUT_COMBINATION`

#### Decision 23

The unresolved fallback reason is:

`OPTIONS_ELIGIBILITY_UNRESOLVED`

#### Decision 24

The following are prohibited:

* aliases;
* unknown values;
* free-text reasons;
* generic `ASSET_CLASS_*` posture reasons;
* Options Deferral / No-Action reason codes;
* cross-lane reasons.

The closed `ReasonCode` vocabulary therefore contains exactly 15 values.

### E. Required actions

#### Decision 25

The full closed `RequiredAction` vocabulary is exactly:

* `NONE`
* `HUMAN_REVIEW`
* `GOVERNANCE_REVIEW`
* `FOUNDER_AUTHORITY_REQUIRED`
* `RESET_REQUIRED`

#### Decision 26

The only emittable actions are:

* `NONE`
* `HUMAN_REVIEW`
* `GOVERNANCE_REVIEW`

#### Decision 27

The exact branch mappings are those recorded in the precedence section below.

No branch may improvise another action.

#### Decision 28

These values remain vocabulary-only and non-emittable:

* `FOUNDER_AUTHORITY_REQUIRED`
* `RESET_REQUIRED`

### F. Authority evidence

#### Decision 29

Options Eligibility / Exclusion adopts the accepted six-field `AuthorityEvidence` structure exactly:

1. `validity`
2. `current`
3. `revoked`
4. `contradictory`
5. `in_scope`
6. `evidence_reference`

#### Decision 30

All six fields are mandatory whenever authority evidence is supplied.

#### Decision 31

Authority evidence is optional by omission only through `create_request`.

Explicit `authority_evidence=None` is rejected.

#### Decision 32

The typed Python API rejects:

* dictionaries;
* empty objects;
* arbitrary objects;
* alternate Deferral-shaped authority representations;
* fields such as `currentness`, `revocation`, or `scope`.

#### Decision 33

The exact authority subprecedence is:

1. contradictory
2. ambiguous
3. invalid
4. revoked
5. stale
6. out of scope

Where:

* ambiguous means `validity == AMBIGUOUS`;
* invalid means `validity == INVALID`;
* stale means `current == False`;
* out of scope means `in_scope == False`.

#### Decision 34

Fully valid authority evidence merely allows evaluation to continue to lower branches.

It does not grant eligibility, permission, trading authority, or execution authority.

Absent authority also allows evaluation to continue.

### G. Exact first-match precedence

#### Decision 35

The complete first-match order is exactly:

1. Options eligibility-evidence contradiction
2. eligible/excluded conflict
3. eligible/restricted conflict
4. governed undefined combination
5. exclusion
6. restriction
7. authority failure
8. missing eligibility evidence
9. stale eligibility evidence
10. insufficient eligibility evidence
11. eligible result
12. unresolved fallback

#### Decision 36

Evidence contradiction and the two eligible conflicts precede exclusion and restriction.

#### Decision 37

Exclusion precedes restriction.

#### Decision 38

Governed undefined combinations occur after the two eligible-conflict branches and before exclusion.

#### Decision 39

Exclusion and restriction precede authority failures.

Authority failure precedes missing, stale, insufficient, eligible, and fallback branches.

#### Decision 40

Evidence-quality precedence is:

1. missing
2. stale
3. insufficient

#### Decision 41

The eligible branch occurs after all evidence-defect branches and before unresolved fallback.

#### Decision 42

Unresolved fallback is always the final branch.

### H. Exact conflicts and undefined combinations

#### Decision 43

Eligible plus excluded maps to:

* Outcome: `REVIEW_REQUIRED`
* Reason: `OPTIONS_ELIGIBLE_EXCLUDED_CONFLICT`
* RequiredAction: `GOVERNANCE_REVIEW`

#### Decision 44

Eligible plus restricted maps to:

* Outcome: `RESTRICTED`
* Reason: `OPTIONS_ELIGIBLE_RESTRICTED_CONFLICT`
* RequiredAction: `HUMAN_REVIEW`

#### Decision 45

Excluded plus restricted, with eligible false, maps to:

* Outcome: `EXCLUDED`
* Reason: `OPTIONS_EXCLUDED`
* RequiredAction: `NONE`

#### Decision 46

When eligible, excluded, and restricted are all true, eligible/excluded conflict wins:

* Outcome: `REVIEW_REQUIRED`
* Reason: `OPTIONS_ELIGIBLE_EXCLUDED_CONFLICT`
* RequiredAction: `GOVERNANCE_REVIEW`

#### Decision 47

Exactly three Boolean predicates are governed as undefined:

1. `not eligibility_evidence_present and eligibility_evidence_current`
2. `not eligibility_evidence_present and eligibility_evidence_sufficient`
3. `not eligibility_evidence_current and eligibility_evidence_sufficient`

Each maps to:

* Outcome: `REVIEW_REQUIRED`
* Reason: `UNDEFINED_INPUT_COMBINATION`
* RequiredAction: `GOVERNANCE_REVIEW`

No fourth undefined predicate is authorized.

#### Decision 48

Excluded without eligible and restricted without eligible are ordinary terminal postures.

They are not undefined combinations.

#### Decision 49

Posture assertions combined with evidence defects follow the first-match order:

* explicit evidence contradiction wins first;
* eligible conflicts win next;
* undefined predicates win next;
* exclusion wins next;
* restriction wins next;
* authority failures win next;
* missing, stale, and insufficient evidence follow;
* eligible follows;
* fallback remains last.

Only logically constructible collision evidence is required.

Impossible Boolean combinations must not be invented.

### I. References

#### Decision 50

The decision preserves exactly:

* `options_reference`
* `eligibility_evidence_reference`
* `correlation_reference`

#### Decision 51

All three references are:

* mandatory;
* non-empty;
* opaque;
* preserved exactly;
* never parsed;
* never normalized;
* never looked up;
* never interpreted.

#### Decision 52

No upstream decision reference appears in the request or decision.

### J. Exact Python API contract

#### Decision 53

The public module path is exactly:

`sniperbot.options.eligibility_decision`

The existing `sniperbot.options` package root must not be broadened with colliding generic names under this lane.

#### Decision 54

The exact public API contains nine symbols:

1. `Outcome`
2. `ReasonCode`
3. `RequiredAction`
4. `Validity`
5. `AuthorityEvidence`
6. `OptionsEligibilityRequest`
7. `Decision`
8. `create_request`
9. `evaluate`

No public `EmittableAction` is authorized.

#### Decision 55

Module `__all__` must contain exactly those nine names in that exact order.

No alias or additional public symbol is authorized.

#### Decision 56

Exactly three frozen dataclasses are authorized.

#### `AuthorityEvidence`

Exact field order:

1. `validity`
2. `current`
3. `revoked`
4. `contradictory`
5. `in_scope`
6. `evidence_reference`

No defaults or default factories.

#### `OptionsEligibilityRequest`

Exact field order:

1. `options_reference`
2. `eligibility_evidence_present`
3. `eligibility_evidence_current`
4. `eligibility_evidence_sufficient`
5. `eligibility_evidence_contradictory`
6. `options_eligible`
7. `options_excluded`
8. `options_restricted`
9. `eligibility_evidence_reference`
10. `correlation_reference`
11. `authority_evidence`

Only `authority_evidence` has a default:

`None`

#### `Decision`

Exact field order:

1. `outcome`
2. `reason_code`
3. `required_action`
4. `options_reference`
5. `eligibility_evidence_reference`
6. `correlation_reference`

No defaults.

#### Decision 57

The public functions are exactly:

```python
def create_request(**values: object) -> OptionsEligibilityRequest:
```

```python
def evaluate(request: OptionsEligibilityRequest) -> Decision:
```

`TypeError` is required for:

* wrong runtime types;
* raw strings instead of enums;
* non-Boolean Boolean fields;
* invalid authority objects;
* dictionaries or alternate authority shapes;
* explicit authority `None` through `create_request`;
* unexpected request keywords;
* non-request evaluation input.

`ValueError` is required for:

* empty required references;
* non-emittable decision actions;
* correctly typed values violating a closed decision-only boundary.

No custom exception or `AssertionError` input validation is authorized.

#### Decision 58

Repeated evaluation of the same request must produce decisions that are:

* equal by value;
* distinct objects.

#### Decision 59

Evaluation must not mutate:

* the request;
* supplied authority evidence;
* references;
* caller-owned objects.

### K. Purity and prohibited capabilities

#### Decision 60

Production imports are limited to:

```python
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
```

No third-party dependency is authorized.

#### Decision 61

The implementation prohibits:

* filesystem access;
* environment access;
* networking;
* subprocess;
* logging;
* persistence;
* runtime invocation;
* evaluator orchestration;
* upstream evaluator invocation;
* EchoAuth runtime calls;
* import-time side effects.

#### Decision 62

The implementation prohibits:

* market data;
* option-chain access;
* quotes;
* prices;
* Greeks;
* implied volatility;
* volume;
* open interest;
* liquidity analysis;
* symbol or underlying selection;
* call or put selection;
* contract selection;
* strike selection;
* expiration selection;
* spread or multi-leg construction;
* strategy;
* signals;
* risk;
* sizing;
* margin;
* collateral;
* assignment;
* exercise;
* broker or exchange access;
* Robinhood access;
* wallet or credential access;
* orders;
* transactions;
* routing;
* execution.

#### Decision 63

The implementation prohibits:

* mutable global state;
* caching;
* time dependence;
* randomness;
* nondeterminism;
* hidden fallback behavior;
* input mutation.

### L. Future evidence requirements

#### Decision 64

Direct tests must prove:

* all 12 branches;
* exact outcome/reason/action mappings;
* both eligible conflicts;
* all-three posture precedence;
* excluded/restricted precedence;
* all three undefined predicates;
* only logically compatible collision witnesses;
* exclusion and restriction over lower branches;
* evidence ordering;
* eligible over fallback;
* fallback independently.

#### Decision 65

Direct tests must prove all 14 logically possible authority subprecedence collisions:

1. contradictory over ambiguous
2. contradictory over invalid
3. contradictory over revoked
4. contradictory over stale
5. contradictory over out of scope
6. ambiguous over revoked
7. ambiguous over stale
8. ambiguous over out of scope
9. invalid over revoked
10. invalid over stale
11. invalid over out of scope
12. revoked over stale
13. revoked over out of scope
14. stale over out of scope

Ambiguous versus invalid is not required because they are mutually exclusive values of one enum field.

#### Decision 66

Direct tests must prove:

* omission-only authority behavior;
* explicit-null rejection;
* all six authority fields required;
* no authority defaults;
* alternate authority representations rejected;
* strict Boolean and enum boundaries.

#### Decision 67

Direct tests must prove:

* exact reference preservation;
* request non-mutation;
* authority non-mutation;
* frozen dataclasses;
* equal-but-distinct repeated decisions.

#### Decision 68

Direct tests must prove:

* `FOUNDER_AUTHORITY_REQUIRED` is never emitted;
* `RESET_REQUIRED` is never emitted;
* both are rejected by `Decision` with `ValueError`.

#### Decision 69

Validation must include:

* schema parse;
* structural parity checks;
* focused Options Eligibility tests;
* Contract and Authority Clarity tests;
* explicit Authority Clarity Validator;
* production-import and prohibited-capability review;
* canonical full suite.

#### Decision 70

Independent implementation-evidence verification and separate formal evidence acceptance remain mandatory before the lane can close.

No implementation commit alone constitutes acceptance.

## Exact closed vocabularies

Record these tables explicitly.

### Outcome — 4

* `ELIGIBLE`
* `EXCLUDED`
* `RESTRICTED`
* `REVIEW_REQUIRED`

### ReasonCode — 15

* `OPTIONS_ELIGIBLE`
* `OPTIONS_EXCLUDED`
* `OPTIONS_RESTRICTED`
* `OPTIONS_ELIGIBILITY_EVIDENCE_MISSING`
* `OPTIONS_ELIGIBILITY_EVIDENCE_STALE`
* `OPTIONS_ELIGIBILITY_EVIDENCE_INSUFFICIENT`
* `OPTIONS_ELIGIBILITY_EVIDENCE_CONTRADICTORY`
* `OPTIONS_ELIGIBLE_EXCLUDED_CONFLICT`
* `OPTIONS_ELIGIBLE_RESTRICTED_CONFLICT`
* `AUTHORITY_EVIDENCE_INVALID`
* `AUTHORITY_EVIDENCE_STALE`
* `AUTHORITY_EVIDENCE_REVOKED`
* `AUTHORITY_EVIDENCE_OUT_OF_SCOPE`
* `UNDEFINED_INPUT_COMBINATION`
* `OPTIONS_ELIGIBILITY_UNRESOLVED`

### RequiredAction — 5

* `NONE`
* `HUMAN_REVIEW`
* `GOVERNANCE_REVIEW`
* `FOUNDER_AUTHORITY_REQUIRED`
* `RESET_REQUIRED`

### Emittable actions — 3

* `NONE`
* `HUMAN_REVIEW`
* `GOVERNANCE_REVIEW`

### Validity — 3

* `VALID`
* `INVALID`
* `AMBIGUOUS`

## Exact branch mappings

Record this exact table:

| Precedence | Trigger                            | Outcome           | ReasonCode                                   | RequiredAction      |
| ---------: | ---------------------------------- | ----------------- | -------------------------------------------- | ------------------- |
|          1 | Eligibility evidence contradictory | `REVIEW_REQUIRED` | `OPTIONS_ELIGIBILITY_EVIDENCE_CONTRADICTORY` | `HUMAN_REVIEW`      |
|          2 | Eligible and excluded              | `REVIEW_REQUIRED` | `OPTIONS_ELIGIBLE_EXCLUDED_CONFLICT`         | `GOVERNANCE_REVIEW` |
|          3 | Eligible and restricted            | `RESTRICTED`      | `OPTIONS_ELIGIBLE_RESTRICTED_CONFLICT`       | `HUMAN_REVIEW`      |
|          4 | Any approved undefined predicate   | `REVIEW_REQUIRED` | `UNDEFINED_INPUT_COMBINATION`                | `GOVERNANCE_REVIEW` |
|          5 | Excluded                           | `EXCLUDED`        | `OPTIONS_EXCLUDED`                           | `NONE`              |
|          6 | Restricted                         | `RESTRICTED`      | `OPTIONS_RESTRICTED`                         | `HUMAN_REVIEW`      |
|          7 | Authority failure                  | `REVIEW_REQUIRED` | Approved authority reason                    | `GOVERNANCE_REVIEW` |
|          8 | Evidence missing                   | `REVIEW_REQUIRED` | `OPTIONS_ELIGIBILITY_EVIDENCE_MISSING`       | `HUMAN_REVIEW`      |
|          9 | Evidence stale                     | `REVIEW_REQUIRED` | `OPTIONS_ELIGIBILITY_EVIDENCE_STALE`         | `HUMAN_REVIEW`      |
|         10 | Evidence insufficient              | `REVIEW_REQUIRED` | `OPTIONS_ELIGIBILITY_EVIDENCE_INSUFFICIENT`  | `HUMAN_REVIEW`      |
|         11 | Eligible                           | `ELIGIBLE`        | `OPTIONS_ELIGIBLE`                           | `NONE`              |
|         12 | Otherwise unresolved               | `REVIEW_REQUIRED` | `OPTIONS_ELIGIBILITY_UNRESOLVED`             | `GOVERNANCE_REVIEW` |

Record authority mappings:

| Authority condition | ReasonCode                        |
| ------------------- | --------------------------------- |
| Contradictory       | `AUTHORITY_EVIDENCE_INVALID`      |
| Ambiguous           | `AUTHORITY_EVIDENCE_INVALID`      |
| Invalid             | `AUTHORITY_EVIDENCE_INVALID`      |
| Revoked             | `AUTHORITY_EVIDENCE_REVOKED`      |
| Stale               | `AUTHORITY_EVIDENCE_STALE`        |
| Out of scope        | `AUTHORITY_EVIDENCE_OUT_OF_SCOPE` |

## Provisional future artifact paths

Record the following future paths as governed targets, not created artifacts.

### Schema

`schemas/sniperbot-options-eligibility-exclusion-decision.schema.json`

### Production module

`src/sniperbot/options/eligibility_decision.py`

### Direct tests

`tests/test_sniperbot_options_eligibility_exclusion.py`

### Future acceptance record

`docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-options-eligibility-exclusion-implementation-evidence-acceptance.md`

State that schema, source, tests, and acceptance documentation require separate founder authorization.

## Decision Boundary and Next Founder Decision

These 70 decisions close the founder-decision surface only. They establish
closed vocabularies, request and decision boundaries, precedence, authority
handling, exact future API requirements, purity constraints, evidence
requirements, and governed future paths without creating any schema, source,
test, implementation, integration, runtime, trading, or execution capability.

The exact next founder decision is whether to authorize bounded implementation
of the Options Eligibility / Exclusion decision schema.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized.
