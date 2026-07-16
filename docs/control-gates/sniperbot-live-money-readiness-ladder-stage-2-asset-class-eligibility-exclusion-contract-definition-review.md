# SniperBot Live-Money Readiness Ladder Stage 2 Asset-Class Eligibility / Exclusion Contract Definition Review

## Status and Boundary

Documentation-only / governance-only / contract-definition-only / non-runtime /
non-execution / non-authorizing.

This review defines one proposed future subject: a pure classification of
caller-supplied asset-class eligibility and exclusion facts. It creates no
schema, implementation, test, runtime integration, asset selection,
market-data access, trading, broker or exchange access, wallet or custody
access, order authority, execution capability, or Stage 3 entry.

Stage 2 remains **HOLD**. Stage 3 remains unentered and unauthorized. EchoAuth
remains the sole owner of permission authority. This proposed classifier may
consume bounded EchoAuth evidence only when a future founder decision requires
it; it may not create, repair, reinterpret, broaden, bypass, or replace
authority.

## Subject Definition

The single subject is **SniperBot Stage 2 — Asset-Class Eligibility / Exclusion
Decision Contract**.

For exactly one caller-supplied asset class from a future closed vocabulary of
`STOCK`, `OPTIONS`, and `CRYPTO`, the proposed contract would classify
caller-supplied facts as one of these unresolved outcome concepts:

* eligible for further governed consideration;
* excluded;
* restricted;
* unresolved evidence; or
* awaiting review.

Eligibility means only continued governed evaluation. It is never trade
permission, asset approval, asset selection, strategy approval, order
authority, or execution authorization. The contract would not choose, rank,
recommend, compare, or switch asset classes, and it would not determine the
eligibility of an individual security, option contract, token, or other asset.

## Separation From Neighboring Subjects

This proposed subject is separate from:

* generic Asset-Class Deferral / No-Action classification;
* Stock, Options, and Crypto Deferral / No-Action classification;
* Stock-, Options-, or Crypto-specific eligibility and exclusion;
* individual asset, instrument, contract, or token eligibility;
* asset-class selection, ranking, recommendation, switching, or routing;
* strategy, signal, risk, sizing, market-data, replay, backtesting, or
  simulation decisions;
* broker, Robinhood, exchange, wallet, custody, order, transaction, or
  execution behavior; and
* runtime integration and Stage 3.

No neighboring subject is selected, bundled, or authorized by this review.

## Proposed Immutable Inputs

The future contract may receive only caller-supplied, already-determined facts:

| Input | Proposed meaning |
| --- | --- |
| `asset_class` | One value from a future closed asset-class vocabulary. |
| `asset_class_reference` | Opaque caller-supplied reference for the classified subject. |
| `evidence_present` | Whether supporting evidence was supplied. |
| `evidence_current` | Whether supplied evidence is current rather than stale. |
| `evidence_sufficient` | Whether evidence is externally marked sufficient. |
| `evidence_contradictory` | Whether evidence is externally marked contradictory. |
| `eligible` | Caller-supplied eligibility fact; never calculated here. |
| `excluded` | Caller-supplied exclusion fact; never calculated here. |
| `restricted` | Caller-supplied restriction fact; never calculated here. |
| `authority_result` | Optional bounded EchoAuth evidence if later required. |
| `correlation_reference` | Opaque caller-supplied correlation reference. |

Whether a separately supplied lane-confirmation fact is required remains an
unresolved founder decision. No market prices, indicators, signals, balances,
credentials, commands, endpoints, network inputs, or executable instructions
are proposed inputs.

## Proposed Descriptive Output

The future output would contain only:

* `asset_class`;
* `outcome`;
* closed `reason_code`;
* `required_action`;
* the echoed `asset_class_reference`; and
* the echoed `correlation_reference`.

The exact closed vocabularies and mappings are unresolved. The output would be
descriptive evidence only and could not grant permission or cause action.

## Validation Boundaries and Prohibited Side Effects

A future contract must be deterministic, fail closed, preserve opaque
references exactly, avoid mutation, and reject unsupported or undefined input
combinations according to founder-approved rules. It must not:

* select, rank, recommend, compare, route, or switch an asset class;
* infer eligibility, exclusion, restriction, evidence quality, or authority;
* convert eligibility into approval or permission;
* access filesystems, environments, networks, processes, logs, databases,
  brokers, exchanges, wallets, custody systems, market data, or order systems;
* persist or mutate state; or
* initiate transactions, orders, trading, execution, integration, or runtime
  behavior.

## Founder Decisions Required Before Schema or Implementation

All decisions below remain unresolved. This review records the decision surface
and does not answer, recommend, or infer any selection.

1. Exact closed `asset_class` vocabulary.
2. Exact closed `outcome` vocabulary.
3. Exact contractual meaning of eligibility.
4. Exact contractual meaning of exclusion.
5. Exact contractual meaning of restriction.
6. Exact closed `reason_code` vocabulary and mappings.
7. Exact `RequiredAction` vocabulary, mappings, and subject-emittable values.
8. Whether an asset-class lane-confirmation fact is required and, if so, its exact type and effect.
9. Precedence and outcome when eligibility and exclusion are both asserted.
10. Precedence and outcome when eligibility and restriction are both asserted.
11. Precedence between exclusion and restriction.
12. Exact contradiction trigger, precedence, outcome, reason, and required action.
13. Precedence among missing, stale, and insufficient evidence.
14. Exact deterministic fallback for otherwise undefined combinations.
15. Whether EchoAuth evidence is required and its exact subprecedence and mappings.
16. Exact relationship to Asset-Class Deferral / No-Action classification.
17. Exact relationship to Stock-, Options-, and Crypto-specific eligibility and exclusion subjects.
18. Unknown, malformed, and otherwise undefined input policy.
19. Exact future schema, package, implementation, initializer, and direct-test paths.
20. Exact validation commands, test vectors, scope checks, and stop conditions.

Resolving any item here would invent behavior not yet authorized by repository
evidence.

## Proposed Future Paths — Not Authorized

If separate founder decisions and a later bounded task order authorize movement,
the proposed paths are:

* `schemas/sniperbot-asset-class-eligibility-exclusion-decision.schema.json`;
* `src/sniperbot/eligibility/__init__.py`;
* `src/sniperbot/eligibility/asset_class_decision.py`; and
* `tests/test_sniperbot_asset_class_eligibility_exclusion.py`.

These paths are planning references only. They do not authorize file creation,
schema definition, package exports, implementation, tests, integration, or
runtime behavior.

## Proposed Future Validation — Not Authorized

A later task order must explicitly approve the canonical JSON parse, focused
direct tests, Contract Validation, Authority Clarity Gate Validation, explicit
Authority Clarity Validator, full-suite, diff, import-boundary, and exact-scope
checks required at that future step. This review neither substitutes a new
validation standard nor authorizes those future commands or artifacts.

## Readiness Conclusion

The bounded decision surface is complete, while all semantic choices remain
reserved for a separate founder decision record. The exact next founder
decision is to create a separate read-only Asset-Class Eligibility / Exclusion
founder decision sheet. Stage 2 remains **HOLD**, and Stage 3 remains unentered
and unauthorized.

**ASSET-CLASS ELIGIBILITY / EXCLUSION CONTRACT READY FOR FOUNDER DECISIONS**
