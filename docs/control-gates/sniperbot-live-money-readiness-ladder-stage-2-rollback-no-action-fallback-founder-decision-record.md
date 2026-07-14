# SniperBot Live-Money Readiness Ladder Stage 2 Rollback / No-Action Fallback Founder Decision Record

## Status and Boundary

Documentation-only / governance-only / founder-decision-record-only /
non-runtime / non-execution / non-authorizing.

This record captures `ROLLBACK-DECISION-01` through `ROLLBACK-DECISION-13` for
the proposed pure Rollback / No-Action Fallback Decision Contract. It
authorizes no schema, Python implementation, tests, rollback execution,
recovery, reset, FSM mutation, runtime integration, broker access, orders,
persistence, networking, execution, or Stage 3 entry.

Stage 2 remains **HOLD**. EchoAuth remains the sole permission authority.

## Founder Decisions

| ID | Founder selection | Contract effect |
| --- | --- | --- |
| `ROLLBACK-DECISION-01` | `DEFER_AND_NO_ACTION_ONLY` | Outcomes are `DEFER` and `NO_ACTION`; neither is authorization, recovery authority, FSM approval, reset permission, mutation, or execution. |
| `ROLLBACK-DECISION-02` | `FOUNDER_DEFINED_ROLLBACK_REASON_SET` | The exact 14-code set below is closed; no free text replaces a code. |
| `ROLLBACK-DECISION-03` | `REUSE_FIVE_VALUE_SET_WITH_EXPLICIT_MAPPINGS` | RequiredAction uses five closed values; only `NONE`, `HUMAN_REVIEW`, and `GOVERNANCE_REVIEW` may be emitted by this subject. |
| `ROLLBACK-DECISION-04` | `EXTERNAL_DESCRIPTIVE_FACT_ONLY` | `rollback_required` is an external assertion that review may be needed; it is not permission or an instruction. |
| `ROLLBACK-DECISION-05` | `EXTERNAL_AVAILABILITY_FACT_ONLY` | `rollback_available` only describes an externally asserted separately controlled path; it is not verified or authorized here. |
| `ROLLBACK-DECISION-06` | `CONSUME_EXTERNAL_FACT_ONLY` | Availability is consumed only; it is not inspected, calculated, derived, or invoked. |
| `ROLLBACK-DECISION-07` | `CONTRADICTION_GOVERNANCE_REVIEW` | Rollback-required plus no-action yields `NO_ACTION`, `ROLLBACK_AND_NO_ACTION_CONFLICT`, `GOVERNANCE_REVIEW`. |
| `ROLLBACK-DECISION-08` | `EXTERNAL_FLAG_ONLY_HIGHEST_PRECEDENCE` | The contradiction flag alone emits `NO_ACTION`, `ROLLBACK_EVIDENCE_CONTRADICTORY`, `HUMAN_REVIEW`. |
| `ROLLBACK-DECISION-09` | `OPTIONAL_CONTEXTUAL_ONLY` | EchoAuth evidence is optional context; supplied failures use the approved sub-precedence and never become permission. |
| `ROLLBACK-DECISION-10` | `REJECT_UNKNOWN_AND_FAIL_CLOSED_UNDEFINED` | Unknown raw values are rejected; exactly three undefined combinations map to governance review; unrecognized valid conditions map to `UNKNOWN_CONDITION`. |
| `ROLLBACK-DECISION-11` | `CONTEXT_ONLY_NO_FSM_OR_RECOVERY_MUTATION` | Halt, reset, lockout, recovery, and six-state references remain opaque, non-decisional context. |
| `ROLLBACK-DECISION-12` | `EXPLICIT_FOUNDER_NAMED_PATHS` | Future schema, initializer, implementation, and test paths are the four exact paths below; creation is not authorized. |
| `ROLLBACK-DECISION-13` | `FULL_CONTRACT_AUTHORITY_SUITE_AND_SCOPE_SCAN` | Future work requires the full listed validation and stop conditions. |

## Closed Vocabularies

Outcomes: `DEFER`, `NO_ACTION`.

Reason codes (14): `ROLLBACK_EXTERNALLY_REQUIRED`, `ROLLBACK_UNAVAILABLE`,
`ROLLBACK_EVIDENCE_MISSING`, `ROLLBACK_EVIDENCE_STALE`,
`ROLLBACK_EVIDENCE_INSUFFICIENT`, `ROLLBACK_EVIDENCE_CONTRADICTORY`,
`ROLLBACK_AND_NO_ACTION_CONFLICT`, `AUTHORITY_EVIDENCE_INVALID`,
`AUTHORITY_EVIDENCE_STALE`, `AUTHORITY_EVIDENCE_REVOKED`,
`AUTHORITY_EVIDENCE_OUT_OF_SCOPE`, `UNKNOWN_CONDITION`,
`UNDEFINED_INPUT_COMBINATION`, `NO_ACTION_REQUIRED`.

RequiredAction values (5): `NONE`, `HUMAN_REVIEW`, `GOVERNANCE_REVIEW`,
`FOUNDER_AUTHORITY_REQUIRED`, `RESET_REQUIRED`. The last two are vocabulary-
only and non-emittable by this subject.

## Precedence and Mappings

The evaluator must use this exact first-match order:

1. rollback-evidence contradiction flag;
2. rollback-required plus no-action conflict;
3. one of the three undefined combinations;
4. authority failure (ambiguous, invalid, revoked, stale, out of scope);
5. missing evidence;
6. stale evidence;
7. insufficient evidence;
8. rollback required but unavailable;
9. rollback externally required;
10. explicit no-action;
11. ordinary no-action fallback.

Contradiction maps to `NO_ACTION / ROLLBACK_EVIDENCE_CONTRADICTORY /
HUMAN_REVIEW`. The rollback/no-action conflict maps to `NO_ACTION /
ROLLBACK_AND_NO_ACTION_CONFLICT / GOVERNANCE_REVIEW`.

Missing, stale, and insufficient evidence map to `DEFER` with their matching
reason and `HUMAN_REVIEW`. Required-but-unavailable maps to `DEFER /
ROLLBACK_UNAVAILABLE / HUMAN_REVIEW`; required maps to `DEFER /
ROLLBACK_EXTERNALLY_REQUIRED / HUMAN_REVIEW`. Explicit or ordinary no-action
maps to `NO_ACTION / NO_ACTION_REQUIRED / NONE`.

Authority failures map to `NO_ACTION / GOVERNANCE_REVIEW` using the approved
sub-precedence and matching authority reason code.

Undefined combinations are exactly:

1. rollback evidence absent while current;
2. rollback evidence absent while sufficient;
3. rollback evidence stale while sufficient.

Each maps to `NO_ACTION / UNDEFINED_INPUT_COMBINATION / GOVERNANCE_REVIEW`.

## Future Boundaries — Not Authorized

1. `schemas/sniperbot-rollback-no-action-fallback-decision.schema.json`
2. `src/sniperbot/rollback/__init__.py`
3. `src/sniperbot/rollback/fallback_decision.py`
4. `tests/test_sniperbot_rollback_no_action_fallback.py`

These are future boundaries only. `src/sniperbot/__init__.py` remains
unchanged unless separately authorized.

## Validation and Stops

Future work must run focused, contract, Authority Clarity, and full-suite tests,
`git diff --check`, vocabulary and file-scope checks, prohibited-import and
side-effect inspection. Stop on new vocabulary or authority meaning,
ambiguous precedence, rollback/recovery/FSM mutation, runtime integration,
neighboring capability, dependency/workflow/configuration change, unexpected
files, unresolved contradictions, or Stage 3 movement.

Stage 2 remains **HOLD** and Stage 3 remains unentered and unauthorized.
