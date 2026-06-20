# Sprint 2L Implementation Evidence

# Scope

Sprint 2L implements only the Runtime State Machine validation foundation:

- typed `RuntimeState`, `RuntimeTransition`, `RuntimeTransitionRequest`,
  `RuntimeTransitionDecision`, and `RuntimeStateEvidence` artifacts,
- a versioned graph containing 33 explicitly enumerated transitions,
- deterministic transition and requested-target validation,
- fail-closed handling for undefined or mismatched transitions,
- immutable, hash-bound validation evidence,
- in-process idempotency,
- Sprint 2A audit-chain integration for allowed and rejected proposals.

The state machine has no state store and no mutation method. `allowed=True`
means only that a proposed edge matches the graph.

# Canonical States

`REQUESTED`, `AUTHORIZED`, `REFUSED`, `ESCALATED`, `UNDER_REVIEW`,
`OVERRIDDEN`, `READY`, `EXECUTION_BLOCKED`, `EXPIRED`, and `HALTED`.

# Explicit Graph

| Current State | Allowed Transitions |
| --- | --- |
| `REQUESTED` | `AUTHORIZE -> AUTHORIZED`; `REFUSE -> REFUSED`; `ESCALATE -> ESCALATED`; `EXPIRE -> EXPIRED`; `HALT -> HALTED` |
| `AUTHORIZED` | `MARK_READY -> READY`; `REFUSE -> REFUSED`; `ESCALATE -> ESCALATED`; `BLOCK_EXECUTION -> EXECUTION_BLOCKED`; `EXPIRE -> EXPIRED`; `HALT -> HALTED` |
| `REFUSED` | `ESCALATE -> ESCALATED` |
| `ESCALATED` | `BEGIN_REVIEW -> UNDER_REVIEW`; `REFUSE -> REFUSED`; `EXPIRE -> EXPIRED`; `HALT -> HALTED` |
| `UNDER_REVIEW` | `OVERRIDE -> OVERRIDDEN`; `REFUSE -> REFUSED`; `ESCALATE -> ESCALATED`; `EXPIRE -> EXPIRED`; `HALT -> HALTED` |
| `OVERRIDDEN` | `MARK_READY -> READY`; `BLOCK_EXECUTION -> EXECUTION_BLOCKED`; `EXPIRE -> EXPIRED`; `HALT -> HALTED` |
| `READY` | `BLOCK_EXECUTION -> EXECUTION_BLOCKED`; `EXPIRE -> EXPIRED`; `HALT -> HALTED` |
| `EXECUTION_BLOCKED` | `RELEASE_BLOCK -> READY`; `ESCALATE -> ESCALATED`; `EXPIRE -> EXPIRED`; `HALT -> HALTED` |
| `EXPIRED` | none |
| `HALTED` | `ESCALATE -> ESCALATED` |

# Deterministic Processing

1. Validate canonical enum types, required identifiers, actor, reason, non-empty
   canonical evidence, and UTC occurrence time.
2. Resolve the exact `(current_state, transition)` key against
   `echoauth.runtime-state.v1`.
3. Allow only when the graph target also equals `requested_state`.
4. For undefined edges, return `undefined_transition`, `allowed=False`, and the
   unchanged current state.
5. For a target mismatch, return `requested_state_mismatch`, `allowed=False`,
   and the unchanged current state.
6. Canonically hash the source evidence and immutable state evidence.
7. Append an audit event for both valid and rejected proposals.
8. Return the same cached decision without a duplicate audit append for
   identical input.

# Test Evidence

Command:

```text
$env:PYTHONPATH='src'; python -B -m unittest discover -s tests -v
```

Result:

```text
Ran 144 tests in 0.173s

OK
```

The result includes every prior Sprint test and 11 Sprint 2L state-machine
tests. The graph test validates all 33 enumerated edges.

# Deferred Dependencies

- Runtime state reads, atomic compare-and-set mutation, transition history
  persistence, and concurrency control.
- Component-role authorization for transition actors.
- Guard integration with authorization, refusal, escalation, review, override,
  invariant, envelope, token, halt, and recovery evidence.
- Execution, token issuance, envelope generation, orchestration, notifications,
  external discovery, and runtime side effects.
- API, protobuf, JSON Schema, event-catalog, database, and integration adapters
  for the Sprint 2L vocabulary.

# Contract Ambiguities

| Ambiguity | Sprint 2L handling |
| --- | --- |
| Sprint 2L's ten states differ from the larger existing specification and generated protobuf enum. | Isolate the Sprint 2L vocabulary under `echoauth.runtime`; do not modify or silently replace generated contract models. |
| The requested compact state set has no complete edge table in existing artifacts. | Use only repository transition principles and the implemented authorization/refusal/escalation/review/override sequence; enumerate every accepted edge literally and reject everything else. |
| `READY`, `EXECUTION_BLOCKED`, `UNDER_REVIEW`, and `OVERRIDDEN` are absent from the older runtime graph. | Treat them as Sprint 2L validation states only; add no execution, persistence, or orchestration semantics. |
| Transition actor roles are not mapped to events. | Hash and audit the explicit actor ID but do not infer authority; caller authorization remains required before integration. |
| The specification uses `accepted` for transitions, while Sprint 2L forbids executing transitions. | Use `allowed` to mean graph validation only; never mutate runtime state. |

# Status

Sprint 2L Runtime State Machine foundation: complete as a deterministic,
validation-only component with documented contract and persistence boundaries.
