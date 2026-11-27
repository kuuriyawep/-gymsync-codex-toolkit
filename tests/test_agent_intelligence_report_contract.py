from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas" / "agent-result.schema.json").read_text(encoding="utf-8"))
TEMPLATE = (ROOT / "templates" / "agent-result.md").read_text(encoding="utf-8")
AGENT_NAMES = (
    "repo_explorer",
    "planner",
    "implementer",
    "reviewer",
    "security_auditor",
    "test_engineer",
)
SPEC = importlib.util.spec_from_file_location(
    "validate_agent_contracts", ROOT / "tools" / "validate_agent_contracts.py"
)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def legacy_handoff() -> dict:
    return {
        "handoff_id": "H-ws1-legacy",
        "recipient": "repo_explorer",
        "constraints": {"write_scope": []},
        "approval": {"status": "not-required"},
    }


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



def intelligence_result() -> dict:
    result = legacy_result()
    result.update(
        {
            "reasoning": {
                "problem_frame": "Determine whether the report contract is backward compatible.",
                "options_considered": ["Keep existing required fields", "Make all new fields mandatory"],
                "rationale": "Optional additions preserve existing producers while enabling richer reports.",
                "assumptions": ["Existing consumers tolerate additive optional fields."],
            },
            "self_critique": {
                "uncertainties": [],
                "missing_evidence": [],
                "counterexamples": ["A consumer may reject unknown fields outside this schema."],
                "failure_modes": [],
            },
            "tools_used": [
                {
                    "tool": "repository_reader",
                    "status": "invoked_succeeded",
                    "purpose": "Inspect the result schema and validator.",
                    "evidence_ref": "schemas/agent-result.schema.json",
                }
            ],
            "memory": {
                "sources_consulted": ["PROJECT_STATE.md"],
                "proposed_updates": [
                    {
                        "content": "The result schema supports optional intelligence sections.",
                        "provenance": "schemas/agent-result.schema.json",
                        "reason": "Help future sessions construct compatible reports.",
                    }
                ],
            },
            "collaboration": [
                {
                    "agent": "reviewer",
                    "purpose": "Independently inspect schema compatibility.",
                    "status": "not_needed",
                    "evidence_refs": [],
                }
            ],
            "initiative_proposals": [
                {
                    "proposal_type": "improvement",
                    "title": "Add runtime report validation",
                    "reason": "Static compatibility tests do not prove runtime agent behavior.",
                    "evidence_refs": ["tests/test_agent_intelligence_report_contract.py"],
                    "benefit": "Measure actual report compliance when Codex runtime is available.",
                    "risk": "Runtime evidence is currently unavailable.",
                    "effort": "medium",
                    "recommended_status": "defer",
                }
            ],
            "evaluation": {
                "criteria_assessed": [
                    {
                        "criterion": "Schema compatibility",
                        "status": "pass",
                        "evidence_refs": ["schemas/agent-result.schema.json"],
                        "rationale": "All supplied optional sections match the declared schema.",
                    }
                ],
                "overall_status": "pass",
                "limitations": ["This is a deterministic schema check, not behavioral evaluation."],
            },
        }
    )
    return result


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
        self.assertEqual(validator.validate_result(legacy_result(), legacy_handoff()), [])

    def test_complete_intelligence_result_passes_existing_contract_validator(self):
        self.assertEqual(
            validator.validate_result(intelligence_result(), legacy_handoff()),
            [],
        )

    def test_invalid_tool_invocation_status_is_rejected(self):
        result = intelligence_result()
        result["tools_used"][0]["status"] = "available_and_used"
        errors = validator.validate_result(result, legacy_handoff())
        self.assertTrue(any("tools_used" in error for error in errors), errors)

    def test_native_agent_definitions_reference_standard_once(self):
        for name in AGENT_NAMES:
            path = ROOT / ".codex" / "agents" / f"{name}.toml"
            source = path.read_text(encoding="utf-8")
            with self.subTest(agent=name):
                self.assertEqual(
                    source.count("docs/agent-intelligence-standard.md"),
                    1,
                    "Each native agent must reference the common standard once.",
                )

    def test_role_briefs_reference_common_standard(self):
        role_files = (
            "explore.md",
            "planner.md",
            "implementer.md",
            "reviewer.md",
            "security.md",
            "test_engineer.md",
        )
        for name in role_files:
            source = (ROOT / "agents" / name).read_text(encoding="utf-8")
            with self.subTest(role_brief=name):
                self.assertIn("Agent Intelligence Core", source)

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
