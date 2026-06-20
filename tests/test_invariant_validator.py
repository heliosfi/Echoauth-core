"""Sprint 2N deterministic Invariant Validator tests."""

from __future__ import annotations

import unittest
from datetime import datetime, timezone

import echoauth.auth  # Preserve the repository's established package initialization order.
from echoauth.audit import InMemoryAuditLogRepository
from echoauth.governance import (
    InvariantFailureState,
    InvariantResultState,
    InvariantRule,
    InvariantService,
    InvariantSet,
    InvariantValidationError,
    InvariantValidationRequest,
)


class InvariantValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.audit = InMemoryAuditLogRepository()
        self.active_set = InvariantSet(
            invariant_version="invariants-v1",
            active=True,
            rules=(
                InvariantRule(
                    invariant_id="authority_explicit",
                    fact_key="authority_explicit",
                    expected_value=True,
                    failure_state=InvariantFailureState.INVALID,
                ),
                InvariantRule(
                    invariant_id="payload_integrity",
                    fact_key="payload_integrity",
                    expected_value=True,
                    failure_state=InvariantFailureState.HALT,
                ),
                InvariantRule(
                    invariant_id="audit_path_available",
                    fact_key="audit_path_available",
                    expected_value=True,
                    failure_state=InvariantFailureState.HALT,
                ),
            ),
        )
        self.inactive_set = InvariantSet(
            invariant_version="invariants-retired",
            active=False,
            rules=(
                InvariantRule(
                    invariant_id="retired_rule",
                    fact_key="retired_rule",
                    expected_value=True,
                    failure_state=InvariantFailureState.INVALID,
                ),
            ),
        )
        self.service = InvariantService(
            self.audit,
            audit_chain_id="invariant-audit",
            invariant_sets=(self.active_set, self.inactive_set),
            clock=lambda: datetime(2026, 6, 19, 18, 0, tzinfo=timezone.utc),
        )

    def _request(
        self,
        facts,
        *,
        version: str = "invariants-v1",
        validation_id: str = "validation-1",
    ) -> InvariantValidationRequest:
        return InvariantValidationRequest(
            validation_id=validation_id,
            request_id="request-1",
            invariant_version=version,
            runtime_state="validating_invariants",
            facts=facts,
            envelope_id=None,
        )

    def test_valid_invariant_result(self) -> None:
        result = self.service.validate(
            self._request(
                {
                    "authority_explicit": True,
                    "payload_integrity": True,
                    "audit_path_available": True,
                }
            )
        )
        self.assertEqual(result.state, InvariantResultState.VALID)
        self.assertEqual(result.failed_invariants, ())
        self.assertIsNotNone(result.definition_hash)

    def test_unknown_invariant_version_holds(self) -> None:
        result = self.service.validate(
            self._request({}, version="unknown-invariants")
        )
        self.assertEqual(result.state, InvariantResultState.HOLD)
        self.assertEqual(result.reason, "invariant_version_unknown")
        self.assertIsNone(result.definition_hash)

    def test_inactive_invariant_version_holds(self) -> None:
        result = self.service.validate(
            self._request({}, version="invariants-retired")
        )
        self.assertEqual(result.state, InvariantResultState.HOLD)
        self.assertEqual(result.reason, "invariant_version_inactive")

    def test_missing_required_fact_holds(self) -> None:
        result = self.service.validate(
            self._request(
                {
                    "authority_explicit": True,
                    "payload_integrity": True,
                }
            )
        )
        self.assertEqual(result.state, InvariantResultState.HOLD)
        self.assertEqual(result.failed_invariants, ("audit_path_available",))

    def test_noncritical_failure_is_invalid(self) -> None:
        result = self.service.validate(
            self._request(
                {
                    "authority_explicit": False,
                    "payload_integrity": True,
                    "audit_path_available": True,
                }
            )
        )
        self.assertEqual(result.state, InvariantResultState.INVALID)
        self.assertEqual(result.failed_invariants, ("authority_explicit",))

    def test_critical_failure_halts(self) -> None:
        result = self.service.validate(
            self._request(
                {
                    "authority_explicit": True,
                    "payload_integrity": False,
                    "audit_path_available": True,
                }
            )
        )
        self.assertEqual(result.state, InvariantResultState.HALT)
        self.assertEqual(result.failed_invariants, ("payload_integrity",))

    def test_critical_failure_precedes_invalid_and_missing(self) -> None:
        result = self.service.validate(
            self._request(
                {
                    "authority_explicit": False,
                    "payload_integrity": False,
                }
            )
        )
        self.assertEqual(result.state, InvariantResultState.HALT)
        self.assertEqual(
            result.failed_invariants,
            (
                "authority_explicit",
                "payload_integrity",
                "audit_path_available",
            ),
        )

    def test_evaluation_order_is_stable(self) -> None:
        result = self.service.validate(
            self._request(
                {
                    "authority_explicit": False,
                    "payload_integrity": False,
                    "audit_path_available": False,
                }
            )
        )
        self.assertEqual(
            result.evaluation_order,
            (
                "authority_explicit",
                "payload_integrity",
                "audit_path_available",
            ),
        )
        self.assertEqual(result.failed_invariants, result.evaluation_order)

    def test_facts_hash_is_stable_for_equivalent_objects(self) -> None:
        first = self.service.validate(
            self._request(
                {
                    "authority_explicit": True,
                    "payload_integrity": True,
                    "audit_path_available": True,
                },
                validation_id="stable-1",
            )
        )
        second = self.service.validate(
            self._request(
                {
                    "audit_path_available": True,
                    "payload_integrity": True,
                    "authority_explicit": True,
                },
                validation_id="stable-2",
            )
        )
        self.assertEqual(first.facts_hash, second.facts_hash)

    def test_configured_definitions_are_detached_from_input(self) -> None:
        expected = {"mode": "safe"}
        invariant_set = InvariantSet(
            invariant_version="detached-v1",
            active=True,
            rules=(
                InvariantRule(
                    invariant_id="mode_safe",
                    fact_key="mode",
                    expected_value=expected,
                    failure_state=InvariantFailureState.HALT,
                ),
            ),
        )
        service = InvariantService(
            self.audit,
            audit_chain_id="detached-audit",
            invariant_sets=(invariant_set,),
        )
        expected["mode"] = "unsafe"

        result = service.validate(
            InvariantValidationRequest(
                validation_id="detached-validation",
                request_id="request-detached",
                invariant_version="detached-v1",
                runtime_state="validating_invariants",
                facts={"mode": {"mode": "safe"}},
            )
        )
        self.assertEqual(result.state, InvariantResultState.VALID)

    def test_duplicate_rule_ids_are_rejected(self) -> None:
        duplicate = InvariantSet(
            invariant_version="duplicate-v1",
            active=True,
            rules=(
                InvariantRule(
                    "same",
                    "first",
                    True,
                    InvariantFailureState.INVALID,
                ),
                InvariantRule(
                    "same",
                    "second",
                    True,
                    InvariantFailureState.HALT,
                ),
            ),
        )
        with self.assertRaises(InvariantValidationError):
            InvariantService(
                self.audit,
                audit_chain_id="duplicate-audit",
                invariant_sets=(duplicate,),
            )

    def test_result_is_audited_and_idempotent(self) -> None:
        request = self._request(
            {
                "authority_explicit": True,
                "payload_integrity": True,
                "audit_path_available": True,
            }
        )
        first = self.service.validate(request)
        audit_count = len(self.audit.chain("invariant-audit"))
        second = self.service.validate(request)
        event = self.audit.chain("invariant-audit")[-1]

        self.assertEqual(first, second)
        self.assertEqual(len(self.audit.chain("invariant-audit")), audit_count)
        self.assertEqual(event.record["event_type"], "invariant.result")
        self.assertEqual(event.record["details"]["facts_hash"], first.facts_hash)


if __name__ == "__main__":
    unittest.main()
