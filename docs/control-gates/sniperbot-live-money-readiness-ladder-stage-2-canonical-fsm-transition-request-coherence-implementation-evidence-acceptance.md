# SniperBot Stage 2 Canonical FSM Transition-Request Coherence Implementation-Evidence Acceptance

## Acceptance Status and Boundary

`ACCEPT BOUNDED CANONICAL FSM TRANSITION-REQUEST COHERENCE IMPLEMENTATION EVIDENCE`

Repository: `heliosfi/Echoauth-core`

Implementation and independent-revalidation checkpoint:
`fe278f6491e328951bc0e1a07f77548eec5c9e7f`.

The separate founder-authorized read-only implementation-evidence
revalidation returned **PASS** with no substantive discrepancies. This
acceptance covers only the Canonical FSM transition-request coherence repair:
the closed relationship between the nine `TransitionRequestName` identifiers
and their canonical state subjects, its deterministic precedence placement,
schema/evaluator parity, and the focused direct evidence for that repair.

This acceptance is documentation-only and non-authorizing. It creates no
schema, Python, test, package, export, runtime, integration, orchestration,
state-mutation, persistence, networking, deployment, execution, or live-money
authority.

Stage 2 remains **HOLD with ESCALATE elements**. Stage 3 remains unentered and
unauthorized.

## Accepted Provenance

The accepted founder decision is commit
`08e8a2d20eeee4a6b6608e3499bac95e290f18cb` (`docs: record sniperbot fsm
transition request coherence decision`). That commit created exactly the
[Canonical FSM Transition-Request Coherence founder decision record](sniperbot-live-money-readiness-ladder-stage-2-canonical-fsm-transition-request-coherence-founder-decision-record.md).

The accepted implementation repair is commit
`fe278f6491e328951bc0e1a07f77548eec5c9e7f` (`fix: align sniperbot fsm
transition request coherence`). It is a direct successor to the founder
decision commit and changed exactly:

* [the Canonical FSM schema](../../schemas/sniperbot-fsm-transition-decision.schema.json);
* [the pure Canonical FSM evaluator](../../src/sniperbot/fsm/transition_contract.py); and
* [the focused Canonical FSM direct tests](../../tests/test_sniperbot_fsm_transition_contract.py).

The acceptance authority is the separate founder-authorized independent
read-only implementation-evidence revalidation performed at the clean,
synchronized implementation checkpoint
`fe278f6491e328951bc0e1a07f77548eec5c9e7f`. The independent oracle was
derived directly from the founder decision and did not import or call the
production canonical-pair helper or use the committed tests as its
expected-value oracle.

## Accepted Scope

The accepted repair establishes that each closed transition-request
identifier is applicable only to its governed canonical state subject. A
closed identifier combined with a non-canonical pair of closed states remains
a well-formed governed request, not a structural boundary error.

After higher-priority boundary, null-applicability, forced-lockout,
contradiction, and current-lockout handling, an ordinary mismatch returns:

* `allowed = false`;
* `resulting_state` equal to the exact request `current_state`;
* `ReasonCode.UNDEFINED_TRANSITION`;
* `RequiredAction.GOVERNANCE_REVIEW`; and
* exact preservation of request current state, requested state, and
  correlation reference.

No public API, state, transition identifier, reason, action, fact, authority
representation, default, sentinel, coercion, import, package export, or
capability is added by the accepted repair.

## Accepted Canonical Mapping Verification

Independent verification confirmed all nine founder-selected mappings:

1. `PAUSE_TO_READY`: `PAUSE -> READY`
2. `READY_TO_ARMED_MANUAL`: `READY -> ARMED_MANUAL`
3. `READY_TO_ARMED_AUTO`: `READY -> ARMED_AUTO`
4. `ARMED_AUTO_TO_IN_TRADE`: `ARMED_AUTO -> IN_TRADE`
5. `ARMED_MANUAL_TO_IN_TRADE`: `ARMED_MANUAL -> IN_TRADE`
6. `IN_TRADE_TO_READY`: `IN_TRADE -> READY`
7. `IN_TRADE_TO_PAUSE`: `IN_TRADE -> PAUSE`
8. `ANY_TO_LOCKOUT`: any declared current state with requested state
   `LOCKOUT`, remaining dependent on `lockout_required = true`
9. `LOCKOUT_TO_PAUSE`: `LOCKOUT -> PAUSE`, the sole reset-exit candidate

`ANY_TO_LOCKOUT` with `lockout_required = false` does not create an
evidence-free lockout. Outside the current-lockout gate it returns the
governed undefined-transition tuple. No identifier has a second canonical
subject.

## Accepted Exhaustive and Precedence Verification

The independent oracle exercised all
`6 current states x 6 requested states x 9 identifiers = 324` closed triples.
The exact result was:

* `14` canonical subjects;
* `310` mismatched subjects;
* `258` ordinary mismatches producing
  `UNDEFINED_TRANSITION / GOVERNANCE_REVIEW`; and
* `52` mismatches while currently locked retaining the higher-priority
  `LOCKOUT_REQUIRED / RESET_REQUIRED` tuple.

All `32` formerly allowed mismatches were independently confirmed closed.
All `324` forced-lockout combinations retained the forced-lockout tuple. All
`324` contradiction combinations retained the contradiction tuple. All `53`
prohibited alternatives to the single exact locked reset exit remained
closed.

The accepted deterministic precedence is:

1. structural, closed-type, required-field, reference, and runtime-type
   validation;
2. transition-specific null-authority applicability validation;
3. forced lockout;
4. contradictory-input handling;
5. the current-`LOCKOUT` gate;
6. identifier/state-pair coherence and ordinary transition legality;
7. transition-specific prerequisites;
8. authority evaluation and collision handling;
9. reset facts; and
10. the final allowed or governed-denial decision.

Independent collision probes confirmed that malformed inputs remain boundary
errors; forced lockout wins over a well-formed mismatch; contradiction wins
over a mismatch; the current-lockout gate wins over a mismatch; and coherence
wins before ordinary prerequisite, authority, collision, or reset-fact
evaluation.

## Accepted Schema/Evaluator Parity

Independent schema evaluation confirmed all nine canonical mapping rows and
validated the evaluator envelopes for:

* all `324` baseline closed triples;
* all `324` forced-lockout triples;
* all `324` contradictory-input triples;
* all `32` formerly allowed mismatches; and
* `81` additional canonical-negative, authority, and reset branches.

Closed mismatches are admitted as structurally valid requests and constrained
to the governed denial fields where Draft 2020-12 can represent those
relationships. Inconsistent allowed mismatch envelopes are rejected. Exact
current-state retention and correlation-reference equality remain enforced
by the pure evaluator where sibling-value comparison is not representable in
the schema.

Higher-priority forced-lockout, contradiction, and current-lockout branches
do not conflict with the coherence constraints. JSON parsing, closed
vocabularies, required properties, contextual authority nullability,
additional-property rejection, strict Boolean fields, and reference
constraints remain intact.

## Accepted Regression Preservation

Independent verification confirmed no regression to:

* strict Python and JSON boundary behavior;
* omission versus explicit `None` behavior;
* transition-specific null-authority applicability;
* authority-failure and collision subprecedence;
* forced-lockout behavior;
* prohibited lockout exits and exact reset behavior;
* prerequisite, authority, reset, reason, and action mappings;
* exact current-state, requested-state, and correlation-reference
  preservation;
* frozen request, nested-evidence, and decision structures;
* deterministic equal-by-value but identity-distinct repeated decisions;
* request and nested-evidence non-mutation;
* evaluator purity and totality for well-formed governed input;
* the public API and package-root exports; and
* production import and prohibited-capability boundaries.

Both arming and reset authority matrices passed all `32` closed evidence
combinations. Each matrix contained `25` multi-failure collisions with the
published winner distribution of `15` absence, `7` stale, and `3` revoked
collisions.

Production imports remain limited to `__future__`, `dataclasses`, and `enum`.
No filesystem, environment, time, randomness, logging, telemetry, network,
HTTP, socket, subprocess, database, persistence, queue, cache, registration,
runtime, integration, orchestration, market-data, broker, wallet, credential,
order, routing, transaction, execution, deployment, or live-money capability
was introduced.

## Accepted Implementation-Evidence Quality

The committed focused evidence contains no skipped, expected-failure,
`xfail`, vacuous, or private-helper-coupled coherence test. It independently
encodes the founder mapping, exhaustively enumerates the closed state space,
proves closure of the `32` formerly allowed mismatches, and verifies the
required precedence collisions.

The separate revalidation used its own founder-derived mapping and precedence
model. It did not infer correctness from passing implementation-authored
tests. The evidence is complete for the bounded transition-request coherence
repair and is accepted as deterministic, non-circular, and independently
reproducible.

## Accepted Repository Validation Summary

The independent read-only revalidation at checkpoint
`fe278f6491e328951bc0e1a07f77548eec5c9e7f` recorded:

* focused Canonical FSM tests: `34 passed`;
* Contract Validation: `7 passed`;
* Contract and Authority Clarity: `30 passed`;
* Explicit Authority Clarity Validator: `23 passed`;
* canonical full suite: `558 passed`;
* canonical mapping verification: passed;
* exhaustive closed-transition verification: passed;
* deterministic precedence verification: passed;
* schema/evaluator parity: passed;
* strict boundary and null/omission preservation: passed;
* authority-collision and lockout regression checks: passed;
* purity, immutability, determinism, identity, and non-mutation checks:
  passed;
* implementation-evidence quality review: passed;
* commit lineage and exact publication-scope checks: passed;
* JSON parsing, final-newline, trailing-whitespace, and `git diff --check`:
  passed;
* repository divergence: `0/0`;
* Git locks: none; and
* working tree and index: clean.

No substantive discrepancy was found.

## Preserved Deferred Items

The pre-existing non-executable schema-description wording that states null
authority represents absent evidence remains deferred, unchanged, and outside
this acceptance. It did not alter executable schema validation or evaluator
behavior in this repair.

Future Stage 2 gates remain separately governed and deferred. This acceptance
does not select, authorize, begin, combine, or complete another repair or
implementation lane. It does not certify Stage 2 completion, modify the
Advancement Gate, index this artifact, or authorize Stage 3.

## Repository State at Acceptance Construction

Before this single documentation artifact was created, branch `main`, `HEAD`,
and `origin/main` were synchronized at
`fe278f6491e328951bc0e1a07f77548eec5c9e7f`, divergence was `0/0`, the working
tree and index were clean, and no Git lock file existed.

The acceptance publication is limited to this record. Post-publication
synchronization and clean-state verification are required independently of
the accepted implementation checkpoint.

## Formal Acceptance Determination

**PASS -- ACCEPTED.**

The Canonical FSM Transition-Request Coherence implementation repair and its
focused direct evidence are accepted as conformant to the founder decision.
The bounded transition-request coherence implementation-evidence requirement
is complete. No substantive discrepancy remains in this repair lane.

This acceptance does not grant authority to invoke, register, integrate,
orchestrate, deploy, persist, network, mutate state, access market data,
access a broker or wallet, create or route an order, execute a transaction,
operate with live money, enter another lane, advance Stage 2, or enter Stage
3.

Stage 2 remains **HOLD with ESCALATE elements**. Stage 3 remains unentered and
unauthorized.
