#!/usr/bin/env python3
"""Local append-only workflow ledger. Records state; never executes tasks."""
from __future__ import annotations

import argparse
import contextlib
import fnmatch
import hashlib
import json
import os
import re
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
sys.path.insert(0, str(ROOT / "tools"))
from evaluate_toolkit import validate_instance  # noqa: E402

ZERO_HASH = "0" * 64
WORKFLOW_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{2,63}$")
READ_ONLY_OWNERS = {"repo_explorer", "planner", "reviewer", "security_auditor"}
WRITE_OWNERS = {"implementer", "test_engineer"}
TEST_DIRS = {"tests", "test", "__tests__", "spec", "evals", "fixtures", "testing", "testdata"}
WORKFLOW_TRANSITIONS = {
    "INTAKE": {"TRIAGE", "NEEDS_CLARIFICATION", "BLOCKED", "CANCELLING"},
    "TRIAGE": {"DISCOVERY", "NEEDS_CLARIFICATION", "BLOCKED", "CANCELLING"},
    "DISCOVERY": {"PLANNING", "NEEDS_CLARIFICATION", "BLOCKED", "FAILED", "CANCELLING"},
    "PLANNING": {"APPROVAL", "EXECUTION", "NEEDS_CLARIFICATION", "BLOCKED", "FAILED", "CANCELLING"},
    "APPROVAL": {"EXECUTION", "AWAITING_APPROVAL", "BLOCKED", "CANCELLING"},
    "AWAITING_APPROVAL": {"APPROVAL", "BLOCKED", "CANCELLING"},
    "EXECUTION": {"VALIDATION", "AWAITING_APPROVAL", "BLOCKED", "FAILED", "CANCELLING"},
    "VALIDATION": {"EXECUTION", "REVIEW", "BLOCKED", "FAILED", "CANCELLING"},
    "REVIEW": {"EXECUTION", "COMPLETION", "BLOCKED", "FAILED", "CANCELLING"},
    "NEEDS_CLARIFICATION": {"TRIAGE", "BLOCKED", "CANCELLING"},
    "BLOCKED": {"DISCOVERY", "PLANNING", "APPROVAL", "EXECUTION", "CANCELLING"},
    "FAILED": {"DISCOVERY", "PLANNING", "CANCELLING"},
    "CANCELLING": {"CANCELLED", "BLOCKED"},
    "COMPLETION": set(), "CANCELLED": set(),
}
TASK_TRANSITIONS = {
    "pending": {"ready", "blocked", "cancelled"},
    "ready": {"active", "blocked", "cancelled"},
    "active": {"completed", "blocked", "failed", "cancelled"},
    "blocked": {"ready", "cancelled"},
    "failed": {"cancelled"},
    "completed": set(), "cancelled": set(),
}
EVENT_TYPES = {
    "workflow_created", "workflow_transitioned", "checkpoint_saved", "task_created",
    "task_transitioned", "approval_requested", "approval_granted", "approval_denied",
    "retry_recorded", "timeout_recorded", "cancellation_requested", "workflow_cancelled",
    "evidence_recorded", "validation_recorded", "review_recorded",
}


class LedgerError(Exception):
    pass


class LedgerCorrupt(LedgerError):
    pass


class LedgerLocked(LedgerError):
    pass


class SnapshotOutOfSync(LedgerError):
    pass


class IdempotencyConflict(LedgerError):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def safe_path(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip() or value.startswith("/") or "\\" in value:
        return False
    if len(value) > 1 and value[1] == ":":
        return False
    parts = [part for part in value.split("/") if part]
    return bool(parts) and not any(part in {".", ".."} for part in parts)


def is_test_path(value: str) -> bool:
    if not safe_path(value):
        return False
    parts = [part for part in value.split("/") if part]
    name = parts[-1].lower()
    return any(part in TEST_DIRS for part in parts) or name.startswith("test_") or name.endswith("_test.py") or ".test." in name or ".spec." in name


def scope_covers(approved: list[str], requested: list[str]) -> bool:
    return all(any(path == item or (item.endswith("/") and path.startswith(item)) or fnmatch.fnmatchcase(path, item)
                   for item in approved) for path in requested)


def schema_errors(value: Any, filename: str) -> list[str]:
    try:
        schema = json.loads((SCHEMA_DIR / filename).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot load {filename}: {exc}"]
    return validate_instance(value, schema)


def event_hash(event: dict[str, Any]) -> str:
    return hashlib.sha256((event["previous_hash"] + canonical(event)).encode("utf-8")).hexdigest()


class WorkflowLedger:
    def __init__(self, store: Path, workflow_id: str):
        if not isinstance(workflow_id, str) or not WORKFLOW_ID_RE.fullmatch(workflow_id):
            raise LedgerError("workflow_id must be a lowercase slug (3-64 characters)")
        self.store = store.expanduser().resolve()
        for parent in (self.store, *self.store.parents):
            if (parent / ".git").exists():
                raise LedgerError("workflow store must be outside all Git working trees")
        self.workflow_id = workflow_id
        self.directory = self.store / workflow_id
        self.events_path = self.directory / "events.jsonl"
        self.snapshot_path = self.directory / "snapshot.json"
        self.lock_path = self.directory / ".writer.lock"

    @contextlib.contextmanager
    def lock(self) -> Iterator[None]:
        self.store.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        if os.name != "nt":
            import stat
            for private_dir in (self.store, self.directory):
                if stat.S_IMODE(private_dir.stat().st_mode) & 0o077:
                    raise LedgerError(f"workflow store directory must be private (0700): {private_dir}")
        try:
            fd = os.open(self.lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError as exc:
            raise LedgerLocked("ledger writer lock exists; verify no writer is active before manual stale-lock removal") from exc
        try:
            with os.fdopen(fd, "w", encoding="ascii") as handle:
                handle.write(f"pid={os.getpid()}\n")
                handle.flush()
                os.fsync(handle.fileno())
            yield
        finally:
            try:
                self.lock_path.unlink()
            except FileNotFoundError:
                pass

    def read_events(self) -> list[dict[str, Any]]:
        if not self.events_path.exists():
            return []
        events = []
        try:
            with self.events_path.open("r", encoding="utf-8") as handle:
                for number, line in enumerate(handle, 1):
                    if not line.strip():
                        raise LedgerCorrupt(f"blank event line at {number}")
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError as exc:
                        raise LedgerCorrupt(f"invalid JSON at event line {number}: {exc}") from exc
        except OSError as exc:
            raise LedgerError(f"cannot read event log: {exc}") from exc
        return events

    def read_snapshot(self) -> dict[str, Any] | None:
        if not self.snapshot_path.exists():
            return None
        try:
            value = json.loads(self.snapshot_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise LedgerCorrupt(f"cannot read snapshot: {exc}") from exc
        if not isinstance(value, dict):
            raise LedgerCorrupt("snapshot root must be an object")
        return value

    def write_snapshot(self, snapshot: dict[str, Any]) -> None:
        self.directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        fd, temporary = tempfile.mkstemp(prefix=".snapshot-", suffix=".tmp", dir=self.directory)
        try:
            if hasattr(os, "fchmod"):
                os.fchmod(fd, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(json.dumps(snapshot, indent=2, sort_keys=True) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, self.snapshot_path)
            try:
                dir_fd = os.open(self.directory, os.O_RDONLY)
                try:
                    os.fsync(dir_fd)
                finally:
                    os.close(dir_fd)
            except OSError:
                pass
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    @staticmethod
    def task(snapshot: dict[str, Any], task_id: str) -> dict[str, Any]:
        for item in snapshot["tasks"]:
            if item["task_id"] == task_id:
                return item
        raise LedgerError(f"unknown task_id: {task_id}")

    @staticmethod
    def require_dependencies(snapshot: dict[str, Any], task: dict[str, Any]) -> None:
        for dep_id in task["depends_on"]:
            if WorkflowLedger.task(snapshot, dep_id)["state"] != "completed":
                raise LedgerError(f"task {task['task_id']} is waiting for dependency {dep_id}")

    def apply(self, snapshot: dict[str, Any] | None, event: dict[str, Any]) -> dict[str, Any]:
        kind, p, stamp = event["event_type"], event["payload"], event["timestamp"]

        if snapshot is not None and snapshot.get("state") in {"COMPLETION", "CANCELLED"}:
            raise LedgerError("terminal workflow cannot accept additional events")

        if kind == "workflow_created":
            if snapshot is not None or event["seq"] != 1:
                raise LedgerCorrupt("workflow_created must be the first event")
            snapshot = {
                "schema_version": "1.0.0", "workflow_id": self.workflow_id,
                "objective": p["objective"], "primary_workflow": p["primary_workflow"],
                "state": "INTAKE", "complexity": p["complexity"], "risk": p["risk"],
                "scope": p["scope"], "acceptance_criteria": p["acceptance_criteria"],
                "approval_required": p["approval_required"],
                "approval_status": "pending" if p["approval_required"] else "not-required",
                "approved_scope": [], "approval_reference": None,
                "review_required": p["review_required"], "validation_status": "pending",
                "review_status": "pending", "tasks": [],
                "checkpoint": {"summary": "Workflow created.", "next_action": "Triage the request.",
                               "evidence_refs": [], "blockers": []},
                "seq": 0, "last_event_hash": ZERO_HASH, "created_at": stamp, "updated_at": stamp,
            }
        elif snapshot is None:
            raise LedgerCorrupt("event log must start with workflow_created")

        elif kind == "workflow_transitioned":
            current, target = snapshot["state"], p["to_state"]
            if p["from_state"] != current:
                raise LedgerError(f"stale transition: expected {current}, received {p['from_state']}")
            if target not in WORKFLOW_TRANSITIONS[current]:
                raise LedgerError(f"illegal workflow transition: {current} -> {target}")
            if target == "EXECUTION" and snapshot["approval_required"] and snapshot["approval_status"] != "approved":
                raise LedgerError("workflow approval is required before execution")
            if target == "VALIDATION" and any(t["state"] != "completed" for t in snapshot["tasks"]):
                raise LedgerError("all workflow tasks must be completed before validation")
            if target == "REVIEW" and snapshot["validation_status"] != "passed":
                raise LedgerError("validation must pass before review")
            if target == "COMPLETION":
                if any(t["state"] != "completed" for t in snapshot["tasks"]):
                    raise LedgerError("workflow cannot complete while tasks remain incomplete")
                if snapshot["validation_status"] != "passed":
                    raise LedgerError("workflow cannot complete until validation passes")
                if snapshot["review_required"] and snapshot["review_status"] != "passed":
                    raise LedgerError("workflow cannot complete until required review passes")
            snapshot["state"] = target

        elif kind == "checkpoint_saved":
            snapshot["checkpoint"] = {
                "summary": p["summary"], "next_action": p["next_action"],
                "evidence_refs": p.get("evidence_refs", []), "blockers": p.get("blockers", []),
            }

        elif kind == "task_created":
            if snapshot["state"] not in {"INTAKE", "TRIAGE", "DISCOVERY", "PLANNING", "APPROVAL", "AWAITING_APPROVAL"}:
                raise LedgerError("tasks can only be added before execution")
            if any(t["task_id"] == p["task_id"] for t in snapshot["tasks"]):
                raise LedgerError(f"duplicate task_id: {p['task_id']}")
            if p["owner"] not in READ_ONLY_OWNERS | WRITE_OWNERS:
                raise LedgerError("task owner is not a canonical agent")
            read_scope, write_scope, deps = p.get("read_scope", []), p.get("write_scope", []), p.get("depends_on", [])
            if any(not safe_path(path) for path in read_scope + write_scope):
                raise LedgerError("task scopes must be safe repository-relative paths")
            if p["owner"] in READ_ONLY_OWNERS and write_scope:
                raise LedgerError(f"read-only agent {p['owner']} cannot own write_scope")
            if p["owner"] == "test_engineer" and any(not is_test_path(path) for path in write_scope):
                raise LedgerError("test_engineer may write test, fixture, or evaluation paths only")
            known = {t["task_id"] for t in snapshot["tasks"]}
            if set(deps) - known:
                raise LedgerError(f"dependencies must exist before this task: {sorted(set(deps) - known)}")
            # Overlapping writes are allowed only when the new task depends transitively on the existing owner.
            ancestors = set(deps)
            pending = list(deps)
            by_id = {t["task_id"]: t for t in snapshot["tasks"]}
            while pending:
                parent_id = pending.pop()
                for ancestor in by_id[parent_id]["depends_on"]:
                    if ancestor not in ancestors:
                        ancestors.add(ancestor)
                        pending.append(ancestor)
            for old in snapshot["tasks"]:
                overlap = any(a == b or a.startswith(b.rstrip("/") + "/") or b.startswith(a.rstrip("/") + "/")
                              or fnmatch.fnmatchcase(a, b) or fnmatch.fnmatchcase(b, a)
                              for a in write_scope for b in old["write_scope"])
                if overlap and old["task_id"] not in ancestors:
                    raise LedgerError(f"parallel write-scope overlap with task {old['task_id']}")
            approved_scope = p.get("approved_scope", [])
            approval_status = p["approval_status"]
            approval_ref = p.get("approval_reference")
            if write_scope and snapshot["approval_status"] == "approved" and scope_covers(snapshot["approved_scope"], write_scope):
                approval_status, approved_scope, approval_ref = "approved", snapshot["approved_scope"], snapshot["approval_reference"]
            if write_scope and approval_status == "approved":
                if not isinstance(approval_ref, str) or not approval_ref.strip():
                    raise LedgerError("approved write task requires approval_reference")
                if not scope_covers(approved_scope, write_scope):
                    raise LedgerError("task approved_scope must cover write_scope")
            state = "pending" if deps or (write_scope and approval_status != "approved") else "ready"
            snapshot["tasks"].append({
                "task_id": p["task_id"], "owner": p["owner"], "objective": p["task_objective"],
                "state": state, "read_scope": read_scope, "write_scope": write_scope, "depends_on": deps,
                "attempt": 0, "max_attempts": p["max_attempts"], "idempotent": p["idempotent"],
                "approval_status": approval_status, "approved_scope": approved_scope,
                "approval_reference": approval_ref, "evidence_refs": [], "summary": "",
                "next_action": "Await dependencies or approval." if state == "pending" else "Ready to start.",
            })

        elif kind == "task_transitioned":
            task = self.task(snapshot, p["task_id"])
            target = p["task_state"]
            if target not in TASK_TRANSITIONS[task["state"]]:
                raise LedgerError(f"illegal task transition: {task['state']} -> {target}")
            if target in {"ready", "active"}:
                self.require_dependencies(snapshot, task)
            if target == "active":
                if snapshot["state"] != "EXECUTION":
                    raise LedgerError("tasks may become active only while workflow state is EXECUTION")
                if task["write_scope"] and (task["approval_status"] != "approved" or not scope_covers(task["approved_scope"], task["write_scope"])):
                    raise LedgerError("write task cannot start without approval covering its write_scope")
                if task["attempt"] == 0:
                    task["attempt"] = 1
            if target == "completed" and not p.get("evidence_refs"):
                raise LedgerError("task completion requires evidence_refs")
            task["state"] = target
            task["summary"] = p.get("summary", task["summary"])
            task["next_action"] = p.get("next_action", task["next_action"])
            if p.get("evidence_refs"):
                task["evidence_refs"] = list(dict.fromkeys(task["evidence_refs"] + p["evidence_refs"]))

        elif kind in {"approval_requested", "approval_granted", "approval_denied"}:
            status = {"approval_requested": "pending", "approval_granted": "approved", "approval_denied": "denied"}[kind]
            task_id = p.get("task_id")
            target = self.task(snapshot, task_id) if task_id else snapshot
            if status == "pending":
                target["approved_scope"], target["approval_reference"] = [], None
            if status == "pending":
                target["approved_scope"], target["approval_reference"] = [], None
            if status == "approved":
                approved_scope, ref = p.get("approved_scope", []), p.get("approval_reference")
                if not isinstance(ref, str) or not ref.strip():
                    raise LedgerError("approval grant requires approval_reference")
                required = target["write_scope"] if task_id else [path for t in snapshot["tasks"] for path in t["write_scope"]]
                if not scope_covers(approved_scope, required):
                    raise LedgerError("approved_scope does not cover requested write paths")
                target["approved_scope"], target["approval_reference"] = approved_scope, ref
            elif status == "denied":
                target["approved_scope"], target["approval_reference"] = [], p.get("approval_reference")
            target["approval_status"] = status

        elif kind == "validation_recorded":
            if snapshot["state"] != "VALIDATION":
                raise LedgerError("validation evidence can only be recorded in VALIDATION state")
            if p["validation_status"] == "passed" and not p.get("evidence_refs"):
                raise LedgerError("passed validation requires evidence_refs")
            snapshot["validation_status"] = p["validation_status"]
            if p.get("evidence_refs"):
                snapshot["checkpoint"]["evidence_refs"] = list(dict.fromkeys(snapshot["checkpoint"]["evidence_refs"] + p["evidence_refs"]))

        elif kind == "review_recorded":
            if snapshot["state"] != "REVIEW":
                raise LedgerError("review evidence can only be recorded in REVIEW state")
            if p["review_status"] == "passed" and not p.get("evidence_refs"):
                raise LedgerError("passed review requires evidence_refs")
            snapshot["review_status"] = p["review_status"]
            if p.get("evidence_refs"):
                snapshot["checkpoint"]["evidence_refs"] = list(dict.fromkeys(snapshot["checkpoint"]["evidence_refs"] + p["evidence_refs"]))

        elif kind == "retry_recorded":
            task = self.task(snapshot, p["task_id"])
            if task["state"] != "failed":
                raise LedgerError("retry is allowed only for a failed task")
            if not p.get("retryable", False):
                raise LedgerError("task failure is not marked retryable")
            if task["attempt"] >= task["max_attempts"]:
                raise LedgerError("task retry limit reached")
            if not task["idempotent"] and not p.get("approval_reference"):
                raise LedgerError("non-idempotent retry requires explicit approval_reference")
            if task["write_scope"] and task["approval_status"] != "approved":
                raise LedgerError("write task approval is not active; obtain approval before retry")
            task["attempt"] += 1
            task["state"] = "ready"
            task["summary"] = p["reason"]
            task["next_action"] = "Retry explicitly; no automatic execution."
            if p.get("approval_reference"):
                task["approval_reference"] = p["approval_reference"]

        elif kind == "timeout_recorded":
            task_id = p.get("task_id")
            if task_id:
                task = self.task(snapshot, task_id)
                if task["state"] != "active":
                    raise LedgerError("task timeout requires an active task")
                task["state"] = "failed"
                task["summary"] = p["reason"]
                task["next_action"] = "Inspect timeout before any retry."
            if snapshot["state"] not in {"EXECUTION", "VALIDATION", "REVIEW"}:
                raise LedgerError("timeout can only be recorded during active workflow work")
            snapshot["state"] = "BLOCKED"
            snapshot["checkpoint"]["blockers"].append(p["reason"])

        elif kind == "cancellation_requested":
            if snapshot["state"] in {"COMPLETION", "CANCELLED"}:
                raise LedgerError("terminal workflow cannot be cancelled")
            snapshot["state"] = "CANCELLING"
            snapshot["checkpoint"]["blockers"].append(p["reason"])

        elif kind == "workflow_cancelled":
            if snapshot["state"] != "CANCELLING":
                raise LedgerError("workflow must be CANCELLING before CANCELLED")
            snapshot["state"] = "CANCELLED"
            for task in snapshot["tasks"]:
                if task["state"] not in {"completed", "cancelled"}:
                    task["state"] = "cancelled"

        elif kind == "evidence_recorded":
            refs, task_id = p["evidence_refs"], p.get("task_id")
            if task_id:
                task = self.task(snapshot, task_id)
                task["evidence_refs"] = list(dict.fromkeys(task["evidence_refs"] + refs))
            else:
                snapshot["checkpoint"]["evidence_refs"] = list(dict.fromkeys(snapshot["checkpoint"]["evidence_refs"] + refs))

        else:
            raise LedgerError(f"unsupported event type: {kind}")

        snapshot["seq"] = event["seq"]
        snapshot["last_event_hash"] = event["event_hash"]
        snapshot["updated_at"] = stamp
        errors = schema_errors(snapshot, "workflow-snapshot.schema.json")
        if errors:
            raise LedgerCorrupt("snapshot schema violation: " + "; ".join(errors))
        return snapshot

    def replay(self, events: list[dict[str, Any]]) -> dict[str, Any] | None:
        snapshot = None
        previous = ZERO_HASH
        keys: set[str] = set()
        for number, event in enumerate(events, 1):
            errors = schema_errors(event, "workflow-event.schema.json")
            if errors:
                raise LedgerCorrupt(f"event {number} schema violation: " + "; ".join(errors))
            if event["workflow_id"] != self.workflow_id or event["seq"] != number:
                raise LedgerCorrupt(f"event {number} has invalid workflow_id or sequence")
            if event["previous_hash"] != previous:
                raise LedgerCorrupt(f"event {number} previous_hash mismatch")
            expected = event_hash({k: v for k, v in event.items() if k != "event_hash"})
            if event["event_hash"] != expected:
                raise LedgerCorrupt(f"event {number} hash mismatch")
            key = event["idempotency_key"]
            if key in keys:
                raise LedgerCorrupt(f"duplicate idempotency key in event log: {key}")
            keys.add(key)
            snapshot = self.apply(snapshot, event)
            previous = event["event_hash"]
        return snapshot

    def append(self, kind: str, payload: dict[str, Any], actor: str, key: str) -> dict[str, Any]:
        if kind not in EVENT_TYPES:
            raise LedgerError(f"unsupported event type: {kind}")
        if not isinstance(actor, str) or len(actor.strip()) < 2:
            raise LedgerError("actor must contain at least two characters")
        if not isinstance(key, str) or len(key.strip()) < 8:
            raise LedgerError("idempotency_key must contain at least eight characters")
        with self.lock():
            events = self.read_events()
            current = self.replay(events)
            stored = self.read_snapshot()
            if events and stored != current:
                raise SnapshotOutOfSync("snapshot is missing or stale; run recover before writing")
            if not events and stored is not None:
                raise SnapshotOutOfSync("snapshot exists without an event log")
            for old in events:
                if old["idempotency_key"] == key:
                    if old["event_type"] == kind and old["payload"] == payload:
                        return old
                    raise IdempotencyConflict("idempotency key reused with a different event")
            previous = events[-1]["event_hash"] if events else ZERO_HASH
            event = {
                "schema_version": "1.0.0", "workflow_id": self.workflow_id, "seq": len(events) + 1,
                "event_id": uuid.uuid4().hex, "timestamp": now_iso(), "actor": actor,
                "event_type": kind, "idempotency_key": key, "previous_hash": previous, "payload": payload,
            }
            event["event_hash"] = event_hash(event)
            errors = schema_errors(event, "workflow-event.schema.json")
            if errors:
                raise LedgerError("event schema violation: " + "; ".join(errors))
            updated = self.apply(current, event)
            self.directory.mkdir(parents=True, exist_ok=True, mode=0o700)
            with self.events_path.open("a", encoding="utf-8") as handle:
                os.chmod(self.events_path, 0o600)
                handle.write(canonical(event) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            self.write_snapshot(updated)
            return event

    def create(self, *, objective: str, primary_workflow: str, scope: list[str],
               acceptance_criteria: list[str], complexity: str = "moderate", risk: str = "low",
               approval_required: bool = False, review_required: bool = True,
               actor: str = "codex-coordinator", idempotency_key: str) -> dict[str, Any]:
        if not scope or any(not safe_path(x) for x in scope):
            raise LedgerError("scope must contain safe repository-relative paths")
        if not acceptance_criteria:
            raise LedgerError("acceptance_criteria must not be empty")
        return self.append("workflow_created", {
            "objective": objective, "primary_workflow": primary_workflow, "scope": scope,
            "acceptance_criteria": acceptance_criteria, "complexity": complexity, "risk": risk,
            "approval_required": approval_required, "review_required": review_required,
        }, actor, idempotency_key)

    def transition(self, target: str, *, actor: str = "codex-coordinator",
                   idempotency_key: str, summary: str = "") -> dict[str, Any]:
        state = self.show()["state"]
        return self.append("workflow_transitioned", {"from_state": state, "to_state": target, "summary": summary},
                           actor, idempotency_key)

    def checkpoint(self, summary: str, next_action: str, *, evidence_refs: list[str] | None = None,
                   blockers: list[str] | None = None, actor: str = "codex-coordinator",
                   idempotency_key: str) -> dict[str, Any]:
        return self.append("checkpoint_saved", {"summary": summary, "next_action": next_action,
                           "evidence_refs": evidence_refs or [], "blockers": blockers or []}, actor, idempotency_key)

    def add_task(self, task_id: str, owner: str, objective: str, *, read_scope: list[str] | None = None,
                 write_scope: list[str] | None = None, depends_on: list[str] | None = None,
                 max_attempts: int = 1, idempotent: bool = True, approval_status: str = "not-required",
                 approved_scope: list[str] | None = None, approval_reference: str | None = None,
                 actor: str = "codex-coordinator", idempotency_key: str) -> dict[str, Any]:
        return self.append("task_created", {
            "task_id": task_id, "owner": owner, "task_objective": objective,
            "read_scope": read_scope or [], "write_scope": write_scope or [], "depends_on": depends_on or [],
            "max_attempts": max_attempts, "idempotent": idempotent, "approval_status": approval_status,
            "approved_scope": approved_scope or [], "approval_reference": approval_reference,
            "attempt": 0, "task_state": "pending", "evidence_refs": [], "summary": "",
            "next_action": "Await dependencies or approval.",
        }, actor, idempotency_key)

    def transition_task(self, task_id: str, target: str, *, evidence_refs: list[str] | None = None,
                        summary: str = "", next_action: str = "", actor: str = "codex-coordinator",
                        idempotency_key: str) -> dict[str, Any]:
        return self.append("task_transitioned", {"task_id": task_id, "task_state": target,
                           "evidence_refs": evidence_refs or [], "summary": summary, "next_action": next_action},
                           actor, idempotency_key)

    def approval(self, status: str, *, task_id: str | None = None, approved_scope: list[str] | None = None,
                 approval_reference: str | None = None, actor: str = "user",
                 idempotency_key: str) -> dict[str, Any]:
        kind = {"pending": "approval_requested", "approved": "approval_granted", "denied": "approval_denied"}.get(status)
        if kind is None:
            raise LedgerError("approval status must be pending, approved, or denied")
        payload: dict[str, Any] = {"approved_scope": approved_scope or []}
        if task_id:
            payload["task_id"] = task_id
        if approval_reference:
            payload["approval_reference"] = approval_reference
        return self.append(kind, payload, actor, idempotency_key)

    def record_validation(self, status: str, evidence_refs: list[str], *, summary: str = "",
                          actor: str = "codex-coordinator", idempotency_key: str) -> dict[str, Any]:
        return self.append("validation_recorded", {"validation_status": status, "evidence_refs": evidence_refs,
                           "summary": summary}, actor, idempotency_key)

    def record_review(self, status: str, evidence_refs: list[str], *, summary: str = "",
                      actor: str = "reviewer", idempotency_key: str) -> dict[str, Any]:
        return self.append("review_recorded", {"review_status": status, "evidence_refs": evidence_refs,
                           "summary": summary}, actor, idempotency_key)

    def retry_task(self, task_id: str, reason: str, *, approval_reference: str | None = None,
                   actor: str = "codex-coordinator", idempotency_key: str) -> dict[str, Any]:
        task = self.task(self.show(), task_id)
        return self.append("retry_recorded", {"task_id": task_id, "reason": reason,
                           "retryable": True, "idempotent": task["idempotent"],
                           "approval_reference": approval_reference}, actor, idempotency_key)

    def timeout(self, reason: str, *, task_id: str | None = None,
                actor: str = "codex-coordinator", idempotency_key: str) -> dict[str, Any]:
        payload = {"reason": reason}
        if task_id:
            payload["task_id"] = task_id
        return self.append("timeout_recorded", payload, actor, idempotency_key)

    def request_cancel(self, reason: str, *, actor: str = "user", idempotency_key: str) -> dict[str, Any]:
        return self.append("cancellation_requested", {"reason": reason}, actor, idempotency_key)

    def finish_cancel(self, reason: str, *, actor: str = "codex-coordinator", idempotency_key: str) -> dict[str, Any]:
        return self.append("workflow_cancelled", {"reason": reason}, actor, idempotency_key)

    def show(self) -> dict[str, Any]:
        snapshot = self.replay(self.read_events())
        if snapshot is None:
            raise LedgerError("workflow does not exist")
        return snapshot

    def resume(self) -> dict[str, Any]:
        valid, message = self.verify()
        if not valid:
            raise SnapshotOutOfSync(message)
        snapshot = self.show()
        snapshot["_resume_note"] = "State restored from verified ledger; no tasks were automatically executed."
        return snapshot

    @staticmethod
    def validate_schemas() -> list[str]:
        errors: list[str] = []
        for filename in ("workflow-event.schema.json", "workflow-snapshot.schema.json"):
            try:
                schema = json.loads((SCHEMA_DIR / filename).read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"cannot read {filename}: {exc}")
                continue
            if not isinstance(schema, dict) or schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("type") != "object":
                errors.append(f"{filename} must be a Draft 2020-12 object schema")
            elif not isinstance(schema.get("required"), list) or not isinstance(schema.get("properties"), dict):
                errors.append(f"{filename} must define required and properties")
            elif set(schema["required"]) - set(schema["properties"]):
                errors.append(f"{filename} required fields must be defined in properties")
        return errors

    def verify(self) -> tuple[bool, str]:
        events = self.read_events()
        if not events:
            return False, "event log is missing or empty"
        replayed = self.replay(events)
        stored = self.read_snapshot()
        if stored is None:
            return False, "snapshot is missing; run recover"
        if stored != replayed:
            return False, "snapshot differs from event replay; run recover"
        return True, f"verified {len(events)} events; head={replayed['last_event_hash']}"

    def recover(self) -> dict[str, Any]:
        with self.lock():
            events = self.read_events()
            if not events:
                raise LedgerError("cannot recover without an event log")
            snapshot = self.replay(events)
            self.write_snapshot(snapshot)
            return snapshot


def add_read_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--store", type=Path, required=True)
    parser.add_argument("--workflow-id", required=True)


def add_write_args(parser: argparse.ArgumentParser) -> None:
    add_read_args(parser)
    parser.add_argument("--actor", default="codex-coordinator")
    parser.add_argument("--idempotency-key", required=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create"); add_write_args(create)
    create.add_argument("--objective", required=True); create.add_argument("--primary-workflow", required=True)
    create.add_argument("--scope", action="append", required=True); create.add_argument("--acceptance", action="append", required=True)
    create.add_argument("--complexity", choices=["simple", "moderate", "complex"], default="moderate")
    create.add_argument("--risk", choices=["low", "medium", "high", "critical"], default="low")
    create.add_argument("--approval-required", action="store_true")
    create.add_argument("--review-required", action=argparse.BooleanOptionalAction, default=True)

    for name in ("show", "verify", "recover", "resume"):
        add_read_args(sub.add_parser(name))

    transition = sub.add_parser("transition"); add_write_args(transition)
    transition.add_argument("--to", choices=sorted(WORKFLOW_TRANSITIONS), required=True); transition.add_argument("--summary", default="")
    checkpoint = sub.add_parser("checkpoint"); add_write_args(checkpoint)
    checkpoint.add_argument("--summary", required=True); checkpoint.add_argument("--next-action", required=True)
    checkpoint.add_argument("--evidence-ref", action="append", default=[]); checkpoint.add_argument("--blocker", action="append", default=[])

    task_add = sub.add_parser("task-add"); add_write_args(task_add)
    task_add.add_argument("--task-id", required=True); task_add.add_argument("--owner", required=True); task_add.add_argument("--objective", required=True)
    task_add.add_argument("--read-scope", action="append", default=[]); task_add.add_argument("--write-scope", action="append", default=[])
    task_add.add_argument("--depends-on", action="append", default=[]); task_add.add_argument("--max-attempts", type=int, default=1)
    task_add.add_argument("--non-idempotent", action="store_true")

    task_move = sub.add_parser("task-transition"); add_write_args(task_move)
    task_move.add_argument("--task-id", required=True); task_move.add_argument("--to", choices=sorted(TASK_TRANSITIONS), required=True)
    task_move.add_argument("--evidence-ref", action="append", default=[]); task_move.add_argument("--summary", default="")
    task_move.add_argument("--next-action", default="")

    approval = sub.add_parser("approval"); add_write_args(approval)
    approval.add_argument("--status", choices=["pending", "approved", "denied"], required=True)
    approval.add_argument("--task-id"); approval.add_argument("--approved-scope", action="append", default=[])
    approval.add_argument("--approval-reference")

    for name in ("validation", "review"):
        p = sub.add_parser(name); add_write_args(p)
        p.add_argument("--status", choices=["pending", "passed", "failed", "skipped"], required=True)
        p.add_argument("--evidence-ref", action="append", default=[]); p.add_argument("--summary", default="")

    retry = sub.add_parser("retry"); add_write_args(retry)
    retry.add_argument("--task-id", required=True); retry.add_argument("--reason", required=True); retry.add_argument("--approval-reference")
    timeout = sub.add_parser("timeout"); add_write_args(timeout)
    timeout.add_argument("--task-id"); timeout.add_argument("--reason", required=True)
    for name in ("cancel-request", "cancel-finish"):
        p = sub.add_parser(name); add_write_args(p); p.add_argument("--reason", required=True)

    args = parser.parse_args()
    ledger = WorkflowLedger(args.store, args.workflow_id)
    try:
        if args.command == "create":
            result = ledger.create(objective=args.objective, primary_workflow=args.primary_workflow, scope=args.scope,
                acceptance_criteria=args.acceptance, complexity=args.complexity, risk=args.risk,
                approval_required=args.approval_required, review_required=args.review_required,
                actor=args.actor, idempotency_key=args.idempotency_key)
        elif args.command == "show":
            result = ledger.show()
        elif args.command == "resume":
            result = ledger.resume()
        elif args.command == "verify":
            valid, message = ledger.verify(); print(message); return 0 if valid else 1
        elif args.command == "recover":
            result = ledger.recover()
        elif args.command == "transition":
            result = ledger.transition(args.to, actor=args.actor, idempotency_key=args.idempotency_key, summary=args.summary)
        elif args.command == "checkpoint":
            result = ledger.checkpoint(args.summary, args.next_action, evidence_refs=args.evidence_ref,
                blockers=args.blocker, actor=args.actor, idempotency_key=args.idempotency_key)
        elif args.command == "task-add":
            result = ledger.add_task(args.task_id, args.owner, args.objective, read_scope=args.read_scope,
                write_scope=args.write_scope, depends_on=args.depends_on, max_attempts=args.max_attempts,
                idempotent=not args.non_idempotent, actor=args.actor, idempotency_key=args.idempotency_key)
        elif args.command == "task-transition":
            result = ledger.transition_task(args.task_id, args.to, evidence_refs=args.evidence_ref,
                summary=args.summary, next_action=args.next_action, actor=args.actor, idempotency_key=args.idempotency_key)
        elif args.command == "approval":
            result = ledger.approval(args.status, task_id=args.task_id, approved_scope=args.approved_scope,
                approval_reference=args.approval_reference, actor=args.actor, idempotency_key=args.idempotency_key)
        elif args.command == "validation":
            result = ledger.record_validation(args.status, args.evidence_ref, summary=args.summary,
                actor=args.actor, idempotency_key=args.idempotency_key)
        elif args.command == "review":
            result = ledger.record_review(args.status, args.evidence_ref, summary=args.summary,
                actor=args.actor, idempotency_key=args.idempotency_key)
        elif args.command == "retry":
            result = ledger.retry_task(args.task_id, args.reason, approval_reference=args.approval_reference,
                actor=args.actor, idempotency_key=args.idempotency_key)
        elif args.command == "timeout":
            result = ledger.timeout(args.reason, task_id=args.task_id, actor=args.actor, idempotency_key=args.idempotency_key)
        elif args.command == "cancel-request":
            result = ledger.request_cancel(args.reason, actor=args.actor, idempotency_key=args.idempotency_key)
        else:
            result = ledger.finish_cancel(args.reason, actor=args.actor, idempotency_key=args.idempotency_key)
    except LedgerError as exc:
        print(f"ERROR: {exc}", file=sys.stderr); return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
