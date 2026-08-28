import unittest
from dataclasses import replace

from echoauth.canonical import canonical_sha256
from echoauth.sai.binding import _record_document
from echoauth.sai import (
    ACCEPTED_OUTCOME, WAIT_POSTURE, SaiIntakeEvidence, SaiReason, validate_sai_intake,
)
from tests.test_sai_binding import configuration, form, request


def evidence(**changes):
    values = dict(evaluated_at="2026-08-28T10:30:00Z", currentness_verified=True,
                  revoked=False, superseded=False, replayed_nonces=(), audit_available=True)
    values.update(changes)
    return SaiIntakeEvidence(**values)


def rehash(record, **changes):
    changed = replace(record, **changes, binding_record_hash="")
    return replace(changed, binding_record_hash=canonical_sha256(
        _record_document(changed, include_hash=False)))


class SaiIntakeTests(unittest.TestCase):
    def assert_reason(self, reason, *, record=None, bound_request=None, intake_evidence=None, config=None):
        result = validate_sai_intake(record or form(), bound_request or request(),
                                     intake_evidence or evidence(), config or configuration())
        self.assertFalse(result.accepted)
        self.assertEqual(result.reason, reason)
        self.assertEqual(result.continuation_posture, WAIT_POSTURE)

    def test_valid_intake_is_inert_and_waits_for_separate_authorization(self):
        result = validate_sai_intake(form(), request(), evidence(), configuration())
        self.assertTrue(result.accepted)
        self.assertEqual(result.outcome, ACCEPTED_OUTCOME)
        self.assertEqual(result.reason, SaiReason.ACCEPTED)
        self.assertEqual(result.continuation_posture, WAIT_POSTURE)

    def test_contract_integrity_and_upstream_substitution_fail(self):
        self.assert_reason(SaiReason.CONTRACT_INVALID, record=replace(form(), contract_version="2.0.0"))
        self.assert_reason(SaiReason.UPSTREAM_BINDING_INVALID, record=replace(form(), upstream_checkpoint="other"))
        self.assert_reason(SaiReason.UPSTREAM_BINDING_INVALID, record=replace(form(), binding_record_hash="0" * 64))

    def test_request_action_resource_and_correlation_substitution_fail(self):
        cases = [
            (request(request_id="other"), SaiReason.REQUEST_BINDING_INVALID),
            (request(correlation_id="other"), SaiReason.CORRELATION_MISMATCH),
            (request(action="write"), SaiReason.ACTION_MISMATCH),
            (request(resource="other"), SaiReason.RESOURCE_MISMATCH),
        ]
        for changed, reason in cases:
            with self.subTest(reason=reason):
                self.assert_reason(reason, bound_request=changed)

    def test_payload_context_policy_and_request_hash_substitution_fail(self):
        cases = [
            (request(payload={"field": "changed"}), SaiReason.PAYLOAD_HASH_MISMATCH),
            (request(context={"channel": "changed"}), SaiReason.CONTEXT_HASH_MISMATCH),
            (request(policy_version="policy-2"), SaiReason.POLICY_VERSION_MISMATCH),
            (request(idempotency_key="other"), SaiReason.REQUEST_BINDING_INVALID),
        ]
        for changed, reason in cases:
            with self.subTest(reason=reason):
                self.assert_reason(reason, bound_request=changed)
        self.assert_reason(SaiReason.PAYLOAD_HASH_MISMATCH,
                           record=rehash(form(), payload_hash="0" * 64))

    def test_currentness_revocation_supersession_replay_and_time_fail(self):
        cases = [
            (evidence(currentness_verified=False), SaiReason.CURRENTNESS_UNVERIFIABLE),
            (evidence(revoked=True), SaiReason.REVOKED),
            (evidence(superseded=True), SaiReason.SUPERSEDED),
            (evidence(replayed_nonces=("nonce-1",)), SaiReason.REPLAYED),
            (evidence(evaluated_at="2026-08-28T09:00:00Z"), SaiReason.NOT_YET_EFFECTIVE),
            (evidence(evaluated_at="2026-08-28T11:00:00Z"), SaiReason.EXPIRED),
        ]
        for changed, reason in cases:
            with self.subTest(reason=reason):
                self.assert_reason(reason, intake_evidence=changed)

    def test_audit_evidence_vocabulary_and_hawk_exclusions_fail(self):
        self.assert_reason(SaiReason.AUDIT_INVALID, intake_evidence=evidence(audit_available=False))
        self.assert_reason(SaiReason.STATE_VOCABULARY_UNKNOWN,
                           config=configuration(accepted_state_vocabularies=()))
        self.assert_reason(SaiReason.HAWK_AUTHORITY_EXCLUSION_INVALID,
                           record=rehash(form(), hawk_authority_excluded=("EXECUTION",)))

    def test_module_has_no_authorization_execution_or_external_dependency(self):
        import ast, inspect
        import echoauth.sai.binding as binding
        import echoauth.sai.intake as intake
        forbidden = {"authorize", "execute", "dispatch", "requests", "socket", "subprocess"}
        trees = [ast.parse(inspect.getsource(module)) for module in (binding, intake)]
        names = {node.id for tree in trees for node in ast.walk(tree) if isinstance(node, ast.Name)}
        names.update(node.attr for tree in trees for node in ast.walk(tree)
                     if isinstance(node, ast.Attribute))
        self.assertTrue(forbidden.isdisjoint(names))
