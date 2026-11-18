#!/usr/bin/env python3
"""Validate agent handoffs, results, and dependency graphs without spawning agents."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
READ_ONLY_ROLES = {"repo_explorer", "planner", "reviewer", "security_auditor"}
WRITE_ROLES = {"implementer"}
ROLES = READ_ONLY_ROLES | WRITE_ROLES
SCHEMA_FILES = ("agent-handoff.schema.json", "agent-result.schema.json", "agent-task-graph.schema.json")


def _strings(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value)


def _covers(approved: list[str], requested: list[str]) -> bool:
    return all(path in approved for path in requested)


def validate_handoff(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["handoff must be an object"]
    if data.get("schema_version") != "1.0.0":
        errors.append("handoff schema_version must be 1.0.0")
    if not isinstance(data.get("handoff_id"), str) or not data["handoff_id"].startswith("H-"):
        errors.append("handoff_id must start with H-")
    role = data.get("recipient")
    if role not in ROLES:
        errors.append("recipient must name an existing canonical agent")
    scope = data.get("scope")
    if not isinstance(scope, dict) or not _strings(scope.get("in_scope")) or not _strings(scope.get("out_of_scope")):
        errors.append("scope must define non-empty in_scope and out_of_scope string arrays")
    approval = data.get("approval")
    constraints = data.get("constraints")
    if not isinstance(approval, dict) or not isinstance(constraints, dict):
        errors.append("approval and constraints objects are required")
        return errors
    status = approval.get("status")
    if status not in {"not-required", "pending", "approved", "denied"}:
        errors.append("approval.status is invalid")
    approved_scope = approval.get("approved_scope", [])
    if not _strings(approved_scope) and approved_scope != []:
        errors.append("approval.approved_scope must be an array of strings")
    write_scope = constraints.get("write_scope", [])
    if not _strings(write_scope) and write_scope != []:
        errors.append("constraints.write_scope must be an array of strings")
    mode = constraints.get("mode")
    if mode not in {"read-only", "scoped-write"}:
        errors.append("constraints.mode is invalid")
    if role in READ_ONLY_ROLES and (write_scope or mode != "read-only"):
        errors.append(f"{role} handoffs must be read-only with an empty write_scope")
    if role == "implementer" and write_scope and mode != "scoped-write":
        errors.append("implementer with write_scope must use scoped-write mode")
    if status == "approved":
        if not isinstance(approval.get("approval_reference"), str) or not approval["approval_reference"].strip():
            errors.append("approved handoff requires approval_reference")
        if not _covers(approved_scope, write_scope):
            errors.append("approved_scope must cover every requested write path")
    elif write_scope and role == "implementer":
        # A proposed handoff may be pending, but it must not be treated as executable.
        if status == "not-required":
            errors.append("implementer write_scope cannot be marked not-required")
    if status == "denied" and write_scope:
        errors.append("denied handoff cannot retain an executable write_scope")
    return errors


def validate_result(result: Any, handoff: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(result, dict):
        return ["agent result must be an object"]
    if result.get("schema_version") != "1.0.0":
        errors.append("result schema_version must be 1.0.0")
    if result.get("handoff_id") != handoff.get("handoff_id"):
        errors.append("result handoff_id does not match its handoff")
    role = handoff.get("recipient")
    if result.get("agent") != role:
        errors.append("result agent does not match handoff recipient")
    if role in READ_ONLY_ROLES and result.get("changed_files"):
        errors.append(f"read-only role {role} cannot report changed_files")
    allowed_writes = handoff.get("constraints", {}).get("write_scope", [])
    approval = handoff.get("approval", {})
    if result.get("changed_files"):
        if role != "implementer":
            errors.append("only implementer may return changed files under current role policy")
        if approval.get("status") != "approved":
            errors.append("changed files require an approved handoff")
        if not _covers(allowed_writes, result["changed_files"]):
            errors.append("changed_files exceed the approved write_scope")
    checks = result.get("checks", [])
    if not isinstance(checks, list):
        errors.append("checks must be an array")
    else:
        for i, check in enumerate(checks):
            if not isinstance(check, dict):
                errors.append(f"checks[{i}] must be an object")
                continue
            if check.get("status") == "passed" and not _strings(check.get("evidence_refs")):
                errors.append(f"checks[{i}] passed status requires evidence_refs")
    if result.get("approval_needed") and result.get("outcome") == "complete":
        errors.append("result cannot be complete while approval_needed is true")
    return errors


def _scope_overlaps(left: str, right: str) -> bool:
    import fnmatch
    if left == right or fnmatch.fnmatchcase(left, right) or fnmatch.fnmatchcase(right, left):
        return True
    left_clean = left.rstrip("/")
    right_clean = right.rstrip("/")
    return left_clean.startswith(right_clean + "/") or right_clean.startswith(left_clean + "/")


def validate_task_graph(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["task graph must be an object"]
    tasks = data.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        return ["task graph tasks must be a non-empty array"]
    if not isinstance(data.get("max_parallel_tasks"), int) or isinstance(data.get("max_parallel_tasks"), bool) or not 1 <= data["max_parallel_tasks"] <= 8:
        errors.append("max_parallel_tasks must be an integer from 1 to 8")

    by_id: dict[str, dict[str, Any]] = {}
    for i, task in enumerate(tasks):
        if not isinstance(task, dict):
            errors.append(f"tasks[{i}] must be an object")
            continue
        tid = task.get("id")
        if not isinstance(tid, str) or not tid:
            errors.append(f"tasks[{i}].id must be a non-empty string")
            continue
        if tid in by_id:
            errors.append(f"duplicate task id: {tid}")
        by_id[tid] = task
        owner = task.get("owner")
        if owner not in ROLES:
            errors.append(f"tasks[{i}].owner is not an existing agent")
        read_scope = task.get("read_scope", [])
        write_scope = task.get("write_scope", [])
        deps = task.get("depends_on", [])
        if not _strings(read_scope) and read_scope != []:
            errors.append(f"tasks[{i}].read_scope must be an array of strings")
        if not _strings(write_scope) and write_scope != []:
            errors.append(f"tasks[{i}].write_scope must be an array of strings")
        if not _strings(deps) and deps != []:
            errors.append(f"tasks[{i}].depends_on must be an array of task IDs")
        if owner in READ_ONLY_ROLES and write_scope:
            errors.append(f"read-only owner {owner} cannot own write_scope")
        if write_scope:
            if owner not in WRITE_ROLES:
                errors.append(f"owner {owner} is not authorized for write tasks")
            if task.get("approval_status") != "approved":
                errors.append(f"write task {tid} requires approval_status=approved")
            if not _covers(task.get("approved_scope", []), write_scope):
                errors.append(f"write task {tid} exceeds approved_scope")
            if not isinstance(task.get("approval_reference"), str) or not task["approval_reference"].strip():
                errors.append(f"write task {tid} requires approval_reference")
        if tid in deps:
            errors.append(f"task {tid} cannot depend on itself")

    for tid, task in by_id.items():
        for dep in task.get("depends_on", []) if isinstance(task.get("depends_on", []), list) else []:
            if dep not in by_id:
                errors.append(f"task {tid} depends on unknown task {dep}")

    # Detect dependency cycles using DFS coloring.
    colors: dict[str, int] = {tid: 0 for tid in by_id}
    def visit(tid: str) -> None:
        if colors[tid] == 1:
            errors.append(f"dependency cycle detected at task {tid}")
            return
        if colors[tid] == 2:
            return
        colors[tid] = 1
        for dep in by_id[tid].get("depends_on", []) if isinstance(by_id[tid].get("depends_on", []), list) else []:
            if dep in by_id:
                visit(dep)
        colors[tid] = 2
    for tid in by_id:
        visit(tid)

    def ancestors(tid: str, seen: set[str] | None = None) -> set[str]:
        seen = seen or set()
        for dep in by_id.get(tid, {}).get("depends_on", []):
            if dep in by_id and dep not in seen:
                seen.add(dep)
                ancestors(dep, seen)
        return seen

    ids = list(by_id)
    ancestor_map = {tid: ancestors(tid) for tid in ids}
    for i, left_id in enumerate(ids):
        left = by_id[left_id]
        for right_id in ids[i + 1:]:
            right = by_id[right_id]
            overlap = any(_scope_overlaps(a, b)
                          for a in left.get("write_scope", [])
                          for b in right.get("write_scope", []))
            if not overlap:
                continue
            sequential = left_id in ancestor_map[right_id] or right_id in ancestor_map[left_id]
            if not sequential:
                errors.append(f"parallel write-scope overlap between {left_id} and {right_id}")
    return errors


def validate_files() -> list[str]:
    errors: list[str] = []
    for filename in SCHEMA_FILES:
        path = SCHEMA_DIR / filename
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"cannot read valid {filename}: {exc}")
            continue
        if not isinstance(schema, dict) or schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("type") != "object":
            errors.append(f"{filename} must be a Draft 2020-12 object schema")
        elif not isinstance(schema.get("required"), list) or not isinstance(schema.get("properties"), dict):
            errors.append(f"{filename} must define required and properties")
    return errors


if __name__ == "__main__":
    issues = validate_files()
    for issue in issues:
        print(f"ERROR: {issue}")
    if issues:
        raise SystemExit(1)
    print("Agent contract schema files are valid JSON and have object roots.")
