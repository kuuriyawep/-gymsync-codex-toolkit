# Project State — GymSync Codex Toolkit

> **Mandatory session checkpoint.** Before starting any task in this repository, read this file in full. Do not begin implementation, research, delegation, or planning until the current state, constraints, and next action are understood. At the end of meaningful work, update this file so the next session resumes from the actual stopping point.

**Last verified:** 2026-11-16  
**Repository:** `kuuriyawep/-gymsync-codex-toolkit`  
**Default branch:** `main`  
**Checkpoint type:** Repository-level source of truth  
**Status vocabulary:** COMPLETE, IN_PROGRESS, PENDING, BLOCKED, NOT_RUN, NOT_SCORED

## 1. Mission and authority

This is a reusable, Codex-first engineering toolkit. Codex remains the primary coordinator and decision-maker; specialist agents are bounded delegates, not replacements for Codex.

This file is the concise cross-session status index. It does not replace detailed source files, phase reports, evaluation records, or current repository inspection.

Authority order:
1. Explicit user decisions and current approved scope.
2. Current repository source and configuration.
3. `AGENTS.md` and the applicable workflow/skill contracts.
4. This checkpoint for current status and next action.
5. Older reports, notes, and conversational summaries (verify before relying on them).

If this file conflicts with current source or a newer explicit user decision, stop, investigate, and reconcile the conflict. Do not silently guess.

## 2. Non-negotiable user constraints

- Work only in this toolkit repository unless the user explicitly expands scope.
- Do not modify GymSync application source, database, deployment, or production data.
- Do not install dependencies, tools, frameworks, or external runtimes unless explicitly approved.
- Do not integrate n8n, CrewAI, Graphify, or other orchestration/runtime systems without explicit approval.
- Keep Codex as the primary orchestrator.
- Do not create a GymSync-specific skill yet; the toolkit remains generic.
- Do not create branches or pull requests unless requested. Default to `main`.
- Obtain user approval before commits or consequential changes unless the user explicitly authorizes the exact action.
- Do not claim runtime tests, agent execution, or behavioral evaluations passed unless they were actually run and evidence is recorded.
- Preserve existing work. Improve and extend the current toolkit; do not restart or replace it.
- Keep current scope stable. New ideas and repositories go into the backlog/source inventory; they do not automatically become active work.
- At task start, identify the exact task, scope, expected output, and acceptance criteria. Do not silently switch tasks.
- At task end, record completed work, changed paths, evidence, checks actually run, unresolved items, and one next action.

## 3. Current repository baseline

The repository already contains a substantial toolkit; it is not a starter project.

- 13 canonical skills under `.agents/skills/`.
- 13 portable mirrors under `skills/`; the latest recorded audit found all 13 mirror pairs had identical Git blob SHAs.
- 5 native Codex agent definitions under `.codex/agents/`.
- 5 corresponding role briefs under `agents/`.
- 7 workflow documents: registry plus 6 detailed workflows.
- 41 evaluation cases.
- 7 Phase 6 agent-coordination behavioral scenarios.
- Project Intelligence templates, retrieval guidance, and a deterministic validator.
- Dependency-free validation/evaluation scripts and GitHub Actions quality gates.

Canonical skills:
1. change-impact-analysis
2. clear-technical-communication
3. code-review
4. documentation-and-decisions
5. implementation-planning
6. project-intelligence
7. requirements-clarification
8. risk-aware-tdd
9. security-review
10. skill-authoring-and-evaluation
11. systematic-debugging
12. verification-gate
13. workflow-orchestration

Detailed structure and current file names are in `README.md`, `workflows/registry.md`, and `docs/project-intelligence.md`. Re-check the live tree before relying on counts.

## 4. Phase and verification status

| Area | Current status | Evidence / limitation |
|---|---|---|
| Phases 1–5 | COMPLETE (per prior project record) | Verify phase-specific reports if a task depends on details |
| Phase 6 agent coordination | PREPARED; behavioral validation NOT_RUN | `docs/agent-validation.md`; seven scenarios await a trusted Codex session |
| Phase 7 integration evaluation | Static review documented; runtime/adoption checks pending | `docs/phase-7-completion-report.md` |
| Phase 8 skill quality audit/remediation | Static remediation COMPLETE | `docs/phase-8-completion-report.md` and `docs/phase-8-skill-audit.md` |
| Deterministic CI | PASS on code-bearing commit only | Run #109: 38 unit tests, 41 evaluation cases, validator zero warnings; commit `fb7967a4ce7b54a6a4731b92af221f8833be9e2c` |
| Latest docs-only reconciliation | Recorded after the above CI run | Commits `e200bb647cf9971dd9958eca7256d6d7eb160fde`, `d518ece9ad9daa78d5d1e475300863c7157a0300`, `1bf38d4a4896715314dc779e1ff8ec51e4b9f417`; CI was not claimed to rerun on these docs-only commits |

Important remaining verification gaps:
- Six-dimension formal static skill scores: NOT_SCORED.
- Codex skill discovery/selection: NOT_RUN.
- Five specialist agents' runtime execution: NOT_RUN.
- Seven Phase 6 behavioral scenarios: NOT_RUN — CODEX_REQUIRED.
- Selective adoption trial: NOT_RUN.
- Full Markdown link integrity audit: NOT_RUN.
- CI does not prove real delegation, approval enforcement, agent behavior, or skill selection.
- Toolkit is not runtime-validated or production-ready.

Do not convert a prepared test into a passed test. Keep these statuses separate.

## 5. Current project direction

The user wants to evolve the existing toolkit into a real capability-oriented engineering system, not merely a collection of written prompts.

Six capability dimensions to preserve:
1. Intelligent workflow engine.
2. Evaluation and testing system.
3. Knowledge and memory system.
4. Delegation and multi-agent review.
5. Tooling and verification.
6. Professional documentation and architecture.

Target capabilities under consideration include real design tooling (e.g. Figma), code editing/terminal/Git/API tools, browser automation and test runners, research/documentation retrieval, SQL/database tooling, security scanning, evidence-based review, permission controls, approval gates, credential safety, and fallbacks.

These are design goals, not evidence that integrations are already implemented. Codex remains the orchestrator. The user currently lacks a Codex runtime/subscription for real behavioral evaluation, so static architecture, documentation, schemas, mocks, and contract tests may be prepared without claiming runtime success.

## 6. External source repository inventory

The user wants detailed, evidence-based audits of source repositories before selecting/adapting useful capabilities. Do not blindly copy, install, or implement. For each source inspect actual tree/code/docs/tests, dependencies, license, maintenance, security, permissions, real capabilities, overlap, Codex adaptation needs, risks, and adopt/adapt/reject recommendations.

Sources already raised (initial reviews only; detailed technical audits remain pending unless a later report says otherwise):

| Source | Potential value | Initial priority |
|---|---|---|
| `vercel-labs/skills` — find-skills | Skill discovery, compatibility, version/content tracking | P0 |
| `anthropics/claude-plugins-official` | Plugin packaging, hooks, agents, skills, MCP patterns | P0 |
| `n8n-io/n8n` | Workflow automation, integrations, human approvals | P1 |
| `nextlevelbuilder/ui-ux-pro-max-skill` | Design intelligence, design tokens, UI/UX references | P1 |
| `Imbad0202/academic-research-skills` | Research pipeline, source verification, agent collaboration | P1 |
| `zarazhangrui/frontend-slides` | Visual preview and presentation-generation patterns | P2 |
| `router-for-me/CLIProxyAPI` | Provider abstraction, routing, API/credential patterns | P2 |

Additional candidate discovered during earlier research: `n8n-io/skills` (not yet fully audited or approved for implementation).

Priority is provisional and indicates review order, not a decision to drop lower-priority sources. User may add more sources; register them here before changing the active task.

## 7. Active work and resume point

**Checkpoint task:** Establish durable cross-session continuity for this repository.

**This checkpoint file:** Created to be the single required starting point for future sessions.

**Repository policy change required:** `AGENTS.md` must also instruct every Codex session to read this file before work. Verify that instruction is present after this checkpoint is added.

**Next action after this continuity setup:** Resume the user's already-open toolkit work from the most recent explicit instruction in the active conversation. Before doing so:
1. Re-read this file and `AGENTS.md`.
2. Inspect the latest repository commit and current worktree/branch state.
3. Identify whether the user intended to continue the Phase 6 audit/validation thread or the external source-repository audit thread; do not choose between them by guesswork if the active conversation does not resolve it.
4. State the exact task and scope, then continue without reopening completed planning.

**No active implementation task is authorized merely by this checkpoint.** Source audits may proceed as read-only research when the user's current instruction identifies the source/task. Installation, integration, or code changes require explicit scope approval.

## 8. Session operating protocol

### Start of every session
- Read this entire file first.
- Read `AGENTS.md`.
- Read the current phase report / workflow / skill relevant to the requested task.
- Inspect current branch, latest commit, and relevant files; do not assume this checkpoint is newer than the repository.
- Compare the user's latest instruction with the active task and constraints.
- If task identity or scope is ambiguous, ask one focused clarification before proceeding.

### During work
- Keep one active task at a time unless the user explicitly authorizes parallel independent tasks.
- Do not change phase, roadmap, priority, or scope without evidence and user approval where required.
- Record new ideas and sources in the inventory/backlog; do not let them displace the active task.
- Separate VERIFIED facts, assumptions, unknowns, and recommendations.
- Never store credentials, tokens, private keys, personal data, or production secrets here.

### End of meaningful work
Update this file with:
- Date and repository commit inspected.
- Active task and status.
- What was completed and exact paths changed.
- Checks actually run and their results.
- Decisions made and approval status.
- Remaining gaps/blockers.
- Exactly one recommended next action.
- Any new source repositories added to the inventory.

Keep this file concise enough to read at the beginning of every session. Put detailed evidence and analysis in dedicated documents and link them here.

## 9. Key reference documents

- `README.md` — repository overview and entry points.
- `AGENTS.md` — operating contract.
- `docs/project-intelligence.md` — persistent project knowledge architecture.
- `docs/memory-maintenance.md` — update and handoff rules.
- `workflows/registry.md` — task routing.
- `docs/agent-validation.md` — Phase 6 agent behavior validation.
- `docs/phase-7-completion-report.md` — Phase 7 integration review.
- `docs/phase-8-skill-audit.md` — Phase 8 audit findings.
- `docs/phase-8-completion-report.md` — Phase 8 completion and verification limits.
- `evals/README.md` and `evals/acceptance-checks.md` — evaluation procedure and quality gates.
