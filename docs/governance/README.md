# EchoAuth Governance Provenance

This directory is the canonical entry point for repository-level governance provenance standards.

## Active standard

- `nbc-timestamp-provenance-standard-2026-08-27.md` — canonical timestamp formats, required fields, evidence boundaries, correction rules, and cross-platform application.
- `timestamp-provenance-repository-propagation-2026-08-27.md` — repository-wide propagation record establishing prospective application to consequential EchoAuth governance records while preserving historical records unchanged.
- `stabilizer-kernel-timestamp-provenance-alignment-2026-08-27.md` — explicit timestamp-provenance alignment for the S-Kernel / Stabilizer / S1-S23 lineage while preserving historical journal and assessment timing.

## Effective rule

The timestamp provenance standard became effective at:

`2026-08-27 · 9:33 PM EDT`

Repository-wide propagation was recorded at:

`2026-08-27 · 9:39 PM EDT`

Stabilizer / kernel lineage alignment was recorded at:

`2026-08-27 · 9:46 PM EDT`

For consequential records created, amended, corrected, reissued, or used to establish a new governed decision after the standard became effective, preserve:

- Timestamp
- Event
- Status
- Authority / Source
- Evidence Boundary
- Reference / Checkpoint

## Historical preservation

Do not mass-rewrite pre-standard records solely to add semantic timestamps. Preserve their original text and Git history. When an older record becomes consequential again, attach a new timestamped amendment or decision that references the historical checkpoint.

`HISTORICAL RECORD TIME != LATER ALIGNMENT TIME`

`TIMESTAMP != ORIGIN OF THOUGHT OR UNDERSTANDING`

Timestamping supplements Git SHAs, artifact hashes, and native platform metadata; it does not replace them or create authority.

## Boundary

This provenance layer is documentation-only. It does not alter existing governance dispositions, thesis results, runtime authority, deployment status, ownership, authorship, novelty, priority, or external validation.
