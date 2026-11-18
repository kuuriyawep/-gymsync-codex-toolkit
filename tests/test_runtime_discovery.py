from __future__ import annotations

import importlib.util
import json
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "discover_codex_runtime", ROOT / "tools" / "discover_codex_runtime.py"
)
assert SPEC and SPEC.loader
discovery = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(discovery)


class RuntimeDiscoveryTests(unittest.TestCase):
    def test_missing_codex_does_not_run_commands(self) -> None:
        def fail_runner(*args, **kwargs):
            raise AssertionError("runner must not execute without codex")
        result = discovery.discover(which=lambda _: None, runner=fail_runner, captured_at="2026-11-18T00:00:00+00:00")
        self.assertFalse(result["codex_cli"]["available"])
        self.assertEqual(result["mcp_servers"]["status"], "not-run")
        self.assertEqual(result["active_session_tool_inventory"], "not-captured")

    def test_collects_only_server_and_plugin_names(self) -> None:
        responses = [
            subprocess.CompletedProcess([], 0, "codex 0.143.0\n", ""),
            subprocess.CompletedProcess([], 0, json.dumps({"servers": [
                {"name": "docs", "url": "https://example.invalid/mcp?token=secret"},
                {"name": "github", "command": "private-command", "env": {"TOKEN": "secret"}}
            ]}), ""),
            subprocess.CompletedProcess([], 0, json.dumps({"installed": [
                {"pluginId": "github@official", "version": "1.0", "token": "secret"}
            ], "available": [{"pluginId": "not-installed"}]}), "")
        ]
        calls = []
        def runner(command, **kwargs):
            calls.append(command)
            return responses[len(calls) - 1]
        result = discovery.discover(which=lambda _: "/usr/bin/codex", runner=runner, captured_at="2026-11-18T00:00:00+00:00")
        self.assertEqual(result["codex_cli"]["version"], "codex 0.143.0")
        self.assertEqual(result["mcp_servers"]["configured_names"], ["docs", "github"])
        self.assertEqual(result["plugins"]["configured_names"], ["github@official"])
        serialized = json.dumps(result)
        self.assertNotIn("secret", serialized)
        self.assertNotIn("example.invalid", serialized)
        self.assertNotIn("private-command", serialized)
        self.assertEqual(calls[1][1:], ["mcp", "list", "--json"])
        self.assertEqual(calls[2][1:], ["plugin", "list", "--json"])

    def test_unrecognized_json_is_not_reported_as_zero_servers(self) -> None:
        responses = [
            subprocess.CompletedProcess([], 0, "codex 0.143.0", ""),
            subprocess.CompletedProcess([], 0, json.dumps({"unexpected": []}), ""),
            subprocess.CompletedProcess([], 0, json.dumps({"unexpected": []}), "")
        ]
        result = discovery.discover(which=lambda _: "codex", runner=lambda *a, **k: responses.pop(0))
        self.assertEqual(result["mcp_servers"]["parse_status"], "unrecognized")
        self.assertIsNone(result["mcp_servers"]["configured_count"])

    def test_nonempty_unrecognized_entries_are_not_reported_as_empty(self) -> None:
        responses = [
            subprocess.CompletedProcess([], 0, "codex 0.143.0", ""),
            subprocess.CompletedProcess([], 0, json.dumps({"servers": [{"unexpected": "shape"}]}), ""),
            subprocess.CompletedProcess([], 0, json.dumps({"installed": []}), "")
        ]
        result = discovery.discover(which=lambda _: "codex", runner=lambda *a, **k: responses.pop(0))
        self.assertEqual(result["mcp_servers"]["parse_status"], "unrecognized")
        self.assertIsNone(result["mcp_servers"]["configured_count"])

    def test_timeout_is_reported_without_crashing(self) -> None:
        def runner(*args, **kwargs):
            raise subprocess.TimeoutExpired(args[0], kwargs.get("timeout", 15))
        result = discovery.discover(which=lambda _: "codex", runner=runner)
        self.assertEqual(result["codex_cli"]["version_status"], "timeout")
        self.assertEqual(result["mcp_servers"]["status"], "timeout")
        self.assertEqual(result["plugins"]["status"], "timeout")

    def test_nonzero_command_is_reported_as_error(self) -> None:
        responses = [
            subprocess.CompletedProcess([], 0, "codex 0.143.0", ""),
            subprocess.CompletedProcess([], 2, "", "private error detail"),
            subprocess.CompletedProcess([], 0, json.dumps({"installed": []}), "")
        ]
        result = discovery.discover(which=lambda _: "codex", runner=lambda *a, **k: responses.pop(0))
        self.assertEqual(result["mcp_servers"]["status"], "error")
        self.assertNotIn("private error detail", json.dumps(result))


if __name__ == "__main__":
    unittest.main()
