---
name: workflow-orchestration
description: Coordinate non-trivial Codex engineering work by selecting the existing toolkit workflow, maintaining session state, and managing bounded agent handoffs.
---
# Workflow Orchestration

## When to use
Use for non-trivial engineering tasks, multi-step repository work, cross-discipline changes, or tasks where risk assessment, workflow selection, delegation, or session checkpoints improve reliability.

For trivial, local, reversible work, use a lightweight path. Do not force a full orchestration ceremony onto every request.

## Authority and boundaries
- Codex is the primary coordinator and remains accountable for the final result.
- The user's explicit request and repository `AGENTS.md` are authoritative.
- `workflows/registry.md` owns task classification, risk/complexity definitions, routing, and agent role boundaries.
- The selected workflow file owns its detailed procedure. Relevant skills own their specialist procedures.
- This skill coordinates those sources; it does not duplicate them, create another runtime, or grant permissions.
- Session state exists only in the active Codex session unless an explicit persistence mechanism is separately configured.

## Procedure
1. **Intake:** Extract the objective, expected outcome, scope, constraints, non-goals, target repository, and approvals already given for this exact task. Inspect available context before asking questions.
2. **Route:** Use `workflows/registry.md` to select one primary category and workflow. Assess complexity and risk separately using the registry. Record secondary concerns only when they add real requirements.
3. **Discover and plan:** Read the selected workflow and matching skill procedures. Inspect repository instructions and relevant evidence. For non-trivial work, define acceptance criteria, scope, dependencies, owners, verification, and rollback/recovery where relevant.
4. **Select execution mode:** Decide whether Codex should work alone or use an existing specialist. Delegate only when the specialist adds material value and the task has a bounded, verifiable deliverable. Parallelize only independent tasks with non-overlapping ownership; sequence dependent work and shared-file edits.
5. **Handoff:** For meaningful delegation, use `templates/agent-handoff.md`. State objective, owner, scope, non-goals, evidence, assumptions, approval status, constraints, expected output, and dependencies. Assign one accountable owner per task.
6. **Approval:** Apply the selected workflow and repository rules. Stop before unapproved destructive/irreversible operations, production writes, migrations, permission changes, deployment, external side effects, or material scope expansion. Approval is specific to the stated action.
7. **Coordinate:** Track each task as pending, active, completed, blocked, or failed in the active session. Validate specialist outputs against source evidence and acceptance criteria. Resolve conflicting findings using reproducible evidence; preserve unresolved disagreement rather than hiding it.
8. **Review and verify:** Follow the selected workflow's review and verification gates. Use an independent read-only reviewer for complex, security-sensitive, or high-impact changes when available.
9. **Report:** State classification, selected workflow, complexity/risk, scope and approval, owners/handoffs, changed files, checks and evidence, review outcome, blockers, and unresolved risks. Distinguish partial completion from verified completion.

## Session checkpoint
Maintain only the state needed to resume safely: current workflow/state, scope, acceptance criteria, decisions, approvals, owners, completed steps, evidence, blockers, and next action. Use `templates/workflow-brief.md` for complex tasks or durable handoffs; avoid paperwork for small tasks.

Primary states:
`INTAKE` → `TRIAGE` → `DISCOVERY` → `PLANNING` → `APPROVAL` → `EXECUTION` → `VALIDATION` → `REVIEW` → `COMPLETION`

Use `NEEDS_CLARIFICATION`, `AWAITING_APPROVAL`, `BLOCKED`, or `FAILED` when applicable. Do not advance past a failed gate as if it passed. Completion requires the selected workflow's required evidence; otherwise report partial or blocked status.

## Stop conditions
Stop or report a blocker when material ambiguity changes the solution, required approval is absent, ownership is unclear, required evidence/tooling is unavailable, or a safety boundary cannot be maintained. Continue only safe read-only discovery while waiting.

## Required output
For non-trivial tasks, leave a session-visible summary of:
- Objective, primary category, and selected workflow.
- Complexity/risk and rationale.
- Scope, acceptance criteria, assumptions, and approval state.
- Execution mode, owners, and handoffs.
- Current state, completed work, and evidence.
- Verification/review results, blockers, and unresolved issues.
