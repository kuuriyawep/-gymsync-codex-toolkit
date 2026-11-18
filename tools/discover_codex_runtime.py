#!/usr/bin/env python3
"""Read-only Codex host preflight. Never prints configuration values or secrets."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Sequence

Runner = Callable[..., subprocess.CompletedProcess[str]]


def _run(command: Sequence[str], runner: Runner, timeout: int = 15) -> dict[str, Any]:
    try:
        result = runner(
            list(command),
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
        )
    except FileNotFoundError:
        return {"status": "unavailable", "returncode": None, "stdout": ""}
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "returncode": None, "stdout": ""}
    except OSError:
        return {"status": "error", "returncode": None, "stdout": ""}
    status = "success" if result.returncode == 0 else "error"
    return {"status": status, "returncode": result.returncode, "stdout": result.stdout or ""}


def _json_payload(raw: str) -> Any:
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None


def _names_from_list(payload: Any, keys: tuple[str, ...]) -> tuple[list[str], str]:
    """Extract names only from known list containers; discard all other server fields."""
    if isinstance(payload, list):
        entries = payload
    elif isinstance(payload, dict):
        entries = None
        for key in keys:
            candidate = payload.get(key)
            if isinstance(candidate, list):
                entries = candidate
                break
        if entries is None:
            return [], "unrecognized"
    else:
        return [], "unrecognized"

    names: set[str] = set()
    for item in entries:
        if not isinstance(item, dict):
            continue
        value = item.get("name") or item.get("server_name") or item.get("pluginId")
        if isinstance(value, str) and value.strip():
            names.add(value.strip())
    return sorted(names), "parsed"


def _command_evidence(result: dict[str, Any], names: list[str], parse_status: str) -> dict[str, Any]:
    raw = result.get("stdout", "")
    return {
        "status": result["status"],
        "returncode": result["returncode"],
        "parse_status": parse_status,
        "configured_names": names,
        "configured_count": len(names) if parse_status == "parsed" else None,
        "stdout_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest() if raw else None,
    }


def discover(
    *,
    which: Callable[[str], str | None] = shutil.which,
    runner: Runner = subprocess.run,
    captured_at: str | None = None,
) -> dict[str, Any]:
    """Inspect installed Codex CLI and configured server/plugin names without exposing values."""
    timestamp = captured_at or datetime.now(timezone.utc).isoformat(timespec="seconds")
    executable = which("codex")
    report: dict[str, Any] = {
        "schema_version": "1.0.0",
        "discovery_kind": "codex-host-preflight",
        "captured_at": timestamp,
        "codex_cli": {"available": bool(executable), "version": None, "version_status": "not-run"},
        "mcp_servers": {
            "status": "not-run", "returncode": None, "parse_status": "not-run",
            "configured_names": [], "configured_count": None, "stdout_sha256": None,
        },
        "plugins": {
            "status": "not-run", "returncode": None, "parse_status": "not-run",
            "configured_names": [], "configured_count": None, "stdout_sha256": None,
        },
        "active_session_tool_inventory": "not-captured",
        "limitations": [
            "This is a local host preflight, not a connection test for any MCP server.",
            "Configured MCP server names do not prove that a server starts or that its tools are callable.",
            "The active session tool inventory must be checked in Codex with /mcp and recorded separately.",
            "No config.toml, environment variable value, token, command argument, endpoint, or server output is copied into this report.",
        ],
    }
    if not executable:
        report["limitations"].insert(0, "Codex CLI was not found on PATH; no Codex commands were run.")
        return report

    version = _run([executable, "--version"], runner)
    report["codex_cli"]["version_status"] = version["status"]
    if version["status"] == "success":
        # Keep only the first short version line; never echo arbitrary stderr or config.
        first_line = version["stdout"].strip().splitlines()
        if first_line and len(first_line[0]) <= 100:
            report["codex_cli"]["version"] = first_line[0]

    mcp = _run([executable, "mcp", "list", "--json"], runner)
    mcp_names, mcp_parse = _names_from_list(_json_payload(mcp["stdout"]), ("servers", "mcp_servers"))
    report["mcp_servers"] = _command_evidence(mcp, mcp_names, mcp_parse)

    plugins = _run([executable, "plugin", "list", "--json"], runner)
    plugin_names, plugin_parse = _names_from_list(_json_payload(plugins["stdout"]), ("installed", "plugins"))
    report["plugins"] = _command_evidence(plugins, plugin_names, plugin_parse)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional path for the sanitized JSON report")
    args = parser.parse_args()
    report = discover()
    rendered = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
