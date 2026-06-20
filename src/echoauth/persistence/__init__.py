"""Persistence foundation exports for EchoAuth Sprint 1."""

from echoauth.persistence.base import (
    InMemoryRepository,
    MissingRecordError,
    RepositoryRecordError,
    StoredRecord,
)

__all__ = [
    "InMemoryRepository",
    "MissingRecordError",
    "RepositoryRecordError",
    "StoredRecord",
]
