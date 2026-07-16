# SniperBot Stage 2 Crypto Deferral / No-Action Implementation-Evidence Acceptance

## Acceptance Status and Boundary

`ACCEPT BOUNDED CRYPTO DEFERRAL / NO-ACTION IMPLEMENTATION EVIDENCE`

Repository: `heliosfi/Echoauth-core`
Acceptance starting checkpoint: `8250816dac7bdf7786e039a4a1a1a4d52cf79ea9`.

This acceptance covers only the pure SniperBot Crypto Deferral / No-Action
Decision Evaluator, its exact package API, frozen structures, closed
vocabularies, strict typed-input and action boundaries, deterministic
precedence, contextual generic and EchoAuth evidence, direct tests, supplied-
object non-mutation, exact reference preservation, and equal but distinct
repeated decisions. Evidence acceptance is not integration authority.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized.

## Accepted Provenance and Files

Implementation commit:
`93bd254ab695a3de0b7994fca78a62d5662757e0` (`Implement Crypto deferral
no-action evaluator`).

Direct-test evidence commit:
`8250816dac7bdf7786e039a4a1a1a4d52cf79ea9` (`Complete Crypto deferral
no-action test evidence`).

Accepted implementation files:

* `src/sniperbot/crypto/__init__.py`
* `src/sniperbot/crypto/deferral_decision.py`

Accepted direct-test file:

* `tests/test_sniperbot_crypto_deferral_no_action.py`

The governing schema remains unchanged at
`schemas/sniperbot-crypto-deferral-no-action-decision.schema.json`.
The implementation commit added exactly the three accepted files. The
evidence-completion commit changed only the Crypto direct-test file. The root
package, generic Asset-Class, Stock, Options, and Rollback files, schemas,
documentation, workflows, configuration, dependencies, validators, archives,
integration, and runtime surfaces were not changed by those implementation-
evidence commits except for the three accepted files themselves.

## Accepted Package API and Vocabularies

The package exports exactly these 12 symbols:

1. `Outcome`
2. `ReasonCode`
3. `EmittableReasonCode`
4. `RequiredAction`
5. `CryptoLaneConfirmation`
6. `AssetClass`
7. `GenericAssetClassContext`
8. `AuthorityEvidence`
9. `CryptoRequest`
10. `Decision`
11. `create_request`
12. `evaluate`

Committed tests prove `__all__` exists, contains exactly 12 unique names,
equals the approved set, has no missing or extra symbol, and names only
attributes exposed by `sniperbot.crypto`.

Vocabulary counts are exactly 2 outcomes, 22 reason codes, 5 full
`RequiredAction` values, 3 subject-emittable actions, 3 Crypto-lane
confirmation values, and 3 unique generic asset classes. Implementation and
schema vocabularies match exactly. No `UNKNOWN`, alias, free-text reason,
hidden fallback, Stock-specific reason, Options-specific reason, or other
cross-lane reason exists. `FOUNDER_AUTHORITY_REQUIRED` and `RESET_REQUIRED`
are vocabulary-only, non-emittable, rejected by `Decision`, and never emitted.

## Accepted Structures and Input Boundaries

Exactly four structures are frozen dataclasses:

1. `GenericAssetClassContext`
2. `AuthorityEvidence`
3. `CryptoRequest`
4. `Decision`

Each contains exactly its schema-approved fields and no extra field. Evidence
proves strict Boolean enforcement, including rejection of integers, strings,
`None`, and representative objects; empty request, nested, and decision
reference rejection; unknown raw-enum rejection; invalid nested-object and
request-type rejection; unexpected-keyword rejection; opaque Crypto and
correlation references; no coercion; and no unapproved construction fallback.

## Accepted Deterministic Behavior

The exact first-match order is:

1. Crypto evidence contradiction.
2. Crypto deferral/no-action conflict.
3. One of the three governed undefined combinations.
4. Crypto-lane confirmation missing.
5. Crypto-lane confirmation contradictory.
6. Crypto lane not confirmed.
7. Generic context contradictory.
8. Generic context ambiguous or invalid.
9. Generic asset class not `CRYPTO`.
10. Generic context stale.
11. Generic context out of scope.
12. External Crypto exclusion.
13. External Crypto restriction.
14. Supplied authority failure.
15. Crypto evidence missing.
16. Crypto evidence stale.
17. Crypto evidence insufficient.
18. External Crypto deferral.
19. Explicit Crypto no-action.
20. Ordinary no-action fallback.

The first matching branch completely determines the decision; lower facts
cannot alter it. Every valid typed request reaches exactly one deterministic
decision, and all outcome, reason-code, and RequiredAction mappings match the
founder decision record and schema.

## Accepted Undefined Predicates and Precedence Evidence

Exactly three governed predicates exist:

1. evidence absent while marked current;
2. evidence absent while marked sufficient;
3. evidence stale while marked sufficient.

AST-based verification confirmed exactly those three evaluator predicates and
no fourth inferred predicate. All three remain constructible typed requests
and map to `NO_ACTION / UNDEFINED_INPUT_COMBINATION / GOVERNANCE_REVIEW`.

Committed tests cover contradiction over lower categories; conflict over
undefined and lower categories; undefined over lane, context, exclusion,
restriction, authority, evidence, deferral, and no-action; lane and generic-
context failures over lower categories; exclusion over restriction and lower
categories; restriction over authority, evidence, deferral, and no-action;
authority failures over evidence, deferral, explicit no-action, and fallback;
missing over stale and insufficient; stale over insufficient; generic-context
and authority sub-precedence; conflict; external deferral; explicit no-action;
and ordinary fallback.

## Accepted Context, Authority, Restriction, and Exclusion Boundaries

Generic asset-class context is optional, contextual, independent, and non-
authorizing. Only valid `CRYPTO` context permits continued evaluation. The
evaluator does not invoke, import for execution, duplicate, modify, orchestrate,
or inherit authority from a generic evaluator.

EchoAuth evidence is optional, contextual, EchoAuth-owned, and non-authorizing.
Its failure order is contradictory, ambiguous, invalid, revoked, stale, then
out of scope. The evaluator does not call EchoAuth or independently validate,
repair, reinterpret, broaden, grant, or bypass authority.

Restriction and exclusion are externally supplied descriptive facts only.
Exclusion precedes restriction. Neither is calculated, verified, derived,
modified, approved, converted into eligibility or asset selection, or treated
as wallet, order, transaction, or execution authority.

## Accepted Object, Reference, and Repeated-Decision Evidence

Committed tests prove all four structures are frozen; the supplied request,
generic context, and authority evidence remain unchanged; exact Crypto and
correlation references are preserved; independent repeated evaluations return
equal but distinct decision instances; and both decisions are distinct from
the request.

## Accepted Import, Purity, and Validation Evidence

Production imports are limited exactly to `__future__`, `dataclasses`, and
`enum`. Verification found no generic, Stock, Options, or Rollback evaluator
invocation; EchoAuth runtime call; eligibility or asset selection; ticker,
symbol, token, chain, wallet, or address parsing; market data; price; signal;
strategy; risk; sizing; broker; order; credential; blockchain transaction;
persistence; filesystem write; networking; subprocess; logging; environment
access; runtime integration; execution; mutable runtime state; or side effect.

Verified evidence at checkpoint `8250816dac7bdf7786e039a4a1a1a4d52cf79ea9`:

* Crypto schema parse: passed;
* focused Crypto tests: 15 passed;
* Contract and Authority Clarity tests: 30 passed;
* canonical full suite: 452 passed;
* diff and repository checks: passed;
* implementation commit scope: exactly three accepted files;
* evidence-completion commit scope: only the direct-test file; and
* Git state during read-only verification: clean and synchronized.

## Explicit Acceptance Scope, Exclusions, and Governance Posture

This acceptance applies only to evidence at
`93bd254ab695a3de0b7994fca78a62d5662757e0` and
`8250816dac7bdf7786e039a4a1a1a4d52cf79ea9` for the pure evaluator, exact API,
frozen structures, closed vocabularies, strict inputs and actions,
deterministic mappings and precedence, three governed undefined predicates,
contextual generic and EchoAuth boundaries, direct tests, immutability,
non-mutation, reference preservation, and equal but distinct decisions.

It does not accept or authorize integration; generic, Stock, Options, or
Rollback orchestration; eligibility; Crypto asset or token selection; wallet,
blockchain, exchange, or market-data access; signals; strategy; risk; sizing;
simulation; replay; backtesting; brokers; orders; credentials; transactions;
execution; another Stage 2 subject; or Stage 3 entry.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized. No
implementation, integration, neighboring subject, or next candidate begins
automatically. The exact next governance posture is that any next subject
requires separate founder selection and a new bounded task order.
