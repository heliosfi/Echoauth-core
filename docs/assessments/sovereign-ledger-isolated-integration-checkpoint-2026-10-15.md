# Sovereign Ledger — isolated C++ integration checkpoint

**Authority:** N.B.C.  
**Date:** 2026-10-15  
**Disposition:** HOLD — source promotion pending, no runtime integration authorized.

## Boundary

This branch is an isolated integration lane for the C++20 Sovereign Ledger prototype. It does **not** replace or modify `specs/audit-chain.md`, `specs/audit-log-spec.md`, `schemas/audit-record.schema.json`, or existing Python audit/runtime services.

The prototype's 80-byte SHA-256 receipt preimage and transition legality model are distinct from EchoAuth's existing audit record, chain ID, event identity, authority and persistence contracts. Hash parity is not evidence of EchoAuth authorization, durable append, replay resistance, or runtime readiness.

## Local verification evidence (2026-10-15)

Executed against the local checkpoint package using GCC 14.2.0, C++20, `-O3 -Wall -Wextra -Werror -msse4.1`:

- Positive production syntax control: PASS.
- `NDEBUG + AUDIT_TEST_HARNESS` rejection: PASS under the tested flag combination.
- Three expected-failure negative compilation checks (fixture inaccessible, final class, non-default constructor): PASS.
- Three SHA-256 NIST known-answer vectors: PASS.
- 257 scalar/SHA-NI differential input lengths (0..256): PASS on the local CPU.
- 80-byte receipt reference/SHA-NI parity: PASS.
- Rejection immutability, saturation latch, valid transition, ordinary C++ `new` tripwire: PASS.
- Regression build/run with AddressSanitizer and UndefinedBehaviorSanitizer: PASS.

These are **local**, not GitHub CI, results. The `new` tripwire does not establish the absence of all allocation mechanisms.

## Required before source promotion

1. Stage the verified `sovereign_ledger.hpp`, `test_full_regression.cpp`, and `run_negative_compile_tests.sh` under an isolated `experimental/sovereign-ledger/` directory.
2. Remove the `ALLOW_TEST_HARNESS_UNDER_NDEBUG` escape hatch or establish an explicitly governed test-only policy; rerun both targets after changes.
3. Preserve the existing audit contract and demonstrate that no production runtime imports or links this module.
4. Run production boundary negatives and ASan/UBSan regression against the **exact committed bytes**, and capture hashes, compiler, CPU capabilities and exit codes.
5. Obtain independent review before considering runtime adapter design. Do not claim durable persistence, signed authority, cross-platform SHA-NI, or zero-allocation proof.

**Promotion gate:** HOLD until the exact module sources are committed and passing tests are attributable to that commit. No merge to `main` under this checkpoint.
