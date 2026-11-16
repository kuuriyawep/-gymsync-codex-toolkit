#!/usr/bin/env python3
"""Validate Codex skills, agents, workflows, and the hybrid evaluation framework.

Uses only the Python standard library. Run from any working directory:
    python tools/validate_toolkit.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from evaluate_toolkit import inspect_cases, inspect_rubrics  # noqa: E402

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
    required = ("## Stop conditions", "## Required output")
    for path in sorted(directory.glob("*.md")):
        content = read_text(path)
        if "## Workflow" not in content and "## Audit workflow" not in content:
            fail(f"{path.relative_to(ROOT)}: missing section '## Workflow' (or '## Audit workflow')")
        for heading in required:
            if heading not in content:
                fail(f"{path.relative_to(ROOT)}: missing section '{heading}'")



def validate_skill_case_coverage(cases: list[dict], rubric: dict) -> list[str]:
    """Enforce the case mix declared by a structured skill-quality rubric."""
    requirement = rubric.get("coverage_requirements")
    if not isinstance(requirement, dict):
        return []
    target_skill = requirement.get("target_skill")
    minimums = requirement.get("minimums", {})
    if not isinstance(target_skill, str) or not isinstance(minimums, dict):
        return ["skill-quality rubric: invalid coverage_requirements contract"]
    counts = {"in-scope": 0, "near-miss": 0, "edge": 0}
    unlabeled: list[str] = []
    for item in cases:
        data = item.get("data", {})
        targets = data.get("target", [])
        if target_skill not in targets:
            continue
        coverage = data.get("coverage")
        if coverage not in counts:
            unlabeled.append(str(item.get("path", "<unknown>")))
        else:
            counts[coverage] += 1
    errors = [f"{target_skill}: evaluation case missing valid coverage label: {path}" for path in unlabeled]
    for category, minimum in minimums.items():
        if counts.get(category, 0) < minimum:
            errors.append(f"{target_skill}: {category} coverage requires at least {minimum} case(s), found {counts.get(category, 0)}")
    return errors


def validate_evaluation_framework() -> None:
    required_files = (
        "evals/README.md",
        "evals/taxonomy.md",
        "evals/rubrics/deterministic.md",
        "evals/rubrics/behavioral.md",
        "evals/rubrics/deterministic.json",
        "evals/rubrics/behavioral.json",
        "schemas/evaluation-case.schema.json",
        "schemas/evaluation-result.schema.json",
        "schemas/evaluation-rubric.schema.json",
        "tools/evaluate_toolkit.py",
        "templates/evaluation-report.md",
    )
    for relative in required_files:
        if not (ROOT / relative).is_file():
            fail(f"required evaluation framework file is missing: {relative}")
    for relative in (
        "schemas/evaluation-case.schema.json",
        "schemas/evaluation-result.schema.json",
        "schemas/evaluation-rubric.schema.json",
    ):
        path = ROOT / relative
        if path.is_file():
            try:
                json.loads(read_text(path))
            except json.JSONDecodeError as exc:
                fail(f"{relative}: invalid JSON ({exc})")
    cases, issues = inspect_cases()
    for issue in issues:
        fail(issue)
    for issue in inspect_rubrics():
        fail(issue)
    skill_rubric_path = ROOT / "evals" / "rubrics" / "skill-quality.json"
    if skill_rubric_path.is_file():
        try:
            skill_rubric = json.loads(read_text(skill_rubric_path))
            for issue in validate_skill_case_coverage(cases, skill_rubric):
                fail(issue)
        except json.JSONDecodeError as exc:
            fail(f"evals/rubrics/skill-quality.json: invalid JSON ({exc})")
    ids = [item["data"].get("id") for item in cases]
    if len(ids) != len(set(ids)):
        fail("evaluation case IDs must be unique")
    if not cases:
        warn("no evaluation cases discovered under evals/cases")


def main() -> int:
    validate_skills()
    validate_agents()
    validate_workflows()
    validate_evaluation_framework()
    for message in WARNINGS:
        print(f"WARNING: {message}")
    for message in ERRORS:
        print(f"ERROR: {message}")
    if ERRORS:
        print(f"\nValidation failed: {len(ERRORS)} error(s), {len(WARNINGS)} warning(s).")
        return 1
    print(f"Validation passed: toolkit and evaluation framework checks completed ({len(WARNINGS)} warning(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
