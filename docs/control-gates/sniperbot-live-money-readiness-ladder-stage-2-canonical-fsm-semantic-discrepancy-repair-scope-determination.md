# SniperBot Live-Money Readiness Ladder Stage 2 Canonical FSM Semantic-Discrepancy Repair-Scope Determination

## Status and Non-Authorization Boundary

DOCUMENTATION ONLY -- GOVERNANCE ONLY -- REPAIR-SCOPE DETERMINATION ONLY --
NOT A REPAIR -- NOT A FOUNDER SEMANTIC DECISION -- NOT A SCHEMA, API,
IMPLEMENTATION, OR TEST TASK ORDER -- NOT IMPLEMENTATION-EVIDENCE ACCEPTANCE --
NOT README INDEXING -- NOT OVERALL STAGE 2 ACCEPTANCE -- NOT STAGE 2
COMPLETION -- NOT AN ADVANCEMENT-GATE DECISION -- NOT STAGE 3 ENTRY --
NON-AUTHORIZATION BOUNDARY.

This artifact determines only the smallest valid governance and repair sequence
for the founder-selected Pure / Canonical FSM discrepancy cluster recorded by
the Stage 2 post-construction cross-file semantic-consistency review. It does
not resolve an unsettled semantic question, perform a repair, reopen an
implementation lane, change an acceptance, or authorize an operational action.

No integration, orchestration, runtime registration, deployment, market-data,
strategy, signal, risk, sizing, trade-card, broker, exchange, wallet, custody,
networking, persistence, routing, order, transaction, execution, or live-money
authority is created.

Stage 2 remains **HOLD**. Stage 3 remains **UNENTERED AND UNAUTHORIZED**.

## Authoritative Checkpoint

Repository: `heliosfi/Echoauth-core`

Authoritative starting checkpoint:
`8e7eda217a37c26855f9e2e1a0b63e11aaf36423`
(`docs: add sniperbot stage 2 cross-file semantic-consistency review`).

At determination start, local `HEAD`, local `origin/main`, and live
`refs/heads/main` resolved to that checkpoint; divergence was `0/0`; the
working tree was clean; no staged or untracked file existed; and no Git lock
file existed. The checkpoint commit created exactly
`docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-post-construction-cross-file-semantic-consistency-review.md`
and changed no existing file.

## Founder-Selected Canonical FSM Scope

The founder selected exactly one discrepancy cluster:

> Pure / Canonical FSM semantic inconsistencies and the missing
> authority-collision subprecedence link.

The selected subject is the existing pure, deterministic, immutable,
side-effect-free, non-persistent, network-free, non-authorizing, and
non-executing FSM transition-decision contract only. This determination may
identify future bounded governance, schema, evaluator, direct-test,
verification, acceptance, and indexing units. It authorizes none of them.

## Explicit Crypto Deferral Exclusion

Crypto Deferral / No-Action is not selected and is not analyzed by this
artifact. Its governance, schema, Python surface, evaluator, tests, acceptance,
and README entry remain unchanged. Its separately recorded inconsistencies and
missing link are neither resolved nor narrowed here.

This artifact cannot convert a later Canonical FSM repair into a composite
semantic-consistency PASS because the controlling review also recorded the
unselected Crypto Deferral lane as inconsistent.

## Three-Rule Protocol Preservation

This determination applies
`docs/control-gates/codex-three-rule-repo-protocol.md` without reinterpretation:

1. **Habitat Before Routine.** The founder-selected Canonical FSM cluster and
   one new documentation artifact define the complete habitat for this order.
2. **Silence Is Not Permission.** A recorded discrepancy does not authorize a
   semantic choice, repair, acceptance, index change, or adjacent lane.
3. **Stop Outside the Lane.** Any need to change an existing file, analyze
   Crypto Deferral, or perform operational work requires a stop and a separate
   exact founder order.

## Controlling Semantic-Failure Findings

The controlling cross-file review recorded these nine Canonical FSM findings:

1. Schema conditionals require valid authority or affirmative facts where the
   evaluator accepts absent or negative evidence and returns denial results.
2. The schema rejects null authority on arming and reset requests while Python
   accepts `None` and emits `AUTHORITY_MISSING` or
   `RESET_EVIDENCE_MISSING`.
3. Schema `$defs.RequiredAction` permits `null` although final governance and
   Python define exactly five non-null action values.
4. With `lockout_required = true`, the schema requires `allowed = false` while
   implementation and direct tests require `allowed = true`.
5. The lockout collision winner is consistent, but its `allowed` semantics
   differ between schema and implementation/tests.
6. Schema-to-Python parity fails for conditional denial inputs, nullable
   RequiredAction, and lockout `allowed`.
7. Contract-to-implementation parity fails because a forced lockout for a
   non-lockout request is neither allowed-to-requested nor denied-to-current
   under final `FSM-SCHEMA-06`.
8. The implementation-evidence acceptance claims satisfaction of the cited
   schema semantics without disclosing those differences.
9. Constructible multi-failure authority evidence has no founder-selected
   collision order, while `_authority_reason` silently selects one.

No finding is repaired by this determination.

## Final-Controlling-Artifact Hierarchy

The Canonical FSM semantic hierarchy is:

1. The founder decisions in the Canonical FSM re-gate record and the later
   schema-semantics founder-decision record control contract semantics.
2. The schema/interface proposal controls only where a later founder decision
   does not expressly resolve or narrow its proposal wording.
3. `schemas/sniperbot-fsm-transition-decision.schema.json` is an expression of
   governance; it does not override a founder decision.
4. `src/sniperbot/fsm/transition_contract.py` is the production evaluator; its
   behavior does not silently create governance.
5. `tests/test_sniperbot_fsm_transition_contract.py` records direct behavior
   evidence; a passing assertion does not make contrary behavior governing.
6. The FSM implementation-evidence decision record accepts only the evidence
   it accurately supports; it does not supersede the cited founder decisions.
7. The exact README entry is an index characterization, not a semantic source.
8. The post-construction semantic-consistency review controls the existence and
   classification of the current cross-file discrepancies, but expressly does
   not select replacement semantics.

Where the final founder records are conclusive, they control the later repair.
Where they are incomplete or internally unable to select one downstream
interpretation, a new founder decision is mandatory before repair.

## Finding-by-Finding Conflict Map

Only the required classification vocabulary is used below. Conditional repair
effects mean that a new founder decision must select which side changes; they
do not grant permission to change either side.

| Finding | Exact conflict and controlling sides | Governance determination | Required classifications | Smallest future repair unit and dependency |
| --- | --- | --- | --- | --- |
| 1 | Schema `allOf` conditionals require `ValidAuthorityEvidence`, true readiness, true confirmed-position, and both true close/cooldown facts. The evaluator instead returns the closed denial reasons for `None`/failing authority or false facts. `FSM-SCHEMA-01` through `04`, `10`, and `11` use requirement wording, while the closed denial reasons and mappings make the negative inputs meaningful. | Final governance says these conditions never allow a transition, but does not conclusively say whether a failing condition is a schema-invalid request or a valid denial-classification request. | `NEW FOUNDER DECISION REQUIRED`; `DOCUMENTATION REPAIR REQUIRED`; then `SCHEMA REPAIR REQUIRED` or `IMPLEMENTATION REPAIR REQUIRED` and `TEST REPAIR REQUIRED` as selected; `ACCEPTANCE REVALIDATION REQUIRED`. | Decide denial-input admissibility first; then align schema, evaluator/API boundary, and direct tests in a separately authorized parity lane. |
| 2 | JSON requires the `authority_evidence` property and conditionally rejects `null` for arming/reset. Python's dataclass default makes omission and explicit `None` identical and the evaluator emits missing-authority/reset denials. Final `FSM-SCHEMA-10` selects null only for non-authority transitions, but no final record selects the Python construction/evaluation rejection point or exception behavior. | The null prohibition on authority-required transitions is controlled; exact Python omission/null and rejection semantics are not. | `EXISTING GOVERNANCE CONTROLS`; `NEW FOUNDER DECISION REQUIRED`; `DOCUMENTATION REPAIR REQUIRED`; `IMPLEMENTATION REPAIR REQUIRED`; `TEST REPAIR REQUIRED`; `ACCEPTANCE REVALIDATION REQUIRED`. | After denial-input admissibility, decide omission, explicit `None`, enforcement location, and exception/result boundary; then repair only the selected surfaces. |
| 3 | Schema `RequiredAction` has type `string` or `null` and six enum entries including `null`. Final `FSM-SCHEMA-09`, Python `RequiredAction`, and `TransitionDecision` define exactly five non-null values. | Final governance conclusively selects five non-null values. No new semantic choice is required. | `EXISTING GOVERNANCE CONTROLS`; `SCHEMA REPAIR REQUIRED`; `TEST REPAIR REQUIRED`; `ACCEPTANCE REVALIDATION REQUIRED`. | One schema-only vocabulary correction followed by direct schema/API parity evidence. No Python public API or evaluator change is required for this finding. |
| 4 | The schema lockout conditional fixes `allowed = false`; `evaluate_transition` returns `allowed = true`; the direct lockout test asserts true. Both downstream forms return `LOCKOUT_REQUIRED` and `resulting_state = LOCKOUT`. | Existing governance selects the lockout winner but not the meaning of `allowed` for a forced safety override. | `NEW FOUNDER DECISION REQUIRED`; `DOCUMENTATION REPAIR REQUIRED`; later `SCHEMA REPAIR REQUIRED`, `IMPLEMENTATION REPAIR REQUIRED`, and/or `TEST REPAIR REQUIRED` as selected; `ACCEPTANCE REVALIDATION REQUIRED`. | Resolve the complete lockout tuple and its exception or conformance to `FSM-SCHEMA-06` before changing any downstream artifact. |
| 5 | Lockout wins over a requested non-lockout transition in both schema and evaluator, but the schema calls the result denied and Python calls it allowed. | `FSM-09` controls winner precedence. It does not control the winning decision's `allowed` meaning. | `EXISTING GOVERNANCE CONTROLS`; `NEW FOUNDER DECISION REQUIRED`; downstream classifications are the same as Finding 4. | No separate winner repair is needed. The unsettled flag/state semantics belong to the same lockout founder-decision dependency as Finding 4. |
| 6 | The schema/Python parity failure aggregates Findings 1 through 5: denial-input admissibility, authority nullability, RequiredAction nullability, and lockout mapping. | It creates no independent semantic question. It resolves only when each underlying component is governed and repaired. | `SCHEMA REPAIR REQUIRED`; `IMPLEMENTATION REPAIR REQUIRED`; `TEST REPAIR REQUIRED`; `ACCEPTANCE REVALIDATION REQUIRED`. | No standalone aggregate repair. Re-run exact schema/API parity after every component repair is complete. |
| 7 | For a non-lockout request forced to `LOCKOUT`, schema `allowed = false` plus `resulting_state = LOCKOUT` violates denied-to-current; Python `allowed = true` plus `resulting_state = LOCKOUT` violates allowed-to-requested. Final `FSM-SCHEMA-06` permits neither tuple. | Existing records do not state whether lockout is an exception to `FSM-SCHEMA-06` or must be represented differently. | `NEW FOUNDER DECISION REQUIRED`; `DOCUMENTATION REPAIR REQUIRED`; downstream classifications are the same as Findings 4 and 5. | The exact same lockout founder-decision lane must reconcile selection, flag meaning, resulting state, reason, action, and the general invariant. |
| 8 | The FSM implementation-evidence decision record cites the schema and all eleven schema-semantics decisions, then states contract satisfaction without disclosing Findings 1 through 7. | Passing tests do not cure the unsupported cross-file conformance claim. The existing record remains historical evidence but cannot serve as conclusive current acceptance after repair. | `DOCUMENTATION REPAIR REQUIRED`; `ACCEPTANCE REVALIDATION REQUIRED`; `README REINDEXING REQUIRED`. | After independent post-repair verification, create a separate superseding/revalidation acceptance disposition, then replace the canonical README characterization in a separate indexing lane. |
| 9 | `_authority_reason` returns the first of missing, stale, revoked, out-of-scope, and invalid failures, with later malformed-value fallbacks. Final founder records deny each individual failure but select no multi-failure order. | No existing founder record governs the collision winner. The returned reason and, for arming, sometimes the required action are externally observable. | `NEW FOUNDER DECISION REQUIRED`; `DOCUMENTATION REPAIR REQUIRED`; later `IMPLEMENTATION REPAIR REQUIRED` if the selected order differs; `TEST REPAIR REQUIRED`; possible `SCHEMA REPAIR REQUIRED` after denial-input admissibility; `ACCEPTANCE REVALIDATION REQUIRED`. | Decide denial-input admissibility, then select authority subprecedence, then implement only if needed and add exhaustive direct collision evidence. |

## Existing-Governance Versus New-Decision Analysis

### Existing Governance Controls

Existing final governance conclusively controls these portions:

* authority or prerequisite failure never becomes permission;
* `lockout_required` wins over every requested non-lockout transition;
* the winning state vocabulary value is `LOCKOUT` and the closed reason is
  `LOCKOUT_REQUIRED` in the committed schema/evaluator chain;
* `READY` to `ARMED_AUTO` remains founder-denied;
* allowed ordinary transitions result in the requested state and denied
  ordinary transitions retain current state under `FSM-SCHEMA-06`;
* RequiredAction has exactly five non-null values under `FSM-SCHEMA-09`;
* correlation references are preserved; and
* the FSM remains pure, descriptive, non-authorizing, and non-executing.

Those decisions are not reopened by this determination.

### New Founder Decisions Required

Four independent founder decisions remain mandatory:

1. **Denial-input admissibility.** Are false prerequisite facts and
   absent/stale/revoked/out-of-scope/invalid authority valid typed requests that
   produce governed denial decisions, or schema/API-invalid requests rejected
   before a decision? The answer must separately cover readiness, confirmed
   position, position closed, cooldown, arming authority, and reset authority.
2. **Null-authority enforcement.** Given final `FSM-SCHEMA-10`, how do JSON
   omission, JSON null, Python constructor omission, and explicit Python
   `None` behave for authority-required versus non-authority transitions; where
   is rejection enforced; and is it a `TypeError`, `ValueError`, or governed
   decision result? This determination selects none.
3. **Lockout override semantics.** When a non-lockout request collides with
   `lockout_required = true`, what do `allowed`, `requested_state`,
   `resulting_state`, `reason_code`, and required action mean, and is lockout an
   express exception to `FSM-SCHEMA-06` or represented in a way that satisfies
   it? This determination selects neither schema nor implementation behavior.
4. **Authority multi-failure subprecedence.** For every admitted combination of
   simultaneous authority failures, which failure reason and required action
   win for arming and reset? This determination does not select the current
   implementation order.

No one answer silently resolves another. In particular, denial-input
admissibility must be settled before collision subprecedence can define the
admitted state space.

## Authority-Collision Decision Dependency

### Exact Current Implementation Order

Within `_authority_reason`, the current observable order is:

1. `evidence is None` or `presence == "ABSENT"` -> `AUTHORITY_MISSING`;
2. `currentness == "STALE"` -> `AUTHORITY_STALE`;
3. `revocation == "REVOKED"` -> `AUTHORITY_REVOKED`;
4. `validity_outcome == "OUT_OF_SCOPE"` or empty `subject_scope` ->
   `AUTHORITY_OUT_OF_SCOPE`;
5. `validity_outcome != "VALID"` -> `AUTHORITY_INVALID`;
6. unsupported presence or currentness values -> `AUTHORITY_INVALID`;
7. empty `authority_reference` -> `AUTHORITY_INVALID`; and
8. otherwise -> no authority failure.

For `READY -> ARMED_MANUAL`, out-of-scope maps to `GOVERNANCE_REVIEW`; the
other current authority failures map to `FOUNDER_AUTHORITY_REQUIRED`. For
`LOCKOUT -> PAUSE`, missing is remapped to `RESET_EVIDENCE_MISSING`, all other
reasons remain their authority reason, and every failure maps to
`RESET_REQUIRED`. The order is therefore externally observable in reason codes
and, for some arming collisions, required actions.

### Exhaustive Constructible Multi-Failure Analysis

Inside the schema-declared enum domain, the four failure axes are:

* presence: `PRESENT` or failing `ABSENT`;
* currentness: `CURRENT` or failing `STALE`;
* revocation: `NON_REVOKED` or failing `REVOKED`; and
* validity: `VALID` or one of failing `INVALID`, `AMBIGUOUS`, or
  `OUT_OF_SCOPE`.

The cross-product contains 32 combinations: one fully valid combination, six
single-failure combinations, and 25 multi-failure combinations. All 25 are
exhaustively partitioned by the current implementation as follows:

| Exhaustive group | Number | Current winner |
| --- | ---: | --- |
| `ABSENT` plus at least one of stale, revoked, or non-valid validity | 15 | `AUTHORITY_MISSING` |
| `PRESENT`, `STALE`, plus at least one of revoked or non-valid validity | 7 | `AUTHORITY_STALE` |
| `PRESENT`, `CURRENT`, `REVOKED`, plus `INVALID`, `AMBIGUOUS`, or `OUT_OF_SCOPE` | 3 | `AUTHORITY_REVOKED` |
| **Total multi-failure combinations** | **25** | Current order only; not founder-selected |

No multi-failure combination reaches out-of-scope or invalid as winner because
every such collision also contains an earlier absence, stale, or revoked
failure. Empty scope/reference and unsupported raw strings are additionally
constructible through the Python dataclass but are outside the schema's closed
enum/minimum-length domain; the implementation orders empty scope before
general invalidity and empty reference last.

`FSM-12` and `FSM-SCHEMA-01` define individual failure as non-permission. They
do not rank collisions. Therefore a new founder decision is mandatory before
implementation or direct-test changes. The decision must state the complete
order, whether arming and reset share it, each winning reason/action mapping,
and whether schema representation is required or evaluator-owned under
`FSM-SCHEMA-11`.

Affected future evidence includes the schema/API parity record, direct tests
for all 25 closed-domain multi-failure combinations in both authority-using
transitions, any malformed-value boundary expressly retained, independent
collision reproduction, and the replacement acceptance disposition.

## Lockout-Semantics Decision Dependency

Lockout must be separated into these fields and meanings:

| Element | Existing control or conflict |
| --- | --- |
| Transition selection | `FSM-09` conclusively makes `lockout_required` win over a requested non-lockout transition. |
| Requested state | Both downstream artifacts echo the caller's non-lockout requested state. |
| Resulting state | Both downstream artifacts emit `LOCKOUT`. |
| `allowed` | Schema emits false; implementation and test emit true. No founder record defines the flag for a forced safety override. |
| Required action | Python emits `NONE`; the schema lockout conditional does not constrain the action; final mappings do not expressly settle a forced-override action. |
| Reason code | Both downstream artifacts emit `LOCKOUT_REQUIRED`. |
| Interaction with `FSM-SCHEMA-06` | Schema violates denied-to-current; implementation violates allowed-to-requested for every non-lockout request. |

The existing records do not conclusively select one complete interpretation.
The founder must define whether `allowed` describes the caller's requested
transition, the safety-selected lockout transition, or another expressly named
descriptive relation; whether lockout is an exception to `FSM-SCHEMA-06`; and
the exact complete output tuple for a non-lockout collision. No schema or
implementation interpretation may be chosen silently.

This one semantic decision controls Findings 4, 5, and 7. It must precede any
schema, evaluator, or direct-test repair for lockout. The repair must not change
the already-controlled absolute winner unless a separate founder order
expressly reopens `FSM-09`, which this determination does not recommend or
authorize.

## Request-Condition and Denial-Input Analysis

The exact current mismatches are:

| Request condition | Schema treatment | Evaluator treatment |
| --- | --- | --- |
| `PAUSE -> READY` with readiness false | Envelope invalid because the conditional requires true. | Denied, current state retained, `READINESS_FACTS_MISSING`, `GOVERNANCE_REVIEW`. |
| `ARMED_AUTO -> IN_TRADE` with confirmed position false | Envelope invalid because the conditional requires true. | Denied, current state retained, `CONFIRMED_POSITION_FACT_MISSING`, `GOVERNANCE_REVIEW`. |
| `IN_TRADE -> PAUSE` with position-closed false | Envelope invalid because both close and cooldown must be true. | Denied first with `POSITION_CLOSED_FACT_MISSING`, `GOVERNANCE_REVIEW`. |
| `IN_TRADE -> PAUSE` with closed true and cooldown false | Envelope invalid because cooldown must be true. | Denied with `COOLDOWN_FACT_MISSING`, `GOVERNANCE_REVIEW`. |
| `READY -> ARMED_MANUAL` with missing or failing authority | Envelope invalid because `ValidAuthorityEvidence` is required. | Denied with the current authority reason and mapped action. |
| `LOCKOUT -> PAUSE` with missing or failing authority | Envelope invalid because `ValidAuthorityEvidence` is required. | Denied with reset-missing or the current authority reason and `RESET_REQUIRED`. |

Final governance clearly prevents allowance when these conditions fail. It is
not conclusive on whether failure belongs to input validation or deterministic
decision classification. That distinction affects JSON Schema, Python public
API behavior, evaluator behavior, exception boundaries, reason reachability,
direct tests, parity evidence, and acceptance. A new founder decision must
settle it before a repair side is selected.

## Null-Authority Analysis

The JSON request requires the `authority_evidence` property for every request.
Its base shape permits an AuthorityEvidence object or `null`, while final
conditional rules reject `null` on the two authority-required transitions and
allow it on non-authority transitions.

The Python `TransitionRequest.authority_evidence` annotation is
`AuthorityEvidence | None` with default `None`. Constructor omission and
explicit `None` are therefore indistinguishable and reach the evaluator for
every transition. On arming, they emit `AUTHORITY_MISSING`; on reset, they emit
`RESET_EVIDENCE_MISSING`; on non-authority transitions they are ignored.

Final `FSM-SCHEMA-10` controls that null is permitted only for non-authority
transitions, but it does not specify:

* whether Python omission and explicit `None` must be distinguishable;
* whether the dataclass default remains part of the public API;
* whether rejection occurs at construction or evaluation;
* the exact `TypeError`, `ValueError`, or decision-result boundary; or
* whether missing-authority reason codes remain reachable through another
  admitted representation.

Those points require a bounded founder decision. The later repair may affect
the Python public API, evaluator behavior, and direct tests. The schema changes
only if the founder expressly supersedes the current null rule; this artifact
does not do so.

## RequiredAction-Nullability Analysis

No new founder decision is required. Final `FSM-SCHEMA-09` says the set is
exactly `NONE`, `HUMAN_REVIEW`, `GOVERNANCE_REVIEW`,
`FOUNDER_AUTHORITY_REQUIRED`, and `RESET_REQUIRED`. Python already defines
exactly those five non-null enum values and its decision annotation is
non-optional.

The smallest repair is confined to schema `$defs.RequiredAction`: remove null
from its type and enum. A later separately authorized direct-test or parity
unit must prove the schema rejects null and exactly matches the Python enum.
No Python public API or evaluator behavior changes for this finding.

## Acceptance and README Impact Analysis

The existing FSM implementation-evidence decision record is a historical
acceptance at commit `80ad01b2730182bfcc1242c4302be35f1c01c83b`. It cites the
schema and final founder semantics and states that the evaluator satisfies the
bounded contract, but it does not disclose the current discrepancies. It must
not be amended during a semantic repair and must not be treated as conclusive
post-repair acceptance.

After every governed repair and independent verification passes, a separate
acceptance revalidation/supersession artifact is required. It must cite the
full repair provenance, disclose the old acceptance disposition, and accept or
hold the repaired chain based on independently reproduced evidence.

The current README entry accurately describes the historical acceptance and
does not itself assert the disputed lockout tuple. No README change is needed
before revalidation. After a new acceptance exists, a separate README-only
indexing order must replace the canonical acceptance characterization so the
lane retains one current canonical acceptance entry. Indexing cannot precede
acceptance and cannot add semantic or operational authority.

## Exact Files Potentially Affected by Later Repair

This list identifies potential later scope; it authorizes no change.

Existing files that one or more future bounded repair lanes may need to change:

1. `schemas/sniperbot-fsm-transition-decision.schema.json`
2. `src/sniperbot/fsm/transition_contract.py`
3. `tests/test_sniperbot_fsm_transition_contract.py`
4. `docs/control-gates/README.md` -- only in the final separate indexing lane

Proposed new governance/evidence paths, each requiring a separate exact founder
authorization before creation:

1. `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-canonical-fsm-denial-input-classification-founder-decision-record.md`
2. `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-canonical-fsm-null-authority-enforcement-founder-decision-record.md`
3. `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-canonical-fsm-authority-collision-subprecedence-founder-decision-record.md`
4. `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-canonical-fsm-lockout-semantics-founder-decision-record.md`
5. `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-canonical-fsm-semantic-repair-implementation-evidence-acceptance.md`
6. `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-canonical-fsm-post-repair-semantic-consistency-review.md`

The names identify independent subjects; they do not authorize combining them.
A later founder may select only one bounded lane at a time.

## Files Proven Not to Require Change

The following existing files need not be modified to preserve history and the
selected scope:

* `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-canonical-fsm-contract-definition-review.md`;
* `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-canonical-fsm-re-gate-founder-decision-record.md`;
* `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-canonical-fsm-schema-interface-proposal.md`;
* `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-canonical-fsm-schema-semantics-founder-decision-record.md`;
* `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-fsm-implementation-evidence-decision-record.md` -- preserved as historical acceptance and superseded only by a new record;
* `src/sniperbot/__init__.py`;
* `src/sniperbot/fsm/__init__.py`; and
* every Crypto Deferral / No-Action artifact and every other evaluator lane's
  governance, schema, source, test, acceptance, and index content.

The controlling post-construction semantic-consistency review also remains
unchanged as the historical finding source.

## Repair Dependency Graph

```text
Denial-input founder decision
    -> null-authority founder decision
        -> authority-collision founder decision
            -> request/null/authority parity repair and evidence

Lockout-semantics founder decision
    -> lockout schema/evaluator/direct-test repair and evidence

Existing FSM-SCHEMA-09
    -> RequiredAction schema-only repair and parity evidence

All governed repair units
    -> independent implementation-evidence revalidation
        -> new acceptance disposition
            -> canonical README reindexing
                -> Canonical FSM post-repair semantic re-review
```

The lockout and RequiredAction branches are semantically independent of
authority admissibility. Publication order may place already-governed
RequiredAction repair after the founder decisions, but no combined commit is
authorized merely because files overlap.

## Smallest Bounded Repair-Lane Sequence

Every numbered lane below requires its own founder authorization and must stop
at its stated boundary:

1. **Denial-input classification founder decision.** Create only its decision
   record; decide valid denial input versus invalid request for each condition.
2. **Null-authority enforcement founder decision.** Create only its decision
   record; settle omission, null, enforcement point, and exception/result
   behavior without silently following lane 1.
3. **Authority-collision subprecedence founder decision.** Create only its
   decision record after the admitted authority state space is known; select
   the complete order and mappings without implementation.
4. **Lockout-semantics founder decision.** Create only its decision record;
   settle the complete forced-lockout tuple and `FSM-SCHEMA-06` interaction.
5. **RequiredAction schema repair.** Modify only the FSM schema and, if the
   exact order expressly authorizes evidence in the same bounded unit, its
   direct schema parity test; make no evaluator change.
6. **Request conditional and denial-input parity repair.** Modify only the
   exact schema, evaluator/API, and direct-test surfaces selected by lane 1.
7. **Null-authority parity repair.** Modify only the exact Python public API,
   evaluator, schema if expressly superseded, and tests selected by lane 2.
8. **Authority-subprecedence implementation and direct-test evidence.** Change
   `_authority_reason` only if lane 3 differs from current order; in all cases
   add independent direct evidence for the governed admitted collision space.
9. **Lockout semantic repair.** Align schema, evaluator, and direct tests to the
   complete tuple selected in lane 4 without changing lockout's existing
   absolute precedence unless separately authorized.
10. **Independent implementation-evidence revalidation.** Read-only review of
    the complete governance/schema/API/implementation/test chain; no repair.
11. **Acceptance disposition.** Create one new acceptance or hold artifact only
    if lane 10 is conclusive; preserve the historical acceptance unchanged.
12. **README reindexing.** Modify only README after a published acceptance;
    retain one current canonical acceptance characterization.
13. **Post-repair semantic re-review.** Create a new Canonical FSM-only
    semantic review; do not alter the controlling historical composite review
    and do not analyze or repair Crypto Deferral.

This decomposition keeps independent founder choices separate and prevents a
schema-only correction from silently selecting lockout or authority behavior.

## Required Independent Verification Sequence

After all authorized repair commits are published, independent verification
must, at minimum:

1. verify exact commit provenance, commit scope, clean synchronization, and
   unchanged out-of-scope files;
2. validate JSON parsing and Draft 2020-12 structural validity;
3. verify exact schema-to-founder-decision and schema-to-Python parity;
4. verify all closed state, transition, reason, and five-value RequiredAction
   vocabularies, including schema rejection of null action;
5. verify every admitted negative-fact and authority-denial input has the exact
   selected validation, exception, or decision outcome;
6. verify Python omission and explicit `None` behavior for authority-required
   and non-authority transitions;
7. independently reproduce every selected authority single-failure and all 25
   closed-domain multi-failure collision outcomes for both arming and reset;
8. verify every non-lockout lockout collision's selected `allowed`, current,
   requested, resulting, reason, action, and reference tuple plus its invariant;
9. verify determinism, totality inside the governed typed domain, immutability,
   reference preservation, purity, and non-mutation;
10. verify production import restrictions and the absence of persistence,
    networking, runtime, broker, order, transaction, execution, or other
    prohibited capabilities;
11. run focused FSM tests, Contract Validation, combined Contract and Authority
    Clarity, the Explicit Authority Clarity Validator, and the canonical suite;
    and
12. run exact scope, final-newline, whitespace, and `git diff --check` checks.

Passing implementation-authored tests alone is insufficient. Collision and
schema/API parity evidence must be independently reproduced from the founder
records rather than copied from implementation helpers.

## Required Acceptance Disposition

Acceptance is blocked until all selected repairs and independent verification
are complete. The later disposition must be one of:

* a new bounded acceptance that expressly supersedes the old acceptance for
  current implementation-evidence purposes and records complete provenance; or
* a HOLD artifact identifying the exact remaining discrepancy.

The disposition must not delete, rewrite, or amend the historical acceptance.
It must not infer overall Stage 2 acceptance, Stage 2 completion, Advancement
Gate movement, or Stage 3 authority.

## Required Post-Repair Semantic Re-Review

After acceptance disposition and canonical indexing, a new read-only Canonical
FSM semantic-consistency review must compare the final founder decisions,
schema, Python API/evaluator, direct tests, independent evidence, acceptance,
and README entry. It must use the same semantic dimensions and required
determination vocabulary as the controlling cross-file review.

That review may determine only whether the Canonical FSM chain is repaired. It
cannot change the historical composite FAIL or declare a new composite PASS
without a separately founder-selected review that includes every still-failing
lane. Crypto Deferral remains outside this sequence.

## Explicit Exclusions

This determination does not:

* repair or modify any governance record, schema, source, test, acceptance, or
  README entry;
* select denial-input, null-authority, authority-collision, or lockout
  semantics;
* create a schema/API contract, implementation instruction, test instruction,
  acceptance, or index entry;
* reopen another evaluator lane or analyze Crypto Deferral;
* determine overall Stage 2 acceptance or completion;
* update or replace the Advancement Gate decision;
* enter or authorize Stage 3; or
* authorize integration, orchestration, runtime, deployment, market data,
  strategy, signals, risk, sizing, broker, exchange, wallet, custody,
  networking, persistence, routing, orders, transactions, execution, or
  live-money behavior.

## Stage 2 HOLD Preservation

Stage 2 remains **HOLD**. This artifact neither changes the historical
Advancement Gate nor certifies Stage 2 completion. A future Canonical FSM
repair, even if accepted, would not by itself resolve the unselected Crypto
Deferral inconsistency or authorize Stage 2 advancement.

## Stage 3 Non-Authorization Preservation

Stage 3 remains **UNENTERED AND UNAUTHORIZED**. No repair lane, acceptance,
integration, runtime behavior, deployment, execution, or live-money capability
is authorized by this determination.

## Refusal and Halt Conditions

Refuse and halt if a later order attempts to:

* repair before the applicable founder decision is published;
* treat current implementation order as founder-selected authority
  subprecedence;
* choose schema or implementation lockout behavior without the complete
  lockout decision;
* combine independent lanes merely because they touch the same file;
* change any file not expressly named by that later bounded order;
* amend the historical acceptance instead of publishing a separate
  disposition;
* index before acceptance is published;
* analyze or repair Crypto Deferral under the Canonical FSM selection;
* infer overall Stage 2 acceptance, completion, or Advancement Gate movement;
  or
* authorize Stage 3 or any operational capability.

Any ambiguous founder answer, parity failure, validation failure, unexpected
file change, dirty repository state, divergence, Git lock, prohibited import,
or prohibited capability requires a stop and discrepancy report.

## Final Determination

The Pure / Canonical FSM discrepancy cluster is not repair-ready under existing
governance alone.

Four independent founder decisions are required before the affected repair
surfaces can be selected: denial-input admissibility, null-authority
enforcement, authority multi-failure subprecedence, and complete lockout
override semantics. RequiredAction nullability is already conclusively
controlled by final `FSM-SCHEMA-09` and needs only a bounded schema correction
and direct parity evidence.

The smallest valid sequence is founder decisions, separately bounded repair
units, independent implementation-evidence revalidation, a new acceptance
disposition, README reindexing, and a Canonical FSM-only post-repair semantic
review. No repair is performed. Crypto Deferral is not analyzed. Overall Stage
2 acceptance is not created, Stage 2 completion is not certified, the
Advancement Gate is unchanged, Stage 2 remains **HOLD**, and Stage 3 remains
**UNENTERED AND UNAUTHORIZED**.
