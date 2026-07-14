# SniperBot Stage 2 Options Deferral / No-Action Founder Decision Record

## Status and Boundary

Documentation-only / governance-only / founder-decision-record-only /
options-specific / non-runtime / non-execution / non-authorizing.

Repository: `heliosfi/Echoauth-core`
Starting checkpoint: `63f0bf5509b485ca7186e0c4c2074e06ac263fd6`.

This record captures the 17 founder decisions for the proposed pure Options
Deferral / No-Action Decision Contract. It authorizes no schema, Python,
tests, package initialization, orchestration, options eligibility, contract
selection, market-data access, signals, strategy, risk, sizing, exercise,
assignment, orders, credentials, persistence, networking, execution, another
Stage 2 subject, or Stage 3 entry.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized.
EchoAuth remains the sole permission authority.

## Founder Decisions

1. **`OPTIONS-DECISION-01` - `DEFER_AND_NO_ACTION_ONLY`**: Outcomes are
   exactly `DEFER` and `NO_ACTION`. Neither is eligibility, contract approval,
   direction, strategy, permission, exercise, assignment, order, or execution
   authority.
2. **`OPTIONS-DECISION-02` - `FOUNDER_DEFINED_OPTIONS_REASON_SET`**: The
   closed reason vocabulary has exactly 22 values listed below. Unknown raw
   values are rejected before typed construction; no stock-specific code,
   free-text replacement, or unapproved `UNKNOWN` reason is allowed.
3. **`OPTIONS-DECISION-03` - `REUSE_FIVE_VALUE_SET_WITH_EXPLICIT_MAPPINGS`**:
   The full RequiredAction vocabulary has five values. Only `NONE`,
   `HUMAN_REVIEW`, and `GOVERNANCE_REVIEW` are subject-emittable;
   `FOUNDER_AUTHORITY_REQUIRED` and `RESET_REQUIRED` are vocabulary-only and
   rejected by the future decision structure.
4. **`OPTIONS-DECISION-04` - `EXTERNAL_DESCRIPTIVE_DEFERRAL_FACT`**: An
   externally supplied deferral fact means options-specific review should
   pause. With no higher condition it maps to `DEFER`,
   `OPTIONS_DEFERRAL_EXTERNALLY_REQUIRED`, `HUMAN_REVIEW`. It is not
   ineligibility, exclusion, data failure, rejection, cancellation, or
   permission.
5. **`OPTIONS-DECISION-05` - `EXPLICIT_AND_ORDINARY_NO_ACTION_SHARE_MAPPING`**:
   Explicit and ordinary no-action map to `NO_ACTION`,
   `NO_ACTION_REQUIRED`, `NONE`. No-action is not approval, eligibility,
   signal, position closure, lifecycle handling, or execution.
6. **`OPTIONS-DECISION-06` - `SEPARATE_EXTERNAL_DESCRIPTIVE_FACTS`**:
   Restriction and exclusion are separate supplied facts. Exclusion maps to
   `NO_ACTION`, `OPTIONS_EXCLUDED`, `NONE`; restriction maps to `NO_ACTION`,
   `OPTIONS_RESTRICTED`, `NONE`; exclusion precedes restriction. Neither is
   calculated, verified, derived, modified, or approved.
7. **`OPTIONS-DECISION-07` - `INDEPENDENT_CLASSIFIERS_WITH_OPTIONAL_CONTEXT`**:
   Generic Asset-Class and Options Deferral remain independent. A generic
   result may be supplied as optional, opaque, non-authorizing context only.
   Neither classifier invokes, orchestrates, imports for execution, or
   inherits authority from the other.
8. **`OPTIONS-DECISION-08` - `STRUCTURAL_SEPARATION_ONLY`**: Options and
   Stock Deferral may share structural governance patterns only. Stock or
   underlying-stock facts cannot become options-lane confirmation,
   eligibility, contract, strategy, exercise, assignment, order, or execution
   authority. Stock files remain unchanged and are not called or orchestrated.
9. **`OPTIONS-DECISION-09` - `OPTIONAL_CONTEXTUAL_OPTIONS_COMPATIBILITY_ONLY`**:
   Generic asset-class context is optional. Absent context has no effect;
   only `OPTIONS` is compatible. Contradictory context maps to
   `GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY`; ambiguous or invalid context
   to `GENERIC_ASSET_CLASS_CONTEXT_INVALID`; `STOCK` or `CRYPTO` to
   `GENERIC_ASSET_CLASS_NOT_OPTIONS`; stale context to
   `GENERIC_ASSET_CLASS_CONTEXT_STALE`; and out-of-scope context to
   `GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE`, each with `NO_ACTION` and
   `GOVERNANCE_REVIEW`. Malformed raw values are rejected first.
10. **`OPTIONS-DECISION-10` - `EXPLICIT_CLOSED_CONFIRMATION_VOCABULARY`**:
    Confirmation values are exactly `CONFIRMED`, `NOT_CONFIRMED`, and
    `CONTRADICTORY`; absence is classifiable. Missing, not-confirmed, and
    contradictory confirmation map respectively to
    `OPTIONS_LANE_CONFIRMATION_MISSING`, `OPTIONS_LANE_NOT_CONFIRMED`, and
    `OPTIONS_LANE_CONTRADICTORY`, each with `NO_ACTION` and
    `GOVERNANCE_REVIEW`. Confirmation is never inferred from identifiers or
    market data.
11. **`OPTIONS-DECISION-11` - `CONFLICT_GOVERNANCE_REVIEW`**: Deferral and
    no-action asserted together map to `NO_ACTION`,
    `OPTIONS_DEFERRAL_NO_ACTION_CONFLICT`, `GOVERNANCE_REVIEW`. This is
    separate from the evidence-contradiction flag.
12. **`OPTIONS-DECISION-12` - `EXTERNAL_FLAG_ONLY_HIGHEST_PRECEDENCE`**:
    Contradiction exists only when `options_evidence_contradictory = true`.
    It maps to `NO_ACTION`, `OPTIONS_EVIDENCE_CONTRADICTORY`,
    `HUMAN_REVIEW`, and has highest precedence. No open-ended inference is
    authorized.
13. **`OPTIONS-DECISION-13` - `FOUNDER_DEFINED_ORDERED_FIRST_MATCH`**: The
    evaluator selects only the first matching condition in the exact order
    below; lower conditions cannot alter the result.
14. **`OPTIONS-DECISION-14` - `OPTIONAL_CONTEXTUAL_ONLY`**: EchoAuth evidence
    is optional contextual input. When supplied, authority failure order is
    contradictory, ambiguous, invalid, revoked, stale, then out of scope.
    Contradictory, ambiguous, or invalid maps to `AUTHORITY_EVIDENCE_INVALID`;
    revoked to `AUTHORITY_EVIDENCE_REVOKED`; stale to
    `AUTHORITY_EVIDENCE_STALE`; and out of scope to
    `AUTHORITY_EVIDENCE_OUT_OF_SCOPE`, all with `NO_ACTION` and
    `GOVERNANCE_REVIEW`. EchoAuth is never called or reinterpreted.
15. **`OPTIONS-DECISION-15` - `REJECT_UNKNOWN_AND_CLASSIFY_CLOSED_UNDEFINED_SET`**:
    Unknown raw enums are rejected before typed construction. Exactly three
    typed undefined combinations map to `NO_ACTION`,
    `UNDEFINED_INPUT_COMBINATION`, `GOVERNANCE_REVIEW`: evidence absent while
    current; evidence absent while sufficient; and stale evidence while
    sufficient. Deferral plus no-action, restriction plus exclusion, lane
    contradiction, and incompatible generic context use their separately
    governed reasons.
16. **`OPTIONS-DECISION-16` - `EXPLICIT_FOUNDER_NAMED_PATHS`**: Future
    boundaries are `schemas/sniperbot-options-deferral-no-action-decision.schema.json`,
    `src/sniperbot/options/__init__.py`,
    `src/sniperbot/options/deferral_decision.py`, and
    `tests/test_sniperbot_options_deferral_no_action.py`. These paths are not
    authorized for creation by this record; accepted generic and Stock
    packages remain unchanged.
17. **`OPTIONS-DECISION-17` - `FULL_CONTRACT_AUTHORITY_SUITE_AND_SCOPE_SCAN`**:
    Future work requires JSON parsing, exact vocabulary checks,
    schema/implementation parity, focused, contract, Authority Clarity, and
    full-suite tests, `git diff --check`, exact file scope, prohibited-import,
    and side-effect inspection. The stop conditions below are mandatory.

## Closed Vocabularies

Outcomes: `DEFER`, `NO_ACTION`.

Reason codes (22):

`OPTIONS_DEFERRAL_EXTERNALLY_REQUIRED`, `OPTIONS_EVIDENCE_MISSING`,
`OPTIONS_EVIDENCE_STALE`, `OPTIONS_EVIDENCE_INSUFFICIENT`,
`OPTIONS_EVIDENCE_CONTRADICTORY`, `OPTIONS_DEFERRAL_NO_ACTION_CONFLICT`,
`OPTIONS_RESTRICTED`, `OPTIONS_EXCLUDED`, `OPTIONS_LANE_CONFIRMATION_MISSING`,
`OPTIONS_LANE_NOT_CONFIRMED`, `OPTIONS_LANE_CONTRADICTORY`,
`GENERIC_ASSET_CLASS_CONTEXT_INVALID`, `GENERIC_ASSET_CLASS_CONTEXT_STALE`,
`GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY`,
`GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE`, `GENERIC_ASSET_CLASS_NOT_OPTIONS`,
`AUTHORITY_EVIDENCE_INVALID`, `AUTHORITY_EVIDENCE_STALE`,
`AUTHORITY_EVIDENCE_REVOKED`, `AUTHORITY_EVIDENCE_OUT_OF_SCOPE`,
`UNDEFINED_INPUT_COMBINATION`, `NO_ACTION_REQUIRED`.

RequiredAction values (5): `NONE`, `HUMAN_REVIEW`,
`GOVERNANCE_REVIEW`, `FOUNDER_AUTHORITY_REQUIRED`, `RESET_REQUIRED`.
Subject-emittable values are exactly `NONE`, `HUMAN_REVIEW`, and
`GOVERNANCE_REVIEW`.

Options-lane confirmation values (3): `CONFIRMED`, `NOT_CONFIRMED`,
`CONTRADICTORY`.

## Exact First-Match Precedence

1. Options-evidence contradiction.
2. Deferral/no-action conflict.
3. The three closed undefined combinations.
4. Lane confirmation missing.
5. Lane confirmation contradictory.
6. Lane not confirmed.
7. Generic context contradictory.
8. Generic context ambiguous or invalid.
9. Generic context not `OPTIONS`.
10. Generic context stale.
11. Generic context out of scope.
12. External options exclusion.
13. External options restriction.
14. Supplied authority failure.
15. Options evidence missing.
16. Options evidence stale.
17. Options evidence insufficient.
18. External options deferral.
19. Explicit options no-action.
20. Ordinary no-action fallback.

Lower-precedence facts cannot change the selected result. Evidence missing,
stale, and insufficient map to `DEFER` with the matching reason and
`HUMAN_REVIEW`. External deferral maps to `DEFER` /
`OPTIONS_DEFERRAL_EXTERNALLY_REQUIRED` / `HUMAN_REVIEW`. Ordinary and
explicit no-action map to `NO_ACTION` / `NO_ACTION_REQUIRED` / `NONE`.

## Non-Authorization and Stop Conditions

The classifier consumes externally supplied facts only. It does not select or
approve a contract, calculate eligibility, access options chains or market
data, inspect strike, expiration, premium, Greeks, volume, open interest,
liquidity, exercise, assignment, lifecycle, signals, strategy, risk, sizing,
simulation, backtesting, brokers, Robinhood, orders, credentials, deployment,
persistence, networking, runtime systems, or execution. EchoAuth authority
cannot be called, repaired, broadened, reinterpreted, granted, or bypassed.

Stop immediately on new vocabulary or authority meaning; ambiguous
precedence; generic or Stock evaluator modification, duplication, invocation,
or orchestration; eligibility or contract selection; options-chain or market
data; strategy, signals, risk, sizing, collateral, margin, portfolio,
exercise, assignment, expiration, settlement, rolling, simulation, replay,
backtesting, broker, Robinhood, order, credential, deployment, persistence,
networking, execution, EchoAuth runtime, unexpected files, dependency,
workflow, CI, configuration, validator, archive, unresolved contradiction, or
Stage 3 movement.

## Decision Boundary and Next Founder Decision

This record authorizes only the future consideration of a separate bounded
schema-only task order. It does not authorize the schema or any implementation
paths listed above. The exact next founder decision is whether to authorize a
separate bounded schema-only task order for the Options Deferral / No-Action
contract.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized.
