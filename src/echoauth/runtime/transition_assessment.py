"""Bounded upstream assessment surface for EchoAuth transition validation.

This module composes the existing validation-only RuntimeStateMachine. It does
not apply state, activate runtime capability, map RuntimeState to S-modes, or
create downstream execution authority.
"""

from __future__ import annotations

from echoauth.runtime.state_machine import RuntimeStateMachine
from echoauth.runtime.state_models import RuntimeTransitionDecision, RuntimeTransitionRequest


def assess_transition(
    machine: RuntimeStateMachine,
    request: RuntimeTransitionRequest,
) -> RuntimeTransitionDecision:
    """Return the canonical validation decision for one caller-supplied request.

    Audit, clock, evidence hashing, canonical request validation, transition-graph
    meaning, caching, and fail-closed behavior remain owned by
    ``RuntimeStateMachine.validate``. This adapter adds no S-mode interpretation
    and performs no state application or external action.
    """

    if not isinstance(machine, RuntimeStateMachine):
        raise TypeError("machine must be a RuntimeStateMachine")
    return machine.validate(request)
