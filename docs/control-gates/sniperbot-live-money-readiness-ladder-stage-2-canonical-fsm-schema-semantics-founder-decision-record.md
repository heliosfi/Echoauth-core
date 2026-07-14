# SniperBot Live-Money Readiness Ladder Stage 2 Canonical FSM Schema Semantics Founder Decision Record

## Status and Boundary

Documentation-only / governance-only / schema-semantics-founder-decision-record-only.

This record captures the founder decisions `FSM-SCHEMA-01` through
`FSM-SCHEMA-11` for the existing pure, deterministic, immutable,
side-effect-free, non-persistent, network-free, non-authorizing, and
non-executing SniperBot FSM transition-decision schema.

Stage 2 remains **HOLD with ESCALATE elements**. Stage 3 remains unentered and
unauthorized. EchoAuth remains the sole owner of permission authority; the FSM
may consume bounded authority evidence only.

This record authorizes only the corresponding schema amendment and this record.
It authorizes no Python implementation, tests, runtime integration, strategy,
signals, risk, sizing, market data, simulation, backtesting, broker or
Robinhood access, orders, credentials, deployment, database access, or
execution.

## Founder Decisions

| ID | Founder selection | Contract effect |
| --- | --- | --- |
| `FSM-SCHEMA-01` | `REQUIRE_VALID_AUTHORITY_FOR_BOTH` | `READY → ARMED_MANUAL` and `LOCKOUT → PAUSE` require present, valid, current, exact, in-scope, non-revoked bounded authority evidence. |
| `FSM-SCHEMA-02` | `READINESS_PRECONDITIONS_TRUE_ONLY` | `PAUSE → READY` requires the non-authority readiness fact. |
| `FSM-SCHEMA-03` | `CONFIRMED_POSITION_REQUIRED_RESULT_IN_TRADE` | `ARMED_AUTO → IN_TRADE` may be allowed only with an externally confirmed position and results in `IN_TRADE`; no fill is executed or confirmed by the FSM. |
| `FSM-SCHEMA-04` | `POSITION_CLOSED_AND_COOLDOWN_REQUIRED` | `IN_TRADE → PAUSE` requires both externally supplied facts and results in `PAUSE`. |
| `FSM-SCHEMA-05` | `DENY_RETAIN_CURRENT_STATE` | Locked, undefined, and denied requests retain the current state without mutation. |
| `FSM-SCHEMA-06` | `ALLOWED_TO_REQUESTED_DENIED_TO_CURRENT` | Allowed decisions result in the requested state; denied decisions retain the current state. |
| `FSM-SCHEMA-07` | `DENY_AMBIGUOUS_INPUT` | Contradictory or ambiguous facts are denied without mutation with `AMBIGUOUS_OR_CONTRADICTORY_INPUT`. |
| `FSM-SCHEMA-08` | `EXACT_REQUEST_DECISION_REFERENCE_MATCH` | The decision correlation reference must exactly equal the request reference. |
| `FSM-SCHEMA-09` | `CLOSED_FIVE_VALUE_SET_WITH_EXPLICIT_MAPPINGS` | Required action remains exactly `NONE`, `HUMAN_REVIEW`, `GOVERNANCE_REVIEW`, `FOUNDER_AUTHORITY_REQUIRED`, or `RESET_REQUIRED`, with the approved mappings. |
| `FSM-SCHEMA-10` | `NULL_ONLY_FOR_NON_AUTHORITY_TRANSITIONS` | Null authority evidence is permitted only where the transition does not require authority. |
| `FSM-SCHEMA-11` | `BOTH_WHERE_REPRESENTABLE` | Rules are enforced in JSON Schema where representable and by the future pure evaluator where cross-object or procedural enforcement is required. |

## Required-Action Mappings

* `NONE`: successful allowed transition requiring no further action.
* `HUMAN_REVIEW`: ambiguous or contradictory input requiring clarification.
* `GOVERNANCE_REVIEW`: undefined transition, unknown state, or evidence-scope uncertainty.
* `FOUNDER_AUTHORITY_REQUIRED`: founder-denied movement or movement requiring separate founder authorization, including `ARMED_AUTO` entry.
* `RESET_REQUIRED`: denied `LOCKOUT → PAUSE` caused by missing reset evidence or reset facts.

## Schema and Evaluator Boundary

The amended schema represents conditional authority, readiness, confirmed
position, position closure, cooldown, explicit denials, current-state
retention for locked transitions, and the closed vocabulary. `READY →
ARMED_AUTO` remains denied.

The future evaluator must enforce exact request/decision correlation equality,
complete allowed/resulting-state relationships, undefined-transition handling,
contradictory-input handling, required-action mappings, and any rule that Draft
2020-12 cannot express across sibling values or procedural outcomes.

No schema or evaluator rule may create, reinterpret, replace, or bypass
EchoAuth authority. No rule authorizes implementation or Stage 3.

## Validation and Stop Conditions

Validation must confirm JSON parsing, Draft 2020-12 structural validity under
available repository tooling, exactly six states, exactly 17 reason codes,
exactly five required-action values, representation of all 11 decisions,
continued `ARMED_AUTO` denial, one README index entry, `git diff --check`,
repository contract validation, and the Authority Clarity Validator.

Stop if any rule requires a new state, transition, reason code, required-action
value, authority behavior, execution behavior, or implementation interpretation
outside this record. Stage 2 remains **HOLD with ESCALATE elements** and Stage 3
remains unentered and unauthorized.
