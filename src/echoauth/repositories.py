"""Repository interfaces for EchoAuth persistence boundaries."""

from __future__ import annotations

from abc import ABC, abstractmethod

from echoauth.models import AuditAppendResult, AuditRecord


class Repository(ABC):
    """Base persistence boundary."""

    @abstractmethod
    def get(self, record_id: str) -> object:
        """Read a record by identifier."""

    @abstractmethod
    def save(self, record: object) -> object:
        """Persist a record."""


class AuthorityRegistryRepository(Repository):
    """Specification: specs/authority-registry.md."""


class RevocationRepository(Repository):
    """Specification: specs/authority-revocation.md."""


class DelegationRepository(Repository):
    """Specification: specs/delegation-model.md."""


class PolicyRegistryRepository(Repository):
    """Specification: specs/policy-registry.md."""


class RuntimeStateRepository(Repository):
    """Specification: specs/runtime-state-machine.md."""


class AuditLogRepository(Repository):
    """Specification: specs/audit-log-spec.md."""

    @abstractmethod
    def append(
        self,
        record: AuditRecord,
        *,
        audit_event_id: str,
        chain_id: str,
        expected_previous_hash: str | None = None,
    ) -> AuditAppendResult:
        """Append one immutable event to an audit chain."""
