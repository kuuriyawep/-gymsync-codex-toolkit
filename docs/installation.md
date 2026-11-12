# Installation in Codex

Codex project-scoped skills are stored under `.agents/skills/`. This repository includes native skill paths in that directory, plus the curated source library under `skills/`.

1. Clone or copy this repository.
2. Copy `.agents/skills/` into the root of the project where you want Codex to use these skills.
3. Copy `AGENTS.md` only if you want this toolkit's operating contract to apply; merge it carefully with existing instructions instead of overwriting project-specific rules.
4. Refresh or restart the Codex session if newly added skills are not immediately detected.
5. Ask Codex to use a skill by name or describe the matching task.

Skills are Markdown guidance only. They do not install external tools, grant permissions, or bypass approval requirements.