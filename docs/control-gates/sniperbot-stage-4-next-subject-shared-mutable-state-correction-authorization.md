# SniperBot Stage 4 Next-Subject Shared-Mutable-State Correction Authorization

## Authorization Disposition

**AUTHORIZED — ONE BOUNDED TWO-FILE IMPLEMENTATION CORRECTION MAY PROCEED**

This record makes the failed independent implementation-acceptance evidence durable and issues a single-use correction order for one exact defect in:

> **Deterministic Typed Fixture Scenario Content and Provenance Validator**

The implementation exists but is not accepted.

## Owner Authority

Nicholas B. Carty assessed and authorized the **SniperBot Stage 4 Next-Subject Shared-Mutable-State Correction Authorization** lane.

This authority permits exactly this Echoauth-core correction record. It authorizes the later bounded SniperBot correction described below but does not itself mutate SniperBot, accept the implementation, move either canonical branch, or authorize adjacent work.

## Exact Formation Evidence

### Echoauth-core

- repository: `heliosfi/Echoauth-core`;
- formation branch: `sniperbot-stage-4-next-subject-shared-mutable-state-correction-authorization`;
- exact formation parent: `f6d302d1aa79742eb1cf394cac093d2551053150`;
- implementation specification blob: `e0fda56c367c41c48c58ca8f117099de2a298624`;
- prior implementation task-order blob: `92a975c0b36c2d3785cbc629a84ebb0dc8f4d5d0`;
- publication-mechanism correction and reissue blob: `9601c995cd722ebe912fd2477607631ec77560d4`;
- canonical Echoauth-core `main` observed at formation: `5c6faea46932836fbb8f04d8a1435298ca8a62b2`.

### SniperBot

- repository: `heliosfi/sniperbot`;
- implementation branch: `sniperbot-stage-4-next-subject-implementation`;
- implementation base and merge base: `998e2d2e91ecb758e084aad0112fd58608dcdb61`;
- production commit: `7a2e2da0de0b6748d54fe4dd82248456cf6ef5f6`;
- final implementation commit and correction base: `b4bf29f8b757fab9e57c2755be0039e1816a96f7`;
- production blob: `d85c80a61eb2dfce32a5281a31c60e6748c72c6e`;
- test blob: `09afa8d2f43f48fe8f9757a46596b4761f2592c8`;
- accepted Stage 4.1A source blob: `d4a8664cc9ec49b9caffd30157ab6992597fef79`;
- accepted Stage 4.1A test blob: `bfe34ff805e66149dc0de4ee8d9d85ee1efd9804`;
- accepted contract blob: `8fe287db830505dfbc59664ad78dbed60f6baec6`;
- independent contract-acceptance blob: `129d8e2777cac10314103d7c0de747e43afd4b25`;
- canonical SniperBot `main` observed at formation: `36c34e363619ccf3f859631820dd12ca1bcf5001`.

## Durable Independent Failure Finding

The independent implementation acceptance review reconstructed the final committed implementation from exact repository bytes and independently verified:

- exact two-commit, two-file ancestry;
- exact production and test blobs;
- preservation of Stage 4.1A blobs and package initializers;
- Python `3.12.13` selected through the closed interpreter procedure;
- 26 predecessor tests: `OK`;
- 24 new tests: `OK`;
- 50 combined tests: `OK`;
- all 67 ordered negative cases: passed;
- API, enums, frozen dataclasses, canonicalization, hashing, evidence shapes, reason precedence, imports, and forbidden operational surfaces: otherwise aligned.

Acceptance was correctly withheld because production blob `d85c80a61eb2dfce32a5281a31c60e6748c72c6e` contains `_CONTENT_FIELDS` as a module-level mutable `dict` used directly by canonical payload construction.

The independent reviewer proved behavioral consequence:

1. an exact request produced `ACCEPTED / accepted`;
2. `_CONTENT_FIELDS[FixtureObservationKind.TRADE]` was changed from `("price", "quantity")` to `("quantity", "price")`;
3. the same request then produced `REFUSED / content_hash_mismatch`.

Therefore the same caller-supplied request can produce different decisions after mutation of shared module state. This violates the accepted requirements for deterministic behavior and freedom from shared mutable runtime state.

Existing `test_22_no_shared_mutable_runtime_state` is insufficient because it inspects only values named in public `__all__`; it does not inspect private module globals that affect production behavior.

No acceptance branch, commit, blob, or record was created. The independent review mutated no repository state.

## Exact Correction Subject

Correct only:

**Shared mutable canonical-field dispatch and incomplete private-global validation.**

No contract, architecture, API, enum, dataclass, validation order, content invariant, canonical representation, digest, accepted output, refused output, test-method inventory, negative-case inventory, import permission, or non-authorization term may change.

## Exact Correction Repository and Branch

- repository: `heliosfi/sniperbot`;
- exact starting checkpoint: `b4bf29f8b757fab9e57c2755be0039e1816a96f7`;
- required branch: `sniperbot-stage-4-next-subject-shared-mutable-state-correction`;
- required merge base: exact starting checkpoint;
- publication: connector-native ordered two-commit sequence.

## Exact Authorized Paths

Modify exactly:

1. `src/sniperbot/simulation/fixture_observation.py`;
2. `tests/test_fixture_observation.py`.

No other path may be created, modified, deleted, renamed, reformatted, regenerated, or re-exported.

## Exact Production Correction

The correction must:

1. remove module-level mutable `_CONTENT_FIELDS` completely;
2. replace it with private function-local immutable tuple dispatch;
3. preserve exact field order:
   - trade: `("price", "quantity")`;
   - quote: `("bid_price", "bid_quantity", "ask_price", "ask_quantity")`;
   - bar: `("open_price", "high_price", "low_price", "close_price", "volume", "interval_seconds")`;
4. return or construct only immutable tuples;
5. add no mutable module-level list, dictionary, set, bytearray, mutable dataclass instance, cache, registry, accumulator, or other behavior-bearing container;
6. preserve the exact eleven-symbol `__all__` tuple;
7. preserve canonical payload bytes and hashes for every previously accepted input; and
8. preserve all prior accepted and refused decisions except removal of susceptibility to shared-state mutation.

Permitted implementation shape:

```python
def _content_fields(kind: FixtureObservationKind) -> tuple[str, ...]:
    if kind is FixtureObservationKind.TRADE:
        return ("price", "quantity")
    if kind is FixtureObservationKind.QUOTE:
        return (
            "bid_price",
            "bid_quantity",
            "ask_price",
            "ask_quantity",
        )
    return (
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume",
        "interval_seconds",
    )
```

An equivalent function-local immutable tuple dispatch is permitted only if it preserves these exact semantics and introduces no shared mutable state.

## Exact Test Correction

Keep exactly one `unittest.TestCase` subclass and the same exact 24 test-method names and order.

Modify only the body of:

`test_22_no_shared_mutable_runtime_state`

The strengthened method must:

1. inspect every non-dunder module global using `vars(fixture_module)`;
2. exclude only names beginning with `__`;
3. fail if any remaining value is an instance of `dict`, `list`, `set`, or `bytearray`;
4. continue proving repeated calls return equal but distinct immutable decisions;
5. assert `_CONTENT_FIELDS` is absent;
6. prove canonical field dispatch returns immutable tuples in exact trade, quote, and bar field order; and
7. prove no caller-visible mutation path can alter canonical field order or change repeated validation results.

No new test method, renamed method, deleted method, second `TestCase`, skip, expected failure, or weakened assertion is permitted.

## Exact Publication Sequence

### Commit 1 — production correction

- parent: `b4bf29f8b757fab9e57c2755be0039e1816a96f7`;
- changed path: only `src/sniperbot/simulation/fixture_observation.py`;
- operation: update existing file;
- message: `Remove shared mutable fixture field state`.

### Commit 2 — regression strengthening

- parent: exact Commit 1 result;
- changed path: only `tests/test_fixture_observation.py`;
- operation: update existing file;
- message: `Test private fixture module state immutability`.

Final aggregate comparison against `b4bf29f8b757fab9e57c2755be0039e1816a96f7` must show exactly two commits, exactly two modified paths, zero additions, zero deletions, zero renames, and exact merge base.

## Required Validation

Before Commit 1 and after Commit 2 committed-byte refetch, use the first qualifying interpreter from the existing closed list and run the unchanged exact commands.

Require:

- predecessor suite: exactly 26 tests and `OK`;
- corrected suite: exactly 24 tests and `OK`;
- combined suite: exactly 50 tests and `OK`;
- all 67 ordered negative cases pass;
- public API and package non-reexports unchanged;
- canonical payload and hash examples unchanged;
- the independent mutation proof can no longer be performed because `_CONTENT_FIELDS` is absent;
- no non-dunder mutable module container exists;
- committed correction bytes equal validated candidate bytes;
- Stage 4.1A, contract, acceptance, and inherited governance blobs remain preserved.

## Consumption Boundary

This correction order is consumed by the first successful remote production-correction commit. After that commit, authority permits only the exact test-correction commit.

Any failure, conflicting state, unexpected path, or need for a third commit requires immediate `WAIT`, `FAIL`, or `BLOCKED`. No deletion, force update, amendment, retry, alternate path, or additional correction is authorized.

## Required Completion Evidence

Report:

- final correction-authorization commit and blob;
- exact correction base and branch;
- Commit 1 and Commit 2 checkpoints and parent relations;
- corrected production and test blobs;
- aggregate two-commit/two-modified-path comparison;
- exact interpreter identity;
- pre-publication and committed-byte 26/24/50 outputs;
- all 67 ordered case results;
- exact removal of `_CONTENT_FIELDS`;
- complete non-dunder mutable-global scan result;
- canonical byte/hash preservation evidence;
- Stage 4.1A and governing-blob preservation;
- absence of any third path, commit, runtime, or external surface; and
- terminal posture `WAIT — CORRECTED, PENDING FRESH INDEPENDENT ACCEPTANCE`.

## Fresh Independent Acceptance Requirement

Correction completion is not acceptance.

A new independently authorized reviewer must bind the correction base, both correction commits, corrected source and test blobs, this authorization commit and blob, the accepted contract, the implementation specification, the publication reissue, and all predecessor evidence.

The implementation remains unaccepted until that fresh review passes and creates its own exact acceptance record.

## Non-Authorization Boundary

This order grants no authority for:

- contract, specification, or unrelated task-order changes;
- any third implementation path or test method;
- historical Stage 4.1B inspection, restoration, copying, merging, or reuse;
- pull request, merge, canonical synchronization, or movement of `main`;
- implementation acceptance;
- runtime orchestration, simulation activation, market-data access, ingestion, replay, backtesting, signals, strategy, candidates, classification, risk, simulated actions, brokers, accounts, credentials, orders, fills, execution, positions, portfolios, balances, funding, capital, or financial action;
- filesystem or database persistence;
- deployment, production, communication, external integration, or autonomous action;
- Stage 4 readiness acceptance or closure; or
- Stage 5 entry.

## Final Determination

`PASS — THE INDEPENDENT FAILURE IS DURABLY RECORDED AND ONE EXACT TWO-FILE SHARED-MUTABLE-STATE CORRECTION IS AUTHORIZED WITHOUT ALTERING THE ACCEPTED CONTRACT OR ANY ADJACENT AUTHORITY.`

## Post-Authorization Posture

`AUTHORIZED — ONE CONNECTOR-NATIVE TWO-COMMIT CORRECTION MAY PROCEED; RETURN TO WAIT PENDING FRESH INDEPENDENT IMPLEMENTATION ACCEPTANCE.`
