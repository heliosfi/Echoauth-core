"""Review-only composition of test-only Ed25519 verification and synthetic lineage.

No trusted source, key enrollment, transparency proof, runtime gate or authority.
"""
from dataclasses import dataclass
from enum import Enum
from review_candidates.xnor_ed25519_test_vector_verifier import (
    Verdict, verify_test_envelope,
)
from review_candidates.xnor_checkpoint_lineage_synthetic import (
    Checkpoint, LineageState, check_lineage,
)


class CombinedState(str, Enum):
    CONSISTENT_FOR_TEST = "CONSISTENT_FOR_TEST"
    HOLD = "HOLD"


@dataclass(frozen=True)
class CombinedResult:
    state: CombinedState
    reason: str
    authority_granted: bool = False
    execution_authorized: bool = False


def verify_composed_fixture(envelope, previous, candidate, *,
                            expected_authority, expected_target, expected_mapping,
                            expected_source, now, max_age, min_checkpoint):
    def hold(reason):
        return CombinedResult(CombinedState.HOLD, reason)
    sig = verify_test_envelope(
        envelope, expected_authority=expected_authority,
        expected_target=expected_target, expected_mapping=expected_mapping,
        now=now, min_checkpoint=min_checkpoint,
    )
    if sig.verdict is not Verdict.VERIFIED_FOR_TEST:
        return hold("signature_or_binding_" + sig.reason)
    if not isinstance(candidate, Checkpoint):
        return hold("missing_lineage_checkpoint")
    lineage = check_lineage(previous, candidate, expected_source=expected_source,
                            now=now, max_age=max_age)
    if lineage.state is not LineageState.CONSISTENT_FOR_TEST:
        return hold("lineage_" + lineage.reason)
    # Cross-bind signed payload's checkpoint fields to the lineage fixture.
    # The test verifier already checked signature over the exact payload bytes.
    import json
    try:
        payload = json.loads(envelope["payload"].decode("utf-8"))
    except (KeyError, TypeError, UnicodeError, ValueError):
        return hold("unreadable_signed_payload")
    if (payload.get("checkpoint_sequence") != candidate.sequence
            or payload.get("checkpoint_digest") != candidate.digest
            or payload.get("checkpoint_source") != candidate.source_id
            or payload.get("checkpoint_epoch") != candidate.epoch):
        return hold("signed_lineage_binding_mismatch")
    return CombinedResult(CombinedState.CONSISTENT_FOR_TEST,
                          "test_signature_and_synthetic_lineage_consistent")
