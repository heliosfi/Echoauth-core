"""Authorization state interface exports.

Specification: specs/authorization-states.md
Contract: contracts/service-contracts.yaml#echoauth_runtime
State machine: specs/runtime-state-machine.md
"""

from echoauth.interfaces import RuntimeService
from echoauth.models import EchoAuthRequest, EchoAuthResult, RuntimeState
from echoauth.auth.authorization_gate import (
    AuthorizationDecision,
    AuthorizationGateAuditError,
    AuthorizationGateService,
    AuthorizationGateValidationError,
    AuthorizationOutcome,
    AuthorizationRequest,
    validate_authorization_request,
)

__all__ = [
    "AuthorizationDecision",
    "AuthorizationGateAuditError",
    "AuthorizationGateService",
    "AuthorizationGateValidationError",
    "AuthorizationOutcome",
    "AuthorizationRequest",
    "EchoAuthRequest",
    "EchoAuthResult",
    "RuntimeService",
    "RuntimeState",
    "validate_authorization_request",
]
