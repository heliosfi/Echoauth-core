# Build Readiness Assessment

## Status

Not build-ready as a complete EchoAuth runtime.

## Ready Inputs

| Area | Status |
|---|---|
| Component specifications | Ready |
| Canonical vocabulary | Ready |
| State-machine definitions | Ready |
| Validation/failure/security/audit/persistence rules | Ready |
| Runtime package skeleton | Partial |

## Blocking Gaps

| Gap | Required Repair |
|---|---|
| No packaging metadata | Add `pyproject.toml` or equivalent package configuration. |
| No automated test tree | Replace placeholder `tests` file with test directory and conformance tests. |
| No schema definitions | Generate JSON Schema, Pydantic models, or dataclasses from specs. |
| Partial runtime implementation only | Implement specs in `src/echoauth`. |
| No persistence layer | Add repository interfaces and storage adapters. |
| No event bus | Implement event publishing and subscription contracts. |
| No notification adapter | Implement notification contracts. |
| No CI workflow | Add lint, type, and test automation. |

## Minimum Build Plan

1. Add package metadata.
2. Convert spec tables into typed Python interfaces.
3. Add conformance tests for every state machine.
4. Implement persistence interfaces.
5. Implement audit chain and audit log.
6. Implement request processing through `echoauth-spec.md`.
7. Add CI.

## Assessment

The repository is ready for implementation work but not ready for build
certification. The next build milestone should be a spec-conformance test suite.
