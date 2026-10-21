# Appendix B — Editorial PDF Integrity and Scope Verification (2026-10-21)

**Authority attribution:** Nicholas B. Carty (N.B.C.)  
**Disposition:** PREPARE — HOLD SUBMISSION / PRESERVE / STOP  
**File:** `NI_AI_EchoAuth_TAE_Evidence_Review_Packet_2026-10-21.pdf`  
**Size:** 79,849 bytes  
**Pages:** 3 (US Letter, unencrypted, PDF 1.4)  
**SHA-256, calculated directly from the PDF bytes:**

```text
21b42d8aba2b94b6601bcec40ed216e430591eaacd276e9549defdbb2eb9df93  NI_AI_EchoAuth_TAE_Evidence_Review_Packet_2026-10-21.pdf
```

**Verification:** SHA-256 recalculated locally. A previously supplied companion checksum file contained the different hash `f8995ba5b72bc32d21f41ddf30157f8d513ca2995da132df7066a2a9c1b4a3f8` and DID NOT match this PDF. The companion checksum file was corrected locally and `sha256sum -c` returned `OK`. This record preserves that discrepancy rather than retroactively asserting the previous checksum was correct.

**Repository evidence checkpoint:** `74dd426251c0174c2e9e2b7f51c70075e08e34fb` (verified historical snapshot).  
**PR #47:** Already merged, merge commit `c2f6780cff5a249467ccaff487f01960bab6eb83`. Its 11-row table and corrected repository citations are in `docs/publication/ni-ai-tae-evidence-linked-claims-and-citations-2026-10-21.md` on main.

## Extracted PDF content audit

- Title: *Evidence-Bounded Adversarial Evaluation of Implicit Authority Transfer in Agentic AI Governance*.
- Type: **Editorial evidence-review packet**, not the original recovered manuscript and not an OpenReview submission receipt.
- Date: 21 October 2026.
- Authority attributed: Nicholas B. Carty (N.B.C.).
- Adversarial matrix: **5 case rows** (SAL-11 to SAL-15), with **3 PASS and 2 HOLD/PARTIAL**. **SAL-9 consolidated HOLD** is stated.
- Sources: `R1` through `R8`, where R6–R8 pair source and tests. All pertain to the corrected source mapping, rather than nonexistent SAL-specific paths.
- Scholarly bibliography: seven cited entries; venue-level bibliography validation is outstanding.
- **Difference from PR #47:** PR #47 has an **11-row evidence-linked claims table**; this condensed PDF has only five case rows and does **not** embed the complete 11-row appendix.
- **Difference from full manuscript:** Three-page PDF is editorial packet; the reconstructed manuscript is longer and independently versioned.

## Integrity and authority boundary

This hash identifies the **exact PDF bytes received and checked**. Any modification to PDF text, layout, metadata, or embedded appendix requires a **new SHA-256**. This hash is not a code signature, test result, external submission receipt, DOI, validation of scholarly metadata, or evidence of paper acceptance.

This GitHub appendix records the hash as text; **the PDF itself was not uploaded into GitHub**, so reproduction requires obtaining the matching PDF byte-for-byte.

**No new tests were run. No deployment, submission, DOI deposit, new authorization, or merge of this addendum is implied.**

**SAL-9 = HOLD — 3 PASS / 2 HOLD-PARTIAL / 0 FAIL.**

**Disposition:** `PDF HASH VERIFIED -> EVIDENCE ADDENDUM PREPARED -> HOLD MERGE / HOLD SUBMISSION -> STOP`.
