from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas" / "agent-result.schema.json").read_text(encoding="utf-8"))
TEMPLATE = (ROOT / "templates" / "agent-result.md").read_text(encoding="utf-8")
SPEC = importlib.util.spec_from_file_location(
    "validate_agent_contracts", ROOT / "tools" / "validate_agent_contracts.py"
)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def legacy_result() -> dict:
    return {
        "schema_version": "1.0.0",
        "handoff_id": "H-ws1-legacy",
        "agent": "repo_explorer",
        "outcome": "complete",
        "summary": "Legacy result remains valid after additive schema evolution.",
        "work_performed": [],
        "findings": [],
        "changed_files": [],
        "checks": [{"name": "Static contract check", "status": "passed", "evidence_refs": ["tests/"]}],
        "risks": [],
        "next_action": "Parent coordinator reviews the result.",
        "approval_needed": False,
    }


class AgentIntelligenceReportContractTests(unittest.TestCase):
    def test_nine_capability_report_fields_are_declared(self):
        properties = SCHEMA["properties"]
        for field in (
            "reasoning",
            "self_critique",
            "tools_used",
            "memory",
            "collaboration",
            "initiative_proposals",
            "evaluation",
        ):
            with self.subTest(field=field):
                self.assertIn(field, properties)

    def test_intelligence_fields_are_additive_not_required(self):
        required = set(SCHEMA["required"])
        for field in (
            "reasoning",
            "self_critique",
            "tools_used",
            "memory",
            "collaboration",
            "initiative_proposals",
            "evaluation",
        ):
            with self.subTest(field=field):
                self.assertNotIn(field, required)

    def test_legacy_result_still_passes_existing_contract_validator(self):
        self.assertEqual(validator.validate_result(legacy_result()), [])

    def test_template_explains_evidence_and_governance_for_new_fields(self):
        for heading in (
            "## Reasoning",
            "## Self-critique",
            "## Tools actually used",
            "## Memory",
            "## Collaboration",
            "## Initiative proposals",
            "## Evaluation",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, TEMPLATE)
        self.assertIn("proposal is not authorization", TEMPLATE)
        self.assertIn("Do not silently write or overwrite canonical shared memory.", TEMPLATE)


if __name__ == "__main__":
    unittest.main()
