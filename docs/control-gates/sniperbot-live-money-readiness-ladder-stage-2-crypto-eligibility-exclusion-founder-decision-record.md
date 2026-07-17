# SniperBot Live-Money Readiness Ladder Stage 2 Crypto Eligibility / Exclusion Founder-Decision Record

## Status and Boundary

Artifact type: **Founder-Decision Record**

Subject: **Crypto Eligibility / Exclusion**

Stage: **SniperBot Live-Money Readiness Ladder - Stage 2**

Repository: `heliosfi/Echoauth-core`

Starting checkpoint:
`4a19be43f86d9714f1ad4d5f8066d8e45288d8aa`.

Governing contract-definition review:
`docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-crypto-eligibility-exclusion-contract-definition-review.md`.

The complete elicitation and scope review identified 72 independent founder
decisions: 52 Core Crypto Eligibility / Exclusion decisions, 20
Caller-Supplied Context decisions, and zero Future Stage 2 decisions. The
scope review found no required narrowing. This record resolves all 72 in their
established dependency order.

This record is documentation-only, governance-only, contract-only,
non-runtime, non-integration, non-execution, and non-authorizing. It does not
create or authorize a schema, Python API, implementation, tests, evidence
review, evidence acceptance, package export, workflow, dependency,
registration, runtime hook, integration surface, or successor lane.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized. EchoAuth
remains the sole permission authority.

## Decision Inventory

| Classification | Decisions | Count |
| --- | --- | ---: |
| Core Crypto Eligibility / Exclusion | 01-16, 35, 38-72 | 52 |
| Caller-Supplied Context | 17-34, 36-37 | 20 |
| Future Stage 2 | none | 0 |
| Total | 01-72 | 72 |

Caller-Supplied Context decisions settle whether external descriptive facts
enter this bounded request. They do not govern the underlying domain.
Caller-supplied context does not authorize operational behavior, including
discovery, retrieval, verification, access, calculation, selection, routing,
transaction, or execution.

## Founder Decisions

### Decision 01 - Classification Subject (Core)

**Final founder decision:** The classifier accepts one opaque, caller-supplied
`crypto_reference` for one already identified Crypto subject. The reference
may designate a token, coin, pair, or other normalized instrument in the
caller's system, but this contract does not distinguish or determine which.

**Rationale:** One opaque identity bounds the decision without creating a
token registry, pair parser, asset resolver, or supported-asset universe.

**Downstream impact:** Every request and decision carries exactly the same
reference value; no asset-kind branch exists.

**Implementation consequence:** Require a non-empty, non-whitespace `str` and
preserve it byte-for-byte as a Python string without parsing or normalization.

### Decision 02 - Crypto Identity Assertion (Core)

**Final founder decision:** Crypto identity is asserted only by an optional
closed `CryptoLaneConfirmation` value. It is never inferred from the subject
reference, package path, generic context, venue, chain, or any other fact.

**Rationale:** Explicit lane confirmation prevents the classifier from
performing identity recognition while retaining a governed missing state.

**Downstream impact:** Missing, contradictory, and not-confirmed lane states
receive dedicated fail-closed mappings.

**Implementation consequence:** The request field is
`crypto_lane_confirmation: CryptoLaneConfirmation | None = None`; no identity
lookup or instrument-kind type is authorized.

### Decision 03 - Eligibility Meaning (Core)

**Final founder decision:** `ELIGIBLE` means only that caller-supplied facts
support continued governed Stage 2 consideration of the referenced Crypto
subject.

**Rationale:** Eligibility must remain descriptive and cannot become asset
approval or permission.

**Downstream impact:** `ELIGIBLE` does not mean safe, suitable, supported,
tradeable, routable, transferable, executable, or live-money ready.

**Implementation consequence:** Only the exact final eligible branch may emit
`ELIGIBLE / CRYPTO_ELIGIBLE / NONE`.

### Decision 04 - Exclusion Meaning (Core)

**Final founder decision:** `EXCLUDED` records a caller-supplied descriptive
exclusion posture and is terminal only within this pure classifier.

**Rationale:** Exclusion evidence must not become a runtime denylist, filter,
order rejection, or enforcement mechanism.

**Downstream impact:** Absence of exclusion never implies eligibility or
permission.

**Implementation consequence:** The ordinary excluded branch emits
`EXCLUDED / CRYPTO_EXCLUDED / NONE` and performs no external action.

### Decision 05 - Restriction Meaning (Core)

**Final founder decision:** `RESTRICTED` is a separate caller-supplied
descriptive posture requiring bounded human review.

**Rationale:** Restriction is distinct from exclusion and must not be modeled
as a runtime market, account, transfer, or execution control.

**Downstream impact:** Restriction pauses continued consideration without
granting or denying operative authority.

**Implementation consequence:** The ordinary restricted branch emits
`RESTRICTED / CRYPTO_RESTRICTED / HUMAN_REVIEW`.

### Decision 06 - Deferral / No-Action Separation (Core)

**Final founder decision:** The accepted Crypto Deferral / No-Action lane is
fully separate and unchanged. No Deferral field, object, enum, reason,
decision, reference, import, evaluator call, or precedence is admitted here.

**Rationale:** Deferral answers a different governed question and cannot be
converted into eligibility.

**Downstream impact:** Neither lane invokes, chains to, overrides, or derives
authority from the other.

**Implementation consequence:** The future eligibility module must not import
`sniperbot.crypto.deferral_decision`, and `src/sniperbot/crypto/__init__.py`
must remain unchanged.

### Decision 07 - Mandatory Non-Authorizing Interpretations (Core)

**Final founder decision:** Every result expressly prohibits selection,
recommendation, approval, permission, allowlisting, blocklisting, market or
chain access, wallet or custody access, transfer, routing, order creation,
execution, deployment, live-money capability, and Stage 3 entry.

**Rationale:** A descriptive classifier must not acquire operative meaning by
label, downstream assumption, or omission.

**Downstream impact:** No outcome or action can be interpreted as an EchoAuth
grant or operational instruction.

**Implementation consequence:** No permission-bearing, executable, endpoint,
credential, address, command, strategy, order, or transaction field exists.

### Decision 08 - Exact Request Structure and Field Order (Core)

**Final founder decision:** The future frozen `CryptoEligibilityRequest` has
exactly these fields in order:

| Order | Field | Exact Python type | Default |
| ---: | --- | --- | --- |
| 1 | `crypto_reference` | `str` | none |
| 2 | `eligibility_evidence_present` | `bool` | none |
| 3 | `eligibility_evidence_current` | `bool` | none |
| 4 | `eligibility_evidence_sufficient` | `bool` | none |
| 5 | `eligibility_evidence_contradictory` | `bool` | none |
| 6 | `crypto_eligible` | `bool` | none |
| 7 | `crypto_excluded` | `bool` | none |
| 8 | `crypto_restricted` | `bool` | none |
| 9 | `eligibility_evidence_reference` | `str` | none |
| 10 | `correlation_reference` | `str` | none |
| 11 | `crypto_lane_confirmation` | `CryptoLaneConfirmation | None` | `None` |
| 12 | `generic_asset_class_context` | `GenericAssetClassContext | None` | `None` |
| 13 | `authority_evidence` | `AuthorityEvidence | None` | `None` |

**Rationale:** This is the smallest structure that carries the selected core
facts, explicit lane state, optional generic context, and optional authority
context without importing any operational domain.

**Downstream impact:** No additional context, upstream decision, market,
chain, account, risk, or runtime property is allowed.

**Implementation consequence:** Schema, dataclass annotations, field order,
constructor behavior, and parity tests must match this table exactly.

### Decision 09 - Requiredness (Core)

**Final founder decision:** The first ten request fields are required and have
no default. Only the final three fields have the exact default `None`. No
request or nested field has a default factory.

**Rationale:** Required caller assertions avoid hidden construction while the
three explicit absence states preserve bounded optionality.

**Downstream impact:** Missing required keywords are structural errors; lane
absence is a governed decision state; generic and authority absence simply
skip their contextual checks.

**Implementation consequence:** Dataclass metadata and direct tests must prove
the exact defaults and absence of every default factory.

### Decision 10 - Exact Runtime Types and Strict Booleans (Core)

**Final founder decision:** The seven request Boolean fields and every nested
Boolean require `type(value) is bool`. References require `type(value) is str`.
Enums and nested objects require their exact declared runtime types.

**Rationale:** Coercion would make the contract ambiguous and expand the
accepted state space.

**Downstream impact:** Integers, truthy or falsey substitutes, raw enum strings,
subclasses, dictionaries, and lookalikes are invalid.

**Implementation consequence:** Enforce exact types in frozen dataclass
validation and test each strict boundary directly.

### Decision 11 - Enum and Raw-String Boundary (Core)

**Final founder decision:** Python APIs accept only exact enum members; they do
not convert raw strings. JSON uses the exact corresponding closed strings at
the schema boundary.

**Rationale:** Schema and Python can remain equivalent without a hidden parser
or coercion path.

**Downstream impact:** Aliases, case folding, `UNKNOWN`, free text, and cross-
lane enum instances are rejected.

**Implementation consequence:** Enum constructors retain their normal
`ValueError` behavior, while dataclass fields reject raw strings with
`TypeError`.

### Decision 12 - Extra, Alternate, and Subclass Representations (Core)

**Final founder decision:** Unknown keywords, extra fields, positional
`create_request` arguments, dictionaries, partial objects, alternate objects,
subclasses, and lookalikes are rejected.

**Rationale:** One exact representation prevents accidental cross-lane and
duck-typed authority.

**Downstream impact:** Stock-, Options-, Asset-Class-, and Deferral-shaped
objects have no standing in this request.

**Implementation consequence:** Use exact-type checks and normal constructor
`TypeError` boundaries; provide no adapter, parser, deserializer, or alias.

### Decision 13 - Opaque Reference Contract (Core)

**Final founder decision:** `crypto_reference`,
`eligibility_evidence_reference`, `correlation_reference`, generic
`context_reference`, and authority `evidence_reference` are mandatory within
their containing object, non-empty, non-whitespace-only, opaque, immutable,
and preserved exactly.

**Rationale:** References provide traceability without retrieval or semantic
interpretation.

**Downstream impact:** Whitespace surrounding meaningful content is preserved;
no reference is stripped, normalized, parsed, dereferenced, or looked up.

**Implementation consequence:** Validate with an exact-string and
non-whitespace check and return the three request-level references unchanged
in every decision.

### Decision 14 - Omission, Null, Defaults, and Empty Objects (Core)

**Final founder decision:** Omitted and explicit
`crypto_lane_confirmation=None` both mean missing confirmation. Generic
context and authority are optional only by omission through `create_request`;
explicit `None` is rejected there. Their dataclass defaults remain `None` to
represent already-constructed absence. JSON null is allowed only for lane
confirmation. Empty objects and empty or whitespace-only references are
invalid.

**Rationale:** The lane has an explicit governed missing state, while nested
contexts must never masquerade as supplied evidence.

**Downstream impact:** Omission/null parity is exact and independently tested.

**Implementation consequence:** `create_request` must distinguish omitted
generic/authority keywords from explicitly supplied `None`; no default object
or default factory may be created.

### Decision 15 - Instrument Decomposition and Category Facts (Core)

**Final founder decision:** Separate base/quote references and token, coin,
native, wrapped, governance, utility, security, stablecoin, or other category
facts are prohibited from this request.

**Rationale:** The opaque subject is sufficient; decomposition would turn this
lane into identity, taxonomy, or registry governance.

**Downstream impact:** A pair may be named only inside the caller's opaque
reference and receives no special behavior.

**Implementation consequence:** No instrument-kind enum, parser, category
field, base/quote field, or identity helper is authorized.

### Decision 16 - Identity Failure States (Core)

**Final founder decision:** Ambiguous, conflicting, stale, unsupported, or
absent instrument identity is not represented or inferred. The only governed
lane-identity states are missing, `NOT_CONFIRMED`, `CONTRADICTORY`, and
`CONFIRMED`.

**Rationale:** The classifier cannot validate the meaning of an opaque subject.

**Downstream impact:** Callers must resolve instrument identity outside this
lane before asserting confirmation.

**Implementation consequence:** Only the three lane failure reasons and one
continue state exist; no identity-status reason or lookup is added.

### Decision 17 - Venue or Exchange Facts (Caller-Supplied Context)

**Final founder decision:** Venue and exchange references or facts are
prohibited from the bounded request.

**Rationale:** Venue eligibility is a separate operational/access concern and
is unnecessary to classify supplied Crypto posture.

**Downstream impact:** Caller-supplied venue facts cannot alter this result or
convey support, access, or routing authority.

**Implementation consequence:** Add no venue, exchange, broker-venue, or
account-venue field, enum, reason, branch, or reference.

### Decision 18 - Venue Categories, Compatibility, and Failures (Caller-Supplied Context)

**Final founder decision:** Centralized, decentralized, broker, and other venue
categories, compatibility, availability, integrity, and their failure states
are prohibited and not classified here.

**Rationale:** Accepting such states would govern venue policy and access
rather than Crypto eligibility posture.

**Downstream impact:** Unsupported, ambiguous, contradictory, stale, or out-
of-scope venue assertions have no input representation.

**Implementation consequence:** No exchange discovery, credentials, quotes,
routing, order behavior, or venue-context subprecedence is permitted.

### Decision 19 - Blockchain or Network Facts (Caller-Supplied Context)

**Final founder decision:** Chain, network, node, explorer, RPC, address,
transaction, finality, fork, and congestion facts are prohibited.

**Rationale:** These facts belong to chain state, operational access, or risk,
not this descriptive posture classifier.

**Downstream impact:** Network compatibility or condition cannot establish or
defeat Crypto eligibility here.

**Implementation consequence:** Add no network reference, status, lookup,
analysis, validation, or reason code.

### Decision 20 - Bridge, Wrapped-Asset, and Network-Condition Facts (Caller-Supplied Context)

**Final founder decision:** Bridge exposure, wrapped-asset relationships, chain
mismatch, and network-condition facts are prohibited.

**Rationale:** The opaque subject boundary avoids modeling protocol topology or
transaction paths.

**Downstream impact:** This lane makes no bridge, wrapper, chain, or path
claim.

**Implementation consequence:** No bridge/wrapper context, subprecedence,
oracle, explorer, or transaction handling is authorized.

### Decision 21 - Stablecoin Classification (Caller-Supplied Context)

**Final founder decision:** Stablecoin classification is prohibited from the
request.

**Rationale:** Stablecoin taxonomy is not required to classify the supplied
core posture and could imply asset approval.

**Downstream impact:** A stablecoin may be referenced opaquely but receives no
special classification or behavior.

**Implementation consequence:** No stablecoin Boolean, enum, reference,
outcome, reason, or branch is authorized.

### Decision 22 - Stablecoin Evidence (Caller-Supplied Context)

**Final founder decision:** Peg, reserve, redemption, issuer, collateral,
venue-support, and depegging evidence is prohibited.

**Rationale:** Those domains require separate evidence governance and cannot
be interpreted safely by this lane.

**Downstream impact:** Unknown, contradictory, stale, or insufficient
stablecoin facts do not enter this state space.

**Implementation consequence:** No stablecoin research, rail, transfer path,
selection rule, or evidence mapping is permitted.

### Decision 23 - Wallet and Custody Inclusion (Caller-Supplied Context)

**Final founder decision:** Wallet and custody context is prohibited.

**Rationale:** Wallet or custody compatibility could be mistaken for access or
transfer authority.

**Downstream impact:** The classifier says nothing about wallets, custodians,
accounts, addresses, or ownership.

**Implementation consequence:** Add no wallet, custody, address, account,
compatibility, or permission field.

### Decision 24 - Wallet and Custody Fact Boundary (Caller-Supplied Context)

**Final founder decision:** Address control, signing control, custody model,
deposit, withdrawal, transfer, and account-ownership facts are prohibited.

**Rationale:** These are sensitive operational facts outside a pure
eligibility/exclusion classification.

**Downstream impact:** Caller-supplied context cannot authorize custody access,
signing, deposits, withdrawals, or transfers.

**Implementation consequence:** No secret, key, seed phrase, address
validation, signing, custody, or transfer behavior may exist.

### Decision 25 - DeFi Exposure (Caller-Supplied Context)

**Final founder decision:** DeFi protocol, pool, staking, lending, borrowing,
liquidity-provider, and approval exposure facts are prohibited.

**Rationale:** Protocol exposure belongs to separately governed risk and
interaction subjects.

**Downstream impact:** No DeFi posture can determine the result in this lane.

**Implementation consequence:** Add no DeFi enum, object, reference, reason,
subprecedence, protocol call, or approval behavior.

### Decision 26 - Smart-Contract Exposure (Caller-Supplied Context)

**Final founder decision:** Smart-contract, oracle, bridge-contract, and
protocol-contract exposure facts are prohibited.

**Rationale:** Contract interpretation and interaction exceed the bounded
descriptive subject.

**Downstream impact:** Unsupported or unresolved contract exposure has no
representation here.

**Implementation consequence:** No ABI, address, RPC, oracle, contract call,
approval, signing, deployment, or execution behavior is authorized.

### Decision 27 - Liquidity, Volume, Spread, and Slippage Facts (Caller-Supplied Context)

**Final founder decision:** Liquidity, volume, spread, slippage, order-book,
and venue-integrity facts, raw values, scores, and postures are prohibited.

**Rationale:** Market-condition interpretation would create market-data and
screening behavior.

**Downstream impact:** No supplied or retrieved market metric can alter the
decision.

**Implementation consequence:** Add no numeric market field, threshold,
calculation, quote, ranking, or market-data import.

### Decision 28 - Volatility Facts (Caller-Supplied Context)

**Final founder decision:** Volatility values, classifications, scores, and
references are prohibited.

**Rationale:** Volatility belongs to separately governed risk or market-data
subjects.

**Downstream impact:** The classifier neither measures nor interprets price
movement.

**Implementation consequence:** No price history, clock, statistic, threshold,
volatility reason, or risk behavior is authorized.

### Decision 29 - Market-Condition Currentness and Computation (Caller-Supplied Context)

**Final founder decision:** Market-condition currentness is not accepted. The
only currentness fact is the caller-supplied Boolean for the bounded
eligibility evidence as a whole.

**Rationale:** One evidence-quality assertion avoids clocks, freshness rules,
data retrieval, and calculation.

**Downstream impact:** `eligibility_evidence_current` does not attest to any
specific market datum and cannot be independently verified here.

**Implementation consequence:** No clock, timestamp, market snapshot, score,
calculation, screening, pricing, or ranking is permitted.

### Decision 30 - Tokenomics, Supply, Issuer, Unlock, Mint, and Burn Facts (Caller-Supplied Context)

**Final founder decision:** Market cap, supply, concentration, issuer,
tokenomics, vesting, unlock, mint, burn, governance, and protocol-change facts
are prohibited.

**Rationale:** These facts require research and domain governance beyond the
opaque subject posture.

**Downstream impact:** No tokenomics claim can establish eligibility,
exclusion, or restriction here.

**Implementation consequence:** Add no tokenomics object, value, reference,
score, forecast, reason, or retrieval behavior.

### Decision 31 - Jurisdictional Facts (Caller-Supplied Context)

**Final founder decision:** Jurisdiction and location facts are prohibited.

**Rationale:** This classifier cannot perform legal, geographic, account, or
venue interpretation.

**Downstream impact:** No jurisdictional assertion is converted into approval,
exclusion, restriction, or advice.

**Implementation consequence:** Add no country, region, residency, location,
legal-status field, or jurisdiction branch.

### Decision 32 - Regulatory Facts (Caller-Supplied Context)

**Final founder decision:** Regulatory status, classification, registration,
licensing, and compliance facts are prohibited.

**Rationale:** Regulatory interpretation requires separate authority and
cannot be embedded in a pure posture classifier.

**Downstream impact:** The result is not legal or regulatory advice.

**Implementation consequence:** Add no regulatory field, rule engine, lookup,
screening, analysis, or compliance mapping.

### Decision 33 - Sanctions Facts (Caller-Supplied Context)

**Final founder decision:** Sanctions status, screening results, lists, and
references are prohibited.

**Rationale:** Sanctions screening is a distinct high-stakes compliance
subject and is not authorized here.

**Downstream impact:** The classifier neither clears nor rejects any subject on
sanctions grounds.

**Implementation consequence:** No list access, name/address screening,
networking, database, sanctions reason, or compliance claim is permitted.

### Decision 34 - Platform-Policy Facts (Caller-Supplied Context)

**Final founder decision:** Listing policy, terms of service, platform policy,
venue policy, and support policy facts are prohibited.

**Rationale:** Platform policy is external and potentially operational; this
lane cannot interpret or enforce it.

**Downstream impact:** A platform-policy assertion cannot create compatibility,
account permission, or execution authority.

**Implementation consequence:** Add no policy field, retrieval, evaluation,
reason, or enforcement behavior.

### Decision 35 - Policy and Permission Conflicts (Core)

**Final founder decision:** Because venue, jurisdiction, regulatory, sanctions,
platform-policy, and account-permission facts are prohibited, no cross-domain
policy conflict is constructible. The only governed conflicts are the exact
evidence, posture, lane, generic-context, and authority conditions recorded
below.

**Rationale:** The conflict model must match the actual typed request rather
than imply absent operational domains.

**Downstream impact:** No hidden policy priority or legal inference exists.

**Implementation consequence:** Do not create policy collision branches or
catch-all policy reasons.

### Decision 36 - Account-Permission Facts (Caller-Supplied Context)

**Final founder decision:** Account, trading, product, deposit, withdrawal, and
transfer permission facts are prohibited.

**Rationale:** Account permissions are operative access facts and cannot be
treated as Crypto eligibility.

**Downstream impact:** The result neither discovers nor grants an account
capability.

**Implementation consequence:** Add no account object, credential, balance,
permission lookup, exchange connection, broker call, or access reason.

### Decision 37 - Margin, Collateral, Leverage, and Liquidation Facts (Caller-Supplied Context)

**Final founder decision:** Margin, collateral, borrowing, leverage, buying
power, liquidation, and position facts are prohibited.

**Rationale:** These belong to risk, sizing, account, or execution governance.

**Downstream impact:** The classifier cannot select leverage or control a
position.

**Implementation consequence:** Add no numeric exposure, balance, margin,
collateral, liquidation, sizing, risk, or account behavior.

### Decision 38 - Evidence-Quality Dimensions (Core)

**Final founder decision:** The exact evidence dimensions are presence,
currentness, sufficiency, and contradiction.

**Rationale:** These four caller assertions are sufficient for the bounded
fail-closed evidence model without scoring or external verification.

**Downstream impact:** Validity, ambiguity, and scope apply only inside the
separately typed generic and authority contexts.

**Implementation consequence:** Use exactly the four request fields
`eligibility_evidence_present`, `eligibility_evidence_current`,
`eligibility_evidence_sufficient`, and
`eligibility_evidence_contradictory`.

### Decision 39 - Evidence-Quality Representation (Core)

**Final founder decision:** All four eligibility-evidence dimensions are
required strict Booleans with no defaults.

**Rationale:** A closed Cartesian state space supports deterministic and
exhaustive evidence.

**Downstream impact:** Missing, null, enum, numeric, string, and truthy/falsy
representations are invalid rather than unknown.

**Implementation consequence:** Enforce exact `bool` and cover all 16
combinations in the independent oracle.

### Decision 40 - Contradictory Evidence (Core)

**Final founder decision:** Eligibility-evidence contradiction is supplied only
by `eligibility_evidence_contradictory`. The evaluator additionally recognizes
only the exact posture conflicts and three evidence-quality undefined
predicates selected below; it infers no other contradiction.

**Rationale:** Explicit triggers prevent open-ended semantic inference.

**Downstream impact:** Evidence contradiction has the highest global
precedence and cannot be repaired by another fact.

**Implementation consequence:** Map it to `REVIEW_REQUIRED /
CRYPTO_ELIGIBILITY_EVIDENCE_CONTRADICTORY / HUMAN_REVIEW`.

### Decision 41 - Evidence References (Core)

**Final founder decision:** Every request requires
`eligibility_evidence_reference` and `correlation_reference`; every supplied
generic or authority object requires its own exact reference.

**Rationale:** Traceability remains available even when evidence is asserted
absent, stale, insufficient, or contradictory.

**Downstream impact:** Request-level evidence and correlation references are
returned in every decision; nested references remain in their frozen input
objects and are not returned or dereferenced.

**Implementation consequence:** Validate all reference strings and prove exact
preservation and non-mutation.

### Decision 42 - Missing, Empty, Duplicate, Mismatched, and Omitted Evidence (Core)

**Final founder decision:** Missing required references are `TypeError` through
construction; empty or whitespace-only references are `ValueError`.
Duplicate textual values are allowed because references are opaque. The
classifier does not compare or infer mismatches. Omitted evidence is expressed
by `eligibility_evidence_present=False`, not by omitting required fields.

**Rationale:** Structural validity and evidence posture are distinct.

**Downstream impact:** No hidden reference-consistency rule or evidence lookup
exists.

**Implementation consequence:** Validate shape only; do not compare, dedupe,
resolve, or repair references.

### Decision 43 - Posture Representation (Core)

**Final founder decision:** Eligibility, exclusion, and restriction are exactly
the three required strict Booleans `crypto_eligible`, `crypto_excluded`, and
`crypto_restricted`.

**Rationale:** Independent Booleans make collisions constructible and explicit
without a lossy single posture enum.

**Downstream impact:** No posture is omitted or inferred from another.

**Implementation consequence:** Enforce exact `bool`; add no posture enum,
alias, or free-text state.

### Decision 44 - Constructible Posture Combinations (Core)

**Final founder decision:** All eight Boolean posture combinations are valid
typed inputs. All false reaches the final unresolved branch after higher
checks. Eligible/excluded and eligible/restricted are conflicts. Excluded plus
restricted without eligible uses exclusion. All three uses the
eligible/excluded conflict.

**Rationale:** The evaluator must totalize caller-supplied collisions rather
than reject structurally valid facts.

**Downstream impact:** Exclusion suppresses restriction when eligibility is
false; eligibility never overrides exclusion or restriction.

**Implementation consequence:** Test all eight combinations and every
higher/lower collision.

### Decision 45 - Posture Evidence Requirements (Core)

**Final founder decision:** Every posture uses the one required
`eligibility_evidence_reference`; no posture-specific or domain-specific
reference exists.

**Rationale:** One opaque evidence record is sufficient and prevents request
expansion.

**Downstream impact:** Exclusion and restriction may be asserted without
eligibility, subject to global precedence.

**Implementation consequence:** Add no per-posture evidence object, reference,
or matching rule.

### Decision 46 - Crypto-Lane Confirmation (Core)

**Final founder decision:** The exact `CryptoLaneConfirmation` vocabulary is
`CONFIRMED`, `NOT_CONFIRMED`, and `CONTRADICTORY`; `None` represents missing.

**Rationale:** The four lane states are closed, caller supplied, and require no
identity inference.

**Downstream impact:** Missing, contradictory, and not-confirmed each map to a
dedicated governance review reason; confirmed continues.

**Implementation consequence:** Use the exact enum and allow omission or
explicit `None` only for this request field.

### Decision 47 - Generic Asset-Class Context (Core)

**Final founder decision:** Generic Asset-Class context is optional by omission
and contextual only. The frozen `GenericAssetClassContext` fields, in order,
are `asset_class: AssetClass`, `validity: Validity`, `current: bool`,
`contradictory: bool`, `in_scope: bool`, and `context_reference: str`. All six
are required and have no defaults or default factories.

**Rationale:** A closed caller assertion can detect a Crypto-lane mismatch
without invoking the generic evaluator.

**Downstream impact:** Absent or fully valid Crypto context continues but never
establishes eligibility. Supplied failures follow the selected subprecedence.

**Implementation consequence:** `AssetClass` is exactly `STOCK`, `OPTIONS`,
`CRYPTO`; `Validity` is exactly `VALID`, `INVALID`, `AMBIGUOUS`; all fields use
strict types and exact reference rules.

### Decision 48 - Generic Reference and Invocation Boundary (Core)

**Final founder decision:** Only the generic context's opaque
`context_reference` is allowed. Generic decision objects, outcomes, reasons,
actions, evaluator calls, imports, and orchestration are prohibited.

**Rationale:** Context is descriptive input, not inherited authority or an
integration surface.

**Downstream impact:** The eligibility evaluator remains independently pure and
cannot consume a generic decision.

**Implementation consequence:** Exact generic subprecedence is contradictory,
ambiguous, invalid, non-`CRYPTO`, stale, then out of scope; no external call is
permitted.

### Decision 49 - Authority Optionality (Core)

**Final founder decision:** Authority evidence is optional only by omission
through `create_request`. Explicit `authority_evidence=None` is rejected.
Absent or fully valid supplied evidence permits evaluation to continue but
never grants eligibility or permission.

**Rationale:** Authority context can fail closed without becoming a required
grant or creating a null-shaped pseudo-object.

**Downstream impact:** No authority evidence means no authority branch; it does
not mean authorized.

**Implementation consequence:** Keep the dataclass default `None`, distinguish
omission in `create_request`, and create no default authority object.

### Decision 50 - Authority Structure (Core)

**Final founder decision:** The frozen `AuthorityEvidence` fields, in order,
are `validity: Validity`, `current: bool`, `revoked: bool`,
`contradictory: bool`, `in_scope: bool`, and `evidence_reference: str`.
All six are required, have no defaults or default factories, and the four
Boolean fields require exact `bool`.

**Rationale:** This independently selected closed shape represents supplied
EchoAuth posture without carrying an authority grant.

**Downstream impact:** Authority evidence is immutable, opaque, and
non-operative.

**Implementation consequence:** Require exact `Validity`, strict Booleans, an
exact non-empty reference, and exact dataclass type.

### Decision 51 - Alternate Authority Representations (Core)

**Final founder decision:** Dictionaries, partial objects, subclasses,
lookalikes, Stock-, Options-, Asset-Class-, and Deferral-shaped objects are
rejected. In particular, alternate `currentness`, `revocation`, or `scope`
fields are invalid.

**Rationale:** Similar shape cannot silently acquire authority meaning.

**Downstream impact:** There is one Crypto-specific representation and no
adapter or structural typing.

**Implementation consequence:** Enforce `type(value) is AuthorityEvidence`
and direct evidence tests for every alternate representation.

### Decision 52 - Authority Failure Set and Mappings (Core)

**Final founder decision:** Authority failures are contradictory, ambiguous,
invalid, revoked, stale, and out of scope. Contradictory, ambiguous, and
invalid map to `AUTHORITY_EVIDENCE_INVALID`; revoked, stale, and out of scope
map to their dedicated reasons. Every failure emits `REVIEW_REQUIRED` and
`GOVERNANCE_REVIEW`.

**Rationale:** The set covers the exact typed fields without inventing
permission semantics.

**Downstream impact:** No failure can be repaired by a lower condition and no
valid state creates authority.

**Implementation consequence:** Implement and directly test all six states and
exact outcome/reason/action mappings.

### Decision 53 - Authority Subprecedence and Global Position (Core)

**Final founder decision:** Authority subprecedence is contradictory,
ambiguous, invalid, revoked, stale, then out of scope. Authority is global
precedence step 11, after ordinary exclusion/restriction and before ordinary
evidence deficiencies.

**Rationale:** Contradiction and validity failures win within authority, while
terminal supplied postures remain higher in the global classifier.

**Downstream impact:** All 14 logically possible pairwise authority collision
witnesses have deterministic winners.

**Implementation consequence:** Provide a private pure authority classifier and
direct collision evidence; no authority invocation or repair occurs.

### Decision 54 - Closed Outcome Set (Core)

**Final founder decision:** `Outcome` contains exactly `ELIGIBLE`, `EXCLUDED`,
`RESTRICTED`, and `REVIEW_REQUIRED`.

**Rationale:** These four values cover every selected terminal descriptive
posture and the fail-closed state.

**Downstream impact:** Deferred, no-action, allow, deny, approved, unsupported,
unknown, buy, sell, route, and execute outcomes are prohibited.

**Implementation consequence:** Use a four-value string enum with no alias or
coercion; `REVIEW_REQUIRED` is the fail-closed outcome.

### Decision 55 - Closed Reason Set (Core)

**Final founder decision:** `ReasonCode` contains exactly these 23 values in
this order:

1. `CRYPTO_ELIGIBLE`
2. `CRYPTO_EXCLUDED`
3. `CRYPTO_RESTRICTED`
4. `CRYPTO_ELIGIBILITY_EVIDENCE_MISSING`
5. `CRYPTO_ELIGIBILITY_EVIDENCE_STALE`
6. `CRYPTO_ELIGIBILITY_EVIDENCE_INSUFFICIENT`
7. `CRYPTO_ELIGIBILITY_EVIDENCE_CONTRADICTORY`
8. `CRYPTO_ELIGIBLE_EXCLUDED_CONFLICT`
9. `CRYPTO_ELIGIBLE_RESTRICTED_CONFLICT`
10. `CRYPTO_LANE_CONFIRMATION_MISSING`
11. `CRYPTO_LANE_NOT_CONFIRMED`
12. `CRYPTO_LANE_CONTRADICTORY`
13. `GENERIC_ASSET_CLASS_CONTEXT_INVALID`
14. `GENERIC_ASSET_CLASS_CONTEXT_STALE`
15. `GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY`
16. `GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE`
17. `GENERIC_ASSET_CLASS_NOT_CRYPTO`
18. `AUTHORITY_EVIDENCE_INVALID`
19. `AUTHORITY_EVIDENCE_STALE`
20. `AUTHORITY_EVIDENCE_REVOKED`
21. `AUTHORITY_EVIDENCE_OUT_OF_SCOPE`
22. `UNDEFINED_INPUT_COMBINATION`
23. `CRYPTO_ELIGIBILITY_UNRESOLVED`

**Rationale:** The set names every constructible branch and excludes all
prohibited operational context domains.

**Downstream impact:** Every reason has exactly one governed outcome/action
mapping. Deferral, risk, venue, network, wallet, market, policy, account,
permission, order, and execution reasons are not present.

**Implementation consequence:** Use an exact ordered string enum with no
aliases, unknown member, free-text fallback, or hidden reason.

### Decision 56 - Required Actions and Emittable Subset (Core)

**Final founder decision:** `RequiredAction` contains exactly `NONE`,
`HUMAN_REVIEW`, `GOVERNANCE_REVIEW`, `FOUNDER_AUTHORITY_REQUIRED`, and
`RESET_REQUIRED`. Only the first three are emittable.

**Rationale:** The repository vocabulary supports descriptive follow-up while
keeping founder-authority and reset actions outside this subject.

**Downstream impact:** No action means permission, market access, account work,
transfer, order handling, execution, or live-money behavior.

**Implementation consequence:** `Decision` rejects either non-emittable value
with `ValueError`; no public emittable-action alias is authorized.

### Decision 57 - Complete Branch Mappings (Core)

**Final founder decision:** Every branch uses the exact mapping in the locked
16-step precedence table below. Generic and authority branches substitute only
their selected exact reason.

**Rationale:** One closed table prevents implicit outcome/action choices.

**Downstream impact:** A reason can never map differently under another input
combination.

**Implementation consequence:** Centralize decision construction, restrict
emittable actions, and test every branch independently and exhaustively.

### Decision 58 - Posture Contradictions and Collisions (Core)

**Final founder decision:** Eligible plus excluded maps to
`REVIEW_REQUIRED / CRYPTO_ELIGIBLE_EXCLUDED_CONFLICT / GOVERNANCE_REVIEW`.
Eligible plus restricted with excluded false maps to
`RESTRICTED / CRYPTO_ELIGIBLE_RESTRICTED_CONFLICT / HUMAN_REVIEW`. Excluded
plus restricted with eligible false maps to `EXCLUDED / CRYPTO_EXCLUDED /
NONE`. All three maps to the eligible/excluded conflict.

**Rationale:** Eligibility cannot override either negative posture, and
exclusion wins over restriction when eligibility is absent.

**Downstream impact:** Evidence contradiction remains higher than every posture
collision.

**Implementation consequence:** Preserve conflict order at global steps 2 and
3 and prove the all-three winner.

### Decision 59 - Cross-Domain Collision Model (Core)

**Final founder decision:** Prohibited caller-context domains create no typed
collisions. Constructible cross-category collisions are resolved solely by the
global precedence plus the generic and authority subprecedence rules.

**Rationale:** Evidence must cover real typed states, not hypothetical fields.

**Downstream impact:** A request may simultaneously contain posture,
evidence-quality, lane, generic, and authority failures, and exactly one
highest branch wins.

**Implementation consequence:** Exhaustively cross those representative states
and separately audit multi-failure generic and authority objects.

### Decision 60 - Missing, Null, Unknown, Undefined, and Fallback States (Core)

**Final founder decision:** Unknown values and invalid nulls are rejected at
construction. Exactly three structurally valid evidence states are governed as
undefined: evidence absent while current, evidence absent while sufficient,
and evidence stale while sufficient. Each maps to `REVIEW_REQUIRED /
UNDEFINED_INPUT_COMBINATION / GOVERNANCE_REVIEW`. The otherwise-unmatched
well-formed request maps to `REVIEW_REQUIRED /
CRYPTO_ELIGIBILITY_UNRESOLVED / GOVERNANCE_REVIEW`.

**Rationale:** These rules distinguish invalid input, constructible
inconsistency, and ordinary unresolved posture.

**Downstream impact:** All-false posture is not permission and reaches fallback
only after every higher branch passes.

**Implementation consequence:** Implement exactly three undefined predicates,
no inferred fourth predicate, and one final total fallback.

### Decision 61 - Complete Deterministic First-Match Precedence (Core)

**Final founder decision:** The exact top-level order has 16 steps:

| Step | Trigger | Outcome | ReasonCode | RequiredAction |
| ---: | --- | --- | --- | --- |
| 1 | Eligibility evidence contradictory | `REVIEW_REQUIRED` | `CRYPTO_ELIGIBILITY_EVIDENCE_CONTRADICTORY` | `HUMAN_REVIEW` |
| 2 | Crypto eligible and excluded | `REVIEW_REQUIRED` | `CRYPTO_ELIGIBLE_EXCLUDED_CONFLICT` | `GOVERNANCE_REVIEW` |
| 3 | Crypto eligible and restricted | `RESTRICTED` | `CRYPTO_ELIGIBLE_RESTRICTED_CONFLICT` | `HUMAN_REVIEW` |
| 4 | Any governed undefined predicate | `REVIEW_REQUIRED` | `UNDEFINED_INPUT_COMBINATION` | `GOVERNANCE_REVIEW` |
| 5 | Crypto-lane confirmation missing | `REVIEW_REQUIRED` | `CRYPTO_LANE_CONFIRMATION_MISSING` | `GOVERNANCE_REVIEW` |
| 6 | Crypto-lane confirmation contradictory | `REVIEW_REQUIRED` | `CRYPTO_LANE_CONTRADICTORY` | `GOVERNANCE_REVIEW` |
| 7 | Crypto lane not confirmed | `REVIEW_REQUIRED` | `CRYPTO_LANE_NOT_CONFIRMED` | `GOVERNANCE_REVIEW` |
| 8 | Generic Asset-Class context failure | `REVIEW_REQUIRED` | exact generic reason | `GOVERNANCE_REVIEW` |
| 9 | Crypto excluded | `EXCLUDED` | `CRYPTO_EXCLUDED` | `NONE` |
| 10 | Crypto restricted | `RESTRICTED` | `CRYPTO_RESTRICTED` | `HUMAN_REVIEW` |
| 11 | Authority failure | `REVIEW_REQUIRED` | exact authority reason | `GOVERNANCE_REVIEW` |
| 12 | Eligibility evidence missing | `REVIEW_REQUIRED` | `CRYPTO_ELIGIBILITY_EVIDENCE_MISSING` | `HUMAN_REVIEW` |
| 13 | Eligibility evidence stale | `REVIEW_REQUIRED` | `CRYPTO_ELIGIBILITY_EVIDENCE_STALE` | `HUMAN_REVIEW` |
| 14 | Eligibility evidence insufficient | `REVIEW_REQUIRED` | `CRYPTO_ELIGIBILITY_EVIDENCE_INSUFFICIENT` | `HUMAN_REVIEW` |
| 15 | Crypto eligible | `ELIGIBLE` | `CRYPTO_ELIGIBLE` | `NONE` |
| 16 | Otherwise unresolved | `REVIEW_REQUIRED` | `CRYPTO_ELIGIBILITY_UNRESOLVED` | `GOVERNANCE_REVIEW` |

Step 8 generic subprecedence is contradictory, ambiguous, invalid,
non-`CRYPTO`, stale, out of scope. Step 11 authority subprecedence is
contradictory, ambiguous, invalid, revoked, stale, out of scope.

**Rationale:** The order protects contradiction and context integrity, honors
caller-supplied terminal negative postures, and remains fail closed.

**Downstream impact:** Lower conditions never alter a selected result.

**Implementation consequence:** Use pure first-match evaluation with no fall-
through side effects and exact mapping tests for all 16 steps.

### Decision 62 - Fallback, Totality, and Exhaustive Proof (Core)

**Final founder decision:** Every well-formed typed request returns exactly one
new `Decision`; no well-formed state raises or falls through. Totality is
proved by the independent 32,768-combination representative oracle and the
two separate multi-failure subprecedence audits specified in Decision 71.

**Rationale:** Finite independent evidence is required beyond implementation-
authored examples.

**Downstream impact:** The fallback covers every otherwise unmatched state and
does not imply eligibility.

**Implementation consequence:** Keep the evaluator deterministic and total;
the oracle must encode the founder table independently of production helpers.

### Decision 63 - Immutable Decision and Reference Behavior (Core)

**Final founder decision:** The future frozen `Decision` fields, in order, are
`outcome: Outcome`, `reason_code: ReasonCode`,
`required_action: RequiredAction`, `crypto_reference: str`,
`eligibility_evidence_reference: str`, and `correlation_reference: str`.
Dataclass equality remains enabled. Every evaluation returns a new object;
repeated decisions are equal by value and distinct by identity.

**Rationale:** A small immutable result carries only classification and exact
traceability.

**Downstream impact:** Nested context and authority objects are not copied into
or returned from the decision.

**Implementation consequence:** Use `@dataclass(frozen=True)` without `slots`,
validate exact enum/reference types, and prove equality, immutability,
identity distinction, preservation, and non-mutation.

### Decision 64 - Future Schema Path, Identifier, and Draft (Core)

**Final founder decision:** The future schema path is
`schemas/sniperbot-crypto-eligibility-exclusion-decision.schema.json`; its
exact `$id` is
`https://echoauth.local/schemas/sniperbot-crypto-eligibility-exclusion-decision.schema.json`;
it uses JSON Schema draft 2020-12.

**Rationale:** This follows repository schema identity convention while naming
the Crypto subject explicitly.

**Downstream impact:** The root contains exactly `request` and `decision` and
does not encode evaluator logic.

**Implementation consequence:** Schema creation requires a separate founder
authorization and exact draft/meta-schema validation.

### Decision 65 - Schema Strictness and Schema/API Parity (Core)

**Final founder decision:** Every schema object sets
`additionalProperties: false`. Property order, required arrays, enums,
reference constraints, object shapes, omission/null behavior, and decision-
emittable actions match this record exactly. The first ten request properties
are required. Lane confirmation is optional and accepts its enum or JSON null;
generic and authority objects are optional by omission and never accept null.

**Rationale:** Exact parity prevents schema and runtime from accepting
different contracts.

**Downstream impact:** JSON Booleans remain strict; references require at least
one non-whitespace character; precedence is excluded from the schema.

**Implementation consequence:** Automated parity tests must compare all six
enums, four dataclasses, property/field order, requiredness, defaults, nulls,
references, nested objects, and the three emittable actions.

### Decision 66 - Future Module, Package, Initializer, and Exports (Core)

**Final founder decision:** The future module is
`sniperbot.crypto.eligibility_decision` at
`src/sniperbot/crypto/eligibility_decision.py`. It coexists with Crypto
Deferral / No-Action only as a sibling module. The existing
`src/sniperbot/crypto/__init__.py` remains unchanged; no package-root or
`sniperbot`-root export, registration, import-time behavior, or convenience
alias is authorized.

**Rationale:** Explicit submodule imports avoid generic-name collisions with
the accepted Deferral API.

**Downstream impact:** Crypto Deferral source, exports, schema, tests, behavior,
and acceptance remain untouched.

**Implementation consequence:** Callers must import the eligibility submodule
directly; any initializer or package expansion is a scope failure.

### Decision 67 - Exact Public API and Frozen Structures (Core)

**Final founder decision:** The future module has exactly this ordered
12-symbol `__all__`:

1. `AssetClass`
2. `AuthorityEvidence`
3. `Decision`
4. `GenericAssetClassContext`
5. `Outcome`
6. `ReasonCode`
7. `RequiredAction`
8. `CryptoEligibilityRequest`
9. `CryptoLaneConfirmation`
10. `Validity`
11. `create_request`
12. `evaluate`

The exact six string-valued enums are `AssetClass`, `Outcome`, `ReasonCode`,
`RequiredAction`, `CryptoLaneConfirmation`, and `Validity`. The exact four
`@dataclass(frozen=True)` structures are `GenericAssetClassContext`,
`AuthorityEvidence`, `CryptoEligibilityRequest`, and `Decision`; equality is
enabled and no `slots` requirement is selected. The exact public functions
are:

```python
def create_request(**values: object) -> CryptoEligibilityRequest:
```

```python
def evaluate(request: CryptoEligibilityRequest) -> Decision:
```

**Rationale:** These symbols are independently selected as the smallest public
surface for the exact Crypto contract; similarity to a same-family structural
pattern grants no inherited semantics.

**Downstream impact:** No alias, emittable-action type, parser, adapter, helper,
protocol, wrapper, registry, or extra public object exists.

**Implementation consequence:** `create_request` performs strict keyword-only
construction without evaluation or coercion; `evaluate` accepts only
`type(request) is CryptoEligibilityRequest`; private helpers start with `_`.

### Decision 68 - Exception and Strict Runtime Boundaries (Core)

**Final founder decision:** `TypeError` applies to wrong exact runtime types,
raw strings for enum fields, non-Boolean Boolean values, invalid nested
objects, subclasses, alternate objects, explicit generic/authority null
through `create_request`, missing or unexpected request keywords, positional
`create_request` arguments, and non-exact request input to `evaluate`.
`ValueError` applies to empty or whitespace-only required references,
non-emittable decision actions, correctly typed values violating an exact
decision-only boundary, and unknown raw values at normal enum construction.
Exception messages are not contractual.

**Rationale:** Error classes distinguish structural type failure from invalid
closed values without custom exceptions.

**Downstream impact:** Every well-formed exact request evaluates without
exception; there is no warning, repair, normalization, or fallback coercion.

**Implementation consequence:** No `AssertionError` validation or custom
exception; strict negative tests cover every listed boundary.

### Decision 69 - Purity, Determinism, Imports, and Prohibited Capabilities (Core)

**Final founder decision:** Evaluation is pure, deterministic, total, and non-
mutating. Production imports are limited exactly to:

```python
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
```

**Rationale:** The classifier needs only immutable value types and closed enum
definitions.

**Downstream impact:** Third-party dependencies, mutable globals, caches,
clocks, randomness, filesystem, environment, subprocess, logging, telemetry,
persistence, database, networking, registration, services, workers,
schedulers, events, other evaluators, orchestration, runtime integration,
market data, nodes, explorers, exchanges, brokers, wallets, custody, accounts,
secrets, transfers, routing, orders, execution, deployment, and live-money
behavior are prohibited.

**Implementation consequence:** Import, AST, behavior, non-mutation, repeated-
decision, dependency, side-effect, and prohibited-capability checks are
mandatory.

### Decision 70 - Direct-Test Path and Required Coverage (Core)

**Final founder decision:** The future focused-test path is
`tests/test_sniperbot_crypto_eligibility_exclusion.py`. Direct tests must prove
the exact API and `__all__`; six enum orders/values; four frozen dataclasses,
fields, annotations, defaults, no default factories, equality, identity,
inequality, and immutability; signatures; strict types; exception boundaries;
omission/null rules; alternate and cross-lane object rejection; all 16
branches and mappings; all posture and lane states; all three undefined
predicates; fallback; both six-step subprecedences and their 14 pairwise
collisions; reference preservation; purity; non-mutation; equal-but-distinct
decisions; schema/API parity; package preservation; import restrictions; and
prohibited-capability absence.

**Rationale:** Every founder-selected boundary requires committed direct
evidence, not passing behavior alone.

**Downstream impact:** A missing assertion is an evidence gap even if the
implementation is correct.

**Implementation consequence:** Tests must use an independent expected-result
model and may not import production private helpers as an oracle.

### Decision 71 - Exhaustive Oracle and Evidence-Gap Completion (Core)

**Final founder decision:** The exhaustive representative model is exactly:

* 16 combinations of four eligibility-evidence Booleans;
* 8 combinations of three posture Booleans;
* 4 lane states: missing, confirmed, not confirmed, contradictory;
* 8 generic-context representatives: absent, fully valid, contradictory,
  ambiguous, invalid, non-Crypto, stale, out of scope; and
* 8 authority representatives: absent, fully valid, contradictory, ambiguous,
  invalid, revoked, stale, out of scope.

The required total is
`16 x 8 x 4 x 8 x 8 = 32,768 combinations`. A separate generic-context audit
and a separate authority audit each prove all 14 logically possible pairwise
subprecedence collisions, including independent out-of-scope winners.

**Rationale:** The finite representative product exhausts every global branch
category while the collision audits cover multi-failure nested states that
the isolated representatives intentionally omit.

**Downstream impact:** Independent review must confirm the oracle is derived
from this record rather than production code.

**Implementation consequence:** If review identifies a specific missing direct
assertion, only a separately founder-authorized test-only evidence-completion
change may close it; production changes are not implied.

### Decision 72 - Validation, Provenance, Formal Acceptance, Indexing, and Stops (Core)

**Final founder decision:** Schema, API clarification, implementation, direct
tests, evidence completion, independent evidence review, formal acceptance,
and README indexing each require separate explicit founder authorization unless
a later task order expressly combines exact files. Every publication requires
clean synchronized `main`, no Git locks, divergence `0/0`, exact scope,
documentation/content guards, applicable JSON Schema validation, schema/API
parity, focused tests, Contract Validation, Contract and Authority Clarity,
Explicit Authority Clarity Validator, canonical suite, package/import/purity/
prohibited-capability checks, final newline, whitespace, and
`git diff --check`.

**Rationale:** Provenance and independent evidence must remain reviewable and
cannot be implied by implementation publication.

**Downstream impact:** Formal acceptance must record contract, founder,
schema, implementation, and evidence-completion commits; exact file scope;
validation counts; exhaustive count; both collision audits; production blob;
clean state; gap closure; and every non-authorization boundary. Acceptance
indexing remains separately bounded.

**Implementation consequence:** Stop immediately on ambiguity, schema/API
drift, implicit inheritance, unexpected file, changed Crypto Deferral or
package initializer, failed validation, missing evidence, prohibited import or
capability, runtime/integration behavior, operative authority, Stage 2
advancement, or Stage 3 movement.

## Locked Closed Vocabularies

### AssetClass - 3

1. `STOCK`
2. `OPTIONS`
3. `CRYPTO`

### CryptoLaneConfirmation - 3

1. `CONFIRMED`
2. `NOT_CONFIRMED`
3. `CONTRADICTORY`

### Validity - 3

1. `VALID`
2. `INVALID`
3. `AMBIGUOUS`

### Outcome - 4

1. `ELIGIBLE`
2. `EXCLUDED`
3. `RESTRICTED`
4. `REVIEW_REQUIRED`

### ReasonCode - 23

The exact ordered values are those recorded in Decision 55.

### RequiredAction - 5

1. `NONE`
2. `HUMAN_REVIEW`
3. `GOVERNANCE_REVIEW`
4. `FOUNDER_AUTHORITY_REQUIRED`
5. `RESET_REQUIRED`

The exact emittable subset is `NONE`, `HUMAN_REVIEW`, and
`GOVERNANCE_REVIEW`.

## Locked Generic-Context Mappings

| Subprecedence | Condition | Outcome | ReasonCode | RequiredAction |
| ---: | --- | --- | --- | --- |
| 1 | Contradictory | `REVIEW_REQUIRED` | `GENERIC_ASSET_CLASS_CONTEXT_CONTRADICTORY` | `GOVERNANCE_REVIEW` |
| 2 | Ambiguous | `REVIEW_REQUIRED` | `GENERIC_ASSET_CLASS_CONTEXT_INVALID` | `GOVERNANCE_REVIEW` |
| 3 | Invalid | `REVIEW_REQUIRED` | `GENERIC_ASSET_CLASS_CONTEXT_INVALID` | `GOVERNANCE_REVIEW` |
| 4 | Asset class is not `CRYPTO` | `REVIEW_REQUIRED` | `GENERIC_ASSET_CLASS_NOT_CRYPTO` | `GOVERNANCE_REVIEW` |
| 5 | Stale | `REVIEW_REQUIRED` | `GENERIC_ASSET_CLASS_CONTEXT_STALE` | `GOVERNANCE_REVIEW` |
| 6 | Out of scope | `REVIEW_REQUIRED` | `GENERIC_ASSET_CLASS_CONTEXT_OUT_OF_SCOPE` | `GOVERNANCE_REVIEW` |
| - | Absent or fully valid Crypto context | continue | none | none |

## Locked Authority Mappings

| Subprecedence | Condition | Outcome | ReasonCode | RequiredAction |
| ---: | --- | --- | --- | --- |
| 1 | Contradictory | `REVIEW_REQUIRED` | `AUTHORITY_EVIDENCE_INVALID` | `GOVERNANCE_REVIEW` |
| 2 | Ambiguous | `REVIEW_REQUIRED` | `AUTHORITY_EVIDENCE_INVALID` | `GOVERNANCE_REVIEW` |
| 3 | Invalid | `REVIEW_REQUIRED` | `AUTHORITY_EVIDENCE_INVALID` | `GOVERNANCE_REVIEW` |
| 4 | Revoked | `REVIEW_REQUIRED` | `AUTHORITY_EVIDENCE_REVOKED` | `GOVERNANCE_REVIEW` |
| 5 | Stale | `REVIEW_REQUIRED` | `AUTHORITY_EVIDENCE_STALE` | `GOVERNANCE_REVIEW` |
| 6 | Out of scope | `REVIEW_REQUIRED` | `AUTHORITY_EVIDENCE_OUT_OF_SCOPE` | `GOVERNANCE_REVIEW` |
| - | Absent or fully valid authority evidence | continue | none | none |

## Exact Future Paths - Not Authorized for Creation

* Schema:
  `schemas/sniperbot-crypto-eligibility-exclusion-decision.schema.json`
* Production module:
  `src/sniperbot/crypto/eligibility_decision.py`
* Direct tests:
  `tests/test_sniperbot_crypto_eligibility_exclusion.py`
* Implementation-evidence acceptance:
  `docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-crypto-eligibility-exclusion-implementation-evidence-acceptance.md`

This record creates no reservation, file, export, implementation, test, or
authority at any listed path.

## No-Inheritance Confirmation

The decisions above were selected expressly for this bounded Crypto subject.
No Stock, Options, Asset-Class, or Crypto Deferral symbol, count, vocabulary,
field, type, default, null rule, reason, mapping, precedence, authority shape,
schema behavior, API behavior, test model, or implementation behavior applies
by similarity. Where this record independently selects a repository structural
convention, this record states the selection and its Crypto-specific boundary.

The accepted Crypto Deferral / No-Action lane remains unchanged. Caller-
supplied context is either excluded from this request or accepted only in the
two exact non-authorizing generic and authority objects. It never authorizes
operational behavior.

## Decision Boundary and Next Founder Decision

This record resolves the bounded founder-decision surface only. It grants no
schema, Python implementation, direct-test, evidence-review, acceptance,
README-indexing, package-export, runtime, integration, orchestration,
market-data, blockchain, exchange, broker, wallet, custody, networking,
persistence, registration, account, transfer, routing, order, execution,
live-money, successor-lane, Stage 2 advancement, or Stage 3 authority.

Any next action requires a new explicit bounded founder authorization. Stage 2
remains **HOLD**. Stage 3 remains unentered and unauthorized.
