-- EchoAuth database contract.
--
-- *_json columns store canonical JSON text for fields resolved as
-- CanonicalJsonObject, StringReferenceList, or ValidationErrorList in
-- schemas/common.schema.json. The approved specifications define
-- deterministic serialization and hashing requirements but do not mandate a
-- database-specific JSON validation function.

CREATE TABLE echoauth_requests (
  request_id TEXT PRIMARY KEY,
  requester_id TEXT NOT NULL,
  subject_id TEXT NOT NULL,
  action TEXT NOT NULL,
  resource TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  context_json TEXT NOT NULL,
  session_id TEXT,
  correlation_id TEXT NOT NULL,
  idempotency_key TEXT NOT NULL UNIQUE,
  request_state TEXT NOT NULL,
  reason TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE identity_verdicts (
  identity_verdict_id TEXT PRIMARY KEY,
  actor_id TEXT NOT NULL,
  actor_type TEXT NOT NULL,
  state TEXT NOT NULL,
  resolved_actor_id TEXT NOT NULL,
  assurance_level TEXT NOT NULL,
  evidence_hash TEXT NOT NULL,
  expires_at TEXT NOT NULL,
  reason TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE authority_records (
  authority_record_id TEXT PRIMARY KEY,
  authority_source_id TEXT NOT NULL,
  subject_id TEXT NOT NULL,
  authority_type TEXT NOT NULL,
  scope_json TEXT NOT NULL,
  priority INTEGER NOT NULL,
  issued_at TEXT NOT NULL,
  expires_at TEXT,
  status TEXT NOT NULL,
  source_document_hash TEXT
);

CREATE TABLE authority_verdicts (
  authority_verdict_id TEXT PRIMARY KEY,
  request_id TEXT NOT NULL,
  state TEXT NOT NULL,
  authority_source_id TEXT,
  authority_type TEXT,
  scope_json TEXT,
  reason TEXT NOT NULL,
  evidence_hash TEXT NOT NULL,
  expires_at TEXT NOT NULL
);

CREATE TABLE delegations (
  delegation_id TEXT PRIMARY KEY,
  grantor_id TEXT NOT NULL,
  delegate_id TEXT NOT NULL,
  subject_id TEXT NOT NULL,
  role TEXT NOT NULL,
  allowed_actions_json TEXT NOT NULL,
  allowed_resources_json TEXT NOT NULL,
  context_constraints_json TEXT NOT NULL,
  issued_at TEXT NOT NULL,
  expires_at TEXT NOT NULL,
  revoked_at TEXT,
  source_authority_reference TEXT NOT NULL
);

CREATE TABLE policy_decisions (
  policy_decision_id TEXT PRIMARY KEY,
  policy_evaluation_id TEXT NOT NULL,
  request_id TEXT NOT NULL,
  decision TEXT NOT NULL,
  reason TEXT NOT NULL,
  matched_policies_json TEXT NOT NULL,
  failed_policies_json TEXT NOT NULL,
  evidence_hash TEXT NOT NULL,
  policy_version TEXT NOT NULL
);

CREATE TABLE invariant_results (
  invariant_result_id TEXT PRIMARY KEY,
  validation_id TEXT NOT NULL,
  request_id TEXT NOT NULL,
  envelope_id TEXT,
  invariant_version TEXT NOT NULL,
  state TEXT NOT NULL,
  failed_invariants_json TEXT NOT NULL,
  reason TEXT NOT NULL,
  facts_hash TEXT NOT NULL
);

CREATE TABLE runtime_envelopes (
  envelope_id TEXT PRIMARY KEY,
  request_id TEXT NOT NULL,
  subject_id TEXT NOT NULL,
  requester_id TEXT NOT NULL,
  authority_verdict_id TEXT NOT NULL,
  delegation_id TEXT,
  action TEXT NOT NULL,
  resource TEXT NOT NULL,
  payload_hash TEXT NOT NULL,
  policy_version TEXT NOT NULL,
  invariant_version TEXT NOT NULL,
  channel_id TEXT NOT NULL,
  nonce TEXT NOT NULL UNIQUE,
  expires_at TEXT NOT NULL,
  audit_sink_id TEXT NOT NULL,
  envelope_state TEXT NOT NULL
);

CREATE TABLE execution_tokens (
  execution_token_id TEXT PRIMARY KEY,
  envelope_id TEXT NOT NULL UNIQUE,
  request_id TEXT NOT NULL,
  authority_verdict_id TEXT NOT NULL,
  action TEXT NOT NULL,
  resource TEXT NOT NULL,
  payload_hash TEXT NOT NULL,
  nonce TEXT NOT NULL UNIQUE,
  issued_at TEXT NOT NULL,
  expires_at TEXT NOT NULL,
  issuer_id TEXT NOT NULL,
  token_state TEXT NOT NULL
);

CREATE TABLE execution_claims (
  claim_id TEXT PRIMARY KEY,
  execution_token_id TEXT NOT NULL,
  executor_id TEXT NOT NULL,
  envelope_id TEXT NOT NULL,
  payload_hash TEXT NOT NULL,
  claimed_at TEXT NOT NULL,
  claim_state TEXT NOT NULL,
  lease_expires_at TEXT
);

CREATE TABLE audit_events (
  audit_event_id TEXT PRIMARY KEY,
  event_type TEXT NOT NULL,
  actor_id TEXT NOT NULL,
  request_id TEXT,
  envelope_id TEXT,
  authority_verdict_id TEXT,
  execution_token_id TEXT,
  state_before TEXT,
  state_after TEXT,
  reason TEXT NOT NULL,
  details_json TEXT NOT NULL,
  occurred_at TEXT NOT NULL,
  event_hash TEXT NOT NULL,
  previous_hash TEXT,
  storage_state TEXT NOT NULL
);

CREATE TABLE event_bus_events (
  event_id TEXT PRIMARY KEY,
  event_type TEXT NOT NULL,
  producer_id TEXT NOT NULL,
  request_id TEXT,
  correlation_id TEXT NOT NULL,
  causation_id TEXT,
  payload_json TEXT NOT NULL,
  occurred_at TEXT NOT NULL,
  delivery_state TEXT NOT NULL
);

CREATE TABLE notifications (
  notification_id TEXT PRIMARY KEY,
  notification_type TEXT NOT NULL,
  recipient_id TEXT NOT NULL,
  recipient_role TEXT NOT NULL,
  request_id TEXT,
  priority TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  expires_at TEXT,
  notification_state TEXT NOT NULL,
  delivery_channel TEXT,
  reason TEXT
);
