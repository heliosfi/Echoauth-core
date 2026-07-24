# Implementation Specification 4.1A-SPEC — Deterministic Simulation Scenario Envelope and Isolation Validator

## Issuance Authority

This specification is durably issued by Founder Order 10G as a governing artifact. Founder Order 10G does not authorize execution of this specification.

Implementation may begin only under a later, separate Founder Order.

## 1. Scope

This specification defines the complete technical contract for one pure Python implementation subject:

**Deterministic Simulation Scenario Envelope and Isolation Validator**

The component accepts only caller-supplied in-memory values, validates that the scenario is simulation-only and fully isolated, and returns one immutable decision.

It performs no I/O, runtime activation, market analysis, trading logic, persistence, logging, routing, or external action.

## 2. Exact Public Module

`sniperbot.simulation.scenario`

## 3. Exact Public API

The module must expose exactly these public symbols:

1. `SimulationMode`
2. `ScenarioValidationState`
3. `ScenarioReasonCode`
4. `ScenarioRequiredAction`
5. `SimulationObservationReference`
6. `SimulationIsolationBoundary`
7. `SimulationScenarioRequest`
8. `ScenarioValidationDecision`
9. `validate_simulation_scenario`

No other public class, enum, function, mutable constant, runtime object, or service interface is authorized.

Private helpers must begin with `_` and may exist only when directly necessary for validation or canonical fingerprint generation.

## 4. Enum Contracts

All enums must inherit from `str` and `Enum`.

### 4.1 `SimulationMode`

```python
SIMULATION_ONLY = "simulation_only"
```

No other mode is permitted.

### 4.2 `ScenarioValidationState`

```python
ACCEPTED = "accepted"
REFUSED = "refused"
```

### 4.3 `ScenarioRequiredAction`

```python
CONTINUE_SIMULATION_ONLY = "continue_simulation_only"
HALT = "halt"
```

### 4.4 `ScenarioReasonCode`

```python
ACCEPTED = "accepted"
INVALID_REQUEST_TYPE = "invalid_request_type"
INVALID_MODE = "invalid_mode"
ISOLATION_VIOLATION = "isolation_violation"
INVALID_SCENARIO_REFERENCE = "invalid_scenario_reference"
INVALID_PROVENANCE_REFERENCE = "invalid_provenance_reference"
INVALID_SEED = "invalid_seed"
INVALID_CLOCK_START = "invalid_clock_start"
INVALID_OBSERVATION_COLLECTION = "invalid_observation_collection"
EMPTY_OBSERVATIONS = "empty_observations"
INVALID_OBSERVATION_TYPE = "invalid_observation_type"
INVALID_OBSERVATION_SEQUENCE = "invalid_observation_sequence"
INVALID_OBSERVATION_TIMESTAMP = "invalid_observation_timestamp"
INVALID_SOURCE_REFERENCE = "invalid_source_reference"
INVALID_PAYLOAD_HASH = "invalid_payload_hash"
```

No free-form reason value is permitted.

## 5. Immutable Data Contracts

All data contracts must be frozen dataclasses.

Field names and field order are exact.

### 5.1 `SimulationObservationReference`

```python
@dataclass(frozen=True)
class SimulationObservationReference:
    sequence: int
    observed_at: datetime
    source_reference: str
    payload_sha256: str
```

Validation requirements:

- `type(sequence) is int`;
- `sequence > 0`;
- `observed_at` must be an exact `datetime`;
- `observed_at` must be timezone-aware;
- `observed_at.utcoffset()` must equal zero;
- `source_reference` must be an exact `str`;
- `source_reference` must be nonempty;
- `source_reference == source_reference.strip()`;
- `payload_sha256` must be an exact `str`;
- it must match exactly `[0-9a-f]{64}`.

Dataclass construction itself must not perform validation or external work. Validation belongs in the validation function.

### 5.2 `SimulationIsolationBoundary`

```python
@dataclass(frozen=True)
class SimulationIsolationBoundary:
    network_allowed: bool = False
    broker_allowed: bool = False
    credential_access_allowed: bool = False
    paper_account_allowed: bool = False
    live_account_allowed: bool = False
    live_order_allowed: bool = False
    capital_allowed: bool = False
    deployment_allowed: bool = False
    external_side_effect_allowed: bool = False
```

Each field must be exactly `False`.

Any value that is not exactly `False`, including truthy non-Booleans, is an isolation violation.

No permissive isolation state is authorized.

### 5.3 `SimulationScenarioRequest`

```python
@dataclass(frozen=True)
class SimulationScenarioRequest:
    scenario_reference: str
    provenance_reference: str
    deterministic_seed: int
    clock_start: datetime
    mode: SimulationMode
    isolation: SimulationIsolationBoundary
    observations: tuple[SimulationObservationReference, ...]
```

Validation requirements:

- `scenario_reference` must be exact `str`, nonempty, and trimmed;
- `provenance_reference` must be exact `str`, nonempty, and trimmed;
- `type(deterministic_seed) is int`;
- Boolean seeds are invalid;
- `clock_start` must be exact `datetime`;
- `clock_start` must be timezone-aware UTC with zero offset;
- `mode is SimulationMode.SIMULATION_ONLY`;
- `type(isolation) is SimulationIsolationBoundary`;
- `type(observations) is tuple`;
- observations must be nonempty;
- every item must have exact type `SimulationObservationReference`;
- sequences must be positive, unique, and strictly increasing in tuple order;
- timestamps must be monotonically nondecreasing in tuple order;
- no observation timestamp may precede `clock_start`;
- every source reference and payload hash must satisfy its contract.

### 5.4 `ScenarioValidationDecision`

```python
@dataclass(frozen=True)
class ScenarioValidationDecision:
    state: ScenarioValidationState
    reason: ScenarioReasonCode
    required_action: ScenarioRequiredAction
    scenario_reference: str
    observation_count: int
    scenario_fingerprint: str | None
```

Accepted decision:

- `state is ScenarioValidationState.ACCEPTED`;
- `reason is ScenarioReasonCode.ACCEPTED`;
- `required_action is ScenarioRequiredAction.CONTINUE_SIMULATION_ONLY`;
- `scenario_reference` equals the validated request value;
- `observation_count == len(request.observations)`;
- `scenario_fingerprint` is exactly 64 lowercase hexadecimal characters.

Refused decision:

- `state is ScenarioValidationState.REFUSED`;
- `reason` is the first applicable refusal reason;
- `required_action is ScenarioRequiredAction.HALT`;
- `scenario_reference` is included only when it can be safely obtained as an exact, nonempty, trimmed string; otherwise `""`;
- `observation_count` is included only after an exact tuple has been established; otherwise `0`;
- `scenario_fingerprint is None`.

## 6. Validation Function

Exact signature:

```python
def validate_simulation_scenario(
    request: SimulationScenarioRequest,
) -> ScenarioValidationDecision:
    ...
```

The function must:

- be deterministic;
- be pure;
- mutate no input;
- use no shared mutable state;
- perform no I/O;
- raise no exception for ordinary invalid input;
- return exactly one immutable decision;
- apply the exact refusal precedence below;
- generate a fingerprint only after all validation passes.

Programming defects and unrecoverable interpreter failures are outside the ordinary refusal contract and must not be silently hidden.

## 7. Exact Refusal Precedence

The first applicable condition must determine the result:

1. `INVALID_REQUEST_TYPE`
2. `INVALID_MODE`
3. `ISOLATION_VIOLATION`
4. `INVALID_SCENARIO_REFERENCE`
5. `INVALID_PROVENANCE_REFERENCE`
6. `INVALID_SEED`
7. `INVALID_CLOCK_START`
8. `INVALID_OBSERVATION_COLLECTION`
9. `EMPTY_OBSERVATIONS`
10. `INVALID_OBSERVATION_TYPE`
11. `INVALID_OBSERVATION_SEQUENCE`
12. `INVALID_OBSERVATION_TIMESTAMP`
13. `INVALID_SOURCE_REFERENCE`
14. `INVALID_PAYLOAD_HASH`
15. `ACCEPTED`

No warning, exception, list of reasons, or alternate precedence is permitted.

### 7.1 Invalid Request Type

Refuse when:

```python
type(request) is not SimulationScenarioRequest
```

### 7.2 Invalid Mode

Refuse unless:

```python
request.mode is SimulationMode.SIMULATION_ONLY
```

A raw string equal to `"simulation_only"` is not sufficient.

### 7.3 Isolation Violation

Refuse unless:

```python
type(request.isolation) is SimulationIsolationBoundary
```

and every isolation field is exactly `False`.

### 7.4 Invalid Scenario Reference

Refuse unless the value is exact `str`, nonempty, and trimmed.

### 7.5 Invalid Provenance Reference

Refuse unless the value is exact `str`, nonempty, and trimmed.

### 7.6 Invalid Seed

Refuse unless:

```python
type(request.deterministic_seed) is int
```

No numeric range restriction is imposed beyond exact integer type.

### 7.7 Invalid Clock Start

Refuse unless:

- exact `datetime`;
- timezone-aware;
- UTC offset exactly zero.

### 7.8 Invalid Observation Collection

Refuse unless:

```python
type(request.observations) is tuple
```

Lists, generators, mappings, sets, iterators, and tuple subclasses are invalid.

### 7.9 Empty Observations

Refuse when the exact tuple is empty.

### 7.10 Invalid Observation Type

Refuse when any item is not exact type `SimulationObservationReference`.

### 7.11 Invalid Observation Sequence

Refuse when any sequence:

- is not exact `int`;
- is Boolean;
- is zero or negative;
- duplicates an earlier sequence;
- is not strictly greater than the immediately prior sequence.

### 7.12 Invalid Observation Timestamp

Refuse when any timestamp:

- is not exact `datetime`;
- is naive;
- has nonzero UTC offset;
- precedes `clock_start`;
- is earlier than the immediately prior observation timestamp.

Equal adjacent timestamps are permitted.

### 7.13 Invalid Source Reference

Refuse when any source reference is not exact `str`, is empty, or is not trimmed.

### 7.14 Invalid Payload Hash

Refuse when any payload hash is not exact `str` or does not match exactly:

```text
[0-9a-f]{64}
```

## 8. Fingerprint Contract

A fingerprint is created only for accepted requests.

Algorithm:

```text
SHA-256(UTF-8(canonical JSON))
```

The canonical JSON structure must contain fields in this exact logical order:

1. `scenario_reference`
2. `provenance_reference`
3. `deterministic_seed`
4. `clock_start`
5. `mode`
6. `isolation`
7. `observations`

The isolation object must contain fields in dataclass order.

Each observation object must contain:

1. `sequence`
2. `observed_at`
3. `source_reference`
4. `payload_sha256`

Canonical JSON requirements:

- UTF-8 encoding;
- compact separators;
- stable ordering;
- no whitespace variability;
- no object-identity values;
- no dictionary-order dependence;
- no machine-specific values;
- no environment values;
- no live clock;
- no random values;
- no filesystem values.

Timestamps must be represented as UTC ISO-8601 strings with an explicit `+00:00` offset.

Semantically identical accepted requests must produce identical fingerprint bytes.

Any material accepted-input difference must change the fingerprint, including:

- either reference;
- seed;
- clock start;
- any isolation value;
- observation order;
- observation sequence;
- observation timestamp;
- observation source reference;
- observation payload hash.

## 9. Permitted Imports

Production code may import only directly necessary names from:

- `dataclasses`
- `datetime`
- `enum`
- `hashlib`
- `json`
- `re`
- `typing`

No third-party import is permitted.

Tests may additionally use:

- `unittest`;
- standard-library reflection or source-inspection facilities required for static checks.

## 10. Forbidden Production Surfaces

Production code must not import, access, reference, open, create, mutate, or invoke:

- filesystem paths or file readers;
- environment variables;
- current-time or live-clock functions;
- random or secrets sources;
- sockets or networking;
- HTTP clients;
- subprocesses;
- databases or persistence;
- logging;
- queues or event buses;
- services, workers, schedulers, loops, CLIs, or APIs;
- market-data feeds;
- historical-data ingestion;
- replay or backtesting;
- signal or indicator computation;
- strategy selection;
- candidate formation;
- confidence scoring;
- risk or sizing logic;
- state-transition or eligibility logic;
- actions, orders, fills, positions, portfolios, balances, or prices;
- brokers, exchanges, accounts, wallets, or paper accounts;
- credentials, secrets, keys, or tokens;
- routing, submission, cancellation, or execution;
- capital or funding;
- deployment or production activation;
- autonomous or external command execution.

## 11. Required Tests

`tests/test_simulation_scenario.py` must directly test all of the following.

### 11.1 API and Immutability

- exact public symbol set;
- no package-root re-export;
- no `sniperbot.simulation` re-export;
- exact enum members and values;
- exact dataclass fields and field order;
- frozen dataclass behavior;
- isolation defaults all exactly `False`.

### 11.2 Accepted Behavior

- one valid request is accepted;
- accepted state, reason, and required action are exact;
- scenario reference is preserved;
- observation count is exact;
- fingerprint matches lowercase SHA-256 form;
- repeated validation returns equal decisions;
- equal independent objects produce equal fingerprints;
- no input mutation occurs;
- no shared mutable state appears.

### 11.3 Fingerprint Sensitivity

Independently verify fingerprint change for each material input difference:

- scenario reference;
- provenance reference;
- seed;
- clock start;
- each isolation field when represented in a directly tested canonical helper or accepted-equivalent contract;
- observation order;
- sequence;
- timestamp;
- source reference;
- payload hash.

Because accepted scenarios require all isolation fields to be false, tests may verify isolation-field inclusion through the private canonicalization helper if one exists. No accepted permissive isolation request may be introduced.

### 11.4 Refusal Cases

Directly test:

- invalid request object;
- raw-string mode;
- every isolation field independently set to an invalid value;
- invalid isolation object type;
- empty scenario reference;
- whitespace-padded scenario reference;
- non-string scenario reference;
- empty provenance reference;
- whitespace-padded provenance reference;
- non-string provenance reference;
- Boolean seed;
- non-integer seed;
- naive clock;
- non-UTC clock;
- non-datetime clock;
- list observations;
- generator observations;
- mapping observations;
- set observations;
- tuple subclass observations;
- empty tuple;
- invalid observation member type;
- Boolean sequence;
- zero sequence;
- negative sequence;
- duplicate sequence;
- decreasing sequence;
- equal sequence;
- naive observation timestamp;
- non-UTC observation timestamp;
- non-datetime observation timestamp;
- timestamp before scenario clock;
- decreasing timestamp;
- empty source reference;
- padded source reference;
- non-string source reference;
- uppercase hash;
- short hash;
- long hash;
- non-hex hash;
- non-string hash.

### 11.5 Refusal Decision Shape

For refusal decisions verify:

- state is `REFUSED`;
- required action is `HALT`;
- fingerprint is `None`;
- safe scenario-reference preservation rule;
- observation-count preservation only after exact tuple establishment.

### 11.6 Exact Precedence

Create multi-defect requests proving each earlier condition dominates every later applicable condition.

At minimum, directly prove the entire ordered chain by paired or cumulative cases so the test inventory demonstrates all fourteen refusal positions.

### 11.7 Static Forbidden-Surface Scan

Inspect the production source and confirm absence of forbidden imports and forbidden operational surfaces.

The scan must avoid naive substring checks that would falsely reject authorized dataclass field names such as `broker_allowed`. It must distinguish closed denial fields from operational APIs or imports.

## 12. Required Validation Command

```powershell
$env:PYTHONPATH = "src"
<PYTHON3> -m unittest discover -s tests -p "test_simulation_scenario.py" -v
```

## 13. Exact Path Boundary

Only these paths may exist in the implementation commit:

1. `src/sniperbot/__init__.py`
2. `src/sniperbot/simulation/__init__.py`
3. `src/sniperbot/simulation/scenario.py`
4. `tests/test_simulation_scenario.py`

No schema, fixture, manifest, dependency, configuration, workflow, runtime, CLI, API, service, or documentation file is part of the implementation commit.

## 14. Completion Standard

The implementation is technically complete only when:

- every required test passes;
- exact public API is proven;
- exact refusal precedence is proven;
- deterministic fingerprint behavior is proven;
- forbidden surfaces are absent;
- the complete diff contains exactly four paths;
- Echoauth-core is unchanged;
- publication and synchronization checks pass.

Technical completion does not equal governance acceptance.

## 15. Non-Authorization Boundary

This specification does not authorize:

- simulation activation;
- replay or backtesting;
- market-data access;
- trading decisions;
- risk decisions;
- mock or real orders;
- account or broker access;
- credentials;
- capital;
- deployment;
- production;
- autonomous external action;
- acceptance;
- Stage 4 closure;
- Stage 5 entry.
