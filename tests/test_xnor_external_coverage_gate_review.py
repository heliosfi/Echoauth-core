"""Review-only external revocation coverage injection into the real EchoAuth gate.

A test double stands in for a future authenticated provider. No real trust,
cryptography, checkpoint validation, or production integration is implied.
"""
from test_authorization_gate import AuthorizationGateTests
from echoauth.auth import AuthorizationOutcome
from echoauth.auth.authority_resolution import AuthorityResolutionOutcome
from unittest.mock import patch


class _SyntheticCoverageService:
    def __init__(self, delegate, coverage):
        self.delegate = delegate
        self.coverage = coverage
        self.calls = 0

    def resolve(self, request):
        self.calls += 1
        if self.coverage == "OUTAGE":
            raise RuntimeError("synthetic external provider outage")
        if self.coverage in ("HOLD", "REVOKED"):
            # Review double deliberately fails closed before the gate can
            # evaluate a potentially cached positive result.
            raise RuntimeError("synthetic coverage not clear: " + self.coverage)
        if self.coverage != "CLEAR_FOR_TEST":
            raise RuntimeError("unknown synthetic coverage")
        return self.delegate.resolve(request)


class ExternalRevocationCoverageGateTests(AuthorizationGateTests):
    def _wrap(self, coverage):
        wrapped = _SyntheticCoverageService(self.authority_service, coverage)
        self.gate._authority_service = wrapped
        return wrapped

    def test_clear_coverage_still_requires_independent_gate_policy(self):
        self._register_policy()
        wrapper = self._wrap("CLEAR_FOR_TEST")
        decision = self.gate.authorize(self._request())
        self.assertEqual(decision.outcome, AuthorizationOutcome.AUTHORIZED)
        self.assertEqual(wrapper.calls, 1)

    def test_external_revoked_blocks_even_with_cached_positive(self):
        self._register_policy()
        wrapper = self._wrap("CLEAR_FOR_TEST")
        request = self._request()
        self.assertEqual(self.gate.authorize(request).outcome, AuthorizationOutcome.AUTHORIZED)
        wrapper.coverage = "REVOKED"
        second = self.gate.authorize(request)
        self.assertNotEqual(second.outcome, AuthorizationOutcome.AUTHORIZED)
        self.assertEqual(second.outcome, AuthorizationOutcome.INVALID_AUTHORITY)
        self.assertEqual(wrapper.calls, 2)

    def test_external_hold_blocks_even_with_cached_positive(self):
        self._register_policy()
        wrapper = self._wrap("CLEAR_FOR_TEST")
        request = self._request()
        self.assertEqual(self.gate.authorize(request).outcome, AuthorizationOutcome.AUTHORIZED)
        wrapper.coverage = "HOLD"
        self.assertEqual(self.gate.authorize(request).outcome, AuthorizationOutcome.INVALID_AUTHORITY)
        self.assertEqual(wrapper.calls, 2)

    def test_provider_outage_blocks_even_with_cached_positive(self):
        self._register_policy()
        wrapper = self._wrap("CLEAR_FOR_TEST")
        request = self._request()
        self.assertEqual(self.gate.authorize(request).outcome, AuthorizationOutcome.AUTHORIZED)
        wrapper.coverage = "OUTAGE"
        self.assertEqual(self.gate.authorize(request).outcome, AuthorizationOutcome.INVALID_AUTHORITY)
        self.assertEqual(wrapper.calls, 2)

    def test_clear_coverage_cannot_override_policy_denial(self):
        from echoauth.policy import PolicyEffect
        self._register_policy(effect=PolicyEffect.DENY)
        self._wrap("CLEAR_FOR_TEST")
        self.assertEqual(self.gate.authorize(self._request()).outcome, AuthorizationOutcome.DENIED)

    def test_missing_coverage_blocks(self):
        self._register_policy()
        self._wrap("MISSING")
        self.assertEqual(self.gate.authorize(self._request()).outcome, AuthorizationOutcome.INVALID_AUTHORITY)

    def test_coverage_is_not_attested_or_bound_to_actual_authority(self):
        # This test documents an intentional limitation: the double has no
        # authority-id, target digest, signed checkpoint or freshness binding.
        wrapper = self._wrap("CLEAR_FOR_TEST")
        self.assertFalse(hasattr(wrapper, "trusted_checkpoint_digest"))
        self.assertFalse(hasattr(wrapper, "authority_binding_digest"))
        self.assertFalse(hasattr(wrapper, "signature_verified"))
