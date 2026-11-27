from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas" / "collaboration-record.schema.json").read_text(encoding="utf-8"))
CONTRACT = (ROOT / "docs" / "agent-collaboration-protocol.md").read_text(encoding="utf-8")


class AgentCollaborationContractTests(unittest.TestCase):
    def test_schema_is_closed_draft_2020_12_contract(self):
        self.assertEqual(SCHEMA["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(SCHEMA["type"], "object")
        self.assertFalse(SCHEMA["additionalProperties"])
        self.assertTrue(set(SCHEMA["required"]).issubset(SCHEMA["properties"]))

    def test_supported_interaction_events_cover_four_protocols(self):
        events = set(SCHEMA["properties"]["event_type"]["enum"])
        self.assertTrue({
            "consultation_requested", "consultation_responded",
            "review_requested", "review_submitted",
            "disagreement_raised", "disagreement_resolved",
            "incident_escalated", "incident_acknowledged", "incident_closed",
        }.issubset(events))

    def test_records_link_interactions_and_preserve_evidence(self):
        required = set(SCHEMA["required"])
        self.assertTrue({
            "record_id", "interaction_id", "workflow_id", "task_id",
            "sender", "recipient", "created_at", "scope", "request", "evidence_refs",
        }.issubset(required))
        self.assertIn("related_record_ids", SCHEMA["properties"])

    def test_disagreement_resolution_requires_codex_decision(self):
        rule = next(rule for rule in SCHEMA["allOf"]
                    if rule["if"]["properties"]["event_type"].get("const") == "disagreement_resolved")
        self.assertIn("codex_decision", rule["then"]["required"])
        self.assertEqual(rule["then"]["properties"]["codex_decision"]["type"], "object")

    def test_incident_escalation_requires_severity_and_dedupe(self):
        rule = next(rule for rule in SCHEMA["allOf"]
                    if rule["if"]["properties"]["event_type"].get("const") == "incident_escalated")
        self.assertTrue({"severity", "dedupe_fingerprint"}.issubset(rule["then"]["required"]))

    def test_contract_preserves_codex_authority_and_ownership(self):
        for phrase in (
            "Codex is the sole accountable coordinator",
            "Does not transfer task ownership",
            "Codex records the outcome and rationale",
            "cannot independently change permissions",
            "do not self-arbitrate, self-approve",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, CONTRACT)

    def test_contract_distinguishes_static_contracts_from_live_runtime(self):
        self.assertIn("live multi-agent behavior is NOT_RUN / BLOCKED", CONTRACT)
        self.assertIn("does not itself send messages, start agents", CONTRACT)
        self.assertIn("not a parallel workflow ledger", CONTRACT)


if __name__ == "__main__":
    unittest.main()
