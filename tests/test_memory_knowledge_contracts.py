from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = json.loads((ROOT / "schemas" / "project-memory-record.schema.json").read_text(encoding="utf-8"))
PROPOSAL = json.loads((ROOT / "schemas" / "memory-update-proposal.schema.json").read_text(encoding="utf-8"))
DOC = (ROOT / "docs" / "memory-knowledge-governance.md").read_text(encoding="utf-8")
TOOLS = json.loads((ROOT / "registry" / "tools.json").read_text(encoding="utf-8"))


class MemoryKnowledgeContractTests(unittest.TestCase):
    def test_memory_record_is_closed_and_provenance_bearing(self):
        self.assertFalse(RECORD["additionalProperties"])
        self.assertTrue({"scope", "status", "confidence", "provenance", "verified_at", "review_policy"}.issubset(RECORD["required"]))
        provenance = RECORD["properties"]["provenance"]
        self.assertGreaterEqual(provenance["minItems"], 1)
        self.assertIn("commit_or_version", provenance["items"]["properties"])

    def test_memory_lifecycle_and_scopes_are_bounded(self):
        self.assertEqual(set(RECORD["properties"]["status"]["enum"]), {"proposed", "accepted", "superseded", "stale", "disputed", "rejected"})
        self.assertEqual(set(RECORD["properties"]["scope"]["properties"]["kind"]["enum"]), {"shared_project", "specialist", "execution_reference"})

    def test_accepted_memory_requires_verification_timestamp(self):
        rule = RECORD["allOf"][1]["then"]["properties"]["verified_at"]
        self.assertEqual(rule["type"], "string")

    def test_specialist_memory_requires_role_identity(self):
        rule = RECORD["allOf"][0]
        self.assertIn("specialist_role", rule["then"]["properties"]["scope"]["required"])

    def test_proposals_cannot_be_confused_with_accepted_memory(self):
        self.assertIn("decision", PROPOSAL["required"])
        self.assertIn("Codex must validate", PROPOSAL["$comment"])
        self.assertIn("proposal submission never mutates canonical memory", PROPOSAL["$comment"])

    def test_graphify_remains_optional_planned_and_read_only(self):
        graph = next(x for x in TOOLS["tools"] if x["id"] == "graphify-local")
        self.assertEqual(graph["availability"], "planned")
        self.assertEqual(graph["default_policy"] if "default_policy" in graph else TOOLS["default_policy"], "deny")
        self.assertTrue(all(op["effect"] == "none" and op["risk"] == "read" for op in graph["operations"]))

    def test_docs_separate_memory_planes_and_preserve_authority(self):
        for phrase in ("Shared Project Memory", "Specialist Memory", "Execution Memory", "Repository Knowledge Graph", "Codex governs canonical project memory", "never sufficient by itself"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), DOC.lower())

    def test_docs_cover_staleness_conflict_and_no_secrets(self):
        for phrase in ("stale", "disputed", "credentials", "provenance", "fail"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), DOC.lower())


if __name__ == "__main__":
    unittest.main()
