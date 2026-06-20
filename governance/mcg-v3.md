# MCG v3 Governance Specification

MCG, the Melanin Cognitive Governance layer, is EchoAuth's judgment and
authority-resolution layer.

MCG exists to resolve which authority controls a request. It does not execute
actions and does not optimize outcomes.

## Scope

MCG is responsible for:

- resolving authority conflicts,
- identifying the controlling authority source,
- producing deterministic authority verdicts,
- preserving human accountability,
- and providing auditable authority evidence to EchoAuth and CEG.

MCG is not responsible for:

- command execution,
- execution sequencing,
- semantic interpretation,
- user-interface behavior,
- optimization,
- or substituting system judgment for human authority.

## Inputs

An MCG decision may receive:

- subject identity,
- requesting actor identity,
- proposed action,
- target resource,
- contextual facts,
- parent/caregiver authority records,
- institutional authority records,
- delegation records,
- revocation records,
- policy version,
- and conflict/escalation rules.

## Output

MCG emits an authority verdict.

A verdict must include:

- verdict identifier,
- request identifier,
- controlling authority source,
- authority status,
- reason code,
- effective scope,
- expiration or review boundary,
- evidence references,
- and audit metadata.

## Verdict States

- `authority_valid`: a controlling authority exists for the request.
- `authority_refused`: authority is absent, invalid, revoked, or out of scope.
- `authority_hold`: authority may exist but cannot be verified at runtime.
- `authority_conflict`: multiple incompatible authority signals exist.
- `authority_escalate`: a designated authority must review before execution.

## Determinism Requirement

MCG must produce the same verdict for the same authority inputs, policy version,
and invariant version.

If evidence is missing or inconsistent, the deterministic result is not
best-effort permission. It is hold, conflict, refusal, or escalation.

## Relationship To NI-AI

NI-AI may interpret language, intent, emotion, and context. NI-AI does not grant
authority.

MCG may consume interpreted context as non-binding evidence, but MCG must resolve
authority through explicit governance rules.

## Relationship To CEG

MCG resolves authority.

CEG sequences execution.

CEG must not execute unless it receives a valid authority/authorization result
from the upstream governance path. MCG must not issue execution tokens or perform
execution sequencing.

## Source Journal Files

- `docs/journal/2026-02-05_(11).html`
- `docs/journal/2026-02-08_(7).html`
- `docs/journal/2026-02-09_(16).html`
- `docs/journal/2026-02-19_(23).html`
