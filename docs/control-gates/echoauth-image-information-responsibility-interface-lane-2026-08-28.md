# N.B.C. AUTHORITY — ECHOAUTH IMAGE-INFORMATION RESPONSIBILITY INTERFACE LANE

**Authority:** Nicholas B. Carty (N.B.C.)  
**Date:** August 28, 2026  
**Decision:** ADVANCE — INFORMATION / INTERFACE GOVERNANCE ONLY

## Principle

An interface may distribute, coordinate, and preserve responsibilities across participants or systems without transferring the underlying authority that belongs to each participant.

Shared responsibility does not mean shared authority.

## EchoAuth Role

Where an image supplies information, EchoAuth may govern the information boundary surrounding that image, including:

- source and provenance;
- timestamp and evidence context;
- permitted use;
- authorized recipients or interfaces;
- interpretation boundaries;
- transformations applied to the information;
- revocation or reassessment;
- fail-closed behavior when authority or meaning is unresolved.

The image itself does not grant authority.

Information extracted, described, or inferred from an image does not automatically become permission to act.

## Timestamp and Provenance Limits

Image-associated timestamps must remain attributable to their source and evidence class. Capture, creation, modification, upload, export, platform, and record timestamps are distinct evidence surfaces and must not silently substitute for one another.

No timestamp or metadata field alone establishes origin, complete chronology, authorship, ownership, authenticity, priority, or truth.

Provenance must remain classified as one of:

- independently verified;
- source-supplied;
- platform-supplied;
- inferred;
- missing; or
- conflicting.

A supplied or platform-preserved value is not independently verified merely because it is present. When the source, evidence class, or relationship among timestamps is unavailable or unresolved, that limitation must remain explicit.

## Transformation and Interpretation Lineage

The following evidence surfaces must remain distinguishable:

- the original image reference;
- a content binding or hash, when available;
- transformation history;
- extracted information;
- description; and
- inferred interpretation.

A transformation, extraction, description, or inference must not be represented as the unchanged original image or as independently verified source information. Missing transformation history or content binding must remain a stated limitation rather than being repaired through assumption.

## Responsibility Interface

The interface may allow different systems or people to perform their legitimate parts of a workflow while preserving responsibility at the correct boundary.

Therefore:

**information may move; responsibility may be coordinated; authority must remain attributable.**

EchoAuth governs that correspondence rather than erasing the distinction.

## Boundary

This lane does not establish:

- unrestricted execution authority;
- automatic runtime activation;
- ownership transfer;
- automatic acceptance of an interpretation;
- authority derived merely from possession of an image;
- equivalence between human judgment and system interpretation.

The governing separations are:

```text
IMAGE != AUTHORITY
INFORMATION != PERMISSION
TIMESTAMP != ORIGIN OR TRUTH
METADATA != VERIFIED PROVENANCE
INTERPRETATION != ACCEPTANCE
RESPONSIBILITY COORDINATION != AUTHORITY TRANSFER
```

## Fail-Closed Handling

Missing, malformed, unknown, unverifiable, contradictory, conflicting, stale, revoked, or unavailable authority or evidence fails closed.

This applies to authority, provenance, timestamp, transformation, recipient, permitted-use, and interpretation evidence.

Where any required evidence or authority is incomplete or unresolved, the correct state remains **HOLD / REQUEST / REASSESS / NO-ACTION** rather than assumed permission.

No error, fallback, partial result, or favorable interpretation becomes permission. No non-advancing state authorizes runtime movement, state mutation, execution, dispatch, or external-system action.

## Thesis Correspondence

This strengthens the applied-intelligence thesis:

**Interfaces can share work without confusing responsibility, capability, permission, or authority. Intelligence becomes useful across domains when the connection is preserved and the boundaries remain visible.**

**Lane status:** ADVANCE — concept and governance boundary established; no implementation is established. Any future implementation remains separately authorized and independently testable.
