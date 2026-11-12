#!/usr/bin/env python3
"""Validate the repository's Codex skills, agents, workflows, and evaluation cases.

Uses only the Python standard library. Run from any working directory:
    python tools/validate_toolkit.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
WARNINGS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def warn(message: str) -> None:
    WARNINGS.append(message)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(f"{path.relative_to(ROOT)}: cannot read file ({exc})")
        return ""


def parse_frontmatter(path: Path) -> tuple[str, dict[str, str]]:
    text = read_text(path)
    if not text.startswith("---\n"):
        fail(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
        return text, {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        fail(f"{path.relative_to(ROOT)}: unterminated YAML frontmatter")
        return text, {}
    metadata: dict[str, str] = {}
    for line in parts[1].splitlines():
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*?)\s*$", line)
        if match:
            metadata[match.group(1)] = match.group(2).strip().strip('"').strip("'")
    return parts[2].lstrip("\n"), metadata


def validate_skills() -> None:
    native_root = ROOT / ".agents" / "skills"
    mirror_root = ROOT / "skills"
    if not native_root.is_dir():
        fail(".agents/skills directory is missing")
        return
    native_names = {p.name for p in native_root.iterdir() if p.is_dir()}
    mirror_names = {p.name for p in mirror_root.iterdir() if p.is_dir()} if mirror_root.is_dir() else set()
    for name in sorted(native_names - mirror_names):
        fail(f"skills/{name} portable mirror is missing")
    for name in sorted(mirror_names - native_names):
        fail(f".agents/skills/{name} native skill is missing")
    for name in sorted(native_names & mirror_names):
        native = native_root / name / "SKILL.md"
        mirror = mirror_root / name / "SKILL.md"
        if not native.is_file():
            fail(f"{native.relative_to(ROOT)} is missing")
            continue
        _, metadata = parse_frontmatter(native)
        if not metadata.get("name"):
            fail(f"{native.relative_to(ROOT)}: metadata name is required")
        if not metadata.get("description"):
            fail(f"{native.relative_to(ROOT)}: metadata description is required")
        if metadata.get("name") != name:
            fail(f"{native.relative_to(ROOT)}: metadata name must match directory '{name}'")
        if not mirror.is_file():
            fail(f"{mirror.relative_to(ROOT)} is missing")
        elif native.read_bytes() != mirror.read_bytes():
            fail(f"{name}: native and portable SKILL.md files differ")


def validate_agents() -> None:
    agent_dir = ROOT / ".codex" / "agents"
    if not agent_dir.is_dir():
        fail(".codex/agents directory is missing")
        return
    try:
        import tomllib
    except ImportError:
        warn("Python 3.11+ is required for native TOML parsing; agent TOML checks skipped")
        return
    for path in sorted(agent_dir.glob("*.toml")):
        try:
            data = tomllib.loads(read_text(path))
        except tomllib.TOMLDecodeError as exc:
            fail(f"{path.relative_to(ROOT)}: invalid TOML ({exc})")
            continue
        for key in ("name", "description", "developer_instructions"):
            if not isinstance(data.get(key), str) or not data[key].strip():
                fail(f"{path.relative_to(ROOT)}: '{key}' must be a non-empty string")
        if data.get("name") and data["name"] != path.stem:
            fail(f"{path.relative_to(ROOT)}: name must match filename '{path.stem}'")


def validate_workflows() -> None:
    directory = ROOT / "workflows"
    required = ("## Workflow", "## Stop conditions", "## Required output")
    for path in sorted(directory.glob("*.md")):
        content = read_text(path)
        for heading in required:
            if heading not in content:
                fail(f"{path.relative_to(ROOT)}: missing section '{heading}'")


def validate_eval_cases() -> None:
    directory = ROOT / "evals" / "cases"
    if not directory.exists():
        warn("evals/cases directory does not exist yet")
        return
    for path in sorted(directory.glob("*.json")):
        try:
            data = json.loads(read_text(path))
        except json.JSONDecodeError as exc:
            fail(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")
            continue
        for key in ("id", "title", "prompt", "expected_behaviors"):
            if key not in data:
                fail(f"{path.relative_to(ROOT)}: missing '{key}'")
        if not isinstance(data.get("expected_behaviors", []), list):
            fail(f"{path.relative_to(ROOT)}: expected_behaviors must be an array")


def main() -> int:
    validate_skills()
    validate_agents()
    validate_workflows()
    validate_eval_cases()
    for message in WARNINGS:
        print(f"WARNING: {message}")
    for message in ERRORS:
        print(f"ERROR: {message}")
    if ERRORS:
        print(f"\nValidation failed: {len(ERRORS)} error(s), {len(WARNINGS)} warning(s).")
        return 1
    print(f"Validation passed: structure and metadata checks completed ({len(WARNINGS)} warning(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
