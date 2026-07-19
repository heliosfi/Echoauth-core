# SniperBot Market Intelligence, Governance, Execution, and Learning Relationship

## Status and Scope

This document is the canonical conceptual definition of the higher-order
relationship among SniperBot Market Intelligence, Governance, Execution, and
Learning.

It clarifies how the repository's existing market-data, signal, strategy,
risk, and execution boundaries relate. It does not redesign, merge, unlock, or
implement those boundaries. The flow described here is conceptual only; it is
not an implemented runtime pipeline, integration plan, or runtime contract.

The governing doctrine is:

> Market intelligence proposes. Governance permits, restricts, defers,
> escalates, or denies. Execution conducts only what governance permits.
> Reality teaches.

When this relationship is shortened to "market intelligence proposes;
governance disposes," **disposes** means only that Governance permits,
restricts, defers, escalates, or denies. Governance does not create the market
thesis.

## Canonical Conceptual Flow

```text
Observe
-> Classify
-> Predict
-> Define Invalidation
-> Form Candidate Intent
-> Govern
-> Authorize or Deny
-> Execute if Authorized
-> Observe Outcome
-> Learn
```

This sequence expresses responsibility and authority boundaries. It does not
assert that any step, handoff, evaluator, orchestration, integration, or
runtime behavior exists.

## Domain Responsibilities

### Market Intelligence

Market Intelligence observes approved evidence, classifies conditions,
predicts, defines invalidation, and proposes an evidence-backed candidate. It
owns:

* approved market-evidence interpretation
* regime and condition classification
* signal formation
* strategy comparison and selection
* prediction
* confidence
* time horizon
* thesis formation
* explicit invalidation
* candidate-trade intent
* expected outcome
* analytical learning from outcomes

Market Intelligence does not own:

* founder authority
* policy exceptions
* risk-policy overrides
* execution activation
* broker permission
* routing permission
* trading authorization

A candidate is an analytical proposal, not permission, approval, an order, or
an executable instruction. Market-data observations, signals, strategies,
predictions, confidence, invalidation, and expected outcomes remain within
their existing boundaries and do not acquire authority by being assembled
into a candidate.

### Governance

Governance evaluates the evidence-backed candidate against authority,
eligibility, policy, risk, and permission. It owns:

* evidence acceptability
* authority validity
* eligibility and exclusions
* policy constraints
* capital and exposure constraints
* stop and loss-limit rules
* manual or founder approval requirements
* kill-switch state
* execution-mode permission
* broker and routing permission
* hold, block, defer, escalate, revoke, and no-action outcomes

Governance may evaluate market-derived evidence supplied through a defined
handoff. It may permit, restrict, defer, escalate, or deny the candidate. It
must not manufacture a market thesis or prediction merely to justify
authorization, and its disposition does not rewrite the analytical claim.

Governance permission is specific and bounded. Analytical eligibility is not
authority; accepted evidence is not authority; the absence of a denial is not
authority.

### Execution

Execution performs only the specifically authorized action. It owns:

* faithful conduct of an authorized action
* enforcement of authorized symbol, asset, size, timing, mode, route, and
  other constraints
* refusal to exceed authorization
* traceable result reporting

Execution must not reinterpret the thesis, broaden the candidate, create
permission, or treat analytical confidence as permission. If authorization
is absent, denied, revoked, expired, ambiguous, or outside its constraints,
this conceptual relationship provides no basis for action.

### Learning

Learning compares prediction with reality and returns analytical evidence
that may improve future Market Intelligence. It owns:

* comparing prediction with reality
* evaluating classification, confidence, invalidation, and strategy quality
* returning analytical evidence for future intelligence

Learning must not:

* alter the historical governance decision
* convert success into retroactive permission
* automatically modify policy or authority
* activate runtime behavior
* authorize future conduct

Reality determines the observed outcome; it does not grant authority. A
successful outcome may inform later analysis, but it cannot validate an
unauthorized action or become standing permission.

## Conceptual Market Intelligence-to-Governance Handoff

A future handoff may convey sufficient analytical context for Governance to
evaluate a candidate without transferring or manufacturing authority. At a
conceptual level, that context may include:

* evidence identity and provenance
* symbol and asset class
* observed market state
* regime classification
* candidate strategy
* thesis
* time horizon
* confidence
* entry conditions
* invalidation conditions
* exit assumptions
* candidate intent
* uncertainty and missing evidence
* timestamp and freshness information

This list describes meaning only. It is not a schema, class, API, interface,
evaluator, validation rule, required field set, or implementation design.
The handoff preserves the distinction between a market-derived proposal and
a governance disposition. It cannot itself authorize execution.

## Boundary Preservation

This conceptual relationship preserves the repository's established
separations:

* market data and tick processing concern market evidence and its integrity;
  they do not create signals, strategy, risk decisions, or trading approval
* signals may express classified analytical information, but do not create
  strategy, risk, routing, execution, or trading authority
* strategy comparison and candidate-intent formation remain distinct from
  risk decisions, sizing, routing, execution, and trading approval
* risk evaluation remains distinct from strategy, sizing, routing, and
  execution and does not inherit permission from analytical output
* Execution remains downstream of specific Governance permission and cannot
  infer or expand that permission
* Learning returns evidence to future analysis without crossing into policy,
  authority, or activation

No domain inherits authority from adjacency, sequencing, successful analysis,
documentation, or inclusion in this conceptual flow. Existing control-gate
records remain locked and governing within their respective scopes.

## Mandatory Non-Authorization

This document does not authorize or implement:

* market-data access
* signal generation
* strategy runtime
* prediction runtime
* risk runtime
* learning runtime
* schemas
* APIs
* evaluators
* orchestration
* integration
* simulation
* paper trading
* deployment
* broker access
* order routing
* live trading
* autonomous action
* Stage 3 entry
* repository separation

It also does not authorize implementation, tests, CI or workflow changes,
runtime contracts, credential use, capital movement, execution activation,
or any other capability expansion.

**No confidence score, prediction, strategy result, analytical conclusion,
historical success, or learning output creates authority or trading
permission.**

Stage 2 formal closure is unchanged. The Advancement Gate remains **FAIL**.
Stage 3 remains **UNENTERED AND UNAUTHORIZED**. This document creates no
implementation authority, runtime authority, deployment authority, broker
authority, trading authority, or autonomous-action authority. Any movement
beyond this documentation boundary requires a separate, explicit, governed,
and authorized lane.
