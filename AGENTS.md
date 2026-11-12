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

## Agent boundaries
- Explore: read-only discovery and evidence gathering.
- Planner: requirements, risks, sequence, acceptance criteria; no implementation.
- Implementer: changes only within approved plan and scope.
- Reviewer: independent correctness, regression, maintainability, and security review.
- Security: threat modeling and security findings; no exploitative actions.

## Skills
Use a skill when its description matches the task. Read its complete SKILL.md before applying it. Skills provide procedures; this file defines repository-wide rules.

## Learning
New lessons go to learning/inbox with evidence and provenance. Promote to learning/approved only after review. Do not silently rewrite instructions or self-modify the toolkit.

## Communication
Be concise but sufficiently detailed. Separate facts, assumptions, risks, and recommendations. Explain uncertainty plainly.
