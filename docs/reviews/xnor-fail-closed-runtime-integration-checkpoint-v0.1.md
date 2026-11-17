# XNOR → EchoAuth fail-closed runtime integration — implementation checkpoint v0.1

**REVIEW CANDIDATE / NOT IMPLEMENTED / PRODUCTION HOLD**

## Verified starting point
EchoAuth PR #57, commit `eebec7df0d519e7ace4a98b6c9e1d0f9235871b8`, Actions run 44144228301: 13 tests PASS (10 existing gate tests, 3 synthetic demonstration tests). Injected test-only revocation forwarding returns REVOKED for direct and delegated cases. The ordinary gate without forwarding still returns AUTHORIZED for the same synthetic external revocation. This is a verified **gap**, not evidence of production readiness.

## Proposed implementation boundary
1. Introduce a typed `TrustedRevocationProvider` protocol at the authorization gate boundary. It must provide an immutable, authenticated, time-bounded, exact-target snapshot for the **resolved authority record**, with mapping version and provenance digest. Caller-provided verdicts, flags, and unsigned envelopes are not trusted.
2. Resolve identity as before. Obtain required revocation coverage **before** accepting authority resolution. The trusted provider must support delegated grantor authority, exact authority record, source, subject, action/resource scope and request time.
3. On missing, stale, ambiguous, untrusted, mismatched or unavailable required coverage: return an audited non-authorizing outcome. Do not silently treat an empty feed as “not revoked.” Specify the canonical outcome/reason mapping before coding.
4. On authenticated effective revocation: pass canonical revocation records to `AuthorityResolutionRequest.revocation_records`, or apply an equivalent independently reviewed gate rejection. Preserve identity → authority → delegation → policy and existing policy denials.
5. No evidence PASS or structural match can yield `AUTHORIZED`; independent authority and policy checks remain necessary. Do not allow evidence to mutate the authority registry, issue credentials, deploy, execute, or authorize continuation.
6. Define a stable request/snapshot consistency point: cache invalidation, effective_at, monotonic checkpoint, revalidation on retries and idempotency; fail closed on uncertain time ordering.
7. Log the provider identity, trust/mapping/checkpoint digests, evidence reason, freshness and final decision without secret material. Bound source failure handling and avoid leakage.

## Open decisions that block production wiring
- Who owns the trust anchor and provider configuration?
- Which authority scopes require external revocation coverage, and how are legacy scopes treated?
- What signed/canonical wire encoding, digest, freshness threshold and trusted clock are approved?
- How is the separately approved XNOR fingerprint → EchoAuth authority-record mapping authenticated and versioned?
- How are conflicting checkpoints, source outages and revocation reinstatement handled?
- Which fail-closed `AuthorizationOutcome` and audit reason are canonical?

## Required implementation tests (not yet written)
- Existing identity/authority/policy success remains authorized only when coverage is trustworthy and no effective revocation exists.
- Effective matching revocation blocks direct and delegated grantor authorization.
- Unavailable/missing/stale/rollback/conflicting source and mapping mismatch all deny/HOLD; never authorize.
- An unrelated target does not revoke a different authority, but does not establish trustworthy coverage for the requested target.
- Untrusted caller-supplied PASS, true authorization flags, malformed evidence, replay and revoked-then-reinstated state cannot bypass the gate.
- Audit evidence and idempotency are stable; no mutation or execution side effects.

## Change controls
This document does not add a provider, alter the production gate, change trust-registry records, merge a PR, or authorize deployment. Next candidate should implement a **test-only fail-closed provider contract** with synthetic fixtures, then obtain independent review before any runtime integration.
