"""Conformance checks for the intentionally fail-closed demonstration."""
import unittest
from echoauth_demo import evaluate

class DemoTests(unittest.TestCase):
    def test_health_never_claims_runtime(self):
        status, body = evaluate("/api/health", "GET")
        self.assertEqual(status, 200)
        self.assertEqual(body["runtime"], "unavailable")
        self.assertFalse(body["authorization_enabled"])

    def test_authorize_always_holds(self):
        status, body = evaluate("/api/v1/authorize", "POST")
        self.assertEqual(status, 503)
        self.assertEqual(body["decision"], "HOLD")
        self.assertFalse(body["authorized"])

    def test_unknown_route(self):
        self.assertEqual(evaluate("/missing", "GET")[0], 404)

    def test_no_get_authorization(self):
        self.assertEqual(evaluate("/api/v1/authorize", "GET")[0], 404)

if __name__ == "__main__":
    unittest.main()
