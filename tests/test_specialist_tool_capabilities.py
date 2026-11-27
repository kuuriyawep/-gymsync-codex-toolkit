from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas" / "specialist-tool-capability.schema.json").read_text(encoding="utf-8"))
MATRIX = (ROOT / "docs" / "specialist-tool-capability-matrix.md").read_text(encoding="utf-8")
AGENTS = {"repo_explorer", "planner", "implementer", "reviewer", "security_auditor", "test_engineer"}


class SpecialistToolCapabilityTests(unittest.TestCase):
    def test_schema_is_closed_and_has_required_contract_fields(self):
        self.assertEqual(SCHEMA["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertFalse(SCHEMA["additionalProperties"])
        self.assertTrue(set(SCHEMA["required"]).issubset(SCHEMA["properties"]))

    def test_owners_are_limited_to_existing_roles(self):
        owners = SCHEMA["properties"]["primary_owner"]["enum"]
        self.assertEqual(set(owners), AGENTS)
        self.assertEqual(set(SCHEMA["properties"]["supporting_roles"]["items"]["enum"]), AGENTS)

    def test_operations_require_scope_risk_effect_and_approval(self):
        operation = SCHEMA["properties"]["operations"]["items"]
        self.assertTrue({"operation_id", "effect", "risk", "approval", "resource_scope", "idempotent", "input_schema", "output_schema"}.issubset(operation["required"]))

    def test_high_risk_operations_require_approval(self):
        rules = SCHEMA["allOf"]
        r4 = next(rule for rule in rules if rule["if"]["properties"].get("risk", {}).get("const") == "R4")
        r3 = next(rule for rule in rules if rule["if"]["properties"].get("risk", {}).get("const") == "R3")
        self.assertEqual(r4["then"]["properties"]["approval"]["const"], "user")
        self.assertEqual(set(r3["then"]["properties"]["approval"]["enum"]), {"codex", "user"})

    def test_availability_cannot_be_claimed_without_matching_evidence_status(self):
        rules = SCHEMA["allOf"]
        verified = next(rule for rule in rules if rule["if"]["properties"]["availability"].get("const") == "verified")
        blocked = next(rule for rule in rules if "blocked" in rule["if"]["properties"]["availability"].get("enum", []))
        self.assertEqual(verified["then"]["properties"]["verification"]["properties"]["status"]["const"], "verified")
        self.assertIn("not_run", blocked["then"]["properties"]["verification"]["properties"]["status"]["enum"])

    def test_matrix_maps_all_required_specialist_capabilities(self):
        for capability in ("frontend.browser-automation", "backend.scenario-testing", "qa.automation", "security.monitoring", "research.source-analysis"):
            with self.subTest(capability=capability):
                self.assertIn(capability, MATRIX)

    def test_matrix_preserves_codex_and_user_authority(self):
        for phrase in ("Codex remains the coordinator", "user retains final authority", "deny by default", "fail closed"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, MATRIX)

    def test_declared_tools_are_not_misrepresented_as_runtime_verified(self):
        self.assertIn("planned", MATRIX)
        self.assertIn("not installed/runtime-verified", MATRIX)
        self.assertIn("NOT_RUN / BLOCKED", MATRIX)

    def test_risk_profiles_cover_all_five_levels(self):
        for level in ("R0", "R1", "R2", "R3", "R4"):
            with self.subTest(level=level):
                self.assertIn(level, MATRIX)


if __name__ == "__main__":
    unittest.main()
