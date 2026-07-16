# SniperBot Live-Money Readiness Ladder Stage 2 Asset-Class Eligibility / Exclusion Founder Decision Record

## Status and Boundary

Documentation-only / governance-only / founder-decision-record-only /
non-runtime / non-execution / non-authorizing.

This record resolves the 20 founder decisions for the bounded future
**SniperBot Stage 2 — Asset-Class Eligibility / Exclusion Decision Contract**.
It authorizes no schema, package, implementation, tests, evaluator
orchestration, Deferral integration, lane-specific eligibility, runtime,
trading, execution, another Stage 2 subject, or Stage 3 movement.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized. EchoAuth
remains the sole permission authority.

## Founder Decisions

1. **`ASSET-ELIGIBILITY-DECISION-01` — `STOCK_OPTIONS_CRYPTO_ONLY`**:
   `asset_class` is exactly one explicitly supplied value from `STOCK`,
   `OPTIONS`, and `CRYPTO`. Unknown raw values are rejected before typed
   construction. Asset class is never inferred from identifiers, contracts,
   tokens, brokers, exchanges, wallets, venues, market data, or metadata.
2. **`ASSET-ELIGIBILITY-DECISION-02` — `FOUR_DISTINCT_NON_AUTHORIZING_OUTCOMES`**:
   Outcomes are exactly `ELIGIBLE`, `EXCLUDED`, `RESTRICTED`, and
   `REVIEW_REQUIRED`. None conveys permission, access, asset approval, order
   authority, transaction authority, or execution authority.
3. **`ASSET-ELIGIBILITY-DECISION-03` — `CONTINUED_GOVERNED_STAGE_2_EVALUATION_ONLY`**:
   `ELIGIBLE` means only that supplied evidence supports continued governed
   Stage 2 evaluation of the named lane. With no higher condition, external
   eligibility maps to `ELIGIBLE / ASSET_CLASS_ELIGIBLE / NONE`. `NONE` means
   no additional action from this classifier and never means permission.
4. **`ASSET-ELIGIBILITY-DECISION-04` — `DISTINCT_TERMINAL_WITHIN_CLASSIFIER_OUTCOME`**:
   External exclusion maps to `EXCLUDED / ASSET_CLASS_EXCLUDED / NONE` and is
   terminal only within this evaluator. The classifier cannot calculate,
   verify, derive, modify, remove, override, narrow, or broaden exclusion.
5. **`ASSET-ELIGIBILITY-DECISION-05` — `DISTINCT_RESTRICTED_OUTCOME_WITH_HUMAN_REVIEW`**:
   External restriction maps to `RESTRICTED / ASSET_CLASS_RESTRICTED /
   HUMAN_REVIEW`. Continued governed consideration pauses for bounded human
   review. Restriction is not exclusion, eligibility, permission, selection,
   access, trading, or execution.
6. **`ASSET-ELIGIBILITY-DECISION-06` — `FOUNDER_DEFINED_ASSET_CLASS_ELIGIBILITY_REASON_SET`**:
   The closed reason vocabulary is the exact 15-value set below. `UNKNOWN`,
   free text, aliases, hidden fallbacks, Deferral reasons, and lane-specific
   reasons are prohibited.
7. **`ASSET-ELIGIBILITY-DECISION-07` — `REUSE_FIVE_VALUE_SET_WITH_THREE_EMITTABLE`**:
   RequiredAction uses the exact five-value repository vocabulary below. Only
   `NONE`, `HUMAN_REVIEW`, and `GOVERNANCE_REVIEW` are emittable.
   `FOUNDER_AUTHORITY_REQUIRED` and `RESET_REQUIRED` must be rejected by the
   future decision structure.
8. **`ASSET-ELIGIBILITY-DECISION-08` — `NO_SEPARATE_LANE_CONFIRMATION_FIELD`**:
   The closed typed `asset_class` is sufficient. No lane-confirmation Boolean,
   enum, missing-lane reason, or contradictory-lane reason is authorized.
9. **`ASSET-ELIGIBILITY-DECISION-09` — `GOVERNANCE_REVIEW_CONFLICT`**:
   Eligible plus excluded maps to `REVIEW_REQUIRED /
   ELIGIBLE_EXCLUDED_CONFLICT / GOVERNANCE_REVIEW`, immediately after external
   evidence contradiction. Eligibility cannot override exclusion.
10. **`ASSET-ELIGIBILITY-DECISION-10` — `RESTRICTION_SUPPRESSES_ELIGIBILITY_WITH_DEDICATED_CONFLICT`**:
    Eligible plus restricted maps to `RESTRICTED /
    ELIGIBLE_RESTRICTED_CONFLICT / HUMAN_REVIEW`, after eligible/excluded and
    before undefined combinations. Eligibility cannot override restriction.
11. **`ASSET-ELIGIBILITY-DECISION-11` — `EXCLUSION_PRECEDES_RESTRICTION`**:
    Excluded plus restricted without eligible maps to `EXCLUDED /
    ASSET_CLASS_EXCLUDED / NONE`. This is governed precedence, not a
    contradiction, undefined combination, or new reason.
12. **`ASSET-ELIGIBILITY-DECISION-12` — `EXTERNAL_FLAG_PLUS_CLOSED_CONFLICT_LIST`**:
    The highest block is external evidence contradiction, eligible/excluded,
    then eligible/restricted. Only `eligibility_evidence_contradictory = true`
    triggers evidence contradiction, mapping to `REVIEW_REQUIRED /
    ELIGIBILITY_EVIDENCE_CONTRADICTORY / HUMAN_REVIEW`. No open-ended
    contradiction inference is authorized.
13. **`ASSET-ELIGIBILITY-DECISION-13` — `FOUNDER_DEFINED_ORDERED_FIRST_MATCH`**:
    The exact first-match precedence and mappings are recorded below. A lower
    condition cannot alter the selected result.
14. **`ASSET-ELIGIBILITY-DECISION-14` — `UNRESOLVED_GOVERNANCE_REVIEW`**:
    When evidence is present, current, and sufficient and no contradiction,
    conflict, undefined combination, exclusion, restriction, authority
    failure, or external eligible fact applies, return `REVIEW_REQUIRED /
    ELIGIBILITY_UNRESOLVED / GOVERNANCE_REVIEW`. Absence of negative posture
    never implies eligibility.
15. **`ASSET-ELIGIBILITY-DECISION-15` — `OPTIONAL_CONTEXTUAL_ONLY`**:
    Bounded EchoAuth evidence is optional contextual input. Absence creates no
    failure, permission, or eligibility. Supplied evidence uses the closed
    subprecedence and mappings below. Valid evidence only permits evaluation
    to continue; it does not establish eligibility or authority.
16. **`ASSET-ELIGIBILITY-DECISION-16` — `RESERVED_FOR_FUTURE_INTEGRATION_ONLY`**:
    Asset-Class Deferral / No-Action context is excluded. Neither evaluator
    invokes, imports for execution, modifies, duplicates, overrides, or
    converts the other. Any relationship requires a separate founder-authorized
    integration contract and task order.
17. **`ASSET-ELIGIBILITY-DECISION-17` — `INDEPENDENT_UNTIL_FUTURE_INTEGRATION_AUTHORITY`**:
    Generic Asset-Class Eligibility / Exclusion remains independent from
    future Stock, Options, and Crypto eligibility subjects. No lane-specific
    results, individual-asset facts, downstream evaluator calls, or automatic
    cross-lane precedence are authorized.
18. **`ASSET-ELIGIBILITY-DECISION-18` — `STRICT_RAW_REJECTION_AND_EXACTLY_THREE_UNDEFINED_COMBINATIONS`**:
    Unknown enums, unsupported asset classes, non-Boolean Boolean inputs,
    empty required references, invalid nested objects, unknown authority
    values, and free-text replacements are rejected before typed construction.
    No coercion or `UNKNOWN` member is allowed. Exactly three typed undefined
    predicates use the governed mapping below; no others may be inferred.
19. **`ASSET-ELIGIBILITY-DECISION-19` — `APPROVE_EXACT_FOUR_FILE_BOUNDARY`**:
    The four future paths below are approved as boundaries only. This record
    does not authorize their creation. Accepted Deferral files remain
    unchanged, and no root `sniperbot` export is authorized.
20. **`ASSET-ELIGIBILITY-DECISION-20` — `FULL_CONTRACT_AUTHORITY_SUITE_AND_SCOPE_SCAN`**:
    Future schema and implementation work requires the exact validation and
    stop boundaries below, using only the verified Python 3.11 interpreter.

## Closed Vocabularies

AssetClass values (3): `STOCK`, `OPTIONS`, `CRYPTO`.

Outcome values (4): `ELIGIBLE`, `EXCLUDED`, `RESTRICTED`, `REVIEW_REQUIRED`.

ReasonCode values (15):

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

RequiredAction values (5): `NONE`, `HUMAN_REVIEW`, `GOVERNANCE_REVIEW`,
`FOUNDER_AUTHORITY_REQUIRED`, `RESET_REQUIRED`.

Subject-emittable RequiredAction values (3): `NONE`, `HUMAN_REVIEW`,
`GOVERNANCE_REVIEW`.

## Locked Request and Decision Boundaries

The future request may contain only:

* `asset_class`
* non-empty opaque `eligibility_reference`
* `eligibility_evidence_present`
* `eligibility_evidence_current`
* `eligibility_evidence_sufficient`
* `eligibility_evidence_contradictory`
* `asset_class_eligible`
* `asset_class_excluded`
* `asset_class_restricted`
* optional contextual `authority_evidence`
* non-empty opaque `correlation_reference`

The seven eligibility facts are strict Booleans: evidence present, current,
sufficient, contradictory, eligible, excluded, and restricted. No lane
confirmation or Deferral / No-Action context is authorized.

The future decision may contain only the exact asset class, exact eligibility
reference, outcome, reason code, subject-emittable RequiredAction, and exact
correlation reference. It contains no permission, individual-asset selection,
market-data, signal, strategy, risk, sizing, order, transaction, or execution
field.

## Exact First-Match Precedence

1. Eligibility-evidence contradiction → `REVIEW_REQUIRED` /
   `ELIGIBILITY_EVIDENCE_CONTRADICTORY` / `HUMAN_REVIEW`.
2. Eligible plus excluded → `REVIEW_REQUIRED` /
   `ELIGIBLE_EXCLUDED_CONFLICT` / `GOVERNANCE_REVIEW`.
3. Eligible plus restricted → `RESTRICTED` /
   `ELIGIBLE_RESTRICTED_CONFLICT` / `HUMAN_REVIEW`.
4. Any governed undefined predicate → `REVIEW_REQUIRED` /
   `UNDEFINED_INPUT_COMBINATION` / `GOVERNANCE_REVIEW`.
5. External exclusion → `EXCLUDED` / `ASSET_CLASS_EXCLUDED` / `NONE`.
6. External restriction → `RESTRICTED` / `ASSET_CLASS_RESTRICTED` /
   `HUMAN_REVIEW`.
7. First supplied authority failure → its approved `REVIEW_REQUIRED` reason /
   `GOVERNANCE_REVIEW` mapping.
8. Evidence missing → `REVIEW_REQUIRED` / `ELIGIBILITY_EVIDENCE_MISSING` /
   `HUMAN_REVIEW`.
9. Evidence stale → `REVIEW_REQUIRED` / `ELIGIBILITY_EVIDENCE_STALE` /
   `HUMAN_REVIEW`.
10. Evidence insufficient → `REVIEW_REQUIRED` /
    `ELIGIBILITY_EVIDENCE_INSUFFICIENT` / `HUMAN_REVIEW`.
11. External eligible → `ELIGIBLE` / `ASSET_CLASS_ELIGIBLE` / `NONE`.
12. Ordinary fallback → `REVIEW_REQUIRED` / `ELIGIBILITY_UNRESOLVED` /
    `GOVERNANCE_REVIEW`.

## Authority Subprecedence

Optional supplied authority evidence uses this order: contradictory,
ambiguous, invalid, revoked, stale, then out of scope.

* contradictory, ambiguous, or invalid → `REVIEW_REQUIRED` /
  `AUTHORITY_EVIDENCE_INVALID` / `GOVERNANCE_REVIEW`
* revoked → `REVIEW_REQUIRED` / `AUTHORITY_EVIDENCE_REVOKED` /
  `GOVERNANCE_REVIEW`
* stale → `REVIEW_REQUIRED` / `AUTHORITY_EVIDENCE_STALE` /
  `GOVERNANCE_REVIEW`
* out of scope → `REVIEW_REQUIRED` / `AUTHORITY_EVIDENCE_OUT_OF_SCOPE` /
  `GOVERNANCE_REVIEW`

The classifier never calls, independently validates, repairs, reinterprets,
broadens, grants, or bypasses EchoAuth authority.

## Governed Undefined Predicates

Exactly these three constructible typed conditions map to `REVIEW_REQUIRED /
UNDEFINED_INPUT_COMBINATION / GOVERNANCE_REVIEW`:

1. evidence absent while marked current;
2. evidence absent while marked sufficient; and
3. evidence stale while marked sufficient.

Eligible/excluded and eligible/restricted are separately governed conflicts.
Excluded/restricted without eligible uses exclusion precedence. External
evidence contradiction uses its dedicated highest-precedence branch. No other
conflict or undefined predicate may be inferred.

## Approved Future Paths — Not Authorized for Creation

1. `schemas/sniperbot-asset-class-eligibility-exclusion-decision.schema.json`
2. `src/sniperbot/eligibility/__init__.py`
3. `src/sniperbot/eligibility/asset_class_decision.py`
4. `tests/test_sniperbot_asset_class_eligibility_exclusion.py`

## Future Validation and Stop Conditions

Future work must use:

```powershell
$python = 'C:\Users\kingc\AppData\Local\Programs\Python\Python311\python.exe'
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONNOUSERSITE = '1'
```

Mandatory validation includes JSON parsing; exact vocabulary counts;
schema/implementation parity; focused direct, Contract, Authority Clarity,
explicit Authority Clarity Validator, and canonical full-suite tests; both
diff checks; exact file scope; prohibited-import and side-effect inspection;
all branches and higher/lower collisions; the three undefined predicates;
authority subprecedence; exclusion-before-restriction evidence; strict raw
rejection; frozen structures; input non-mutation; deterministic repetition;
equal but distinct decisions; exact asset-class, eligibility-reference, and
correlation-reference preservation; and proof that both vocabulary-only
RequiredAction values are never emitted.

Stop on any failed check, permission-bearing eligibility meaning, unsupported
asset class, ambiguous vocabulary or precedence, individual-asset or venue
eligibility, selection or inference, market data, signals, strategy, risk,
sizing, orders, transactions, execution, EchoAuth reinterpretation, Deferral
invocation or orchestration, lane-specific integration, runtime integration,
dependency, workflow, configuration, validator, or archive change, unexpected
file, unresolved contradiction, repair outside the bounded lane, or Stage 3
movement.

## Decision Boundary and Next Founder Decision

These selections authorize only this founder decision record and its README
index entry. They do not authorize the four future files or any schema,
implementation, test, integration, runtime, trading, execution, neighboring
subject, or Stage 3 work.

The exact next founder decision is whether to authorize a separate bounded
schema-only Asset-Class Eligibility / Exclusion task order.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized.
