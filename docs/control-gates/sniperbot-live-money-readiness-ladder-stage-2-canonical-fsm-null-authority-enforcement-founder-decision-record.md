# SniperBot Live-Money Readiness Ladder Stage 2 Canonical FSM Null-Authority Enforcement Founder Decision Record

## Status and Non-Authorization Boundary

DOCUMENTATION ONLY -- GOVERNANCE ONLY -- FOUNDER-DECISION RECORD ONLY --
NULL-AUTHORITY ENFORCEMENT ONLY -- NOT A SCHEMA REPAIR -- NOT A PYTHON OR
PUBLIC-API CHANGE -- NOT A TEST CHANGE -- NOT IMPLEMENTATION-EVIDENCE
ACCEPTANCE -- NOT README INDEXING -- NOT OVERALL STAGE 2 ACCEPTANCE -- NOT
STAGE 2 COMPLETION -- NOT AN ADVANCEMENT-GATE DECISION -- NOT STAGE 3 ENTRY --
NON-AUTHORIZATION BOUNDARY.

This record preserves and clarifies the binding Canonical FSM null-authority
contract. It establishes the target boundary for a later separately authorized
repair. It does not modify schema, Python, tests, acceptance, README, runtime,
or any operational surface.

Stage 2 remains **HOLD**. Stage 3 remains **UNENTERED AND UNAUTHORIZED**.

## Authoritative Checkpoint

Repository: `heliosfi/Echoauth-core`

Authoritative starting checkpoint:
`ec5b85c41e415a87206b0a6325f92c3a1e0ab7c3`
(`docs: record sniperbot fsm denial-input classification decision`).

At record start, local `HEAD`, local `origin/main`, and live
`refs/heads/main` resolved to that checkpoint; divergence was `0/0`; the
working tree was clean; no staged or untracked file existed; and no Git lock
file existed. The denial-input founder-decision record was present and tracked.

## Withdrawn Prior Direction

The earlier, unpublished null-authority execution direction is withdrawn. It
would have rejected explicit null for every transition and allowed JSON
omission for non-authority transitions, contrary to binding `FSM-SCHEMA-10`
and the published schema's required-property contract.

No artifact, commit, or repository change resulted from that withdrawn
direction. This record does not preserve or apply it.

## Controlling Authority and Contract Hierarchy

The following existing authority remains binding:

1. `FSM-SCHEMA-10`, `NULL_ONLY_FOR_NON_AUTHORITY_TRANSITIONS`: null authority
   evidence is permitted only where the transition does not require authority.
2. The published `TransitionRequest` schema requires the
   `authority_evidence` property on every request and permits its value to be an
   AuthorityEvidence object or null.
3. `FSM-SCHEMA-01` identifies `READY -> ARMED_MANUAL` and
   `LOCKOUT -> PAUSE` as authority-required transition classes.
4. `FSM-SCHEMA-11` requires schema enforcement where representable and pure
   evaluator enforcement for cross-object or procedural rules.
5. The denial-input founder-decision record admits only well-formed
   closed-domain prerequisite failures and isolated non-null authority-failure
   objects for governed denial classification.

The earlier schema/interface proposal's provisional statement that authority
evidence was required only for arming/reset does not override the later final
schema-semantics decision or the published required-property schema. The
current Python dataclass default is existing implementation behavior to be
assessed in a later repair lane; it is not a founder decision that supersedes
this record.

This record clarifies the final contract. It does not amend, repeal, or
supersede `FSM-SCHEMA-10` or any other schema-semantics founder decision.

## Founder Decision Summary

The founder selects the following complete null-authority enforcement rule:

* `authority_evidence` remains a required JSON property on every Canonical FSM
  request;
* JSON omission is invalid for every transition;
* explicit JSON null is valid only where the selected transition does not
  require authority evidence;
* Python omission of the required authority argument is `TypeError`;
* explicit Python `None` represents JSON null and is valid only for a
  non-authority transition;
* explicit Python `None` for an authority-required transition is `ValueError`;
* validation occurs before governed denial precedence or transition selection;
  and
* neither omission nor null enlarges the governed denial domain.

No default, sentinel, coercion, signature change, or repair is introduced by
this documentation-only record.

## Required JSON Property Decision

`authority_evidence` remains required on every Canonical FSM request.

JSON omission is invalid for every transition, including a transition that
does not require authority evidence. Omission is a missing required property
and must be rejected during structural schema validation.

This record does not remove, conditionalize, or weaken the published schema's
required-property rule.

## Explicit JSON Null Decision

Explicit JSON null is a valid authority-evidence representation only when the
selected transition does not require authority evidence.

For such a transition, null means exactly:

* authority evidence is not applicable;
* no authority evaluation is required;
* no authority denial is implied; and
* no authority failure is synthesized.

Null does not mean false, denied, unavailable, malformed, failed, omitted, or
permission to bypass another prerequisite. It is a present property with the
contextually permitted null value.

## Authority-Required Transition Decision

For a transition requiring authority evidence, `authority_evidence` must
contain the contractually required AuthorityEvidence object. Under the final
current contract, the authority-required transition classes are:

1. `READY -> ARMED_MANUAL`; and
2. `LOCKOUT -> PAUSE`.

For those transition classes:

* explicit null is contextually invalid;
* null is rejected before governed denial evaluation;
* null is not converted to `presence = "ABSENT"`;
* null is not converted into any individual authority-failure condition;
* null produces no governed denial `TransitionDecision`; and
* null never allows evaluation to continue through authority or transition
  selection.

This record does not change which transitions require authority and does not
decide forced-lockout semantics.

## Python Omission and None Decision

The target Python request contract must require an `authority_evidence`
argument so that Python preserves the schema-level required-property boundary.

* Omitting that required constructor or function argument is normal Python
  missing-argument `TypeError`.
* Explicit `None` is the Python representation corresponding to JSON null.
* Explicit `None` is valid only for a transition that does not require
  authority evidence.
* Explicit `None` for an authority-required transition is a contextually
  invalid value and belongs to the `ValueError` boundary.
* A wrong runtime type other than the permitted contextual `None` belongs to
  the `TypeError` boundary.

Omission must not be coerced into `None`. `None` must not be coerced into an
AuthorityEvidence object, `presence = "ABSENT"`, or any authority-failure
condition.

The current Python dataclass has a default of `None`. This record establishes
the target contract for a later bounded repair but does not change that
default, the dataclass, a signature, or any source file in this lane.

## JSON and Python Parity Matrix

| Context | JSON representation | JSON boundary | Python representation | Python boundary | Governed decision created |
| --- | --- | --- | --- | --- | --- |
| Any transition | `authority_evidence` omitted | Schema rejection: missing required property | Required argument omitted | `TypeError` | NO |
| Authority-required transition | Explicit null | Transition-specific validation rejection | Explicit `None` | `ValueError` | NO |
| Non-authority transition | Explicit null | Valid present property; authority not applicable | Explicit `None` | Valid input | Not for authority absence; ordinary FSM evaluation may continue |
| Authority-required transition | Wrong non-null JSON type | Schema rejection | Wrong non-null runtime type | `TypeError` | NO |
| Authority-required transition | Well-formed isolated failure object admitted by the denial-input record | Valid closed-domain input | Well-formed AuthorityEvidence object | Valid closed-domain input | YES, governed denial |

The last row does not rank simultaneous authority failures. Collision
subprecedence remains deferred.

## Enforcement Point and Boundary Order

Null, missing-required, malformed, or wrong-type authority input is enforced
before governed FSM denial precedence or transition selection.

The boundary order is exactly:

1. structural and type validation;
2. transition-specific null-authority applicability validation;
3. governed prerequisite and authority-denial evaluation; and
4. transition selection.

Rejected input does not enter the next boundary. No rejected input can trigger
authority-collision handling, state selection, state mutation, or a governed
denial result.

## JSON Validation Boundary

The JSON rules are:

* missing `authority_evidence` -> schema rejection;
* wrong JSON type -> schema rejection;
* explicit null on an authority-required transition -> transition-specific
  validation rejection; and
* explicit null on a non-authority transition -> valid present property with
  authority not applicable.

The published schema already represents the required property, base
object-or-null type, and authority-required transition conditionals. A later
repair/revalidation lane must determine complete alignment with this record;
this lane changes no schema.

## Python Exception Boundary

The Python rules are:

* omitted required argument -> `TypeError`;
* wrong runtime type -> `TypeError`;
* explicit `None` on an authority-required transition -> `ValueError`; and
* explicit `None` on a non-authority transition -> valid input.

`ValueError` is not newly assigned to omission or wrong-type input. No exception
is converted into a governed denial decision, and no invalid input is coerced.

This is target governance only. Python implementation and direct evidence
require separate founder authorization.

## Governed-Decision Boundary

Only well-formed, typed, closed-domain negative inputs admitted by the
published denial-input founder-decision record may produce governed denials.
That admitted domain remains:

* four closed-domain negative prerequisite conditions; and
* ten transition-specific isolated authority-failure conditions represented by
  non-null, structurally valid AuthorityEvidence objects.

The missing-authority conditions use a non-null AuthorityEvidence object with
`presence = "ABSENT"`. JSON null, Python `None`, and missing-required input are
not substitutes for that object and remain outside the governed-denial domain.

## Non-Authority Transition Boundary

For a transition that the existing contract classifies as not requiring
authority evidence:

* the JSON `authority_evidence` property must still be present;
* its value may be null under `FSM-SCHEMA-10`;
* Python may receive explicit `None`;
* no authority evaluation is required; and
* no authority failure or denial is inferred from that null/`None` value.

This record does not broaden the set of non-authority transitions and does not
decide whether unrelated or prohibited authority fields may be supplied.
Existing transition classification and object-shape rules remain binding.

## Existing Authority Preserved

This record expressly preserves:

* `FSM-SCHEMA-10` as binding;
* the existing schema-level required-property contract;
* `FSM-SCHEMA-01` authority-required transition classification;
* the schema-versus-evaluator enforcement boundary in `FSM-SCHEMA-11`;
* the denial-input record's closed admitted denial domain;
* EchoAuth as the sole owner of permission authority; and
* every existing non-authorization boundary.

This decision clarifies transition-specific enforcement. It does not amend,
repeal, or supersede the schema-semantics founder record.

## Schema Implications -- Not Authorized

The target schema contract retains a required `authority_evidence` property and
the object-or-null base representation, while enforcing the authority-required
transition restriction before decision evaluation.

No schema edit, amendment, validation change, or schema repair is authorized or
performed by this record.

## Python Implications -- Not Authorized

The target Python contract requires the authority argument, distinguishes
omission from explicit `None`, applies the contextual `ValueError` rule, and
preserves explicit `None` only for non-authority transitions.

No dataclass, default, sentinel, signature, constructor, evaluator, export, or
exception implementation is changed or authorized by this record.

## Test Implications -- Not Authorized

Future separately authorized direct evidence must distinguish:

* omitted JSON property from explicit JSON null;
* omitted Python argument from explicit Python `None`;
* authority-required from non-authority transitions;
* `TypeError` from contextual `ValueError`;
* rejected input from admitted isolated authority-failure denial input; and
* enforcement before precedence, collision handling, or transition selection.

No test is added, changed, or authorized by this record.

## Deferred Decisions and Work

This record does not decide or implement:

* authority multi-failure collision subprecedence;
* lockout semantics;
* schema repair;
* Python or public-API repair;
* test repair or evidence completion;
* implementation-evidence revalidation or acceptance;
* README indexing;
* overall Stage 2 acceptance or completion;
* Advancement Gate changes; or
* Stage 3 entry.

RequiredAction nullability remains a separately governed repair subject. No
deferred subject follows automatically from this record.

## Explicit Prohibitions

Do not use this record to:

* omit `authority_evidence` from a JSON request;
* treat null or `None` as absent authority, an authority failure, a denial, or
  permission;
* add a default, sentinel, coercion, or signature change;
* select an authority-collision winner;
* select or implement lockout behavior;
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
null-authority enforcement question. It does not repair the Canonical FSM
semantic chain, accept Stage 2, certify completion, or update the Advancement
Gate.

## Stage 3 Non-Authorization Preservation

Stage 3 remains **UNENTERED AND UNAUTHORIZED**. No integration, runtime,
deployment, execution, or live-money authority is created.

## Refusal and Halt Conditions

Refuse and halt any attempt to:

* treat omission and explicit null as the same representation;
* reject permitted null on a non-authority transition;
* accept null on an authority-required transition;
* convert null or `None` into an admitted authority failure;
* assign omission or wrong type to `ValueError`;
* apply the Python `None` default as the target governed signature;
* perform a repair without a separate exact founder order;
* decide authority collision or lockout semantics;
* modify an unlisted file or broaden this lane; or
* infer Stage 2 acceptance, completion, advancement, or Stage 3 authority.

Any later contract conflict, ambiguity, validation failure, unexpected file
change, dirty tree, divergence, Git lock, or prohibited capability requires a
stop and discrepancy report.

## Final Determination

* Null-authority enforcement: **FOUNDER DECIDED**
* `FSM-SCHEMA-10` preserved: **YES**
* JSON `authority_evidence` property required on every request: **YES**
* JSON omission valid: **NO**
* JSON null valid for non-authority transitions: **YES**
* JSON null valid for authority-required transitions: **NO**
* Python authority argument required: **YES**
* Python omission boundary: **TYPEERROR**
* Python explicit `None` valid for non-authority transitions: **YES**
* Python explicit `None` on authority-required transitions: **VALUEERROR**
* Null or missing input creates governed denial: **NO**
* Authority-collision subprecedence decided: **NO**
* Lockout semantics decided: **NO**
* Repairs performed or authorized: **NO**
* Schema changed: **NO**
* Python changed: **NO**
* Tests changed: **NO**
* Overall Stage 2 acceptance: **NO**
* Stage 2 completion: **NO**
* Advancement Gate changed: **NO**
* Stage 2: **HOLD**
* Stage 3: **UNENTERED AND UNAUTHORIZED**

The required-property contract and `FSM-SCHEMA-10` remain binding. Null/`None`
is permitted only for non-authority transitions and never becomes an authority
failure or governed denial. Missing-required and contextually invalid input is
rejected before governed FSM evaluation. No repair is performed.
