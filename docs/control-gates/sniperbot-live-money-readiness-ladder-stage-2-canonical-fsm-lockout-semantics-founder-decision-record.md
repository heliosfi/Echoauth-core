# SniperBot Live-Money Readiness Ladder Stage 2 Canonical FSM Lockout Semantics Founder Decision Record

## Status and Non-Authorization Boundary

DOCUMENTATION ONLY -- GOVERNANCE ONLY -- LOCKOUT-SEMANTICS FOUNDER DECISION
ONLY -- NOT A SCHEMA, API, IMPLEMENTATION, OR TEST REPAIR -- NOT
IMPLEMENTATION-EVIDENCE ACCEPTANCE -- NOT README INDEXING -- NOT OVERALL
STAGE 2 ACCEPTANCE -- NOT STAGE 2 COMPLETION -- NOT AN ADVANCEMENT-GATE
DECISION -- NOT STAGE 3 ENTRY -- NON-AUTHORIZATION BOUNDARY.

This record resolves only the fourth and final founder-semantic dependency in
the founder-selected Canonical FSM semantic-discrepancy repair sequence. It
defines fail-closed lockout behavior, the complete forced-lockout decision
tuple, the only governed exit from `State.LOCKOUT`, and the interaction with
`FSM-SCHEMA-06`.

No schema, Python, test, README, acceptance, integration, orchestration,
runtime registration, deployment, market-data, strategy, signal, risk,
sizing, trade-card, broker, exchange, wallet, custody, networking,
persistence, routing, order, transaction, execution, or live-money authority
is created.

Stage 2 remains **HOLD**. Stage 3 remains **UNENTERED AND UNAUTHORIZED**.

## Authoritative Checkpoint

Repository: `heliosfi/Echoauth-core`

Authoritative starting checkpoint:
`00103e5f78403aa4cb6d390e383cf8f6ad4af64d`
(`docs: record sniperbot fsm authority collision subprecedence decision`).

At record creation, local `HEAD`, local `origin/main`, and live
`refs/heads/main` resolved to that checkpoint; divergence was `0/0`; the
working tree was clean; no staged or untracked file existed; and no Git lock
file existed.

The three prerequisite founder-semantic records were present and tracked:

1. Canonical FSM denial-input classification;
2. Canonical FSM null-authority enforcement; and
3. Canonical FSM authority-collision subprecedence.

## Founder-Selected Subject

The subject is exactly the existing pure, deterministic, immutable,
side-effect-free, non-persistent, network-free, non-authorizing, and
non-executing Canonical FSM transition-decision contract.

The selected decision is lockout semantics only. The record does not reopen
the preceding denial-input, null-authority, or authority-collision decisions,
and it does not repair any downstream artifact.

## Three-Rule Protocol Preservation

This record applies
`docs/control-gates/codex-three-rule-repo-protocol.md` without
reinterpretation:

1. **Habitat Before Routine.** The Canonical FSM lockout-semantic dependency
   and this one new record define the complete habitat.
2. **Silence Is Not Permission.** Resolving the semantic dependency does not
   authorize schema, Python, test, evidence, acceptance, index, or operational
   work.
3. **Stop Outside the Lane.** Any change beyond this one record requires a
   separate exact founder order.

## Controlling Records and Conflict Review

This decision was compared with the binding Canonical FSM governance, schema,
API, evaluator, tests, and repair-scope record. The relevant controls are:

* `FSM-09`: an externally determined `lockout_required` fact has precedence
  over every requested non-lockout transition;
* `FSM-11`: `LOCKOUT -> PAUSE` may be considered only with valid bounded reset
  evidence and required externally supplied reset facts;
* `FSM-12`: absent, stale, ambiguous, contradictory, out-of-scope, or revoked
  authority evidence is not permission;
* `FSM-SCHEMA-05`: ordinary locked, undefined, and denied requests retain the
  current state without mutation;
* `FSM-SCHEMA-06`: ordinary allowed decisions result in the requested state
  and ordinary denied decisions retain the current state;
* `FSM-SCHEMA-08`: the decision preserves the exact request correlation
  reference;
* `FSM-SCHEMA-09`: `RequiredAction` remains the closed five-value set;
* `FSM-SCHEMA-10`: null authority is permitted only for transitions that do
  not require authority; and
* `FSM-SCHEMA-11`: schema and pure-evaluator enforcement remain divided by
  representability.

The committed schema and evaluator already agree that a winning
`lockout_required` branch produces `State.LOCKOUT` with
`ReasonCode.LOCKOUT_REQUIRED`, but disagree on `allowed`. They also do not
share a binding required-action constraint for the forced override. The
repair-scope determination expressly reserved those choices for this founder
decision.

No binding conflict prevents this record. The bounded safety exception to
`FSM-SCHEMA-06` and the clarified `RESET_REQUIRED` mapping below are express
later founder decisions. They do not enlarge either closed vocabulary.

## Founder Decision Summary

The founder selects all of the following:

1. Lockout is a hard, fail-closed safety state.
2. Active lockout cannot be bypassed by arming authority, founder authority,
   authority-collision outcomes, or successful ordinary prerequisites.
3. While the current state is `State.LOCKOUT`, only the exact governed
   `TransitionRequestName.LOCKOUT_TO_PAUSE` reset path may exit lockout.
4. No direct transition from lockout to `State.READY`,
   `State.ARMED_MANUAL`, `State.ARMED_AUTO`, `State.IN_TRADE`, or any other
   state is permitted.
5. No automatic, time-based, implicit, evidence-free, inferred, or fallback
   unlock is permitted.
6. Invalid boundary input is rejected before governed FSM evaluation and is
   never converted into lockout, reset, or authority-denial output.
7. For a well-formed ordinary request while locked out, lockout wins over
   ordinary arming, prerequisite, and authority-denial reporting unless the
   request is the exact governed reset path.
8. The published reset authority-collision order and every published
   reason/action mapping remain unchanged.
9. Lockout is not an authority-collision participant and does not modify the
   published arming or reset authority-failure ordering.

## Exact Identifier Set

This record uses only existing contract identifiers:

* state identifiers: `State.LOCKOUT` and `State.PAUSE`;
* reset transition identifier:
  `TransitionRequestName.LOCKOUT_TO_PAUSE`;
* reason identifiers: `ReasonCode.LOCKOUT_REQUIRED`,
  `ReasonCode.RESET_EVIDENCE_MISSING`, `ReasonCode.AUTHORITY_STALE`,
  `ReasonCode.AUTHORITY_REVOKED`, `ReasonCode.AUTHORITY_OUT_OF_SCOPE`,
  `ReasonCode.AUTHORITY_INVALID`, `ReasonCode.RESET_FACTS_MISSING`, and
  `ReasonCode.ALLOWED`; and
* action identifiers: `RequiredAction.RESET_REQUIRED` and
  `RequiredAction.NONE`.

No replacement, composite, alias, or additional identifier is created.

## Input Boundary Before Lockout Evaluation

The existing boundary order is preserved:

1. structural and runtime-type validation;
2. transition-specific null-authority applicability validation; and only then
3. governed FSM evaluation, including lockout precedence.

Structurally malformed, wrong-type, missing-required, and contextually invalid
null inputs are boundary errors. They do not produce a governed lockout
decision, do not enter authority-collision handling, and do not select a state
transition.

Python explicit `None` and JSON null retain the previously decided
null-authority boundary. Omission retains the previously decided required-
argument and required-property behavior. This record introduces no default,
sentinel, coercion, or signature change.

## Global Lockout Precedence

After boundary validation, a true
`ExternalFacts.lockout_required` (`"lockout_required": true`) is the outer
governed safety winner. It is evaluated before:

* ordinary transition precedence;
* ordinary prerequisite failure reporting;
* arming authority evaluation;
* authority-collision subprecedence;
* reset-facts evaluation; and
* any ordinary allowed transition.

If `lockout_required` is true on a reset request, the active external lockout
condition wins and the reset does not exit `State.LOCKOUT`.

The existing ambiguity/contradiction rule remains governed and is not
redefined here. This record settles only lockout's position relative to
ordinary transition, prerequisite, authority, collision, and reset branches.

## Complete Forced-Lockout Decision Tuple

For every well-formed request where `external_facts.lockout_required` is true,
the complete decision tuple is:

| Decision field | Founder-selected value |
| --- | --- |
| `current_state` | Exact request `current_state` |
| `requested_state` | Exact request `requested_state` |
| `allowed` | `false` |
| `resulting_state` | `State.LOCKOUT` |
| `reason_code` | `ReasonCode.LOCKOUT_REQUIRED` |
| `required_next_human_or_governance_action` | `RequiredAction.RESET_REQUIRED` |
| `correlation_reference` | Exact request `correlation_reference` |

`allowed = false` describes the caller-requested transition: that transition
is not allowed to proceed. `resulting_state = State.LOCKOUT` describes the
independently forced fail-closed safety result. The decision is descriptive
only; it performs no mutation, command, persistence, or execution.

`RequiredAction.RESET_REQUIRED` means only that leaving lockout requires the
separately governed reset path. It is not permission to reset, does not supply
reset evidence or facts, and does not authorize an operational action.

## Bounded FSM-SCHEMA-06 Safety Exception

The forced-lockout tuple is an express, narrowly bounded safety exception to
`FSM-SCHEMA-06`:

* the caller-requested transition is denied; and
* the descriptive resulting state is nevertheless `State.LOCKOUT`, even when
  the request's current state is not `State.LOCKOUT`.

This exception exists only for the winning `lockout_required == true` safety
branch. It does not change `FSM-SCHEMA-06` for ordinary allowed or denied
transitions. When the current state is already `State.LOCKOUT`, the same tuple
also retains the current state and therefore conforms to the ordinary denied-
to-current relation.

## Locked-State Gate and Sole Permitted Exit

When the request is well formed, `lockout_required` is false, and
`current_state == State.LOCKOUT`, the FSM applies a locked-state gate before
ordinary transition evaluation.

The only request eligible to leave lockout is the exact reset subject:

* `current_state = State.LOCKOUT`;
* `requested_state = State.PAUSE`; and
* `transition_request = TransitionRequestName.LOCKOUT_TO_PAUSE`.

Every other transition request while currently locked out is denied with:

| Decision field | Founder-selected value |
| --- | --- |
| `current_state` | `State.LOCKOUT` |
| `requested_state` | Exact request `requested_state` |
| `allowed` | `false` |
| `resulting_state` | `State.LOCKOUT` |
| `reason_code` | `ReasonCode.LOCKOUT_REQUIRED` |
| `required_next_human_or_governance_action` | `RequiredAction.RESET_REQUIRED` |
| `correlation_reference` | Exact request `correlation_reference` |

This locked-state denial wins over ordinary arming/prerequisite authority-
denial reporting. Authority evidence supplied on a non-reset locked-state
request cannot bypass lockout and is not evaluated as a collision.

## Exact Reset Authority Subprecedence and Mappings

For the exact `LOCKOUT_TO_PAUSE` reset path, after boundary validation and
only when no active `lockout_required` condition wins, reset authority is
evaluated using the published first-applicable-failure order:

| Order | First applicable reset-authority condition | Winning reason | Winning action | Allowed | Resulting state |
| ---: | --- | --- | --- | --- | --- |
| 1 | `AuthorityEvidence.presence == "ABSENT"` | `ReasonCode.RESET_EVIDENCE_MISSING` | `RequiredAction.RESET_REQUIRED` | `false` | `State.LOCKOUT` |
| 2 | `AuthorityEvidence.currentness == "STALE"` | `ReasonCode.AUTHORITY_STALE` | `RequiredAction.RESET_REQUIRED` | `false` | `State.LOCKOUT` |
| 3 | `AuthorityEvidence.revocation == "REVOKED"` | `ReasonCode.AUTHORITY_REVOKED` | `RequiredAction.RESET_REQUIRED` | `false` | `State.LOCKOUT` |
| 4 | `AuthorityEvidence.validity_outcome == "OUT_OF_SCOPE"` | `ReasonCode.AUTHORITY_OUT_OF_SCOPE` | `RequiredAction.RESET_REQUIRED` | `false` | `State.LOCKOUT` |
| 5 | `AuthorityEvidence.validity_outcome == "INVALID"` or `"AMBIGUOUS"` | `ReasonCode.AUTHORITY_INVALID` | `RequiredAction.RESET_REQUIRED` | `false` | `State.LOCKOUT` |

First applicable failure wins. Input/property order does not affect the result.
No composite reason or action is permitted. Null, omission, malformed input,
wrong types, and lockout itself are not collision participants.

Every denied reset decision preserves the exact current state, requested
state, and correlation reference supplied by the well-formed request.

## Reset Facts and Successful Reset Mapping

If reset authority is fully valid but
`ExternalFacts.reset_facts_explicit == false`, the exact mapping is:

* `allowed = false`;
* `resulting_state = State.LOCKOUT`;
* `reason_code = ReasonCode.RESET_FACTS_MISSING`; and
* `required_next_human_or_governance_action = RequiredAction.RESET_REQUIRED`.

Only fully valid reset authority plus
`ExternalFacts.reset_facts_explicit == true`, with no active
`lockout_required` condition and no earlier governed failure, permits the
existing transition:

* `allowed = true`;
* `resulting_state = State.PAUSE`;
* `reason_code = ReasonCode.ALLOWED`; and
* `required_next_human_or_governance_action = RequiredAction.NONE`.

The successful reset permits only the descriptive existing transition to
`State.PAUSE`. It does not permit a direct transition to `State.READY`,
`State.ARMED_MANUAL`, `State.ARMED_AUTO`, `State.IN_TRADE`, or any other
operational state.

## Deterministic Lockout Precedence

The governed lockout-related evaluation order is:

1. reject structurally malformed, wrong-type, missing-required, and
   contextually invalid null input at the boundary;
2. apply the winning external `lockout_required` safety branch;
3. preserve any already-governed higher-priority ambiguity/contradiction
   handling not reopened by this record;
4. if currently locked out, classify the request as the exact reset path or a
   locked-state denial;
5. on the exact reset path, apply the published reset authority-collision
   subprecedence;
6. if authority succeeds, require explicit reset facts;
7. if both reset evidence and reset facts succeed, permit only
   `LOCKOUT_TO_PAUSE`; and
8. only outside the locked-state gate may ordinary transition evaluation
   proceed.

This order is deterministic and independent of JSON property order or Python
construction order.

## No Automatic or Implicit Unlock

No passage of time, timeout, cooldown, retry, evidence refresh, callback,
successful unrelated prerequisite, new authority claim, founder-authority
claim, inferred fact, missing fact, or absence of a repeated lockout signal may
leave `State.LOCKOUT`.

The FSM does not fetch, refresh, calculate, discover, verify through external
calls, or persist reset evidence or facts. All accepted inputs remain bounded,
caller-supplied descriptions of already-determined facts.

## Collision-Order Preservation

The authority-collision founder decision remains unchanged:

* arming order: `ABSENT`, `STALE`, `REVOKED`, `OUT_OF_SCOPE`, then `INVALID`
  or `AMBIGUOUS`;
* reset order: `ABSENT`, `STALE`, `REVOKED`, `OUT_OF_SCOPE`, then `INVALID`
  or `AMBIGUOUS`; and
* the reset missing-authority branch remains remapped to
  `ReasonCode.RESET_EVIDENCE_MISSING` with
  `RequiredAction.RESET_REQUIRED`.

Lockout is an outer safety state and condition, not an additional authority
failure. It is never inserted into either collision order and never changes a
single-failure mapping.

## Schema, Python, and Test Implications -- Not Authorized

A future separately authorized lockout semantic repair must align:

* `schemas/sniperbot-fsm-transition-decision.schema.json`;
* `src/sniperbot/fsm/transition_contract.py`; and
* `tests/test_sniperbot_fsm_transition_contract.py`.

That repair must implement and directly prove the complete forced-lockout
tuple, the bounded `FSM-SCHEMA-06` exception, the locked-state gate, the sole
reset exit, reset subprecedence preservation, reference preservation,
determinism, purity, non-mutation, and prohibited-capability absence.

This record does not modify or authorize modification of any of those files.

## Remaining Canonical FSM Repair Sequence

All four founder-semantic dependencies are now decided. The controlling repair
sequence remains separately bounded:

1. `RequiredAction` schema repair and direct parity evidence;
2. request-conditional and denial-input parity repair;
3. null-authority parity repair;
4. authority-subprecedence implementation and direct-test evidence;
5. lockout semantic repair;
6. independent implementation-evidence revalidation;
7. a new acceptance disposition, if revalidation is conclusive;
8. canonical README reindexing after published acceptance; and
9. Canonical FSM-only post-repair semantic re-review.

Each unit requires a separate exact founder authorization. This record does
not combine, reorder, or authorize any repair unit.

## Explicitly Deferred and Prohibited Scope

This record does not:

* repair schema, Python, or tests;
* create direct or independent evidence;
* create an acceptance artifact;
* modify README indexing;
* certify Stage 2 completion;
* alter the Advancement Gate;
* analyze or repair Crypto Deferral / No-Action;
* begin another Stage 2 lane;
* authorize integration, orchestration, runtime, deployment, or an external
  connection; or
* enter or authorize Stage 3.

No market-data, strategy, signal, risk, sizing, trade-card, broker, exchange,
wallet, custody, networking, persistence, routing, order, transaction,
execution, or live-money capability is created.

## Validation and Stop Conditions

Publication requires:

* exactly this one new file and no existing-file modification;
* documentation/content guards;
* Contract Validation;
* Contract and Authority Clarity;
* Explicit Authority Clarity Validator;
* the canonical suite;
* whitespace, final-newline, scope, and `git diff --check`; and
* clean synchronized post-publication state with divergence `0/0`.

Any binding conflict, ambiguous identifier, validation failure, unexpected
file change, dirty tree, divergence, Git lock, or prohibited capability
requires a stop and discrepancy report.

## Final Determination

* Lockout semantics: **FOUNDER DECIDED**
* Lockout state: **HARD AND FAIL-CLOSED**
* Boundary errors evaluated before governed FSM: **YES**
* `lockout_required` outer safety precedence preserved: **YES**
* Forced-lockout `allowed`: **FALSE**
* Forced-lockout resulting state: **LOCKOUT**
* Forced-lockout reason: **LOCKOUT_REQUIRED**
* Forced-lockout action: **RESET_REQUIRED**
* Forced-lockout exception to `FSM-SCHEMA-06`: **YES, BOUNDED**
* Only permitted lockout exit: **LOCKOUT_TO_PAUSE**
* Successful reset resulting state: **PAUSE ONLY**
* Automatic, implicit, time-based, or evidence-free unlock: **PROHIBITED**
* Reset collision order changed: **NO**
* Arming collision order changed: **NO**
* Composite reasons or actions permitted: **NO**
* Schema changed: **NO**
* Python changed: **NO**
* Tests changed: **NO**
* README changed: **NO**
* Acceptance created: **NO**
* Stage 2 completion: **NO**
* Advancement Gate changed: **NO**
* Stage 2: **HOLD**
* Stage 3: **UNENTERED AND UNAUTHORIZED**

The complete lockout policy is now founder-governed. Lockout remains an outer,
fail-closed safety condition; only the exact governed reset path can produce a
descriptive exit to `State.PAUSE`; and all downstream repairs remain deferred
to separate exact founder authorizations.
