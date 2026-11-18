from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_skill_scores", ROOT / "tools" / "validate_skill_scores.py")
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class SkillScoreTests(unittest.TestCase):
    def valid_scorecard(self):
        return {
            "schema_version": "1.0.0",
            "skill_id": "change-impact-analysis",
            "skill_path": ".agents/skills/change-impact-analysis/SKILL.md",
            "target_revision": "a" * 40,
            "reviewer": "Codex static review (model-assisted)",
            "reviewed_at": "2026-11-18T12:15:00Z",
            "review_type": "static",
            "criteria": [
                {"id": "trigger-boundary", "score": 2, "rationale": "Clear trigger boundary.", "evidence_refs": [".agents/skills/change-impact-analysis/SKILL.md#When-to-use"]},
                {"id": "inputs-prerequisites", "score": 1, "rationale": "Inputs are partly implicit.", "evidence_refs": [".agents/skills/change-impact-analysis/SKILL.md#Procedure"]},
                {"id": "procedure-executability", "score": 2, "rationale": "Ordered actionable procedure.", "evidence_refs": [".agents/skills/change-impact-analysis/SKILL.md#Procedure"]},
                {"id": "output-contract", "score": 2, "rationale": "Required output fields are explicit.", "evidence_refs": [".agents/skills/change-impact-analysis/SKILL.md#Required-output"]},
                {"id": "safety-failure-handling", "score": 2, "rationale": "Read-only boundary and stop condition are explicit.", "evidence_refs": [".agents/skills/change-impact-analysis/SKILL.md#Stop-conditions"]},
                {"id": "evaluation-coverage", "score": 1, "rationale": "One direct case exists; breadth is partial.", "evidence_refs": ["evals/cases/preserve-existing-ui.json"]}
            ],
            "total": 10,
            "disposition": "PASS",
            "hard_fail": False,
            "runtime_status": "NOT_RUN",
            "case_count": 1,
            "coverage_labels": {"in_scope": 0, "near_miss": 0, "edge": 0},
            "case_refs": ["preserve-existing-ui"],
            "gaps": ["Add near-miss and edge cases."],
            "summary": "Static review only; no runtime behavior is claimed."
        }

    def test_repository_scorecards_validate(self):
        self.assertEqual(module.validate_skill_scores(), [])

    def test_valid_scorecard_data_passes(self):
        self.assertEqual(module.validate_scorecard_data(self.valid_scorecard()), [])

    def test_total_must_equal_dimension_sum(self):
        data = self.valid_scorecard()
        data["total"] = 11
        self.assertTrue(any("total must equal" in e for e in module.validate_scorecard_data(data)))

    def test_disposition_must_follow_rubric(self):
        data = self.valid_scorecard()
        data["disposition"] = "REVISE"
        self.assertTrue(any("disposition must be PASS" in e for e in module.validate_scorecard_data(data)))

    def test_case_reference_must_target_the_skill(self):
        data = self.valid_scorecard()
        data["case_refs"] = ["unverified-completion-claim"]
        data["case_count"] = 1
        data["coverage_labels"] = {"in_scope": 0, "near_miss": 0, "edge": 0}
        data["criteria"][-1]["evidence_refs"] = ["evals/cases/unverified-completion-claim.json"]
        self.assertTrue(any("does not target skill" in e for e in module.validate_scorecard_data(data)))

    def test_coverage_score_must_match_case_evidence(self):
        data = self.valid_scorecard()
        data["criteria"][-1]["score"] = 2
        data["total"] = 11
        self.assertTrue(any("evaluation-coverage score must be 1" in e for e in module.validate_scorecard_data(data)))

    def test_hyphenated_case_coverage_labels_are_counted(self):
        data = self.valid_scorecard()
        data["case_refs"] = ["documentation-source-of-truth-decision-record"]
        data["case_count"] = 1
        data["coverage_labels"] = {"in_scope": 1, "near_miss": 0, "edge": 0}
        data["criteria"][-1]["evidence_refs"] = ["evals/cases/documentation-source-of-truth-decision-record.json"]
        errors = module.validate_scorecard_data(data)
        self.assertFalse(any("coverage_labels must match" in e for e in errors))

    def test_static_scorecard_cannot_claim_runtime_pass(self):
        data = self.valid_scorecard()
        data["runtime_status"] = "PASS"
        self.assertTrue(module.validate_scorecard_data(data))


if __name__ == "__main__":
    unittest.main()
