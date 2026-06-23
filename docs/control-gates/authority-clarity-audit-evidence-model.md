# Authority Clarity Audit Evidence Model

Status: AUDIT EVIDENCE MODEL -- DOCUMENTATION ONLY -- NOT RUNTIME

## Purpose

This file defines what evidence must be preserved after Authority Clarity
validation so proof can survive inspection.

It is an auditor-facing documentation-only planning artifact. It defines
evidence expectations only. It does not define storage, collection, logging,
schema fields, validator output, workflows, queues, services, or any runtime
mechanism.

It does not create runtime behavior, enforcement behavior, approval authority,
blocker resolution, register mutation, event-bus behavior, broker/trading paths,
services, agents, autonomous actions, click-through overrides, or
command-execution capability.

## Evidence Preservation Thesis

Authority Clarity proof is inspectable only when the validation result can be
traced back to stable, reviewable evidence.

The evidence model must preserve:

* how the operating law remained traceable
* which document, schema, validator, test, and CI proof references applied
* what was validated
* what authority source was claimed
* what ambiguity, absence, or conflict was found
* why a HOLD, REFUSE, or ESCALATE classification was produced
* what validator result was produced
* what test and CI proof supported the validator state
* what audit trail can reconstruct the validation path

## Spine Alignment

Authority Clarity audit evidence extends the current spine:

`operating law -> documents -> schema -> validator -> tests -> CI proof -> audit evidence`

Audit evidence must remain downstream of validation. It records proof for later
inspection. It does not move authority upstream, replace validation, approve
actions, resolve blockers, or create live behavior.

## Validation Input Evidence

Validation input evidence must preserve the submitted Authority Clarity payload
or a stable reference to it.

The preserved input evidence must make clear:

* input record identifier
* input source reference
* validation timestamp
* actor role
* subject role
* requested action
* requested mode
* authority scope
* delegated scope, if any
* lifecycle state
* freshness state
* conflict state
* asserted authority source
* validation schema version or schema reference
* validator version, commit, or source reference
* payload hash or equivalent integrity reference, if available

Input evidence must not depend on hidden defaults, inferred consent,
notification-only records, mutable UI state, click-through confirmation, or
runtime side effects.

## Authority-Source Evidence

Authority-source evidence must preserve the source that was used to evaluate
whether authority was explicit, current, role-aligned, scope-aligned,
lifecycle-aligned, and conflict-checked.

Authority-source evidence must identify:

* authority source type
* authority source identifier
* issuer or originating record
* reviewer or verification reference, if applicable
* actor and subject relationship
* permitted action scope
* delegated scope boundaries
* effective date
* expiration date or freshness rule
* lifecycle state reference
* revocation, supersession, or conflict reference
* reason the source was accepted, rejected, or treated as insufficient

Documentation-only files, planning files, Slack messages, GitHub notifications,
calendar entries, unreviewed notes, and unknown sources must not become
authority sources.

## Ambiguity And Conflict Evidence

Ambiguity and conflict evidence must preserve the facts that made authority
unclear, absent, stale, disputed, or out of scope.

The evidence set must identify:

* missing authority fields
* unknown actor or subject role
* unclear requested action
* unknown or stale authority source
* scope mismatch
* delegated authority exceeding its boundary
* lifecycle mismatch
* conflicting records
* unresolved reviewer state
* unavailable freshness proof
* any field that prevented a clear validator-only ALLOW classification

Ambiguity evidence must preserve non-action as a valid protected outcome.

Conflict evidence must be traceable enough for a later reviewer to see which
records disagreed and why Authority Clarity validation did not produce an
unambiguous validator result.

## HOLD / REFUSE / ESCALATE Evidence

HOLD evidence must preserve why validation stopped without authorizing action.

HOLD evidence should include:

* missing evidence reference
* stale evidence reference
* unknown evidence source reference
* incomplete role, scope, lifecycle, or freshness information
* reason validation could not proceed

REFUSE evidence must preserve why a requested action was not permitted.

REFUSE evidence should include:

* prohibited action reference
* invalid authority source reference
* explicit denial or revocation reference
* out-of-scope delegation reference
* reason the request must not be accepted

ESCALATE evidence must preserve why the evidence requires separately authorized
human review before any future movement could be considered.

ESCALATE evidence should include:

* conflicting authority records
* unresolved authority hierarchy
* contested role or delegation
* high-risk ambiguity
* reviewer reference, if one exists from a separately authorized process
* reason automated acceptance must not be inferred

HOLD, REFUSE, and ESCALATE evidence must not create approval authority or
resolve the blocker it records.

## Validator Result Evidence

Validator result evidence must preserve proof of the result produced by the
Authority Clarity validator without creating runtime behavior.

The evidence set must identify:

* validator command text or invocation reference, if available
* validator source path
* schema source path
* input reference
* output result
* error code or failure reason, if any
* validation timestamp
* commit reference
* local command output reference, if available
* CI run reference, if available

Current traceability references:

* schema: `schemas/authority-clarity-gate.schema.json`
* validator: `src/echoauth/contracts/authority_clarity_gate_validation.py`
* tests: `tests/test_authority_clarity_gate_validation.py`
* CI workflow: `.github/workflows/authority-clarity-validator.yml`

## Test And CI Proof References

Audit evidence must preserve test and CI proof references separately from
runtime decision evidence.

Test and CI proof references should include:

* test file path
* test command
* test result
* CI workflow path
* CI run identifier or URL, if available
* commit SHA tested
* timestamp of proof
* proof artifact reference, if available

Test and CI proof can show that validation rules were checked. Test and CI proof
must not become authority evidence for a real-world action.

## Audit Trail Expectations

The audit trail expectation is that preserved evidence must be sufficient for an
auditor to reconstruct:

* the input that was validated
* the evidence considered
* the authority source classified as sufficient, insufficient, or rejected
* the ambiguity or conflict encountered
* the validator result
* the reason for the validator-only HOLD, REFUSE, ESCALATE, BLOCK, LOG_ONLY,
  or ALLOW classification
* the test and CI proof supporting the validator state
* the commit and document references in effect at validation time

Preserved audit evidence must include enough context to show ordering,
timestamps, source references, and non-action outcomes.

Audit evidence must be reviewable without relying on live service state,
broker/trading state, event-bus mutation, register mutation, command execution,
click-through confirmation, or autonomous agent behavior.

## Prohibited Powers

This audit evidence model does not authorize:

* code changes
* schema changes
* validator changes
* test changes
* CI changes
* runtime behavior
* enforcement behavior
* approval authority
* blocker resolution
* register mutation
* event-bus behavior
* broker access
* trading permission
* services
* agents
* autonomous actions
* click-through overrides
* command-execution capability

## Future Movement Rule

Any future implementation of audit evidence storage, schema fields, validator
output, logging, CI artifact preservation, runtime gates, enforcement behavior,
approval behavior, blocker resolution, register mutation, event-bus behavior,
broker/trading behavior, services, agents, autonomous actions, click-through
overrides, or command-execution capability requires a separate explicit bounded
task.
