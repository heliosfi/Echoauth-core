# Stage 4.1B Observation Implementation Specification

## Status

TECHNICAL SPECIFICATION ONLY -- STAGE 4 -- NON-RUNTIME -- NON-EXECUTION -- NOT AN IMPLEMENTATION ORDER

## Governing Inputs

This specification is subordinate to:

1. `sniperbot-stage-4.1b-multi-variant-observation-contract-specification.md`
2. `sniperbot-stage-4.1b-multi-variant-observation-contract-independent-acceptance.md`
3. the accepted Stage 4.1A scenario-envelope implementation and independent acceptance.

A contradiction requires refusal. This specification may not broaden the accepted contract.

## Exact Implementation Subject

Implement one deterministic, in-memory, simulation-only observation-content validator that consumes the existing Stage 4.1A `SimulationObservationReference`, validates one closed payload variant, canonicalizes the payload, calculates SHA-256, compares the digest with the reference, and returns an immutable decision.

## Exact Repository Surface

Proposed implementation repository:

`heliosfi/SniperBot`

Proposed new paths:

- `src/sniperbot/simulation/observation.py`
- `tests/test_simulation_observation.py`

No existing path is required to change. No package re-export is required.

## Exact Public Module

`sniperbot.simulation.observation`

## Exact Public API

The module public surface is exactly:

- `ObservationVariant`
- `ObservationValidationState`
- `ObservationRequiredAction`
- `ObservationReasonCode`
- `GenericEvidencePayload`
- `PricePayload`
- `QuotePayload`
- `BarPayload`
- `ObservationPayload`
- `ObservationValidationRequest`
- `ObservationValidationDecision`
- `validate_simulation_observation`

All helper names must begin with an underscore.

## Enums

### ObservationVariant

- `GENERIC_EVIDENCE = "generic_evidence"`
- `PRICE = "price"`
- `QUOTE = "quote"`
- `BAR = "bar"`

### ObservationValidationState

- `ACCEPTED = "accepted"`
- `REFUSED = "refused"`

### ObservationRequiredAction

- `CONTINUE_SIMULATION_ONLY = "continue_simulation_only"`
- `HALT = "halt"`

### ObservationReasonCode

The closed reason vocabulary is:

- `ACCEPTED`
- `REQUEST_TYPE_INVALID`
- `REFERENCE_TYPE_INVALID`
- `VARIANT_TYPE_INVALID`
- `PAYLOAD_TYPE_INVALID`
- `VARIANT_PAYLOAD_MISMATCH`
- `REFERENCE_SEQUENCE_INVALID`
- `REFERENCE_OBSERVED_AT_INVALID`
- `REFERENCE_SOURCE_INVALID`
- `REFERENCE_DIGEST_INVALID`
- `TEXT_FIELD_INVALID`
- `DECIMAL_TYPE_INVALID`
- `DECIMAL_NOT_FINITE`
- `PRICE_NOT_POSITIVE`
- `QUOTE_PRICE_ORDER_INVALID`
- `QUOTE_SIZE_PAIR_INVALID`
- `SIZE_NEGATIVE`
- `BAR_TIME_INVALID`
- `BAR_PRICE_COHERENCE_INVALID`
- `VOLUME_NEGATIVE`
- `CANONICALIZATION_FAILED`
- `PAYLOAD_DIGEST_MISMATCH`

No aliases or unknown reason strings are permitted.

## Frozen Dataclasses

### GenericEvidencePayload

Field order:

1. `evidence_type: str`
2. `subject_reference: str`
3. `value_text: str`
4. `unit_reference: str | None = None`

### PricePayload

Field order:

1. `instrument_reference: str`
2. `price: Decimal`
3. `currency_reference: str`

### QuotePayload

Field order:

1. `instrument_reference: str`
2. `bid_price: Decimal`
3. `ask_price: Decimal`
4. `currency_reference: str`
5. `bid_size: Decimal | None = None`
6. `ask_size: Decimal | None = None`

### BarPayload

Field order:

1. `instrument_reference: str`
2. `interval_reference: str`
3. `period_start: datetime`
4. `period_end: datetime`
5. `open_price: Decimal`
6. `high_price: Decimal`
7. `low_price: Decimal`
8. `close_price: Decimal`
9. `currency_reference: str`
10. `volume: Decimal | None = None`

### ObservationValidationRequest

Field order:

1. `reference: SimulationObservationReference`
2. `variant: ObservationVariant`
3. `payload: ObservationPayload`

### ObservationValidationDecision

Field order:

1. `state: ObservationValidationState`
2. `required_action: ObservationRequiredAction`
3. `reason_code: ObservationReasonCode`
4. `calculated_payload_sha256: str | None = None`

## Strict-Type Rules

Validation uses exact concrete type equality, not `isinstance`, for public request, reference, enum, and payload objects.

Strings must be exact `str`, non-empty, and unchanged. No trimming or normalization is permitted.

Numeric values must be exact `Decimal`. `int`, `float`, `bool`, strings, fractions, and subclasses are refused.

Datetime values must be exact `datetime`, timezone-aware, have `utcoffset() == timedelta(0)`, and retain UTC semantics. Naive and non-UTC values are refused.

## Payload Mapping

The only valid mapping is:

- `GENERIC_EVIDENCE` -> `GenericEvidencePayload`
- `PRICE` -> `PricePayload`
- `QUOTE` -> `QuotePayload`
- `BAR` -> `BarPayload`

Cross-variant payloads are refused.

## Deterministic Validation Order

The validator evaluates in this exact order and returns the first refusal:

1. request exact type;
2. reference exact type;
3. variant exact type;
4. payload belongs to the closed payload types;
5. variant-to-payload compatibility;
6. reference sequence exact integer and non-negative, with bool refused;
7. reference observed-at strict UTC datetime;
8. reference source reference strict non-empty string;
9. reference digest exact lowercase 64-character hexadecimal string;
10. shared payload string fields;
11. payload decimal exact types;
12. decimal finiteness;
13. variant-specific semantic rules;
14. deterministic canonicalization;
15. SHA-256 calculation;
16. exact digest comparison;
17. accepted decision.

No exception may be used as an accepted result. Unexpected canonicalization failure returns `CANONICALIZATION_FAILED` and `HALT`.

## Variant Semantics

### Generic Evidence

Required text fields must be valid. Optional `unit_reference` must be absent or a valid non-empty exact string. `value_text` remains opaque.

### Price

`price` must be finite and greater than zero.

### Quote

Bid and ask must be finite and greater than zero. Bid must not exceed ask. Bid size and ask size must be both absent or both present. Present sizes must be finite and greater than or equal to zero.

### Bar

Period start and end must be strict UTC. Require:

`period_start < period_end <= reference.observed_at`

All four prices must be finite and greater than zero. Require:

- `high_price >= open_price`
- `high_price >= close_price`
- `high_price >= low_price`
- `low_price <= open_price`
- `low_price <= close_price`

Present volume must be finite and greater than or equal to zero.

## Canonical Decimal Algorithm

For a finite `Decimal`:

1. normalize numerical zero to `"0"`;
2. render with fixed-point formatting;
3. remove trailing fractional zeros;
4. remove a trailing decimal point;
5. prohibit exponent notation;
6. never convert through float.

## Canonical Datetime Algorithm

Render strict UTC datetimes using:

`value.isoformat(timespec="microseconds")`

The output must include `+00:00`.

## Canonical Payload Field Order

### Generic Evidence

1. `evidence_type`
2. `subject_reference`
3. `value_text`
4. `unit_reference`

### Price

1. `instrument_reference`
2. `price`
3. `currency_reference`

### Quote

1. `instrument_reference`
2. `bid_price`
3. `ask_price`
4. `currency_reference`
5. `bid_size`
6. `ask_size`

### Bar

1. `instrument_reference`
2. `interval_reference`
3. `period_start`
4. `period_end`
5. `open_price`
6. `high_price`
7. `low_price`
8. `close_price`
9. `currency_reference`
10. `volume`

Absent optionals serialize as JSON null.

## Canonical JSON and Digest

Use equivalent behavior to:

```python
json.dumps(
    canonical_payload,
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=False,
)
```

Calculate:

```python
hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()
```

Accepted decisions return the calculated digest. Refused decisions return `None` for the calculated digest.

## Required Tests

Tests must prove:

- exact public surface;
- exact enum values and no aliases;
- frozen dataclasses and field order;
- exact-type refusal including subclasses and bool-as-int;
- all four accepted variants;
- every cross-variant mismatch;
- strict strings, Decimal values, and UTC datetimes;
- generic-evidence optional behavior;
- positive-price rules;
- quote ordering and size pairing;
- bar temporal and OHLC coherence;
- volume and size non-negativity;
- decimal canonicalization including exponent forms and negative zero;
- six-digit UTC datetime rendering;
- Unicode preservation;
- optional null serialization;
- deterministic canonical JSON and digest;
- digest sensitivity to each semantic field;
- digest mismatch refusal;
- exact first-match refusal precedence;
- no digest on refusal;
- repeated-input determinism;
- Stage 4.1A regression remains passing;
- no external-effect imports or surfaces.

## Locked Exclusions

The implementation must not introduce:

- filesystem, fixture, environment, clock, random, socket, HTTP, websocket, subprocess, database, logging, or persistence access;
- feeds, polling, ingestion, replay, adapters, or providers;
- signals, strategies, confidence, risk, ranking, intent, candidate selection, action, outcome, order, fill, broker, account, or capital concepts;
- runtime orchestration, activation, deployment, credentials, or secrets;
- third-party dependencies;
- modifications outside the two proposed paths.

## Review Determination

- semantic translation: COMPLETE
- deterministic algorithm: FIXED
- public API: FIXED
- test obligations: FIXED
- architectural boundaries: PRESERVED
- bounded-task readiness: PASS
- implementation authority created by this specification: NONE

`IMPLEMENTATION SPECIFICATION COMPLETE -- BOUNDED TASK ORDER MAY BE PREPARED -- WAIT`
