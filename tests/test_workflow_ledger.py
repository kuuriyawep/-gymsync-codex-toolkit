from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("workflow_ledger", ROOT / "tools" / "workflow_ledger.py")
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)
WorkflowLedger = module.WorkflowLedger
LedgerError = module.LedgerError
LedgerCorrupt = module.LedgerCorrupt
IdempotencyConflict = module.IdempotencyConflict
SnapshotOutOfSync = module.SnapshotOutOfSync


class WorkflowLedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.ledger = WorkflowLedger(Path(self.temp.name), "sample-workflow")
        self.ledger.create(objective="Implement a bounded sample workflow.", primary_workflow="feature-delivery",
            scope=["src/", "tests/"], acceptance_criteria=["Tests pass", "Review passes"],
            approval_required=True, review_required=True, idempotency_key="create-sample-01")

    def tearDown(self):
        self.temp.cleanup()

    def to_approval(self):
        for state in ["TRIAGE", "DISCOVERY", "PLANNING", "APPROVAL"]:
            self.ledger.transition(state, idempotency_key=f"state-{state.lower()}-01")

    def approve_workflow(self):
        self.ledger.approval("approved", approved_scope=["src/", "tests/"],
            approval_reference="user-approval-001", idempotency_key="workflow-approval-01")

    def enter_execution(self):
        self.to_approval()
        self.approve_workflow()
        self.ledger.transition("EXECUTION", idempotency_key="workflow-execution-01")

    def test_create_is_idempotent_with_same_key_and_payload(self):
        event = self.ledger.create(objective="Implement a bounded sample workflow.", primary_workflow="feature-delivery",
            scope=["src/", "tests/"], acceptance_criteria=["Tests pass", "Review passes"],
            approval_required=True, review_required=True, idempotency_key="create-sample-01")
        self.assertEqual(event["seq"], 1)
        self.assertEqual(self.ledger.show()["seq"], 1)

    def test_store_inside_toolkit_repository_is_rejected(self):
        with self.assertRaises(LedgerError):
            WorkflowLedger(ROOT / ".codex" / "workflow-state", "invalid-store")

    def test_create_persists_event_and_snapshot(self):
        snapshot = self.ledger.show()
        self.assertEqual(snapshot["state"], "INTAKE")
        self.assertEqual(snapshot["seq"], 1)
        self.assertEqual(snapshot["approval_status"], "pending")
        self.assertTrue(self.ledger.verify()[0])

    def test_illegal_transition_is_rejected(self):
        with self.assertRaises(LedgerError):
            self.ledger.transition("EXECUTION", idempotency_key="illegal-execution-01")

    def test_execution_requires_approval(self):
        self.to_approval()
        self.ledger.transition("AWAITING_APPROVAL", idempotency_key="await-approval-01")
        with self.assertRaises(LedgerError):
            self.ledger.transition("EXECUTION", idempotency_key="premature-execution-01")

    def test_approval_grant_unlocks_execution(self):
        self.enter_execution()
        self.assertEqual(self.ledger.show()["state"], "EXECUTION")

    def test_idempotent_duplicate_is_noop(self):
        first = self.ledger.checkpoint("Known state", "Continue triage", idempotency_key="checkpoint-0001")
        second = self.ledger.checkpoint("Known state", "Continue triage", idempotency_key="checkpoint-0001")
        self.assertEqual(first["event_id"], second["event_id"])
        self.assertEqual(self.ledger.show()["seq"], 2)

    def test_conflicting_idempotency_reuse_is_rejected(self):
        self.ledger.checkpoint("Known state", "Continue", idempotency_key="checkpoint-0002")
        with self.assertRaises(IdempotencyConflict):
            self.ledger.checkpoint("Different state", "Other", idempotency_key="checkpoint-0002")

    def test_task_dependencies_and_task_approval_gate(self):
        self.ledger.add_task("inspect", "repo_explorer", "Inspect source", read_scope=["src/"],
                             idempotency_key="task-inspect-001")
        self.ledger.add_task("implement", "implementer", "Implement source", read_scope=["src/"],
                             write_scope=["src/main.py"], depends_on=["inspect"], idempotency_key="task-implement-001")
        self.enter_execution()
        with self.assertRaises(LedgerError):
            self.ledger.transition_task("implement", "active", idempotency_key="task-implement-active-01")
        self.ledger.transition_task("inspect", "active", idempotency_key="task-inspect-active-01")
        self.ledger.transition_task("inspect", "completed", evidence_refs=["commit:abc123"],
                                    idempotency_key="task-inspect-done-01")
        self.ledger.approval("approved", task_id="implement", approved_scope=["src/main.py"],
            approval_reference="user-approval-002", idempotency_key="task-approval-01")
        self.ledger.transition_task("implement", "ready", idempotency_key="task-implement-ready-01")
        self.ledger.transition_task("implement", "active", idempotency_key="task-implement-active-02")
        self.ledger.transition_task("implement", "completed", evidence_refs=["test:unit-01"],
                                    idempotency_key="task-implement-done-01")
        self.assertEqual(module.WorkflowLedger.task(self.ledger.show(), "implement")["state"], "completed")

    def test_tasks_cannot_activate_outside_execution(self):
        self.ledger.add_task("inspect", "repo_explorer", "Inspect source", idempotency_key="task-outside-01")
        with self.assertRaises(LedgerError):
            self.ledger.transition_task("inspect", "active", idempotency_key="task-outside-02")

    def test_task_completion_requires_evidence(self):
        self.ledger.add_task("inspect", "repo_explorer", "Inspect source", idempotency_key="task-evidence-01")
        self.enter_execution()
        self.ledger.transition_task("inspect", "active", idempotency_key="task-evidence-02")
        with self.assertRaises(LedgerError):
            self.ledger.transition_task("inspect", "completed", idempotency_key="task-evidence-03")

    def test_test_engineer_is_restricted_to_test_paths(self):
        with self.assertRaises(LedgerError):
            self.ledger.add_task("bad-tests", "test_engineer", "Edit source", write_scope=["src/main.py"],
                                 idempotency_key="test-scope-bad-01")
        self.ledger.add_task("good-tests", "test_engineer", "Add tests", write_scope=["tests/test_main.py"],
                             approval_status="approved", approved_scope=["tests/test_main.py"],
                             approval_reference="user-approval-003", idempotency_key="test-scope-good-01")
        self.enter_execution()
        self.assertEqual(module.WorkflowLedger.task(self.ledger.show(), "good-tests")["state"], "ready")

    def test_parallel_overlapping_write_scopes_are_rejected(self):
        self.ledger.add_task("write-a", "implementer", "Edit shared module", write_scope=["src/shared.py"],
                             approval_status="approved", approved_scope=["src/shared.py"],
                             approval_reference="user-approval-004", idempotency_key="write-overlap-a")
        with self.assertRaises(LedgerError):
            self.ledger.add_task("write-b", "implementer", "Edit same module", write_scope=["src/shared.py"],
                                 approval_status="approved", approved_scope=["src/shared.py"],
                                 approval_reference="user-approval-005", idempotency_key="write-overlap-b")

    def test_overlapping_writes_are_allowed_when_sequenced(self):
        self.ledger.add_task("write-a", "implementer", "Edit shared module", write_scope=["src/shared.py"],
                             approval_status="approved", approved_scope=["src/shared.py"],
                             approval_reference="user-approval-006", idempotency_key="write-sequence-a")
        self.ledger.add_task("write-b", "implementer", "Update shared module tests", write_scope=["src/shared.py"],
                             depends_on=["write-a"], approval_status="approved", approved_scope=["src/shared.py"],
                             approval_reference="user-approval-007", idempotency_key="write-sequence-b")
        self.assertEqual(len(self.ledger.show()["tasks"]), 2)

    def test_completion_requires_all_gates(self):
        self.enter_execution()
        self.ledger.transition("VALIDATION", idempotency_key="to-validation-01")
        with self.assertRaises(LedgerError):
            self.ledger.transition("REVIEW", idempotency_key="premature-review-01")
        self.ledger.record_validation("passed", ["ci:run-100"], idempotency_key="validation-pass-01")
        self.ledger.transition("REVIEW", idempotency_key="to-review-01")
        with self.assertRaises(LedgerError):
            self.ledger.transition("COMPLETION", idempotency_key="premature-complete-01")
        self.ledger.record_review("passed", ["review:report-1"], idempotency_key="review-pass-01")
        self.ledger.transition("COMPLETION", idempotency_key="complete-01")
        self.assertEqual(self.ledger.show()["state"], "COMPLETION")

    def test_passed_validation_requires_evidence(self):
        self.enter_execution()
        self.ledger.transition("VALIDATION", idempotency_key="to-validation-02")
        with self.assertRaises(LedgerError):
            self.ledger.record_validation("passed", [], idempotency_key="validation-no-evidence")

    def test_non_idempotent_retry_requires_manual_approval_reference(self):
        self.ledger.add_task("publish", "implementer", "Publish artifact", write_scope=["dist/"],
            approval_status="approved", approved_scope=["dist/"], approval_reference="user-approval-008",
            idempotent=False, max_attempts=2, idempotency_key="publish-task-01")
        self.to_approval()
        self.ledger.approval("approved", approved_scope=["src/", "tests/", "dist/"],
            approval_reference="user-approval-publish", idempotency_key="workflow-approval-publish")
        self.ledger.transition("EXECUTION", idempotency_key="workflow-execution-publish")
        self.ledger.transition_task("publish", "active", idempotency_key="publish-active-01")
        self.ledger.transition_task("publish", "failed", summary="Network timeout", idempotency_key="publish-failed-01")
        with self.assertRaises(LedgerError):
            self.ledger.retry_task("publish", "Retry publish", idempotency_key="retry-no-approval-01")
        self.ledger.retry_task("publish", "Manual retry approved", approval_reference="user-approval-009",
                               idempotency_key="retry-approved-01")
        task = module.WorkflowLedger.task(self.ledger.show(), "publish")
        self.assertEqual(task["attempt"], 2)
        self.assertEqual(task["state"], "ready")

    def test_timeout_moves_workflow_to_blocked(self):
        self.enter_execution()
        self.ledger.timeout("Time budget exceeded", idempotency_key="timeout-01")
        self.assertEqual(self.ledger.show()["state"], "BLOCKED")

    def test_cancellation_is_two_phase_and_terminal(self):
        self.ledger.request_cancel("User stopped work", idempotency_key="cancel-request-01")
        self.assertEqual(self.ledger.show()["state"], "CANCELLING")
        self.ledger.finish_cancel("Stopped safely", idempotency_key="cancel-finish-01")
        self.assertEqual(self.ledger.show()["state"], "CANCELLED")
        with self.assertRaises(LedgerError):
            self.ledger.transition("TRIAGE", idempotency_key="cancel-reopen-01")

    def test_hash_chain_detects_tampering(self):
        lines = self.ledger.events_path.read_text(encoding="utf-8").splitlines()
        event = json.loads(lines[0]); event["payload"]["objective"] = "tampered"
        lines[0] = json.dumps(event)
        self.ledger.events_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        with self.assertRaises(LedgerCorrupt):
            self.ledger.show()

    def test_recover_rebuilds_missing_snapshot(self):
        self.ledger.checkpoint("Checkpoint", "Continue", idempotency_key="recover-checkpoint-01")
        self.ledger.snapshot_path.unlink()
        valid, message = self.ledger.verify()
        self.assertFalse(valid); self.assertIn("snapshot is missing", message)
        snapshot = self.ledger.recover()
        self.assertEqual(snapshot["seq"], 2)
        self.assertTrue(self.ledger.verify()[0])

    def test_stale_snapshot_blocks_writes_until_recovery(self):
        self.ledger.checkpoint("Checkpoint", "Continue", idempotency_key="stale-checkpoint-01")
        snapshot = json.loads(self.ledger.snapshot_path.read_text(encoding="utf-8"))
        snapshot["state"] = "COMPLETION"
        self.ledger.snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")
        with self.assertRaises(SnapshotOutOfSync):
            self.ledger.checkpoint("Next", "Continue", idempotency_key="stale-checkpoint-02")
        self.ledger.recover()
        self.assertTrue(self.ledger.verify()[0])

    def test_existing_lock_blocks_concurrent_writer(self):
        self.ledger.lock_path.write_text("pid=123\n", encoding="ascii")
        with self.assertRaises(module.LedgerLocked):
            self.ledger.checkpoint("Checkpoint", "Next", idempotency_key="lock-test-01")


if __name__ == "__main__":
    unittest.main()
