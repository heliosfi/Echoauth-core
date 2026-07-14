# SniperBot Live-Money Readiness Ladder Stage 2 Asset-Class Deferral / No-Action Semantics Founder Decision Record

## Status and Boundary

Documentation-only / governance-only / founder-semantics-decision-only /
schema-amendment-only / non-runtime / non-execution / non-authorizing.

This record captures `ASSET-SEMANTICS-01` through `ASSET-SEMANTICS-07` for the
approved Asset-Class Deferral / No-Action contract. It authorizes only the
corresponding schema amendment and this record. It does not authorize Python,
tests, eligibility calculation, asset selection, market data, signals,
strategy, risk, sizing, simulation, backtesting, broker or Robinhood access,
orders, credentials, deployment, persistence, networking, execution, or Stage
3 entry.

Stage 2 remains **HOLD**. EchoAuth remains the sole permission authority.

## Founder Decisions

| ID | Founder selection | Contract effect |
| --- | --- | --- |
| `ASSET-SEMANTICS-01` | `CLOSED_LIST_PLUS_NONCOHERENT_COMBINATIONS` | The seven listed incoherent combinations produce `NO_ACTION`, `UNDEFINED_INPUT_COMBINATION`, `GOVERNANCE_REVIEW`; additional combinations require a separate founder decision. |
| `ASSET-SEMANTICS-02` | `AMBIGUOUS_INVALID_REVOKED_STALE_OUT_OF_SCOPE` | Same-level authority failures use that exact first-match order and one matching reason code. |
| `ASSET-SEMANTICS-03` | `AUTHORITY_EVIDENCE_INVALID` | Ambiguous supplied authority produces `NO_ACTION`, `AUTHORITY_EVIDENCE_INVALID`, `GOVERNANCE_REVIEW`. |
| `ASSET-SEMANTICS-04` | `CONTEXTUAL_ONLY_NO_EFFECT` | Eligibility is contextual evidence only; only external exclusion activates the exclusion branch. |
| `ASSET-SEMANTICS-05` | `EXTERNAL_FLAG_ONLY` | `EVIDENCE_CONTRADICTORY` is emitted only when the supplied contradiction flag is true; closed incoherent combinations use `UNDEFINED_INPUT_COMBINATION`. |
| `ASSET-SEMANTICS-06` | `REJECT_UNKNOWN_RAW_INPUT` | Unknown raw asset classes are rejected before typed request/decision creation; no `UNKNOWN` enum or raw decision field is added. |
| `ASSET-SEMANTICS-07` | `ORDERED_FIRST_MATCH_ONLY` | The evaluator selects the first matching condition in the approved precedence order and ignores lower-precedence matches. |

## Undefined Combinations

The closed undefined set is:

1. Evidence absent while current is true.
2. Evidence absent while sufficient is true.
3. Evidence stale while sufficient is true.
4. Eligibility and exclusion are both affirmative.
5. Authority evidence is absent while authority details are supplied.
6. Authority fields report incompatible validity, currentness, revocation, or scope facts.
7. Any combination violating the approved request structure’s logical invariants.

Each yields `NO_ACTION`, `UNDEFINED_INPUT_COMBINATION`, and
`GOVERNANCE_REVIEW`. This is a closed rule; no open-ended contradiction
inference is authorized.

## Authority Failure Order

The evaluator selects only the first matching failure:

1. Ambiguous → `AUTHORITY_EVIDENCE_INVALID`
2. Invalid → `AUTHORITY_EVIDENCE_INVALID`
3. Revoked → `AUTHORITY_EVIDENCE_REVOKED`
4. Stale → `AUTHORITY_EVIDENCE_STALE`
5. Out of scope → `AUTHORITY_EVIDENCE_OUT_OF_SCOPE`

Every authority failure yields `NO_ACTION` and `GOVERNANCE_REVIEW`. Supplied
authority remains optional, contextual, and non-authorizing.

## Overall Precedence

The approved first-match order is: contradiction flag; undefined combination;
external exclusion; authority failure; missing evidence; stale evidence;
insufficient evidence; explicit deferral; ordinary no-action. Identical inputs
must produce the same single outcome, reason, and action.

## Evaluator Boundary

Eligibility remains contextual and never becomes selection, approval, or
exclusion. Unknown raw asset classes are rejected before typed evaluation and
may be retained only by the caller outside this contract for diagnostics.
Cross-field precedence and exact correlation equality remain mandatory future
evaluator semantics wherever Draft 2020-12 cannot safely enforce them.

Stage 2 remains **HOLD** and Stage 3 remains unentered and unauthorized.
