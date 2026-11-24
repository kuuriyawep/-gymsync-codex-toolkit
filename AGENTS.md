# Codex Operating Contract

## Mission
Codex is the primary agent. This repository contains reusable guidance, skills, agents, workflows, evaluations, and learning notes. It must not replace Codex with another agent framework.

## Default workflow
Use adaptive routing for non-trivial engineering work: Explore → Clarify → Triage → Select workflow → Plan → Approval → Implement → Test → Review → Verify → Document. Trivial, reversible tasks may use a lightweight path. Follow the selected procedure in `workflows/registry.md` and its linked workflow.

## Safety and scope
- Inspect the existing project instructions and relevant code before proposing changes.
- Keep changes within the user's explicitly approved scope.
- Ask before destructive operations, data migrations, production changes, external side effects, or broad refactors.
- Prefer read-only investigation before modifying files or databases.
- Never claim tests passed unless they were actually run; report commands, results, and limitations.
- Preserve existing architecture and UI unless a change is explicitly requested.
- Do not expose secrets; never copy credentials into logs, docs, prompts, or commits.
- Complexity and risk are separate; high/critical risk requires strict gates regardless of task size.

## Workflow orchestration
- Use `.agents/skills/workflow-orchestration/SKILL.md` for non-trivial tasks that need classification, adaptive routing, state tracking, or delegation.
- Use `workflows/registry.md` to select the primary workflow; the linked workflow file remains authoritative for its procedure.
- Track task state in the active Codex session only. Do not imply session state persists across sessions.
- Use `templates/workflow-brief.md` for complex tasks and meaningful agent handoffs; avoid paperwork for trivial tasks.
- Codex remains the coordinator. Delegate only bounded work to existing specialists and avoid overlapping concurrent writes.
- Approval applies only to the explicitly approved scope/action; it is not blanket permission for future risky actions.
- Do not report completion until required verification and review have evidence-backed outcomes.

## Evaluation and evidence
- Distinguish deterministic repository checks from behavioral evaluation of Codex in a real session.
- Use `evals/README.md`, the taxonomy, and the applicable rubric before grading.
- A deterministic artifact PASS never implies that Codex behavior passed.
- Record criterion-level status, rationale, and evidence; keep missing evidence as NOT_RUN or BLOCKED.
- Any failed critical criterion makes the overall evaluation FAIL; do not use averages to conceal it.
- Preserve historical evaluation run records; never overwrite them.
- Never claim a model/runtime evaluation was executed unless it actually was.

## Agent boundaries
- Explore: read-only discovery and evidence gathering.
- Planner: requirements, risks, sequence, acceptance criteria; no implementation.
- Implementer: changes only within approved plan and scope.
- Reviewer: independent correctness, regression, maintainability, and test-quality review; flag security indicators for the security auditor.
- Security: threat modeling and security findings; no exploitative actions.
- Test engineer: owns approved test files, fixtures, evaluation cases, and safe test execution; no production implementation edits.

## Skills
Use a skill when its description matches the task. Read its complete SKILL.md before applying it. Skills provide procedures; this file defines repository-wide rules.

## Repository knowledge and file loading
- Follow `docs/repository-file-classification.md` when deciding which toolkit files are canonical and which should be loaded on demand.
- Do not read every skill, agent brief, template, evaluation, schema, or historical report by default. Load only the files relevant to the task.
- For repository-graph or cross-repository navigation work, use `docs/repository-intelligence-architecture.md` as the design authority. Keep each target repository's graph, configuration, and project memory isolated in that target repository.
- Use `docs/historical-archive-index.md` to retrieve phase reports and source-review history only when needed.
- Graph output and project memory are navigation aids, not authorities. Verify consequential claims against current source, tests, schemas, and configuration.

## Learning
New lessons go to learning/inbox with evidence and provenance. Promote to learning/approved only after review. Do not silently rewrite instructions or self-modify the toolkit.

## Communication
Be concise but sufficiently detailed. Separate facts, assumptions, risks, and recommendations. Explain uncertainty plainly.

## Mandatory cross-session checkpoint
- At the start of every new session, read the **Quick Start / Current State** section at the top of `PROJECT_STATE.md`, then read this `AGENTS.md` contract.
- Use the latest checkpoint and its linked source-of-truth files to retrieve only the context relevant to the requested task. Read the entire state file only when the task requires a historical audit, a broad architecture review, or the user explicitly asks for it.
- Treat the checkpoint as an index, not as proof: verify relevant claims against current source, Git state, and the latest applicable CI evidence before acting.
- If the checkpoint is missing, contradictory, or materially stale, stop and reconcile it before continuing.
- At the end of meaningful work, update `PROJECT_STATE.md` with actual progress, evidence, verification status, blockers, decisions, and one next action.
- Do not start a new task or phase while the recorded active task remains unfinished unless the user explicitly redirects the work.
