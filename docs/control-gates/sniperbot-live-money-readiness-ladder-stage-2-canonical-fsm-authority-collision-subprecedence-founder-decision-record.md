# SniperBot Live-Money Readiness Ladder Stage 2 Canonical FSM Authority-Collision Subprecedence Founder Decision Record

## Status and Non-Authorization Boundary

DOCUMENTATION ONLY -- GOVERNANCE ONLY -- FOUNDER-DECISION RECORD ONLY --
AUTHORITY-COLLISION SUBPRECEDENCE ONLY -- NOT A SCHEMA REPAIR -- NOT A PYTHON
OR PUBLIC-API CHANGE -- NOT A TEST CHANGE -- NOT IMPLEMENTATION-EVIDENCE
ACCEPTANCE -- NOT README INDEXING -- NOT OVERALL STAGE 2 ACCEPTANCE -- NOT
STAGE 2 COMPLETION -- NOT AN ADVANCEMENT-GATE DECISION -- NOT STAGE 3 ENTRY --
NON-AUTHORIZATION BOUNDARY.

This record formalizes the existing deterministic authority-failure branch
order for the Pure / Canonical FSM. It selects first-applicable-failure
subprecedence and preserves every existing isolated-failure reason/action
mapping for arming and reset.

It creates no schema, implementation, test, acceptance, indexing, integration,
or operational authority. Stage 2 remains **HOLD**. Stage 3 remains
**UNENTERED AND UNAUTHORIZED**.

## Authoritative Checkpoint

Repository: `heliosfi/Echoauth-core`

Authoritative starting checkpoint:
`489aca25cb719502edd5844f1acd3d5ae340e79d`
(`docs: record sniperbot fsm null-authority enforcement decision`).

Before this record was created, `origin` was refreshed once. Local `HEAD`,
local `origin/main`, and refreshed `FETCH_HEAD` all resolved to the
authoritative checkpoint; divergence was `0/0`; the working tree was clean;
no staged or untracked file existed; and no Git lock file existed.

The denial-input classification founder decision at
`ec5b85c41e415a87206b0a6325f92c3a1e0ab7c3` and null-authority enforcement
founder decision at the authoritative checkpoint were present and tracked.

## Founder-Selected Scope

The founder selects exactly one governance lane:

> Canonical FSM authority-collision subprecedence.

This record decides which recognized individual authority failure supplies the
reason and required action when one structurally valid non-null
AuthorityEvidence object contains two or more simultaneously failing,
closed-domain conditions.

It does not decide lockout override semantics and does not perform any repair.

## Three-Rule Protocol Preservation

This record applies
`docs/control-gates/codex-three-rule-repo-protocol.md` without reinterpretation:

1. **Habitat Before Routine.** The habitat is the admitted closed-domain
   multi-failure AuthorityEvidence state space and one new founder record.
2. **Silence Is Not Permission.** Formalizing an observable branch order does
   not authorize implementation, evidence, acceptance, indexing, or runtime.
3. **Stop Outside the Lane.** Null, malformed input, lockout semantics, outer
   transition precedence, and every repair remain outside this lane.

## Controlling Prerequisite Decisions

This record depends on and preserves:

1. the denial-input founder decision, which admits four prerequisite failures
   and ten transition-specific isolated authority-failure conditions;
2. the null-authority enforcement founder decision, which excludes JSON null,
   Python `None`, and missing-required authority input from governed denial and
   collision handling;
3. `FSM-SCHEMA-01`, which identifies `READY -> ARMED_MANUAL` and
   `LOCKOUT -> PAUSE` as authority-required transition classes;
4. `FSM-SCHEMA-05` and `FSM-SCHEMA-06`, which retain current state for the
   ordinary denials governed here;
5. `FSM-SCHEMA-08`, which preserves the exact correlation reference; and
6. the closed ReasonCode and RequiredAction vocabularies.

No prerequisite decision is reopened or superseded.

## Founder Decision

**FOUNDER DECIDED: first applicable failing authority condition wins.**

For a structurally valid, non-null AuthorityEvidence object containing two or
more admitted closed-domain failures, evaluate the named failure branches in
the exact order selected below. The first applicable branch supplies the
complete reason/action mapping. Lower failures do not alter, combine, qualify,
or replace that result.

The selected order formalizes the evaluator's existing deterministic
authority-failure branch order. No composite reason, composite action, list of
reasons, or multi-result decision is permitted.

## Collision Participants

Only these closed-domain AuthorityEvidence failure conditions participate:

1. `AuthorityEvidence.presence == "ABSENT"`;
2. `AuthorityEvidence.currentness == "STALE"`;
3. `AuthorityEvidence.revocation == "REVOKED"`;
4. `AuthorityEvidence.validity_outcome == "OUT_OF_SCOPE"`; and
5. `AuthorityEvidence.validity_outcome == "INVALID"` or
   `AuthorityEvidence.validity_outcome == "AMBIGUOUS"`, treated as the existing
   `AUTHORITY_INVALID` failure family.

All other properties must satisfy their structurally valid closed-domain
requirements. A collision exists only when at least two participating failure
conditions are simultaneously true.

`INVALID`, `AMBIGUOUS`, and `OUT_OF_SCOPE` are mutually exclusive values of
one property. Their relative branch positions remain explicit, but two of
those values cannot coexist in one closed-domain object.

## Excluded Non-Participants

The following are not collision participants:

* JSON null;
* Python `None`;
* omitted required authority input;
* a wrong primitive or runtime type;
* a malformed or alternate authority object;
* an unknown enum or raw value;
* an empty `subject_scope` or `authority_reference` prohibited by the schema;
* a prohibited extra property; or
* any other structurally invalid input.

Those inputs are rejected at the structural/type or transition-specific
null-applicability boundary before governed authority collision handling. The
evaluator's current malformed-value fallback checks are not elevated into
collision governance by this record.

## Exact Authority-Failure Subprecedence

The complete closed-domain authority-failure order is:

1. `presence == "ABSENT"`
2. `currentness == "STALE"`
3. `revocation == "REVOKED"`
4. `validity_outcome == "OUT_OF_SCOPE"`
5. `validity_outcome == "INVALID"` or `"AMBIGUOUS"`

The comparison is strict first-match evaluation. A failure at position 1 wins
over positions 2 through 5; position 2 wins over positions 3 through 5;
position 3 wins over positions 4 and 5; and position 4 precedes the invalid
family where the branch order is relevant.

## Exact Arming Collision Order and Mappings

The arming subject is exactly:

* `current_state = State.READY` (`"READY"`);
* `requested_state = State.ARMED_MANUAL` (`"ARMED_MANUAL"`); and
* `transition_request = TransitionRequestName.READY_TO_ARMED_MANUAL`
  (`"READY_TO_ARMED_MANUAL"`).

For every arming collision, the decision is denied, retains `State.READY`, and
preserves the exact correlation reference.

| Order | First applicable condition | Winning ReasonCode | Winning RequiredAction |
| ---: | --- | --- | --- |
| 1 | `AuthorityEvidence.presence == "ABSENT"` | `ReasonCode.AUTHORITY_MISSING` | `RequiredAction.FOUNDER_AUTHORITY_REQUIRED` |
| 2 | `AuthorityEvidence.currentness == "STALE"` | `ReasonCode.AUTHORITY_STALE` | `RequiredAction.FOUNDER_AUTHORITY_REQUIRED` |
| 3 | `AuthorityEvidence.revocation == "REVOKED"` | `ReasonCode.AUTHORITY_REVOKED` | `RequiredAction.FOUNDER_AUTHORITY_REQUIRED` |
| 4 | `AuthorityEvidence.validity_outcome == "OUT_OF_SCOPE"` | `ReasonCode.AUTHORITY_OUT_OF_SCOPE` | `RequiredAction.GOVERNANCE_REVIEW` |
| 5 | `AuthorityEvidence.validity_outcome == "INVALID"` or `"AMBIGUOUS"` | `ReasonCode.AUTHORITY_INVALID` | `RequiredAction.FOUNDER_AUTHORITY_REQUIRED` |

These are the existing isolated-failure mappings. The collision winner uses
the same mapping as that condition would use alone.

## Exact Reset Collision Order and Mappings

The reset subject is exactly:

* `current_state = State.LOCKOUT` (`"LOCKOUT"`);
* `requested_state = State.PAUSE` (`"PAUSE"`); and
* `transition_request = TransitionRequestName.LOCKOUT_TO_PAUSE`
  (`"LOCKOUT_TO_PAUSE"`).

For every reset collision governed here, the decision is denied, retains
`State.LOCKOUT`, preserves the exact correlation reference, and uses
`RequiredAction.RESET_REQUIRED`.

| Order | First applicable condition | Winning ReasonCode | Winning RequiredAction |
| ---: | --- | --- | --- |
| 1 | `AuthorityEvidence.presence == "ABSENT"` | `ReasonCode.RESET_EVIDENCE_MISSING` | `RequiredAction.RESET_REQUIRED` |
| 2 | `AuthorityEvidence.currentness == "STALE"` | `ReasonCode.AUTHORITY_STALE` | `RequiredAction.RESET_REQUIRED` |
| 3 | `AuthorityEvidence.revocation == "REVOKED"` | `ReasonCode.AUTHORITY_REVOKED` | `RequiredAction.RESET_REQUIRED` |
| 4 | `AuthorityEvidence.validity_outcome == "OUT_OF_SCOPE"` | `ReasonCode.AUTHORITY_OUT_OF_SCOPE` | `RequiredAction.RESET_REQUIRED` |
| 5 | `AuthorityEvidence.validity_outcome == "INVALID"` or `"AMBIGUOUS"` | `ReasonCode.AUTHORITY_INVALID` | `RequiredAction.RESET_REQUIRED` |

The reset mapping preserves the existing remap of the missing-authority branch
to `RESET_EVIDENCE_MISSING`. No new reason or action is created.

## Exhaustive Closed-Domain Collision Partition

The schema-declared enum cross-product has 32 AuthorityEvidence state
combinations across presence, currentness, revocation, and validity: one fully
valid combination, six isolated-failure combinations, and 25 multi-failure
combinations.

The selected order partitions all 25 multi-failure combinations completely:

| Exhaustive group | Combinations | Winning branch |
| --- | ---: | --- |
| `ABSENT` plus at least one stale, revoked, or non-valid validity condition | 15 | Presence/absence branch |
| `PRESENT` and `STALE` plus at least one revoked or non-valid validity condition | 7 | Currentness/stale branch |
| `PRESENT`, `CURRENT`, and `REVOKED` plus `INVALID`, `AMBIGUOUS`, or `OUT_OF_SCOPE` | 3 | Revocation branch |
| **Total** | **25** | **Exactly one first-match winner each** |

For arming, each group's winning branch uses the corresponding arming table
mapping. For reset, it uses the corresponding reset table mapping.

No closed-domain multi-failure combination reaches out-of-scope or invalid as
winner because any second simultaneously representable failure is an earlier
absence, stale, or revoked condition. Their branch positions still govern
isolated failures and any future representable comparison that does not change
the closed AuthorityEvidence contract.

## Input and Property Order Independence

The decision depends only on named typed values, not on:

* JSON property order;
* Python keyword argument order;
* dataclass field traversal order by a caller;
* serialization order;
* construction history; or
* the order in which a caller discovered the evidence.

Reordering an otherwise identical AuthorityEvidence object's properties must
produce the same winning reason and action. Only the founder-selected branch
subprecedence controls the result.

## Prerequisite and Outer Precedence Preservation

Authority-collision subprecedence is nested. It does not change any outer FSM
precedence or input boundary.

The preserved order is:

1. structural/type validation;
2. transition-specific null-authority applicability validation;
3. higher-priority governed FSM prerequisites and collisions;
4. transition-specific authority evaluation;
5. the selected authority-failure subprecedence; and
6. lower transition-specific conditions.

In particular:

* `lockout_required` retains its existing outer first-match precedence, while
  the output semantics of that lockout remain separately undecided;
* contradictory fact handling retains its existing position;
* authority collision handling occurs only in an authority-required transition
  after structurally valid non-null authority input is established; and
* for `LOCKOUT_TO_PAUSE`, the authority result remains evaluated before the
  lower `reset_facts_explicit` failure branch, matching the existing evaluator
  order.

This record does not add, remove, or reorder a top-level transition branch.

## Determinism and Non-Combination Rule

The same well-formed request must always produce the same collision winner.
Every admitted collision has exactly one reason and one required action.

Do not:

* concatenate reason identifiers;
* emit multiple reasons or actions;
* synthesize a composite authority failure;
* select a branch based on input/property order;
* choose a more severe, newer, or caller-preferred failure; or
* allow a lower failure to modify the first winner.

The decision remains pure, descriptive, non-mutating, non-persistent,
network-free, non-authorizing, and non-executing.

## Schema Implications -- Not Authorized

A future separately authorized schema/parity repair must preserve the admitted
closed-domain collision participants and the selected reason/action winner
where Draft 2020-12 representation is required and feasible under
`FSM-SCHEMA-11`.

This record does not edit, repair, or authorize changes to
`schemas/sniperbot-fsm-transition-decision.schema.json`.

## Python Implications -- Not Authorized

The current `_authority_reason` order already reflects the selected
closed-domain failure order. Its null and malformed fallback branches remain
subject to the previously decided input boundaries and are not collision
participants.

A later bounded repair/revalidation must verify exact conformance after the
null-authority API repair. This record does not edit, repair, or authorize
changes to `src/sniperbot/fsm/transition_contract.py`.

## Direct-Test and Evidence Implications -- Not Authorized

Future separately authorized evidence must independently prove:

* every isolated-failure mapping in both transition classes;
* all 25 closed-domain multi-failure combinations for arming;
* all 25 closed-domain multi-failure combinations for reset;
* exact first-match reason/action winners;
* input/property-order independence;
* prerequisite and outer-precedence preservation;
* rejection of null, omission, malformed values, and wrong types before
  collision handling;
* reference preservation, determinism, purity, and non-mutation; and
* absence of composite reasons or actions.

The independent oracle must derive expected winners from this founder record,
not call `_authority_reason` or another production helper. No test or evidence
artifact is created or authorized here.

## Lockout Semantics Explicitly Deferred

This record preserves the existing precedence of the `lockout_required`
condition but does not decide:

* the meaning of `allowed` for a forced lockout;
* requested versus resulting state semantics;
* required action or complete output tuple;
* an exception to or conformance with `FSM-SCHEMA-06`; or
* any schema, Python, or test repair for lockout.

The separate Canonical FSM lockout-semantics founder-decision lane remains
required and is not authorized by this record.

## Deferred Repair and Acceptance Scope

This record does not decide or implement:

* lockout override semantics;
* RequiredAction schema repair;
* denial-input or null-authority schema/API repair;
* authority-subprecedence implementation or direct-test evidence;
* schema/API parity verification;
* implementation-evidence revalidation or acceptance;
* README indexing;
* post-repair semantic re-review;
* overall Stage 2 acceptance or completion;
* Advancement Gate changes; or
* Stage 3 entry.

No deferred action follows automatically. Every later lane requires its own
exact founder order.

## Explicit Prohibitions

Do not use this record to:

* treat null, omission, malformed input, or wrong types as collision failures;
* change a single-failure reason or action mapping;
* create composite reasons or actions;
* vary a result by property or input order;
* change prerequisite or outer FSM precedence;
* select lockout output semantics;
* edit schema, Python, tests, package initializers, acceptance, or README;
* analyze or repair Crypto Deferral or another evaluator lane;
* certify Stage 2 completion or change the Advancement Gate;
* enter or authorize Stage 3; or
* authorize integration, orchestration, runtime, deployment, market data,
  strategy, signals, risk, sizing, broker, exchange, wallet, custody,
  networking, persistence, routing, orders, transactions, execution, or
  live-money behavior.

## Stage 2 HOLD Preservation

Stage 2 remains **HOLD**. This founder decision resolves only the bounded
authority-collision subprecedence question. It does not repair the Canonical
FSM semantic chain, accept Stage 2, certify completion, or update the
Advancement Gate.

## Stage 3 Non-Authorization Preservation

Stage 3 remains **UNENTERED AND UNAUTHORIZED**. No integration, runtime,
deployment, execution, or live-money authority is created.

## Refusal and Halt Conditions

Refuse and halt any attempt to:

* include a non-participating invalid input in collision handling;
* reorder the selected five failure branches;
* alter an isolated-failure mapping;
* create a combined reason or action;
* use property order to select a winner;
* change top-level prerequisite or lockout precedence;
* decide lockout output semantics;
* perform a repair without separate exact authorization;
* modify an unlisted file or broaden this lane; or
* infer Stage 2 acceptance, completion, advancement, or Stage 3 authority.

Any later contract conflict, ambiguity, validation failure, unexpected file
change, dirty tree, divergence, Git lock, or prohibited capability requires a
stop and discrepancy report.

## Final Determination

* Authority-collision subprecedence: **FOUNDER DECIDED**
* Selection rule: **FIRST APPLICABLE FAILURE WINS**
* Ordered failure branches: **ABSENT, STALE, REVOKED, OUT_OF_SCOPE, INVALID**
* `AMBIGUOUS` mapping: **AUTHORITY_INVALID FAMILY**
* Arming order and mappings complete: **YES**
* Reset order and mappings complete: **YES**
* Existing single-failure mappings preserved: **YES**
* Closed-domain multi-failure combinations governed: **25**
* Input/property order affects result: **NO**
* Composite reasons or actions permitted: **NO**
* Null, omission, malformed input, or wrong types participate: **NO**
* Prerequisite and outer precedence changed: **NO**
* Lockout semantics decided: **NO**
* Repairs performed or authorized: **NO**
* Schema changed: **NO**
* Python changed: **NO**
* Tests changed: **NO**
* README changed: **NO**
* Implementation-evidence acceptance created: **NO**
* Overall Stage 2 acceptance: **NO**
* Stage 2 completion: **NO**
* Advancement Gate changed: **NO**
* Stage 2: **HOLD**
* Stage 3: **UNENTERED AND UNAUTHORIZED**

The existing authority branch order is now founder-governed for all admitted
closed-domain collisions. Arming and reset retain their exact individual
reason/action mappings. Lockout output semantics and every repair remain
deferred. No repository behavior is changed.
