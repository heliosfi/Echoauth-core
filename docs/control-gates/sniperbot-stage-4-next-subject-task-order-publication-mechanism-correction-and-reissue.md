# SniperBot Stage 4 Next-Subject Task-Order Publication-Mechanism Correction and Reissue

## Reissue Disposition

**PASS — PUBLICATION MECHANISM CORRECTED; SINGLE-USE IMPLEMENTATION TASK ORDER REISSUED**

This record corrects one disproven transport assumption in the task order at commit:

`9a19d29cad6925da46a31a05b3ad58af0d447a41`

Prior task-order blob:

`92a975c0b36c2d3785cbc629a84ebb0dc8f4d5d0`

The prior order required exactly one implementation commit containing both authorized files and required a stop if the available connector could not publish that atomic two-file commit. During the authorized implementation attempt, the connected GitHub capability proved that it can create each file safely through the contents API but does not expose the parent tree identity required to synthesize one atomic two-file commit.

The implementation itself passed its exact local validation contract, and no remote SniperBot branch or repository byte changed. The defect is therefore limited to publication mechanics, not contract scope, implementation behavior, evidence lineage, or repository state.

## Owner Authority

Nicholas B. Carty authorized the necessary upgrade after assessing that the governing sequence remained aligned and that the publication transport rule was narrower than the meaningful safety boundary.

This authority permits exactly this immutable correction-and-reissue record. It preserves the accepted contract and implementation specification and reissues the implementation task order only with the publication and consumption rules below.

## Exact Formation Evidence

- governing repository: `heliosfi/Echoauth-core`;
- formation branch: `sniperbot-stage-4-next-subject-task-order-publication-reissue`;
- exact formation parent: `9a19d29cad6925da46a31a05b3ad58af0d447a41`;
- preserved implementation specification blob: `e0fda56c367c41c48c58ca8f117099de2a298624`;
- prior task-order blob: `92a975c0b36c2d3785cbc629a84ebb0dc8f4d5d0`;
- accepted SniperBot contract checkpoint: `fb2b26aaad63e17dce7b8b76b0ca92b9b70cd149`;
- accepted contract blob: `8fe287db830505dfbc59664ad78dbed60f6baec6`;
- independent contract-acceptance checkpoint and implementation base: `998e2d2e91ecb758e084aad0112fd58608dcdb61`;
- independent acceptance-record blob: `129d8e2777cac10314103d7c0de747e43afd4b25`;
- accepted Stage 4.1A source blob: `d4a8664cc9ec49b9caffd30157ab6992597fef79`;
- accepted Stage 4.1A test blob: `bfe34ff805e66149dc0de4ee8d9d85ee1efd9804`;
- canonical SniperBot `main` observed at reissue: `36c34e363619ccf3f859631820dd12ca1bcf5001`;
- canonical Echoauth-core `main` observed at reissue: `5c6faea46932836fbb8f04d8a1435298ca8a62b2`.

## Preserved Contract

Every technical, behavioral, validation, evidence, failure, and non-authorization requirement in these governing artifacts remains unchanged:

1. accepted contract blob `8fe287db830505dfbc59664ad78dbed60f6baec6`;
2. implementation specification blob `e0fda56c367c41c48c58ca8f117099de2a298624`;
3. prior task-order blob `92a975c0b36c2d3785cbc629a84ebb0dc8f4d5d0`, except where its one-commit publication and attempt-consumption clauses are expressly superseded below.

This reissue does not change:

- the exact implementation subject;
- the exact two authorized paths;
- the eleven-symbol public surface;
- enums, dataclasses, fields, types, invariants, canonicalization, hashes, decisions, or precedence;
- permitted imports or forbidden surfaces;
- the exact 24-method test inventory;
- the exact 67-case ordered negative matrix;
- the 26, 24, and 50-test output contract;
- the Python interpreter-resolution procedure;
- Stage 4.1A preservation requirements;
- completion evidence;
- independent implementation acceptance; or
- any non-authorization boundary.

## Corrected Governing Principle

The material implementation boundary is the exact final committed transformation:

- exact parent lineage;
- exactly two authorized new paths;
- exact final bytes;
- no existing-path modification;
- complete deterministic validation against committed bytes; and
- independent acceptance before any later movement.

Commit count is transport evidence, not domain meaning. It may be frozen only after available publication capability is proven. For this connector-native lane, two ordered commits are the exact proven transport.

## Reissued Implementation Authority

The single-use implementation authority is reissued for branch:

`sniperbot-stage-4-next-subject-implementation`

The branch must be created directly from:

`998e2d2e91ecb758e084aad0112fd58608dcdb61`

The branch and both authorized remote paths were absent when the earlier local construction began. Before resumed publication, their absence and the current governing anchors must be reverified.

The already constructed isolated local candidate may be used only if all three exact validation commands are rerun successfully immediately before publication and the local candidate contains only the two authorized files relative to exact accepted predecessor bytes. Otherwise reconstruct within the same two-file contract or return `BLOCKED`.

## Exact Connector-Native Publication Sequence

Publish exactly two ordered commits through the connected GitHub contents API.

### Commit 1 — production module

- exact parent: `998e2d2e91ecb758e084aad0112fd58608dcdb61`;
- exact changed path: `src/sniperbot/simulation/fixture_observation.py`;
- exact operation: create;
- exact commit message: `Implement typed fixture scenario validator`.

No other path may change in Commit 1.

### Commit 2 — validation suite

- exact parent: Commit 1 resulting checkpoint;
- exact changed path: `tests/test_fixture_observation.py`;
- exact operation: create;
- exact commit message: `Test typed fixture scenario validator`.

No other path may change in Commit 2.

### Final aggregate state

Relative to `998e2d2e91ecb758e084aad0112fd58608dcdb61`, the final branch must be:

- exactly two commits ahead;
- zero commits behind;
- merge base exactly `998e2d2e91ecb758e084aad0112fd58608dcdb61`;
- exactly two added paths;
- zero modified, deleted, renamed, or additional paths.

The final two-file tree is the implementation evidence. Neither intermediate Commit 1 nor its source-only tree constitutes technical completion or acceptance.

## Corrected Consumption Boundary

The earlier isolated local construction and validation did not mutate the governed SniperBot repository and therefore did not consume repository implementation authority. It is classified as pre-publication construction evidence.

This reissued order is consumed when the first authorized remote SniperBot file-creation commit succeeds.

After Commit 1 succeeds:

- authority permits only the exact Commit 2 operation;
- any failure, conflict, unexpected state, or need for correction requires immediate `BLOCKED` or `FAIL`;
- no retry, deletion, force movement, amendment, third commit, or alternate path is authorized.

If Commit 1 never succeeds, the order remains unconsumed but no mutation may proceed after a governing conflict is discovered without renewed assessment.

## Required Immediate Pre-Publication Validation

Before Commit 1:

1. resolve the final reissue commit and blob;
2. verify both canonical repository observations remain compatible;
3. verify the implementation branch is absent;
4. verify both authorized output paths are absent at the exact base;
5. verify accepted contract, acceptance, specification, and Stage 4.1A blobs;
6. bind the first qualifying interpreter from the existing closed list;
7. run the exact predecessor command and obtain `Ran 26 tests` and `OK`;
8. run the exact new command and obtain `Ran 24 tests` and `OK`;
9. run the exact combined command and obtain `Ran 50 tests` and `OK`;
10. confirm all 67 ordered negative cases pass;
11. confirm static forbidden-surface checks pass; and
12. confirm the candidate diff contains only the two authorized files.

## Required Committed-Byte Validation

After Commit 2, fetch both exact committed files from the final branch into a clean isolated verification tree together with the exact accepted predecessor source, tests, and package initializers.

Rerun the same exact three commands using the same interpreter invocation. Require `26`, `24`, and `50` tests, exit `0`, and `OK` with no failures, errors, skips, warnings, tracebacks, or subtest failures.

Compare the fetched committed bytes with the pre-publication candidate bytes and require exact equality.

## Required Completion Evidence Addendum

In addition to all prior evidence requirements, report:

- final reissue commit and blob;
- Commit 1 checkpoint and production blob;
- Commit 2 checkpoint and test blob;
- exact parent relation for each commit;
- exact aggregate two-file diff from the accepted implementation base;
- confirmation of two-ahead, zero-behind, and exact merge base;
- pre-publication and committed-byte 26/24/50 outputs;
- exact pre-publication-to-committed byte equality;
- confirmation that no third commit or path occurred; and
- terminal `WAIT — IMPLEMENTED, PENDING INDEPENDENT ACCEPTANCE`.

## Failure Conditions

Return `WAIT`, `BLOCKED`, or `FAIL` without expansion if:

- any governing commit or blob differs;
- either authorized branch or path has unexpected existing content;
- either canonical anchor creates a new unresolved conflict;
- pre-publication validation differs from 26/24/50 successful tests;
- any ordered negative case or static scan fails;
- Commit 1 changes anything other than the production module;
- Commit 2 changes anything other than the test module;
- aggregate comparison is not exactly two added files and two commits;
- committed bytes differ from validated candidate bytes;
- any third commit, correction, deletion, force update, or alternate transport becomes necessary; or
- any prior non-authorization boundary would be crossed.

## Non-Authorization Boundary

This correction and reissue grants no authority for:

- changing the accepted contract or specification;
- changing implementation behavior, API, tests, or evidence requirements;
- a third implementation file or commit;
- historical Stage 4.1B inspection, restoration, copying, merging, or reuse;
- pull request, merge, canonical synchronization, or movement of `main`;
- implementation acceptance;
- runtime orchestration, simulation activation, market-data access, ingestion, replay, backtesting, signals, strategy, candidates, risk, simulated actions, brokers, accounts, credentials, orders, fills, execution, positions, portfolios, balances, funding, capital, or financial action;
- database or filesystem persistence;
- deployment, production, communication, external integration, or autonomous action;
- Stage 4 readiness acceptance or closure; or
- Stage 5 entry.

## Final Determination

`PASS — THE PUBLICATION MECHANISM IS CORRECTED TO THE PROVEN CONNECTOR-NATIVE TWO-COMMIT SEQUENCE WHILE THE EXACT FINAL TWO-FILE IMPLEMENTATION, VALIDATION, EVIDENCE, INDEPENDENT-ACCEPTANCE, AND NON-AUTHORIZATION BOUNDARIES REMAIN FROZEN.`

## Reissued Posture

`AUTHORIZED — ONE CONNECTOR-NATIVE TWO-COMMIT IMPLEMENTATION PUBLICATION MAY PROCEED; RETURN TO WAIT PENDING INDEPENDENT IMPLEMENTATION ACCEPTANCE.`
