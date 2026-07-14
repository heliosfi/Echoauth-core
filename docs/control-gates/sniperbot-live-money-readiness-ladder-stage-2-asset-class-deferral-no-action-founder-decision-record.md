# SniperBot Live-Money Readiness Ladder Stage 2 Asset-Class Deferral / No-Action Founder Decision Record

## Status and Boundary

Documentation-only / governance-only / founder-decision-record-only /
non-runtime / non-execution / non-authorizing.

This record captures the founder decisions `ASSET-DEFERRAL-01` through
`ASSET-DEFERRAL-09` for the proposed pure Asset-Class Deferral / No-Action
Decision Contract. It authorizes no schema, Python implementation, tests,
runtime integration, asset selection, eligibility calculation, market-data
access, trading, broker access, orders, credentials, persistence, networking,
execution, or Stage 3 entry.

Stage 2 remains **HOLD**. EchoAuth remains the sole permission authority.

## Founder Decisions

| ID | Founder selection | Contract effect |
| --- | --- | --- |
| `ASSET-DEFERRAL-01` | `FOUNDER_DEFINED_CLOSED_VOCABULARY` | The only asset classes are `STOCK`, `OPTIONS`, and `CRYPTO`; unknown identifiers fail closed and these lanes remain separate. |
| `ASSET-DEFERRAL-02` | `DEFER_AND_NO_ACTION_ONLY` | The only outcomes are `DEFER` and `NO_ACTION`; neither is permission, eligibility, approval, execution, or authorization. |
| `ASSET-DEFERRAL-03` | `FOUNDER_DEFINED_DEFERRAL_REASON_SET` | The closed reason set is the 13 values listed below; no free text replaces a governing code. |
| `ASSET-DEFERRAL-04` | `OPTIONAL_BOUNDED_INPUT_ONLY` | EchoAuth evidence may be supplied only as contextual bounded input. Supplied invalid, stale, revoked, contradictory, or out-of-scope evidence fails closed to `NO_ACTION`. |
| `ASSET-DEFERRAL-05` | `FOUNDER_DEFINED_FAIL_CLOSED_PRECEDENCE` | The exact precedence and outcomes are recorded below; lower conditions cannot override higher conditions. |
| `ASSET-DEFERRAL-06` | `REUSE_FIVE_VALUE_SET_WITH_EXPLICIT_MAPPINGS` | RequiredAction uses the repository’s five-value set with the subject-specific mappings below. |
| `ASSET-DEFERRAL-07` | `DENY_UNKNOWN_GOVERNANCE_REVIEW` | Unknown asset class yields `NO_ACTION`, `UNKNOWN_ASSET_CLASS`, and `GOVERNANCE_REVIEW`. |
| `ASSET-DEFERRAL-08` | `EXPLICIT_FOUNDER_NAMED_PATHS` | Future boundaries are the four exact paths listed below; this record does not authorize their creation. |
| `ASSET-DEFERRAL-09` | `CONTRACT_AUTHORITY_FOCUSED_FULL_AND_DIFF_CHECK` | The future validation commands and stop conditions listed below are required. |

## Closed Vocabularies

Asset classes: `STOCK`, `OPTIONS`, `CRYPTO`.

Outcomes: `DEFER`, `NO_ACTION`.

Reason codes (13):

`EXTERNAL_DEFERRAL_REQUIRED`, `NO_ACTION_REQUIRED`, `EVIDENCE_MISSING`,
`EVIDENCE_STALE`, `EVIDENCE_INSUFFICIENT`, `EVIDENCE_CONTRADICTORY`,
`EXTERNALLY_EXCLUDED`, `AUTHORITY_EVIDENCE_INVALID`,
`AUTHORITY_EVIDENCE_STALE`, `AUTHORITY_EVIDENCE_REVOKED`,
`AUTHORITY_EVIDENCE_OUT_OF_SCOPE`, `UNKNOWN_ASSET_CLASS`,
`UNDEFINED_INPUT_COMBINATION`.

RequiredAction values (5): `NONE`, `HUMAN_REVIEW`, `GOVERNANCE_REVIEW`,
`FOUNDER_AUTHORITY_REQUIRED`, `RESET_REQUIRED`.

## Precedence and Outcomes

The classifier applies this exact precedence:

1. Contradictory evidence → `NO_ACTION`.
2. Unknown asset class or undefined input → `NO_ACTION`.
3. External exclusion → `NO_ACTION`.
4. Invalid, stale, revoked, or out-of-scope supplied authority → `NO_ACTION`.
5. Missing evidence → `DEFER`.
6. Stale evidence → `DEFER`.
7. Insufficient evidence → `DEFER`.
8. Explicit external deferral → `DEFER`.
9. Otherwise → `NO_ACTION`.

## RequiredAction Mappings

* `NONE`: external deferral, external exclusion, or ordinary no-action.
* `HUMAN_REVIEW`: missing, stale, insufficient, or contradictory evidence.
* `GOVERNANCE_REVIEW`: unknown asset class, undefined input, or invalid,
  stale, revoked, or out-of-scope supplied authority.
* `FOUNDER_AUTHORITY_REQUIRED`: retained vocabulary; not emitted by this
  classifier without a separate founder decision.
* `RESET_REQUIRED`: retained vocabulary; not emitted by this classifier.

## Future Boundaries — Not Authorized

1. `schemas/sniperbot-asset-class-deferral-no-action-decision.schema.json`
2. `src/sniperbot/deferral/__init__.py`
3. `src/sniperbot/deferral/asset_class_decision.py`
4. `tests/test_sniperbot_asset_class_deferral_no_action.py`

These are future boundaries only. They must not be created without a separate
task order.

## Validation and Stop Conditions

Future work must run the focused test, contract and Authority Clarity tests,
full suite, and `git diff --check`. It must stop on any new vocabulary,
precedence ambiguity, authority reinterpretation, eligibility or asset-selection
logic, market-data or execution-adjacent capability, dependency/workflow/
configuration change, unexpected file, unresolved contradiction, or Stage 3
movement.

Stage 2 remains **HOLD** and Stage 3 remains unentered and unauthorized.
