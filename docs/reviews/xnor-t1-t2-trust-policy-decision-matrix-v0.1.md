# NODE XNOR T1/T2 trust-policy decision matrix v0.1

**REVIEW CANDIDATE — NO POLICY APPROVAL / NO KEY ENROLLMENT / NO RUNTIME WIRING / PRODUCTION HOLD**

Purpose: make the decisions needed for a future independently reviewed issuer/key trust policy and cryptographic profile explicit. A choice shown here is a **question**, not an approved default. No live issuer, key fingerprint, provider, algorithm or parser profile is designated.

## Evidence and provenance

- [Authenticated revocation provider contract](xnor-authenticated-revocation-provider-contract-v0.1.md) defines gate-originated binding, immutable signed response, trusted verifier, and fail-closed validation; explicitly lacks trust anchors.
- [Cryptographic verifier design](xnor-cryptographic-verifier-design-v0.1.md) lists required trust-policy and canonicalization decisions; it is design-only.
- [Signed lineage / authority binding](xnor-signed-lineage-actual-authority-binding-v0.1.md) and [PR #91 test-key boundary](https://github.com/heliosfi/Echoauth-core/pull/91) provide **synthetic** evidence, not trusted production issuer enrollment. PR #91 merged `73cf93d393f2f7f4a99a76d8fb89d2759f7b3050`; CI 321 XNOR tests + 10 baseline gate tests PASS, Authority Clarity PASS; independent review pending.
- [T1–T8 draft register, PR #90](https://github.com/heliosfi/Echoauth-core/pull/90) remains open and unapproved.
- [Reviewer evidence index](xnor-independent-reviewer-evidence-index-v0.1.md) links the relevant implementation, review-only tests, and gaps.

## T1 — trusted issuer, key and custody policy

| ID | Explicit decision for human authority | Minimum evidence needed | Current disposition |
| --- | --- | --- | --- |
| T1.1 | Name the accountable trust-policy owner and approval quorum, including separation of issuer and approver roles | Signed or attributable governance decision and change-control record | OPEN — no approver inferred |
| T1.2 | Identify permitted checkpoint issuers, their organizational identities and independently verified source-of-truth | Authenticated issuer provenance, identity verification and approval record | OPEN — no issuer approved |
| T1.3 | Approve **out-of-band** public key fingerprints and key IDs, each bound to issuer and allowed namespace/target/scope | Fingerprint verified independently of the envelope, registry provenance and scope mapping | OPEN — public fixture keys excluded |
| T1.4 | Select custody and signing-key protection requirements, issuance and enrollment procedure | Custody attestation, key-generation/enrollment evidence, separation of duties | OPEN |
| T1.5 | Set key validity windows, rotation overlap, revocation, compromise response, emergency suspension and rollback rules | Lifecycle runbook, negative substitution/expiry/compromise tests | OPEN |
| T1.6 | Define authenticated registry update, replication, outage and rollback semantics | Registry integrity/authenticity, monotonically versioned updates, failure-injection tests | OPEN |
| T1.7 | Decide cross-repository or delegated issuer scope; explicitly deny unapproved transitive trust | Authority mapping and bounded delegation policy with negative cross-scope tests | OPEN |

**Hard exclusions:** A signature produced with a deterministic public test vector, an embedded self-declared public key, a caller-supplied `approved_registry`, or a `claimed_trusted` flag must never become issuer enrollment or authorization. Unknown, missing, conflicting, revoked or expired trust roots fail closed.

## T2 — canonical encoding and cryptographic verification policy

| ID | Explicit decision for human authority | Minimum evidence needed | Current disposition |
| --- | --- | --- | --- |
| T2.1 | Choose the approved schema/version and exact wire format | Versioned normative schema, independent parser conformance tests | OPEN |
| T2.2 | Choose canonical serialization and byte-for-byte signature input | Duplicate-key, Unicode, numeric, ordering, normalization and trailing-byte vectors | OPEN |
| T2.3 | Specify domain separation and anti-cross-protocol replay binding | Signed domain/version/purpose/context specification and replay negatives | OPEN |
| T2.4 | Approve allowed signature and digest suites, algorithm IDs and minimum security levels | Cryptographic review, known-answer vectors, downgrade/algorithm-confusion tests | OPEN — Ed25519 test vector is **not** approval |
| T2.5 | Define envelope size, nesting, field, time and parser resource limits | Fuzzing and adversarial parsing results; fail-closed rejection | OPEN |
| T2.6 | Specify verifier implementation and library provenance, maintenance and failure behavior | Dependency review, deterministic positive/negative vectors, independent code review | OPEN |
| T2.7 | Define signed payload fields required to bind issuer, source, selected authority, delegated grantor, subject, action/resource, target, mapping and checkpoint | Canonical signed-field specification and substitution/mismatch tests | OPEN |
| T2.8 | Define key-registry and verifier policy-version binding and migration/downgrade rules | Signed/pinned policy provenance, version-transition and rollback tests | OPEN |

**Hard exclusions:** Syntactically valid envelopes and successful cryptographic verification are insufficient without independently governed trust roots, exact gate-selected authority mapping, authenticated checkpoint lineage/freshness, independent policy checks and audit. A verifier may report coverage or revocation evidence; it never grants execution permission.

## Decision record template (for future human review only)

| Field | Value |
| --- | --- |
| Decision ID | T1.x or T2.x |
| Proposed option | **UNSPECIFIED** |
| Alternatives and threat analysis | **REQUIRED** |
| Source artifact, version and digest | **REQUIRED** |
| Independent security reviewer and finding | **PENDING** |
| Authorized human approver and approval scope | **PENDING** |
| Approval timestamp / change-control reference | **PENDING** |
| Negative tests and CI evidence | **PENDING** |
| Rollback / expiry conditions | **PENDING** |
| Final disposition | **OPEN / HOLD** |

## Dependency and exit criteria

1. Obtain attributable human governance choices for **all** T1/T2 rows; record rejection/alternatives and scope.
2. Independently verify approved issuer provenance, registry custody and cryptographic profile; do not use public test-key fixture identity as an approved production root.
3. Produce reproducible test-only positive and adversarial vectors under an explicitly approved **test policy**; a test-policy PASS does not authorize production trust.
4. Reconcile T3 authenticated checkpoint source/freshness and T4 exact gate-selected authority mapping, followed by T5–T7 atomicity/audit/entrypoint evidence.
5. Require a separate explicit T8 owner authorization before **any** production key enrollment, runtime gate integration, deployment or activation.

**Current decision:** T1 UNAPPROVED; T2 UNAPPROVED; T3–T7 unresolved; T8 NOT GRANTED. No production modifications proposed.

CAPABILITY != AUTHORITY; MATCH != ACCEPTANCE; PASS != PERMISSION; RETURN != REAUTHORIZATION.
