# SniperBot Robinhood Provider-Permission Reality Evidence Completeness Assessment

## Result

**WAIT — current authoritative Robinhood evidence confirms a broad Trading MCP read grant and does not establish any narrower account-scoped or data-class-scoped permission configuration for Agentic Trading.**

The evidence is sufficient to close the present completeness question. It is not sufficient to form a narrower provider boundary.

Final posture:

```text
BROAD CROSS-ACCOUNT READ GRANT
→ CONFIRMED

NARROWER OFFICIAL TRADING MCP PERMISSION MODEL
→ NOT EVIDENCED

PROVIDER-PERMISSION CORRESPONDENCE REASSESSMENT
→ NOT READY

CLIENT / CONNECTION / ACCESS / IMPLEMENTATION / EXECUTION AUTHORITY
→ NONE

RESULT
→ WAIT
```

## Authority

Nicholas B. Carty authorized one bounded, documentation-only Robinhood Provider-Permission Reality Evidence Completeness Assessment.

The authority permitted authoritative-provider evidence review and correspondence assessment only. It prohibited connection, authentication, authorization, MCP configuration, account creation or funding, client activation, data access, secret handling, asset activation, order activity, autonomous behavior, implementation, and execution.

The authority is consumed by this assessment.

## Authoritative Robinhood evidence reviewed

- `Agentic Trading overview`
- `Trading with your agent`
- `Agentic Trading on Robinhood`
- `Robinhood is Now Open to Agents`
- `Agentic Credit Card` only as evidence that Robinhood documents narrower authorization when a product actually provides it; it is not evidence that Trading MCP inherits that narrower model

## Evidence Sending

Current Robinhood-controlled materials establish:

1. Connecting a third-party client to the Trading MCP grants read access to all Robinhood accounts.
2. The disclosed read surface includes account numbers, positions, balances, transactions, order history, watchlists, and scans.
3. Trade placement is restricted to the dedicated Agentic account.
4. Robinhood documents one Trading MCP endpoint used across supported MCP clients.
5. Robinhood documents tool-specific functions, but does not state that selecting fewer tools narrows the authorization grant.
6. Robinhood does not publicly document an account-selection consent step for Trading MCP read access.
7. Robinhood does not publicly document data-class scopes, optional-versus-required read permissions, session scopes, or client-specific reduced scopes for Agentic Trading.
8. Robinhood documents customer disconnection at the product level.
9. Robinhood does not publicly establish that disconnection deletes or retracts data already transferred to the third-party provider.
10. Robinhood separately documents a narrowly scoped Banking MCP for Agentic Credit Card access. That demonstrates product-specific scoping is possible in Robinhood architecture, but it does not establish narrower Trading MCP permissions.

## 1. Alignment Assessment

### Robinhood reality

Robinhood reality owns the actual permission model and product behavior.

The present official Trading MCP reality is:

```text
READ AUTHORIZATION
→ all Robinhood accounts
→ broad account and activity data classes

TRADE AUTHORIZATION
→ dedicated Agentic account only
```

### Echoauth

Echoauth owns interpretation of whether that provider model corresponds to the preserved minimum purpose. It cannot infer hidden scopes from technical possibility or from another Robinhood product.

### SniperBot

SniperBot's minimum surface remains unchanged and dedicated-account-only. The upstream evidence review does not broaden its account or data role.

### NI AI Spine

The Spine preserves continuity between the real provider condition and the existing refusal. It does not manufacture a missing permission boundary.

Order 1 result: **PASS**.

## 2. Inconsistency Detection and Bounded Repair

### Account-scoped permission test

No authoritative Trading MCP evidence reviewed establishes that a customer can restrict read access to the dedicated Agentic account or exclude the primary individual, Roth IRA, Money, or other Robinhood accounts.

Result: **NOT EVIDENCED**.

### Data-class-scoped permission test

No authoritative Trading MCP evidence reviewed establishes that account numbers, balances, positions, transactions, order history, watchlists, or scans can be separately denied while retaining a narrower subset.

Result: **NOT EVIDENCED**.

### Tool-scoped permission test

Robinhood publishes individual tools such as account, portfolio, position, order, watchlist, scan, market-data, and order-placement tools.

However:

```text
TOOL INVOCATION SCOPE
≠
AUTHORIZATION GRANT SCOPE
```

The documentation does not establish that disabling or avoiding a tool prevents the client from being granted the broader read authorization.

Result: **NO NARROWER PERMISSION ESTABLISHED**.

### Consent-, session-, client-, and configuration-scoped tests

No authoritative evidence reviewed establishes:

- optional read categories on a Trading MCP consent screen;
- a dedicated-account-only Trading MCP session;
- different permission grants by supported MCP client;
- a setup choice that narrows account visibility;
- a product configuration that excludes specific data classes; or
- reauthorization with a reduced Trading MCP scope.

Result: **NOT EVIDENCED**.

### Revocation and retained-data test

Robinhood documents that a customer can disconnect the agent. This establishes a future-connectivity control at the Robinhood product boundary.

The public Trading MCP evidence does not establish:

- deletion of data already transferred to the client;
- deletion from client logs, memory, storage, or provider systems;
- revocation propagation to derived data;
- proof of no post-disconnection retention; or
- a Robinhood-controlled deletion guarantee outside Robinhood's environment.

Result: **FUTURE ACCESS STOP SUPPORTED; RETAINED THIRD-PARTY DATA DISPOSITION NOT ESTABLISHED**.

### Apparent cross-document tension

Robinhood's newsroom describes the agentic account as separate and says the agent only has access to funds deposited into that account. The detailed support documentation clarifies that trade authority is restricted to the Agentic account while read access spans all Robinhood accounts.

The detailed permission statement governs this assessment because it directly defines what the connected agent can access.

No narrower data boundary can be inferred from the high-level account-separation language.

### Bounded repair

No repository or interpretation repair can create the absent provider scope.

The existing correspondence refusal remains correct.

Order 2 result: **NO BOUNDED REPAIR — WAIT**.

## 3. Consistency Verification

| Question | Result |
|---|---|
| Broad all-account Trading MCP read grant confirmed | YES |
| Dedicated Agentic account trade restriction confirmed | YES |
| Account-scoped Trading MCP read option documented | NO |
| Data-class-scoped Trading MCP option documented | NO |
| Optional-versus-required read permissions documented | NO |
| Tool selection proven to narrow authorization | NO |
| Client-specific reduced permission documented | NO |
| Session-specific reduced permission documented | NO |
| Consent-screen account selection documented | NO |
| Reauthorization with narrower Trading scope documented | NO |
| Disconnect control documented | YES |
| Third-party retained-data deletion documented | NO |
| Exact narrower real provider boundary demonstrated | NO |
| Existing evidence sufficient for current completeness question | YES |
| Provider-permission correspondence ready to reassess | NO |

Order 3 result: **WAIT**.

## Completeness determination

The evidence is complete enough to answer the bounded current question:

> The publicly documented Trading MCP permission model is broad, and no narrower official Trading MCP configuration is presently evidenced.

This does not prove that no unpublished internal capability exists. It means no authoritative evidence available to this assessment permits NI AI to rely on such a capability.

## Direction and closure

The returned result belongs upstream in Robinhood provider reality and is now preserved there.

Direction test:

```text
DOWNSTREAM
→ NO
→ no client or implementation can repair the provider grant

FURTHER UPSTREAM INTERNAL WORK
→ NO
→ current authoritative public evidence is complete for the bounded question

CURRENT RESPONSIBILITY
→ COMPLETE / CLOSED IN WAIT
```

The unresolved condition remains external:

```text
REQUIRED CONDITION
→ authoritative evidence of a narrower Trading MCP permission model

CURRENT EVIDENCE
→ none
```

No next entrusted responsibility is revealed by the current evidence.

## Closing sequence

```text
PROVIDER-PERMISSION REALITY EVIDENCE RECEIVED
→ ACCOUNT, DATA, TOOL, CONSENT, SESSION, CLIENT, AND REVOCATION SCOPES TESTED
→ BROAD TRADING MCP READ GRANT CONFIRMED
→ NO NARROWER TRADING MCP BOUNDARY EVIDENCED
→ TOOL SELECTION REJECTED AS AUTHORIZATION NARROWING
→ DISCONNECT DISTINGUISHED FROM THIRD-PARTY DATA DELETION
→ CURRENT CORRESPONDENCE REFUSAL PRESERVED
→ COMPLETENESS RESPONSIBILITY CLOSED IN WAIT
→ NO NEXT RESPONSIBILITY REVEALED
→ STOP
```

## Final disposition

```text
CURRENT ASSESSMENT
→ COMPLETE

OFFICIAL BROAD GRANT
→ CONFIRMED

OFFICIAL NARROWER TRADING MCP GRANT
→ NOT EVIDENCED

PROVIDER CORRESPONDENCE REASSESSMENT
→ NOT READY

NEXT RESPONSIBILITY
→ NOT REVEALED

CLIENT / CONNECTION / ACCESS / IMPLEMENTATION / EXECUTION AUTHORITY
→ NONE
```

**Final result: WAIT — preserve the current refusal until Robinhood reality returns authoritative evidence of a different Trading MCP permission condition.**
