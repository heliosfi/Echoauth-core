# SniperBot Stage 2 Crypto Eligibility / Exclusion Implementation-Evidence Acceptance

## Acceptance Status and Boundary

`ACCEPT BOUNDED CRYPTO ELIGIBILITY / EXCLUSION IMPLEMENTATION EVIDENCE`

Repository: `heliosfi/Echoauth-core`

Independent verification checkpoint:
`9b61ca69132a29af403b780ed3a86c31e70e4f06`.

Formal independent verification completed with no contract, schema,
implementation, or direct-test evidence discrepancy. This acceptance covers
only the pure, descriptive Crypto Eligibility / Exclusion evaluator, its
published contract evidence, exact submodule API, frozen data structures,
closed vocabularies, strict typed boundaries, deterministic precedence,
direct tests, reference preservation, purity, and non-mutation.

This evidence acceptance is not integration, runtime activation,
orchestration, market-data, blockchain, exchange, broker, wallet, custody,
routing, order, execution, deployment, live-money, or Stage 3 authority.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized.

## Accepted Provenance and Exact Scope

Accepted contract-definition commit:
`4a19be43f86d9714f1ad4d5f8066d8e45288d8aa` (`Define crypto eligibility
exclusion contract`).

That commit created exactly:

* `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-crypto-eligibility-exclusion-contract-definition-review.md`

Accepted founder-decision commit:
`c3aaad85cadcd123a7ba7aeabd500ba902443572` (`Create crypto eligibility
exclusion founder decision record`).

That commit created exactly:

* `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-crypto-eligibility-exclusion-founder-decision-record.md`

Accepted schema commit:
`9fe9f704b6f3cc465dd2243e48f822127507fee1` (`Add crypto eligibility
exclusion decision schema`).

That commit created exactly:

* `schemas/sniperbot-crypto-eligibility-exclusion-decision.schema.json`

Accepted Python implementation checkpoint:
`41fe2ae15ab0047af6f0c5bd4ea03f93e1996801` (`Implement crypto eligibility
exclusion evaluator`).

That commit created exactly:

* `src/sniperbot/crypto/eligibility_decision.py`

Accepted direct-test evidence checkpoint:
`9b61ca69132a29af403b780ed3a86c31e70e4f06` (`Add crypto eligibility
exclusion evaluator tests`).

That commit is exactly one commit after the implementation checkpoint and
created exactly:

* `tests/test_sniperbot_crypto_eligibility_exclusion.py`

The independent read-only implementation-evidence verification ran at
checkpoint `9b61ca69132a29af403b780ed3a86c31e70e4f06`. The repository remained
unchanged throughout verification.

The accepted schema, implementation, and direct-test surface is exactly:

* `schemas/sniperbot-crypto-eligibility-exclusion-decision.schema.json`
* `src/sniperbot/crypto/eligibility_decision.py`
* `tests/test_sniperbot_crypto_eligibility_exclusion.py`

The accepted production evaluator blob is:

`8ff85031507814ac6cfb092dae848914c1bf1859`

The accepted direct-test blob is:

`174637aa8135b7052c09ba48fe6f9661c7de684d`

No implementation, test, schema, founder record, package initializer,
accepted Crypto Deferral / No-Action file, README, validator, workflow,
dependency, runtime, or integration file changed during independent
verification.

## Accepted Founder-Decision Traceability

The founder-decision record resolves exactly 72 decisions in dependency
order:

* 52 Core Crypto Eligibility / Exclusion decisions;
* 20 Caller-Supplied Context decisions; and
* zero Future Stage 2 decisions.

Independent verification traced all `72/72` decisions. The schema comment
accounts for Decisions 01 through 72, including the decisions that govern
Python-only behavior and the decisions that intentionally create no schema
property.

Caller-supplied venue, exchange, blockchain, network, bridge, wrapped-asset,
stablecoin, wallet, custody, DeFi, smart-contract, liquidity, volatility,
market-condition, tokenomics, jurisdiction, regulation, sanctions,
platform-policy, account-permission, margin, collateral, leverage, and
liquidation facts remain prohibited from the request. Their exclusion from
the bounded type surface creates no authority to retrieve, infer, calculate,
screen, interpret, or act on any such fact.

## Accepted Public API

The accepted public module is exactly:

`sniperbot.crypto.eligibility_decision`

Module `__all__` contains exactly these 12 symbols in this order:

1. `AssetClass`
2. `AuthorityEvidence`
3. `Decision`
4. `GenericAssetClassContext`
5. `Outcome`
6. `ReasonCode`
7. `RequiredAction`
8. `CryptoEligibilityRequest`
9. `CryptoLaneConfirmation`
10. `Validity`
11. `create_request`
12. `evaluate`

No alias, adapter, parser, helper, protocol, wrapper, registry, public
`EmittableAction`, public `EmittableReasonCode`, or additional public symbol
is accepted.

The existing `sniperbot.crypto` package root remains the accepted Crypto
Deferral / No-Action API. Crypto Eligibility / Exclusion symbols are not
re-exported there.

## Accepted Closed String Enums

Exactly six string-valued enums are accepted.

`AssetClass`:

* `STOCK`
* `OPTIONS`
* `CRYPTO`

`CryptoLaneConfirmation`:

* `CONFIRMED`
* `NOT_CONFIRMED`
* `CONTRADICTORY`

`Validity`:

* `VALID`
* `INVALID`
* `AMBIGUOUS`

`Outcome` contains exactly four values:

* `ELIGIBLE`
* `EXCLUDED`
* `RESTRICTED`
* `REVIEW_REQUIRED`

`RequiredAction` contains exactly five values:

* `NONE`
* `HUMAN_REVIEW`
* `GOVERNANCE_REVIEW`
* `FOUNDER_AUTHORITY_REQUIRED`
* `RESET_REQUIRED`

Exactly three required actions are emittable: `NONE`, `HUMAN_REVIEW`, and
`GOVERNANCE_REVIEW`. `FOUNDER_AUTHORITY_REQUIRED` and `RESET_REQUIRED` remain
vocabulary-only and are rejected by `Decision` with `ValueError`.

`ReasonCode` contains exactly these 23 values in this order:

1. `CRYPTO_ELIGIBLE`
2. `CRYPTO_EXCLUDED`
3. `CRYPTO_RESTRICTED`
4. `CRYPTO_ELIGIBILITY_EVIDENCE_MISSING`
5. `CRYPTO_ELIGIBILITY_EVIDENCE_STALE`
6. `CRYPTO_ELIGIBILITY_EVIDENCE_INSUFFICIENT`
7. `CRYPTO_ELIGIBILITY_EVIDENCE_CONTRADICTORY`
8. `CRYPTO_ELIGIBLE_EXCLUDED_CONFLICT`
9. `CRYPTO_ELIGIBLE_RESTRICTED_CONFLICT`
10. `CRYPTO_LANE_CONFIRMATION_MISSING`
11. `CRYPTO_LANE_NOT_CONFIRMED`
12. `CRYPTO_LANE_CONTRADICTORY`
13. `GENERIC_ASSET_CLASS_CONTEXT_INVALID`
14. `GENERIC_ASSET_CLASS_CONTEXT_STALE`
15. `GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY`
16. `GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE`
17. `GENERIC_ASSET_CLASS_NOT_CRYPTO`
18. `AUTHORITY_EVIDENCE_INVALID`
19. `AUTHORITY_EVIDENCE_STALE`
20. `AUTHORITY_EVIDENCE_REVOKED`
21. `AUTHORITY_EVIDENCE_OUT_OF_SCOPE`
22. `UNDEFINED_INPUT_COMBINATION`
23. `CRYPTO_ELIGIBILITY_UNRESOLVED`

No hidden alias, duplicate value, unknown value, free-text reason, generic
catch-all, operational reason, or additional fallback is accepted.

## Accepted Frozen Dataclasses and Typed Construction

Exactly four frozen, equality-enabled dataclasses are accepted.

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

`CryptoEligibilityRequest` contains exactly these fields in this order:

1. `crypto_reference: str`
2. `eligibility_evidence_present: bool`
3. `eligibility_evidence_current: bool`
4. `eligibility_evidence_sufficient: bool`
5. `eligibility_evidence_contradictory: bool`
6. `crypto_eligible: bool`
7. `crypto_excluded: bool`
8. `crypto_restricted: bool`
9. `eligibility_evidence_reference: str`
10. `correlation_reference: str`
11. `crypto_lane_confirmation: CryptoLaneConfirmation | None = None`
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
4. `crypto_reference: str`
5. `eligibility_evidence_reference: str`
6. `correlation_reference: str`

The exact public function signatures are:

```python
def create_request(**values: object) -> CryptoEligibilityRequest:
```

```python
def evaluate(request: CryptoEligibilityRequest) -> Decision:
```

Construction is strict and non-coercing. Evaluation accepts only
`type(request) is CryptoEligibilityRequest`.

## Accepted Omission, Null, Reference, and Exception Boundaries

Omitted `crypto_lane_confirmation` and explicit
`crypto_lane_confirmation=None` both represent missing lane confirmation.

Generic context and authority evidence are optional through omission from
`create_request`. Explicit `generic_asset_class_context=None` or
`authority_evidence=None` through `create_request` is rejected with
`TypeError`. Their dataclass defaults remain `None` for the already-constructed
absence state. The schema permits JSON `null` only for lane confirmation and
uses omission-only generic and authority properties.

Every Boolean field requires exact `bool`. Every enum field requires its exact
enum type. Nested context and authority values require their exact Crypto
dataclass types. Dictionaries, partial objects, subclasses, lookalikes,
alternate representations, and Asset-Class-, Options-, Stock-, and
Deferral-shaped objects are rejected rather than coerced.

Every reference requires exact `str` with at least one non-whitespace
character. Surrounding meaningful whitespace is preserved. References are
never stripped, normalized, parsed, dereferenced, looked up, enriched,
compared, deduplicated, or repaired.

`TypeError` is accepted for wrong exact runtime types, raw enum strings,
non-Boolean Boolean fields, invalid nested representations, subclasses,
explicit generic or authority `None` through `create_request`, missing or
unexpected request keywords, positional `create_request` arguments, and
non-exact request inputs to `evaluate`.

`ValueError` is accepted for empty or whitespace-only references, unknown raw
values at ordinary enum construction, correctly typed values that violate an
exact decision-only boundary, and either non-emittable required action.

Well-formed exact request evaluation is total and does not raise.

## Accepted Equality, Identity, Reference, and Non-Mutation Evidence

Independent verification confirmed for `GenericAssetClassContext`,
`AuthorityEvidence`, `CryptoEligibilityRequest`, and `Decision` that:

* `__dataclass_params__.eq is True`;
* separately constructed equal-valued instances compare equal;
* equal-valued instances are identity-distinct;
* a changed-field instance compares unequal; and
* frozen instances reject mutation.

Independent verification also confirmed:

* exact preservation of `crypto_reference`;
* exact preservation of `eligibility_evidence_reference`;
* exact preservation of `correlation_reference`;
* generic and authority objects and their references remain inside their
  caller-supplied frozen inputs;
* evaluation never mutates a request, nested context, authority object,
  reference, package root, or Crypto Deferral object;
* every evaluation returns a new `Decision`;
* repeated decisions are equal by value and distinct by identity; and
* all caller-supplied context remains descriptive, non-governing,
  non-operational, and non-authorizing.

## Accepted Deterministic Evaluator Precedence

The exact 16-step first-match order and mapping is:

1. Eligibility-evidence contradiction -> `REVIEW_REQUIRED /
   CRYPTO_ELIGIBILITY_EVIDENCE_CONTRADICTORY / HUMAN_REVIEW`
2. Eligible/excluded conflict -> `REVIEW_REQUIRED /
   CRYPTO_ELIGIBLE_EXCLUDED_CONFLICT / GOVERNANCE_REVIEW`
3. Eligible/restricted conflict -> `RESTRICTED /
   CRYPTO_ELIGIBLE_RESTRICTED_CONFLICT / HUMAN_REVIEW`
4. Governed undefined combination -> `REVIEW_REQUIRED /
   UNDEFINED_INPUT_COMBINATION / GOVERNANCE_REVIEW`
5. Crypto-lane confirmation missing -> `REVIEW_REQUIRED /
   CRYPTO_LANE_CONFIRMATION_MISSING / GOVERNANCE_REVIEW`
6. Crypto-lane confirmation contradictory -> `REVIEW_REQUIRED /
   CRYPTO_LANE_CONTRADICTORY / GOVERNANCE_REVIEW`
7. Crypto lane not confirmed -> `REVIEW_REQUIRED /
   CRYPTO_LANE_NOT_CONFIRMED / GOVERNANCE_REVIEW`
8. Generic Asset-Class context failure -> `REVIEW_REQUIRED / exact generic
   reason / GOVERNANCE_REVIEW`
9. Crypto excluded -> `EXCLUDED / CRYPTO_EXCLUDED / NONE`
10. Crypto restricted -> `RESTRICTED / CRYPTO_RESTRICTED / HUMAN_REVIEW`
11. Authority failure -> `REVIEW_REQUIRED / exact authority reason /
    GOVERNANCE_REVIEW`
12. Eligibility evidence missing -> `REVIEW_REQUIRED /
    CRYPTO_ELIGIBILITY_EVIDENCE_MISSING / HUMAN_REVIEW`
13. Eligibility evidence stale -> `REVIEW_REQUIRED /
    CRYPTO_ELIGIBILITY_EVIDENCE_STALE / HUMAN_REVIEW`
14. Eligibility evidence insufficient -> `REVIEW_REQUIRED /
    CRYPTO_ELIGIBILITY_EVIDENCE_INSUFFICIENT / HUMAN_REVIEW`
15. Crypto eligible -> `ELIGIBLE / CRYPTO_ELIGIBLE / NONE`
16. Otherwise unresolved -> `REVIEW_REQUIRED /
    CRYPTO_ELIGIBILITY_UNRESOLVED / GOVERNANCE_REVIEW`

The first match completely determines the descriptive decision. Lower facts
cannot alter the result.

Exactly three governed undefined predicates are accepted:

* `not eligibility_evidence_present and eligibility_evidence_current`
* `not eligibility_evidence_present and eligibility_evidence_sufficient`
* `not eligibility_evidence_current and eligibility_evidence_sufficient`

Independent verification covered all three predicates and all four
constructible nonempty predicate masks. No fourth undefined predicate is
accepted.

## Accepted Generic-Context and Authority Subprecedence

The generic-context six-step sequence is:

1. contradictory
2. ambiguous
3. invalid
4. asset class other than `CRYPTO`
5. stale
6. out of scope

The exact generic mappings are:

* contradictory -> `GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY`
* ambiguous or invalid -> `GENERIC_ASSET_CLASS_CONTEXT_INVALID`
* non-Crypto -> `GENERIC_ASSET_CLASS_NOT_CRYPTO`
* stale -> `GENERIC_ASSET_CLASS_CONTEXT_STALE`
* out of scope -> `GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE`

The authority-evidence six-step sequence is:

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
evaluation to continue. They establish no eligibility and grant no
permission, access, routing, transaction, order, execution, or live-money
authority.

Independent verification passed all 14 logically constructible two-failure
generic-context collisions and all 14 logically constructible two-failure
authority-evidence collisions. Ambiguous versus invalid is not constructible
within either sequence because both are mutually exclusive values of one
`validity` field. Independent single-state witnesses confirmed out-of-scope
as the winning failure when no higher subprecedence condition was active.

## Accepted Schema, Package, Import, and Capability Boundaries

The accepted schema uses JSON Schema Draft 2020-12 and the exact identifier:

`https://echoauth.local/schemas/sniperbot-crypto-eligibility-exclusion-decision.schema.json`

Independent verification confirmed JSON parsing, Draft 2020-12 meta-schema
compliance, and exact schema/API parity for:

* all six closed vocabularies and their exact order;
* request, generic-context, authority-evidence, and decision fields and order;
* requiredness, defaults, omission, null, and additional-property behavior;
* strict Boolean, enum, nested-object, and reference boundaries;
* non-whitespace reference constraints;
* all 72 founder-decision trace references;
* the three-action decision-emittable subset; and
* exclusion of evaluator precedence from the structural schema.

The existing `src/sniperbot/crypto/__init__.py` remains unchanged and
Deferral-only. The accepted Crypto Deferral implementation, schema, tests,
exports, behavior, and acceptance remain unchanged. No eligibility symbol is
re-exported at `sniperbot.crypto`.

Production imports are limited exactly to:

```python
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
```

Independent source, AST, behavior, and package inspection confirmed no
filesystem, environment, logging, telemetry, network, socket, HTTP,
subprocess, inter-process, persistence, database, file, queue, cache,
registration, clock, randomness, mutable hidden state, service, worker,
scheduler, event-publication, runtime, evaluator-chaining, orchestration,
integration, market-data, token or pair resolution, blockchain node or
explorer access, stablecoin analysis, DeFi or smart-contract interaction,
legal or sanctions screening, signal, strategy, risk, sizing, exchange,
broker, account, wallet, custody, credential, transfer, routing, order,
transaction, trading, execution, deployment, or live-money capability. No
third-party production dependency is used.

## Accepted Exhaustive Independent Verification

The governed finite representative model is exactly:

* 16 combinations of the four eligibility-evidence Booleans;
* 8 combinations of the three posture Booleans;
* 4 Crypto-lane states;
* 8 generic-context representatives; and
* 8 authority-evidence representatives.

The independent audit covered:

`16 x 8 x 4 x 8 x 8 = 32,768 combinations`

All `32,768 combinations passed`. The independent oracle was executed
separately from tracked repository files, encoded directly from the founder
record, imported no production-private evaluator helper, and did not use the
published direct tests as its expected-value oracle.

The audit reached all 16 global precedence steps, all 4 outcomes, all 23
reason codes, and exactly the 3 approved emittable actions. It confirmed the
exact outcome/reason/action mapping on every combination, deterministic
repeated evaluation, equal but identity-distinct repeated decisions, exact
reference identity preservation, caller-input non-mutation, totality, and the
fail-closed unresolved fallback.

The exhaustive product covered all constructible global branch interactions
and verified 102 constructible global step-pair collisions. Separate
multi-failure audits passed all 14 generic-context collision witnesses and
all 14 authority-evidence collision witnesses.

## Accepted Direct-Test and Validation Evidence

The published direct-test module contains 21 focused tests and independently
asserts every founder-mandated direct-evidence boundary, including the exact
API, closed vocabularies, frozen dataclasses, strict types, exceptions,
omission/null behavior, cross-lane object rejection, all 16 branches, both
six-step subprecedences, all 28 pairwise subprecedence collisions, all 3
undefined predicates, every reason/action mapping, fallback, references,
purity, non-mutation, schema/API parity, package preservation, imports, and
prohibited-capability absence.

Final independent read-only verification at checkpoint
`9b61ca69132a29af403b780ed3a86c31e70e4f06` recorded:

* focused Crypto Eligibility / Exclusion tests: `21 passed`;
* independent exhaustive audit: `32,768 combinations passed`;
* constructible global collision audit: `102 collisions passed`;
* generic-context pairwise collision audit: `14 collisions passed`;
* authority-evidence pairwise collision audit: `14 collisions passed`;
* Contract Validation: `7 passed`;
* Contract and Authority Clarity tests: `30 passed`;
* Explicit Authority Clarity Validator tests: `23 passed`;
* canonical full suite: `536 passed`;
* all `72/72` founder decisions traced;
* JSON parsing and Draft 2020-12 meta-schema validation: passed;
* schema/API parity: passed;
* strict type and exact exception-boundary checks: passed;
* omission-versus-explicit-`None` checks: passed;
* equality, immutability, identity, and reference-preservation checks: passed;
* purity, determinism, totality, and caller-input non-mutation checks: passed;
* implementation and direct-test commit-scope checks: passed;
* production blob provenance and unchanged-source checks: passed;
* Crypto Deferral and package-root preservation checks: passed;
* production import and prohibited-capability scans: passed;
* whitespace, final-newline, and repository-state checks: passed;
* all validation exit codes: `0`;
* repository state after verification: clean and synchronized;
* Git locks: none; and
* branch divergence: `0/0`.

The independent verification verdict was **PASS**. Discrepancies: **none**.
No missing, weak, circular, implementation-coupled, or otherwise unresolved
contract or evidence gap remains.

## Formal Acceptance Conclusion

The Crypto Eligibility / Exclusion implementation and published direct-test
evidence are accepted as conformant to the governed contract. The lane's
bounded implementation-evidence requirement is complete.

This acceptance applies only to the bounded pure Crypto Eligibility /
Exclusion evaluator and its published contract, founder-decision, schema,
implementation, and direct-test evidence. The evaluator is descriptive and
non-authorizing. An `ELIGIBLE` outcome means only that caller-supplied Crypto
posture may continue to further governed Stage 2 consideration. It is not
approval, selection, recommendation, safety, suitability, support,
tradeability, routability, transfer authority, order authority, execution
authority, or live-money authority. Absence of exclusion or restriction is
never permission.

This acceptance grants no authority for evaluator invocation, integration,
orchestration, runtime registration or activation, market-data access, token
or pair resolution, blockchain node or explorer access, stablecoin analysis,
DeFi or smart-contract interaction, legal interpretation, sanctions
screening, exchange or broker access, account access, wallet access, custody
access, credential access, persistence, networking, registration, signals,
strategy, risk, sizing, allocation, deposits, withdrawals, transfers, routing,
order creation, transaction handling, trading, execution, deployment,
live-money operation, another Stage 2 subject, Stage 2 advancement, or Stage
3 entry.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized. This
acceptance closes only the bounded Crypto Eligibility / Exclusion
implementation-evidence requirement. It does not index this artifact, select
another lane, authorize a successor lane, or authorize any next
implementation or system move.
