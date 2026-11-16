# Installation in Codex

For the recommended first-use sequence, see the [Toolkit Quickstart](quickstart.md) and [Integration Map](toolkit-integration.md).

## What Codex discovers
- Project instructions: `AGENTS.md` at the repository root.
- Project skills: `.agents/skills/<skill-name>/SKILL.md`.
- Project custom subagents: `.codex/agents/<agent-name>.toml`.

## Use the toolkit in another project
1. Clone this repository or copy the files you need.
2. Copy `.agents/skills/` into the target repository root to make the skills discoverable.
3. Copy `.codex/agents/` into the target repository root to add the custom subagents.
4. Copy or carefully merge `AGENTS.md` only if you want this toolkit's operating contract to apply. Do not overwrite existing project-specific instructions blindly.
5. Trust the project in Codex if prompted; project-scoped configuration is only loaded for trusted projects.
6. Start a new Codex session or refresh it if the agents or skills do not appear.

## Selective adoption dependencies

Copying only the discoverable skills and agent definitions is sufficient for basic skill/agent discovery, but some procedures reference companion files in this repository. When adopting them, also copy the required companion paths:

| Component | Companion paths to include when used |
|---|---|
| Workflow orchestration | `workflows/` and the relevant files under `templates/` |
| Project intelligence | `templates/project-memory/` and `tools/validate_project_memory.py` |
| Skill authoring/evaluation | `evals/`, `schemas/`, `tools/evaluate_toolkit.py`, and the relevant evaluation templates if you intend to run the toolkit's evaluator |
| Toolkit maintenance | `tools/`, `tests/`, `schemas/`, `evals/`, and `.github/workflows/` as a complete maintenance set |

Do not copy the toolkit's sample evaluation results into another project's evaluation history as if they were results from that project. Keep each target project's memory and evaluation records separate. If a referenced companion file is not copied, treat that step as unavailable and do not claim it ran.

For a non-destructive adoption checklist with acceptance criteria and rollback rules, see the [Selective Adoption Usability Test](selective-adoption-test.md).

## Important distinctions
- `agents/*.md` are human-readable role briefs, not executable Codex agent definitions.
- `.codex/agents/*.toml` are the actual project-scoped custom subagent definitions.
- `skills/*.md` are a portable catalog; `.agents/skills/` is the Codex discovery location.
- Skills and agents do not install external tools, grant extra permissions, or bypass the parent session's sandbox and approval settings.
- Custom subagents inherit the parent session's permissions and tools. Their instructions request read-only behavior where appropriate, but are not a substitute for sandbox or permission controls.
