from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOVERNANCE = ROOT / "docs" / "intelligence-evaluation-governance.md"
CASE_DIR = ROOT / "evals" / "cases"

WS7_CASES = {
    "intelligence-initiative-quality-deduplication",
    "backend-payment-concurrency-synthetic-fixture",
    "evaluation-untrusted-evidence-and-self-grading",
}


class IntelligenceEvaluationGovernanceTests(unittest.TestCase):
    def test_governance_defines_all_six_dimensions(self) -> None:
        text = GOVERNANCE.read_text(encoding="utf-8")
        for dimension in (
            "Reasoning quality",
            "Tool proficiency",
            "Initiative quality",
            "Collaboration",
            "Reliability and recovery",
            "Governance compliance",
        ):
            with self.subTest(dimension=dimension):
                self.assertIn(dimension, text)

    def test_governance_preserves_runtime_evaluation_boundary(self) -> None:
        text = GOVERNANCE.read_text(encoding="utf-8")
        self.assertIn("does not launch Codex", text)
        self.assertIn("NOT_RUN / BLOCKED", text)
        self.assertIn("A proposal is not an authorization", text)
        self.assertIn("critical failure", text.lower())

    def test_ws7_cases_exist_and_have_unique_ids(self) -> None:
        seen = set()
        for case_id in WS7_CASES:
            path = CASE_DIR / f"{case_id}.json"
            self.assertTrue(path.is_file(), f"missing case: {path.name}")
            case = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(case["id"], case_id)
            self.assertNotIn(case_id, seen)
            seen.add(case_id)
            self.assertTrue(case["expected_behaviors"])
            self.assertIn(case["risk_level"], {"low", "medium", "high", "critical"})

    def test_backend_case_is_synthetic_and_covers_concurrency(self) -> None:
        case = json.loads(
            (CASE_DIR / "backend-payment-concurrency-synthetic-fixture.json").read_text(
                encoding="utf-8"
            )
        )
        text = " ".join(case["preconditions"] + case["expected_behaviors"] + case["must_not"]).lower()
        for required in ("synthetic", "concurrent", "idempotency", "production"):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_untrusted_evidence_case_prohibits_self_grading(self) -> None:
        case = json.loads(
            (CASE_DIR / "evaluation-untrusted-evidence-and-self-grading.json").read_text(
                encoding="utf-8"
            )
        )
        combined = " ".join(case["expected_behaviors"] + case["must_not"]).lower()
        self.assertIn("sole grader", combined)
        self.assertIn("untrusted", combined)
        self.assertTrue(case["critical_behaviors"])


if __name__ == "__main__":
    unittest.main()
