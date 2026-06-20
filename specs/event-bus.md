# Purpose

Define the internal event contract for EchoAuth runtime components.

# Scope

Applies to identity, authority, delegation, policy, invariant, envelope, token,
execution, audit, escalation, recovery, and notification events.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `event_id` | string | yes | Unique event identifier. |
| `event_type` | string | yes | Event name. |
| `producer_id` | string | yes | Component producing event. |
| `request_id` | string | no | Related request. |
| `correlation_id` | string | yes | Cross-component correlation ID. |
| `causation_id` | string | no | Event that caused this event. |
| `payload` | object | yes | Canonical event payload. |
| `occurred_at` | timestamp | yes | Event time. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `delivery_state` | enum | `accepted`, `published`, `rejected`, `dead_lettered`. |
| `subscribers_notified` | list | Subscribers receiving event. |
| `reason` | string | Machine-readable reason. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `received` | `validate` | `accepted` |
| `received` | `validation_failed` | `rejected` |
| `accepted` | `publish` | `published` |
| `published` | `subscriber_failure` | `dead_lettered` |

# Validation Rules

1. Event ID must be unique.
2. Producer must be registered.
3. Payload must match event schema.
4. Correlation ID is mandatory.
5. Event payload must be canonicalizable.
6. Security-sensitive events must require authorized subscribers.

# Failure Conditions

| Condition | Result |
|---|---|
| Duplicate event ID | `rejected` |
| Unknown producer | `rejected` |
| Schema mismatch | `rejected` |
| Subscriber failure | `dead_lettered` |
| Bus unavailable | runtime `hold` or degraded mode |

# Security Requirements

- Authenticate producers.
- Authorize subscribers by event type.
- Do not publish secrets in event payloads.
- Preserve event ordering per request.
- Sign high-integrity events when distributed.

# Audit Requirements

Record event accept/reject, producer, event type, correlation, subscriber
delivery, dead-letter state, and timestamp.

# Persistence Requirements

- Persist events required for replay.
- Persist dead-letter queue.
- Index by request, correlation ID, event type, and producer.
- Store event schema version.

# Deterministic Rules

- Event ordering per `request_id` uses occurred time then event ID.
- Same payload and schema version produce same payload hash.
- Subscriber routing is deterministic by event type and subscription version.

# Examples

```json
{
  "event_id": "evt_bus_001",
  "event_type": "authority.verdict.valid",
  "delivery_state": "published"
}
```
