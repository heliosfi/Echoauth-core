# Purpose

Define notification contracts for authority review, escalation, refusal,
runtime halt, emergency override, audit alerts, and recovery events.

# Scope

Applies to human notifications, service notifications, audit alerts, escalation
requests, and runtime safety notifications.

# Inputs

| Field | Type | Required | Description |
|---|---:|---:|---|
| `notification_id` | string | yes | Unique notification. |
| `notification_type` | enum | yes | `escalation`, `refusal`, `hold`, `halt`, `revocation`, `emergency`, `audit_alert`, `recovery`. |
| `recipient_id` | string | yes | Recipient actor or service. |
| `recipient_role` | string | yes | Authority or operational role. |
| `request_id` | string | no | Related request. |
| `priority` | enum | yes | `low`, `normal`, `high`, `critical`. |
| `payload` | object | yes | Notification payload. |
| `expires_at` | timestamp | no | Delivery deadline. |

# Outputs

| Field | Type | Description |
|---|---:|---|
| `notification_state` | enum | `queued`, `sent`, `delivered`, `acknowledged`, `failed`, `expired`. |
| `delivery_channel` | string | Channel used. |
| `reason` | string | Machine-readable reason. |

# State Machine

| Current | Event | Next |
|---|---|---|
| `created` | `queue` | `queued` |
| `queued` | `send` | `sent` |
| `sent` | `delivery_confirmed` | `delivered` |
| `delivered` | `acknowledge` | `acknowledged` |
| `queued` | `send_failed` | `failed` |
| any nonterminal | `deadline_elapsed` | `expired` |

# Validation Rules

1. Recipient must be authorized to receive notification type.
2. Payload must match notification schema.
3. Sensitive payload fields must be redacted by recipient role.
4. Critical notifications require delivery tracking.
5. Escalation notifications must link to escalation ID or request ID.
6. Expired notifications must not be treated as acknowledgement.

# Failure Conditions

| Condition | Result |
|---|---|
| Unauthorized recipient | `failed` |
| Unknown channel | `failed` |
| Payload schema mismatch | `failed` |
| Delivery deadline elapsed | `expired` |
| Delivery provider unavailable | `failed` and retry if configured |

# Security Requirements

- Enforce recipient authorization.
- Minimize disclosed evidence.
- Do not send secrets or raw credentials.
- Critical notifications must be tamper-evident.
- Acknowledgement must be attributable to verified identity.

# Audit Requirements

Record notification creation, recipient, type, redaction profile, channel,
send attempts, delivery, acknowledgement, failure, expiration, and timestamp.

# Persistence Requirements

- Persist notification lifecycle.
- Persist redacted payload hash.
- Persist delivery attempts.
- Retain acknowledgement records.
- Index by request, recipient, type, and state.

# Deterministic Rules

- Channel selection uses configured recipient preference, priority, then fallback order.
- Redaction is deterministic by recipient role and notification type.
- Expiration always supersedes late acknowledgement unless policy permits late review.

# Examples

```json
{
  "notification_id": "note_001",
  "notification_type": "escalation",
  "recipient_role": "parent_authority",
  "notification_state": "sent"
}
```
