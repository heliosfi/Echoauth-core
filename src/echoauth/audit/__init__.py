"""Audit append foundations."""

from echoauth.audit.hashing import (
    AUDIT_HASH_FORMAT,
    AuditRecordValidationError,
    audit_event_payload,
    hash_audit_event,
    validate_audit_record,
)
from echoauth.audit.logging import (
    AuditAppendResult,
    AuditAppendState,
    AuditLogRepository,
    AuditRecord,
    AuditRecordResult,
    AuditService,
    AuditStorageState,
)
from echoauth.audit.repository import InMemoryAuditLogRepository, StoredAuditEvent

__all__ = [
    "AUDIT_HASH_FORMAT",
    "AuditAppendResult",
    "AuditAppendState",
    "AuditLogRepository",
    "AuditRecord",
    "AuditRecordResult",
    "AuditRecordValidationError",
    "AuditService",
    "AuditStorageState",
    "InMemoryAuditLogRepository",
    "StoredAuditEvent",
    "audit_event_payload",
    "hash_audit_event",
    "validate_audit_record",
]
