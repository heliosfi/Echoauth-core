# SniperBot Live-Money Readiness Ladder Stage 2 Asset-Class Deferral / No-Action Schema Consistency Founder Decision Record

## Status and Boundary

Documentation-only / governance-only / schema-consistency-decision-only /
non-runtime / non-execution / non-authorizing.

This record captures the bounded consistency repair for the Asset-Class
Deferral / No-Action schema. It authorizes no Python implementation, tests,
eligibility calculation, asset selection, market data, signals, strategy, risk,
sizing, simulation, backtesting, broker or Robinhood access, orders,
credentials, deployment, persistence, networking, execution, runtime
integration, or Stage 3 movement.

Stage 2 remains **HOLD**. EchoAuth remains the sole permission authority.

## Consistency Decisions

The exact undefined-input set is limited to four typed combinations:

1. `evidence_present = false` and `evidence_current = true`;
2. `evidence_present = false` and `evidence_sufficient = true`;
3. `evidence_current = false` and `evidence_sufficient = true`;
4. `eligibility_status = true` and `exclusion_status = true`.

Each is evaluator-owned and returns `NO_ACTION`,
`UNDEFINED_INPUT_COMBINATION`, and `GOVERNANCE_REVIEW`. Authority failures
are not undefined input. Malformed authority objects fail schema validation.

`EVIDENCE_CONTRADICTORY` is emitted only when the supplied contradiction flag
is true and remains higher precedence than undefined combinations.

When multiple authority failures coexist, the evaluator selects only the first
matching failure in this order: ambiguous, invalid, revoked, stale, out of
scope. The corresponding closed reason is emitted with `NO_ACTION` and
`GOVERNANCE_REVIEW`.

## Schema and Evaluator Responsibilities

The schema owns closed vocabularies, required fields, types, object structure,
and malformed-authority rejection. It no longer imposes competing procedural
output mappings through independent conditionals.

The pure evaluator owns ordered first-match precedence, one outcome/reason/
action selection, ordinary `NO_ACTION` (`NO_ACTION_REQUIRED` / `NONE`),
authority-failure sub-precedence, and exact request/decision correlation
equality. For valid typed input not matching a higher-precedence condition, the
deterministic fallback is `NO_ACTION`, `NO_ACTION_REQUIRED`, `NONE`.

No open-ended logical-invariant interpretation is authorized. Any future
undefined combination requires a separate founder decision.

## Validation Boundary

The schema remains Draft 2020-12 with exactly 3 asset classes, 2 outcomes, 13
reason codes, and 5 RequiredAction values. Stage 2 remains **HOLD** and Stage 3
remains unentered and unauthorized.
