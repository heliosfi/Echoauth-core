"""EchoAuth reference runtime skeleton.

Specification: specs/echoauth-spec.md
Contracts: api/openapi.yaml, contracts/service-contracts.yaml,
contracts/protobuf/echoauth.proto

This module intentionally contains no application logic. It defines the
top-level runtime boundary and dependency wiring shape only.
"""

from __future__ import annotations

from dataclasses import dataclass

from echoauth.interfaces import (
    AuditService,
    AuthorityService,
    DelegationService,
    EnvelopeService,
    EmergencyOverrideService,
    EscalationService,
    ExecutionClaimService,
    HaltService,
    IdentityService,
    InvariantService,
    NotificationService,
    PolicyService,
    RecoveryService,
    RefusalService,
    RuntimeService,
    TokenService,
)


@dataclass(frozen=True)
class EchoAuthRuntimeDependencies:
    """Service graph required by the EchoAuth runtime boundary.

    State machine: specs/echoauth-spec.md and specs/runtime-state-machine.md
    """

    identity_service: IdentityService
    authority_service: AuthorityService
    delegation_service: DelegationService
    policy_service: PolicyService
    refusal_service: RefusalService
    invariant_service: InvariantService
    escalation_service: EscalationService
    envelope_service: EnvelopeService
    token_service: TokenService
    claim_service: ExecutionClaimService
    halt_service: HaltService
    recovery_service: RecoveryService
    emergency_override_service: EmergencyOverrideService
    notification_service: NotificationService
    audit_service: AuditService


class EchoAuthRuntime(RuntimeService):
    """Abstract runtime boundary for EchoAuth request processing.

    Implementations must follow specs/echoauth-spec.md. This class does not
    implement request processing.
    """

    dependencies: EchoAuthRuntimeDependencies
