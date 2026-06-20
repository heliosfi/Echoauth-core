# Ambiguity Resolution Report

# Scope

Resolved all fields listed in `contracts/ambiguities.md` from the previous
contract generation pass:

- `payload`
- `context`
- `details`
- `evidence`
- `scope`
- `rules`
- `facts`
- `credential_set`
- `credential_refs`
- `role_refs`
- `context_constraints`
- `effective_scope`
- `validation_errors`

# Resolution Summary

| Resolution | Fields |
| --- | --- |
| `CanonicalJsonObject` | `payload`, `context`, `details`, `evidence`, `scope`, `rules`, `facts`, `credential_set`, `context_constraints`, `effective_scope` |
| `StringReferenceList` | `credential_refs`, `role_refs` |
| `ValidationErrorList` | `validation_errors` |

# Updated Artifacts

| Artifact | Update |
| --- | --- |
| `api/openapi.yaml` | Added canonical shared schemas; replaced ambiguous object references with `CanonicalJsonObject`; replaced `validation_errors` with `ValidationErrorList`. |
| `contracts/protobuf/echoauth.proto` | Documented `google.protobuf.Struct` fields as canonical JSON objects without changing wire shape. |
| `schemas/common.schema.json` | Added `CanonicalJsonObject`, `StringReferenceList`, and `ValidationErrorList`. |
| `schemas/echoauth-request.schema.json` | Replaced request `payload` and `context` with `CanonicalJsonObject`. |
| `schemas/authority-resolution.schema.json` | Replaced `context` and record object arrays with `CanonicalJsonObject`. |
| `schemas/audit-record.schema.json` | Replaced `details` with `CanonicalJsonObject`. |
| `events/event-envelope.schema.json` | Documented event `payload` as canonical JSON selected by event type. |
| `events/event-catalog.yaml` | Added payload contract and selection rule. |
| `database/schema.sql` | Added canonical JSON text storage convention for `*_json` columns. |
| `contracts/service-contracts.yaml` | Added canonical data contract definitions. |
| `contracts/integration-contracts.yaml` | Replaced prior ambiguity policy with resolved canonical data contracts. |
| `runtime/dependency-graph.md` | Refreshed decision dependencies. |
| `runtime/traceability-matrix.md` | Refreshed ambiguity and decision traceability. |
| `runtime/coverage-report.md` | Refreshed implementation readiness and exception status. |

# Blocking Issues

None for contract typing.

Nested business schemas remain intentionally unspecified by the existing
specifications. Implementations may not infer nested behavior from the
canonical object type alone.
