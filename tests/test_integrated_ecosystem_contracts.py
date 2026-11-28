from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE = json.loads((ROOT / "evals" / "cases" / "integrated-security-backend-qa-approval-report.json").read_text(encoding="utf-8"))
DOC = (ROOT / "docs" / "integration-readiness-validation.md").read_text(encoding="utf-8")


class IntegratedEcosystemContractTests(unittest.TestCase):
    def test_scenario_has_the_required_ordered_lifecycle(self):
        stages = CASE["ordered_stages"]
        self.assertEqual(
            [stage["id"] for stage in stages],
            [
                "security_detection",
                "codex_triage",
                "backend_analysis",
                "qa_independent_validation",
                "codex_arbitration",
                "approval_gate",
                "authorized_report",
            ],
        )
        self.assertEqual(stages[0]["owner"], "security_auditor")
        self.assertEqual(stages[1]["owner"], "codex")
        self.assertEqual(stages[3]["owner"], "test_engineer")
        self.assertEqual(stages[5]["owner"], "user")

    def test_each_stage_declares_evidence_and_prohibited_actions(self):
        for stage in CASE["ordered_stages"]:
            with self.subTest(stage=stage["id"]):
                self.assertTrue(stage["requires"])
                self.assertTrue(stage["forbids"])

    def test_scenario_covers_all_required_failure_paths(self):
        self.assertEqual(
            set(CASE["failure_paths"]),
            {
                "specialist_or_runtime_unavailable",
                "conflicting_security_backend_or_qa_findings",
                "messaging_delivery_failure",
                "duplicate_event_or_replayed_message",
                "false_positive_security_signal",
                "unauthorized_action_attempt",
                "partial_execution_and_checkpoint_recovery",
                "codex_runtime_unavailable",
            },
        )

    def test_scenario_is_synthetic_and_does_not_claim_live_execution(self):
        self.assertFalse(CASE["preconditions"]["runtime_available"])
        self.assertFalse(CASE["preconditions"]["production_access"])
        self.assertFalse(CASE["preconditions"]["external_messaging_enabled"])
        self.assertEqual(CASE["behavioral_status"], "BLOCKED")
        self.assertEqual(CASE["live_execution_claim"], "NOT_CLAIMED")

    def test_governance_invariants_are_explicit(self):
        invariants = " ".join(CASE["invariants"]).lower()
        for phrase in ("codex remains", "user remains", "no production", "no agent self-approval", "traceable"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, invariants)

    def test_document_separates_repository_and_behavioral_acceptance(self):
        for phrase in ("BLOCKED / NOT_RUN", "cannot prove", "exact action", "failure paths", "architecture reconciliation"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), DOC.lower())


if __name__ == "__main__":
    unittest.main()
