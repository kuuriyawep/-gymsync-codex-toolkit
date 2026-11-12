# Installation in Codex

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

## Important distinctions
- `agents/*.md` are human-readable role briefs, not executable Codex agent definitions.
- `.codex/agents/*.toml` are the actual project-scoped custom subagent definitions.
- `skills/*.md` are a portable catalog; `.agents/skills/` is the Codex discovery location.
- Skills and agents do not install external tools, grant extra permissions, or bypass the parent session's sandbox and approval settings.
- Custom subagents inherit the parent session's permissions and tools. Their instructions request read-only behavior where appropriate, but are not a substitute for sandbox or permission controls.
