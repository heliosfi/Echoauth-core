"""Service wiring contracts for EchoAuth runtime skeleton."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeDependencyEdge:
    """A dependency edge from contracts/service-contracts.yaml."""

    source_service: str
    target_service: str
    contract: str


RUNTIME_DEPENDENCY_GRAPH: tuple[RuntimeDependencyEdge, ...] = (
    RuntimeDependencyEdge("echoauth_runtime", "identity_service", "contracts/service-contracts.yaml"),
    RuntimeDependencyEdge("echoauth_runtime", "authority_service", "contracts/service-contracts.yaml"),
    RuntimeDependencyEdge("echoauth_runtime", "delegation_service", "contracts/service-contracts.yaml"),
    RuntimeDependencyEdge("echoauth_runtime", "policy_service", "contracts/service-contracts.yaml"),
    RuntimeDependencyEdge("echoauth_runtime", "refusal_service", "contracts/service-contracts.yaml"),
    RuntimeDependencyEdge("echoauth_runtime", "invariant_service", "contracts/service-contracts.yaml"),
    RuntimeDependencyEdge("echoauth_runtime", "escalation_service", "contracts/service-contracts.yaml"),
    RuntimeDependencyEdge("echoauth_runtime", "envelope_service", "contracts/service-contracts.yaml"),
    RuntimeDependencyEdge("echoauth_runtime", "token_service", "contracts/service-contracts.yaml"),
    RuntimeDependencyEdge("echoauth_runtime", "claim_service", "contracts/service-contracts.yaml"),
    RuntimeDependencyEdge("echoauth_runtime", "halt_service", "contracts/service-contracts.yaml"),
    RuntimeDependencyEdge("echoauth_runtime", "recovery_service", "contracts/service-contracts.yaml"),
    RuntimeDependencyEdge("echoauth_runtime", "emergency_override_service", "contracts/service-contracts.yaml"),
    RuntimeDependencyEdge("echoauth_runtime", "notification_service", "contracts/integration-contracts.yaml"),
    RuntimeDependencyEdge("echoauth_runtime", "audit_service", "contracts/service-contracts.yaml"),
    RuntimeDependencyEdge("audit_service", "event_bus", "events/event-catalog.yaml"),
    RuntimeDependencyEdge("notification_service", "event_bus", "events/event-catalog.yaml"),
)
