# Source Audit — OpenCode

- **Source:** [anomalyco/opencode](https://github.com/anomalyco/opencode)
- **Audited revision:** branch `dev`, commit `22377659a8ed223f3eebc86660dd1a5bc2b33ca5`
- **Version:** 2.3.0
- **License noted during audit:** MIT; dependencies/plugins require separate review.
- **Audit date:** 2026-11-18
- **Evidence status:** Source/documentation inspection; no runtime tests.

## Findings

OpenCode is a full AI coding-agent platform, not a reusable Codex skills toolkit. Useful patterns:
1. Capability/action/resource/effect permission rules with allow/deny/ask, ordered matching, deny precedence for multi-resource operations, and a separate hard-deny policy layer.
2. Primary/subagent/all agent modes, child sessions with fresh context, parent-controlled delegation permissions, and child-specific permissions.
3. Typed tool registry with input/output schema validation and consistent error normalization.
4. Plugin lifecycle and event hooks.
5. Lazy skill discovery/loading, supporting references/scripts, and source precedence.
6. Context compaction that summarizes older history while preserving a recent exact tail.
7. Focused tests for permissions, skills, plugins, MCP, sessions, and compaction.

Security findings:
- OpenCode explicitly states it does not sandbox the agent; Docker/VM isolation is needed for actual isolation.
- External MCP servers are outside its trust boundary.
- Shell command templates may execute outside the ordinary tool-permission flow.
- Broad unrestricted build-agent defaults are unsuitable.

## Adoption decisions

**ADAPT** tool/action/resource/effect permission concepts, typed schemas, error normalization, plugin lifecycle, lazy skill loading, child-session boundaries, and context compaction into the appropriate toolkit phases.

**REJECT** the full OpenCode runtime/dependency stack, treating permission UX as a sandbox, unrestricted agent defaults, and shell interpolation of untrusted workflow arguments.

## Phase mapping

- Phase 7: tool registry, schemas, permission policy, adapters, plugin/MCP boundaries.
- Phase 8: scoped agent modes, child sessions, delegation permissions.
- Phase 9: workflow templates, child-session execution, lifecycle events.
- Phase 10: schema, permission, plugin, session, and compaction regression tests.
- Phase 11: real Codex handoff, approval, and runtime validation.

No OpenCode code or package was installed.
