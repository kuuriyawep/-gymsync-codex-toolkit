#!/usr/bin/env python3
"""Validate static skill scorecards against the canonical rubric and case inventory."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
SCORE_DIR = ROOT / "evals" / "skill-scores"
CASE_DIR = ROOT / "evals" / "cases"
SKILL_DIR = ROOT / ".agents" / "skills"
CRITERIA = {
    "trigger-boundary", "inputs-prerequisites", "procedure-executability",
    "output-contract", "safety-failure-handling", "evaluation-coverage",
}
SHA_RE = re.compile(r"^[a-f0-9]{40}$")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid JSON from {path}: {exc}") from exc


def schema_errors(value: Any) -> list[str]:
    try:
        schema = load_json(ROOT / "schemas" / "skill-quality-score.schema.json")
        from evaluate_toolkit import validate_instance
        return validate_instance(value, schema)
    except (ValueError, ImportError) as exc:
        return [str(exc)]


def expected_disposition(total: int, scores: list[int], hard_fail: bool) -> str:
    if hard_fail or total <= 6:
        return "FAIL"
    if total >= 10 and scores and min(scores) >= 1:
        return "PASS"
    return "REVISE"


def validate_scorecard_data(data: Any, *, check_case_files: bool = True) -> list[str]:
    errors = schema_errors(data)
    if errors:
        return errors
    if not isinstance(data, dict):
        return ["scorecard must be an object"]

    skill_id = data["skill_id"]
    skill_path = data["skill_path"]
    if skill_path != f".agents/skills/{skill_id}/SKILL.md":
        errors.append("skill_path must match skill_id")
    if not SHA_RE.fullmatch(data["target_revision"]):
        errors.append("target_revision must be a 40-character commit SHA")

    criteria = data["criteria"]
    ids = [item["id"] for item in criteria]
    if len(ids) != len(set(ids)) or set(ids) != CRITERIA:
        errors.append("criteria must contain each of the six rubric dimensions exactly once")
    scores = [item["score"] for item in criteria]
    total = sum(scores)
    if data["total"] != total:
        errors.append(f"total must equal criterion score sum ({total})")
    expected = expected_disposition(total, scores, data["hard_fail"])
    if data["disposition"] != expected:
        errors.append(f"disposition must be {expected} for the recorded scores/hard-fail state")

    refs = data["case_refs"]
    if data["case_count"] != len(refs):
        errors.append("case_count must equal the number of case_refs")
    observed = {"in_scope": 0, "near_miss": 0, "edge": 0}
    if check_case_files:
        for case_id in refs:
            path = CASE_DIR / f"{case_id}.json"
            if not path.is_file():
                errors.append(f"referenced evaluation case does not exist: {case_id}")
                continue
            try:
                case = load_json(path)
            except ValueError as exc:
                errors.append(str(exc))
                continue
            targets = case.get("target", [])
            if skill_id not in targets and skill_path not in targets:
                errors.append(f"case {case_id} does not target skill {skill_id}")
            coverage = case.get("coverage")
            if coverage in observed:
                observed[coverage] += 1
    if data["coverage_labels"] != observed:
        errors.append(f"coverage_labels must match referenced cases: expected {observed}")
    if data["case_count"] == 0:
        expected_coverage_score = 0
    elif data["case_count"] >= 6 and observed["in_scope"] >= 3 and observed["near_miss"] >= 2 and observed["edge"] >= 1:
        expected_coverage_score = 2
    else:
        expected_coverage_score = 1
    coverage_scores = [item["score"] for item in criteria if item["id"] == "evaluation-coverage"]
    if coverage_scores and coverage_scores[0] != expected_coverage_score:
        errors.append(f"evaluation-coverage score must be {expected_coverage_score} for the available case evidence")
    return errors


def validate_skill_scores() -> list[str]:
    errors: list[str] = []
    expected_skills = {path.parent.name for path in SKILL_DIR.glob("*/SKILL.md")}
    score_files = sorted(SCORE_DIR.glob("*.json")) if SCORE_DIR.exists() else []
    found_skills = {path.stem for path in score_files}
    for missing in sorted(expected_skills - found_skills):
        errors.append(f"missing static skill scorecard: {missing}")
    for extra in sorted(found_skills - expected_skills):
        errors.append(f"scorecard has no matching native skill: {extra}")
    for path in score_files:
        try:
            data = load_json(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if data.get("skill_id") != path.stem:
            errors.append(f"{path.name}: skill_id must match filename")
        for issue in validate_scorecard_data(data):
            errors.append(f"{path.name}: {issue}")
    return errors


if __name__ == "__main__":
    issues = validate_skill_scores()
    for issue in issues:
        print(f"ERROR: {issue}")
    if issues:
        raise SystemExit(1)
    print("Static skill scorecards validated; runtime status remains NOT_RUN.")
