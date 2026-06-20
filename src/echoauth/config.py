"""Configuration contracts for EchoAuth runtime skeleton."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ContractPaths:
    """Generated contract artifact locations."""

    openapi: str = "api/openapi.yaml"
    protobuf: str = "contracts/protobuf/echoauth.proto"
    service_contracts: str = "contracts/service-contracts.yaml"
    integration_contracts: str = "contracts/integration-contracts.yaml"
    database_schema: str = "database/schema.sql"
    event_catalog: str = "events/event-catalog.yaml"


@dataclass(frozen=True)
class RuntimeConfig:
    """Runtime configuration shape.

    Specification: specs/security-model.md
    Contract: contracts/integration-contracts.yaml
    """

    contract_paths: ContractPaths
    policy_version: str
    invariant_version: str
    security_profile_id: str
    audit_sink_id: str
