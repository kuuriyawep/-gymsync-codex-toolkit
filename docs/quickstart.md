# Toolkit Quickstart

This guide is the shortest supported path from opening the repository to using it safely in Codex. Codex remains the coordinator; the toolkit supplies procedures and optional specialist roles.

## 1. Understand what is installed

| Path | Purpose | Runtime role |
|---|---|---|
| `AGENTS.md` | Project-wide operating contract | Loaded as project instructions when supported |
| `.agents/skills/*/SKILL.md` | Reusable task procedures | Codex-discoverable skills |
| `.codex/agents/*.toml` | Specialist role definitions | Project-scoped Codex subagents |
| `agents/*.md` | Human-readable role briefs | Reference only; not executable agents |
| `workflows/registry.md` | Task-to-procedure routing | Selects authoritative workflow documents |
| `workflows/*.md` | Detailed task procedures | Follow the selected procedure |
| `templates/` | Handoffs, reviews, memory, and reports | Copy/adapt only when useful |
| `evals/` and `schemas/` | Deterministic and behavioral evaluation | Validate artifacts and record evidence |
| `tools/` | Dependency-free local validators and runner | Run explicitly from a terminal |

## 2. Choose an adoption mode

### Full project adoption

Use when this repository itself is the Codex workspace. Open/trust it in Codex, read `AGENTS.md`, and start with the task-routing instructions below.

### Selective adoption into another project

1. Copy `.agents/skills/` and `.codex/agents/` into the target repository.
2. Review `AGENTS.md` and merge only compatible rules; do not overwrite existing project instructions.
3. Copy only the workflow, reference, and template files that the target project will use.
4. Keep project-specific memory in the target project's own repository.
5. Do not copy evaluation results from this toolkit as if they were evidence about the target project.
6. Trust the target project in Codex if prompted, then start a fresh session if discovery does not refresh.

See [Installation in Codex](installation.md) for the full adoption procedure and limitations, and the [Selective Adoption Usability Test](selective-adoption-test.md) for a preflight checklist.

See the [illustrative end-to-end example](end-to-end-example.md) for a complete bug-fix lifecycle. It is a walkthrough, not a record of an executed Codex run.

## 3. Start a task

For non-trivial work, ask Codex to:
1. Read the target repository's `AGENTS.md` and relevant instructions.
2. Classify the task using `workflows/registry.md`.
3. Assess complexity and risk separately.
4. Read the selected workflow and relevant skills before acting.
5. Inspect current source, tests, schemas, and configuration.
6. State scope, non-goals, acceptance criteria, and required approvals.
7. Work alone or delegate only when a specialist adds material value.
8. Validate, independently review when warranted, and report evidence.

Suggested first-session instruction:

> Read AGENTS.md and docs/installation.md. Explain which toolkit components Codex can discover in this workspace, identify any conflicts with the target project's existing instructions, and propose a safe task-routing plan. Do not edit files, install dependencies, or perform external actions.

This is a discovery prompt, not proof that every feature is supported by the current Codex client/runtime.

## 4. Use delegation carefully

- Codex remains accountable for the result.
- Use `repo_explorer` for read-only discovery, `planner` for plans, `implementer` for approved scoped changes, `reviewer` for independent read-only review, and `security_auditor` for defensive assessment.
- Markdown files in `agents/` are reference briefs; executable subagent definitions are in `.codex/agents/`.
- One owner per task. Parallel tasks must have non-overlapping write scopes.
- A handoff does not grant permission or bypass the parent session's sandbox and approval settings.

## 5. Verify before reporting completion

From the repository root, with Python 3.11+:

```bash
python -m unittest discover -s tests -v
python tools/sync_skills.py --check
python tools/validate_project_memory.py
python tools/validate_toolkit.py
python tools/evaluate_toolkit.py --validate
python tools/evaluate_toolkit.py --run --revision "$(git rev-parse HEAD)"
```

The final command creates a new immutable deterministic evaluation record and report. It does not launch Codex or pass behavioral evaluations.

For Codex behavior, run the relevant case in a trusted Codex session and grade it using the matching rubric. Until then, keep it `NOT_RUN` or `BLOCKED`; never infer a pass from repository artifacts.

## 6. Know when to stop

Stop and ask for approval before destructive operations, production writes, migrations, permission changes, deployment, external side effects, or material scope expansion. Stop for material ambiguity or missing evidence. Report blockers instead of silently improvising.

## 7. Understand the limits

This toolkit is version-controlled guidance, project-scoped configuration, templates, and local scripts. It is not a hosted agent service, persistent task database, vector database, automatic repository watcher, or substitute for Codex. Skills and agent instructions do not create security isolation or grant extra permissions.