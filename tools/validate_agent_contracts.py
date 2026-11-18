#!/usr/bin/env python3
"""Validate agent handoffs, results, and dependency graphs without spawning agents."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
sys.path.insert(0, str(ROOT / "tools"))
from evaluate_toolkit import validate_instance  # noqa: E402
READ_ONLY_ROLES = {"repo_explorer", "planner", "reviewer", "security_auditor"}
WRITE_ROLES = {"implementer", "test_engineer"}
TEST_ONLY_ROLES = {"test_engineer"}
TEST_PATH_PARTS = {"tests", "test", "__tests__", "spec", "evals", "fixtures", "testing", "testdata"}
ROLES = READ_ONLY_ROLES | WRITE_ROLES
SCHEMA_FILES = ("agent-handoff.schema.json", "agent-result.schema.json", "agent-task-graph.schema.json")
TASK_GRAPH_EXAMPLE = ROOT / "templates" / "agent-task-graph.json"
REQUIRED_DOCS = ("docs/phase-8-agent-capability-audit.md", "references/agent-tool-access-matrix.md", "templates/agent-result.md", "templates/agent-task-graph.json")


def _schema_errors(value: Any, filename: str) -> list[str]:
    try:
        schema = json.loads((SCHEMA_DIR / filename).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot load {filename}: {exc}"]
    return [f"{filename}: {issue}" for issue in validate_instance(value, schema)]


def _strings(value: Any, *, nonempty: bool = False) -> bool:
    return isinstance(value, list) and (not nonempty or bool(value)) and all(isinstance(item, str) and item.strip() for item in value)


def _is_test_path(path: Any) -> bool:
    if not isinstance(path, str) or not path.strip() or path.startswith("/") or "\\" in path:
        return False
    parts = [part for part in path.split("/") if part]
    if not parts or any(part in {".", ".."} for part in parts):
        return False
    filename = parts[-1].lower()
    return any(part in TEST_PATH_PARTS for part in parts) or filename.startswith("test_") or filename.endswith("_test.py") or ".test." in filename or ".spec." in filename


def _covers(approved: list[str], requested: list[str]) -> bool:
    return all(path in approved for path in requested)


def validate_handoff(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["handoff must be an object"]
    errors.extend(_schema_errors(data, "agent-handoff.schema.json"))
    if data.get("schema_version") != "1.0.0":
        errors.append("handoff schema_version must be 1.0.0")
    if not isinstance(data.get("handoff_id"), str) or not data["handoff_id"].startswith("H-"):
        errors.append("handoff_id must start with H-")
    role = data.get("recipient")
    if not isinstance(role, str) or role not in ROLES:
        errors.append("recipient must name an existing canonical agent")
    scope = data.get("scope")
    if not isinstance(scope, dict) or not _strings(scope.get("in_scope"), nonempty=True) or not _strings(scope.get("out_of_scope"), nonempty=True):
        errors.append("scope must define non-empty in_scope and out_of_scope string arrays")
    approval = data.get("approval")
    constraints = data.get("constraints")
    if not isinstance(approval, dict) or not isinstance(constraints, dict):
        errors.append("approval and constraints objects are required")
        return errors
    status = approval.get("status")
    if not isinstance(status, str) or status not in {"not-required", "pending", "approved", "denied"}:
        errors.append("approval.status is invalid")
    approved_scope = approval.get("approved_scope", [])
    if not _strings(approved_scope) and approved_scope != []:
        errors.append("approval.approved_scope must be an array of strings")
        approved_scope = []
    write_scope = constraints.get("write_scope", [])
    if not _strings(write_scope) and write_scope != []:
        errors.append("constraints.write_scope must be an array of strings")
        write_scope = []
    mode = constraints.get("mode")
    if not isinstance(mode, str) or mode not in {"read-only", "scoped-write"}:
        errors.append("constraints.mode is invalid")
    if isinstance(role, str) and role in READ_ONLY_ROLES and (write_scope or mode != "read-only"):
        errors.append(f"{role} handoffs must be read-only with an empty write_scope")
    if isinstance(role, str) and role in WRITE_ROLES and write_scope and mode != "scoped-write":
        errors.append(f"{role} with write_scope must use scoped-write mode")
    if isinstance(role, str) and role in TEST_ONLY_ROLES and any(not _is_test_path(path) for path in write_scope):
        errors.append("test_engineer write_scope may contain test files, fixtures, or evaluation cases only")
    if status == "approved":
        if not isinstance(approval.get("approval_reference"), str) or not approval["approval_reference"].strip():
            errors.append("approved handoff requires approval_reference")
        if not _covers(approved_scope, write_scope):
            errors.append("approved_scope must cover every requested write path")
    elif write_scope and isinstance(role, str) and role in WRITE_ROLES:
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
    errors.extend(_schema_errors(result, "agent-result.schema.json"))
    if result.get("schema_version") != "1.0.0":
        errors.append("result schema_version must be 1.0.0")
    if result.get("handoff_id") != handoff.get("handoff_id"):
        errors.append("result handoff_id does not match its handoff")
    role = handoff.get("recipient")
    if result.get("agent") != role:
        errors.append("result agent does not match handoff recipient")
    changed_files = result.get("changed_files", [])
    if not _strings(changed_files) and changed_files != []:
        errors.append("changed_files must be an array of file paths")
        changed_files = []
    if isinstance(role, str) and role in READ_ONLY_ROLES and changed_files:
        errors.append(f"read-only role {role} cannot report changed_files")
    constraints = handoff.get("constraints", {})
    allowed_writes = constraints.get("write_scope", []) if isinstance(constraints, dict) else []
    approval = handoff.get("approval", {})
    if not isinstance(approval, dict):
        approval = {}
    if changed_files:
        if not isinstance(role, str) or role not in WRITE_ROLES:
            errors.append("only approved write roles may return changed files under current role policy")
        if isinstance(role, str) and role in TEST_ONLY_ROLES and any(not _is_test_path(path) for path in changed_files):
            errors.append("test_engineer changed_files must remain inside test/fixture/evaluation paths")
        if approval.get("status") != "approved":
            errors.append("changed files require an approved handoff")
        if not isinstance(allowed_writes, list) or not _covers(allowed_writes, changed_files):
            errors.append("changed_files exceed the approved write_scope")
    checks = result.get("checks", [])
    if not isinstance(checks, list):
        errors.append("checks must be an array")
    else:
        for i, check in enumerate(checks):
            if not isinstance(check, dict):
                errors.append(f"checks[{i}] must be an object")
                continue
            if check.get("status") == "passed" and not _strings(check.get("evidence_refs"), nonempty=True):
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
    errors.extend(_schema_errors(data, "agent-task-graph.schema.json"))
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
        if not isinstance(owner, str) or owner not in ROLES:
            errors.append(f"tasks[{i}].owner is not an existing agent")
        read_scope = task.get("read_scope", [])
        write_scope = task.get("write_scope", [])
        deps = task.get("depends_on", [])
        if not _strings(read_scope) and read_scope != []:
            errors.append(f"tasks[{i}].read_scope must be an array of strings")
            read_scope = []
        if not _strings(write_scope) and write_scope != []:
            errors.append(f"tasks[{i}].write_scope must be an array of strings")
            write_scope = []
        if not _strings(deps) and deps != []:
            errors.append(f"tasks[{i}].depends_on must be an array of task IDs")
            deps = []
        task["read_scope"] = read_scope
        task["write_scope"] = write_scope
        task["depends_on"] = deps
        if isinstance(owner, str) and owner in READ_ONLY_ROLES and write_scope:
            errors.append(f"read-only owner {owner} cannot own write_scope")
        if write_scope:
            if not isinstance(owner, str) or owner not in WRITE_ROLES:
                errors.append(f"owner {owner} is not authorized for write tasks")
            if isinstance(owner, str) and owner in TEST_ONLY_ROLES and any(not _is_test_path(path) for path in write_scope):
                errors.append(f"test_engineer task {tid} may write test/fixture/evaluation paths only")
            if task.get("approval_status") != "approved":
                errors.append(f"write task {tid} requires approval_status=approved")
            approved_scope = task.get("approved_scope", [])
            if not _strings(approved_scope) or not _covers(approved_scope, write_scope):
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
                          for a in left.get("write_scope", []) if isinstance(a, str)
                          for b in right.get("write_scope", []) if isinstance(b, str))
            if not overlap:
                continue
            sequential = left_id in ancestor_map[right_id] or right_id in ancestor_map[left_id]
            if not sequential:
                errors.append(f"parallel write-scope overlap between {left_id} and {right_id}")
    return errors


def validate_files() -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_DOCS:
        if not (ROOT / relative).is_file():
            errors.append(f"required agent contract document is missing: {relative}")
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
        elif set(schema["required"]) - set(schema["properties"]):
            errors.append(f"{filename} required fields must all be defined in properties")
    if TASK_GRAPH_EXAMPLE.is_file():
        try:
            example = json.loads(TASK_GRAPH_EXAMPLE.read_text(encoding="utf-8"))
            errors.extend(f"agent task graph example: {issue}" for issue in validate_task_graph(example))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"cannot read agent task graph example: {exc}")
    return errors


if __name__ == "__main__":
    issues = validate_files()
    for issue in issues:
        print(f"ERROR: {issue}")
    if issues:
        raise SystemExit(1)
    print("Agent contract schema files are valid JSON and have object roots.")
