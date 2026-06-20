# EchoAuth Authority Model

The EchoAuth authority model defines who may authorize an action, who may
execute a delegated action, and what the system must do when authority is
unclear.

Authority is explicit, bounded, auditable, and prior to execution.

## Authority Classes

### Root Human Authority

Root human authority is the legally or operationally responsible human actor for
the request context.

In child, school, clinical, and caregiver environments, this is normally the
parent or legal caregiver unless another legally recognized authority controls
the specific action.

### Institutional Authority

Institutional authority may apply when a public agency, school, clinic, court,
or regulated organization has a recognized responsibility for a specific
workflow.

Institutional authority must be constrained to the institution's lawful scope.
It does not automatically override parent or caregiver authority.

### Delegated Authority

Delegated authority is a bounded permission granted by a valid authority source.

Delegation must define:

- grantor,
- delegate,
- permitted action,
- permitted resource or context,
- duration or expiration,
- constraints,
- revocation conditions,
- and audit requirements.

### Execution Role

An execution role allows a person or subsystem to carry out an authorized action.

Execution roles are not authority sources. Teachers, aides, clinicians,
caregivers, services, and agents may execute, observe, document, or assist only
inside the granted scope.

## Parent-Anchored Care Model

For vulnerable-care settings, EchoAuth uses a parent-anchored model:

1. The parent or legal caregiver is the default authority anchor.
2. School and clinical staff are delegates unless a separate legal instrument
   grants authority.
3. Delegates may not approve actions outside the delegated scope.
4. Ambiguous authority produces hold or escalation, not inferred permission.
5. The audit trail must preserve the distinction between authority source and
   execution actor.

## Authority Resolution

Authority resolution answers one question:

Can this actor authorize this action in this context at this time?

The authority resolver must evaluate:

- actor identity,
- relationship to the subject,
- legal or operational role,
- delegation scope,
- expiration,
- action/resource match,
- context constraints,
- conflicts,
- revocation status,
- and required escalation rules.

## Authority Failure Modes

The following conditions are non-authorized states:

- unknown authority source,
- unreachable authority source,
- expired delegation,
- scope mismatch,
- substituted authority,
- conflicting authority signals,
- missing identity proof,
- revoked permission,
- replayed authorization,
- and policy or invariant mismatch.

The compliant outcome is refusal, hold, halt, or escalation according to the
runtime envelope.

## Non-Expansion Rule

No EchoAuth component may increase the permissions of a subject, delegate, or
execution actor without a valid authority event.

Permission expansion requires a new authorization path, new audit record, and
valid authority proof.

## Source Journal Files

- `docs/journal/2026-02-05_(11).html`
- `docs/journal/2026-02-09_(16).html`
- `docs/journal/2026-02-09_(24).html`
- `docs/journal/2026-02-09_(26).html`
- `docs/journal/2026-02-19_(23).html`
