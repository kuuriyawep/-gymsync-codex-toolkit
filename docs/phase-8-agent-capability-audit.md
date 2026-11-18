# Phase 8 — Agent Capability Audit

**Status:** Existing-role audit complete; typed handoff/task contracts are implemented; dedicated test-engineer role added with test-only scope checks.  
**Date:** 2026-11-18  
**Inputs:** [Phase 6 final synthesis](phase-6-final-synthesis.md), [workflow registry](../workflows/registry.md), [agent handoff](../templates/agent-handoff.md), [agent validation](agent-validation.md)

## 1. Existing agent inventory

The repository now defines six executable Codex custom agents and six human-readable role briefs.

| Agent ID | Native config | Role brief | Primary responsibility | Write policy |
|---|---|---|---|---|
| `repo_explorer` | `.codex/agents/repo_explorer.toml` | `agents/explore.md` | Read-only repository architecture and evidence discovery | No writes |
| `planner` | `.codex/agents/planner.toml` | `agents/planner.md` | Requirements, sequence, dependencies, risks, acceptance criteria | No writes |
| `implementer` | `.codex/agents/implementer.toml` | `agents/implementer.md` | Approved implementation and scoped tests | Approved write scope only |
| `reviewer` | `.codex/agents/reviewer.toml` | `agents/reviewer.md` | Independent correctness, regression, maintainability, and test review | No writes |
| `security_auditor` | `.codex/agents/security_auditor.toml` | `agents/security.md` | Defensive application security and trust-boundary review | No writes |
| `test_engineer` | `.codex/agents/test_engineer.toml` | `agents/test_engineer.md` | Test strategy, fixtures, test harnesses, coverage, and safe test execution | Approved test/fixture/evaluation paths only |

All six native files contain the required `name`, `description`, and `developer_instructions` fields. Each TOML name matches its filename. All six role briefs map to the corresponding executable definitions.

No agent is missing a canonical brief. No duplicate native agent ID was found in the current inventory.

## 2. Responsibility ownership and overlap

| Boundary | Current overlap | Resolution |
|---|---|---|
| Explorer vs planner | Both inspect project context | Explorer owns observed facts, code paths, and evidence; planner consumes evidence and owns task decomposition/acceptance criteria |
| Planner vs implementer | Both discuss implementation | Planner proposes; implementer changes files only after exact user approval |
| Implementer vs reviewer | Both inspect tests and code | Implementer owns changes and first-line checks; reviewer independently inspects the actual diff/source/tests |
| Reviewer vs security auditor | Both may notice security issues | Reviewer covers general correctness/regression and flags security indicators; security auditor owns dedicated threat/auth/data-exposure assessment |
| Codex vs any agent | Parent and subagent both coordinate | Codex alone owns global routing, approvals, integration, conflict resolution, and final completion report |

The current reviewer instructions include security as one review dimension. Keep that as a detection responsibility; do not duplicate the full security-audit workflow. A high-risk security finding should trigger a bounded security-auditor handoff when useful.

## 3. Codex runtime constraints verified from current documentation

Official Codex documentation confirms:
- Project-scoped custom agent TOML files live in `.codex/agents/`.
- Required custom-agent fields are `name`, `description`, and `developer_instructions`.
- Custom agents inherit the parent session's permissions, provider, and MCP servers.
- A custom agent cannot override the parent's `sandbox_mode`, `approval_policy`, or MCP server configuration.
- Supported feature reductions include `features.shell_tool`, `features.apps`, `features.plugins`, `features.memories`, and `features.request_permissions_tool`.
- Global `[agents]` settings include `enabled`, `max_concurrent_threads_per_session`, default subagent model/reasoning, and interruption messaging.
- Codex coordinates spawning, waiting, steering, and closing agent threads.

Official references:
- [Codex subagents and custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Codex sandbox and approvals](https://learn.chatgpt.com/docs/sandboxing)

### Security consequence

Agent instructions and role briefs do **not** create a separate security boundary. A `read-only` label is an expected behavior contract, not a distinct OS sandbox. All spawned agents inherit the parent's actual sandbox and approval mode. MCP servers are configured at the parent session and inherited by agents.

Therefore:
- Enforce technical file/network boundaries at the parent Codex sandbox and host configuration.
- Use MCP `enabled_tools` allowlists at the server/parent level.
- Use capability feature flags only when the role can still complete its job without the disabled feature.
- Never describe per-agent instructions as hard permission enforcement.
- Keep file ownership, handoffs, and dependency ordering as coordination controls, not security isolation.

No new feature flags, global concurrency settings, or parent sandbox settings have been written by this audit.

## 4. Proposed role-to-tool access profiles

The following is the intended task-level allowlist. It is not yet enforced independently per agent because Codex agents inherit parent tools and permissions.

| Agent | Read access | Write access | External / privileged actions |
|---|---|---|---|
| `repo_explorer` | Approved repository files, Git history/status, tests, approved read-only graph queries | None | No network writes, secrets, deployments, or destructive commands |
| `planner` | Relevant source, project instructions, architecture and existing test evidence | None | No external side effects or privileged operations |
| `implementer` | Approved task files and dependencies | Only exact approved paths and owned test/code files | No commits, pushes, merges, deployment, production writes, or permission changes without separate approval |
| `reviewer` | Diff, source, tests, CI logs, evidence | None | No external side effects or permission changes |
| `security_auditor` | Source, auth/RLS/grants/config, dependencies, logs with secrets redacted | None | No exploitation, credential extraction, live-system mutation, or destructive tests |

The registry's permission profiles and Phase 7 operation metadata remain the source for tool/operation descriptions. The parent Codex session must apply the actual permission mode.

## 5. Candidate roles — add only when ownership is distinct

| Candidate | Decision | Rationale |
|---|---|---|
| `test_engineer` | **Added in Phase 8** | Distinct test strategy, fixture design, test-only implementation, test execution, flakiness and coverage analysis. Must own test paths separately from application-code implementation. |
| `docs_researcher` | Defer | Useful for external framework/API documentation, but first confirm an approved documentation MCP/search tool is available in the target Codex runtime. |
| `designer` | Defer | Requires a defined design-system/Figma workflow and tool availability; no evidence that a generic role would improve current toolkit workflows yet. |
| `database_specialist` | Defer | Current security auditor and database/backend workflow cover defensive review; add only if repeatable database implementation tasks justify a separate owner. |
| `manager` | Reject as a separate agent | Duplicates Codex's primary coordinator responsibility and would create competing orchestration authority. |

### Test engineer boundary

If added:
- Own test plans, test files, fixtures, test harnesses, and safe test execution.
- Do not edit production application code or decide product behavior.
- Return failures with exact test IDs, commands, output, and reproduction conditions.
- Use disposable fixtures; no production data or real external side effects.
- Implementer owns application code. When a dedicated test engineer is assigned, the handoff must name the test-file owner to prevent overlapping writes.
- Reviewer remains independent and does not modify tests or implementation.

The test engineer was added only after the handoff/result schema and task ownership validator could express test-only write boundaries.

## 6. Current gaps

1. Role and write-scope rules remain procedural; they do not create independent OS sandboxing.
2. Per-agent capability reductions have not been tested in a real Codex session.
3. Existing evaluation cases still need trusted-session execution for behavioral sign-off.
4. The task graph validator checks repository-relative safe write paths, declared write overlap, dependencies, and cycles, but actual concurrent agent behavior remains unverified.

## 7. Phase 8 work sequence

1. Freeze the original five-role inventory and ownership boundaries. **Complete.**
2. Define JSON Schemas for handoffs, agent results, and task graphs. **Complete.**
3. Implement deterministic checks for approval scope, result evidence, DAG cycles, and parallel write ownership. **Complete.**
4. Add test_engineer with test-only scope checks. **Complete.**
5. Update workflow routing and handoff templates. **Complete.**
6. Add evaluation cases for role fit, context boundaries, conflicts, failure recovery, and write-scope enforcement. **Initial test-engineer case added; broader suite in progress.**
7. Run CI; leave actual subagent behavior as NOT_RUN until a trusted Codex session is available.

## 8. Explicit non-goals

- Do not replace Codex with CrewAI, Hermes, n8n, OpenCode, or another runtime.
- Do not create a manager agent or a competing orchestrator.
- Do not change GymSync application code, database, deployment, or production data.
- Do not install MCP servers or external services as part of this static role audit.
- Do not claim independent per-agent sandboxing.
