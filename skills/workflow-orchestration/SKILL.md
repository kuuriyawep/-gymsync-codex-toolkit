---
name: workflow-orchestration
description: Classify engineering requests, assess complexity and risk, route work to the existing toolkit workflows and skills, coordinate bounded agent handoffs, and enforce approval and verification gates in Codex sessions.
---
# Workflow Orchestration

## Mission and authority

Use this skill to select and coordinate the repository's existing engineering procedures. Codex remains the primary orchestrator and execution host. This skill does not create a separate runtime, task database, agent framework, or permission boundary.

- Treat the user's explicit request and the repository's `AGENTS.md` as authoritative.
- Reuse existing workflows, skills, and agents; do not duplicate their detailed procedures here.
- Keep task state in the active Codex session. Do not imply that state persists across sessions.
- Use `workflows/registry.md` as the routing index and follow the selected workflow as the procedure of record.
- Keep work within the approved scope. This skill does not grant approval for deployment, production writes, destructive actions, or external side effects.

## When to use

Use for non-trivial engineering requests, multi-step repository work, tasks spanning multiple disciplines, or whenever workflow selection, risk assessment, delegation, or explicit state tracking would improve reliability.

For trivial, local, reversible requests, use adaptive lightweight routing rather than forcing every phase of a full workflow.

## Operating procedure

### 1. Intake

Extract the following from the request and current session:

- Objective and expected outcome.
- Explicit scope, constraints, and non-goals.
- Target repository, component, environment, and affected users when known.
- User-stated deadlines or ordering constraints.
- Existing decisions and approvals relevant to this exact task.

Do not invent missing requirements. Ask one focused clarification when an unknown materially changes the route, safety, or expected behavior.

### 2. Triage

Classify the primary task using the categories in `workflows/registry.md`. For mixed tasks, identify one primary workflow and list secondary concerns rather than starting several overlapping workflows.

Assess **complexity** and **risk separately**:

- Complexity: `simple`, `moderate`, or `complex`.
- Risk: `low`, `medium`, `high`, or `critical`.

Complexity estimates coordination and technical effort. Risk estimates potential impact, reversibility, sensitivity, and blast radius. A small change can still be high risk.

Use the definitions and override rules in the workflow registry. Record the evidence or assumptions behind non-obvious classifications. If uncertainty could conceal a high-impact operation, choose the safer route until clarified.

### 3. Route adaptively

Select the workflow, relevant skills, and optional specialist agents from `workflows/registry.md`.

- Simple + low risk: use a lightweight path (targeted discovery, bounded action, proportionate verification, concise report).
- Moderate or multi-step: use the selected workflow's discovery, clarification, planning, verification, and reporting steps.
- Complex: use the full selected workflow, explicit dependencies, acceptance criteria, and a workflow brief.
- High or critical risk: apply the relevant strict safety and approval gates regardless of complexity. Prefer read-only investigation first.
- Mixed or uncertain tasks: resolve the dominant task first; add secondary workflow requirements only where they materially affect safety or correctness.

Never skip an approval gate because a task is classified as simple.

### 4. Discover and plan

Read the selected workflow and every skill whose description matches the task before applying their procedures. Inspect relevant repository instructions and implementation evidence.

For non-trivial work, prepare a bounded plan with:

- Intended behavior and acceptance criteria.
- In-scope and out-of-scope changes.
- Files/components likely to change.
- Dependencies and ordered steps.
- Complexity, risk, assumptions, and mitigations.
- Verification strategy and rollback/recovery notes where relevant.
- Approval required before any gated action.

Use `templates/workflow-brief.md` for complex work, multi-agent handoffs, or tasks that need a durable handoff within the current session. Do not create unnecessary paperwork for trivial work.

### 5. Approval gate

Before proceeding, check whether the exact action is already within the user's explicit approval and repository policy.

Stop and request explicit approval before:
- Destructive or irreversible operations.
- Production writes, migrations, backfills, or permission/RLS changes.
- Deployment, release publication, or external side effects.
- Expanding scope materially beyond the agreed plan.
- Actions with unclear ownership, authorization, or unacceptable blast radius.

An approval applies only to the described scope and action. Do not treat approval for one task as blanket approval for future tasks. If approval is absent, mark the session state `AWAITING_APPROVAL` and do not perform the gated action.

### 6. Execute and delegate

Codex remains accountable for coordination and final reporting.

Delegate only when a specialist role materially improves the result:
- `repo_explorer`: read-only discovery and evidence gathering.
- `planner`: requirements, options, risks, sequence, and acceptance criteria; no implementation.
- `implementer`: implementation only within the approved plan.
- `reviewer`: independent correctness, regression, maintainability, and security review.
- `security_auditor`: threat modeling and security findings; no exploitative actions.

Each handoff must communicate the objective, scope, non-goals, relevant decisions, assumptions, approval status, expected output, and constraints. Use the workflow brief when useful.

Parallelize only independent work, especially read-only analysis. Avoid concurrent edits to overlapping files or dependent tasks. Agent instructions do not create security isolation: the parent Codex session's sandbox, tools, and approval settings remain authoritative.

### 7. Track state in the active session

Maintain a concise current-session record for non-trivial tasks:

- Current state.
- Selected workflow and task classification.
- Complexity and risk with rationale.
- Scope and acceptance criteria.
- Decisions, assumptions, and approval status.
- Completed steps and evidence.
- Active owner/agent, blockers, and next action.

Use only these primary states:

`INTAKE` → `TRIAGE` → `DISCOVERY` → `PLANNING` → `APPROVAL` → `EXECUTION` → `VALIDATION` → `REVIEW` → `COMPLETION`

Additional states:
- `NEEDS_CLARIFICATION`: a material requirement is unresolved.
- `AWAITING_APPROVAL`: a gated action is not yet approved.
- `BLOCKED`: progress depends on an unavailable prerequisite or external decision.
- `FAILED`: an attempted step failed and needs diagnosis or recovery.

State transition rules:
- Move to `NEEDS_CLARIFICATION` when a material ambiguity prevents safe or correct progress.
- Move to `AWAITING_APPROVAL` before any unapproved gated action.
- Move to `BLOCKED` when a prerequisite cannot be satisfied; state the blocker and owner.
- After a failed check, return to diagnosis/planning as appropriate; do not advance as if it passed.
- Reassess scope and risk when new evidence materially changes the task.
- Enter `COMPLETION` only after proportionate validation and review are complete, or clearly report a partial/blocked outcome instead.

Session state is not a persistent database. If work must survive a session boundary, ask whether the user wants a decision record, issue, or other explicit artifact.

### 8. Validate and review

Follow the selected workflow's verification requirements. Report each check as `passed`, `failed`, `skipped`, or `not run`, with exact command/evidence where applicable.

- Do not infer a test passed because code looks correct.
- Do not hide skipped checks or unresolved risks.
- Use independent review for complex, security-sensitive, or high-impact changes when available.
- If reviewer findings conflict, compare evidence and resolve the specific disagreement; do not decide by agent seniority.
- Inspect the final diff and ensure changes remain within approved scope.

### 9. Report completion

Provide a concise report containing:

- Task and selected workflow.
- Classification, complexity, and risk.
- Work completed and changed files.
- Verification results and evidence.
- Approval gates encountered and their status.
- Remaining blockers, limitations, and risks.
- Any follow-up decision required.

Do not claim completion if required validation failed or was not performed. State whether the outcome is complete, partial, blocked, or failed.

## Stop conditions

Stop, clarify, or request approval when:
- The intended behavior or ownership boundary is materially ambiguous.
- The next action exceeds approved scope.
- A destructive, production, permission, deployment, or external side effect lacks explicit approval.
- A required tool, test, or evidence source is unavailable.
- A safety boundary cannot be maintained.

## Required output

For non-trivial tasks, leave a session-visible summary of:
- Classification and selected workflow.
- Complexity and risk.
- Current state and next action.
- Scope, decisions, and approval status.
- Verification evidence and unresolved issues.
