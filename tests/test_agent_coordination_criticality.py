from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import validate_toolkit  # noqa: E402


# Independent test oracle: do not derive expected values from the production
# constant being validated, or a regression in that constant becomes invisible.
EXPECTED_PHASE6_CRITICAL_BEHAVIORS = {
    "agent-selection-and-scope": {"must-not-02"},
    "handoff-approval-inheritance": {"must-not-01", "must-not-02"},
    "parallel-write-boundaries": {"must-not-01", "must-not-02"},
    "independent-review-findings": {"must-not-01"},
    "agent-conflict-evidence-resolution": {"must-not-01", "must-not-02"},
    "agent-failure-recovery": {"must-not-01", "must-not-02"},
    "agent-output-verification-honesty": {"must-not-01", "must-not-02"},
}


class AgentCoordinationCriticalityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cases = []
        for case_id, critical in EXPECTED_PHASE6_CRITICAL_BEHAVIORS.items():
            self.cases.append({
                "path": Path(f"evals/cases/{case_id}.json"),
                "data": {
                    "id": case_id,
                    "tags": ["phase-6"],
                    "critical_behaviors": sorted(critical),
                },
            })

    def test_phase6_criticality_contract_passes(self) -> None:
        self.assertEqual(
            validate_toolkit.validate_agent_critical_behavior_contract(self.cases),
            [],
        )

    def test_missing_critical_behavior_is_rejected(self) -> None:
        self.cases[0]["data"]["critical_behaviors"] = []
        errors = validate_toolkit.validate_agent_critical_behavior_contract(self.cases)
        self.assertTrue(any("critical_behaviors must be" in error for error in errors))

    def test_missing_phase6_case_is_rejected(self) -> None:
        self.cases.pop()
        errors = validate_toolkit.validate_agent_critical_behavior_contract(self.cases)
        self.assertTrue(any("required case is missing" in error for error in errors))

    def test_unexpected_phase6_case_is_rejected(self) -> None:
        self.cases.append({
            "path": Path("evals/cases/unexpected.json"),
            "data": {
                "id": "unexpected",
                "tags": ["phase-6"],
                "critical_behaviors": [],
            },
        })
        errors = validate_toolkit.validate_agent_critical_behavior_contract(self.cases)
        self.assertTrue(any("unexpected phase-6 case" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
