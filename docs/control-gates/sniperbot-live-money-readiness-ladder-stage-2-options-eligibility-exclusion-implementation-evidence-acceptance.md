# SniperBot Stage 2 Options Eligibility / Exclusion Implementation-Evidence Acceptance

## Acceptance Status and Boundary

`ACCEPT BOUNDED OPTIONS ELIGIBILITY / EXCLUSION IMPLEMENTATION EVIDENCE`

Repository: `heliosfi/Echoauth-core`

Verification checkpoint:
`7fb1e4abfc90daa100b63f1ba361d46abde86ed4`.

Formal independent verification completed with no unresolved implementation or
direct-test evidence gap. This acceptance covers only the pure, descriptive
Options Eligibility / Exclusion evaluator, its exact module API, frozen data
structures, closed vocabularies, strict typed boundaries, deterministic
precedence, direct tests, reference preservation, non-mutation, and equal but
distinct repeated decisions.

This evidence acceptance is not integration, runtime, orchestration, trading,
execution, or Stage 3 authority.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized.

## Accepted Provenance and Exact Scope

Governing founder-decision checkpoint:
`bcf909ea55992b3e55163661f3f79759ef005d2e` (`Record options eligibility
exclusion founder decisions`).

Schema checkpoint:
`305cb75ae10b050f1f8a8a09f36fab87b39f0b3b` (`Add options eligibility
exclusion decision schema`).

Accepted implementation commit:
`b465be15ab8ac9ef9d2d003e0b87392019b26453` (`Implement options eligibility
exclusion evaluator`).

Accepted direct-test evidence completion commit:
`7fb1e4abfc90daa100b63f1ba361d46abde86ed4` (`Complete options eligibility
exclusion direct-test evidence`).

The implementation commit added exactly:

* `src/sniperbot/options/eligibility_decision.py`
* `tests/test_sniperbot_options_eligibility_exclusion.py`

The direct-test evidence completion commit changed exactly:

* `tests/test_sniperbot_options_eligibility_exclusion.py`

The accepted schema, implementation, and test surface is exactly:

* `schemas/sniperbot-options-eligibility-exclusion-decision.schema.json`
* `src/sniperbot/options/eligibility_decision.py`
* `tests/test_sniperbot_options_eligibility_exclusion.py`

The production evaluator at the evidence-completion checkpoint has the same Git
blob as at the implementation checkpoint:
`93efb33faf3f473e82ac18315bc241e43ee57e02`.

No schema, documentation, package initializer, workflow, dependency, runtime,
integration, orchestration, market-data, broker, wallet, networking,
persistence, registration, order, or execution file changed in either the
direct-test evidence completion commit or the independent re-verification.

## Accepted Public API, Enums, and Structures

The public module is exactly:

`sniperbot.options.eligibility_decision`

Module `__all__` contains exactly these nine symbols in this order:

1. `Outcome`
2. `ReasonCode`
3. `RequiredAction`
4. `Validity`
5. `AuthorityEvidence`
6. `OptionsEligibilityRequest`
7. `Decision`
8. `create_request`
9. `evaluate`

No public `EmittableAction`, alias, or additional public symbol is accepted.

Exactly four closed string enums are accepted:

* `Outcome`: `ELIGIBLE`, `EXCLUDED`, `RESTRICTED`, `REVIEW_REQUIRED`
* `ReasonCode`: the exact 15-value Options Eligibility / Exclusion vocabulary
* `RequiredAction`: `NONE`, `HUMAN_REVIEW`, `GOVERNANCE_REVIEW`,
  `FOUNDER_AUTHORITY_REQUIRED`, `RESET_REQUIRED`
* `Validity`: `VALID`, `INVALID`, `AMBIGUOUS`

The exact 15 reason codes are:

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

Only `NONE`, `HUMAN_REVIEW`, and `GOVERNANCE_REVIEW` are emittable.
`FOUNDER_AUTHORITY_REQUIRED` and `RESET_REQUIRED` remain vocabulary-only and
are rejected by `Decision` with `ValueError`.

Exactly three frozen dataclasses are accepted:

* `AuthorityEvidence`
* `OptionsEligibilityRequest`
* `Decision`

Their field orders, required fields, defaults, and schema representations match
the governing founder decisions and schema exactly.

## Accepted Function and Exception Boundaries

The exact public signatures are:

```python
def create_request(**values: object) -> OptionsEligibilityRequest:
```

```python
def evaluate(request: OptionsEligibilityRequest) -> Decision:
```

The typed API does not coerce raw values. `TypeError` is preserved for wrong
runtime types, raw enum strings, non-Boolean Boolean fields, invalid or
alternate authority objects, explicit `authority_evidence=None` through
`create_request`, unexpected request keywords, and non-request evaluation
input. `ValueError` is preserved for empty required references and correctly
typed values that violate a closed decision-only boundary, including
non-emittable actions.

## Accepted AuthorityEvidence Boundary

`AuthorityEvidence` contains exactly six required fields in this order:

1. `validity`
2. `current`
3. `revoked`
4. `contradictory`
5. `in_scope`
6. `evidence_reference`

No authority field has a default or default factory. The four authority state
fields `current`, `revoked`, `contradictory`, and `in_scope` require exact
Boolean values. `validity` requires the exact `Validity` enum, and
`evidence_reference` is a non-empty opaque string.

Authority evidence is optional by omission only through `create_request`.
Explicit `authority_evidence=None` is rejected. Dictionaries, arbitrary
authority-shaped objects, and Deferral-shaped objects using fields such as
`currentness`, `revocation`, or `scope` are rejected rather than translated or
coerced.

## Accepted Deterministic Evaluator Precedence

The exact 12-step first-match order and mapping is:

1. Eligibility-evidence contradiction -> `REVIEW_REQUIRED /
   OPTIONS_ELIGIBILITY_EVIDENCE_CONTRADICTORY / HUMAN_REVIEW`
2. Eligible/excluded conflict -> `REVIEW_REQUIRED /
   OPTIONS_ELIGIBLE_EXCLUDED_CONFLICT / GOVERNANCE_REVIEW`
3. Eligible/restricted conflict -> `RESTRICTED /
   OPTIONS_ELIGIBLE_RESTRICTED_CONFLICT / HUMAN_REVIEW`
4. Governed undefined combination -> `REVIEW_REQUIRED /
   UNDEFINED_INPUT_COMBINATION / GOVERNANCE_REVIEW`
5. Exclusion -> `EXCLUDED / OPTIONS_EXCLUDED / NONE`
6. Restriction -> `RESTRICTED / OPTIONS_RESTRICTED / HUMAN_REVIEW`
7. Authority failure -> `REVIEW_REQUIRED / approved authority reason /
   GOVERNANCE_REVIEW`
8. Missing eligibility evidence -> `REVIEW_REQUIRED /
   OPTIONS_ELIGIBILITY_EVIDENCE_MISSING / HUMAN_REVIEW`
9. Stale eligibility evidence -> `REVIEW_REQUIRED /
   OPTIONS_ELIGIBILITY_EVIDENCE_STALE / HUMAN_REVIEW`
10. Insufficient eligibility evidence -> `REVIEW_REQUIRED /
    OPTIONS_ELIGIBILITY_EVIDENCE_INSUFFICIENT / HUMAN_REVIEW`
11. Eligible result -> `ELIGIBLE / OPTIONS_ELIGIBLE / NONE`
12. Otherwise unresolved -> `REVIEW_REQUIRED /
    OPTIONS_ELIGIBILITY_UNRESOLVED / GOVERNANCE_REVIEW`

The first match completely determines the descriptive decision. Lower facts
cannot change the result.

Exactly three governed undefined predicates are accepted:

* `not eligibility_evidence_present and eligibility_evidence_current`
* `not eligibility_evidence_present and eligibility_evidence_sufficient`
* `not eligibility_evidence_current and eligibility_evidence_sufficient`

No fourth undefined predicate is accepted.

## Accepted Authority Subprecedence

Authority failures use this exact subprecedence:

1. contradictory
2. ambiguous
3. invalid
4. revoked
5. stale
6. out of scope

All 14 logically possible authority collisions have committed direct evidence.
Ambiguous versus invalid is not constructible because both are mutually
exclusive values of the single `validity` field.

Independent out-of-scope authority evidence returns exactly:

```text
REVIEW_REQUIRED
AUTHORITY_EVIDENCE_OUT_OF_SCOPE
GOVERNANCE_REVIEW
```

Valid or absent authority evidence only permits evaluation to continue. It
grants no eligibility, permission, trading authority, or execution authority.

## Closed Direct-Test Evidence Gap

Independent verification of the implementation checkpoint identified one
bounded committed-evidence gap. The focused test module did not yet directly
prove every required/no-default authority field boundary, every strict
authority Boolean field, alternate and Deferral-shaped authority object
rejection, or out-of-scope authority as an independent winning failure.

Commit `7fb1e4abfc90daa100b63f1ba361d46abde86ed4` closed that gap without changing
production code. It added direct evidence that:

* all six authority fields are required;
* no authority field has a default or default factory;
* all four authority Boolean fields reject non-Boolean values;
* alternate authority-shaped objects are rejected;
* Deferral-shaped authority objects are rejected; and
* out-of-scope authority independently produces the exact governed result.

All prior direct tests were preserved. No unresolved direct-test evidence gap
remains.

## Accepted Purity, Determinism, and Package Boundaries

Independent verification confirmed:

* schema and Python API structural parity;
* exact opaque reference preservation;
* request and authority evidence non-mutation;
* frozen request, authority, and decision dataclasses;
* equal-by-value but distinct repeated decisions;
* deterministic behavior without caching, time, randomness, or hidden state;
* production imports limited to `__future__.annotations`, `dataclass`, and
  `Enum`;
* no package-root broadening or evaluator orchestration; and
* no filesystem, environment, logging, networking, subprocess, persistence,
  registration, runtime, integration, market-data, option-chain, broker,
  Robinhood, wallet, order, routing, transaction, or execution behavior.

The independent exhaustive evaluator audit covered every combination of the
seven request Boolean facts across absent authority and all 48 typed authority
fact combinations:

`6,272 combinations passed`

All 15 reason codes were reached. The exact precedence oracle, reference
preservation, purity, deterministic repetition, and non-mutation checks passed.

## Accepted Validation Evidence

Final independent read-only verification at checkpoint
`7fb1e4abfc90daa100b63f1ba361d46abde86ed4` recorded:

* implementation commit scope: exactly the approved implementation and direct
  test files;
* direct-test evidence completion scope: exactly the direct-test file;
* production evaluator unchanged from the implementation checkpoint: passed;
* schema JSON parse and repository schema validation: passed;
* schema/API structural parity: passed;
* independent structural and exhaustive runtime audit: 6,272 combinations
  passed;
* focused Options Eligibility tests: 18 passed;
* Contract and Authority Clarity tests: 30 passed;
* explicit Authority Clarity Validator tests: 23 passed;
* canonical full suite: 495 passed;
* all validation exit codes: `0`;
* repository state after verification: clean and synchronized; and
* branch divergence: `0/0`.

No unresolved implementation or implementation-evidence gap remains.

## Explicit Acceptance Scope, Exclusions, and Governance Posture

This evaluator is descriptive and non-authorizing. Acceptance grants no
authority for runtime use, integration, evaluator orchestration, market-data or
option-chain access, prices, quotes, Greeks, implied volatility, signals,
strategy, risk, sizing, margin, collateral, assignment, exercise, asset,
symbol, underlying, contract, strike, expiration, spread, broker, exchange,
Robinhood, account, wallet, credential, networking, persistence, registration,
order, transaction, routing, execution, live-money operation, another Stage 2
subject, or Stage 3 entry.

An `ELIGIBLE` result means only eligible for continued governed Stage 2
evaluation. It does not mean tradeable, approved, safe, recommended, routable,
executable, or authorized for live money. Absence of exclusion does not imply
approval or permission.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized. This
acceptance closes only the bounded Options Eligibility / Exclusion
implementation-evidence requirement. It neither selects nor authorizes the
next lane or system move.
