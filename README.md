# GymSync Codex Toolkit

A curated, Codex-first engineering toolkit: repository instructions, role-bounded agents, reusable skills, adaptive delivery workflows, safety gates, and evidence-backed learning.

> Codex remains the primary agent. This toolkit does not replace it with another agent framework.

## Adaptive delivery loop

For non-trivial engineering work, the toolkit uses adaptive routing:

**Intake → Triage → Discovery → Planning → Approval → Execution → Validation → Review → Completion**

Simple, low-risk, reversible tasks may use a lightweight path. High- or critical-risk actions retain strict approval and safety gates regardless of complexity. Complexity and risk are assessed separately.

The [workflow registry](workflows/registry.md) maps task categories to the existing detailed procedures. The [workflow orchestration skill](.agents/skills/workflow-orchestration/SKILL.md) defines classification, routing, session state, delegation, and completion rules.

## Repository layout

- `AGENTS.md` — repository-wide operating contract and safety rules.
- `.codex/agents/` — native project-scoped Codex subagents (TOML definitions).
- `agents/` — readable role briefs and portable reference prompts.
- `.agents/skills/` — the 12 Codex-discoverable project skills, including workflow orchestration.
- `skills/` — matching portable Markdown skill catalog for browsing and reuse.
- `workflows/registry.md` — adaptive routing index for task categories, skills, and specialist agents.
- `workflows/` — authoritative end-to-end bug, feature, database, security, research, and release procedures.
- `templates/workflow-brief.md` — session-oriented task and agent handoff brief.
- `references/` — permission/approval and source-adaptation policies.
- `evals/` — acceptance checks and structured behavior scenarios.
- `learning/inbox/` — proposed lessons awaiting review.
- `learning/approved/` — curated lessons approved for reuse.
- `templates/` — reusable workflow and decision-record templates.
- `docs/` — source influence and attribution register.

## Use with Codex

1. Clone this repository or copy the relevant files into the target project's working directory.
2. Keep `AGENTS.md` at the project root if you want its instructions to apply to that project.
3. Trust the project in Codex if prompted; project-scoped instructions, skills, and agents require a trusted project.
4. Start or refresh the Codex session so project-scoped configuration can be discovered.
5. Skills under `.agents/skills/` are the native discovery path; Codex can select relevant skills from their descriptions, and you can also invoke one explicitly when supported.
6. For non-trivial engineering tasks, use the workflow orchestration skill and follow the selected procedure in `workflows/registry.md`. The registry routes; the individual workflow file defines the detailed process.
7. Custom subagents under `.codex/agents/` are native project-scoped agents. The Markdown files under `agents/` are reference briefs only.
8. Review all instructions against the target project's own rules before use.

## Workflow state and delegation

- Workflow state is tracked in the active Codex session; it is not a persistent task database.
- Use `templates/workflow-brief.md` for complex work or meaningful handoffs, not for every small task.
- Codex remains the primary coordinator. Existing specialist agents are delegated bounded responsibilities.
- Parallelize only independent work and avoid overlapping concurrent writes.
- Subagents inherit the parent session's sandbox and approval settings; their instructions do not create a separate security boundary.

## Safety model

- Read-only investigation before implementation.
- Explicit approval for destructive actions, production writes, schema/permission changes, deployment, and external side effects.
- Complexity and risk are separate; high/critical risk overrides lightweight routing.
- Approval applies only to the stated scope/action.
- Least privilege and no secrets in prompts or commits.
- Tests and verification are reported honestly; unrun checks are never presented as passed.
- Learning is reviewed before promotion; no autonomous self-modification.

## Source policy

The toolkit adapts general ideas from public engineering repositories. It is not a wholesale copy. See [source attribution](docs/source-attribution.md) and [source adaptation policy](references/source-adaptation.md). Verify exact per-file licensing before any verbatim reuse.

## Explicit exclusions

- Graphify is intentionally not included; install it separately if desired.
- No destructive automatic file compression or rewriting.
- No changes to the GymSync application source code.
- No dependency on Claude-, Hermes-, or OpenCode-specific runtime commands.
- No external orchestration framework or persistent workflow database.

## Quality checks

See [toolkit acceptance checks](evals/acceptance-checks.md). These checks are a checklist; they are not claims that automated or model-runtime tests have passed.

## Functional tooling

This repository includes dependency-free maintenance utilities under `tools/`:

- `python tools/validate_toolkit.py` checks skill metadata, native/portable skill parity, native agent TOML, workflow sections, and structured evaluation cases.
- `python tools/sync_skills.py` previews differences between native skills and the portable mirror.
- `python tools/sync_skills.py --check` exits non-zero when the mirror is out of sync.
- `python tools/sync_skills.py --write` copies native skill files into the portable mirror. The native `.agents/skills/` tree is the source of truth.

Python 3.11+ is recommended for full TOML validation. The scripts use only the Python standard library.

## Structured evaluation

Reusable behavior scenarios live in `evals/cases/*.json` and follow `schemas/evaluation-case.schema.json`. They are designed for later manual or hybrid evaluation in an actual Codex environment. They are not evidence that model runtime tests have already passed.

## Schemas

- `schemas/evaluation-case.schema.json` defines evaluation case structure.
- `schemas/decision-record.schema.json` defines engineering decision record structure.
