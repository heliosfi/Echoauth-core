# Stage 4.1B Multi-Variant Observation Contract Specification

## Status

GOVERNANCE SPECIFICATION ONLY -- STAGE 4 -- NON-RUNTIME -- NON-EXECUTION

## Authority and Scope

Founder Nicholas B. Carty authorized specification of a closed multi-variant observation model for the SniperBot Stage 4 simulation lane.

This specification creates no implementation, runtime, ingestion, replay, strategy, risk, broker, order, fill, deployment, or external-action authority.

## Exact Subject

Define deterministic caller-supplied simulation observation content compatible with the accepted Stage 4.1A `SimulationObservationReference` boundary.

## Closed Variant Vocabulary

The complete vocabulary is:

1. `generic_evidence`
2. `price`
3. `quote`
4. `bar`

Unknown variants, plugin registration, subclass extension, arbitrary dictionaries, and open-ended payload types are prohibited.

## Shared Reference Boundary

Every content payload is bound to the existing Stage 4.1A reference fields:

- `sequence`
- `observed_at`
- `source_reference`
- `payload_sha256`

The Stage 4.1B component must consume that type without copying, redefining, or modifying it.

## Payload Contracts

### Generic Evidence

Required fields:

- `evidence_type: str`
- `subject_reference: str`
- `value_text: str`
- `unit_reference: str | None`

All values remain caller-supplied and opaque. `value_text` is not parsed.

### Price

Required fields:

- `instrument_reference: str`
- `price: Decimal`
- `currency_reference: str`

Price must be finite and greater than zero.

### Quote

Required fields:

- `instrument_reference: str`
- `bid_price: Decimal`
- `ask_price: Decimal`
- `currency_reference: str`
- `bid_size: Decimal | None`
- `ask_size: Decimal | None`

Bid and ask must be finite and positive. Bid must not exceed ask. Sizes must both be absent or both present. Present sizes must be finite and non-negative.

### Bar

Required fields:

- `instrument_reference: str`
- `interval_reference: str`
- `period_start: datetime`
- `period_end: datetime`
- `open_price: Decimal`
- `high_price: Decimal`
- `low_price: Decimal`
- `close_price: Decimal`
- `currency_reference: str`
- `volume: Decimal | None`

Period timestamps must be strict UTC and satisfy `period_start < period_end <= observed_at`. Prices must be finite and positive. High must be greater than or equal to open, close, and low. Low must be less than or equal to open and close. Present volume must be finite and non-negative.

## Canonicalization Contract

Canonical payloads must use fixed field order, UTF-8, JSON separators `(',', ':')`, `ensure_ascii=False`, and `sort_keys=False`.

Decimals must be canonical finite fixed-point strings with trailing fractional zeros removed, no trailing decimal point, and all numerical zero forms normalized to `0`. Conversion through binary floating point is prohibited.

UTC datetimes must use ISO 8601 with six fractional digits and `+00:00`.

The payload digest is lowercase SHA-256 over the canonical JSON bytes.

## Validation Decision

The closed decision vocabulary is:

- state: `accepted` or `refused`
- required action: `continue_simulation_only` or `halt`

Accepted decisions may expose the calculated digest. Refused decisions must not expose a partially calculated digest.

Validation is deterministic and first-match. Invalid caller data must fail closed without coercion.

## Compatibility Rule

The calculated payload digest must equal the supplied Stage 4.1A `payload_sha256`. Digest mismatch requires refusal and halt.

Stage 4.1B does not replace scenario validation, sequence ordering, scenario fingerprinting, or isolation validation.

## Locked Exclusions

This contract authorizes no:

- file or fixture reading;
- feed, websocket, polling, ingestion, or replay;
- market access;
- signal, strategy, confidence, risk, or candidate-intent evaluation;
- simulated action, outcome, order, fill, broker, account, or capital surface;
- persistence, logging, network, subprocess, environment, clock, randomness, deployment, or runtime activation.

## Final Posture

- contract semantics: SPECIFIED
- Stage 4: OPEN
- implementation authority: NONE BY THIS SPECIFICATION
- runtime authority: NONE
- next permissible governance action: independent contract acceptance review
