# SniperBot Live-Money Readiness Ladder Stage 2 Rollback / No-Action Fallback Contract Definition Review

## Status and Boundary

Documentation-only / governance-only / contract-definition-only /
fallback-planning-only / non-runtime / non-execution / non-authorizing.

This review defines one proposed future pure classification contract for
externally supplied rollback and no-action fallback facts. It does not execute
rollback, mutate state, restore data, reverse orders, interact with a broker,
orchestrate recovery, integrate with the FSM, or enter Stage 3.

Stage 2 remains **HOLD**. EchoAuth remains the sole permission authority. No
next lane begins automatically.

## Exact Subject

The subject is **SniperBot Stage 2 — Rollback / No-Action Fallback Decision
Contract**: a descriptive, deterministic classification of supplied facts
about whether rollback review, no action, or further governance review is
required.

It consumes no executable recovery procedure and creates no rollback authority.

## Proposed Immutable Inputs

The smallest proposed input set is caller-supplied and already determined:

* current condition or opaque state reference;
* rollback-required indicator;
* rollback-available indicator;
* rollback-evidence-present indicator;
* rollback-evidence-current indicator;
* rollback-evidence-sufficient indicator;
* rollback-evidence-contradictory indicator;
* externally supplied no-action indicator;
* externally supplied halt, failure, or recovery context;
* optional bounded EchoAuth authority evidence or reference; and
* mandatory opaque correlation reference.

No runtime state transition, broker fact, order detail, credential, command,
market datum, or recovery procedure is in scope.

## Proposed Descriptive Outputs

The smallest output set may contain:

* classification outcome;
* closed reason code;
* required human or governance action;
* correlation reference; and
* optional descriptive rollback/no-action posture.

Outputs must not contain rollback commands, state mutations, cancellation or
replacement instructions, broker instructions, database operations,
credentials, or recovery orchestration.

## Proposed Fail-Closed Behavior

The future contract must remain non-authorizing and fail closed when rollback
evidence is missing, stale, insufficient, contradictory, unavailable, or
uncertain; when rollback and no-action are both asserted; when authority is
absent, invalid, stale, revoked, contradictory, or out of scope; or when an
input combination is unknown or undefined.

Silence, absence, or uncertainty must never become rollback permission,
recovery authority, or execution authority. Exact precedence and mappings are
intentionally unresolved for founder decision.

## Authority and State Boundaries

EchoAuth remains the sole permission authority. Optional authority evidence is
contextual only unless a later founder decision requires it. This contract may
not grant, recreate, repair, broaden, reinterpret, or bypass authority.

The subject is separate from FSM transition evaluation, halt or lockout state
changes, recovery-state transitions, reset execution, override processing,
state restoration, compensating transactions, and runtime integration. A
classification result cannot mutate the accepted six-state FSM.

## Neighboring Subjects Excluded

Asset-Class Deferral / No-Action; eligibility or exclusion; stock, options, or
crypto rules; market data; signals; strategy; risk; sizing; simulation;
replay/backtesting; order routing; broker or Robinhood access; cancellation,
replacement, reversal, or liquidation; credentials; deployment; persistence;
networking; execution; FSM integration; EchoAuth runtime integration; and
Stage 3 remain separate and unauthorized.

## Founder Decisions Required Before Schema Definition

1. Outcome vocabulary.
2. Reason-code vocabulary.
3. RequiredAction vocabulary and mappings.
4. Meaning of rollback required.
5. Meaning of rollback available.
6. Whether availability is only consumed as an external fact.
7. Rollback versus no-action precedence.
8. Contradiction precedence.
9. Authority-evidence requirement.
10. Unknown and undefined input behavior.
11. Relationship to halt, lockout, reset, and recovery concepts.
12. Exact future schema, implementation, and test paths.
13. Validation and stop conditions.

These decisions are not resolved by this review.

## Future Boundaries — Not Authorized

If separately approved, a future order may define one schema/interface file,
one pure implementation file, one direct test file, and a package initializer
only if repository conventions require it. No such files are created or
authorized here.

## Readiness Conclusion

`ROLLBACK / NO-ACTION FALLBACK CONTRACT READY FOR FOUNDER DECISIONS`

The exact next founder decision is creation of a bounded founder decision
sheet. It is not schema or implementation authorization.

Stage 2 remains **HOLD** and Stage 3 remains unentered and unauthorized.
