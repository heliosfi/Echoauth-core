# PR #60 independent-boundary review: caller-selected authority binding gap

**REVIEW HOLD — synthetic tests PASS, production enforcement NOT established.**

## Evidence
- PR #59 synthetic provider: 13 tests PASS in run 44145553420.
- PR #60 isolated gate boundary: 17 tests PASS (10 inherited gate tests and 7 boundary tests) in run 44146594855.
- PR #60 implementation takes `authority_record_id` and `target_digest` as separate caller arguments, then invokes the ordinary gate with a distinct `AuthorizationRequest`.

## Unresolved security invariant
A successful provider check is not proven to refer to the *same authority actually selected by the gate* for this request. The caller can supply a different, otherwise clear authority record and target digest. The wrapper does not derive the expected binding from a trusted authority resolution, nor does it compare the gate's resolved authority to the snapshot. Therefore current tests must not be described as complete end-to-end revocation enforcement.

## Required next implementation
1. Bind revocation coverage to the exact authority selected during resolution (including delegated grantor and action/resource/subject/scope), using independently authenticated mapping.
2. Ensure no time-of-check/time-of-use gap: same trusted snapshot/checkpoint must govern the decision, including retries and idempotency.
3. Make the gate require coverage for relevant authority scopes rather than relying on an optional caller wrapper.
4. Define typed fail-closed errors for provider outage, malformed response, missing mapping, unknown state, checkpoint rollback and stale coverage. No caller-provided PASS or flags may stand in for cryptographic evidence.
5. Add a **negative mismatch test** in which the provider clears authority A but the gate resolves authority B; authorization must not proceed.
6. Add negative delegated-grantor and multi-authority resolution cases, plus evidence-to-audit traceability.
7. Obtain security review of source trust, mapping, canonical bytes, and freshness before any production gate modification.

## Boundaries
No production wiring, no real cryptographic validation, no trust registry mutation, no deployment, no merge authorization. PR #60 is a review-only synthetic demonstration dependent on PR #59.
