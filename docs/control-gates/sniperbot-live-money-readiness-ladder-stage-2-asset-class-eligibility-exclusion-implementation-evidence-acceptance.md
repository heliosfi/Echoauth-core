# SniperBot Stage 2 Asset-Class Eligibility / Exclusion Implementation-Evidence Acceptance

## Acceptance Status and Boundary

`ACCEPT BOUNDED ASSET-CLASS ELIGIBILITY / EXCLUSION IMPLEMENTATION EVIDENCE`

Repository: `heliosfi/Echoauth-core`

Verification checkpoint: `dd59f31638cec1d0140e368e60efbce3984ef0aa`.

Formal verification completed with no unresolved evidence gap. This acceptance
covers only the pure, descriptive Asset-Class Eligibility / Exclusion
evaluator, its exact package API, frozen structures, closed vocabularies,
strict typed boundaries, deterministic precedence, direct tests, non-mutation,
reference preservation, and equal but distinct repeated decisions. Evidence
acceptance is not integration, runtime, trading, execution, or Stage 3
authority.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized.

## Accepted Provenance and Surface

Schema checkpoint: `8a60b26c6b30fe05be5aa5e1a30cd33026d79a2d` (`Add
asset-class eligibility exclusion decision schema`).

Python API clarification checkpoint:
`962ea18e4214bc69488fd2580bfbfbd931613be1` (`Clarify asset-class eligibility
Python API contract`).

Accepted implementation checkpoint:
`2cff2b5fa1d12b3026d20eb1c2831085888a8b36` (`Implement asset-class
eligibility exclusion evaluator`).

Accepted direct-test evidence checkpoints:

* `0025143af884a10818145d561e85fc045a4236ed` (`Complete asset-class
  eligibility exclusion test evidence`); and
* `dd59f31638cec1d0140e368e60efbce3984ef0aa` (`Complete asset-class
  eligibility exclusion authority precedence evidence`).

Accepted surface:

* `schemas/sniperbot-asset-class-eligibility-exclusion-decision.schema.json`
* `src/sniperbot/eligibility/__init__.py`
* `src/sniperbot/eligibility/asset_class_decision.py`
* `tests/test_sniperbot_asset_class_eligibility_exclusion.py`

The schema and governing contract records were not changed by the implementation
or evidence commits. The implementation commit added exactly the approved
three files. Each evidence commit changed only the direct-test file.

## Accepted Public API and Structures

The package exports exactly ten symbols:

1. `AssetClass`
2. `Outcome`
3. `ReasonCode`
4. `RequiredAction`
5. `Validity`
6. `AuthorityEvidence`
7. `EligibilityRequest`
8. `Decision`
9. `create_request`
10. `evaluate`

There is no public `EmittableAction` and no additional public API. Exactly five
public enums and three frozen dataclasses exist. Construction and evaluation
are typed and non-coercing. Every evaluation returns a new decision; repeated
evaluations of the same request return equal but distinct decisions.

## Accepted Closed Vocabularies

Asset classes (3): `STOCK`, `OPTIONS`, `CRYPTO`.

Outcomes (4): `ELIGIBLE`, `EXCLUDED`, `RESTRICTED`, `REVIEW_REQUIRED`.

Reason codes (15):

* `ASSET_CLASS_ELIGIBLE`
* `ASSET_CLASS_EXCLUDED`
* `ASSET_CLASS_RESTRICTED`
* `ELIGIBILITY_EVIDENCE_MISSING`
* `ELIGIBILITY_EVIDENCE_STALE`
* `ELIGIBILITY_EVIDENCE_INSUFFICIENT`
* `ELIGIBILITY_EVIDENCE_CONTRADICTORY`
* `ELIGIBLE_EXCLUDED_CONFLICT`
* `ELIGIBLE_RESTRICTED_CONFLICT`
* `AUTHORITY_EVIDENCE_INVALID`
* `AUTHORITY_EVIDENCE_STALE`
* `AUTHORITY_EVIDENCE_REVOKED`
* `AUTHORITY_EVIDENCE_OUT_OF_SCOPE`
* `UNDEFINED_INPUT_COMBINATION`
* `ELIGIBILITY_UNRESOLVED`

Full RequiredAction vocabulary (5): `NONE`, `HUMAN_REVIEW`,
`GOVERNANCE_REVIEW`, `FOUNDER_AUTHORITY_REQUIRED`, `RESET_REQUIRED`.

Emittable subset (3): `NONE`, `HUMAN_REVIEW`, `GOVERNANCE_REVIEW`.

Validity values (3): `VALID`, `INVALID`, `AMBIGUOUS`.

Committed evidence excludes hidden aliases, duplicate values, `UNKNOWN`,
vocabulary drift, hidden fallbacks, and raw-string coercion.

## Accepted AuthorityEvidence Boundary

`AuthorityEvidence` contains exactly six required fields in this order:

1. `validity`
2. `current`
3. `revoked`
4. `contradictory`
5. `in_scope`
6. `evidence_reference`

No field has a default or default factory. `validity` requires the approved
enum; the four state fields require exact Boolean values; and the evidence
reference is a non-empty opaque string. Absence is represented only by
omission. Explicit `None` through `create_request` is rejected. Alternate
Deferral-shaped fields and objects using `currentness`, `revocation`, or
`scope` are rejected rather than translated.

## Accepted Deterministic Behavior

The exact first-match order and mapping is:

1. eligibility-evidence contradiction → `REVIEW_REQUIRED /
   ELIGIBILITY_EVIDENCE_CONTRADICTORY / HUMAN_REVIEW`;
2. eligible/excluded conflict → `REVIEW_REQUIRED /
   ELIGIBLE_EXCLUDED_CONFLICT / GOVERNANCE_REVIEW`;
3. eligible/restricted conflict → `RESTRICTED /
   ELIGIBLE_RESTRICTED_CONFLICT / HUMAN_REVIEW`;
4. governed undefined combination → `REVIEW_REQUIRED /
   UNDEFINED_INPUT_COMBINATION / GOVERNANCE_REVIEW`;
5. exclusion → `EXCLUDED / ASSET_CLASS_EXCLUDED / NONE`;
6. restriction → `RESTRICTED / ASSET_CLASS_RESTRICTED / HUMAN_REVIEW`;
7. authority failure → `REVIEW_REQUIRED / approved authority reason /
   GOVERNANCE_REVIEW`;
8. missing eligibility evidence → `REVIEW_REQUIRED /
   ELIGIBILITY_EVIDENCE_MISSING / HUMAN_REVIEW`;
9. stale eligibility evidence → `REVIEW_REQUIRED /
   ELIGIBILITY_EVIDENCE_STALE / HUMAN_REVIEW`;
10. insufficient eligibility evidence → `REVIEW_REQUIRED /
    ELIGIBILITY_EVIDENCE_INSUFFICIENT / HUMAN_REVIEW`;
11. eligible result → `ELIGIBLE / ASSET_CLASS_ELIGIBLE / NONE`; and
12. unresolved fallback → `REVIEW_REQUIRED / ELIGIBILITY_UNRESOLVED /
    GOVERNANCE_REVIEW`.

The first match fully determines the descriptive result. Lower facts cannot
alter it.

## Accepted Undefined Predicates and Collision Evidence

Exactly three governed undefined predicates exist:

* `not evidence_present and evidence_current`
* `not evidence_present and evidence_sufficient`
* `not evidence_current and evidence_sufficient`

No fourth predicate was found. Tests use logically compatible witnesses for
undefined-versus-lower collisions. They do not invent impossible Boolean
combinations to manufacture evidence. Conflict, undefined, exclusion,
restriction, authority, evidence, eligible, and fallback precedence are
covered according to the approved total order.

## Accepted Authority Subprecedence

Authority failures use this exact order:

1. contradictory
2. ambiguous
3. invalid
4. revoked
5. stale
6. out of scope

All 14 logically possible authority collisions have direct committed evidence.
Ambiguous-versus-invalid is not required because both are mutually exclusive
values of the single `validity` field.

The final completed collision supplies `contradictory = true` and `validity =
INVALID` and returns:

```text
REVIEW_REQUIRED
AUTHORITY_EVIDENCE_INVALID
GOVERNANCE_REVIEW
```

Contradiction wins over invalid validity and lower evaluator branches. The
approved reason vocabulary has no separate authority-contradiction reason.

## Accepted Validation Evidence

Final read-only verification recorded:

* CPython `3.11.9`;
* independent structural/runtime audit: passed;
* schema parse: passed;
* focused eligibility tests: 25 passed;
* Contract and Authority Clarity tests: 30 passed;
* explicit Authority Clarity Validator tests: 23 passed;
* canonical full suite: 477 passed;
* all exit codes: `0`;
* implementation commit scope: exactly three approved files;
* first evidence commit scope: direct-test file only;
* final authority-precedence evidence commit scope: direct-test file only; and
* repository state after verification: clean and synchronized.

No unresolved evidence gap remains.

## Material System Strength

This accepted lane materially strengthens the system through deterministic
asset-class eligibility classification, immutable typed evidence structures,
closed vocabularies, contradiction and conflict detection, fail-closed
unresolved handling, explicit authority subprecedence, resistance to enum and
schema drift, rejection of coercion and alternate authority representations,
non-mutation, deterministic repeated decisions, and regression protection
against precedence changes. This is accumulated system strength, not merely
additional documentation.

Classification remains strictly separate from execution.

## Explicit Acceptance Scope, Exclusions, and Governance Posture

This evaluator is descriptive, not authorizing. Acceptance grants no authority
for evaluator integration, runtime orchestration, lane-specific Stock,
Options, or Crypto permission, signals, strategy, risk, sizing, market data,
asset, ticker, contract, token, wallet, exchange, venue, or broker selection,
orders, transactions, execution, live-money operation, another Stage 2
subject, or Stage 3 entry.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized. The next
system move must be derived from repository state after this acceptance commit.
This order neither selects nor authorizes the next lane.
