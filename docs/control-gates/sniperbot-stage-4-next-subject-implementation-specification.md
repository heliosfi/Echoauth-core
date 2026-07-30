# SniperBot Stage 4 Next-Subject Implementation Specification

## Specification Status

**ISSUED WITH TASK ORDER — IMPLEMENTATION REQUIRES THE INSEPARABLE TASK ORDER AND REMAINS PENDING EXECUTION**

This specification freezes the complete technical implementation contract for:

> **Deterministic Typed Fixture Scenario Content and Provenance Validator**

It is governed by the independently accepted SniperBot contract and does not alter that contract.

## Authority and Exact Evidence

Nicholas B. Carty authorized the **SniperBot Stage 4 Next-Subject Implementation Specification and Task Order Authorization** lane.

The governing evidence is:

- SniperBot accepted-contract branch: `sniperbot-stage-4-next-subject-independent-contract-acceptance`;
- accepted-contract checkpoint: `998e2d2e91ecb758e084aad0112fd58608dcdb61`;
- accepted-contract record blob: `129d8e2777cac10314103d7c0de747e43afd4b25`;
- contract checkpoint: `fb2b26aaad63e17dce7b8b76b0ca92b9b70cd149`;
- contract blob: `8fe287db830505dfbc59664ad78dbed60f6baec6`;
- corrected-readiness checkpoint: `05e1137a201ae0c699ea8e28c60f3014dde24f7b`;
- corrected-readiness blob: `df5db9e1d040baf20f42b535744e75d9c7045ce0`;
- accepted Stage 4.1A implementation checkpoint: `085cd82742a93f0a631cb2185d868f719ddd84f5`;
- accepted Stage 4.1A source blob: `d4a8664cc9ec49b9caffd30157ab6992597fef79`;
- accepted Stage 4.1A test blob: `bfe34ff805e66149dc0de4ee8d9d85ee1efd9804`;
- current canonical SniperBot `main`: `36c34e363619ccf3f859631820dd12ca1bcf5001`;
- current canonical Echoauth-core `main` and specification formation parent: `5c6faea46932836fbb8f04d8a1435298ca8a62b2`.

This specification and the task order issued in the same lane are inseparable. Missing, stale, contradictory, revoked, or nonmatching evidence requires `WAIT` before implementation mutation.

## Exact Implementation Repository and Starting Point

- repository: `heliosfi/sniperbot`;
- exact implementation starting checkpoint: `998e2d2e91ecb758e084aad0112fd58608dcdb61`;
- required implementation branch: `sniperbot-stage-4-next-subject-implementation`;
- branch parent and merge base: exactly the starting checkpoint;
- implementation commit message: `Implement typed fixture scenario validator`.

The accepted-contract branch, not canonical `main`, supplies the complete current governed ancestry. No merge from a historical Stage 4.1B branch is permitted.

## Exact Authorized Implementation Paths

Create exactly two paths:

1. `src/sniperbot/simulation/fixture_observation.py`;
2. `tests/test_fixture_observation.py`.

Both paths must be absent before mutation.

No existing path may be modified, deleted, renamed, reformatted, regenerated, or re-exported. In particular, preserve:

- `src/sniperbot/simulation/scenario.py` at blob `d4a8664cc9ec49b9caffd30157ab6992597fef79`;
- `tests/test_simulation_scenario.py` at blob `bfe34ff805e66149dc0de4ee8d9d85ee1efd9804`;
- both existing package `__init__.py` files; and
- every governance file inherited from the starting checkpoint.

## Exact Production Module

Module:

`sniperbot.simulation.fixture_observation`

The module must expose exactly these public symbols through `__all__`, in this order:

1. `FixtureObservationKind`;
2. `FixtureValidationState`;
3. `FixtureReasonCode`;
4. `FixtureRequiredAction`;
5. `FixtureTradeContent`;
6. `FixtureQuoteContent`;
7. `FixtureBarContent`;
8. `TypedFixtureObservation`;
9. `TypedFixtureScenarioRequest`;
10. `FixtureValidationDecision`;
11. `validate_typed_fixture_scenario`.

No package re-export is permitted. Imported Stage 4.1A names are dependencies, not members of `__all__`.

Private helpers must begin with `_`, have no external side effects, and exist only to implement exact validation, canonicalization, safe evidence preservation, or hashing.

## Exact Enum Contracts

All four enums inherit from `str` and `Enum`.

### `FixtureObservationKind`

```python
TRADE = "trade"
QUOTE = "quote"
BAR = "bar"
```

### `FixtureValidationState`

```python
ACCEPTED = "accepted"
REFUSED = "refused"
```

### `FixtureRequiredAction`

```python
CONTINUE_SIMULATION_ONLY = "continue_simulation_only"
HALT = "halt"
```

### `FixtureReasonCode`

Exact declaration and refusal-precedence order:

```python
INVALID_REQUEST_TYPE = "invalid_request_type"
SCENARIO_REFUSED = "scenario_refused"
INVALID_OBSERVATION_COLLECTION = "invalid_observation_collection"
EMPTY_OBSERVATIONS = "empty_observations"
OBSERVATION_COUNT_MISMATCH = "observation_count_mismatch"
INVALID_OBSERVATION_TYPE = "invalid_observation_type"
REFERENCE_MISMATCH = "reference_mismatch"
INVALID_INSTRUMENT_REFERENCE = "invalid_instrument_reference"
INVALID_KIND = "invalid_kind"
CONTENT_KIND_MISMATCH = "content_kind_mismatch"
INVALID_DECIMAL = "invalid_decimal"
INVALID_TRADE_CONTENT = "invalid_trade_content"
INVALID_QUOTE_CONTENT = "invalid_quote_content"
INVALID_BAR_CONTENT = "invalid_bar_content"
CONTENT_HASH_MISMATCH = "content_hash_mismatch"
ACCEPTED = "accepted"
```

The first applicable reason wins. Observations are processed in tuple order; fields are processed in dataclass order. No aggregation or alternate precedence is permitted.

## Exact Frozen Data Contracts

All six data classes use `@dataclass(frozen=True)`. Field names, order, and annotations are exact.

```python
@dataclass(frozen=True)
class FixtureTradeContent:
    price: Decimal
    quantity: Decimal

@dataclass(frozen=True)
class FixtureQuoteContent:
    bid_price: Decimal
    bid_quantity: Decimal
    ask_price: Decimal
    ask_quantity: Decimal

@dataclass(frozen=True)
class FixtureBarContent:
    open_price: Decimal
    high_price: Decimal
    low_price: Decimal
    close_price: Decimal
    volume: Decimal
    interval_seconds: int

@dataclass(frozen=True)
class TypedFixtureObservation:
    reference: SimulationObservationReference
    instrument_reference: str
    kind: FixtureObservationKind
    content: FixtureTradeContent | FixtureQuoteContent | FixtureBarContent

@dataclass(frozen=True)
class TypedFixtureScenarioRequest:
    scenario: SimulationScenarioRequest
    observations: tuple[TypedFixtureObservation, ...]

@dataclass(frozen=True)
class FixtureValidationDecision:
    state: FixtureValidationState
    reason: FixtureReasonCode
    required_action: FixtureRequiredAction
    scenario_reference: str
    observation_count: int
    scenario_fingerprint: str | None
    content_sha256: tuple[str, ...]
```

Construction performs no validation or external work.

## Exact Content Rules

### Trade

- `price` and `quantity` have exact type `Decimal` and are finite;
- `price > 0`;
- `quantity > 0`.

### Quote

- all four values have exact type `Decimal` and are finite;
- `bid_price > 0` and `ask_price > 0`;
- quantities are greater than or equal to zero;
- `bid_price <= ask_price`.

### Bar

- all price and volume values have exact type `Decimal` and are finite;
- every price is greater than zero;
- `volume >= 0`;
- `type(interval_seconds) is int` and `interval_seconds > 0`;
- `low_price <= open_price`;
- `low_price <= close_price`;
- `high_price >= open_price`;
- `high_price >= close_price`;
- `low_price <= high_price`.

Boolean, integer, float, string, `Decimal` subclass, NaN, and infinity substitutions for Decimal fields are refused.

### Typed observation

- exact accepted Stage 4.1A reference type;
- exact nonempty trimmed `str` instrument reference;
- exact `FixtureObservationKind`;
- exact matching content type;
- the instrument reference remains opaque and is never parsed, normalized, classified, enriched, or resolved.

### Typed request

- exact `TypedFixtureScenarioRequest`;
- contained scenario must be accepted by Stage 4.1A first;
- `type(observations) is tuple`;
- tuple is nonempty;
- typed-observation count equals Stage 4.1A reference count;
- every member has exact `TypedFixtureObservation` type;
- every typed reference equals the same-position Stage 4.1A reference.

## Exact Canonicalization and Hashing

The per-observation canonical payload inserts keys in this order:

1. `instrument_reference`;
2. `kind`;
3. `content`.

The content object inserts fields in frozen dataclass order.

Decimal canonicalization:

1. accept only exact finite `Decimal`;
2. preserve mathematical value;
3. emit plain base-10 without exponent;
4. strip insignificant trailing fractional zeros;
5. strip a trailing decimal point;
6. emit every mathematical zero as `"0"`;
7. never convert through float.

Canonical JSON:

```python
json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
```

Requirements:

- explicit insertion order;
- no key sorting;
- UTF-8 encoding;
- no extra fields;
- lowercase SHA-256 hexadecimal digest;
- digest must equal `reference.payload_sha256` exactly.

## Exact Validation Function and Decision Shapes

```python
def validate_typed_fixture_scenario(
    request: TypedFixtureScenarioRequest,
) -> FixtureValidationDecision:
    ...
```

Execution order:

1. exact request type;
2. accepted Stage 4.1A scenario validation;
3. exact observation collection;
4. nonempty observations;
5. equal count;
6. observation type;
7. same-position reference;
8. instrument reference;
9. kind;
10. matching content type;
11. Decimal exactness and finiteness;
12. content-specific invariants;
13. canonicalization and hashing;
14. first hash mismatch;
15. accepted decision after all observations pass.

Accepted decision:

- `state is ACCEPTED`;
- `reason is ACCEPTED`;
- `required_action is CONTINUE_SIMULATION_ONLY`;
- exact scenario reference and observation count;
- accepted Stage 4.1A fingerprint;
- ordered tuple of all computed content hashes.

Refused decision:

- `state is REFUSED`;
- first applicable exact reason;
- `required_action is HALT`;
- safe scenario reference and observation count only when obtainable from exact fields;
- Stage 4.1A fingerprint only after Stage 4.1A acceptance;
- `content_sha256 == ()`;
- no mutation, log, retry, fallback, persistence, communication, or external action.

The function is deterministic, pure, total for ordinary caller-supplied objects, side-effect free, and free of shared mutable state. Programming defects and unrecoverable interpreter failures are not silently hidden.

## Permitted Imports

Production imports are limited to directly necessary names from:

- `dataclasses`;
- `decimal`;
- `enum`;
- `hashlib`;
- `json`;
- `typing`;
- `sniperbot.simulation.scenario`.

Tests may additionally use `unittest`, `datetime`, and standard-library reflection/source inspection required for contract validation.

No third-party dependency is authorized.

## Exact New Test Inventory

`tests/test_fixture_observation.py` must contain exactly one `unittest.TestCase` subclass and exactly these 24 test methods, in order:

1. `test_01_exact_public_api_and_no_package_reexports`;
2. `test_02_exact_enum_contracts_and_reason_order`;
3. `test_03_exact_frozen_dataclass_contracts`;
4. `test_04_accepted_trade_scenario`;
5. `test_05_accepted_quote_scenario`;
6. `test_06_accepted_bar_scenario`;
7. `test_07_accepted_mixed_observation_scenario`;
8. `test_08_repeated_evaluation_is_deterministic`;
9. `test_09_equal_independent_inputs_produce_equal_decisions`;
10. `test_10_decimal_semantic_equivalence_produces_equal_hashes`;
11. `test_11_material_content_differences_change_hashes`;
12. `test_12_canonical_key_and_field_order`;
13. `test_13_canonical_decimal_strings`;
14. `test_14_canonical_unicode_and_compact_utf8_json`;
15. `test_15_stage_4_1a_refusal_is_propagated`;
16. `test_16_accepted_evidence_lineage_is_preserved`;
17. `test_17_refused_decision_safe_evidence_shape`;
18. `test_18_ordered_negative_case_matrix`;
19. `test_19_exact_global_reason_precedence`;
20. `test_20_first_observation_and_field_failure_order`;
21. `test_21_inputs_are_not_mutated`;
22. `test_22_no_shared_mutable_runtime_state`;
23. `test_23_exact_signature_and_permitted_imports`;
24. `test_24_static_forbidden_surface_scan`.

No additional test method or `TestCase` subclass is permitted in the new test file.

## Exact Ordered Negative-Case Matrix

`test_18_ordered_negative_case_matrix` must evaluate these 67 labeled subcases in this exact order and assert the exact reason:

1. nonrequest object;
2. request subclass;
3. Stage 4.1A raw-string mode refusal;
4. Stage 4.1A isolation refusal;
5. Stage 4.1A invalid scenario reference refusal;
6. Stage 4.1A invalid provenance reference refusal;
7. Stage 4.1A Boolean seed refusal;
8. Stage 4.1A naive clock refusal;
9. Stage 4.1A invalid observation collection refusal;
10. Stage 4.1A empty observation references refusal;
11. Stage 4.1A invalid observation member refusal;
12. Stage 4.1A invalid sequence refusal;
13. Stage 4.1A invalid source refusal;
14. observations list;
15. observations tuple subclass;
16. empty typed observations;
17. observation count too few;
18. observation count too many;
19. observation object member;
20. observation subclass member;
21. reordered reference;
22. substituted reference;
23. non-string instrument reference;
24. empty instrument reference;
25. padded instrument reference;
26. string-subclass instrument reference;
27. raw-string kind;
28. unrelated enum kind;
29. kind subclass or substitute object;
30. trade kind with quote content;
31. quote kind with bar content;
32. bar kind with trade content;
33. Boolean Decimal field;
34. integer Decimal field;
35. float Decimal field;
36. string Decimal field;
37. Decimal-subclass field;
38. Decimal NaN field;
39. Decimal positive infinity field;
40. Decimal negative infinity field;
41. zero trade price;
42. negative trade price;
43. zero trade quantity;
44. negative trade quantity;
45. zero bid price;
46. zero ask price;
47. negative bid price;
48. negative ask price;
49. negative bid quantity;
50. negative ask quantity;
51. crossed quote;
52. zero bar open price;
53. zero bar high price;
54. zero bar low price;
55. zero bar close price;
56. negative bar price;
57. negative bar volume;
58. Boolean bar interval;
59. zero bar interval;
60. negative bar interval;
61. float bar interval;
62. bar low above open;
63. bar low above close;
64. bar high below open;
65. bar high below close;
66. bar low above high;
67. content hash mismatch.

Cases 1–2 require `INVALID_REQUEST_TYPE`; cases 3–13 require `SCENARIO_REFUSED`; cases 14–15 require `INVALID_OBSERVATION_COLLECTION`; case 16 requires `EMPTY_OBSERVATIONS`; cases 17–18 require `OBSERVATION_COUNT_MISMATCH`; cases 19–20 require `INVALID_OBSERVATION_TYPE`; cases 21–22 require `REFERENCE_MISMATCH`; cases 23–26 require `INVALID_INSTRUMENT_REFERENCE`; cases 27–29 require `INVALID_KIND`; cases 30–32 require `CONTENT_KIND_MISMATCH`; cases 33–40 require `INVALID_DECIMAL`; cases 41–44 require `INVALID_TRADE_CONTENT`; cases 45–51 require `INVALID_QUOTE_CONTENT`; cases 52–66 require `INVALID_BAR_CONTENT`; case 67 requires `CONTENT_HASH_MISMATCH`.

## Exact Output Contract

The accepted predecessor test file contains exactly 26 test methods. The new file must contain exactly 24. Combined discovery must report exactly 50 tests.

Elapsed time is environment-dependent and is not part of the deterministic evidence comparison. Required terminal summaries are:

```text
Ran 26 tests in <ELAPSED>

OK
```

```text
Ran 24 tests in <ELAPSED>

OK
```

```text
Ran 50 tests in <ELAPSED>

OK
```

Every command must exit `0`, produce no failure, error, skip, expected failure, unexpected success, warning, traceback, or subtest failure, and enumerate verbose test methods in source order within each module.

## Static Forbidden-Surface Contract

The production source must contain no operational import, call, or interface for:

- filesystem or environment access;
- credentials, secrets, keys, or tokens;
- network, socket, HTTP, websocket, polling, feeds, brokers, exchanges, wallets, chains, or market-data access;
- file parsing, acquisition, ingestion, buffering, normalization, deduplication, stale-data filtering, timestamp correction, or source resolution;
- replay, backtesting, optimization, tuning, prediction, confidence, signals, indicators, strategy, candidates, classification, enrichment, or risk;
- simulated action, orders, fills, execution, positions, portfolios, balances, funding, or capital;
- current clocks, sleep, randomness, queues, logging, caches, persistence, databases, services, workers, schedulers, CLIs, APIs, subprocesses, or commands;
- deployment, production activation, communication, or autonomous external action;
- shared mutable state, import-time side effects, or package re-exports; or
- Echoauth-core imports or copied implementation.

The static scan must parse imports and public definitions and distinguish forbidden operational behavior from closed-denial vocabulary inherited from Stage 4.1A references.

## Required Completion Evidence

The implementation lane must return:

- exact starting and resulting commits and parent relation;
- exact implementation branch and merge base;
- proof both authorized paths were absent before mutation;
- exact two-path diff and resulting blobs;
- exact production public surface, enum, dataclass, signature, import, and private-helper inventories;
- selected Python invocation, resolved executable path when available, and version;
- exact three commands and complete captured output;
- proof of 26, 24, and 50 successful tests;
- mapping of all 24 methods and 67 ordered negative cases to contract clauses;
- repeated-run deterministic equality evidence;
- canonical payload and hash examples for one trade, quote, and bar;
- exact preservation of Stage 4.1A source and test blobs;
- evidence both package `__init__.py` files and inherited governance files were unchanged;
- static forbidden-surface results;
- evidence Echoauth-core remained unchanged from the task-order checkpoint;
- evidence no historical Stage 4.1B implementation was merged, cherry-picked, restored, or used as authority;
- evidence no third path, dependency, fixture, schema, configuration, workflow, runtime, broker, credential, order, financial, database, persistence, deployment, production, communication, or external-integration surface changed;
- clean committed branch evidence; and
- terminal `WAIT` pending separately authorized independent implementation acceptance.

## Non-Authorization Boundary

This specification does not itself authorize implementation; implementation authority exists only through the inseparable task order and explicit owner authorization embodied by this lane.

Neither artifact authorizes contract correction, historical restoration, runtime orchestration, simulation activation, market-data access, ingestion, replay, backtesting, signals, strategy, candidates, risk, simulated actions, paper or live accounts, brokers, exchanges, wallets, credentials, orders, fills, execution, positions, portfolios, balances, capital, financial activity, database or filesystem persistence, deployment, production, communication, external integration, canonical synchronization, merge, Stage 4 readiness acceptance, Stage 4 closure, or Stage 5 entry.

## Final Specification Posture

`READY — EXACT IMPLEMENTATION REQUIREMENTS FROZEN; EXECUTION IS GOVERNED ONLY BY THE INSEPARABLE TASK ORDER AND MUST RETURN TO WAIT PENDING INDEPENDENT ACCEPTANCE.`
