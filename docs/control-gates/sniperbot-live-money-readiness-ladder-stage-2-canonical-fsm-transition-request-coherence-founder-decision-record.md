# SniperBot Live-Money Readiness Ladder Stage 2 Canonical FSM Transition-Request Coherence Founder Decision Record

## Status and Non-Authorization Boundary

Documentation-only / governance-only / founder-decision-record-only.

This record resolves the Canonical FSM relationship between the nine closed
`TransitionRequestName` identifiers and their canonical state pairs. It does
not implement, repair, validate for acceptance, or index that relationship.

Stage 2 remains **HOLD with ESCALATE elements**. Stage 3 remains unentered and
unauthorized. This record creates no runtime, integration, orchestration,
market-data, broker, wallet, order, routing, persistence, networking,
deployment, execution, or live-money authority.

## Authoritative Checkpoint and Trigger

The authoritative starting checkpoint is
`3c766a0cf8e9576e69cb923f056e74f66ee06e98` (`fix: align sniperbot fsm
lockout semantics`). At that checkpoint, `main` and `origin/main` are
synchronized at divergence `0/0` with a clean working tree.

The separate read-only implementation-evidence revalidation found that the
evaluator accepts 32 closed but mismatched `transition_request` identifiers as
allowed across four ordinary state pairs:

* eight mismatches for `PAUSE -> READY`;
* eight mismatches for `READY -> ARMED_MANUAL`;
* eight mismatches for `ARMED_AUTO -> IN_TRADE`; and
* eight mismatches for `IN_TRADE -> PAUSE`.

The schema likewise closes the identifier vocabulary but does not define the
complete identifier-to-state-pair relationship. Focused evidence proves exact
identifier coherence only for the locked reset path. This is an acceptance
blocker, not authority to repair implementation.

## Evidence Inspected

This decision is grounded in:

1. the Canonical FSM contract-definition review;
2. the Canonical FSM re-gate founder-decision record, including `FSM-15`;
3. the Canonical FSM schema and interface proposal, including its allowed
   transition table and fail-closed undefined-transition rule;
4. the Canonical FSM schema-semantics founder-decision record;
5. the denial-input classification founder-decision record;
6. the null-authority enforcement founder-decision record;
7. the authority-collision subprecedence founder-decision record, including
   its exact three-field arming and reset subjects;
8. the lockout-semantics founder-decision record, including the exact reset
   exit and locked-state gate;
9. the semantic-discrepancy repair-scope determination;
10. `schemas/sniperbot-fsm-transition-decision.schema.json`;
11. `src/sniperbot/fsm/transition_contract.py`; and
12. `tests/test_sniperbot_fsm_transition_contract.py`.

The earlier records close the identifier vocabulary and govern undefined
transitions, but they do not state one complete rule for every closed
identifier paired with every declared current/requested state combination.
This record supplies that missing semantic link.

## Founder Decision

**FOUNDER DECIDED: select Option B, governed undefined transition.**

Each closed `TransitionRequestName` identifier is semantically applicable only
to its canonical state pair defined below. Supplying a closed identifier with
a non-canonical state pair is a well-formed, typed request, not a structural
boundary error.

After higher-priority forced-lockout, contradiction, and current-lockout
handling, a closed but mismatched identifier produces exactly:

| Decision field | Founder-selected value |
| --- | --- |
| `current_state` | Exact request `current_state` |
| `requested_state` | Exact request `requested_state` |
| `allowed` | `false` |
| `resulting_state` | Exact request `current_state` |
| `reason_code` | `ReasonCode.UNDEFINED_TRANSITION` |
| `required_next_human_or_governance_action` | `RequiredAction.GOVERNANCE_REVIEW` |
| `correlation_reference` | Exact request `correlation_reference` |

The decision is descriptive, deterministic, pure, non-mutating, and
non-authorizing. A mismatched identifier cannot reach ordinary prerequisite,
authority, collision, reset-fact, or allowed-transition evaluation.

## Complete Nine-Identifier Mapping

`Authority applicable` means authority evaluation is required for that exact
subject. JSON must still contain the governed `authority_evidence` property on
every request; explicit null remains permitted only where the null-authority
record permits it.

| `transition_request` identifier | Canonical `current_state` | Canonical `requested_state` | Authority applicable | Reset facts applicable | Exact canonical-subject behavior | Same identifier with a non-canonical state pair |
| --- | --- | --- | --- | --- | --- | --- |
| `PAUSE_TO_READY` | `PAUSE` | `READY` | NO | NO | `readiness_preconditions_satisfied = true` permits `READY / ALLOWED / NONE`; false denies in `PAUSE` with `READINESS_FACTS_MISSING / GOVERNANCE_REVIEW`. | After higher precedence, deny to exact current state with `UNDEFINED_TRANSITION / GOVERNANCE_REVIEW`. |
| `READY_TO_ARMED_MANUAL` | `READY` | `ARMED_MANUAL` | YES | NO | Fully valid authority permits `ARMED_MANUAL / ALLOWED / NONE`; governed authority failures retain `READY` with the published arming reason/action mapping. | After higher precedence, deny to exact current state with `UNDEFINED_TRANSITION / GOVERNANCE_REVIEW`; do not evaluate authority. |
| `READY_TO_ARMED_AUTO` | `READY` | `ARMED_AUTO` | NO | NO | Always denied in `READY` with `TRANSITION_FOUNDER_DENIED / FOUNDER_AUTHORITY_REQUIRED`. | After higher precedence, deny to exact current state with `UNDEFINED_TRANSITION / GOVERNANCE_REVIEW`. |
| `ARMED_AUTO_TO_IN_TRADE` | `ARMED_AUTO` | `IN_TRADE` | NO | NO | `confirmed_position_exists = true` permits `IN_TRADE / ALLOWED / NONE`; false denies in `ARMED_AUTO` with `CONFIRMED_POSITION_FACT_MISSING / GOVERNANCE_REVIEW`. | After higher precedence, deny to exact current state with `UNDEFINED_TRANSITION / GOVERNANCE_REVIEW`. |
| `ARMED_MANUAL_TO_IN_TRADE` | `ARMED_MANUAL` | `IN_TRADE` | NO | NO | Governed excluded transition: deny in `ARMED_MANUAL` with `UNDEFINED_TRANSITION / GOVERNANCE_REVIEW`. | After higher precedence, deny to exact current state with the same `UNDEFINED_TRANSITION / GOVERNANCE_REVIEW` tuple. |
| `IN_TRADE_TO_READY` | `IN_TRADE` | `READY` | NO | NO | Governed prohibited transition: deny in `IN_TRADE` with `UNDEFINED_TRANSITION / GOVERNANCE_REVIEW`. | After higher precedence, deny to exact current state with the same `UNDEFINED_TRANSITION / GOVERNANCE_REVIEW` tuple. |
| `IN_TRADE_TO_PAUSE` | `IN_TRADE` | `PAUSE` | NO | NO | Closed-position and cooldown facts both true permit `PAUSE / ALLOWED / NONE`; the first failing fact retains `IN_TRADE` with its published reason and `GOVERNANCE_REVIEW`. | After higher precedence, deny to exact current state with `UNDEFINED_TRANSITION / GOVERNANCE_REVIEW`. |
| `ANY_TO_LOCKOUT` | Any of the six declared states | `LOCKOUT` | NO | NO | Only `lockout_required = true` activates the forced-lockout safety tuple: `false / LOCKOUT / LOCKOUT_REQUIRED / RESET_REQUIRED`. With the fact false, it does not create an evidence-free lockout; outside the current-lockout gate it is `UNDEFINED_TRANSITION / GOVERNANCE_REVIEW`. | A requested state other than `LOCKOUT` is non-canonical and, after higher precedence, is `UNDEFINED_TRANSITION / GOVERNANCE_REVIEW`; the current-lockout gate remains higher when current state is `LOCKOUT`. |
| `LOCKOUT_TO_PAUSE` | `LOCKOUT` | `PAUSE` | YES | YES | Only fully valid reset authority plus `reset_facts_explicit = true` permits `PAUSE / ALLOWED / NONE`; published reset authority and reset-fact denials retain `LOCKOUT`. | Every other state pair is non-canonical; after higher precedence, deny to exact current state with `UNDEFINED_TRANSITION / GOVERNANCE_REVIEW`. While currently locked, the locked-state gate supplies `LOCKOUT_REQUIRED / RESET_REQUIRED` instead. |

No identifier gains a second canonical pair. No state, transition, reason,
action, input representation, or output field is added.

## Boundary Classification

The selected governed-denial policy applies only when all three identifier
components are individually well formed:

* `current_state` is a member of the closed `State` enum;
* `requested_state` is a member of the closed `State` enum; and
* `transition_request` is a member of the closed `TransitionRequestName` enum.

The following remain boundary errors before FSM evaluation:

* wrong runtime or JSON primitive types;
* an unknown raw state or transition-request enum value;
* a malformed request or nested object;
* a missing required property or Python argument;
* a prohibited extra field;
* an empty or wrong-type mandatory reference; and
* contextually invalid authority null/`None`.

No boundary error becomes `UNDEFINED_TRANSITION`, lockout, an authority
failure, or any other governed decision.

## Deterministic Precedence

The complete selected order is:

1. structural, closed-type, required-field, reference, and runtime-type
   validation;
2. transition-specific null-authority applicability validation;
3. the external `lockout_required = true` forced-lockout safety branch;
4. the already-governed ambiguity/contradiction branch;
5. the current-`LOCKOUT` gate, including the sole exact
   `LOCKOUT_TO_PAUSE` reset exit candidate;
6. transition-request identifier/state-pair coherence and ordinary transition
   legality;
7. transition-specific prerequisite facts;
8. transition-specific authority evaluation and published collision
   subprecedence;
9. reset-fact validation; and
10. the exact allowed or governed-denial decision.

This order resolves the required collisions as follows:

| Simultaneous condition | Founder-selected result |
| --- | --- |
| Malformed `transition_request` representation plus `lockout_required = true` | Boundary rejection. Malformed input never reaches forced lockout. |
| Closed mismatched identifier plus `lockout_required = true` | Forced-lockout tuple wins after successful boundary validation. |
| Closed mismatched identifier plus contradictory position facts | `AMBIGUOUS_OR_CONTRADICTORY_INPUT / HUMAN_REVIEW` wins. |
| Closed mismatched identifier while `current_state = LOCKOUT` | Current-lockout gate wins with `LOCKOUT_REQUIRED / RESET_REQUIRED`, except the exact reset subject proceeds to reset evaluation. |
| Closed mismatched identifier plus failed ordinary prerequisites | Mismatch wins with `UNDEFINED_TRANSITION / GOVERNANCE_REVIEW`; prerequisite facts are not evaluated. |
| Closed mismatched identifier plus authority failure | Mismatch wins with `UNDEFINED_TRANSITION / GOVERNANCE_REVIEW`; authority is not evaluated. |
| Exact `LOCKOUT -> PAUSE` state pair with a wrong closed identifier | Current-lockout gate wins; remain `LOCKOUT` with `LOCKOUT_REQUIRED / RESET_REQUIRED`. |
| `ANY_TO_LOCKOUT` with `lockout_required = false` | Outside current lockout, deny to current state with `UNDEFINED_TRANSITION / GOVERNANCE_REVIEW`; no evidence-free lockout entry. |
| `ANY_TO_LOCKOUT` with `lockout_required = true` from any declared current state | Forced-lockout tuple wins: `false / LOCKOUT / LOCKOUT_REQUIRED / RESET_REQUIRED`. |

The selected coherence rule does not reorder boundary validation, forced
lockout, contradiction handling, or the current-lockout gate.

## Rejected Alternative

**Option A, boundary error, is rejected.**

A closed identifier combined with two closed state values is structurally and
type valid. Treating only their semantic mismatch as malformed would blur the
repository's established distinction between invalid representation and a
well-formed undefined transition. `FSM-15` and the interface proposal already
assign undefined transitions to a deterministic denial without mutation.

The rejected alternative would also make a closed, inspectable request vanish
at the exception boundary instead of producing the existing closed
`UNDEFINED_TRANSITION / GOVERNANCE_REVIEW` explanation. No repository evidence
requires that widening of boundary exceptions.

## Schema Obligations -- Not Implemented Here

A later separately authorized repair must:

* represent all nine canonical mappings where Draft 2020-12 permits;
* reject no well-formed closed mismatch merely for being mismatched;
* constrain a governed mismatch decision to `allowed = false`,
  `UNDEFINED_TRANSITION`, and `GOVERNANCE_REVIEW` where representable;
* preserve current-state retention and exact reference equality at the
  evaluator boundary where sibling comparison is not representable;
* preserve forced-lockout, contradiction, and locked-state branch precedence;
* avoid conflicts between higher- and lower-priority `allOf` branches;
* preserve the required `authority_evidence` property and contextual
  object-or-null behavior; and
* preserve closed vocabularies and `additionalProperties: false`.

This record makes no schema change.

## Evaluator Obligations -- Not Implemented Here

A later separately authorized repair must:

* compare the closed `transition_request` identifier with the complete
  canonical state-pair table after higher-priority branches;
* return the exact governed mismatch tuple before ordinary prerequisite,
  authority, collision, or reset-fact evaluation;
* preserve the current-lockout exact-name gate;
* preserve `ANY_TO_LOCKOUT` as fact-dependent forced lockout only;
* preserve all existing exact-subject reason/action mappings;
* preserve Python omission, explicit `None`, strict-type, and exception
  boundaries;
* preserve reference identity by value, determinism, purity, immutability,
  and non-mutation; and
* add no public API, default, sentinel, coercion, import, capability, or
  package export.

This record makes no evaluator change.

## Focused-Test and Independent-Evidence Obligations -- Not Implemented Here

A later separately authorized repair must directly prove:

* every exact row in the nine-identifier table;
* every closed identifier combined with every non-canonical state pair;
* closure of the 32 currently allowed mismatches;
* the exact mismatch reason/action/current/requested/result/reference tuple;
* every simultaneous-condition precedence row above;
* wrong type, unknown enum, malformed, omitted, prohibited, and invalid
  reference inputs remain boundary errors;
* exact arming and reset authority collision evidence remains unchanged;
* null-authority behavior remains unchanged;
* all 324 forced-lockout combinations and all prohibited lockout exits remain
  unchanged;
* schema/evaluator parity for every repaired branch;
* deterministic equal-but-distinct decisions, reference preservation,
  purity, immutability, and request/evidence non-mutation; and
* absence of skipped, expected-failure, implementation-coupled, or vacuous
  evidence.

Independent revalidation must derive the mapping from this founder record and
must not call a private production helper as its oracle.

## Deferred Null-Authority Wording Finding

The executable schema currently describes null authority as representing
"absent evidence." The controlling null-authority record defines null as
authority not applicable and distinguishes it from a non-null
`AuthorityEvidence` object with `presence = "ABSENT"`.

That wording discrepancy is non-executable and does not alter the decision in
this record. It remains deferred to a separately bounded schema-description
repair. This artifact does not modify, reinterpret, or silently combine that
repair with transition-request coherence.

## Acceptance Impact

The prior read-only implementation-evidence revalidation remains **FAIL**.
Formal current implementation-evidence acceptance is blocked until:

1. a separately authorized schema/evaluator/focused-test coherence repair is
   published;
2. the complete chain is independently revalidated again; and
3. a separate acceptance disposition is founder-authorized and published.

Historical acceptance remains unchanged as historical evidence. This record
does not create acceptance, indexing, Stage 2 completion, Advancement Gate
movement, or Stage 3 authority.

## Non-Goals and Explicit Prohibitions

This record does not:

* implement or test the selected policy;
* change schema behavior or schema descriptions;
* change the evaluator, public API, package, exports, validators, workflows,
  dependencies, runtime, or integration surfaces;
* create new states, transitions, reasons, actions, facts, or authority forms;
* reopen denial-input, null-authority, collision, or lockout semantics;
* authorize automatic lockout, reset, state mutation, or persistence;
* authorize market data, strategy, signals, risk, sizing, simulation,
  backtesting, broker, wallet, order, routing, networking, execution, or
  live-money behavior;
* create or amend acceptance or README indexing; or
* enter Stage 3.

## Final Determination

Closed but mismatched transition-request identifiers are governed undefined
transitions, not boundary errors. Higher-priority forced lockout,
contradiction handling, and the current-lockout gate retain their published
precedence. Ordinary prerequisite, authority, collision, reset-fact, and
allowance evaluation may occur only after exact identifier/state-pair
coherence is established.

Stage 2 remains **HOLD with ESCALATE elements**. Stage 3 remains unentered and
unauthorized. The exact next possible action is a separate founder-authorized
schema/evaluator/focused-test transition-request coherence repair.
