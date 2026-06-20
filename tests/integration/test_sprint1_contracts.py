"""Sprint 1 contract integration tests."""

from __future__ import annotations

import unittest

from echoauth.config_loader import load_runtime_config, resolve_contract_paths
from echoauth.contracts.validation import validate_contracts


VALID_CONFIG = {
    "policy_version": "policy-v1",
    "invariant_version": "invariant-v1",
    "security_profile_id": "security-profile-v1",
    "audit_sink_id": "audit-sink-v1",
}


class Sprint1ContractIntegrationTests(unittest.TestCase):
    def test_config_paths_feed_contract_validation(self) -> None:
        config = load_runtime_config(VALID_CONFIG)
        paths = resolve_contract_paths(config.contract_paths)
        report = validate_contracts()

        self.assertTrue(paths["openapi"].is_file())
        self.assertTrue(paths["database_schema"].is_file())
        self.assertTrue(report.passed, report.failures())


if __name__ == "__main__":
    unittest.main()
