# SniperBot Live-Money Readiness Ladder Stage 2 - Post-Construction Cross-File Semantic-Consistency Review

## Status and Non-Authorization Boundary

DOCUMENTATION ONLY -- GOVERNANCE ONLY -- CROSS-FILE SEMANTIC-CONSISTENCY
REVIEW ONLY -- NOT A REPAIR -- NOT OVERALL STAGE 2 EVIDENCE ACCEPTANCE -- NOT
A STAGE 2 COMPLETION CERTIFICATION -- NOT AN UPDATED ADVANCEMENT-GATE
DECISION -- NOT STAGE 2 ADVANCEMENT -- NOT STAGE 3 ENTRY -- NOT AN
IMPLEMENTATION TASK ORDER -- NOT IMPLEMENTATION -- NOT INTEGRATION,
ORCHESTRATION, RUNTIME, DEPLOYMENT, EXECUTION, OR LIVE-MONEY AUTHORITY --
NON-AUTHORIZATION BOUNDARY

This review determines only whether the committed artifacts within each of the
ten completed evaluator lanes express the same governed semantics across their
final controlling definitions, founder decisions, schemas, Python interfaces,
implementations, tests, independent evidence, formal acceptances, and
canonical README entries.

The review records and preserves inconsistencies. It does not repair them,
reopen an implementation lane, accept Stage 2 as a whole, certify completion,
change the Advancement Gate decision, advance Stage 2, enter Stage 3, or
authorize any operational behavior.

Stage 2 remains **HOLD**. Stage 3 remains **UNENTERED AND UNAUTHORIZED**.

## Authoritative Checkpoint

Repository: `heliosfi/Echoauth-core`

Authoritative starting checkpoint:
`fc0daf5d70b0cad40d476bb0582ccf3f4f4667d1`
(`docs: add sniperbot stage 2 accumulated-evidence coverage and sufficiency
review`).

At review start, local `HEAD`, local `origin/main`, and live
`refs/heads/main` resolved to the authoritative checkpoint; divergence was
`0/0`; the working tree was clean; no staged or untracked file existed; and no
Git lock file existed. The checkpoint commit created only the controlling
coverage-and-sufficiency review and changed no existing file.

## Founder-Selected Scope

The founder selected semantic-consistency review for exactly these completed
evaluator lanes:

1. Pure / Canonical FSM
2. Rollback / No-Action Fallback
3. Asset-Class Deferral / No-Action
4. Stock Deferral / No-Action
5. Options Deferral / No-Action
6. Crypto Deferral / No-Action
7. Asset-Class Eligibility / Exclusion
8. Stock Eligibility / Exclusion
9. Options Eligibility / Exclusion
10. Crypto Eligibility / Exclusion

The comparison is internal to each lane except for the explicitly bounded
shared-term review. It does not require separate lanes to share decision
tables, infer a universal abstraction, or determine whether the lanes compose
safely.

## Three-Rule Protocol Preservation

This review preserves
`docs/control-gates/codex-three-rule-repo-protocol.md` without
reinterpretation:

1. **Habitat Before Routine.** Each lane's final controlling records define
   the semantics against which its committed artifacts are compared.
2. **Silence Is Not Permission.** A design or strictness rule from one lane is
   not imposed on another lane unless the latter's governance selects it.
3. **Stop Outside the Lane.** Every inconsistency or missing link is recorded
   and left unchanged; no repair or adjacent work follows automatically.

## Controlling Currentness Result

The currentness review at
`docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-post-construction-accumulated-evidence-inventory-currentness-validation-review.md`,
committed at `bb3da97f8b34fc63112fbed0209bfe850dc22381`,
established that all 73 identified evidence paths were present, traceable,
unchanged after their final controlling commits, and represented by exactly
one canonical acceptance entry per lane.

All ten lane chains were `CURRENT`. This semantic review uses those final
controlling paths and does not revive superseded wording.

## Controlling Coverage-and-Sufficiency Result

The coverage-and-sufficiency review at
`docs/control-gates/sniperbot-live-money-readiness-ladder-stage-2-post-construction-accumulated-evidence-coverage-sufficiency-review.md`,
committed at `fc0daf5d70b0cad40d476bb0582ccf3f4f4667d1`,
recorded 108 required findings as covered and sufficient, zero insufficient
findings, zero missing required evidence, zero unsupported acceptance claims,
and zero unresolved findings.

That result assessed whether evidence existed and supported each acceptance.
It expressly did not determine cross-file semantic consistency. The
inconsistencies found here therefore do not alter that review's historical
scope or result; they answer the separately selected semantic question.

## Semantic-Consistency Methodology

For each lane, this review compared the final controlling contract and founder
records to the schema/interface, Python surface, implementation, direct tests,
independent evidence, acceptance, and exact README characterization. It
examined, where applicable:

1. governed subject;
2. input vocabulary;
3. input type and strictness;
4. required versus optional fields;
5. omission versus explicit null;
6. enum or literal values;
7. output vocabulary;
8. decision mapping;
9. precedence;
10. authority subprecedence;
11. generic-context subprecedence;
12. collision behavior;
13. unknown or undefined behavior;
14. exception behavior;
15. schema-to-Python parity;
16. contract-to-implementation parity;
17. implementation-to-test parity;
18. evidence-to-acceptance parity;
19. acceptance-to-index parity; and
20. the non-authorization boundary.

Only the required determination vocabulary is used for comparison findings:

* `CONSISTENT`
* `INTENTIONALLY LANE-SPECIFIC`
* `INCONSISTENT`
* `REQUIRED SEMANTIC LINK MISSING`
* `UNRESOLVED`
* `NOT APPLICABLE`

The review distinguishes invalid values outside an earlier lane's governed
typed domain from an actual semantic contradiction. It does not import later
strict-runtime exception requirements into earlier lanes. It does compare
valid typed requests that the schema and Python evaluator treat differently,
because those requests are inside the same lane's governed domain.

## Supersession and Final-Controlling-Record Method

Later committed founder or schema-consistency records control over earlier
proposal wording when they expressly resolve or narrow it:

* Canonical FSM re-gate and schema-semantics decisions control over unresolved
  questions and provisional interface wording in the initial FSM review.
* Rollback's unknown-condition founder decision controls over the earlier
  reachable-`UNKNOWN_CONDITION` wording: the code remains vocabulary-only and
  non-emittable.
* Asset-Class Deferral's semantics record rejects unknown raw asset classes,
  and its later schema-consistency record narrows the open invariant language
  to four exact typed undefined combinations. Those records control over the
  earlier unknown-output and open-invariant wording.
* The final Asset-Class Eligibility founder-decision file at
  `962ea18e4214bc69488fd2580bfbfbd931613be1` controls over its earlier
  revisions.
* Direct-test evidence completions close evidence gaps but do not alter the
  governing semantics of their lanes.
* The Rollback acceptance whitespace repair at
  `8f5f91737c58ec3777a4901c383a8dba1440587c` and the Stock Deferral contract
  whitespace repair at `fa1296ab8b42d1df7e4874e20717e3d25719d490`
  make no semantic change.

No other later committed artifact supersedes a final governing semantic record
identified here.

## Exact Ten-Lane Inventory

| # | Evaluator lane | Final lane determination |
| --- | --- | --- |
| 1 | Pure / Canonical FSM | `INCONSISTENT` |
| 2 | Rollback / No-Action Fallback | `CONSISTENT` |
| 3 | Asset-Class Deferral / No-Action | `CONSISTENT` |
| 4 | Stock Deferral / No-Action | `CONSISTENT` |
| 5 | Options Deferral / No-Action | `CONSISTENT` |
| 6 | Crypto Deferral / No-Action | `INCONSISTENT` |
| 7 | Asset-Class Eligibility / Exclusion | `CONSISTENT` |
| 8 | Stock Eligibility / Exclusion | `CONSISTENT` |
| 9 | Options Eligibility / Exclusion | `CONSISTENT` |
| 10 | Crypto Eligibility / Exclusion | `CONSISTENT` |

## Per-Lane Controlling Artifacts

### 1. Pure / Canonical FSM

Final governance is the contract review at
`0726b7492c2ba84feacd15b277dc4e8c80b7f8d5`, re-gate founder record at
`76f427cd2068e7b1605bf9f4171606258a54b03a`, interface proposal at
`d3eb72e5911249d4389afc3e736497f7eb0038db`, and schema-semantics founder
record at `73f415197a650f6750a2883b882dccd9c3157e8e`. The schema was finalized at
`73f415197a650f6750a2883b882dccd9c3157e8e`; implementation and tests are at
`bd57d6b8185b3dec57b37a6f2e38b5de1675d89b`; acceptance and canonical index
are at `80ad01b2730182bfcc1242c4302be35f1c01c83b`.

### 2. Rollback / No-Action Fallback

Final governance is the contract at
`29e9ee28ad72bbe76fb4bd14aa335ea8049acb9a`, founder record at
`369bf5c0ce5403daef1e299f64b82c14082f5bc7`, and unknown-condition founder
record at `26b2ef91f48e4e1d9e829470b78f9852b3488027`. The schema is at the latter
commit; implementation is at `c172aaed8382399c117fe9fc5653ac80b3f63965`;
tests end at `e9b4dddeca3ab8d1cb0867c53d1c2c2d9bc71a95`; acceptance and index are at
`d16fc872629aed3f4e5a46a6df58bd55332a27b1`, with whitespace-only final path
repair at `8f5f91737c58ec3777a4901c383a8dba1440587c`.

### 3. Asset-Class Deferral / No-Action

Final governance is the contract at
`497c375e2c1649e7db1559159fb69150ed3dbb89`, founder record at
`0204ef43aea0424d7afe8d0de61779cf9fe88ae7`, semantics record at
`e855a5f08cbd76d5f9447f035d368408c84c923e`, and final schema-consistency
record and schema at `8cecd357e43dcaa0791dfb7d6c0b1213d114c841`. Implementation and tests are at
`908c88204f6d4750a2f1ffa2695cb781fce9c724`; acceptance and index are at
`34b227f0b3207ad52096a4c04fc4dc9324d4d88d`.

### 4. Stock Deferral / No-Action

Final governance is the contract introduced at
`0971b2f4d5015dc7056ba075132638301cd3898f` and finalized without semantic
change at `fa1296ab8b42d1df7e4874e20717e3d25719d490`, plus the founder record at
`88393d9d8d46b61d04cdcc8a7bee52bfdd9abbd2`. The schema is at
`e1110a27c088dd0a9ceef1c0805fee03801aa8d4`; implementation is at
`ea6b61f05b0e8664e1902ede9106e5c8822180a4`; tests end at
`153f33c911b4bdbcf10e596066e6b4001c1eb88e`; acceptance and index are at
`261600c8e93615b82488b31df6a07d23a9d45588`.

### 5. Options Deferral / No-Action

Final governance is the contract at
`63f0bf5509b485ca7186e0c4c2074e06ac263fd6` and founder record at
`9455e3efc2f9f65ab9d3a4639fc6c7e8ded5bd05`. The schema is at
`c8c1d0713d5369e4399fe7a28b0a8617f2ed55c5`; implementation and tests are at
`a4ddcf061f4696ea9281c2d90d0889fb55ad0f43`; acceptance and index are at
`e8d5932d75578fccf1bf39ebdf72fa46e5acc8fd`.

### 6. Crypto Deferral / No-Action

Final governance is the contract at
`fffa3e43fd6629075e9eba955ff86ae16a55e13b` and founder record at
`7306a1ce13b90d6c66025e37e7024e53d98d9552`. The schema is at
`deb614768b4ae25a688ff2ca79a120e4892baa56`; implementation is at
`93bd254ab695a3de0b7994fca78a62d5662757e0`; direct tests end at
`8250816dac7bdf7786e039a4a1a1a4d52cf79ea9`; acceptance and index are at
`436bf3f2684e3b55d87c102694854ef1d441bee8`.

### 7. Asset-Class Eligibility / Exclusion

Final governance is the contract at
`fd3ebcd4bb06c33825e870f3638d4b771f757265` and founder-decision chain ending
at `962ea18e4214bc69488fd2580bfbfbd931613be1`. The schema is at
`8a60b26c6b30fe05be5aa5e1a30cd33026d79a2d`; implementation is at
`2cff2b5fa1d12b3026d20eb1c2831085888a8b36`; direct evidence ends at
`dd59f31638cec1d0140e368e60efbce3984ef0aa`; acceptance and index are at
`7f9bd718317f2c17d7b7de0099a48815dc799bfe`.

### 8. Stock Eligibility / Exclusion

Final governance is the contract at
`59a57194112a7af5a745d9243bcf058b8d724fbc` and founder record at
`172e300eea4250e92e498b3a5bbe437aed68c70e`. The schema is at
`d64e5a2a9a9d402a01fe894b4ad811d64064e1d2`; implementation is at
`f22faab66007e1100de4a3689ea34f3cfff93bbe`; tests end at
`ddad1e0fe9d2bcea5929a5095cfd17296fba24b2`; acceptance is at
`5e481a9eefebc1674a3131f5b26f73b8dd277c5c`; the canonical index is at
`31b344802d6088a72260447ecd47e42e74ba8e30`.

### 9. Options Eligibility / Exclusion

Final governance is the contract at
`854f4f85e2b5bd5ca0cce91cfbe2b08a54ed56dd` and founder record at
`bcf909ea55992b3e55163661f3f79759ef005d2e`. The schema is at
`305cb75ae10b050f1f8a8a09f36fab87b39f0b3b`; implementation is at
`b465be15ab8ac9ef9d2d003e0b87392019b26453`; tests end at
`7fb1e4abfc90daa100b63f1ba361d46abde86ed4`; acceptance is at
`a22f948a08c47e9993eba48e17eceaf4ed200a54`; the canonical index is at
`7ee771ba57a29e706291c44a61401612bc8ba742`.

### 10. Crypto Eligibility / Exclusion

Final governance is the contract at
`4a19be43f86d9714f1ad4d5f8066d8e45288d8aa` and founder record at
`c3aaad85cadcd123a7ba7aeabd500ba902443572`. The schema is at
`9fe9f704b6f3cc465dd2243e48f822127507fee1`; implementation is at
`41fe2ae15ab0047af6f0c5bd4ea03f93e1996801`; direct tests are at
`9b61ca69132a29af403b780ed3a86c31e70e4f06`; acceptance is at
`4a77c9394de813d5f9a79bbc528cd2c2e435f928`; the canonical index is at
`6602d2233c86cd37c07706068bd6d970c6d06a62`.

## Per-Lane Semantic Matrices

### 1. Pure / Canonical FSM

| # | Semantic comparison | Cross-file finding | Determination |
| --- | --- | --- | --- |
| 1 | Governed subject | Every artifact confines the subject to a pure descriptive transition evaluator. | `CONSISTENT` |
| 2 | Input vocabulary | Six states, nine transition-request names, external facts, authority evidence, and correlation reference align. | `CONSISTENT` |
| 3 | Input type and strictness | Schema types and Python annotations express the governed typed domain; no later strict-runtime exception model is imported. | `CONSISTENT` |
| 4 | Required versus optional fields | Schema conditionals require valid authority or affirmative facts for transitions whose Python evaluator accepts absent/negative evidence to return governed denials. | `INCONSISTENT` |
| 5 | Omission versus explicit null | Schema rejects null authority on arming/reset requests while Python accepts `None` and emits `AUTHORITY_MISSING` or `RESET_EVIDENCE_MISSING`. | `INCONSISTENT` |
| 6 | Enum or literal values | Six states, 17 reasons, transition names, and the five Python action values align except for the separate nullable-output issue below. | `CONSISTENT` |
| 7 | Output vocabulary | Final `FSM-SCHEMA-09` and Python define five RequiredAction values, but schema `$defs.RequiredAction` additionally accepts `null`. | `INCONSISTENT` |
| 8 | Decision mapping | For `lockout_required = true`, schema requires `allowed = false`; implementation and direct test require `allowed = true`. | `INCONSISTENT` |
| 9 | Precedence | Lockout-required facts retain first-match precedence over lower requested transitions. | `CONSISTENT` |
| 10 | Authority subprecedence | Constructible multi-failure authority evidence has no founder-selected collision order, while `_authority_reason` silently chooses one. | `REQUIRED SEMANTIC LINK MISSING` |
| 11 | Generic-context subprecedence | The FSM has no governed generic asset-class context. | `NOT APPLICABLE` |
| 12 | Collision behavior | The lockout collision winner is consistent, but its governed `allowed` semantics differ between schema and implementation/test. | `INCONSISTENT` |
| 13 | Unknown or undefined behavior | Unknown states and undefined transition requests fail closed without requested-state mutation as governed. | `CONSISTENT` |
| 14 | Exception behavior | Non-request objects are rejected; other invalid-value handling is evaluated only within the FSM's governed typed boundary. | `CONSISTENT` |
| 15 | Schema-to-Python parity | Conditional denial inputs, nullable RequiredAction, and lockout `allowed` behavior do not match. | `INCONSISTENT` |
| 16 | Contract-to-implementation parity | The implementation's lockout result is neither allowed-to-requested nor denied-to-current for a non-lockout request, contrary to final `FSM-SCHEMA-06`. | `INCONSISTENT` |
| 17 | Implementation-to-test parity | Direct tests accurately assert implementation behavior, including `allowed = true` on lockout precedence. | `CONSISTENT` |
| 18 | Evidence-to-acceptance parity | Acceptance states the bounded implementation satisfies the cited schema semantics but does not disclose the schema/implementation differences above. | `INCONSISTENT` |
| 19 | Acceptance-to-index parity | README accurately characterizes the bounded acceptance and its non-authorization boundary without adding lockout semantics. | `CONSISTENT` |
| 20 | Non-authorization boundary | Every artifact preserves pure, non-executing, non-runtime scope. | `CONSISTENT` |

Final lane determination: `INCONSISTENT`.

### 2. Rollback / No-Action Fallback

| # | Semantic comparison | Cross-file finding | Determination |
| --- | --- | --- | --- |
| 1 | Governed subject | Pure descriptive rollback/no-action classification remains separate from recovery execution and FSM mutation. | `CONSISTENT` |
| 2 | Input vocabulary | Rollback facts, optional authority, opaque context, and references align. | `CONSISTENT` |
| 3 | Input type and strictness | Typed booleans, enums, bounded strings, and nested objects align within the governed typed domain. | `CONSISTENT` |
| 4 | Required versus optional fields | Nine required facts/references and optional authority/context fields align. | `CONSISTENT` |
| 5 | Omission versus explicit null | Optional Python `None` and serialized absence/null behavior retain contextual absence without changing decisions. | `CONSISTENT` |
| 6 | Enum or literal values | Two outcomes, 14 full reasons, 13 emittable reasons, five actions, three emittable actions, and six contextual states align. | `CONSISTENT` |
| 7 | Output vocabulary | Decision fields and emittable restrictions align. | `CONSISTENT` |
| 8 | Decision mapping | All eleven top-level mappings align with final founder decisions. | `CONSISTENT` |
| 9 | Precedence | Contradiction through ordinary fallback first-match order aligns. | `CONSISTENT` |
| 10 | Authority subprecedence | Ambiguous, invalid, revoked, stale, then out-of-scope order aligns. | `CONSISTENT` |
| 11 | Generic-context subprecedence | Opaque FSM/recovery context is deliberately non-decisional, not generic asset-class context. | `NOT APPLICABLE` |
| 12 | Collision behavior | Direct tests and acceptance preserve the governed winner for every required collision class. | `CONSISTENT` |
| 13 | Unknown or undefined behavior | Later founder record makes `UNKNOWN_CONDITION` vocabulary-only and retains exactly three undefined predicates. | `CONSISTENT` |
| 14 | Exception behavior | Unknown raw state values and invalid typed structures fail before decision creation as governed. | `CONSISTENT` |
| 15 | Schema-to-Python parity | Schema vocabularies, request/decision shapes, emittable subsets, and evaluator-owned procedure align. | `CONSISTENT` |
| 16 | Contract-to-implementation parity | External descriptive facts remain non-executable and all final mappings align. | `CONSISTENT` |
| 17 | Implementation-to-test parity | Tests assert the implementation's branches, collisions, opacity, preservation, and non-mutation. | `CONSISTENT` |
| 18 | Evidence-to-acceptance parity | Acceptance cites and accurately describes the implementation and test evidence. | `CONSISTENT` |
| 19 | Acceptance-to-index parity | README preserves acceptance scope and non-authorization without semantic expansion. | `CONSISTENT` |
| 20 | Non-authorization boundary | No rollback, recovery, reset, FSM mutation, runtime, or execution authority is created. | `CONSISTENT` |

Final lane determination: `CONSISTENT`.

### 3. Asset-Class Deferral / No-Action

| # | Semantic comparison | Cross-file finding | Determination |
| --- | --- | --- | --- |
| 1 | Governed subject | Pure generic asset-class deferral/no-action classification remains descriptive. | `CONSISTENT` |
| 2 | Input vocabulary | Three asset classes, evidence, posture context, optional authority, and correlation align after supersession. | `CONSISTENT` |
| 3 | Input type and strictness | Schema-owned types and typed Python fields align within the governed typed-request boundary. | `CONSISTENT` |
| 4 | Required versus optional fields | Required request shape and required nullable authority field align. | `CONSISTENT` |
| 5 | Omission versus explicit null | Authority absence is represented consistently as the governed nullable value. | `CONSISTENT` |
| 6 | Enum or literal values | Three classes, two outcomes, 13 reasons, and five actions align. | `CONSISTENT` |
| 7 | Output vocabulary | Decision fields and intentionally non-emitted vocabulary values align. | `CONSISTENT` |
| 8 | Decision mapping | Nine final mappings apply the superseding semantics and schema-consistency decisions. | `CONSISTENT` |
| 9 | Precedence | Contradiction, four undefined predicates, exclusion, authority, evidence, deferral, and fallback order aligns. | `CONSISTENT` |
| 10 | Authority subprecedence | Ambiguous, invalid, revoked, stale, then out-of-scope order aligns. | `CONSISTENT` |
| 11 | Generic-context subprecedence | This generic lane has no nested generic-context subprecedence. | `NOT APPLICABLE` |
| 12 | Collision behavior | Direct tests preserve contradiction, undefined, exclusion, authority, and lower-branch ordering. | `CONSISTENT` |
| 13 | Unknown or undefined behavior | Unknown raw asset classes are rejected; `UNKNOWN_ASSET_CLASS` is vocabulary-only; exactly four typed predicates are undefined. | `CONSISTENT` |
| 14 | Exception behavior | Unknown raw asset class and malformed typed objects are handled within the final governed boundary. | `CONSISTENT` |
| 15 | Schema-to-Python parity | Closed values, fields, nullability, and evaluator-owned procedural semantics align. | `CONSISTENT` |
| 16 | Contract-to-implementation parity | Later records correctly replace the earlier unknown-output and open-invariant wording. | `CONSISTENT` |
| 17 | Implementation-to-test parity | Tests assert the final implementation behavior, not the superseded behavior. | `CONSISTENT` |
| 18 | Evidence-to-acceptance parity | Acceptance explicitly records non-emission and final four-predicate precedence. | `CONSISTENT` |
| 19 | Acceptance-to-index parity | README accurately records those non-emission and boundary conclusions. | `CONSISTENT` |
| 20 | Non-authorization boundary | Eligibility, selection, runtime, integration, and execution remain excluded. | `CONSISTENT` |

Final lane determination: `CONSISTENT`.

### 4. Stock Deferral / No-Action

| # | Semantic comparison | Cross-file finding | Determination |
| --- | --- | --- | --- |
| 1 | Governed subject | Stock-specific descriptive deferral/no-action remains independent of the generic lane. | `CONSISTENT` |
| 2 | Input vocabulary | Stock evidence, posture, lane confirmation, generic context, authority, and references align. | `CONSISTENT` |
| 3 | Input type and strictness | Typed request, nested-object, Boolean, enum, and reference contracts align within the governed domain. | `CONSISTENT` |
| 4 | Required versus optional fields | Ten required fields and three optional context fields align. | `CONSISTENT` |
| 5 | Omission versus explicit null | Missing lane/context/authority states retain the schema and Python absence behavior selected for this lane. | `CONSISTENT` |
| 6 | Enum or literal values | Two outcomes, 22 reasons, five actions, three emittable actions, lane values, and asset classes align. | `CONSISTENT` |
| 7 | Output vocabulary | Five decision fields and emittable-action restrictions align. | `CONSISTENT` |
| 8 | Decision mapping | All 20 mappings align. | `CONSISTENT` |
| 9 | Precedence | The exact 20-step first-match order aligns. | `CONSISTENT` |
| 10 | Authority subprecedence | Contradictory, ambiguous, invalid, revoked, stale, then out of scope aligns. | `CONSISTENT` |
| 11 | Generic-context subprecedence | Contradictory, invalid, non-Stock, stale, then out of scope aligns with its governed mapping. | `CONSISTENT` |
| 12 | Collision behavior | Required global and nested collision winners align. | `CONSISTENT` |
| 13 | Unknown or undefined behavior | Unknown raw values are rejected and exactly three undefined evidence predicates are classified. | `CONSISTENT` |
| 14 | Exception behavior | Invalid enums, nested objects, actions, and empty required references follow the governed boundary. | `CONSISTENT` |
| 15 | Schema-to-Python parity | Vocabularies, structures, optional contexts, decision restrictions, and serialized shapes align. | `CONSISTENT` |
| 16 | Contract-to-implementation parity | Stock restriction/exclusion remain descriptive and generic context remains non-authorizing. | `CONSISTENT` |
| 17 | Implementation-to-test parity | Tests assert every branch, collision class, reference, purity, and non-mutation behavior. | `CONSISTENT` |
| 18 | Evidence-to-acceptance parity | Acceptance accurately cites the implementation and completed direct evidence. | `CONSISTENT` |
| 19 | Acceptance-to-index parity | README accurately records bounded acceptance and exclusions. | `CONSISTENT` |
| 20 | Non-authorization boundary | No eligibility, selection, orchestration, runtime, market, order, or execution authority is added. | `CONSISTENT` |

Final lane determination: `CONSISTENT`.

### 5. Options Deferral / No-Action

| # | Semantic comparison | Cross-file finding | Determination |
| --- | --- | --- | --- |
| 1 | Governed subject | Options-specific descriptive deferral/no-action remains independent of Stock and generic lanes. | `CONSISTENT` |
| 2 | Input vocabulary | Options evidence, posture, lane confirmation, generic context, authority, and references align. | `CONSISTENT` |
| 3 | Input type and strictness | Governed typed fields, strict Booleans, enums, nested objects, and references align. | `CONSISTENT` |
| 4 | Required versus optional fields | Ten required request fields and three optional contexts align. | `CONSISTENT` |
| 5 | Omission versus explicit null | Absent optional lane, generic, and authority context has the same non-authorizing meaning. | `CONSISTENT` |
| 6 | Enum or literal values | Two outcomes, 22 reasons, five actions, three emittable actions, lane values, and asset classes align. | `CONSISTENT` |
| 7 | Output vocabulary | Decision fields and emittable restrictions align. | `CONSISTENT` |
| 8 | Decision mapping | All 20 branch mappings align. | `CONSISTENT` |
| 9 | Precedence | Exact 20-step first-match order aligns. | `CONSISTENT` |
| 10 | Authority subprecedence | Contradictory, ambiguous, invalid, revoked, stale, then out of scope aligns. | `CONSISTENT` |
| 11 | Generic-context subprecedence | Contradictory, ambiguous/invalid, non-Options, stale, then out of scope aligns. | `CONSISTENT` |
| 12 | Collision behavior | Direct evidence preserves global and nested winners. | `CONSISTENT` |
| 13 | Unknown or undefined behavior | Unknown enums are rejected and exactly three typed predicates are undefined. | `CONSISTENT` |
| 14 | Exception behavior | Boolean, enum, nested-object, action, and empty-reference boundaries align. | `CONSISTENT` |
| 15 | Schema-to-Python parity | Vocabularies, structures, optional contexts, and emittable output restrictions align. | `CONSISTENT` |
| 16 | Contract-to-implementation parity | Options-specific semantics do not inherit Stock, selection, or contract behavior. | `CONSISTENT` |
| 17 | Implementation-to-test parity | Tests assert the governed branches, strict boundaries, collisions, and preservation. | `CONSISTENT` |
| 18 | Evidence-to-acceptance parity | Acceptance accurately records independently reproduced evidence. | `CONSISTENT` |
| 19 | Acceptance-to-index parity | README accurately records the bounded acceptance without expansion. | `CONSISTENT` |
| 20 | Non-authorization boundary | No contract selection, chain data, market, runtime, order, or execution authority is created. | `CONSISTENT` |

Final lane determination: `CONSISTENT`.

### 6. Crypto Deferral / No-Action

| # | Semantic comparison | Cross-file finding | Determination |
| --- | --- | --- | --- |
| 1 | Governed subject | Crypto-specific descriptive deferral/no-action remains independent and non-operational. | `CONSISTENT` |
| 2 | Input vocabulary | Crypto evidence, posture, lane confirmation, generic context, authority, and opaque references align. | `CONSISTENT` |
| 3 | Input type and strictness | Strict Booleans/enums align, but request, nested, and decision reference constructors accept non-string truthy values despite the exact `str` contract. | `INCONSISTENT` |
| 4 | Required versus optional fields | Ten required fields and three optional contexts align. | `CONSISTENT` |
| 5 | Omission versus explicit null | Optional contextual absence retains the same non-authorizing meaning across surfaces. | `CONSISTENT` |
| 6 | Enum or literal values | Exact 12-symbol API and all closed vocabularies align. | `CONSISTENT` |
| 7 | Output vocabulary | Five decision fields and three emittable actions align. | `CONSISTENT` |
| 8 | Decision mapping | All 20 branch mappings align. | `CONSISTENT` |
| 9 | Precedence | Exact 20-step first-match order aligns. | `CONSISTENT` |
| 10 | Authority subprecedence | Contradictory, ambiguous, invalid, revoked, stale, then out of scope aligns. | `CONSISTENT` |
| 11 | Generic-context subprecedence | Contradictory, ambiguous/invalid, non-Crypto, stale, then out of scope aligns. | `CONSISTENT` |
| 12 | Collision behavior | Global, generic, and authority collision evidence aligns. | `CONSISTENT` |
| 13 | Unknown or undefined behavior | Unknown enums fail before decision construction and exactly three predicates are undefined. | `CONSISTENT` |
| 14 | Exception behavior | Founder-selected wrong-type rejection has no exception for truthy non-string request, nested, or decision references. | `INCONSISTENT` |
| 15 | Schema-to-Python parity | Schema requires string references with minimum length one; Python accepts values such as integer `1` for those fields. | `INCONSISTENT` |
| 16 | Contract-to-implementation parity | The exact typed contract requires mandatory opaque strings and strict wrong-type rejection, which the reference constructors do not enforce. | `INCONSISTENT` |
| 17 | Implementation-to-test parity | Required strict raw-reference evidence is absent: tests reject empty strings but do not test non-string references accepted by implementation. | `REQUIRED SEMANTIC LINK MISSING` |
| 18 | Evidence-to-acceptance parity | Acceptance describes strict typed-input boundaries without recording the non-string reference acceptance or missing direct evidence. | `INCONSISTENT` |
| 19 | Acceptance-to-index parity | README repeats the accepted `strict typed boundaries` characterization although the reference boundary is not strict. | `INCONSISTENT` |
| 20 | Non-authorization boundary | No wallet, chain, market, runtime, order, transaction, or execution authority is created. | `CONSISTENT` |

Final lane determination: `INCONSISTENT`.

### 7. Asset-Class Eligibility / Exclusion

| # | Semantic comparison | Cross-file finding | Determination |
| --- | --- | --- | --- |
| 1 | Governed subject | Generic asset-class eligibility/exclusion remains a descriptive continuation classification only. | `CONSISTENT` |
| 2 | Input vocabulary | Three classes, evidence-quality facts, three postures, optional authority, and references align. | `CONSISTENT` |
| 3 | Input type and strictness | Exact enum, strict Boolean, nested-object, and reference boundaries align. | `CONSISTENT` |
| 4 | Required versus optional fields | Ten required request fields and omission-only optional authority align. | `CONSISTENT` |
| 5 | Omission versus explicit null | Omitted authority is accepted; explicit `None`/JSON null is rejected as governed. | `CONSISTENT` |
| 6 | Enum or literal values | Three classes, four outcomes, 15 reasons, five actions, three emittable actions, and validity values align. | `CONSISTENT` |
| 7 | Output vocabulary | Six decision fields and emittable-action restriction align. | `CONSISTENT` |
| 8 | Decision mapping | Exact 12-step mappings, conflicts, exclusion/restriction semantics, and fallback align. | `CONSISTENT` |
| 9 | Precedence | Exact first-match order aligns. | `CONSISTENT` |
| 10 | Authority subprecedence | Six-step order and mappings align. | `CONSISTENT` |
| 11 | Generic-context subprecedence | This is the generic classifier and has no nested generic-context object. | `NOT APPLICABLE` |
| 12 | Collision behavior | Direct evidence covers global and all required authority collisions. | `CONSISTENT` |
| 13 | Unknown or undefined behavior | Unknown values reject; exactly three evidence predicates are undefined. | `CONSISTENT` |
| 14 | Exception behavior | Exact `TypeError`/`ValueError` boundaries align with schema and API. | `CONSISTENT` |
| 15 | Schema-to-Python parity | Fields, order, requiredness, omission/null, enums, strict types, references, and actions align. | `CONSISTENT` |
| 16 | Contract-to-implementation parity | Implementation preserves descriptive meanings and all founder-selected mappings. | `CONSISTENT` |
| 17 | Implementation-to-test parity | Tests assert the exact implementation and required collisions without contrary behavior. | `CONSISTENT` |
| 18 | Evidence-to-acceptance parity | Acceptance accurately records the implementation and evidence-completion chain. | `CONSISTENT` |
| 19 | Acceptance-to-index parity | README accurately characterizes the bounded accepted evaluator. | `CONSISTENT` |
| 20 | Non-authorization boundary | No asset selection, integration, runtime, trading, or execution authority is created. | `CONSISTENT` |

Final lane determination: `CONSISTENT`.

### 8. Stock Eligibility / Exclusion

| # | Semantic comparison | Cross-file finding | Determination |
| --- | --- | --- | --- |
| 1 | Governed subject | One opaque Stock reference is classified descriptively without lookup or selection. | `CONSISTENT` |
| 2 | Input vocabulary | Exact request, lane, generic, authority, posture, evidence, and reference vocabulary aligns. | `CONSISTENT` |
| 3 | Input type and strictness | Exact enum, Boolean, nested-object, reference, subclass, and alternate-shape boundaries align. | `CONSISTENT` |
| 4 | Required versus optional fields | Ten required fields and the three governed optional contexts align. | `CONSISTENT` |
| 5 | Omission versus explicit null | Lane confirmation permits omission/null; generic and authority are omission-only, exactly as governed. | `CONSISTENT` |
| 6 | Enum or literal values | Six enums and exact 12-symbol `__all__` align. | `CONSISTENT` |
| 7 | Output vocabulary | Six decision fields, 23 reasons, and three emittable actions align. | `CONSISTENT` |
| 8 | Decision mapping | Exact 16-branch mappings align. | `CONSISTENT` |
| 9 | Precedence | Exact 16-step first-match order aligns. | `CONSISTENT` |
| 10 | Authority subprecedence | Six-step order and all 14 pairwise collision winners align. | `CONSISTENT` |
| 11 | Generic-context subprecedence | Six-step order and all 14 pairwise collision winners align. | `CONSISTENT` |
| 12 | Collision behavior | Posture, global, generic, authority, and independent 32,768-state evidence align. | `CONSISTENT` |
| 13 | Unknown or undefined behavior | Unknown values reject; exactly three evidence predicates are undefined; fallback is total. | `CONSISTENT` |
| 14 | Exception behavior | Exact strict runtime `TypeError` and `ValueError` boundaries align. | `CONSISTENT` |
| 15 | Schema-to-Python parity | Exact structural, vocabulary, nullability, reference, and emittable-action parity aligns. | `CONSISTENT` |
| 16 | Contract-to-implementation parity | Stock Deferral remains unchanged and no package-root eligibility export is introduced. | `CONSISTENT` |
| 17 | Implementation-to-test parity | Direct tests and the independent oracle assert the actual evaluator without production coupling. | `CONSISTENT` |
| 18 | Evidence-to-acceptance parity | Acceptance accurately records both implementation and equality-evidence completion. | `CONSISTENT` |
| 19 | Acceptance-to-index parity | README records the exact provenance and no operative authority. | `CONSISTENT` |
| 20 | Non-authorization boundary | No selection, market, broker, wallet, routing, order, runtime, or execution authority is created. | `CONSISTENT` |

Final lane determination: `CONSISTENT`.

### 9. Options Eligibility / Exclusion

| # | Semantic comparison | Cross-file finding | Determination |
| --- | --- | --- | --- |
| 1 | Governed subject | Options eligibility/exclusion remains descriptive and does not select a contract or strategy. | `CONSISTENT` |
| 2 | Input vocabulary | Exact request, authority, posture, evidence, and reference vocabulary aligns. | `CONSISTENT` |
| 3 | Input type and strictness | Exact enum, Boolean, authority-object, reference, alternate-shape, and request boundaries align. | `CONSISTENT` |
| 4 | Required versus optional fields | Ten required request fields and omission-only authority align. | `CONSISTENT` |
| 5 | Omission versus explicit null | Authority omission is accepted and explicit `None`/JSON null is rejected. | `CONSISTENT` |
| 6 | Enum or literal values | Four enums and exact nine-symbol `__all__` align. | `CONSISTENT` |
| 7 | Output vocabulary | Six decision fields, 15 reasons, and three emittable actions align. | `CONSISTENT` |
| 8 | Decision mapping | Exact 12-step mappings align. | `CONSISTENT` |
| 9 | Precedence | Exact 12-step first-match order aligns. | `CONSISTENT` |
| 10 | Authority subprecedence | Six-step order and all 14 collision winners align, including independent out-of-scope evidence. | `CONSISTENT` |
| 11 | Generic-context subprecedence | Options governance deliberately defines no generic-context object for this lane. | `NOT APPLICABLE` |
| 12 | Collision behavior | Posture, undefined, authority, and 6,272-combination independent evidence align. | `CONSISTENT` |
| 13 | Unknown or undefined behavior | Unknown values reject and exactly three evidence predicates are undefined. | `CONSISTENT` |
| 14 | Exception behavior | Exact strict `TypeError` and `ValueError` boundaries align. | `CONSISTENT` |
| 15 | Schema-to-Python parity | Exact fields, order, omission/null, vocabulary, reference, and action parity aligns. | `CONSISTENT` |
| 16 | Contract-to-implementation parity | Options Deferral and package initializer remain unchanged and unexported eligibility is preserved. | `CONSISTENT` |
| 17 | Implementation-to-test parity | Completed direct tests assert the implementation's exact authority and branch behavior. | `CONSISTENT` |
| 18 | Evidence-to-acceptance parity | Acceptance accurately records the direct-test evidence completion and independent audit. | `CONSISTENT` |
| 19 | Acceptance-to-index parity | README records the exact provenance and no next-lane authority. | `CONSISTENT` |
| 20 | Non-authorization boundary | No chain, contract, market, broker, wallet, order, runtime, or execution authority is created. | `CONSISTENT` |

Final lane determination: `CONSISTENT`.

### 10. Crypto Eligibility / Exclusion

| # | Semantic comparison | Cross-file finding | Determination |
| --- | --- | --- | --- |
| 1 | Governed subject | One opaque Crypto reference is classified without token, pair, venue, chain, wallet, or protocol interpretation. | `CONSISTENT` |
| 2 | Input vocabulary | Exact request, lane, generic, authority, posture, evidence, and reference vocabulary aligns. | `CONSISTENT` |
| 3 | Input type and strictness | Exact enum, Boolean, nested-object, reference, subclass, and alternate-shape boundaries align. | `CONSISTENT` |
| 4 | Required versus optional fields | Ten required fields and three governed optional contexts align. | `CONSISTENT` |
| 5 | Omission versus explicit null | Lane confirmation permits omission/null; generic and authority are omission-only. | `CONSISTENT` |
| 6 | Enum or literal values | Six enums and exact 12-symbol `__all__` align. | `CONSISTENT` |
| 7 | Output vocabulary | Six decision fields, 23 reasons, and exactly three emittable actions align. | `CONSISTENT` |
| 8 | Decision mapping | Exact 16-branch mappings align. | `CONSISTENT` |
| 9 | Precedence | Exact 16-step first-match order aligns. | `CONSISTENT` |
| 10 | Authority subprecedence | Six-step order and all 14 independent collision winners align. | `CONSISTENT` |
| 11 | Generic-context subprecedence | Six-step order and all 14 independent collision winners align. | `CONSISTENT` |
| 12 | Collision behavior | Posture, 102 global collisions, two 14-collision audits, and 32,768-state oracle align. | `CONSISTENT` |
| 13 | Unknown or undefined behavior | Unknown and invalid nulls reject; exactly three predicates are undefined; fallback is total. | `CONSISTENT` |
| 14 | Exception behavior | Exact strict runtime exceptions and no-coercion rules align. | `CONSISTENT` |
| 15 | Schema-to-Python parity | Exact structures, order, vocabularies, nullability, references, and actions align. | `CONSISTENT` |
| 16 | Contract-to-implementation parity | All 20 caller-context domains remain excluded from the implementation surface as governed. | `CONSISTENT` |
| 17 | Implementation-to-test parity | Direct tests and independent oracle assert actual behavior without production-helper coupling. | `CONSISTENT` |
| 18 | Evidence-to-acceptance parity | Acceptance accurately records the implementation, direct tests, collision audits, and exhaustive oracle. | `CONSISTENT` |
| 19 | Acceptance-to-index parity | README accurately records provenance, bounded acceptance, and prohibited capabilities. | `CONSISTENT` |
| 20 | Non-authorization boundary | No blockchain, exchange, wallet, custody, market, routing, order, runtime, or execution authority is created. | `CONSISTENT` |

Final lane determination: `CONSISTENT`.

## Contract-to-Founder-Decision Findings

Later founder records resolve the earlier proposal questions for all ten
lanes. Rollback's `UNKNOWN_CONDITION` and Asset-Class Deferral's
`UNKNOWN_ASSET_CLASS` are correctly treated under their later controlling
non-emission decisions.

For the FSM, final `FSM-SCHEMA-06` states that allowed decisions result in the
requested state and denied decisions retain the current state. A
`lockout_required` collision with a non-lockout request cannot satisfy that
invariant under either committed downstream interpretation: the schema uses
`allowed = false` with `resulting_state = LOCKOUT`, while implementation and
test use `allowed = true` with the same non-requested resulting state. This is
not a wording difference; it is a governed semantic contradiction.

## Governance-to-Schema/Interface Findings

Nine lanes' final governance is reflected by their schemas/interfaces within
the selected boundary.

The FSM schema differs from its final founder semantics in three material
ways:

1. `$defs.RequiredAction` accepts `null` in addition to the five values, while
   final `FSM-SCHEMA-09` says the set remains exactly five values.
2. Conditional rules require valid authority for arming/reset and affirmative
   readiness/position/cooldown facts. They therefore reject valid typed
   denial-classification inputs for which the reason vocabulary and Python
   evaluator define `AUTHORITY_MISSING`, `READINESS_FACTS_MISSING`,
   `CONFIRMED_POSITION_FACT_MISSING`, `POSITION_CLOSED_FACT_MISSING`,
   `COOLDOWN_FACT_MISSING`, or reset denial.
3. The lockout conditional fixes `allowed = false` and
   `resulting_state = LOCKOUT`, which conflicts with the general final
   denied-to-current invariant.

## Schema/Interface-to-Implementation Findings

Eight lane implementations preserve their governing schema/interface semantics
within their typed domains.

The FSM implementation accepts and classifies the negative fact and absent or
invalid authority requests that the schema conditionals reject. It also emits
`allowed = true` for `lockout_required`, while the schema requires
`allowed = false`. Python has five non-null RequiredAction enum values while
the schema permits a sixth, null output possibility.

These are schema-to-implementation widening/narrowing and mapping differences,
not different wording for the same behavior.

The Crypto Deferral schema requires every request, nested-context, authority,
and decision reference to be a string of minimum length one. Its final founder
record also requires mandatory opaque strings, strict typed boundaries, wrong-
type rejection, and direct strict reference evidence. The Python dataclasses
check only truthiness for these references, so a truthy non-string value such
as integer `1` is accepted. That is a schema/interface-to-implementation
widening inside an expressly strict typed boundary.

## Implementation-to-Test Findings

Nine direct-test files describe the behavior of their corresponding
implementations. The FSM test at the lockout-precedence branch explicitly
asserts `allowed = true`, so the test agrees with the implementation but
preserves rather than detects the schema/founder mismatch.

The Crypto Deferral direct tests reject empty references but do not exercise
non-string truthy references, despite the founder record's required strict raw-
reference rejection. The missing comparison lets the implementation widening
remain unobserved.

The remaining eight test files align with their implementation semantics,
including final supersession decisions, strict governed boundaries,
precedence, collision evidence, reference preservation, purity, and
non-mutation where required.

## Test/Evidence-to-Acceptance Findings

Eight formal acceptances accurately describe the implementation and test
evidence they cite.

The FSM acceptance cites the final schema and `FSM-SCHEMA-01` through
`FSM-SCHEMA-11`, then states that the isolated evaluator satisfies its bounded
implementation contract. It does not identify the nullable-action,
conditional-denial, lockout-flag, or allowed/resulting-state differences. The
acceptance claim is therefore not semantically supported by the complete cited
chain, even though its recorded tests passed.

The Crypto Deferral acceptance describes strict typed-input boundaries and
completed direct-test evidence but does not record that truthy non-string
references are accepted or that direct strict reference-type evidence is
missing. That acceptance claim is broader than the committed implementation
and test evidence supports.

## Acceptance-to-README Findings

Every exact README entry preserves its acceptance's non-authorization
language. Nine entries add no semantic characterization beyond their accepted
records. The Crypto Deferral entry repeats `strict typed boundaries`, which is
not fully supported for references by the implementation/test chain.

For the FSM, the index accurately says the local implementation/test evidence
was accepted and that unavailable remote CI was not proof. It does not assert
the disputed lockout value directly. The semantic defect is in the underlying
governance/schema/implementation/acceptance chain, not a separate README
mischaracterization. The separate Crypto Deferral index finding is the strict-
typed-boundary overstatement described above.

## Shared-Term Findings

| Shared term | Cross-lane meaning | Determination |
| --- | --- | --- |
| `ELIGIBLE` | In every eligibility lane, descriptive continued Stage 2 consideration only, never permission or execution authority. | `CONSISTENT` |
| `INELIGIBLE` | Not a governed output or shared decision term in the ten final evaluator contracts. | `NOT APPLICABLE` |
| `EXCLUDED` | Eligibility lanes emit descriptive exclusion; deferral lanes consume exclusion as a safe no-action fact. The difference follows lane purpose. | `INTENTIONALLY LANE-SPECIFIC` |
| `DEFER` | Across Rollback and Deferral lanes, review pauses pending evidence or human handling and never grants action. | `CONSISTENT` |
| `NO_ACTION` | Across Rollback and Deferral lanes, no operative action follows and no permission is implied. | `CONSISTENT` |
| `ALLOW` | Only the FSM has an `allowed` transition flag; eligibility contracts expressly do not convert classification into ALLOW authority. | `INTENTIONALLY LANE-SPECIFIC` |
| `DENY` | FSM denial is transition-descriptive; other lanes use their closed outcomes/reasons rather than a universal DENY output. | `INTENTIONALLY LANE-SPECIFIC` |
| `UNKNOWN` | FSM has `UNKNOWN_STATE`; Rollback and Asset-Class Deferral retain non-emittable unknown reasons; later typed lanes reject unknown values. | `INTENTIONALLY LANE-SPECIFIC` |
| `UNDEFINED` | Each lane defines only its own closed valid-typed undefined conditions or transitions. | `INTENTIONALLY LANE-SPECIFIC` |
| Authority evidence | All uses are caller-supplied, bounded, fail-closed, and non-authorizing; shapes and failure orders are separately governed. | `INTENTIONALLY LANE-SPECIFIC` |
| Generic context | Present only in selected Stock/Options/Crypto lanes as optional non-authorizing context; absence elsewhere is explicit. | `INTENTIONALLY LANE-SPECIFIC` |
| Precedence | Every evaluator uses deterministic first-match precedence within its own closed table. | `CONSISTENT` |
| Collision | Multiple simultaneously true governed conditions are resolved by the selected first-match or nested subprecedence rule. | `CONSISTENT` |
| Rollback | Operational rollback is excluded everywhere; only the Rollback lane classifies supplied rollback facts. | `INTENTIONALLY LANE-SPECIFIC` |
| Fallback | Each lane's final safe fallback is separately governed and does not create permission; exact outcome/reason differs by subject. | `INTENTIONALLY LANE-SPECIFIC` |

## Intentional Lane-Specific Differences

Nine shared-term findings are `INTENTIONALLY LANE-SPECIFIC`:

* exclusion maps to an `EXCLUDED` eligibility outcome but to safe
  `NO_ACTION` in deferral lanes;
* transition `ALLOW`/`DENY` is confined to the FSM and is not inherited as
  eligibility or execution authority;
* unknown and undefined conditions use only each lane's closed founder-selected
  treatment;
* authority-evidence representations and subprecedence differ only where each
  lane expressly selects them;
* generic context exists only in lanes that expressly select it;
* rollback classification is confined to the Rollback lane; and
* deterministic fallback mappings are subject-specific.

These differences are bounded and do not create a cross-lane inconsistency.

## Inconsistencies, If Any

Fourteen semantic matrix positions are `INCONSISTENT`: eight in the Pure /
Canonical FSM lane and six in Crypto Deferral / No-Action.

FSM findings:

1. Required/optional semantics: schema conditionals reject denial inputs that
   the evaluator accepts and classifies.
2. Omission/null semantics: schema rejects absent/null authority for
   authority-required transitions while evaluator emits governed denial
   reasons for it.
3. Output vocabulary: schema permits nullable RequiredAction after the final
   founder record closes the set at five non-null values.
4. Decision mapping: lockout precedence requires `allowed = false` in schema
   but `allowed = true` in implementation and test.
5. Collision behavior: the lockout collision winner's `allowed` meaning
   differs even though lockout wins in both artifacts.
6. Schema-to-Python parity: conditional denial, nullable action, and lockout
   mappings diverge.
7. Contract-to-implementation parity: the lockout result violates the final
   allowed-to-requested/denied-to-current invariant for a non-lockout request.
8. Evidence-to-acceptance parity: acceptance states contract conformance
   without recording these differences.

Crypto Deferral findings:

1. Input strictness: truthy non-string request, nested, and decision references
   are accepted despite the exact string contract.
2. Exception behavior: wrong reference types do not raise the governed
   rejection exception.
3. Schema-to-Python parity: schema `type: string` constraints are wider in the
   Python runtime surface.
4. Contract-to-implementation parity: mandatory opaque string and strict
   wrong-type rejection decisions are not enforced for references.
5. Evidence-to-acceptance parity: acceptance records strict typed boundaries
   without the contrary runtime behavior or missing direct evidence.
6. Acceptance-to-index parity: README repeats the unsupported strict typed-
   boundary characterization.

No inconsistency is repaired by this artifact.

## Missing Semantic Links, If Any

Two findings are `REQUIRED SEMANTIC LINK MISSING`.

The FSM schema permits one `AuthorityEvidence` object to contain multiple
simultaneous failure facts. The final founder records define which individual
failures deny authority but do not define which reason/action wins a
multi-failure collision. The implementation silently chooses this effective
order: absence, stale, revoked, out of scope, then invalid, with additional
presence/currentness/reference fallbacks. Direct tests do not establish a
founder-selected collision order.

The missing link is recorded only. No subprecedence is selected here.

The Crypto Deferral founder record requires direct strict raw-reference
rejection evidence. The committed direct test checks empty strings but not a
non-string reference, and the implementation accepts truthy non-string values.
The required contract-to-test semantic link is therefore missing. No test is
added here.

## Unresolved Findings, If Any

None. Zero findings are `UNRESOLVED`.

The FSM contradictions are classified as concrete inconsistencies, and its
authority-collision gap is classified as a missing semantic link. No
additional interpretation is required to state those findings.

## Composite Semantic-Consistency Determination

**FAIL.**

The review examined 215 semantic comparisons: 200 per-lane matrix positions
and 15 shared terms. Findings are:

* `CONSISTENT`: 184;
* `INTENTIONALLY LANE-SPECIFIC`: 9;
* `INCONSISTENT`: 14;
* `REQUIRED SEMANTIC LINK MISSING`: 2;
* `UNRESOLVED`: 0; and
* `NOT APPLICABLE`: 6.

Eight lanes are `CONSISTENT`. The Pure / Canonical FSM and Crypto Deferral /
No-Action lanes are `INCONSISTENT`; each also lacks one required semantic
link. Composite PASS is therefore unavailable.

This FAIL does not reject or repair code, rescind a historical acceptance,
accept Stage 2 as a whole, certify completion, update the Advancement Gate,
authorize another lane, or authorize Stage 3.

## Explicit Exclusions

This review does not determine or authorize:

* whether the ten lanes compose safely;
* orchestration correctness or global system completeness;
* a universal shared contract or normalized terminology;
* overall Stage 2 evidence acceptance or a Stage 2 completion certificate;
* an updated Advancement Gate outcome, Stage 2 advancement, or Stage 3 entry;
* any repair, source, schema, test, package, validator, workflow, dependency,
  configuration, or acceptance amendment;
* another governance or implementation subject;
* integration, orchestration, runtime registration, deployment, or live-money
  wiring; or
* market-data, signal, strategy, risk, sizing, allocation, broker, exchange,
  wallet, custody, networking, persistence, registration, routing, order,
  transaction, execution, or live-money behavior.

Semantic review is not repair authority. A finding is not an implementation
task order. Lane-level acceptance is not overall Stage 2 acceptance.

## Stage 2 HOLD Preservation

Stage 2 remains **HOLD**. This review does not change, refresh, supersede, or
replace the historical Advancement Gate decision. The composite FAIL does not
authorize repair, and the nine consistent lane findings do not certify Stage 2
completion or permit advancement.

## Stage 3 Non-Authorization Preservation

Stage 3 remains **UNENTERED AND UNAUTHORIZED**. No founder approval artifact,
implementation task order, repair authority, integration authority, runtime
authority, deployment authority, execution authority, or live-money authority
is created.

## Refusal and Halt Conditions

Refuse and halt any attempt to treat this artifact as:

* authority to repair the FSM schema, implementation, tests, acceptance, or
  README;
* overall Stage 2 evidence acceptance or rejection;
* a Stage 2 completion certificate;
* an updated advancement-gate decision;
* Stage 2 advancement or Stage 3 entry;
* authorization for another lane;
* a founder approval artifact, approval mechanism, or implementation task
  order; or
* integration, orchestration, runtime, deployment, broker, exchange, wallet,
  routing, order, execution, or live-money authority.

Any repair or subsequent governance question requires a separate exact founder
selection and bounded task order.

## Final Determination

Composite cross-file semantic consistency: **FAIL**.

Eight completed evaluator chains are internally `CONSISTENT` within their
final governed boundaries. The Pure / Canonical FSM chain contains eight
`INCONSISTENT` semantic positions involving schema conditional denial inputs,
nullable action vocabulary, lockout mapping/invariants, schema-to-Python and
contract-to-implementation parity, and evidence-to-acceptance parity. It also
contains one `REQUIRED SEMANTIC LINK MISSING` for authority multi-failure
subprecedence.

The Crypto Deferral / No-Action chain contains six `INCONSISTENT` semantic
positions involving non-string reference acceptance, exception and
schema/API parity, contract/implementation parity, and acceptance/index
characterization. It also contains one `REQUIRED SEMANTIC LINK MISSING` for
the required strict raw-reference direct-test evidence.

No finding is repaired.
Overall Stage 2 evidence acceptance is not created.
Stage 2 completion is not certified.
The Advancement Gate decision is unchanged.
Stage 2 remains **HOLD**.
Stage 3 remains **UNENTERED AND UNAUTHORIZED**.
