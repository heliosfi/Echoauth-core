"""Sprint 1 runtime configuration loader tests."""

from __future__ import annotations

import unittest

from echoauth.config import RuntimeConfig
from echoauth.config_loader import ConfigurationError, load_runtime_config, resolve_contract_paths


VALID_CONFIG = {
    "policy_version": "policy-v1",
    "invariant_version": "invariant-v1",
    "security_profile_id": "security-profile-v1",
    "audit_sink_id": "audit-sink-v1",
}


class ConfigLoaderTests(unittest.TestCase):
    def test_default_contract_paths_resolve(self) -> None:
        paths = resolve_contract_paths()

        self.assertIn("openapi", paths)
        self.assertTrue(paths["openapi"].is_file())
        self.assertTrue(paths["database_schema"].is_file())

    def test_runtime_config_loads_required_fields(self) -> None:
        config = load_runtime_config(VALID_CONFIG)

        self.assertIsInstance(config, RuntimeConfig)
        self.assertEqual(config.policy_version, "policy-v1")
        self.assertEqual(config.invariant_version, "invariant-v1")
        self.assertEqual(config.security_profile_id, "security-profile-v1")
        self.assertEqual(config.audit_sink_id, "audit-sink-v1")

    def test_missing_required_config_fails_deterministically(self) -> None:
        with self.assertRaises(ConfigurationError):
            load_runtime_config({"policy_version": "policy-v1"})


if __name__ == "__main__":
    unittest.main()
