# EchoAuth Timestamp Provenance — Repository Propagation Record

**Authority:** Nicholas B. Carty (N.B.C.)  
**Propagation timestamp:** 2026-08-27 · 9:39 PM EDT  
**ISO-8601:** `2026-08-27T21:39:23-04:00`  
**UTC:** `2026-08-28T01:39:23Z`  
**Status:** MILESTONE / DOCUMENTATION ALIGNMENT  
**Pre-propagation main:** `d772546867e0eb260431df4c0a91a2bdd7c4d4c8`  
**Established timestamp standard:** `docs/governance/nbc-timestamp-provenance-standard-2026-08-27.md`

## Decision

The N.B.C. Timestamp Provenance Standard is now the repository-level provenance discipline for consequential EchoAuth governance records.

This propagation applies prospectively to consequential records created, amended, corrected, reissued, or used to establish a new governed decision after the standard became effective at **2026-08-27 · 9:33 PM EDT**.

## In-scope record classes

The standard applies to consequential governance material in, including but not limited to:

- `docs/governance/`
- `docs/control-gates/`
- `docs/assessments/`
- `docs/acceptance-records/`
- `docs/records/`
- governance-bearing `docs/foundation/` material
- thesis amendments and aligned governance notes
- future repository records that declare authority, permission, decision, milestone, status change, acceptance, refusal, hold, pass, fail, closure, entry, or execution boundary

## Historical-record preservation rule

Pre-standard records are **not mass-rewritten** merely to add a semantic timestamp. Their original text, Git history, commit timing, artifact hashes, and native evidence surfaces remain historical evidence.

When a pre-standard record becomes consequential again, the new record or amendment SHOULD attach the current provenance fields and reference the historical checkpoint rather than silently rewriting the historical event time.

This preserves the distinction:

`HISTORICAL RECORD TIME != LATER ALIGNMENT TIME`

and:

`TIMESTAMP != ORIGIN OF THOUGHT OR UNDERSTANDING`

## Required fields for new consequential records

New consequential records SHOULD preserve:

- **Timestamp**
- **Event**
- **Status**
- **Authority / Source**
- **Evidence Boundary**
- **Reference / Checkpoint**

Human-facing, ISO-8601, and UTC forms follow the canonical standard where useful.

## Repository identity rule

A semantic timestamp supplements but does not replace repository identity.

- Git commit SHA identifies exact repository state.
- Artifact hash identifies exact artifact bytes.
- Platform-native created/updated time identifies platform activity.
- Semantic timestamp identifies the governed event time recorded by the document.

None silently substitutes for another.

## Evidence boundary

This propagation establishes documentation and provenance discipline only. It does not:

- change any historical PASS, FAIL, HOLD, PARTIAL, closure, or acceptance disposition;
- create runtime, deployment, trading, command-execution, autonomous-action, institutional, legal, medical, ownership, authorship, novelty, priority, or external-validation authority;
- convert an old record into a newly validated record;
- alter the NI-AI thesis conclusion or consolidated adversarial result;
- establish cross-domain implementation safety by timestamp alone.

The current NI-AI thesis posture remains:

`SAL-9 = HOLD — 3 PASS / 2 HOLD-PARTIAL / 0 FAIL`

## Propagation record

**TIMESTAMP — 2026-08-27 · 9:39 PM EDT**  
**ISO — `2026-08-27T21:39:23-04:00`**  
**STATUS — MILESTONE / DOCUMENTATION ALIGNMENT**  
**AUTHORITY / SOURCE — Nicholas B. Carty (N.B.C.)**  
**EVENT — The timestamp provenance standard becomes the prospective repository-level discipline for consequential EchoAuth governance records while preserving pre-standard records as historical evidence.**  
**EVIDENCE BOUNDARY — Provenance alignment only; no retroactive re-dating, no change to research/runtime status, and no creation of authority.**  
**REFERENCE — Standard effective at 2026-08-27 · 9:33 PM EDT; pre-propagation main `d772546867e0eb260431df4c0a91a2bdd7c4d4c8`.**
