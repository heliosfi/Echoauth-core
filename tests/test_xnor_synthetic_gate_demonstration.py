"""Review-only synthetic gate demonstration; no production gate changes.

An injected test-only authority resolver forwards a fixed synthetic revocation
record to the existing EchoAuth resolver. This is NOT an authenticated XNOR
adapter and does NOT demonstrate real source trust or mapping.
"""
from dataclasses import replace
import unittest

from echoauth.auth import AuthorizationOutcome
from test_authorization_gate import AuthorizationGateTests


class _SyntheticRevocationForwarder:
    def __init__(self, delegate, records):
        self.delegate = delegate
        self.records = tuple(records)
        self.calls = []

    def resolve(self, request):
        forwarded = replace(request, revocation_records=self.records)
        self.calls.append(forwarded)
        return self.delegate.resolve(forwarded)


class XnorSyntheticGateDemonstrationTests(unittest.TestCase):
    def setUp(self):
        self.fixture = AuthorizationGateTests(methodName="test_successful_authorization")
        self.fixture.setUp()
        self.fixture._register_policy()
        self.revocation = {
            "revocation_id": "synthetic-xnor-revocation-1",
            "target_type": "authority",
            "target_id": "authority-1",
            "effective_at": "2026-06-19T12:30:00Z",
        }

    def test_matching_effective_revocation_blocks_authorization(self):
        forwarder = _SyntheticRevocationForwarder(
            self.fixture.authority_service, [self.revocation]
        )
        self.fixture.gate._authority_service = forwarder
        decision = self.fixture.gate.authorize(
            self.fixture._request(request_id="synthetic-revoked")
        )
        self.assertEqual(len(forwarder.calls), 1)
        self.assertEqual(forwarder.calls[0].revocation_records, (self.revocation,))
        self.assertEqual(decision.outcome, AuthorizationOutcome.REVOKED)

    def test_delegated_grantor_revocation_blocks_authorization(self):
        self.fixture._create_delegation()
        forwarder = _SyntheticRevocationForwarder(
            self.fixture.authority_service, [self.revocation]
        )
        self.fixture.gate._authority_service = forwarder
        decision = self.fixture.gate.authorize(
            self.fixture._request(
                request_id="synthetic-delegated-revoked",
                requester_id="teacher-1",
                delegation_id="delegation-1",
            )
        )
        self.assertEqual(decision.outcome, AuthorizationOutcome.REVOKED)

    def test_existing_gate_without_forwarder_is_not_protected_by_external_record(self):
        # Deliberately characterizes the known gap, NOT desired behavior.
        decision = self.fixture.gate.authorize(
            self.fixture._request(request_id="synthetic-no-feed")
        )
        self.assertEqual(decision.outcome, AuthorizationOutcome.AUTHORIZED)


if __name__ == "__main__":
    unittest.main()
