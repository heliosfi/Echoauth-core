# SniperBot Stage 2 Stock Deferral / No-Action Founder Decision Record

## Status and Boundary

Documentation-only / governance-only / founder-decision-record-only / stock-specific / non-runtime / non-execution / non-authorizing.

Repository: `heliosfi/Echoauth-core`
Starting checkpoint: `fa1296ab8b42d1df7e4874e20717e3d25719d490`
Contract-definition commit: `0971b2f4d5015dc7056ba075132638301cd3898f`

These decisions define only the future Stock Deferral / No-Action contract. They do not authorize its schema, implementation, tests, package initializer, orchestration, eligibility, market data, signals, strategy, risk, sizing, orders, execution, another Stage 2 subject, or Stage 3. The accepted generic Asset-Class Deferral evaluator remains unchanged.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized.

## Founder Decisions

1. **`STOCK-DECISION-01` — `DEFER_AND_NO_ACTION_ONLY`**: Outcomes are exactly `DEFER` and `NO_ACTION`; neither is eligibility, approval, signal, trade, order, or execution authority.
2. **`STOCK-DECISION-02` — `FOUNDER_DEFINED_STOCK_REASON_SET`**: The closed vocabulary has exactly 22 values: `STOCK_DEFERRAL_EXTERNALLY_REQUIRED`, `STOCK_EVIDENCE_MISSING`, `STOCK_EVIDENCE_STALE`, `STOCK_EVIDENCE_INSUFFICIENT`, `STOCK_EVIDENCE_CONTRADICTORY`, `STOCK_DEFERRAL_NO_ACTION_CONFLICT`, `STOCK_RESTRICTED`, `STOCK_EXCLUDED`, `STOCK_LANE_CONFIRMATION_MISSING`, `STOCK_LANE_NOT_CONFIRMED`, `STOCK_LANE_CONTRADICTORY`, `GENERIC_ASSET_CLASS_CONTEXT_INVALID`, `GENERIC_ASSET_CLASS_CONTEXT_STALE`, `GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY`, `GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE`, `GENERIC_ASSET_CLASS_NOT_STOCK`, `AUTHORITY_EVIDENCE_INVALID`, `AUTHORITY_EVIDENCE_STALE`, `AUTHORITY_EVIDENCE_REVOKED`, `AUTHORITY_EVIDENCE_OUT_OF_SCOPE`, `UNDEFINED_INPUT_COMBINATION`, and `NO_ACTION_REQUIRED`. Unknown raw values are rejected before typed construction; no `UNKNOWN` reason is approved.
3. **`STOCK-DECISION-03` — `REUSE_FIVE_VALUE_SET_WITH_EXPLICIT_MAPPINGS`**: Full actions are `NONE`, `HUMAN_REVIEW`, `GOVERNANCE_REVIEW`, `FOUNDER_AUTHORITY_REQUIRED`, and `RESET_REQUIRED`. Only the first three are subject-emittable; the latter two are vocabulary-only and rejected.
4. **`STOCK-DECISION-04` — `EXTERNAL_DESCRIPTIVE_DEFERRAL_FACT`**: Stock deferral means stock-specific review should pause. With no higher condition: `DEFER / STOCK_DEFERRAL_EXTERNALLY_REQUIRED / HUMAN_REVIEW`. It is not ineligibility, exclusion, data failure, rejection, cancellation, or permission.
5. **`STOCK-DECISION-05` — `EXPLICIT_AND_ORDINARY_NO_ACTION_SHARE_MAPPING`**: Explicit and ordinary no-action both map to `NO_ACTION / NO_ACTION_REQUIRED / NONE`; no-action is not approval, eligibility, signal, or execution.
6. **`STOCK-DECISION-06` — `SEPARATE_EXTERNAL_DESCRIPTIVE_FACTS`**: Restriction and exclusion are separate supplied facts. Exclusion maps to `NO_ACTION / STOCK_EXCLUDED / NONE`; restriction maps to `NO_ACTION / STOCK_RESTRICTED / NONE`; exclusion precedes restriction. Neither is calculated, verified, derived, modified, or approved.
7. **`STOCK-DECISION-07` — `INDEPENDENT_CLASSIFIERS_WITH_OPTIONAL_CONTEXT`**: Generic Asset-Class and Stock Deferral remain independent. Neither invokes or orchestrates the other. A generic result is optional contextual evidence only and never authorizes stock activity.
8. **`STOCK-DECISION-08` — `OPTIONAL_CONTEXTUAL_STOCK_COMPATIBILITY_ONLY`**: Generic context is optional; absent context has no effect. Only `STOCK` is compatible. Contradictory, invalid, non-`STOCK`, stale, and out-of-scope context use their approved reason and `GOVERNANCE_REVIEW`; malformed raw values are rejected first.
9. **`STOCK-DECISION-09` — `EXPLICIT_CLOSED_CONFIRMATION_VOCABULARY`**: Confirmation values are `CONFIRMED`, `NOT_CONFIRMED`, and `CONTRADICTORY`. Missing, not-confirmed, and contradictory values map to their corresponding stock-lane reason with `NO_ACTION / GOVERNANCE_REVIEW`; `CONFIRMED` continues. No inference from identifiers or data is allowed.
10. **`STOCK-DECISION-10` — `CONFLICT_GOVERNANCE_REVIEW`**: Deferral and no-action together map to `NO_ACTION / STOCK_DEFERRAL_NO_ACTION_CONFLICT / GOVERNANCE_REVIEW`, separate from evidence contradiction.
11. **`STOCK-DECISION-11` — `EXTERNAL_FLAG_ONLY_HIGHEST_PRECEDENCE`**: Only `stock_evidence_contradictory = true` establishes contradiction. It maps to `NO_ACTION / STOCK_EVIDENCE_CONTRADICTORY / HUMAN_REVIEW` and has highest precedence.
12. **`STOCK-DECISION-12` — `FOUNDER_DEFINED_ORDERED_FIRST_MATCH`**: First-match order is contradiction; deferral/no-action conflict; the three undefined combinations; missing, contradictory, and not-confirmed lane status; generic context contradictory, invalid, non-`STOCK`, stale, and out of scope; exclusion; restriction; authority failure; evidence missing; evidence stale; evidence insufficient; external deferral; explicit no-action; ordinary fallback. Lower conditions cannot change the result. Evidence defects map to `DEFER` with their reason and `HUMAN_REVIEW`.
13. **`STOCK-DECISION-13` — `OPTIONAL_CONTEXTUAL_ONLY`**: EchoAuth evidence is optional contextual input. Failure order is contradictory, ambiguous, invalid, revoked, stale, then out of scope. Failures map to `NO_ACTION / GOVERNANCE_REVIEW` with the approved reason. EchoAuth is never called, reproduced, repaired, broadened, reinterpreted, granted, or bypassed.
14. **`STOCK-DECISION-14` — `REJECT_UNKNOWN_AND_CLASSIFY_CLOSED_UNDEFINED_SET`**: Unknown raw values are rejected before typed request or decision creation. Exactly three undefined combinations are evidence absent while current, evidence absent while sufficient, and evidence stale while sufficient; each maps to `NO_ACTION / UNDEFINED_INPUT_COMBINATION / GOVERNANCE_REVIEW`. No additional undefined combination is inferred.
15. **`STOCK-DECISION-15` — `EXPLICIT_FOUNDER_NAMED_PATHS`**: Future boundaries are `schemas/sniperbot-stock-deferral-no-action-decision.schema.json`, `src/sniperbot/stock/__init__.py`, `src/sniperbot/stock/deferral_decision.py`, and `tests/test_sniperbot_stock_deferral_no_action.py`. They are not created or authorized here; the generic package remains unchanged.
16. **`STOCK-DECISION-16` — `FULL_CONTRACT_AUTHORITY_SUITE_AND_SCOPE_SCAN`**: Future work requires JSON parsing, exact vocabulary/schema parity, focused, contract, Authority Clarity, and full-suite tests, `git diff --check`, exact scope, prohibited-import, and side-effect scans. Stop on new vocabulary or authority meaning, ambiguous precedence, generic duplication, eligibility/selection, market data, signals, strategy, risk, sizing, simulation, broker/order/execution behavior, EchoAuth runtime, orchestration, dependency/workflow/configuration/validator/archive changes, unexpected files, unresolved contradictions, or Stage 3 movement.

## Decision Boundary

These decisions authorize only one future founder decision record and index entry. They do not authorize schema, Python, tests, package initialization, classifier orchestration, eligibility, market data, signals, strategy, risk, sizing, orders, execution, another Stage 2 subject, or Stage 3.

The exact next founder decision is whether to authorize a separate bounded schema-only task order for the Stock Deferral / No-Action contract.
