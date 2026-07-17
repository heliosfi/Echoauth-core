# SniperBot Live-Money Readiness Ladder Stage 2 Canonical FSM Denial-Input Classification Founder Decision Record

## Status and Non-Authorization Boundary

DOCUMENTATION ONLY -- GOVERNANCE ONLY -- FOUNDER-DECISION RECORD ONLY --
DENIAL-INPUT CLASSIFICATION ONLY -- NOT A SCHEMA REPAIR -- NOT A PYTHON OR
PUBLIC-API CHANGE -- NOT A TEST CHANGE -- NOT IMPLEMENTATION-EVIDENCE
ACCEPTANCE -- NOT README INDEXING -- NOT OVERALL STAGE 2 ACCEPTANCE -- NOT
STAGE 2 COMPLETION -- NOT AN ADVANCEMENT-GATE DECISION -- NOT STAGE 3 ENTRY --
NON-AUTHORIZATION BOUNDARY.

This record captures the founder-selected admissibility rule for closed-domain
negative prerequisite facts and individually recognized authority failures in
the Pure / Canonical FSM lane. It creates no schema, implementation, test,
acceptance, indexing, integration, orchestration, runtime, deployment,
execution, or live-money authority.

Stage 2 remains **HOLD**. Stage 3 remains **UNENTERED AND UNAUTHORIZED**.

## Authoritative Checkpoint

Repository: `heliosfi/Echoauth-core`

Authoritative starting checkpoint:
`ebe2f41e63ab6cfcb5324b77d6c180999e4beb3a`
(`docs: add sniperbot canonical fsm semantic repair-scope determination`).

At decision-record start, local `HEAD`, local `origin/main`, and live
`refs/heads/main` resolved to that checkpoint; divergence was `0/0`; the
working tree was clean; no staged or untracked file existed; and no Git lock
file existed. The checkpoint commit created exactly
`docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-canonical-fsm-semantic-discrepancy-repair-scope-determination.md`
and changed no existing file.

## Founder-Selected Scope

The founder selects exactly one governance lane:

> Canonical FSM denial-input classification.

The decision answers whether each named closed-domain failing prerequisite or
individual authority condition is a valid typed request that receives a
`TransitionDecision`, or an invalid request rejected before decision creation.

This record does not decide JSON omission versus null, Python omission versus
`None`, null-authority enforcement or exception type, authority multi-failure
collision order, lockout override semantics, or any repair.

## Three-Rule Protocol Preservation

This record applies
`docs/control-gates/codex-three-rule-repo-protocol.md` without reinterpretation:

1. **Habitat Before Routine.** The habitat is one founder decision about the
   admissibility of the 14 named denial conditions and one new record.
2. **Silence Is Not Permission.** Admitting a descriptive denial input does not
   authorize schema, Python, test, acceptance, README, runtime, or operational
   work.
3. **Stop Outside the Lane.** Null behavior, collision subprecedence, lockout
   semantics, Crypto Deferral, and every repair remain separate lanes.

## Controlling Discrepancy

The post-construction semantic-consistency review found that current schema
conditionals reject valid closed-domain requests with false prerequisites or
non-valid authority, while the Python evaluator accepts those inputs and emits
closed denial decisions. The repair-scope determination identified denial-input
admissibility as an independent founder question that must precede repair.

The discrepancy concerns input classification, not whether a failed condition
can allow a transition. Existing governance already establishes that a failed
prerequisite or authority condition never grants permission.

## Existing Governance Reviewed

This decision preserves the final controlling records and their boundaries:

* `FSM-01` through `FSM-03` defer authority until arming and require valid
  authority before manual arming may be allowed;
* `FSM-05` requires an externally supplied confirmed-position fact;
* `FSM-08` requires position-closed and cooldown facts;
* `FSM-11` requires bounded reset evidence and reset facts;
* `FSM-12` makes absent, stale, ambiguous, contradictory, out-of-scope, and
  revoked authority non-permission;
* `FSM-13` keeps denial descriptive and non-persistent;
* `FSM-15` denies without mutation;
* `FSM-16` requires a closed reason-code set;
* `FSM-17` requires an opaque caller reference;
* `FSM-SCHEMA-05` and `FSM-SCHEMA-06` retain current state for ordinary denied
  requests;
* `FSM-SCHEMA-08` requires exact request/decision reference equality; and
* `FSM-SCHEMA-09` controls the five non-null required actions and their
  existing mappings.

The existing schema conditionals express prerequisite requirements as input
rejection. This record narrows the meaning of those requirements: they remain
conditions for allowance, but their closed-domain failure values are admitted
for deterministic denial classification. No schema change occurs here.

## Founder Decision

**FOUNDER DECIDED: all named closed-domain negative prerequisite facts and all
individually recognized authority-failure states are valid typed Canonical FSM
requests.**

They must not be rejected merely because the requested transition cannot be
allowed. For every admitted request, the evaluator must return a deterministic
governed denial `TransitionDecision` using the closed reason and required-action
vocabularies.

This decision establishes admissibility only. A failing condition never grants
permission, changes authority ownership, performs a state mutation, or
authorizes execution.

## Denial-Input Classification Rule

Category A is **admitted negative evidence**:

* the request object and every nested object are structurally valid;
* every value belongs to its closed typed vocabulary;
* every required field and non-null reference is otherwise valid; and
* one named prerequisite boolean is false or one recognized individual
  authority failure is present.

Category A is a valid typed request. It receives a denial decision with
`allowed = false`, current-state retention, an exact closed reason, an exact
closed required action, exact correlation-reference preservation, and no
mutation.

Category B is **malformed or unknown input**: wrong primitive type, unknown
enum, malformed nested object, prohibited extra field, invalid reference, or a
value outside the governed vocabulary. Category B remains invalid and is
rejected at the applicable validation or API boundary before a governed
denial-classification decision under this record.

The founder labels `ready_for_entry` and `position_confirmed` do not add or
rename fields. They map to the existing governed fields
`readiness_preconditions_satisfied` and `confirmed_position_exists`.
"Missing/false" for a boolean means the governed boolean is present with value
`false`; omission of a required field remains malformed.

## Exact Admitted Negative-Input Inventory

The admitted prerequisite conditions are:

1. `PAUSE -> READY` with
   `external_facts.readiness_preconditions_satisfied = false`.
2. `ARMED_AUTO -> IN_TRADE` with
   `external_facts.confirmed_position_exists = false`.
3. `IN_TRADE -> PAUSE` with `external_facts.position_closed = false` and
   `external_facts.cooldown_complete = true`, isolating position-close failure.
4. `IN_TRADE -> PAUSE` with `external_facts.position_closed = true` and
   `external_facts.cooldown_complete = false`, isolating cooldown failure.

The admitted individual authority conditions apply separately to
`READY -> ARMED_MANUAL` and `LOCKOUT -> PAUSE`:

5. recognized missing authority represented by a structurally valid non-null
   `AuthorityEvidence` object with `presence = "ABSENT"`;
6. stale authority represented by `currentness = "STALE"`;
7. revoked authority represented by `revocation = "REVOKED"`;
8. out-of-scope authority represented by
   `validity_outcome = "OUT_OF_SCOPE"`; and
9. invalid authority represented by `validity_outcome = "INVALID"` or the
   existing recognized ambiguous validity value `"AMBIGUOUS"`, both within the
   closed validity vocabulary and both classified by the closed
   `AUTHORITY_INVALID` reason family when individually isolated.

Each authority condition in this inventory is considered individually with
all other authority fields set to their valid closed-domain values. Any object
containing two or more simultaneous authority failures belongs to the deferred
authority-collision decision, not this record.

## Exact Excluded Malformed-Input Inventory

This decision does not admit:

* an omitted required request, facts, authority-object, or reference field;
* explicit authority `null` or Python `None`, whose classification is deferred;
* a wrong primitive type, including non-boolean fact values;
* an unknown state, transition-request name, authority enum, reason, or action;
* a malformed request, `ExternalFacts`, or `AuthorityEvidence` object;
* a prohibited additional JSON property;
* empty or wrong-type mandatory opaque references;
* an unknown raw string where a closed enum value is required;
* an unsupported authority representation or alternate object shape; or
* a multi-failure authority collision, whose input may be structurally valid
  but whose winning reason/action remains separately undecided.

The last item is deferred rather than declared malformed. This record admits
each recognized failure individually but does not rank simultaneous failures.

## Per-Condition Decision Matrix

`Current` in the resulting-state column means exact current-state retention.
Every row requires exact correlation-reference preservation and no mutation.

| # | Condition | Transition class | Valid typed request | Decision created | Allowed | Resulting state | Reason code | Required action | Authority involved | Null decision still required | Collision decision still required |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Readiness false | `PAUSE -> READY` | YES | YES | NO | Current (`PAUSE`) | `READINESS_FACTS_MISSING` | `GOVERNANCE_REVIEW` | NO | NO | NO |
| 2 | Confirmed position false | `ARMED_AUTO -> IN_TRADE` | YES | YES | NO | Current (`ARMED_AUTO`) | `CONFIRMED_POSITION_FACT_MISSING` | `GOVERNANCE_REVIEW` | NO | NO | NO |
| 3 | Position not closed | `IN_TRADE -> PAUSE` | YES | YES | NO | Current (`IN_TRADE`) | `POSITION_CLOSED_FACT_MISSING` | `GOVERNANCE_REVIEW` | NO | NO | NO |
| 4 | Cooldown incomplete, with position closed | `IN_TRADE -> PAUSE` | YES | YES | NO | Current (`IN_TRADE`) | `COOLDOWN_FACT_MISSING` | `GOVERNANCE_REVIEW` | NO | NO | NO |
| 5 | Arming authority missing through non-null `presence = ABSENT` | `READY -> ARMED_MANUAL` | YES | YES | NO | Current (`READY`) | `AUTHORITY_MISSING` | `FOUNDER_AUTHORITY_REQUIRED` | YES | YES | YES |
| 6 | Arming authority stale | `READY -> ARMED_MANUAL` | YES | YES | NO | Current (`READY`) | `AUTHORITY_STALE` | `FOUNDER_AUTHORITY_REQUIRED` | YES | YES | YES |
| 7 | Arming authority revoked | `READY -> ARMED_MANUAL` | YES | YES | NO | Current (`READY`) | `AUTHORITY_REVOKED` | `FOUNDER_AUTHORITY_REQUIRED` | YES | YES | YES |
| 8 | Arming authority out of scope | `READY -> ARMED_MANUAL` | YES | YES | NO | Current (`READY`) | `AUTHORITY_OUT_OF_SCOPE` | `GOVERNANCE_REVIEW` | YES | YES | YES |
| 9 | Arming authority invalid or individually ambiguous | `READY -> ARMED_MANUAL` | YES | YES | NO | Current (`READY`) | `AUTHORITY_INVALID` | `FOUNDER_AUTHORITY_REQUIRED` | YES | YES | YES |
| 10 | Reset authority missing through non-null `presence = ABSENT` | `LOCKOUT -> PAUSE` | YES | YES | NO | Current (`LOCKOUT`) | `RESET_EVIDENCE_MISSING` | `RESET_REQUIRED` | YES | YES | YES |
| 11 | Reset authority stale | `LOCKOUT -> PAUSE` | YES | YES | NO | Current (`LOCKOUT`) | `AUTHORITY_STALE` | `RESET_REQUIRED` | YES | YES | YES |
| 12 | Reset authority revoked | `LOCKOUT -> PAUSE` | YES | YES | NO | Current (`LOCKOUT`) | `AUTHORITY_REVOKED` | `RESET_REQUIRED` | YES | YES | YES |
| 13 | Reset authority out of scope | `LOCKOUT -> PAUSE` | YES | YES | NO | Current (`LOCKOUT`) | `AUTHORITY_OUT_OF_SCOPE` | `RESET_REQUIRED` | YES | YES | YES |
| 14 | Reset authority invalid or individually ambiguous | `LOCKOUT -> PAUSE` | YES | YES | NO | Current (`LOCKOUT`) | `AUTHORITY_INVALID` | `RESET_REQUIRED` | YES | YES | YES |

## Resulting-State Rule

Every denial in the matrix retains the request's exact current state. It does
not result in the requested state, create a separate state, or mutate either
state object. The decision remains descriptive only.

This rule applies to the 14 ordinary denial conditions only. It does not decide
the separate forced-lockout collision, where the current schema and evaluator
disagree with the general allowed/resulting-state invariant.

## Reason and Required-Action Rule

Each matrix row uses the existing closed reason and required-action vocabulary.
No free-text reason or new action is introduced.

* prerequisite failures use their exact fact-missing reason and
  `GOVERNANCE_REVIEW`;
* missing, stale, revoked, and invalid arming authority use
  `FOUNDER_AUTHORITY_REQUIRED`;
* out-of-scope arming authority uses `GOVERNANCE_REVIEW`; and
* every reset-authority failure uses `RESET_REQUIRED`, with non-null absent
  authority mapped to `RESET_EVIDENCE_MISSING`.

These mappings govern isolated individual failures. This record does not
select which reason/action wins when multiple authority failures coexist.

## Schema Implications

The current schema's affirmative-fact and `ValidAuthorityEvidence`
conditionals reject the admitted denial requests. A future separately
authorized schema repair must distinguish structural/type validity from the
conditions required for allowance and must admit every matrix row.

Where Draft 2020-12 can represent the corresponding decision relationship, a
future repair must preserve `allowed = false`, current-state retention, the
closed reason/action mapping, and exact reference requirements. Base closed
types, required fields, additional-property prohibitions, and malformed-input
rejection remain in force.

This record does not determine authority nullability and does not authorize any
schema edit.

## Python API and Evaluator Implications

The Python surface must eventually preserve the same Category A versus
Category B boundary: admitted closed-domain failures produce decisions;
malformed or unknown inputs remain rejected at their applicable boundary.

The current evaluator already emits the matrix mappings for isolated non-null
failure representations, but that observation is not implementation-evidence
acceptance and authorizes no source change. A later independent repair or
verification order must determine exact conformance after all dependent
founder decisions are published.

This record does not alter dataclass fields, annotations, defaults, signatures,
exception behavior, public exports, or evaluator code.

## Direct-Test Implications

A future separately authorized direct-test lane must prove every matrix row
independently, including:

* valid request construction without rejection;
* creation of a `TransitionDecision`;
* `allowed = false` and exact current-state retention;
* exact reason and required action;
* exact correlation-reference preservation;
* request/facts/authority non-mutation and deterministic repeated results; and
* continued rejection of Category B malformed or unknown input.

Authority tests must isolate one failure at a time. Null/`None` tests and
multi-failure collision tests are prohibited until their separate founder
decisions are published. No test is added or changed by this record.

## Null-Authority Decision Explicitly Deferred

This record does not classify JSON omission, JSON null, Python constructor
omission, or explicit Python `None`. It does not select the enforcement point,
exception type, or whether those representations create a decision.

The matrix's missing-authority rows use only a non-null, structurally valid
AuthorityEvidence object with `presence = "ABSENT"`. The separate
null-authority enforcement founder-decision lane remains required.

## Authority-Collision Decision Explicitly Deferred

This record admits every recognized authority failure when individually
isolated. It does not rank absence, stale, revoked, out-of-scope, invalid, or
ambiguous states when two or more coexist.

The current `_authority_reason` ordering is not adopted as governance. The
separate authority-collision subprecedence founder-decision lane remains
required before collision implementation or test evidence.

## Lockout-Semantics Decision Explicitly Deferred

This record does not decide `lockout_required` override behavior, the meaning
of `allowed` for a forced lockout, the resulting-state exception, required
action, reason mapping, or interaction with `FSM-SCHEMA-06`.

The matrix's `LOCKOUT -> PAUSE` rows concern reset-authority denial only when
the separate forced-lockout collision is not winning. The lockout-semantics
founder-decision lane remains required.

## Required Future Repair Boundary

No future action follows automatically. A later exact founder order is required
before any schema, Python, or test change.

The narrow future denial-input repair subject is limited to aligning schema
admissibility and direct evidence with this 14-row matrix, plus any Python
surface correction independently shown necessary. Null authority,
multi-failure collision order, lockout semantics, RequiredAction nullability,
acceptance revalidation, and README indexing remain separately bounded.

Every future repair order must name exact files, validation, scope, and stop
conditions. This record itself grants no repair authority.

## Explicit Exclusions

This record does not:

* modify the FSM schema, Python evaluator, direct tests, package initializers,
  historical acceptance, README, or any existing governance record;
* decide null-authority representation or exception behavior;
* decide authority multi-failure subprecedence;
* decide lockout override semantics;
* repair RequiredAction nullability;
* analyze or repair Crypto Deferral or another evaluator lane;
* create implementation-evidence acceptance or overall Stage 2 acceptance;
* certify Stage 2 completion or change the Advancement Gate;
* enter or authorize Stage 3; or
* authorize integration, orchestration, runtime, deployment, market data,
  strategy, signals, risk, sizing, broker, exchange, wallet, custody,
  networking, persistence, routing, orders, transactions, execution, or
  live-money behavior.

## Stage 2 HOLD Preservation

Stage 2 remains **HOLD**. This founder decision resolves only denial-input
classification. It does not satisfy the remaining Canonical FSM decisions,
repair the semantic chain, accept Stage 2, certify completion, or update the
Advancement Gate.

## Stage 3 Non-Authorization Preservation

Stage 3 remains **UNENTERED AND UNAUTHORIZED**. No integration, runtime,
deployment, execution, or live-money authority is created.

## Refusal and Halt Conditions

Refuse and halt any attempt to use this record to:

* treat explicit null or Python `None` as admitted or rejected;
* adopt the current `_authority_reason` order as founder-selected;
* decide a multi-failure collision or lockout override;
* repair schema, Python, tests, acceptance, or README;
* add an enum, field, reason, action, state, or transition;
* weaken malformed/unknown-input rejection;
* analyze Crypto Deferral or another lane;
* infer overall Stage 2 acceptance, completion, or advancement; or
* authorize Stage 3 or any operational capability.

Any later ambiguity, scope expansion, unexpected file change, validation
failure, dirty tree, divergence, Git lock, or prohibited capability requires a
stop and discrepancy report.

## Final Determination

* Denial-input classification: **FOUNDER DECIDED**
* Closed-domain negative prerequisite inputs: **VALID TYPED REQUESTS**
* Recognized individual authority-failure inputs: **VALID TYPED REQUESTS**
* Governed denial decision required: **YES**
* Schema repair authorized by this record: **NO**
* Python repair authorized by this record: **NO**
* Test repair authorized by this record: **NO**
* Null-authority semantics decided: **NO**
* Authority-collision subprecedence decided: **NO**
* Lockout semantics decided: **NO**
* Overall Stage 2 acceptance: **NO**
* Stage 2 completion: **NO**
* Advancement decision changed: **NO**
* Stage 2: **HOLD**
* Stage 3: **UNENTERED AND UNAUTHORIZED**

The 14 named closed-domain denial conditions are admitted and require exact,
deterministic, non-mutating denial decisions. Malformed and unknown inputs
remain invalid. No repair is performed or authorized.
