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

Extract the objective, observable outcome, explicit scope, constraints, non-goals, target repository/environment, deadlines, and decisions or approvals already given for this exact task. Do not invent missing requirements. Ask one focused clarification when an unknown materially changes routing, safety, or expected behavior.

### 2. Triage

Classify the primary task using `workflows/registry.md`. For mixed tasks, identify one primary workflow and list secondary concerns rather than starting overlapping workflows.

Assess **complexity** and **risk** separately:

- Complexity: `simple`, `moderate`, or `complex`.
- Risk: `low`, `medium`, `high`, or `critical`.

Complexity estimates coordination and technical effort. Risk estimates potential impact, reversibility, sensitivity, and blast radius. Use the registry definitions and override rules. If uncertainty could conceal high impact, choose the safer route until clarified.

### 3. Select the execution mode

Choose deliberately between Codex working alone, delegation, and parallel delegation.

**Codex works alone when:**
- The task is trivial, localized, and low risk.
- The context is tightly coupled and delegation would add more coordination than value.
- No existing specialist has a meaningful advantage.
- The work requires a single continuous edit to a small set of interdependent files.

**Delegate when:**
- A specialist can materially improve discovery, planning, implementation, or review quality.
- A bounded task can be described with clear ownership and a useful deliverable.
- The parent can verify the result and retain accountability.

**Parallelize only when:**
- Tasks are independent and have explicit, non-overlapping ownership.
- Each agent can proceed without depending on another agent's unfinished output.
- Concurrent work will not create conflicting edits or inconsistent assumptions.

**Sequence when:**
- One task consumes another task's findings or artifacts.
- Multiple agents would edit the same file or tightly coupled behavior.
- Implementation must follow an approved plan.
- Independent review must inspect the completed implementation rather than its proposal.

Do not delegate merely to increase agent count. Prefer one well-scoped specialist over several redundant agents.

### 4. Choose the right existing agent

Use the registry's role boundaries:
- `repo_explorer`: read-only architecture, code-path, and evidence discovery.
- `planner`: options, dependencies, acceptance criteria, risks, and implementation sequence; no edits.
- `implementer`: changes only within the explicitly approved plan.
- `reviewer`: independent read-only correctness, regression, maintainability, and test review.
- `security_auditor`: defensive read-only security and trust-boundary review.

If no agent fits, Codex should perform the work itself or explain why a suitable role is unavailable. Do not invent capabilities or imply that Markdown role briefs are executable agents.

### 5. Discover and plan

Read the selected workflow and every skill whose description matches the task before applying their procedures. Inspect relevant repository instructions and implementation evidence.

For non-trivial work, define intended behavior, acceptance criteria, in-scope/out-of-scope changes, likely files, dependencies, ordered steps, complexity/risk assumptions, mitigations, verification, and rollback/recovery notes where relevant. Use `templates/workflow-brief.md` for complex tasks, multi-agent handoffs, or a useful session checkpoint; do not create paperwork for trivial work.

### 6. Prepare bounded handoffs

For non-trivial delegation, use `templates/agent-handoff.md`. Include objective, recipient, scope, non-goals, context/evidence, assumptions, exact approval status, constraints, expected output, dependencies, and parallelization status.

- Assign one accountable owner per task.
- State exactly which files or questions the agent owns.
- Give agents only relevant context.
- Do not assign concurrent agents overlapping write scopes.
- Handoff text does not grant permission or change the parent session's sandbox/tool settings.
- If ownership, approval, or safety is unclear, stop and report the blocker.

The parent remains responsible for task coordination, validating agent output, and final reporting.

### 7. Approval gate

Check whether the exact action is already within the user's explicit approval and repository policy. Stop and request approval before destructive/irreversible operations, production writes, migrations, permission/RLS changes, deployment, external side effects, material scope expansion, or actions with unclear ownership or unacceptable blast radius.

Approval applies only to the described scope and action. Do not treat approval for one task as blanket approval for future tasks. If approval is absent, mark `AWAITING_APPROVAL`; continue only safe read-only discovery/planning.

### 8. Coordinate work and resolve conflicts

Track each delegated task as pending, active, completed, blocked, or failed in the active session. Record its owner, output, dependencies, and evidence.

- Accept parallel results independently; do not assume completion order implies correctness.
- If agents disagree, isolate the exact disputed claim and compare source evidence, reproduction steps, test results, and scope.
- Prefer directly reproducible evidence over opinion or agent seniority.
- Ask the relevant agent for a focused re-check when evidence is incomplete.
- If disagreement remains unresolved, preserve both positions and mark the issue unresolved; the parent Codex coordinator makes the final engineering recommendation and escalates material product/scope decisions to the user.
- Never silently discard a security finding or suppress a minority finding without documenting the evidence-based reason.

### 9. Track state in the active session

Maintain a concise record of current state, workflow, classification, scope, acceptance criteria, decisions, approval, completed work, evidence, owners, blockers, and next action.

Primary states:

`INTAKE` → `TRIAGE` → `DISCOVERY` → `PLANNING` → `APPROVAL` → `EXECUTION` → `VALIDATION` → `REVIEW` → `COMPLETION`

Additional states:
- `NEEDS_CLARIFICATION`: a material ambiguity prevents safe or correct progress.
- `AWAITING_APPROVAL`: the next gated action is not approved; continue only safe read-only work.
- `BLOCKED`: a prerequisite is unavailable; name the blocker and owner.
- `FAILED`: an attempted step failed and needs diagnosis or recovery.

State transition rules:
- Move to `NEEDS_CLARIFICATION` when a material ambiguity prevents safe or correct progress.
- Move to `AWAITING_APPROVAL` before any unapproved gated action.
- Move to `BLOCKED` when a prerequisite cannot be satisfied; state the blocker and owner.
- After a failed check, return to diagnosis/planning as appropriate; do not advance as if it passed.
- Reassess scope and risk when new evidence materially changes the task.
- Enter `COMPLETION` only after proportionate validation and review are complete, or clearly report a partial/blocked outcome instead.

Session state is not a persistent database. Use `templates/workflow-brief.md` for complex tasks or durable handoffs when useful.

### 10. Independent review

For complex, security-sensitive, or high-impact changes, request a reviewer who did not implement the change whenever available. Give the reviewer the approved scope, acceptance criteria, diff/revision, and relevant test evidence, but do not tell them what conclusion to reach.

Use `templates/agent-review-report.md`. Require findings to identify severity, status, location, triggering scenario, evidence, impact, remediation, and verification. Separate confirmed defects from hypotheses and questions. Reviewers remain read-only; implementation fixes return to the implementer or parent.

A clean review means no findings were identified within the stated scope; it is not proof that the whole system is defect-free.

### 11. Validate and report

Follow the selected workflow's verification requirements. Report each check as `passed`, `failed`, `skipped`, or `not run`, with exact command/evidence. Do not infer a test passed because code looks correct. Inspect the final diff and ensure changes remain within approved scope.

The completion report includes classification, work completed, changed files, checks and evidence, review outcome, unresolved conflicts/risks, blockers, and any required user decision. Do not claim completion if required validation or review is incomplete.

## Stop conditions

Stop, clarify, or request approval when scope, ownership, approval, or safety is materially ambiguous; a gated action is unapproved; required evidence/tooling is unavailable; or a safety boundary cannot be maintained.

## Required output

For non-trivial tasks, leave a session-visible summary of classification, selected workflow, complexity/risk, current state, scope/approval, owners and handoffs, completed steps, verification evidence, and unresolved issues.
