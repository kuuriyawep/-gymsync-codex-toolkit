from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import validate_toolkit  # noqa: E402


class SkillCaseCoverageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rubric = {
            "coverage_requirements": {
                "target_skill": "skill-authoring-and-evaluation",
                "minimums": {"in-scope": 3, "near-miss": 2, "edge": 1},
            }
        }

    def case(self, case_id: str, coverage: str | None) -> dict:
        data = {"id": case_id, "target": ["skill-authoring-and-evaluation"]}
        if coverage is not None:
            data["coverage"] = coverage
        return {"path": Path(f"evals/cases/{case_id}.json"), "data": data}

    def test_complete_coverage_passes(self) -> None:
        cases = [
            self.case("in-1", "in-scope"), self.case("in-2", "in-scope"),
            self.case("in-3", "in-scope"), self.case("near-1", "near-miss"),
            self.case("near-2", "near-miss"), self.case("edge-1", "edge"),
        ]
        self.assertEqual(validate_toolkit.validate_skill_case_coverage(cases, self.rubric), [])

    def test_missing_coverage_is_reported(self) -> None:
        cases = [self.case("in-1", "in-scope"), self.case("unlabelled", None)]
        errors = validate_toolkit.validate_skill_case_coverage(cases, self.rubric)
        self.assertTrue(any("missing valid coverage label" in error for error in errors))
        self.assertTrue(any("in-scope coverage requires at least 3" in error for error in errors))

    def test_other_skill_cases_do_not_count(self) -> None:
        cases = [{"path": Path("evals/cases/other.json"), "data": {
            "id": "other", "target": ["different-skill"], "coverage": "in-scope"}}]
        errors = validate_toolkit.validate_skill_case_coverage(cases, self.rubric)
        self.assertEqual(len(errors), 3)

    def test_unknown_coverage_label_does_not_count(self) -> None:
        cases = [self.case("bad", "misc")]
        errors = validate_toolkit.validate_skill_case_coverage(cases, self.rubric)
        self.assertTrue(any("missing valid coverage label" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
