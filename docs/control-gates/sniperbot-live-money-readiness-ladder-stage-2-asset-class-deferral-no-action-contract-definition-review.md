# SniperBot Live-Money Readiness Ladder Stage 2 Asset-Class Deferral / No-Action Contract Definition Review

## Status and Boundary

Documentation-only / governance-only / contract-definition-only / non-runtime /
non-execution / non-authorizing.

This review defines one proposed future subject: a pure classification of
already-supplied asset-class deferral and no-action facts. It creates no schema,
implementation, test, runtime integration, market-data access, asset
selection, trading, broker access, order authority, execution capability, or
Stage 3 entry.

Stage 2 remains **HOLD**. EchoAuth remains the sole owner of permission
authority. The proposed classifier may consume a bounded authority result only
as caller-supplied evidence; it may not create, repair, reinterpret, broaden,
bypass, or replace authority.

## Subject Definition

The single subject is **SniperBot Stage 2 — Asset-Class Deferral / No-Action
Decision Contract**.

The contract would distinguish, without taking action:

* asset-class identifier;
* externally supplied evidence;
* deferral condition;
* no-action condition;
* classification decision;
* closed reason code; and
* required next human or governance action.

Deferral and no-action are descriptive governance outcomes only. They are not
asset selection, eligibility approval, exclusion enforcement, strategy,
signals, risk, sizing, order, broker, or execution decisions.

## Proposed Immutable Inputs

The future contract may receive only caller-supplied, already-determined
values:

| Input | Proposed meaning |
| --- | --- |
| `asset_class` | Opaque asset-class identifier; exact vocabulary remains unresolved. |
| `evidence_present` | Whether supporting evidence was supplied. |
| `evidence_current` | Whether supplied evidence is current rather than stale. |
| `evidence_sufficient` | Whether evidence is sufficient under a future founder-defined rule. |
| `evidence_contradictory` | Whether evidence is externally marked contradictory. |
| `eligibility_status` | Eligibility already determined externally; never calculated here. |
| `exclusion_status` | Exclusion already determined externally; never calculated here. |
| `authority_result` | Optional bounded EchoAuth result when a future rule requires it. |
| `correlation_reference` | Mandatory opaque caller reference, neither generated nor interpreted. |

No market prices, indicators, signals, orders, balances, credentials,
commands, network inputs, or executable instructions are in scope.

## Proposed Descriptive Output

The future output would contain only:

* `asset_class`;
* `outcome`;
* closed `reason_code`;
* `required_next_human_or_governance_action`; and
* the echoed `correlation_reference`.

The only currently supported outcome concepts are **deferral** and
**no-action**. Their exact closed vocabulary is not settled by the repository
and must not be invented here.

## Proposed Fail-Closed Treatment

The future contract should deny classification as an affirmative outcome and
request the appropriate review when inputs are missing, stale, insufficient,
contradictory, excluded, unauthorized, unknown, or undefined. In particular:

* missing, stale, or insufficient evidence must not become permission;
* contradictory evidence must resolve to a non-action review outcome;
* externally determined exclusion must remain an external fact and must not
  become runtime blocking or asset selection;
* absent, invalid, revoked, or out-of-scope authority must never become
  permission;
* unknown asset classes and undefined combinations must fail closed and remain
  subject to governance review; and
* no branch may call an external service, mutate state, persist data, or act on
  an asset.

Precedence among deferral, exclusion, contradiction, and no-action is not
settled by the construction record and is intentionally left unresolved.

## Neighboring Subjects Excluded

This subject is strictly separate from asset-class eligibility/exclusion,
stock/options/crypto-specific deferral, market-data processing, signal
classification, strategy, risk, position sizing, replay/backtesting,
simulation, order routing, broker access, Robinhood access, and FSM runtime
integration. No neighboring subject is selected, bundled, or authorized.

## Founder Decisions Required Before Schema or Implementation

1. Exact supported `asset_class` vocabulary.
2. Exact closed `outcome` vocabulary for deferral and no-action.
3. Exact closed `reason_code` vocabulary.
4. Whether bounded authority evidence is required for this classification.
5. Precedence among deferral, exclusion, contradiction, and no-action.
6. Required-action values and mappings.
7. Unknown-asset-class behavior.
8. Exact future schema, implementation, test, and initializer paths.
9. Required validation commands, test vectors, and stop conditions.

These questions cannot be resolved without inventing unsupported semantics.

## Future Boundary Proposal — Not Authorized

If separately approved, a future order may define one schema/interface file,
one pure implementation file, one direct test file, and package initializers
only if repository conventions require them. Exact paths are intentionally
provisional and are not authorized by this review. Any future order must name
the files explicitly and prohibit all neighboring capabilities listed above.

## Current Determination

This is one documentation-only contract-definition review. It does not create
a schema, implementation, authority, asset selection, runtime behavior, or
execution capability. Stage 2 remains **HOLD**, and Stage 3 remains unentered
and unauthorized.
