# SniperBot Stage 2 Crypto Deferral / No-Action Founder Decision Record

## Status and Boundary

Documentation-only / governance-only / founder-decision-record-only /
crypto-specific / non-runtime / non-execution / non-authorizing.

Repository: `heliosfi/Echoauth-core`
Starting checkpoint: `fffa3e43fd6629075e9eba955ff86ae16a55e13b`.

This record contains the 18 founder-approved decisions for the future pure
Crypto Deferral / No-Action Decision Contract. These decisions authorize only
the future bounded contract, schema, and evaluator sequence when each step is
separately ordered. This record does not authorize a schema, Python package,
evaluator, tests, integration, runtime, exchange, wallet, market-data,
strategy, risk, broker, order, execution, another Stage 2 subject, or Stage 3.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized. EchoAuth
remains the sole permission authority.

## Founder Decisions

1. **`CRYPTO-DECISION-01` — `DEFER_AND_NO_ACTION_ONLY`**: Outcomes are
   exactly `DEFER` and `NO_ACTION`. Neither conveys eligibility, asset
   approval, permission, strategy, order, transfer, or execution authority.
2. **`CRYPTO-DECISION-02` — `FOUNDER_DEFINED_CRYPTO_REASON_SET`**: The closed
   reason vocabulary has exactly 22 values listed below. Unknown raw values,
   aliases, free text, and an unapproved `UNKNOWN` reason are rejected.
3. **`CRYPTO-DECISION-03` — `REUSE_FIVE_VALUE_SET_WITH_EXPLICIT_SUBSET`**:
   The full RequiredAction vocabulary has five values. Only `NONE`,
   `HUMAN_REVIEW`, and `GOVERNANCE_REVIEW` are emittable;
   `FOUNDER_AUTHORITY_REQUIRED` and `RESET_REQUIRED` are vocabulary-only.
4. **`CRYPTO-DECISION-04` — `MANDATORY_OPAQUE_CRYPTO_REFERENCE`**:
   `crypto_reference` and `correlation_reference` are mandatory, non-empty,
   opaque strings preserved exactly. They are not parsed as symbols, tokens,
   addresses, chains, venues, wallets, accounts, or market identifiers.
5. **`CRYPTO-DECISION-05` — `EXTERNAL_DESCRIPTIVE_DEFERRAL_FACT`**: With no
   higher condition, `crypto_deferral = true` maps to `DEFER`,
   `CRYPTO_DEFERRAL_EXTERNALLY_REQUIRED`, `HUMAN_REVIEW`. It describes a pause
   for review and is not rejection, eligibility, timing, strategy, or future
   permission.
6. **`CRYPTO-DECISION-06` — `EXPLICIT_AND_FALLBACK_SHARE_MAPPING`**: Explicit
   Crypto no-action and the ordinary fallback both map to `NO_ACTION`,
   `NO_ACTION_REQUIRED`, `NONE`. No-action is not approval, asset handling,
   position handling, transfer, order, or execution.
7. **`CRYPTO-DECISION-07` — `EXPLICIT_CLOSED_BOOLEAN_EVIDENCE`**: Evidence is
   represented only by `crypto_evidence_present`, `crypto_evidence_current`,
   `crypto_evidence_sufficient`, and `crypto_evidence_contradictory`, all
   strict Booleans. Only an explicit true contradiction flag establishes
   Crypto-evidence contradiction; no external fact is inferred.
8. **`CRYPTO-DECISION-08` — `SEPARATE_EXTERNAL_DESCRIPTIVE_FACTS`**:
   `crypto_excluded` and `crypto_restricted` are separate strict Boolean facts.
   Exclusion maps to `NO_ACTION`, `CRYPTO_EXCLUDED`, `NONE`; restriction maps
   to `NO_ACTION`, `CRYPTO_RESTRICTED`, `NONE`; exclusion precedes restriction.
   Neither fact is calculated, verified, changed, or treated as eligibility.
9. **`CRYPTO-DECISION-09` — `OPTIONAL_FIELD_WITH_FAIL_CLOSED_ABSENCE`**:
   `crypto_lane_confirmation` is optional with values `CONFIRMED`,
   `NOT_CONFIRMED`, and `CONTRADICTORY`. Missing, contradictory, and
   not-confirmed values map respectively to `CRYPTO_LANE_CONFIRMATION_MISSING`,
   `CRYPTO_LANE_CONTRADICTORY`, and `CRYPTO_LANE_NOT_CONFIRMED`, each with
   `NO_ACTION` and `GOVERNANCE_REVIEW`. Crypto is never inferred.
10. **`CRYPTO-DECISION-10` — `OPTIONAL_NON_AUTHORIZING_CRYPTO_COMPATIBILITY_CONTEXT`**:
    Generic Asset-Class context is optional, opaque, independent, and
    non-authorizing. Its AssetClass vocabulary is `STOCK`, `OPTIONS`,
    `CRYPTO`; only `CRYPTO` is compatible. The generic evaluator is not
    imported, called, invoked, or orchestrated.
11. **`CRYPTO-DECISION-11` — `STRUCTURAL_SEPARATION_ONLY`**: Stock and Options
    may inform structural rigor only. Their meanings, codes, inputs, outputs,
    calls, orchestration, and authority are not inherited. Their accepted
    files remain unchanged and parked.
12. **`CRYPTO-DECISION-12` — `OPTIONAL_CONTEXTUAL_ONLY`**: EchoAuth authority
    evidence is optional, externally supplied, opaque, and contextual. Failure
    order is contradictory, ambiguous, invalid, revoked, stale, then out of
    scope. EchoAuth is never called, validated, repaired, broadened, granted,
    replaced, reinterpreted, or bypassed.
13. **`CRYPTO-DECISION-13` — `CONFLICT_GOVERNANCE_REVIEW`**: Simultaneous
    Crypto deferral and no-action maps to `NO_ACTION`,
    `CRYPTO_DEFERRAL_NO_ACTION_CONFLICT`, `GOVERNANCE_REVIEW`. This is distinct
    from evidence contradiction.
14. **`CRYPTO-DECISION-14` — `FOUNDER_DEFINED_ORDERED_FIRST_MATCH`**: The
    future evaluator uses the exact 20-step first-match order below. A lower
    condition cannot change the selected result.
15. **`CRYPTO-DECISION-15` — `REJECT_UNKNOWN_AND_CLASSIFY_CLOSED_UNDEFINED_SET`**:
    Unknown raw enums, invalid nested objects, empty required references,
    non-Boolean Boolean fields, unexpected schema properties, and wrong typed
    objects are rejected without coercion. Exactly three typed undefined
    predicates map through the governed undefined branch below.
16. **`CRYPTO-DECISION-16` — `PURE_FROZEN_PUBLIC_API`**: The future surface is
    immutable, pure, side-effect-free, exact-reference-preserving, and limited
    to the approved request, decision, and 12 public symbols below.
17. **`CRYPTO-DECISION-17` — `EXPLICIT_FOUNDER_NAMED_PATHS`**: The exact future
    paths are listed below. This record does not authorize creating them.
18. **`CRYPTO-DECISION-18` — `FULL_CONTRACT_AUTHORITY_SUITE_AND_SCOPE_SCAN`**:
    Future authorized work requires JSON parsing, exact vocabulary and
    schema/implementation parity, focused, Contract, Authority Clarity, and
    canonical full-suite tests, diff and scope checks, prohibited-import and
    side-effect inspection, and a clean final state. The canonical full-suite
    command is `& $python -B -m unittest discover -s tests`.

## Closed Vocabularies

Outcomes (2): `DEFER`, `NO_ACTION`.

Reason codes (22):

`CRYPTO_DEFERRAL_EXTERNALLY_REQUIRED`, `CRYPTO_EVIDENCE_MISSING`,
`CRYPTO_EVIDENCE_STALE`, `CRYPTO_EVIDENCE_INSUFFICIENT`,
`CRYPTO_EVIDENCE_CONTRADICTORY`, `CRYPTO_DEFERRAL_NO_ACTION_CONFLICT`,
`CRYPTO_RESTRICTED`, `CRYPTO_EXCLUDED`,
`CRYPTO_LANE_CONFIRMATION_MISSING`, `CRYPTO_LANE_NOT_CONFIRMED`,
`CRYPTO_LANE_CONTRADICTORY`, `GENERIC_ASSET_CLASS_CONTEXT_INVALID`,
`GENERIC_ASSET_CLASS_CONTEXT_STALE`,
`GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY`,
`GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE`, `GENERIC_ASSET_CLASS_NOT_CRYPTO`,
`AUTHORITY_EVIDENCE_INVALID`, `AUTHORITY_EVIDENCE_STALE`,
`AUTHORITY_EVIDENCE_REVOKED`, `AUTHORITY_EVIDENCE_OUT_OF_SCOPE`,
`UNDEFINED_INPUT_COMBINATION`, `NO_ACTION_REQUIRED`.

RequiredAction values (5): `NONE`, `HUMAN_REVIEW`, `GOVERNANCE_REVIEW`,
`FOUNDER_AUTHORITY_REQUIRED`, `RESET_REQUIRED`.

Emittable actions (3): `NONE`, `HUMAN_REVIEW`, `GOVERNANCE_REVIEW`.

Crypto-lane confirmation values (3): `CONFIRMED`, `NOT_CONFIRMED`,
`CONTRADICTORY`.

AssetClass values (3): `STOCK`, `OPTIONS`, `CRYPTO`.

Context and authority validity values (3): `VALID`, `INVALID`, `AMBIGUOUS`.

## Exact Typed Contract

The future `CryptoRequest` has exactly these fields:

* `crypto_reference: str`
* `crypto_evidence_present: bool`
* `crypto_evidence_current: bool`
* `crypto_evidence_sufficient: bool`
* `crypto_evidence_contradictory: bool`
* `crypto_deferral: bool`
* `crypto_no_action: bool`
* `crypto_restricted: bool`
* `crypto_excluded: bool`
* `correlation_reference: str`
* `crypto_lane_confirmation: CryptoLaneConfirmation | None = None`
* `generic_asset_class_context: GenericAssetClassContext | None = None`
* `authority_evidence: AuthorityEvidence | None = None`

The eight strict Boolean Crypto facts are the four evidence facts plus
`crypto_deferral`, `crypto_no_action`, `crypto_restricted`, and
`crypto_excluded`.

`GenericAssetClassContext` has exactly `asset_class`, `validity`, `current`,
`contradictory`, `in_scope`, and non-empty opaque `context_reference` fields.
The last three status fields are strict Booleans.

`AuthorityEvidence` has exactly `validity`, `current`, `revoked`,
`contradictory`, `in_scope`, and non-empty opaque `evidence_reference` fields.
The four status fields are strict Booleans.

The future `Decision` has exactly `crypto_reference`, `outcome`, `reason_code`,
`required_action`, and `correlation_reference`. Both references equal their
request values exactly.

## Exact First-Match Precedence

1. `crypto_evidence_contradictory` → `NO_ACTION` /
   `CRYPTO_EVIDENCE_CONTRADICTORY` / `HUMAN_REVIEW`.
2. Deferral and no-action both true → `NO_ACTION` /
   `CRYPTO_DEFERRAL_NO_ACTION_CONFLICT` / `GOVERNANCE_REVIEW`.
3. Any governed undefined predicate → `NO_ACTION` /
   `UNDEFINED_INPUT_COMBINATION` / `GOVERNANCE_REVIEW`.
4. Lane confirmation missing → `NO_ACTION` /
   `CRYPTO_LANE_CONFIRMATION_MISSING` / `GOVERNANCE_REVIEW`.
5. Lane confirmation contradictory → `NO_ACTION` /
   `CRYPTO_LANE_CONTRADICTORY` / `GOVERNANCE_REVIEW`.
6. Lane not confirmed → `NO_ACTION` / `CRYPTO_LANE_NOT_CONFIRMED` /
   `GOVERNANCE_REVIEW`.
7. Generic context contradictory → `NO_ACTION` /
   `GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY` / `GOVERNANCE_REVIEW`.
8. Generic context ambiguous or invalid → `NO_ACTION` /
   `GENERIC_ASSET_CLASS_CONTEXT_INVALID` / `GOVERNANCE_REVIEW`.
9. Generic asset class is not `CRYPTO` → `NO_ACTION` /
   `GENERIC_ASSET_CLASS_NOT_CRYPTO` / `GOVERNANCE_REVIEW`.
10. Generic context stale → `NO_ACTION` /
    `GENERIC_ASSET_CLASS_CONTEXT_STALE` / `GOVERNANCE_REVIEW`.
11. Generic context out of scope → `NO_ACTION` /
    `GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE` / `GOVERNANCE_REVIEW`.
12. Crypto excluded → `NO_ACTION` / `CRYPTO_EXCLUDED` / `NONE`.
13. Crypto restricted → `NO_ACTION` / `CRYPTO_RESTRICTED` / `NONE`.
14. First authority failure under its sub-precedence → `NO_ACTION` /
    corresponding authority reason / `GOVERNANCE_REVIEW`.
15. Evidence missing → `DEFER` / `CRYPTO_EVIDENCE_MISSING` / `HUMAN_REVIEW`.
16. Evidence stale → `DEFER` / `CRYPTO_EVIDENCE_STALE` / `HUMAN_REVIEW`.
17. Evidence insufficient → `DEFER` / `CRYPTO_EVIDENCE_INSUFFICIENT` /
    `HUMAN_REVIEW`.
18. External deferral → `DEFER` / `CRYPTO_DEFERRAL_EXTERNALLY_REQUIRED` /
    `HUMAN_REVIEW`.
19. Explicit no-action → `NO_ACTION` / `NO_ACTION_REQUIRED` / `NONE`.
20. Ordinary fallback → `NO_ACTION` / `NO_ACTION_REQUIRED` / `NONE`.

Generic-context sub-precedence is contradictory, ambiguous or invalid,
asset class not `CRYPTO`, stale, then out of scope. Authority sub-precedence
is contradictory, ambiguous, invalid, revoked, stale, then out of scope.
Contradictory, ambiguous, and invalid authority all use
`AUTHORITY_EVIDENCE_INVALID`; the remaining failures use their matching
authority reasons.

## Governed Undefined Predicates

Exactly these three typed predicates use branch 3:

1. evidence absent while current;
2. evidence absent while sufficient;
3. evidence stale while sufficient.

## Approved Public API

The future public API contains exactly these 12 symbols:

`Outcome`, `ReasonCode`, `EmittableReasonCode`, `RequiredAction`,
`CryptoLaneConfirmation`, `AssetClass`, `GenericAssetClassContext`,
`AuthorityEvidence`, `CryptoRequest`, `Decision`, `create_request`, `evaluate`.

## Approved Future Paths

These paths are approved as boundaries for separately authorized future work;
they are not authorized for creation by this record:

* `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-crypto-deferral-no-action-founder-decision-record.md`
* `schemas/sniperbot-crypto-deferral-no-action-decision.schema.json`
* `src/sniperbot/crypto/__init__.py`
* `src/sniperbot/crypto/deferral_decision.py`
* `tests/test_sniperbot_crypto_deferral_no_action.py`

## Validation and Stop Conditions

Future authorized lanes use only:

```powershell
$python = 'C:\Users\kingc\AppData\Local\Programs\Python\Python311\python.exe'
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONNOUSERSITE = '1'

& $python -B -m json.tool `
  schemas\sniperbot-crypto-deferral-no-action-decision.schema.json `
  > $null

& $python -B -m unittest tests.test_sniperbot_crypto_deferral_no_action

& $python -B -m unittest `
  tests.test_contract_validation `
  tests.test_authority_clarity_gate_validation

& $python -B -m unittest discover -s tests

git diff --check
git diff --cached --check
git status --short --branch
git diff --name-only
git diff --cached --name-only
```

Validation must also prove exact vocabulary and schema/implementation parity,
all 20 mappings and precedence relations, the three undefined predicates,
frozen structures, exact reference preservation, input non-mutation, strict
raw enum/Boolean/reference/nested-object rejection, exact public exports,
prohibited imports, absence of side effects, exact authorized-file scope, and
a clean final repository state.

Stop on any failed command, vocabulary mismatch, ambiguous precedence,
unexpected file, new authority meaning, prohibited import, side effect,
integration, dependency, workflow, configuration, validator, archive, runtime,
execution, another Stage 2 subject, or Stage 3 movement.

## Prohibited Surfaces and Next Decision

This contract excludes token or coin eligibility, asset approval, exchange
selection, wallet selection or access, address validation, private keys, seed
phrases, credentials, custody, deposits or withdrawals, blockchain or node
access, chain analysis, market-data retrieval, pricing, liquidity, slippage,
strategy, risk, sizing, simulation, paper trading, broker or exchange APIs,
orders, routing, execution, runtime wiring, another Stage 2 subject, and
Stage 3.

The exact next founder decision is whether to authorize a separate bounded
Crypto Deferral / No-Action decision-schema task order. This record creates no
schema or implementation authority. Stage 2 remains **HOLD**. Stage 3 remains
unentered and unauthorized.
