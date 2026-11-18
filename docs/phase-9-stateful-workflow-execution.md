# Phase 9 — Stateful Workflow Execution

**Status:** IMPLEMENTATION COMPLETE — local append-only ledger, hash-chain, state/approval/task gates, explicit recovery, and deterministic tests are implemented. Latest CI passed 117 tests; live Codex behavior remains deferred to Phase 11.  
**Date:** 2026-11-18  
**Inputs:** [Workflow orchestration skill](../.agents/skills/workflow-orchestration/SKILL.md), [Workflow brief](../templates/workflow-brief.md), [Agent task graph schema](../schemas/agent-task-graph.schema.json), [Phase 8 handoff/result contracts](../docs/phase-8-agent-capability-audit.md)

## 1. Existing behavior and gap

The current orchestration skill already defines primary session states and a Markdown workflow brief. The project checkpoint is version-controlled Markdown, and project-memory validation checks structure and freshness.

These are useful but distinct:
- Session states are in-memory guidance, not a durable execution ledger.
- `templates/workflow-brief.md` is a handoff/checkpoint document, not an event log.
- `PROJECT_STATE.md` is the durable project-level checkpoint, not a per-workflow task ledger.
- The Phase 8 task graph validates dependency/ownership structure but does not persist task transitions, retries, approvals, or recovery events.

Phase 9 adds a small local append-only workflow ledger. It does not replace Codex, Project Intelligence, the Phase 8 task graph, or the project-level checkpoint.

## 2. Design principles

1. **Codex remains the only coordinator.** The ledger records state; it does not spawn agents or autonomously execute tasks.
2. **Event log is the source of truth.** The snapshot is a rebuildable projection of the ordered event log.
3. **Single writer.** Only the parent coordinator writes a workflow ledger. Agents return results; they do not mutate the ledger directly.
4. **Explicit transitions.** Invalid transitions are rejected; terminal states cannot silently reopen.
5. **Idempotent commands.** Every mutation has a caller-supplied idempotency key. Duplicate identical requests are no-ops; conflicting reuse is an error.
6. **Approval is scoped.** An approval event records the exact approved scope/reference. No write/external task can start from pending/denied approval.
7. **Evidence references, not raw output.** Store paths, commit IDs, CI run URLs, test IDs, and artifact references; do not store raw tool output, secrets, or full transcripts by default.
8. **Recovery is explicit.** Rebuild the snapshot from a valid event chain after interruption. Never mark interrupted work complete.
9. **Local and private by default.** Runtime ledgers live outside Git tracking. No external database, cloud service, or background daemon is required.

## 3. Workflow state machine

Primary states:
`INTAKE → TRIAGE → DISCOVERY → PLANNING → APPROVAL → EXECUTION → VALIDATION → REVIEW → COMPLETION`

Additional states:
`NEEDS_CLARIFICATION`, `AWAITING_APPROVAL`, `BLOCKED`, `FAILED`, `CANCELLING`, `CANCELLED`.

| From | Allowed next states |
|---|---|
| INTAKE | TRIAGE, NEEDS_CLARIFICATION, BLOCKED, CANCELLED |
| TRIAGE | DISCOVERY, NEEDS_CLARIFICATION, BLOCKED, CANCELLED |
| DISCOVERY | PLANNING, NEEDS_CLARIFICATION, BLOCKED, FAILED, CANCELLED |
| PLANNING | APPROVAL, EXECUTION, NEEDS_CLARIFICATION, BLOCKED, FAILED, CANCELLED |
| APPROVAL | EXECUTION, AWAITING_APPROVAL, BLOCKED, CANCELLED |
| AWAITING_APPROVAL | APPROVAL, BLOCKED, CANCELLED |
| EXECUTION | VALIDATION, AWAITING_APPROVAL, BLOCKED, FAILED, CANCELLING |
| VALIDATION | EXECUTION, REVIEW, BLOCKED, FAILED, CANCELLING |
| REVIEW | EXECUTION, COMPLETION, BLOCKED, FAILED, CANCELLING |
| NEEDS_CLARIFICATION | TRIAGE, BLOCKED, CANCELLED |
| BLOCKED | DISCOVERY, PLANNING, APPROVAL, EXECUTION, CANCELLING |
| FAILED | DISCOVERY, PLANNING, CANCELLING |
| CANCELLING | CANCELLED, BLOCKED |
| COMPLETION | Terminal |
| CANCELLED | Terminal |

Transition gates:
- A workflow with `approval_required=true` cannot enter EXECUTION unless `approval_status=approved` and the approved scope covers the task write scope.
- COMPLETION requires all tasks completed, `validation_status=passed`, and `review_status=passed` when review is required.
- FAILED, BLOCKED, AWAITING_APPROVAL, CANCELLING, and CANCELLED are never reported as complete.
- Reopening completed/cancelled work requires a new workflow ID and a new event chain.

## 4. Task states and retries

Task states:
`pending → ready → active → completed`, with side states `blocked`, `failed`, and `cancelled`.

| From | Allowed next states |
|---|---|
| pending | ready, blocked, cancelled |
| ready | active, blocked, cancelled |
| active | completed, blocked, failed, cancelled |
| blocked | ready, cancelled |
| failed | retry event to ready, or cancelled |
| completed | Terminal |
| cancelled | Terminal |

- A task becomes ready only after all dependencies are completed.
- A task may become active only when its approval and write-scope requirements are satisfied.
- A task completion event requires evidence references.
- Retry is explicit and bounded by `max_attempts`.
- Non-idempotent tasks are not automatically retried. A manual retry requires a new approval reference or a documented recovery decision.
- A timeout records a timeout event and moves the task/workflow to a non-complete state; it never implies success.

## 5. Event ledger and snapshot

Proposed local layout:

```text
<private-workflow-store>/
  <workflow-id>/
    events.jsonl
    snapshot.json
```

- `events.jsonl` is append-only and hash chained. The chain is tamper-evident, not digitally signed; an actor with write access to the full store could recompute it.
- Each event has sequence number, event ID, timestamp, actor, event type, idempotency key, previous hash, minimal payload, and event hash.
- `snapshot.json` is an atomically replaced projection containing current state, tasks, approval status, checkpoint, sequence number, and last event hash.
- POSIX store/workflow directories must be private (mode `0700`) and ledger/lock files are created with restrictive permissions. On Windows, filesystem ACLs remain authoritative.
- On startup/resume, verify the event chain and compare the snapshot to a replayed projection.
- If the event chain is valid but the snapshot is stale/missing, rebuild it from events.
- If the event chain is corrupt or has a sequence gap, stop and report BLOCKED; do not silently repair or truncate.

The store must be outside this toolkit repository and Git tracking, e.g. a user-selected path under `~/.codex/workflow-state/gymsync-codex-toolkit/`. The CLI requires an explicit `--store` path and rejects paths inside this repository. Do not commit live workflow logs into this public repository. The tool does not create a cloud service or write to production.

## 6. Event types

- `workflow_created`
- `workflow_transitioned`
- `checkpoint_saved`
- `task_created`
- `task_transitioned`
- `approval_requested`
- `approval_granted`
- `approval_denied`
- `retry_recorded`
- `timeout_recorded`
- `cancellation_requested`
- `workflow_cancelled`
- `evidence_recorded`
- `validation_recorded`
- `review_recorded`

Events contain concise metadata and references. They do not store full terminal output, full agent transcripts, environment variables, credentials, or raw production records.

## 7. Interruption and recovery behavior

| Interruption point | Recovery behavior |
|---|---|
| Before event append | No mutation; retry with same idempotency key |
| After event append, before snapshot update | Replay event log and rebuild snapshot |
| Duplicate command after successful append | Return existing event/result; do not apply twice |
| Same idempotency key with different payload | Reject as conflict |
| Corrupt hash chain or sequence gap | BLOCKED; preserve files and require manual investigation |
| Agent process stops mid-task | Keep task active/blocked; record interruption; never auto-complete |
| Timeout | Record timeout, increment bounded attempt only on explicit retry |
| Cancellation during execution | Enter CANCELLING, stop new work, record partial effects, then CANCELLED or BLOCKED |
| Approval denied | Keep write/external task blocked; no side effect |
| Missing evidence for completion | Reject completion transition |

## 8. Privacy and retention

- Default store contains summaries, scopes, event metadata, and evidence references only.
- No secrets, tokens, raw command output, customer records, or full chat transcripts.
- Evidence links may point to private artifacts; ledger does not copy their contents.
- User controls retention and deletion of the local store.
- The validator checks structural and hash-chain integrity, not the truth of evidence.

## 9. CLI usage

Choose a private local store outside the repository:

```bash
STORE="$HOME/.codex/workflow-state/gymsync-codex-toolkit"
python tools/workflow_ledger.py create --store "$STORE" --workflow-id toolkit-phase9 --objective "Implement stateful workflow execution" --primary-workflow "toolkit-development" --scope docs/ --scope tools/ --acceptance "Ledger tests pass" --acceptance "CI passes" --idempotency-key create-phase9-0001
python tools/workflow_ledger.py verify --store "$STORE" --workflow-id toolkit-phase9
python tools/workflow_ledger.py resume --store "$STORE" --workflow-id toolkit-phase9
```

`resume` verifies the event log and snapshot, then returns the restored state. It does not launch agents or execute pending tasks. If the snapshot is missing/stale, use `recover` only after the event chain verifies.

## 10. Implementation sequence

1. Freeze state names and transition table. **Complete.**
2. Add event and snapshot schemas. **Complete.**
3. Implement deterministic ledger with append, replay, hash-chain verification, idempotency, atomic snapshot update, and explicit recovery. **Complete in initial implementation.**
4. Add task/approval/checkpoint operations and completion gates. **Complete in initial implementation.**
5. Add tests for legal/illegal transitions, duplicate keys, hash corruption, snapshot rebuild, interruption, retries, cancellation, private-store boundaries, and no false completion. **Initial deterministic suite complete (117 tests across toolkit); broader evaluation continues in Phase 10.**
6. Integrate ledger validation and commands into the workflow-orchestration skill and templates. **Complete.**
7. Run full CI. **Complete:** all 10 substantive quality-gate steps passed. Real Codex end-to-end workflow execution remains NOT_RUN until Phase 11.

## 11. Non-goals

- No autonomous agent runtime or scheduler.
- No n8n/CrewAI/Hermes/OpenCode.
- No database/cloud persistence.
- No automatic tool execution or external side effects.
- No replacement for `PROJECT_STATE.md` or Project Intelligence.


## 12. Phase 9 closeout

Phase 9 implementation is complete at the repository level.

- Append-only event log and hash-chain verification.
- Rebuildable atomic snapshot and explicit recovery.
- Unique idempotency keys and stale-snapshot protection.
- Workflow/task state transitions, dependency gates, scoped approvals, and completion gates.
- Retry limits, non-idempotent retry approval, timeout, and two-stage cancellation.
- Private local store outside Git worktrees; restrictive POSIX permissions.
- Resume verifies state and does not execute pending work.
- Main toolkit validation includes workflow schema checks.
- Native/portable workflow skill and workflow brief template are synchronized.

<badge>CI verified</badge> GitHub Actions [run #44297943897](https://github.com/kuuriyawep/-gymsync-codex-toolkit/actions/runs/44297943897) passed all 10 substantive steps for commit `6f4069dc65314bf4057e7b545d9d1958b22f67d5`; 117 unit tests passed.

This is deterministic code/contract validation, not live Codex workflow execution or a proof of behavior under concurrent real agents. Phase 11 owns that runtime validation.

## 13. Next phase — Phase 10: Evaluation & Reliability

Audit the 13 canonical skills, all current evaluation cases and rubrics, and the new Phase 7–9 contracts. Remove duplicates, identify missing cases, score static skill quality with evidence, add recovery/adversarial/permission/delegation cases, and measure context/output fidelity. Keep behavioral execution clearly marked NOT_RUN until Phase 11.
