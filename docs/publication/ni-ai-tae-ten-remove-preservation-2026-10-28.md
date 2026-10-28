# IEEE S&P 2027 TEN-REMOVE manuscript preservation

**Authority / source:** N.B.C.; explicit user instruction to preserve the supplied corrected PDF on a separate branch and open a draft PR.  
**Timestamp:** 2026-10-28 · 06:46 PM EDT  
**ISO-8601:** `2026-10-28T18:46:33-04:00`  
**Status:** OBSERVATION / PRESERVE — DRAFT REVIEW; HOLD MERGE / HOLD SUBMISSION  
**Base checkpoint:** `1af7c1f17e9e019982e74262cdc9fc2a779f1c9d`

## Preserved artifact

- File: `IEEE_SP2027_Anonymous_TEN_REMOVE_Corrected_2026-10-28.pdf`
- Supplied source: exact-name corrected PDF, Library file `libfile_647403e63f808191936c97ca1b21f9d0`, version 7.
- Size: 318,526 bytes.
- SHA-256: `6a57543fda8ca7c1343f1ed9ac9995df7fda6d749ebdc3f70966567dea757ecc`.
- Integrity: parsed successfully by Poppler and MuPDF; 6 US Letter pages, PDF 1.7, unencrypted. All pages rendered; visual review found readable manuscript content.
- Supplied bytes copied unchanged; no PDF regeneration or editing performed.

## Exact abstract verification

PASS — column-aware extraction with line-break and whitespace normalization finds exactly one occurrence in the abstract:

> This paper presents an evidence-bounded governance model in which these functions remain separately governed responsibilities.

PASS — the former enumeration “capability, reasoning, proposal, state assessment, permission, execution eligibility, execution, return, reassessment, and continuation” is absent from the corrected PDF's normalized text.

## Bounded preservation comparison

Comparison-only baseline: `IEEE_SP2027_Anonymous_Wording_Revised_2026-10-26.pdf` (325,649 bytes; 6 pages), Library file `libfile_99effcee61c881919b64ec8bab039793`.

Column-aware text extraction, ordered by position and normalized for whitespace and line-wrap hyphenation, establishes identical manuscript text from section 1 through the end, including references and appendices. Abstract differences are the requested enumeration replacement with “these functions” and heading `Abstract—` becoming `Abstract`. Both PDFs have 6 pages. This is a normalized text comparison, not a claim of identical PDF layout or byte identity between versions. The baseline is not committed or substituted for the corrected artifact.

## HOLD and scope boundaries

Existing records in `docs/publication/` remain unchanged, including the canonical reconstruction and prior integrity/readiness records. No existing tracked file is altered by this preservation commit. Historical/frozen evidence and runtime work are preserved.

SAL-9 remains HOLD — 3 PASS / 2 HOLD-PARTIAL / 0 FAIL. SAL-13 and SAL-15 remain HOLD/PARTIAL. No runtime tests were rerun; PDF checks do not establish new research outcomes, venue compliance, independent validation, or submission readiness.

No merge, deployment, IEEE submission, or inferred authority. Draft PR review remains pending. Bibliographic and venue requirements remain outside this preservation task.
