"""Runtime configuration loading helpers for Sprint 1."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from echoauth.config import ContractPaths, RuntimeConfig


class ConfigurationError(ValueError):
    """Raised when required runtime configuration is missing or invalid."""


REQUIRED_CONFIG_KEYS = (
    "policy_version",
    "invariant_version",
    "security_profile_id",
    "audit_sink_id",
)


def load_runtime_config(values: Mapping[str, str], root: str | Path = ".") -> RuntimeConfig:
    """Load runtime configuration using repository-defined contract paths."""

    missing = [key for key in REQUIRED_CONFIG_KEYS if not values.get(key)]
    if missing:
        raise ConfigurationError(f"missing required configuration: {', '.join(missing)}")
    contract_paths = ContractPaths()
    resolve_contract_paths(contract_paths, root)
    return RuntimeConfig(
        contract_paths=contract_paths,
        policy_version=values["policy_version"],
        invariant_version=values["invariant_version"],
        security_profile_id=values["security_profile_id"],
        audit_sink_id=values["audit_sink_id"],
    )


def resolve_contract_paths(contract_paths: ContractPaths | None = None, root: str | Path = ".") -> dict[str, Path]:
    """Resolve configured contract paths relative to the repository root."""

    paths = contract_paths or ContractPaths()
    root_path = Path(root)
    resolved = {
        "openapi": root_path / paths.openapi,
        "protobuf": root_path / paths.protobuf,
        "service_contracts": root_path / paths.service_contracts,
        "integration_contracts": root_path / paths.integration_contracts,
        "database_schema": root_path / paths.database_schema,
        "event_catalog": root_path / paths.event_catalog,
    }
    missing = [name for name, path in resolved.items() if not path.is_file()]
    if missing:
        raise ConfigurationError(f"missing contract paths: {', '.join(missing)}")
    return resolved
