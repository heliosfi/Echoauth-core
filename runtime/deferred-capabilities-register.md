# Deferred Capabilities Register

Freeze timestamp: `2026-06-19T21:12:47Z`

The following capabilities are outside the Sprint 2A-2P frozen baseline.
Absence is intentional and must fail closed where applicable.

| Capability | Current Evidence Boundary | Blocking Dependency | Implementation Before Resolution |
| --- | --- | --- | --- |
| Full runtime orchestration | Individual services exist without an orchestrator | Canonical orchestration and atomic sequencing contract | No |
| Autonomous or command execution | Execution Control emits eligibility evidence only | Execution service, dispatch, provider, and safety contracts | No |
| Runtime-state mutation | Sprint 2L validates proposed transitions only | Atomic state repository, concurrency, and transition-authority contracts | No |
| Recovery execution | Sprint 2P emits eligibility outcomes only | Separate operational Recovery and state-transition contracts | No |
| `HOLD` proposal processing | Proposal-only JSON Schema exists | Canonical proposal consumer and transition contract | No |
| Execution-token issuance | Models/interfaces only | Issuance authority, uniqueness, nonce, replay, signing, and storage contracts | No |
| Runtime-envelope generation | Models/interfaces only | Envelope assembly, validation, signing, and persistence contracts | No |
| Execution claims | Abstract boundary only | Claim lifecycle, atomic ownership, replay, and persistence contracts | No |
| Notification delivery | Abstract boundary and event contracts only | Delivery adapter, recipient, retry, privacy, and failure contracts | No |
| External event transport | Event validation exists without transport | Broker, delivery, ordering, retry, and dead-letter contracts | No |
| Production persistence adapters | In-memory repositories and SQL contract only | Engine selection, migrations, transactions, locking, and operational controls | No |
| External identity providers | Provider-neutral verifier boundary only | Credential-provider, secret-handling, and assurance contracts | No |
| External authority and reviewer discovery | Explicit supplied records/configuration only | Trusted registry, lifecycle, identity proof, and roster contracts | No |
| Evidence signing and key management | Canonical hashes and audit chaining only | Signature format, trust roots, rotation, revocation, and KMS contracts | No |
| Durable idempotency | In-process caches only | Persistent decision-key and concurrency contract | No |
| Delegation-chain execution | Chain metadata preserved and fails closed | Bounded chain schema and validation algorithm | No |
| Domain policy expression language | Explicit local rule model only | Canonical expression grammar and evaluator contract | No |
| Domain invariant fact production | Configured equality validation only | Trusted fact-producer and provenance contracts | No |
| Institutional override execution | Override records are inert evidence | Explicit institutional precedence and execution-effect contracts | No |
| Emergency override execution | Override classification is non-executing | Emergency authority, bounded effect, transition, and audit contracts | No |
| Recovery Review Protocol issuance | Protocol evidence can be validated | Protocol issuer, lifecycle repository, signature, and revocation contracts | No |
| Legacy API/protobuf vocabulary alignment | Documented contract exceptions remain | Approved regeneration against current Sprint vocabulary | Contract work only |
| Nested domain schemas | Canonical JSON object boundaries remain open | Domain-specific field specifications | Contract work only |

# Preserved Boundaries

- Identity verifies; it does not grant authority.
- Authority originates from explicit authority records.
- Delegation cannot expand source authority.
- Policy and invariants fail closed.
- Refusal and Halt evidence cannot be bypassed by escalation, review, override,
  execution eligibility, or Recovery eligibility.
- Coordination proposes, governance permits, and execution remains separate
  from authorization.

# Register Status

All listed capabilities remain **DEFERRED** at the Sprint 2A-2P freeze.
