# Repository Architecture Map

## Specification Layers

```mermaid
flowchart TD
    A["EchoAuth Request Contract"] --> B["Identity Resolution"]
    B --> C["Authority Resolution"]
    C --> D["Delegation Validation"]
    D --> E["Policy Evaluation"]
    E --> F["Invariant Validator"]
    F --> G["Runtime Envelope"]
    G --> H["Execution Token"]
    H --> I["Execution Claims"]
    I --> J["Runtime State Machine"]
    J --> K["Audit Record"]
    K --> L["Audit Chain"]

    C --> M["Authority Registry"]
    C --> N["Authority Revocation"]
    E --> O["Policy Registry"]
    J --> P["Runtime Halt Model"]
    P --> Q["Refusal Engine"]
    P --> R["Escalation Engine"]
    P --> S["Runtime Recovery"]
    J --> T["Runtime Session Model"]
    J --> U["Event Bus"]
    U --> V["Notification Contracts"]
    J --> W["Emergency Override Controls"]
    J --> X["Security Model"]
    J --> Y["API Spec"]
    K --> Z["Audit Log Spec"]
```

## Repository Areas

| Area | Purpose | Status |
|---|---|---|
| `specs/` | Implementation-facing component contracts | Complete at specification structure level. |
| `governance/` | Governance foundation and authority principles | Populated. |
| `architecture/` | System overview and architecture placeholders | Partially populated. |
| `runtime/` | Runtime implementation guidance | Initial README only. |
| `src/echoauth/` | Python runtime stubs | Partial starter implementation. |
| `docs/` | Glossary, vision, use cases, readiness reports | Partially populated. |
| `patents/` | Patent support placeholders | Mostly empty. |
| `tests` | Test placeholder | Empty file, not usable test tree. |

## Implementation Sequence

1. Define schemas for all spec inputs and outputs.
2. Implement identity model and identity resolution.
3. Implement authority registry, revocation, and authority resolution.
4. Implement delegation model and delegation validation.
5. Implement policy registry, policy engine, and policy evaluation.
6. Implement invariant validator.
7. Implement runtime envelope, execution token, and execution claims.
8. Implement runtime state machine, halt/refusal/escalation/recovery.
9. Implement audit record, audit log, and audit chain.
10. Implement event bus and notification contracts.
11. Add conformance tests and CI.
