#!/usr/bin/env python3
"""Prepare and validate hybrid toolkit evaluation runs.

This runner validates repository artifacts and creates evidence-ready records.
It deliberately does not launch Codex or claim to grade model behavior.
Python standard library only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASE_DIR = ROOT / "evals" / "cases"
CASE_SCHEMA = ROOT / "schemas" / "evaluation-case.schema.json"
RUBRIC_DIR = ROOT / "evals" / "rubrics"
RUBRIC_SCHEMA = ROOT / "schemas" / "evaluation-rubric.schema.json"
RESULT_SCHEMA = ROOT / "schemas" / "evaluation-result.schema.json"
VALID_STATUSES = {"PASS", "FAIL", "BLOCKED", "NOT_RUN", "NOT_APPLICABLE"}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def type_matches(value: Any, expected: str) -> bool:
    checks = {
        "object": lambda v: isinstance(v, dict),
        "array": lambda v: isinstance(v, list),
        "string": lambda v: isinstance(v, str),
        "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
        "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
        "boolean": lambda v: isinstance(v, bool),
        "null": lambda v: v is None,
    }
    return checks.get(expected, lambda _v: True)(value)


def validate_instance(value: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    """Validate the JSON Schema keywords used by this repository's schemas."""
    errors: list[str] = []
    expected = schema.get("type")
    if isinstance(expected, list):
        if not any(type_matches(value, item) for item in expected):
            return [f"{path}: expected one of types {expected}"]
    elif expected and not type_matches(value, expected):
        return [f"{path}: expected {expected}"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value must be one of {schema['enum']!r}")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: shorter than minLength")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: does not match required pattern")
        if schema.get("format") == "date-time":
            try:
                parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
                if parsed.tzinfo is None:
                    raise ValueError("timezone is required")
            except ValueError:
                errors.append(f"{path}: expected an ISO 8601 date-time with timezone")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if value < schema.get("minimum", float("-inf")):
            errors.append(f"{path}: below minimum")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: fewer than minItems")
        if schema.get("uniqueItems") and len({json.dumps(x, sort_keys=True) for x in value}) != len(value):
            errors.append(f"{path}: items must be unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(validate_instance(item, item_schema, f"{path}[{index}]"))
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing required property {key!r}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value.keys() - properties.keys():
                errors.append(f"{path}: unexpected property {key!r}")
        for key, child in properties.items():
            if key in value and isinstance(child, dict):
                errors.extend(validate_instance(value[key], child, f"{path}.{key}"))
    return errors


def case_files() -> list[Path]:
    return sorted(CASE_DIR.glob("*.json")) if CASE_DIR.is_dir() else []


def inspect_cases() -> tuple[list[dict[str, Any]], list[str]]:
    issues: list[str] = []
    cases: list[dict[str, Any]] = []
    if not CASE_SCHEMA.is_file():
        return [], ["Missing schema: schemas/evaluation-case.schema.json"]
    schema = load_json(CASE_SCHEMA)
    seen: set[str] = set()
    for path in case_files():
        try:
            case = load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            issues.append(f"{path.relative_to(ROOT)}: cannot parse JSON ({exc})")
            continue
        if not isinstance(case, dict):
            issues.append(f"{path.relative_to(ROOT)}: root must be an object")
            continue
        errors = validate_instance(case, schema)
        issues.extend(f"{path.relative_to(ROOT)}: {error}" for error in errors)
        targets = case.get("target", [])
        if isinstance(targets, list):
            for target in targets:
                if not isinstance(target, str):
                    continue  # The schema error above already reports the invalid target type.
                # Existing cases use both semantic target IDs and repository-relative paths.
                path_like = target.startswith(".") or "/" in target or Path(target).suffix in {".md", ".py", ".json", ".toml"}
                if not path_like:
                    continue
                target_path = (ROOT / target).resolve()
                if ROOT.resolve() not in target_path.parents and target_path != ROOT.resolve():
                    issues.append(f"{path.relative_to(ROOT)}: target escapes repository root: {target}")
                elif not target_path.exists():
                    issues.append(f"{path.relative_to(ROOT)}: target does not exist: {target}")
        critical_ids = case.get("critical_behaviors", [])
        allowed_critical_ids = {f"behavior-{i:02d}" for i in range(1, len(case.get("expected_behaviors", [])) + 1)} | {f"must-not-{i:02d}" for i in range(1, len(case.get("must_not", [])) + 1)}
        if isinstance(critical_ids, list):
            for criterion_id in critical_ids:
                if criterion_id not in allowed_critical_ids:
                    issues.append(f"{path.relative_to(ROOT)}: critical_behaviors references unknown criterion {criterion_id!r}")
        case_id = case.get("id")
        if isinstance(case_id, str):
            if case_id in seen:
                issues.append(f"{path.relative_to(ROOT)}: duplicate case id {case_id!r}")
            seen.add(case_id)
        cases.append({"path": path, "data": case, "valid": not errors})
    if not cases:
        issues.append("No evaluation cases discovered under evals/cases/*.json")
    return cases, issues



def inspect_rubrics() -> list[str]:
    issues: list[str] = []
    if not RUBRIC_SCHEMA.is_file():
        return ["Missing schema: schemas/evaluation-rubric.schema.json"]
    if not RUBRIC_DIR.is_dir():
        return ["Missing rubric directory: evals/rubrics"]
    schema = load_json(RUBRIC_SCHEMA)
    rubric_paths = sorted(RUBRIC_DIR.glob("*.json"))
    if not rubric_paths:
        return ["No structured rubric definitions found under evals/rubrics"]
    seen: set[str] = set()
    for path in rubric_paths:
        try:
            rubric = load_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            issues.append(f"{path.relative_to(ROOT)}: cannot parse JSON ({exc})")
            continue
        if not isinstance(rubric, dict):
            issues.append(f"{path.relative_to(ROOT)}: root must be an object")
            continue
        for error in validate_instance(rubric, schema):
            issues.append(f"{path.relative_to(ROOT)}: {error}")
        rubric_id = rubric.get("id")
        if isinstance(rubric_id, str):
            if rubric_id in seen:
                issues.append(f"{path.relative_to(ROOT)}: duplicate rubric id {rubric_id!r}")
            seen.add(rubric_id)
    return issues

def print_case_list(cases: list[dict[str, Any]]) -> None:
    for item in cases:
        data = item["data"]
        print(f"{data.get('id', '<missing>')} — {data.get('title', item['path'].name)}")


def overall_status(criteria: list[dict[str, Any]]) -> str:
    if any(c["critical"] and c["status"] == "FAIL" for c in criteria):
        return "FAIL"
    if any(c["status"] == "FAIL" for c in criteria):
        return "FAIL"
    if any(c["status"] == "BLOCKED" for c in criteria):
        return "BLOCKED"
    applicable = [c for c in criteria if c["status"] != "NOT_APPLICABLE"]
    if not applicable or any(c["status"] == "NOT_RUN" for c in applicable):
        return "NOT_RUN"
    if any(c["status"] != "PASS" for c in applicable):
        return "PARTIAL"
    return "PASS"


def make_report(record: dict[str, Any]) -> str:
    summary = record["summary"]
    lines = [
        f"# Evaluation Report — {record['run_id']}", "",
        f"- **Created:** {record['created_at']}",
        f"- **Repository:** {record['target']['repository']}",
        f"- **Revision:** {record['target']['revision'] or 'unknown'}",
        f"- **Grader:** {record['grader']}",
        f"- **Overall status:** {record['overall_status']}", "",
        "## Criterion summary", "",
        "| Status | Count |", "|---|---:|",
    ]
    for key, label in [("pass", "PASS"), ("fail", "FAIL"), ("blocked", "BLOCKED"),
                       ("not_run", "NOT_RUN"), ("not_applicable", "NOT_APPLICABLE")]:
        lines.append(f"| {label} | {summary[key]} |")
    lines.extend(["", "## Case results", ""])
    for case in record["case_results"]:
        lines.extend([f"### {case['case_id']} — {case['case_status']}", ""])
        for criterion in case["criteria"]:
            lines.append(
                f"- **{criterion['criterion_id']}** — {criterion['status']}"
                f" (critical: {str(criterion['critical']).lower()}): {criterion['reason']}"
            )
            for evidence in criterion["evidence"]:
                lines.append(f"  - Evidence: {evidence}")
        lines.append("")
    regression = record.get("regression")
    if regression is not None:
        lines.extend(["## Regression comparison", ""])
        lines.append(f"Compared with previous run: {record.get('previous_run_id') or 'unknown'}")
        for key in ("new_failures", "resolved_failures", "changed", "unchanged", "new_criteria", "removed_criteria"):
            values = regression.get(key, [])
            lines.append(f"- **{key.replace('_', ' ').title()} ({len(values)}):** " + (", ".join(values) if values else "None"))
        lines.append("")
    lines.extend(["## Limitations", ""])
    lines.extend([f"- {item}" for item in record["limitations"]] or ["- None recorded."])
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="list discovered evaluation cases")
    parser.add_argument("--validate", action="store_true", help="validate all evaluation case files")
    parser.add_argument("--run", action="store_true", help="prepare an evidence-ready evaluation run")
    parser.add_argument("--run-id", help="explicit unique run identifier")
    parser.add_argument("--revision", help="target commit SHA or version label")
    parser.add_argument("--output", help="output JSON path; defaults to evals/results/<run-id>.json")
    parser.add_argument("--compare", help="previous run JSON file for regression comparison")
    args = parser.parse_args()
    previous_run = None
    if args.compare:
        previous_path = Path(args.compare)
        if not previous_path.is_absolute():
            previous_path = ROOT / previous_path
        try:
            previous_run = load_json(previous_path)
            if not isinstance(previous_run, dict) or not isinstance(previous_run.get("case_results"), list):
                raise ValueError("previous run must contain a case_results array")
            previous_errors = validate_instance(previous_run, load_json(RESULT_SCHEMA))
            if previous_errors:
                raise ValueError("previous run does not match the result schema: " + "; ".join(previous_errors[:5]))
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            print(f"ERROR: cannot read comparison run ({exc})")
            return 2
    cases, issues = inspect_cases()
    issues.extend(inspect_rubrics())
    if args.list:
        print_case_list(cases)
        return 0
    if args.validate or not args.run:
        for issue in issues:
            print(f"ERROR: {issue}")
        if not issues:
            print(f"Validated {len(cases)} evaluation case(s) against {CASE_SCHEMA.relative_to(ROOT)}.")
        return 1 if issues else 0
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}")
        print("Run not created because case validation failed.")
        return 1

    run_id = args.run_id or dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._-]*", run_id):
        print("ERROR: invalid run ID")
        return 2
    output = Path(args.output) if args.output else ROOT / "evals" / "results" / f"{run_id}.json"
    if not output.is_absolute():
        output = ROOT / output
    report_dir = ROOT / "evals" / "reports"
    report_path = report_dir / f"{run_id}.md"
    if output.exists() or report_path.exists():
        print(f"ERROR: refusing to overwrite existing run artifacts: {output} or {report_path}")
        return 2

    case_results: list[dict[str, Any]] = []
    flat_criteria: list[dict[str, Any]] = []
    integrity = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "validate_toolkit.py")],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    integrity_output = (integrity.stdout + integrity.stderr).strip()
    integrity_criterion = {
        "criterion_id": "toolkit-integrity",
        "status": "PASS" if integrity.returncode == 0 else "FAIL",
        "critical": True,
        "reason": "Full toolkit validator completed successfully." if integrity.returncode == 0 else "Full toolkit validator reported one or more integrity errors.",
        "evidence": [f"python tools/validate_toolkit.py (exit {integrity.returncode})", integrity_output or "No validator output."],
    }
    case_results.append({"case_id": "__toolkit__", "case_status": integrity_criterion["status"], "criteria": [integrity_criterion]})
    flat_criteria.append(integrity_criterion)
    for item in cases:
        data = item["data"]
        critical_ids = set(data.get("critical_behaviors", []))
        criteria = [{
            "criterion_id": "case-schema-valid",
            "status": "PASS",
            "critical": True,
            "reason": "Case JSON conforms to the repository evaluation-case schema.",
            "evidence": [str(item["path"].relative_to(ROOT))],
        }]
        for index, behavior in enumerate(data.get("expected_behaviors", []), start=1):
            criteria.append({
                "criterion_id": f"behavior-{index:02d}",
                "status": "NOT_RUN",
                "critical": f"behavior-{index:02d}" in critical_ids,
                "reason": "Behavioral grading requires an actual Codex session and reviewer evidence; this runner does not execute a model.",
                "evidence": [],
            })
        for index, prohibited in enumerate(data.get("must_not", []), start=1):
            criteria.append({
                "criterion_id": f"must-not-{index:02d}",
                "status": "NOT_RUN",
                "critical": f"must-not-{index:02d}" in critical_ids,
                "reason": "Prohibited-behavior review requires actual session evidence; no model behavior was executed.",
                "evidence": [],
            })
        case_status = overall_status(criteria)
        case_results.append({"case_id": data["id"], "case_status": case_status, "criteria": criteria})
        flat_criteria.extend(criteria)

    counts = {key: 0 for key in ("pass", "fail", "blocked", "not_run", "not_applicable")}
    for criterion in flat_criteria:
        key = criterion["status"].lower()
        counts[key] += 1
    status = overall_status(flat_criteria)
    current_index = {
        f"{case['case_id']}/{criterion['criterion_id']}": criterion["status"]
        for case in case_results for criterion in case["criteria"]
    }
    previous_index = {}
    if previous_run:
        previous_index = {
            f"{case.get('case_id')}/{criterion.get('criterion_id')}": criterion.get("status")
            for case in previous_run.get("case_results", [])
            for criterion in case.get("criteria", [])
        }
    regression = None
    if previous_run:
        regression = {
            "new_failures": sorted(k for k, value in current_index.items() if value == "FAIL" and previous_index.get(k) != "FAIL"),
            "resolved_failures": sorted(k for k, value in previous_index.items() if value == "FAIL" and current_index.get(k) == "PASS"),
            "changed": sorted(f"{k}: {previous_index[k]} -> {current_index[k]}" for k in set(current_index) & set(previous_index) if current_index[k] != previous_index[k]),
            "unchanged": sorted(k for k, value in current_index.items() if previous_index.get(k) == value),
            "new_criteria": sorted(set(current_index) - set(previous_index)),
            "removed_criteria": sorted(set(previous_index) - set(current_index)),
        }
    record = {
        "schema_version": "1.0",
        "run_id": run_id,
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
        "target": {"repository": "kuuriyawep/-gymsync-codex-toolkit", "revision": args.revision},
        "grader": "deterministic-runner",
        "overall_status": status,
        "case_results": case_results,
        "summary": counts,
        "limitations": [
            "This run validates evaluation case artifacts only; it does not execute Codex or an AI model.",
            "All behavioral criteria remain NOT_RUN until reviewed against a real Codex session and evidence.",
            "The runner implements the JSON Schema keywords used by this repository's schemas, not the entire JSON Schema specification.",
        ],
        "previous_run_id": previous_run.get("run_id") if previous_run else None,
        "regression": regression,
    }
    result_schema = load_json(RESULT_SCHEMA)
    result_errors = validate_instance(record, result_schema)
    if result_errors:
        for issue in result_errors:
            print(f"ERROR: generated result: {issue}")
        print("Run artifacts were not written because the generated record failed its schema.")
        return 1
    output.parent.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report_path.write_text(make_report(record), encoding="utf-8")
    print(f"Run record: {output}")
    print(f"Report: {report_path.relative_to(ROOT)}")
    print(f"Overall status: {status} (behavioral checks are NOT_RUN)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
