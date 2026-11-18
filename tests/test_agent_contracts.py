from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_agent_contracts", ROOT / "tools" / "validate_agent_contracts.py"
)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def handoff(role="repo_explorer", write_scope=None, approval_status="not-required"):
    write_scope = write_scope or []
    return {
        "schema_version": "1.0.0",
        "handoff_id": "H-audit-repo",
        "task": "Audit the repository structure",
        "recipient": role,
        "objective": "Map the relevant architecture and report evidence.",
        "scope": {"in_scope": ["src/"], "out_of_scope": ["production data"]},
        "context": {"evidence": [{"path": "AGENTS.md", "note": "Project instructions"}], "assumptions": [], "unknowns": []},
        "approval": {
            "status": approval_status,
            "approved_scope": list(write_scope) if approval_status == "approved" else [],
            "approval_reference": "user-approved-task-123" if approval_status == "approved" else None
        },
        "constraints": {
            "mode": "scoped-write" if write_scope else "read-only",
            "permission_profile": "repo-readonly" if role != "implementer" else "approved-scoped-write",
            "write_scope": list(write_scope),
            "no_go_actions": ["deploy", "delete production data"]
        },
        "expected_output": {"format": "markdown", "required_sections": ["Findings", "Evidence"]},
        "dependencies": {"blocked_by": [], "parallel_safe": False}
    }


def result(role="repo_explorer", changed=None, check_status="passed", evidence=None):
    return {
        "schema_version": "1.0.0",
        "handoff_id": "H-audit-repo",
        "agent": role,
        "outcome": "complete",
        "summary": "Repository audit completed with evidence.",
        "work_performed": [{"description": "Inspected project instructions.", "evidence_refs": ["AGENTS.md"]}],
        "findings": [],
        "changed_files": changed or [],
        "checks": [{"name": "Read-only inspection", "status": check_status, "evidence_refs": evidence if evidence is not None else ["AGENTS.md"]}],
        "risks": [],
        "next_action": "Parent coordinator reviews the evidence.",
        "approval_needed": False
    }


def task(task_id, owner="repo_explorer", reads=None, writes=None, deps=None, approved=False):
    writes = writes or []
    return {
        "id": task_id,
        "owner": owner,
        "objective": f"Complete task {task_id}",
        "read_scope": reads or [],
        "write_scope": writes,
        "depends_on": deps or [],
        "approval_status": "approved" if approved else "not-required",
        "approved_scope": list(writes) if approved else [],
        "approval_reference": "user-approved-task-123" if approved else None,
        "state": "ready"
    }


def graph(tasks):
    return {"schema_version": "1.0.0", "graph_id": "sample-graph", "max_parallel_tasks": 3, "tasks": tasks}


class HandoffContractTests(unittest.TestCase):
    def test_readonly_handoff_is_valid(self):
        self.assertEqual(validator.validate_handoff(handoff()), [])

    def test_readonly_role_cannot_receive_write_scope(self):
        errors = validator.validate_handoff(handoff("reviewer", ["src/main.py"], "approved"))
        self.assertTrue(any("must be read-only" in e for e in errors))

    def test_implementer_pending_approval_is_a_valid_non_executable_handoff(self):
        self.assertEqual(validator.validate_handoff(handoff("implementer", ["src/main.py"], "pending")), [])

    def test_empty_in_scope_is_rejected(self):
        data = handoff()
        data["scope"]["in_scope"] = []
        self.assertTrue(any("non-empty in_scope" in e for e in validator.validate_handoff(data)))

    def test_missing_required_handoff_field_is_rejected(self):
        data = handoff()
        del data["objective"]
        self.assertTrue(any("objective" in e for e in validator.validate_handoff(data)))

    def test_malformed_recipient_does_not_crash(self):
        data = handoff()
        data["recipient"] = []
        self.assertTrue(any("recipient must name" in e for e in validator.validate_handoff(data)))

    def test_approved_write_scope_must_cover_requested_paths(self):
        data = handoff("implementer", ["src/main.py"], "approved")
        data["approval"]["approved_scope"] = ["src/other.py"]
        self.assertTrue(any("must cover every requested write path" in e for e in validator.validate_handoff(data)))


class AgentResultTests(unittest.TestCase):
    def test_readonly_agent_cannot_return_changed_files(self):
        errors = validator.validate_result(result(changed=["src/main.py"]), handoff())
        self.assertTrue(any("cannot report changed_files" in e for e in errors))

    def test_implementer_cannot_change_unapproved_file(self):
        errors = validator.validate_result(
            result("implementer", ["src/other.py"]),
            handoff("implementer", ["src/main.py"], "approved")
        )
        self.assertTrue(any("exceed the approved write_scope" in e for e in errors))

    def test_passed_check_requires_evidence(self):
        errors = validator.validate_result(result(evidence=[]), handoff())
        self.assertTrue(any("passed status requires evidence_refs" in e for e in errors))

    def test_missing_result_summary_is_rejected(self):
        data = result()
        del data["summary"]
        self.assertTrue(any("summary" in e for e in validator.validate_result(data, handoff())))

    def test_malformed_changed_files_is_rejected_without_crashing(self):
        data = result()
        data["changed_files"] = {"unexpected": "object"}
        self.assertTrue(any("changed_files must be an array" in e for e in validator.validate_result(data, handoff())))

    def test_result_must_match_handoff_recipient(self):
        errors = validator.validate_result(result("planner"), handoff())
        self.assertTrue(any("does not match handoff recipient" in e for e in errors))


class TaskGraphTests(unittest.TestCase):
    def test_disjoint_parallel_tasks_are_valid(self):
        data = graph([
            task("inspect-api", reads=["api/"]),
            task("inspect-ui", reads=["ui/"])
        ])
        self.assertEqual(validator.validate_task_graph(data), [])

    def test_dependency_cycle_is_rejected(self):
        data = graph([
            task("a", deps=["b"]),
            task("b", deps=["a"])
        ])
        self.assertTrue(any("dependency cycle" in e for e in validator.validate_task_graph(data)))

    def test_parallel_overlapping_writes_are_rejected(self):
        data = graph([
            task("edit-one", "implementer", writes=["src/shared/types.ts"], approved=True),
            task("edit-two", "implementer", writes=["src/shared/types.ts"], approved=True)
        ])
        self.assertTrue(any("parallel write-scope overlap" in e for e in validator.validate_task_graph(data)))

    def test_overlapping_writes_are_allowed_when_sequenced(self):
        data = graph([
            task("edit-one", "implementer", writes=["src/shared/types.ts"], approved=True),
            task("edit-two", "implementer", writes=["src/shared/types.ts"], deps=["edit-one"], approved=True)
        ])
        self.assertEqual(validator.validate_task_graph(data), [])

    def test_write_task_requires_user_approval(self):
        data = graph([task("edit-one", "implementer", writes=["src/main.py"])])
        self.assertTrue(any("requires approval_status=approved" in e for e in validator.validate_task_graph(data)))

    def test_readonly_role_cannot_own_write_task(self):
        data = graph([task("edit-one", "reviewer", writes=["src/main.py"], approved=True)])
        self.assertTrue(any("cannot own write_scope" in e for e in validator.validate_task_graph(data)))

    def test_malformed_owner_does_not_crash(self):
        data = graph([task("inspect")])
        data["tasks"][0]["owner"] = []
        self.assertTrue(any("owner is not an existing agent" in e for e in validator.validate_task_graph(data)))

    def test_unknown_dependency_is_rejected(self):
        data = graph([task("inspect", deps=["missing"])])
        self.assertTrue(any("unknown task" in e for e in validator.validate_task_graph(data)))


if __name__ == "__main__":
    unittest.main()
