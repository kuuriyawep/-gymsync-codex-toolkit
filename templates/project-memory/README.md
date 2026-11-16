# Project memory templates

Copy these templates into a target repository's chosen knowledge location and replace placeholders with evidence-backed project facts.

- `project-profile.md`: purpose, stack, scope.
- `repository-map.md`: modules, entry points, tests, configuration.
- `architecture.md`: component boundaries and critical flows.
- `system-inventory.md`: integrations, APIs, dependencies.
- `constraints.md`: invariants, security and compatibility constraints.
- `current-state.md`: concise session handoff checkpoint.
- `decisions/README.md`: durable decision history.

## Rules
Use Verified, Assumption, Unknown, and Stale labels. Cite source paths, tests, schemas, commits, or explicit user decisions. Record verification dates. Do not store secrets or personal data. Source code, tests, schemas, and current configuration outrank memory. The validator checks structure and selected safety/freshness patterns; it cannot prove factual correctness.

Run `python tools/validate_project_memory.py` from the toolkit root.
