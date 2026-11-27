from __future__ import annotations

import json
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"


def load_schema(name: str) -> dict:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


class AutonomousRuntimeContractTests(unittest.TestCase):
    def test_runtime_schemas_are_draft_2020_12_object_contracts(self):
        for name in ("runtime-event-envelope.schema.json", "runtime-task-lease.schema.json"):
            with self.subTest(schema=name):
                schema = load_schema(name)
                self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
                self.assertEqual(schema["type"], "object")
                self.assertFalse(schema["additionalProperties"])
                self.assertTrue(set(schema["required"]).issubset(schema["properties"]))

    def test_event_envelope_requires_identity_deduplication_and_expiry(self):
        schema = load_schema("runtime-event-envelope.schema.json")
        required = set(schema["required"])
        self.assertTrue({"event_id", "source_id", "issued_at", "expires_at",
                         "idempotency_key", "correlation_id", "subscription_id",
                         "target", "payload"}.issubset(required))
        self.assertEqual(schema["properties"]["schema_version"]["const"], "1.0.0")

    def test_event_target_is_bounded_to_workflow_task_or_intake(self):
        schema = load_schema("runtime-event-envelope.schema.json")
        target = schema["properties"]["target"]
        self.assertEqual(target["properties"]["kind"]["enum"], ["workflow", "task", "intake"])
        self.assertFalse(target["additionalProperties"])

    def test_lease_requires_fencing_token_worker_and_attempt(self):
        schema = load_schema("runtime-task-lease.schema.json")
        required = set(schema["required"])
        self.assertTrue({"lease_id", "workflow_id", "task_id", "worker_id",
                         "fencing_token", "attempt", "issued_at", "expires_at",
                         "heartbeat_at", "status"}.issubset(required))
        self.assertEqual(schema["properties"]["fencing_token"]["minimum"], 1)
        self.assertEqual(schema["properties"]["attempt"]["minimum"], 1)

    def test_lease_states_include_revocation_and_expiry(self):
        schema = load_schema("runtime-task-lease.schema.json")
        self.assertEqual(schema["properties"]["status"]["enum"],
                         ["active", "released", "expired", "revoked"])

    def test_runtime_contract_does_not_claim_live_execution(self):
        contract = (ROOT / "docs" / "autonomous-runtime-contract.md").read_text(encoding="utf-8")
        self.assertIn("no live runtime is implemented or claimed", contract)
        self.assertIn("Codex remains the sole workflow coordinator", contract)
        self.assertIn("Non-idempotent work", contract)
        self.assertIn("NOT_RUN / BLOCKED", contract)


if __name__ == "__main__":
    unittest.main()
