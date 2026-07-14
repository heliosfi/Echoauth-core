# SniperBot Live-Money Readiness Ladder Stage 2 Canonical FSM Schema and Interface Proposal

## Status and Boundary

Documentation-only / governance-only / schema-interface-proposal-only.

This proposal translates founder decisions `FSM-01` through `FSM-17` into a
future shape for one pure, deterministic, side-effect-free, non-executing
transition-decision subject. It creates no schema, interface, implementation,
test, validator, CI workflow, runtime integration, or execution capability.

Stage 2 remains **HOLD with ESCALATE elements**. Stage 3 is not entered or
authorized. No market data, strategy, signals, risk, sizing, trade cards,
simulation, backtesting, broker, Robinhood, orders, credentials, deployment,
database, production, or execution capability is created or authorized.

## Authority and State Vocabulary

EchoAuth remains the sole owner of permission authority. The future FSM may
consume a bounded authority result as input only. It may not issue authority,
validate authority independently, reinterpret scope, repair missing authority,
bypass denial, contact EchoAuth, or persist approval records.

The only state values are `PAUSE`, `READY`, `ARMED_MANUAL`, `ARMED_AUTO`,
`IN_TRADE`, and `LOCKOUT`. No state is added, renamed, normalized, or implied.
`START`, rejection, disablement, denial, and escalation are not states.

## Proposed Transition-Request Input

The future interface has one immutable request object:

| Field | Proposed type | Boundary |
| --- | --- | --- |
| `current_state` | six-value `State` enum | Unknown values are invalid. |
| `requested_state` | six-value `State` enum | A request only; never mutation. |
| `correlation_reference` | mandatory non-empty opaque string | Caller-provided; not generated, interpreted, persisted, or audited. |
| `transition_request` | non-empty opaque request label | Not a command, order, strategy, signal, or permission. |
| `external_facts` | immutable `ExternalFacts` | Already-determined facts only; no discovery, calculation, external verification, or persistence. |
| `authority_evidence` | nullable `AuthorityEvidence` | Required only for arming or bounded reset requests. |

The input excludes executable commands, broker instructions, orders, strategy
decisions, signals, risk calculations, sizing, credentials, and mutable
runtime authority.

## Proposed External Facts

`ExternalFacts` contains only these already-determined booleans:

| Field | Meaning |
| --- | --- |
| `readiness_preconditions_satisfied` | Non-authority facts for `PAUSE → READY`. |
| `confirmed_position_exists` | External fact for `ARMED_AUTO → IN_TRADE`. |
| `position_closed` | External fact for `IN_TRADE → PAUSE`. |
| `cooldown_complete` | External fact for `IN_TRADE → PAUSE`. |
| `lockout_required` | Absolute-precedence external safety fact. |
| `logging_failure_indicated` | May only support the external lockout fact. |
| `reset_facts_explicit` | External facts required for `LOCKOUT → PAUSE`. |

The FSM does not calculate, discover, fetch, verify through external calls,
refresh, mutate, or persist these facts.

## Proposed Authority Evidence

`AuthorityEvidence` represents an already-bounded EchoAuth result:

| Field | Proposed type |
| --- | --- |
| `presence` | `PRESENT` or `ABSENT` |
| `subject_scope` | exact non-empty opaque string |
| `currentness` | `CURRENT` or `STALE` |
| `revocation` | `NON_REVOKED` or `REVOKED` |
| `validity_outcome` | `VALID`, `INVALID`, `AMBIGUOUS`, or `OUT_OF_SCOPE` |
| `authority_reference` | non-empty opaque string |

Only `PRESENT`, exact scope, `CURRENT`, `NON_REVOKED`, and `VALID` may satisfy
the approved authority condition. The FSM does not independently validate,
repair, reinterpret, replace, or bypass EchoAuth authority.

## Proposed Transition Decision Output

The future interface returns one descriptive result:

| Field | Proposed type |
| --- | --- |
| `current_state` | six-value `State` enum |
| `requested_state` | six-value `State` enum |
| `allowed` | boolean |
| `resulting_state` | six-value `State` enum, descriptive only |
| `reason_code` | closed `ReasonCode` enum |
| `required_next_human_or_governance_action` | nullable closed action value |
| `correlation_reference` | opaque string echoed without interpretation |

The output has no side effect, persistence, state mutation, permission,
runtime activation, execution authority, or Stage 3 effect.

## Allowed Transition Table

Only these transitions are represented:

| Transition or condition | Rule |
| --- | --- |
| `PAUSE → READY` | Allowed only when `readiness_preconditions_satisfied` is true; authority is deferred to arming. |
| `READY → ARMED_MANUAL` | Allowed only with valid, exact, current, in-scope, non-revoked bounded authority evidence. |
| `READY → ARMED_AUTO` | Always denied pending separate founder authority; state remains vocabulary only. |
| `ARMED_AUTO → IN_TRADE` | Considered only when `confirmed_position_exists` is true; FSM neither executes nor confirms a fill. |
| `ARMED_MANUAL → IN_TRADE` | Denied and excluded; no manual-trade detection. |
| `IN_TRADE → READY` | Prohibited. |
| `IN_TRADE → PAUSE` | Requires both `position_closed` and `cooldown_complete`. |
| `ANY → LOCKOUT` | `lockout_required` has absolute precedence over every non-lockout request. |
| Logging failure | Represented only through the external lockout fact; no log write. |
| `LOCKOUT → PAUSE` | Requires valid bounded reset authority evidence and `reset_facts_explicit`. |
| Unknown or undefined transition | Denied without mutation. |

No other transition is added.

## Closed Reason-Code Proposal

The smallest closed set contains 17 codes:

`ALLOWED`, `UNDEFINED_TRANSITION`, `UNKNOWN_STATE`,
`READINESS_FACTS_MISSING`, `AUTHORITY_MISSING`, `AUTHORITY_INVALID`,
`AUTHORITY_STALE`, `AUTHORITY_REVOKED`, `AUTHORITY_OUT_OF_SCOPE`,
`TRANSITION_FOUNDER_DENIED`, `CONFIRMED_POSITION_FACT_MISSING`,
`POSITION_CLOSED_FACT_MISSING`, `COOLDOWN_FACT_MISSING`, `LOCKOUT_REQUIRED`,
`RESET_EVIDENCE_MISSING`, `RESET_FACTS_MISSING`,
`AMBIGUOUS_OR_CONTRADICTORY_INPUT`.

Free-text reasons are not the governing decision field.

## Precedence and Fail-Closed Rules

1. `lockout_required == true` overrides every requested non-lockout transition.
2. `logging_failure_indicated` may only contribute to that external lockout fact.
3. Missing mandatory fields, including the correlation reference, deny without mutation.
4. Unknown enum values deny with `UNKNOWN_STATE` without mutation.
5. Undefined transitions deny with `UNDEFINED_TRANSITION` without mutation.
6. Contradictory or ambiguous facts deny with `AMBIGUOUS_OR_CONTRADICTORY_INPUT`.
7. Missing, stale, invalid, revoked, or out-of-scope authority never becomes permission.
8. No network call, persistence, retry, fallback, callback, mutation, approval, or execution is permitted.
9. No fallback converts uncertainty, absence, ambiguity, or denial into an allowed transition.

## Future Boundary Proposals — Not Authorized

These paths are proposals only and must not be created by this document:

| Future artifact | Proposed path | Required separate authority |
| --- | --- | --- |
| Schema/interface | `schemas/sniperbot-fsm-transition-decision.schema.json` | Founder task order naming exact fields and validation. |
| Narrowest implementation interface | `src/sniperbot/fsm/transition_contract.py` | Separate implementation task order. |
| Direct tests | `tests/test_sniperbot_fsm_transition_contract.py` | Separate test vectors and scope. |
| Validation | Schema validation plus deterministic pure transition tests | Separate task order naming commands and pass/fail criteria. |

The proposed paths remain absent until separately authorized. Any future order
must stop on schema mismatch, unknown enum, missing field, contradictory fact,
invalid authority, unexpected mutation, external call, or out-of-scope file
change. It must prohibit strategy, signals, market data, risk, sizing,
trade-cards, simulation, backtesting, broker/Robinhood/orders, credentials,
deployment, database, execution, EchoAuth runtime changes, and Stage 3.

## Current Determination

This is one documentation-only schema/interface proposal. It creates no
schema, implementation, test, runtime integration, permission, or execution
capability. Stage 2 remains **HOLD with ESCALATE elements** and Stage 3 remains
unentered and unauthorized.
