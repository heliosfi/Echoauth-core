# SniperBot Stage 2 Crypto Deferral / No-Action Contract Definition Review

## Status and Boundary

**Established repository fact:** Repository `heliosfi/Echoauth-core`; starting
checkpoint `e8d5932d75578fccf1bf39ebdf72fa46e5acc8fd`; supporting Crypto boundary
commit `552ac5d3048a43857bc66d2f64736d770b1ff358`.

**Established repository fact:** The subject is **SniperBot Stage 2 Crypto
Deferral / No-Action Decision Contract**. This record is documentation and
founder-decision review only. Stage 2 remains **HOLD**. Stage 3 remains
unentered and unauthorized.

**Prohibited:** This review is not a schema, evaluator, test, integration,
runtime, approval, task order, or execution authority.

## Established Facts

* **Established repository fact:** Crypto Deferral / No-Action is the next
  same-family unresolved candidate.
* **Established repository fact:** Stock and Options Deferral / No-Action are
  complete and parked.
* **Established repository fact:** The Crypto posture must remain descriptive
  and non-authorizing.
* **Established repository fact:** Ambiguity, incomplete evidence, and
  contradiction must remain fail-closed.
* **Established repository fact:** Crypto Deferral / No-Action is separate
  from Crypto Eligibility / Exclusion, Crypto Risk, token or asset approval,
  exchange or wallet selection, market data, strategy, and broker or execution
  behavior.
* **Established repository fact:** No schema, evaluator, test, integration, or
  runtime work is authorized by this document.

## Contract Boundary Under Review

**Unresolved:** The exact Crypto input vocabulary, output vocabulary,
precedence, mappings, validation rules, and public API are not established.
They require all 18 founder decisions below.

**Recommendation only — not Crypto authority:** Consider a pure descriptive
classifier that consumes only externally supplied, immutable facts and emits
only a fail-closed classification with opaque references. Structural
similarity to Stock or Options is a review aid, not inherited authority.

**Prohibited:** The future subject may not identify, validate, select, rank,
approve, price, size, route, trade, transfer, custody, or execute a crypto
asset, and may not call or reinterpret an authority system.

## Founder Decisions Required

Each item is unresolved. Its recommendation is explicitly not founder
authority and cannot be used to create a schema or implementation.

### 1. Outcome vocabulary

* **Founder decision required - question:** What closed outcome values may the
  Crypto classifier emit?
* **Founder decision required - supported choices:** Crypto-specific
  `DEFER`/`NO_ACTION`; a different closed set; or no classifier contract.
* **Founder decision required - consequences:** The first preserves the
  same-family descriptive posture; the second requires independently defined
  semantics; the third ends this proposed lane.
* **Recommendation only — not Crypto authority:** Use only `DEFER` and
  `NO_ACTION`, neither of which conveys eligibility, approval, permission, or
  execution.
* **Recommendation only — not Crypto authority:** Safest fail-closed default is
  `NO_ACTION` where an authorized mapping eventually requires a default.
* **Unresolved:** Decide before any reason vocabulary, schema, or evaluator;
  enforce later in the decision record, schema enum, evaluator types, and
  direct tests.

### 2. Closed reason-code vocabulary

* **Founder decision required - question:** What exact closed Crypto-specific
  reason codes exist?
* **Founder decision required - supported choices:** Founder-name a complete
  Crypto set; authorize a bounded shared subset plus Crypto-specific codes; or
  decline a reason-code contract.
* **Founder decision required - consequences:** A named set enables exact
  validation; reuse risks importing Stock/Options meaning; declining prevents
  deterministic structured output.
* **Recommendation only — not Crypto authority:** Founder-name every code and
  prohibit free text, implicit aliases, and an unapproved catch-all code.
* **Recommendation only — not Crypto authority:** Safest fail-closed default is
  rejection of unknown raw codes, not invented normalization.
* **Unresolved:** Decide before schema definition; enforce later in the decision
  record, schema, enums, mapping tests, and contract tests.

### 3. `RequiredAction` vocabulary and emittable subset

* **Founder decision required - question:** Which `RequiredAction` values exist
  and which may this subject emit?
* **Founder decision required - supported choices:** Reuse a separately bounded
  closed vocabulary with an explicit Crypto subset; define a Crypto-specific
  vocabulary; or omit the field.
* **Founder decision required - consequences:** Reuse aids consistency but may
  import meaning; a new set needs full governance; omission reduces review
  signaling.
* **Recommendation only — not Crypto authority:** Reuse only after founder maps
  each emittable value and explicitly rejects non-emittable values.
* **Recommendation only — not Crypto authority:** Safest fail-closed default is
  a human or governance review action, never permission or execution.
* **Unresolved:** Decide with outcomes and reasons; enforce later in schema
  conditionals, evaluator mappings, and exhaustive tests.

### 4. Opaque Crypto subject identity

* **Founder decision required - question:** What opaque subject reference is
  required and what validation is allowed?
* **Founder decision required - supported choices:** Mandatory non-empty opaque
  reference; optional opaque reference; or no subject reference.
* **Founder decision required - consequences:** Mandatory identity supports
  correlation without asset semantics; optional or absent identity weakens
  traceability.
* **Recommendation only — not Crypto authority:** Require a non-empty opaque
  reference and preserve it exactly without interpreting symbol, token, chain,
  address, contract, venue, wallet, or account meaning.
* **Recommendation only — not Crypto authority:** Safest fail-closed default is
  reject missing or malformed identity before classification.
* **Unresolved:** Decide before input schema; enforce later in schema, immutable
  input structure, exact-reference tests, and prohibited-interpretation review.

### 5. Deferral meaning

* **Founder decision required - question:** What does an externally supplied
  Crypto deferral fact mean and how is it mapped?
* **Founder decision required - supported choices:** Pause pending review;
  distinguish multiple deferral categories; or exclude explicit deferral.
* **Founder decision required - consequences:** A single fact is bounded but
  coarse; categories require new vocabulary; exclusion leaves only other
  fail-closed facts.
* **Recommendation only — not Crypto authority:** Treat deferral only as an
  external descriptive pause requiring review, never rejection, approval,
  eligibility, timing, strategy, or execution behavior.
* **Recommendation only — not Crypto authority:** Safest fail-closed default is
  no movement while deferral is unresolved.
* **Unresolved:** Decide before mappings and precedence; enforce later in the
  decision record, schema, evaluator branch, and direct tests.

### 6. No-action meaning

* **Founder decision required - question:** What does Crypto no-action mean and
  how is explicit no-action distinguished from an ordinary fallback?
* **Founder decision required - supported choices:** One shared no-action
  mapping; separate explicit and fallback mappings; or no fallback.
* **Founder decision required - consequences:** A shared mapping is simple;
  separate mappings improve provenance; no fallback requires every combination
  to match another governed condition.
* **Recommendation only — not Crypto authority:** Define no-action solely as a
  descriptive absence of authorized movement, not approval, rejection,
  position handling, or execution.
* **Recommendation only — not Crypto authority:** Safest fail-closed default is
  no action with no executable instruction.
* **Unresolved:** Decide before global precedence; enforce later in closed
  mappings and explicit fallback tests.

### 7. Evidence fields and contradiction semantics

* **Founder decision required - question:** Which supplied evidence fields are
  admitted, and what exactly constitutes contradiction, absence, staleness,
  or insufficiency?
* **Founder decision required - supported choices:** Closed Boolean/status
  fields; a founder-defined closed evidence object; or no evidence input.
* **Founder decision required - consequences:** Closed fields support
  deterministic evaluation; an object expands schema and ambiguity; omission
  prevents evidence-sensitive classification.
* **Recommendation only — not Crypto authority:** Admit only explicitly supplied
  closed facts and never infer contradiction or quality from external systems.
* **Recommendation only — not Crypto authority:** Safest fail-closed default is
  review/no-action for contradiction, incomplete evidence, or invalid
  combinations.
* **Unresolved:** Decide before schema vocabulary; enforce later in schema
  conditionals, first-match mappings, truth-table tests, and validation tests.

### 8. Restriction and exclusion treatment

* **Founder decision required - question:** May supplied Crypto restriction and
  exclusion facts be consumed, are they distinct, and how do they map?
* **Founder decision required - supported choices:** Separate external facts;
  one combined fact; contextual-only facts; or prohibit both.
* **Founder decision required - consequences:** Separation preserves provenance;
  combination loses detail; contextual-only treatment needs precedence;
  prohibition removes this boundary input.
* **Recommendation only — not Crypto authority:** If admitted, keep them separate,
  externally supplied, descriptive, and non-calculated; do not treat them as
  token eligibility or approval.
* **Recommendation only — not Crypto authority:** Safest fail-closed default is
  no action when either governed fact applies.
* **Unresolved:** Decide before reason codes and precedence; enforce later in
  schema fields, mappings, mutual-combination tests, and exclusion scans.

### 9. Crypto-lane confirmation

* **Founder decision required - question:** Is explicit Crypto-lane confirmation
  required, and what is its closed vocabulary?
* **Founder decision required - supported choices:** Mandatory closed
  confirmation; optional confirmation; externally guaranteed context; or no
  confirmation field.
* **Founder decision required - consequences:** Mandatory confirmation is most
  explicit; optional or implicit context increases ambiguity; omission relies
  entirely on caller boundaries.
* **Recommendation only — not Crypto authority:** Require a closed explicit value
  and never infer Crypto from identity, token metadata, chain, venue, wallet,
  market data, or another classifier.
* **Recommendation only — not Crypto authority:** Safest fail-closed default is
  no action/governance review when confirmation is absent, negative,
  contradictory, malformed, or ambiguous.
* **Unresolved:** Decide before schema and API definition; enforce later in enum,
  validation, precedence, and exhaustive confirmation tests.

### 10. Generic Asset-Class context treatment

* **Founder decision required - question:** Is generic Asset-Class context
  required, optional, or prohibited, and what compatibility means are allowed?
* **Founder decision required - supported choices:** Optional opaque context;
  mandatory opaque context; prohibit it; or accept only a bounded reference.
* **Founder decision required - consequences:** Context may aid traceability but
  risks orchestration or inherited authority; prohibition maximizes separation.
* **Recommendation only — not Crypto authority:** If admitted, make it optional,
  opaque, non-authorizing, and never invoke or import the generic evaluator.
* **Recommendation only — not Crypto authority:** Safest fail-closed default is
  no action/governance review for supplied incompatible, stale, contradictory,
  invalid, or out-of-scope context.
* **Unresolved:** Decide before context fields and mappings; enforce later in
  schema, precedence, prohibited-import scans, and direct tests.

### 11. Separation from Stock and Options

* **Founder decision required - question:** What structural reuse, if any, is
  allowed without importing Stock or Options semantics or authority?
* **Founder decision required - supported choices:** Structural pattern only;
  explicitly named shared vocabulary; or total independent definition.
* **Founder decision required - consequences:** Pattern reuse reduces novelty but
  risks semantic inheritance; shared vocabulary requires explicit authority;
  independence is safest but may duplicate governance structure.
* **Recommendation only — not Crypto authority:** Permit document rigor and pure
  classifier shape as comparison only; prohibit calls, orchestration, semantic
  inheritance, and modification of accepted Stock/Options surfaces.
* **Recommendation only — not Crypto authority:** Safest fail-closed default is
  no cross-lane inference.
* **Unresolved:** Decide before any shared import or vocabulary; enforce later by
  exact-scope review, prohibited-import scans, and independence tests.

### 12. Authority-evidence treatment and precedence

* **Founder decision required - question:** Is bounded EchoAuth authority
  evidence admitted, and how do failure states and sub-precedence map?
* **Founder decision required - supported choices:** Optional opaque contextual
  evidence; mandatory evidence; prohibit it; or accept only a correlation
  reference.
* **Founder decision required - consequences:** Context can record supplied
  authority posture but risks reinterpretation; mandatory evidence couples the
  subjects; prohibition maximizes separation.
* **Recommendation only — not Crypto authority:** If admitted, keep it optional,
  externally supplied, contextual, and fail-closed; never call, validate,
  repair, broaden, grant, replace, or bypass EchoAuth.
* **Recommendation only — not Crypto authority:** Safest fail-closed default is
  no action/governance review for any governed failure or ambiguity.
* **Unresolved:** Decide before reason codes and precedence; enforce later in
  schema, mapping order, prohibited-side-effect review, and tests.

### 13. Deferral/no-action conflict mapping

* **Founder decision required - question:** How does simultaneous explicit
  deferral and no-action map?
* **Founder decision required - supported choices:** Dedicated conflict reason;
  deferral wins; no-action wins; or reject the combination before evaluation.
* **Founder decision required - consequences:** A dedicated mapping preserves
  conflict evidence; either winner hides one fact; rejection moves behavior to
  validation.
* **Recommendation only — not Crypto authority:** Use a dedicated fail-closed
  conflict mapping requiring governance review.
* **Recommendation only — not Crypto authority:** Safest fail-closed default is
  no action, never deferral interpreted as future permission.
* **Unresolved:** Decide before global precedence; enforce later in schema
  constraints or evaluator ordering and conflict tests.

### 14. Exact global first-match precedence

* **Founder decision required - question:** What is the complete ordered list of
  all classifiable conditions?
* **Founder decision required - supported choices:** Founder-defined first-match
  order; mutually exclusive schema branches; or reject overlapping facts.
* **Founder decision required - consequences:** First-match is deterministic but
  must be exhaustive; exclusivity shifts complexity to validation; rejecting
  overlap may discard useful conflict provenance.
* **Recommendation only — not Crypto authority:** Founder approve one explicit,
  exhaustive first-match order with contradiction and invalidity ahead of
  ordinary deferral/no-action.
* **Recommendation only — not Crypto authority:** Safest fail-closed default is
  stop if any precedence relation is ambiguous.
* **Unresolved:** Decide only after Decisions 1-13; enforce later in the decision
  record, evaluator order, exhaustive pairwise tests, and parity checks.

### 15. Unknown and undefined input policy

* **Founder decision required - question:** How are unknown raw values and
  founder-defined invalid or undefined typed combinations handled?
* **Founder decision required - supported choices:** Reject unknown raw values
  and classify a closed undefined set; reject both; or classify both with
  separately authorized reasons.
* **Founder decision required - consequences:** Split handling distinguishes
  validation from governed ambiguity; rejection is strict; classification
  requires more vocabulary and precedence.
* **Recommendation only — not Crypto authority:** Reject unknown raw values
  before typed construction and founder-name every classifiable undefined
  combination.
* **Recommendation only — not Crypto authority:** Safest fail-closed default is
  rejection or no action/governance review, never permissive coercion.
* **Unresolved:** Decide after input vocabulary; enforce later in schema,
  constructors, validation tests, and undefined-combination tests.

### 16. Output and public API surface

* **Founder decision required - question:** What exact immutable output fields
  and public imports may a future package expose?
* **Founder decision required - supported choices:** Outcome, reason,
  RequiredAction, opaque subject reference, and correlation reference; a
  smaller subset; or no public package API.
* **Founder decision required - consequences:** The fuller descriptive result
  supports traceability; a smaller result limits meaning; no API prevents an
  evaluator surface.
* **Recommendation only — not Crypto authority:** Expose only founder-approved
  frozen input/output types, closed enums, and one pure evaluator; preserve
  opaque references exactly and export no runtime helpers.
* **Recommendation only — not Crypto authority:** Safest fail-closed default is
  no executable command, permission, asset detail, address, venue, wallet,
  price, size, strategy, order, or routing field.
* **Unresolved:** Decide before package or schema work; enforce later in exact
  exports, frozen structures, API tests, and scope scans.

### 17. Future schema, package, evaluator, and test paths

* **Founder decision required - question:** Which exact paths, if any, may be
  considered in separately authorized future lanes?
* **Founder decision required - supported choices:** The proposed bounded paths
  below; different founder-named paths; or no future files.
* **Founder decision required - consequences:** Named paths bound scope;
  alternatives require renewed inspection; no files ends the lane.
* **Recommendation only — not Crypto authority:** Consider one schema, the
  minimal package initializer required by convention, one pure evaluator, and
  one direct test only.
* **Recommendation only — not Crypto authority:** Safest fail-closed default is
  create nothing until each path and each later task order is separately
  authorized.
* **Unresolved:** Decide before schema work; enforce later by exact allowlists,
  maximum-file limits, staged-name checks, and stop conditions.

### 18. Validation commands and stop conditions

* **Founder decision required - question:** What exact validations must each
  future lane run, and which failures prohibit commit or push?
* **Founder decision required - supported choices:** Focused plus contract,
  Authority Clarity, full-suite, JSON, parity, scope, import, and side-effect
  checks as applicable; a founder-defined stricter set; or no future lane.
* **Founder decision required - consequences:** Comprehensive validation gives
  strongest repository evidence; narrower validation may miss boundary drift;
  no lane requires no commands.
* **Recommendation only — not Crypto authority:** Require exact-path JSON parse,
  vocabulary/schema/evaluator parity, focused tests, Contract and Authority
  Clarity modules, full suite when implementation exists, clean diff checks,
  exact scope, prohibited imports, and side-effect scans.
* **Recommendation only — not Crypto authority:** Safest fail-closed default is
  stop without repair, commit, or push on any failure, ambiguity, unexpected
  file, authority expansion, or repository operation.
* **Unresolved:** Decide before authorizing a schema lane; enforce in each future
  task order, validation evidence, staging review, and acceptance record.

## Prohibited Contract Surfaces

**Prohibited:** Token or coin eligibility; asset approval; exchange selection;
wallet selection or access; address validation; private keys; seed phrases;
credentials; custody; deposits or withdrawals; blockchain or node access;
chain analysis; market-data retrieval; pricing; liquidity calculations;
slippage; strategy; risk; sizing; simulation; paper trading; exchange or
broker APIs; orders; routing; execution; runtime wiring; another Stage 2
subject; and Stage 3.

**Prohibited:** No recommendation in this review is approved, locked, accepted,
final, or executable. No Stock or Options decision is Crypto authority.

## Proposed Future Surfaces

* **Proposed only — requires separate founder authorization:** Crypto
  contract-definition founder-decision record at a founder-approved path.
* **Proposed only — requires separate founder authorization:** Crypto decision
  schema at a founder-approved path.
* **Proposed only — requires separate founder authorization:**
  `src/sniperbot/crypto/__init__.py`.
* **Proposed only — requires separate founder authorization:**
  `src/sniperbot/crypto/deferral_decision.py`.
* **Proposed only — requires separate founder authorization:** Direct Crypto
  evaluator tests at a founder-approved test path.

## Validation and Next Founder Decision

**Established repository fact:** This documentation lane requires exact
two-file scope plus Contract and Authority Clarity validation. It does not
authorize the full suite, schema validation, or executable work.

**Unresolved:** All 18 founder decisions remain unanswered.

**Founder decision required:** The exact next founder decision is
`AUTHORIZE CRYPTO DEFERRAL / NO-ACTION FOUNDER-DECISION RESOLUTION`.

**Established repository fact:** Stage 2 remains **HOLD**. Stage 3 remains
unentered and unauthorized.
