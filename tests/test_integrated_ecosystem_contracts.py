from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE = json.loads((ROOT / "evals" / "cases" / "integrated-security-backend-qa-approval-report.json").read_text(encoding="utf-8"))
DOC = (ROOT / "docs" / "integration-readiness-validation.md").read_text(encoding="utf-8")


class IntegratedEcosystemContractTests(unittest.TestCase):
    def test_case_uses_the_canonical_evaluation_contract(self):
        self.assertEqual(CASE["id"], "integrated-security-backend-qa-approval-report")
        for field in ("prompt", "target", "preconditions", "expected_behaviors", "must_not", "expected_artifacts", "risk_level", "evaluation_method"):
            with self.subTest(field=field):
                self.assertIn(field, CASE)
                self.assertTrue(CASE[field])

    def test_scenario_covers_the_required_ordered_lifecycle(self):
        behaviors = " ".join(CASE["expected_behaviors"]).lower()
        ordered_concepts = [
            "security specialist",
            "codex validates",
            "backend/implementer",
            "qa/test_engineer",
            "codex compares",
            "r4 action requires user approval",
            "whatsapp gateway",
        ]
        positions = [behaviors.index(concept) for concept in ordered_concepts]
        self.assertEqual(positions, sorted(positions))

    def test_all_required_failure_paths_are_covered(self):
        behaviors = " ".join(CASE["expected_behaviors"]).lower()
        for phrase in (
            "specialist or runtime unavailable",
            "conflicting security, backend, or qa findings",
            "messaging delivery failure",
            "duplicate event or replayed message",
            "false-positive security signal",
            "unauthorized action attempt",
            "partial execution and checkpoint recovery",
            "codex runtime unavailable",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, behaviors)

    def test_prohibited_actions_and_truthful_blocked_status_are_explicit(self):
        prohibited = " ".join(CASE["must_not"]).lower()
        for phrase in ("production", "real external message", "self-approve", "user approval", "behavioral pass"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, prohibited)

    def test_evidence_and_traceability_are_required(self):
        behaviors = " ".join(CASE["expected_behaviors"]).lower()
        artifacts = " ".join(CASE["expected_artifacts"]).lower()
        self.assertIn("evidence references", behaviors)
        self.assertIn("traceable event, task, evidence, review, approval, and report references", behaviors)
        self.assertIn("every stage", artifacts)

    def test_document_separates_repository_and_behavioral_acceptance(self):
        for phrase in ("BLOCKED / NOT_RUN", "cannot prove", "exact action", "failure paths", "architecture reconciliation"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), DOC.lower())


if __name__ == "__main__":
    unittest.main()
