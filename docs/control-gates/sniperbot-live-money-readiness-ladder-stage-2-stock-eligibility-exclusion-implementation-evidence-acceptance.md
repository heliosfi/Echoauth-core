# SniperBot Stage 2 Stock Eligibility / Exclusion Implementation-Evidence Acceptance

## Acceptance Status and Boundary

`ACCEPT BOUNDED STOCK ELIGIBILITY / EXCLUSION IMPLEMENTATION EVIDENCE`

Repository: `heliosfi/Echoauth-core`

Independent verification checkpoint:
`ddad1e0fe9d2bcea5929a5095cfd17296fba24b2`.

Formal independent verification completed with no unresolved implementation or
direct-test evidence gap. This acceptance covers only the pure, descriptive
Stock Eligibility / Exclusion evaluator, its exact submodule API, frozen data
structures, closed vocabularies, strict typed boundaries, deterministic
precedence, direct tests, reference preservation, purity, non-mutation, and
equal but distinct value objects.

This evidence acceptance is not integration, runtime, orchestration,
market-data, broker, wallet, order, execution, persistence, networking, or
Stage 3 authority.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized.

## Accepted Provenance and Exact Scope

Accepted contract-definition commit:
`59a57194112a7af5a745d9243bcf058b8d724fbc` (`docs: define stock eligibility
exclusion contract`).

That commit created the bounded contract-definition review and indexed it:

* `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-stock-eligibility-exclusion-contract-definition-review.md`
* `docs/control-gates/README.md`

Accepted founder-decision commit:
`172e300eea4250e92e498b3a5bbe437aed68c70e` (`docs: record stock eligibility
exclusion founder decisions`).

That commit created the founder-decision record and indexed it:

* `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-stock-eligibility-exclusion-founder-decision-record.md`
* `docs/control-gates/README.md`

Accepted schema commit:
`d64e5a2a9a9d402a01fe894b4ad811d64064e1d2` (`Add Stock eligibility exclusion
decision schema`).

That commit created exactly:

* `schemas/sniperbot-stock-eligibility-exclusion-decision.schema.json`

Accepted Python implementation and initial direct-test commit:
`f22faab66007e1100de4a3689ea34f3cfff93bbe` (`Implement stock eligibility
exclusion evaluator`).

That commit created exactly:

* `src/sniperbot/stock/eligibility_decision.py`
* `tests/test_sniperbot_stock_eligibility_exclusion.py`

Accepted dataclass-equality direct-test evidence completion commit:
`ddad1e0fe9d2bcea5929a5095cfd17296fba24b2` (`Complete stock eligibility
dataclass equality evidence`).

That commit changed exactly:

* `tests/test_sniperbot_stock_eligibility_exclusion.py`

The accepted schema, implementation, and direct-test surface is exactly:

* `schemas/sniperbot-stock-eligibility-exclusion-decision.schema.json`
* `src/sniperbot/stock/eligibility_decision.py`
* `tests/test_sniperbot_stock_eligibility_exclusion.py`

The production evaluator at the evidence-completion checkpoint has the same
Git blob as at the implementation checkpoint:

`b073b56a55eaa1d980fcec0a0db49b425eb62c59`

No production implementation, schema, package initializer, accepted Stock
Deferral / No-Action file, documentation, validator, workflow, dependency,
runtime, or integration file changed in the equality evidence completion.

## Accepted Public API

The accepted public module is exactly:

`sniperbot.stock.eligibility_decision`

Module `__all__` contains exactly these 12 symbols in this order:

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

No alias, helper, public `EmittableAction`, public `EmittableReasonCode`, or
additional public symbol is accepted.

The existing `sniperbot.stock` package root remains the accepted Stock
Deferral / No-Action API. Eligibility symbols are not re-exported there.

## Accepted Closed String Enums

Exactly six string-valued enums are accepted.

`AssetClass`:

* `STOCK`
* `OPTIONS`
* `CRYPTO`

`StockLaneConfirmation`:

* `CONFIRMED`
* `NOT_CONFIRMED`
* `CONTRADICTORY`

`Validity`:

* `VALID`
* `INVALID`
* `AMBIGUOUS`

`Outcome`:

* `ELIGIBLE`
* `EXCLUDED`
* `RESTRICTED`
* `REVIEW_REQUIRED`

`RequiredAction`:

* `NONE`
* `HUMAN_REVIEW`
* `GOVERNANCE_REVIEW`
* `FOUNDER_AUTHORITY_REQUIRED`
* `RESET_REQUIRED`

Independent verification confirmed exactly three emittable required actions:
`NONE`, `HUMAN_REVIEW`, and `GOVERNANCE_REVIEW`.
`FOUNDER_AUTHORITY_REQUIRED` and `RESET_REQUIRED` remain vocabulary-only and
are rejected by `Decision` with `ValueError`.

`ReasonCode` contains exactly these 23 governed values:

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

No hidden aliases, duplicate values, unknown value, free-text reason, or
additional fallback is accepted.

## Accepted Frozen Dataclasses and Typed Construction

Exactly four frozen dataclasses are accepted.

`GenericAssetClassContext` contains exactly these six required fields in this
order, with no defaults or default factories:

1. `asset_class: AssetClass`
2. `validity: Validity`
3. `current: bool`
4. `contradictory: bool`
5. `in_scope: bool`
6. `context_reference: str`

`AuthorityEvidence` contains exactly these six required fields in this order,
with no defaults or default factories:

1. `validity: Validity`
2. `current: bool`
3. `revoked: bool`
4. `contradictory: bool`
5. `in_scope: bool`
6. `evidence_reference: str`

`StockEligibilityRequest` contains exactly these fields in this order:

1. `stock_reference: str`
2. `eligibility_evidence_present: bool`
3. `eligibility_evidence_current: bool`
4. `eligibility_evidence_sufficient: bool`
5. `eligibility_evidence_contradictory: bool`
6. `stock_eligible: bool`
7. `stock_excluded: bool`
8. `stock_restricted: bool`
9. `eligibility_evidence_reference: str`
10. `correlation_reference: str`
11. `stock_lane_confirmation: StockLaneConfirmation | None = None`
12. `generic_asset_class_context: GenericAssetClassContext | None = None`
13. `authority_evidence: AuthorityEvidence | None = None`

The first ten request fields are required and have no defaults. Only the final
three fields have the exact default `None`. No request field has a default
factory.

`Decision` contains exactly these six required fields in this order, with no
defaults or default factories:

1. `outcome: Outcome`
2. `reason_code: ReasonCode`
3. `required_action: RequiredAction`
4. `stock_reference: str`
5. `eligibility_evidence_reference: str`
6. `correlation_reference: str`

The exact public function signatures are:

```python
def create_request(**values: object) -> StockEligibilityRequest:
```

```python
def evaluate(request: StockEligibilityRequest) -> Decision:
```

Construction is strict and non-coercing. Evaluation accepts only
`type(request) is StockEligibilityRequest`.

## Accepted Omission, Null, Reference, and Exception Boundaries

Omitted `stock_lane_confirmation` and explicit
`stock_lane_confirmation=None` both represent missing lane confirmation.

Generic context and authority evidence are optional through omission from
`create_request`. Explicit `generic_asset_class_context=None` or
`authority_evidence=None` through `create_request` is rejected with
`TypeError`. Their dataclass defaults remain `None` for the constructed
absence state. The schema permits JSON `null` only for lane confirmation and
uses omission-only generic and authority properties.

Every Boolean field requires exact `bool`. Every enum field requires its exact
enum type. Nested context and authority values require their exact dataclass
types. Dictionaries, subclasses, lookalikes, partial objects, alternate
representations, and Deferral-shaped objects are rejected rather than coerced.

Every reference requires exact `str` with at least one non-whitespace
character. References are never stripped, normalized, parsed, dereferenced,
looked up, or enriched.

`TypeError` is accepted for wrong runtime types, raw enum strings, non-Boolean
Boolean fields, invalid nested representations, explicit generic or authority
`None` through `create_request`, missing or unexpected request keywords,
positional construction through `create_request`, and non-request evaluation
inputs.

`ValueError` is accepted for empty or whitespace-only references, unknown enum
constructor values, and correctly typed values that violate a closed
decision-only boundary, including either non-emittable required action.

Well-formed request evaluation is total and does not raise.

## Accepted Dataclass Equality Evidence

Independent verification originally found one narrowly bounded committed
evidence gap: the initial direct tests did not explicitly prove the governed
equality contract for every frozen dataclass.

Commit `ddad1e0fe9d2bcea5929a5095cfd17296fba24b2` closed that gap without
changing production code. Committed direct evidence now proves, independently
for `GenericAssetClassContext`, `AuthorityEvidence`,
`StockEligibilityRequest`, and `Decision`, that:

* `__dataclass_params__.eq is True`;
* two separately constructed equal-valued instances compare equal;
* the two equal-valued instances are identity-distinct; and
* a changed-field instance compares unequal.

Repeated evaluation also returns decisions that are equal by value and
distinct by object identity. No unresolved dataclass or equality evidence gap
remains.

## Accepted Deterministic Evaluator Precedence

The exact 16-step first-match order and mapping is:

1. Eligibility-evidence contradiction -> `REVIEW_REQUIRED /
   STOCK_ELIGIBILITY_EVIDENCE_CONTRADICTORY / HUMAN_REVIEW`
2. Eligible/excluded conflict -> `REVIEW_REQUIRED /
   STOCK_ELIGIBLE_EXCLUDED_CONFLICT / GOVERNANCE_REVIEW`
3. Eligible/restricted conflict -> `RESTRICTED /
   STOCK_ELIGIBLE_RESTRICTED_CONFLICT / HUMAN_REVIEW`
4. Governed undefined combination -> `REVIEW_REQUIRED /
   UNDEFINED_INPUT_COMBINATION / GOVERNANCE_REVIEW`
5. Stock-lane confirmation missing -> `REVIEW_REQUIRED /
   STOCK_LANE_CONFIRMATION_MISSING / GOVERNANCE_REVIEW`
6. Stock-lane confirmation contradictory -> `REVIEW_REQUIRED /
   STOCK_LANE_CONTRADICTORY / GOVERNANCE_REVIEW`
7. Stock lane not confirmed -> `REVIEW_REQUIRED /
   STOCK_LANE_NOT_CONFIRMED / GOVERNANCE_REVIEW`
8. Generic Asset-Class context failure -> `REVIEW_REQUIRED / exact generic
   reason / GOVERNANCE_REVIEW`
9. Stock excluded -> `EXCLUDED / STOCK_EXCLUDED / NONE`
10. Stock restricted -> `RESTRICTED / STOCK_RESTRICTED / HUMAN_REVIEW`
11. Authority failure -> `REVIEW_REQUIRED / exact authority reason /
    GOVERNANCE_REVIEW`
12. Eligibility evidence missing -> `REVIEW_REQUIRED /
    STOCK_ELIGIBILITY_EVIDENCE_MISSING / HUMAN_REVIEW`
13. Eligibility evidence stale -> `REVIEW_REQUIRED /
    STOCK_ELIGIBILITY_EVIDENCE_STALE / HUMAN_REVIEW`
14. Eligibility evidence insufficient -> `REVIEW_REQUIRED /
    STOCK_ELIGIBILITY_EVIDENCE_INSUFFICIENT / HUMAN_REVIEW`
15. Stock eligible -> `ELIGIBLE / STOCK_ELIGIBLE / NONE`
16. Otherwise unresolved -> `REVIEW_REQUIRED /
    STOCK_ELIGIBILITY_UNRESOLVED / GOVERNANCE_REVIEW`

The first match completely determines the descriptive decision. Lower facts
cannot change the result.

Exactly three governed undefined predicates are accepted:

* `not eligibility_evidence_present and eligibility_evidence_current`
* `not eligibility_evidence_present and eligibility_evidence_sufficient`
* `not eligibility_evidence_current and eligibility_evidence_sufficient`

No fourth undefined predicate is accepted.

## Accepted Generic-Context and Authority Subprecedence

Generic-context failures use this exact order:

1. contradictory
2. ambiguous
3. invalid
4. asset class other than `STOCK`
5. stale
6. out of scope

The exact generic mappings are:

* contradictory -> `GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY`
* ambiguous or invalid -> `GENERIC_ASSET_CLASS_CONTEXT_INVALID`
* non-Stock -> `GENERIC_ASSET_CLASS_NOT_STOCK`
* stale -> `GENERIC_ASSET_CLASS_CONTEXT_STALE`
* out of scope -> `GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE`

Authority failures use this exact order:

1. contradictory
2. ambiguous
3. invalid
4. revoked
5. stale
6. out of scope

The exact authority mappings are:

* contradictory, ambiguous, or invalid -> `AUTHORITY_EVIDENCE_INVALID`
* revoked -> `AUTHORITY_EVIDENCE_REVOKED`
* stale -> `AUTHORITY_EVIDENCE_STALE`
* out of scope -> `AUTHORITY_EVIDENCE_OUT_OF_SCOPE`

Absent or fully valid generic context and authority evidence only permit
evaluation to continue. They grant no eligibility, permission, trading
authority, order authority, or execution authority.

Committed direct tests and independent re-verification each covered all 14
logically possible two-failure generic collisions and all 14 logically
possible two-failure authority collisions. Ambiguous versus invalid is not
constructible because each is a mutually exclusive value of one `validity`
field.

## Accepted Reference, Purity, and Non-Mutation Evidence

Independent verification confirmed:

* exact preservation of `stock_reference`;
* exact preservation of `eligibility_evidence_reference`;
* exact preservation of `correlation_reference`;
* generic and authority references remain inside their caller-supplied input
  objects;
* requests, nested contexts, authority evidence, and decisions are frozen;
* evaluation does not mutate requests, nested objects, references, globals,
  the package root, or any Stock Deferral object;
* evaluation never returns a request or nested input object by identity;
* repeated decisions are equal by value and distinct by identity;
* evaluation is deterministic and total over the approved typed request
  space; and
* no time, randomness, cache, memoization, mutable hidden state, or import-time
  side effect influences a result.

## Accepted Schema, Package, Import, and Capability Boundaries

Independent verification confirmed exact schema/API parity for:

* every closed vocabulary and exact order;
* request, generic-context, authority, and decision fields;
* requiredness, defaults, omission, null, and additional-property behavior;
* strict Boolean and nested-object boundaries;
* non-whitespace reference constraints;
* the three-action emittable subset; and
* the unchanged accepted Stock Deferral / No-Action schema and API.

The existing `src/sniperbot/stock/__init__.py` remains unchanged and
Deferral-only. The accepted Stock Deferral implementation, schema, tests,
exports, behavior, and acceptance remain unchanged. No eligibility symbol is
re-exported at `sniperbot.stock`.

Production imports are limited exactly to:

```python
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
```

Independent source and AST inspection confirmed no filesystem, environment,
logging, telemetry, network, socket, HTTP, subprocess, inter-process,
persistence, database, file, queue, cache, registration, clock, randomness,
service, worker, scheduler, event-publication, runtime, evaluator-chaining,
orchestration, integration, market-data, ticker-resolution, security-selection,
signal, strategy, risk, sizing, broker, Robinhood, exchange, account, wallet,
credential, order, route, transaction, trading, execution, deployment, or
live-money capability. No third-party dependency is used.

## Accepted Exhaustive Independent Verification

The governed finite representative model is exactly:

* 16 combinations of the four eligibility-evidence Booleans;
* 8 combinations of the three posture Booleans;
* 4 lane states;
* 8 generic-context representatives; and
* 8 authority representatives.

The independent audit covered:

`16 x 8 x 4 x 8 x 8 = 32,768 combinations`

All `32,768 combinations passed`. The independent oracle was encoded
separately from production evaluator helpers and separately from the committed
test oracle. It reached all 23 reason codes, emitted exactly `NONE`,
`HUMAN_REVIEW`, and `GOVERNANCE_REVIEW`, preserved all decision references on
every combination, and confirmed determinism, distinct repeated decisions,
and non-mutation.

Independent multi-failure audits also passed all 14 generic-context collision
witnesses and all 14 authority-evidence collision witnesses.

## Accepted Validation Evidence

Final independent read-only re-verification at checkpoint
`ddad1e0fe9d2bcea5929a5095cfd17296fba24b2` recorded:

* focused Stock Eligibility / Exclusion tests: `20 passed`;
* independent exhaustive audit: `32,768 combinations passed`;
* Contract Validation: `7 passed`;
* Contract and Authority Clarity tests: `30 passed`;
* Explicit Authority Clarity Validator tests: `23 passed`;
* canonical full suite: `515 passed`;
* schema/API parity: passed;
* implementation and evidence-completion commit-scope checks: passed;
* production blob provenance and unchanged-production check: passed;
* Stock Deferral and package-root preservation checks: passed;
* production import and prohibited-capability checks: passed;
* scope and prohibited-capability checks: passed;
* whitespace, final newline, and `git diff --check`: passed;
* all validation exit codes: `0`;
* repository state after re-verification: clean and synchronized;
* Git locks: none; and
* branch divergence: `0/0`.

The committed direct-test suite now proves every founder-mandated evidence
requirement. No missing, weak, circular, implementation-coupled, or otherwise
unresolved evidence gap remains after independent verification.

## Formal Acceptance Conclusion

The Stock Eligibility / Exclusion implementation and direct-test evidence are
accepted as conformant to the governed contract. The lane's bounded
implementation-evidence requirement is complete.

This evaluator is descriptive and non-authorizing. An `ELIGIBLE` outcome means
only that the caller-supplied Stock posture may continue to further governed
Stage 2 consideration. It is not approval, selection, safety, suitability,
tradeability, routability, order authority, execution authority, or live-money
authority. Absence of exclusion or restriction is never permission.

This acceptance grants no authority for evaluator invocation, integration,
orchestration, runtime registration, market-data access, ticker or security
resolution, broker access, Robinhood access, exchange access, account access,
wallet access, credential access, persistence, networking, registration,
signals, strategy, risk, sizing, allocation, order creation, routing,
transaction handling, trading, execution, deployment, live-money operation,
another Stage 2 subject, or Stage 3 entry.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized. This
acceptance closes only the bounded Stock Eligibility / Exclusion
implementation-evidence requirement. It does not index this artifact, select
another lane, or authorize any next implementation or system move.
