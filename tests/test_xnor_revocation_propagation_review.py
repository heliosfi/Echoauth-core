"""Synthetic, review-only demonstration of EchoAuth revocation propagation gap.

This test DOES NOT implement a NODE XNOR adapter or assert real-key readiness.
It compares the existing direct authority resolver path with the ordinary gate
path using only synthetic in-memory records. It intentionally documents the
current non-propagation behavior; future fixes must replace this characterization
with fail-closed enforcement tests.
"""

from __future__ import annotations

import unittest
from dataclasses import replace

from echoauth.auth import AuthorizationOutcome
from echoauth.auth.authority import AuthorityResolutionOutcome
from echoauth.models import AuthorityResolutionRequest

from test_authorization_gate import AuthorizationGateTests


class _RecordingAuthorityResolver:
    def __init__(self, delegate):
        self.delegate = delegate
        self.requests = []

    def resolve(self, request):
        self.requests.append(request)
        return self.delegate.resolve(request)


class XnorRevocationPropagationReviewTests(unittest.TestCase):
    def test_synthetic_direct_resolver_revocation_is_not_forwarded_by_gate(self):
        fixture = AuthorizationGateTests(methodName="test_successful_authorization")
        fixture.setUp()
        fixture._register_policy()

        synthetic_revocation = {
            "revocation_id": "synthetic-revocation-1",
            "target_type": "authority",
            "target_id": "authority-1",
            "effective_at": "2026-06-19T12:30:00Z",
        }
        # The resolver can consume this record explicitly. It does not prove
        # any XNOR signature, checkpoint, or external source authentication.
        direct = fixture.authority_service.resolve(
            AuthorityResolutionRequest(
                request_id="synthetic-direct-revocation",
                subject_id="subject-1",
                requester_id="parent-1",
                action="read",
                resource="record-1",
                context={"location": "school"},
                identity_verdict_id="synthetic-identity",
                authority_records=(),
                policy_version="policy-v1",
                revocation_records=(synthetic_revocation,),
            )
        )
        self.assertEqual(direct.outcome, AuthorityResolutionOutcome.REVOKED)

        recorder = _RecordingAuthorityResolver(fixture.authority_service)
        fixture.gate._authority_service = recorder
        ordinary = fixture.gate.authorize(fixture._request(request_id="synthetic-gate-no-revocation"))
        self.assertEqual(len(recorder.requests), 1)
        self.assertEqual(tuple(recorder.requests[0].revocation_records), ())
        # Characterization of CURRENT behavior, NOT desired security behavior:
        # without a trusted revocation feed, the ordinary gate may authorize.
        self.assertEqual(ordinary.outcome, AuthorizationOutcome.AUTHORIZED)


if __name__ == "__main__":
    unittest.main()
