# NODE XNOR → EchoAuth wire-schema reconciliation v0.1

**Disposition: REVIEW HOLD / CONTRACT MISMATCH. No runtime adapter, no production authority.**

## Compared exact draft surfaces
- NODE XNOR draft PR #70: `deep-dives/xnor/revocation/NODE-XNOR-NI-AI-SPINE-EVIDENCE-ONLY-CROSSING-V0.1.md` (`RevocationEvidenceEnvelopeV01`).
- NODE XNOR draft PR #70: `deep-dives/xnor/revocation/NODE-XNOR-REVOCATION-CONTRACT-V0.1-REVIEW-CANDIDATE.md`.
- EchoAuth draft PR #53: `review_candidates/xnor_revocation_synthetic_boundary.py`.
- EchoAuth draft PR #54: `docs/reviews/xnor-echoauth-authority-binding-fail-closed-contract-v0.1.md`.

## Exact incompatibilities
| XNOR envelope field | EchoAuth synthetic classifier | Disposition |
|---|---|---|
| `schema` | `schema` | literal agrees |
| `verdict` | `verdict` | vocabulary agrees; semantics still require authenticated verification |
| `target_fingerprint_digest` | `target_fingerprint_digest` | name agrees, digest profile not selected |
| `revocation_record_digest` | `record_digest` | name mismatch |
| `trusted_checkpoint_digest: string \| null` | `checkpoint_digest: str` | name and nullability mismatch |
| `observed_at` | absent | freshness cannot be inferred from a bare boolean |
| `verifier_version`, `reason_codes` | absent | lost provenance/reason semantics |
| `evidence_source: synthetic-review` | `synthetic_only: bool` | source claim is not source authentication |
| four always-false authority/registry/execution/continuation flags | three false flags; continuation absent | non-authorization contract incomplete |
| absent authority-record ID | `target_authority_record_id` | **no canonical mapping established** |
| absent signature/checkpoint/freshness/binding booleans | four booleans supplied | **not trustworthy attestations** |

## Critical semantic distinction
XNOR `PASS` indicates bounded verification of a **revocation artifact**, not that the target is unrevoked or ACTIVE. Never map PASS to `AuthorizationOutcome.AUTHORIZED`. If authenticated effective revocation matches an authority record, independent EchoAuth authority resolution should block authorization. Invalid, stale, missing, conflicting, or untrusted evidence cannot become implicit permission.

## Recommendation for next contract revision
1. Keep the XNOR evidence-only envelope as the producer-side proposal, without inventing an EchoAuth-specific authority ID inside it.
2. Define a separately authenticated mapping object: exact target fingerprint digest, namespace, role, tier, scope, source identity, EchoAuth `authority_record_id`, `authority_source_id`, `subject_id`, approved mapping version/digest and provenance.
3. Consumer recomputes trust/freshness/target/checkpoint decisions from verified source evidence; never accept caller-set booleans as authoritative.
4. Define a versioned canonical wire schema and reason-code precedence; select timestamp and digest algorithms, checkpoint nullability and trust policy before any implementation.
5. Add continuation_authorized=false to the consumer's review contract and keep all authorization flags false-only.
6. Separate evidence verdict (PASS/FAIL/HOLD) from operational revocation state (effective, pending, expired-artifact, conflict) and EchoAuth permission outcome.
7. Do not implement a field-name shim and call it integration. Require signed provenance and negative tests at each boundary.

## Review blockers
No authenticated source, trust-anchor selection, real mapping registry, timestamp/freshness policy, wire encoding, signed checkpoint or consumer runtime propagation has been verified. PR #53 tests are synthetic and do not close these gaps. No merge, registry write, key activation, execution or production promotion is authorized.
