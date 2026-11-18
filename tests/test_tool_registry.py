from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_tool_registry", ROOT / "tools" / "validate_tool_registry.py"
)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ToolRegistryTests(unittest.TestCase):
    def test_empty_deny_by_default_registry_is_valid(self) -> None:
        self.assertEqual(validator.validate_files(), [])

    def valid_tool(self) -> dict:
        return {
            "id": "repo.read",
            "name": "Repository Read",
            "description": "Read repository files through an explicitly exposed host tool.",
            "provider": "codex-host",
            "transport": "codex-native",
            "capabilities": ["filesystem.read"],
            "operations": [{
                "id": "read-file",
                "description": "Read a file within the approved repository scope.",
                "risk": "read",
                "idempotent": True,
                "approval": "none",
                "input_schema": {"type": "object"},
                "output_schema": {"type": "object"}
            }],
            "availability": "configured",
            "permission_profile": "repo-explorer",
            "credential_ref": None,
            "evidence": {
                "status": "static-reviewed",
                "references": ["docs/phase-7-tool-ecosystem.md"]
            }
        }

    def registry(self, tool: dict) -> dict:
        return {"schema_version": "1.0.0", "registry_id": "codex-toolkit",
                "default_policy": "deny", "tools": [tool]}

    def test_valid_declared_tool_is_accepted(self) -> None:
        self.assertEqual(validator.validate_registry(self.registry(self.valid_tool())), [])

    def test_duplicate_tool_id_is_rejected(self) -> None:
        tool = self.valid_tool()
        data = self.registry(tool)
        data["tools"].append(dict(tool))
        self.assertTrue(any("duplicate tool id" in e for e in validator.validate_registry(data)))

    def test_raw_credential_is_rejected(self) -> None:
        tool = self.valid_tool()
        tool["credential_ref"] = "sk-live-secret-value"
        self.assertTrue(any("raw credentials are forbidden" in e for e in validator.validate_registry(self.registry(tool))))

    def test_verified_tool_requires_runtime_evidence(self) -> None:
        tool = self.valid_tool()
        tool["availability"] = "verified"
        self.assertTrue(any("verified availability requires runtime-verified evidence" in e for e in validator.validate_registry(self.registry(tool))))

    def test_destructive_operation_requires_explicit_approval(self) -> None:
        tool = self.valid_tool()
        tool["operations"][0]["risk"] = "destructive"
        tool["operations"][0]["approval"] = "none"
        self.assertTrue(any("destructive/external operations must require approval" in e for e in validator.validate_registry(self.registry(tool))))


if (require.main === module) {
  // Python unit tests are the executable test contract.
}
