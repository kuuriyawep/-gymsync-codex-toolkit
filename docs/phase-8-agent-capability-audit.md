# Phase 8 — Agent Capability Audit

**Status:** Initial audit complete; role contracts and delegation schemas are next.  
**Date:** 2026-11-18  
**Inputs:** [Phase 6 final synthesis](phase-6-final-synthesis.md), [workflow registry](../workflows/registry.md), [agent handoff](../templates/agent-handoff.md), [agent validation](agent-validation.md)

## 1. Existing agent inventory

The repository currently defines five executable Codex custom agents and five human-readable role briefs.

| Agent ID | Native config | Role brief | Primary responsibility | Write policy |
|---|---|---|---|---|
| `repo_explorer` | `.codex/agents/repo_explorer.toml` | `agents/explore.md` | Read-only repository architecture and evidence discovery | No writes |
| `planner` | `.codex/agents/planner.toml` | `agents/planner.md` | Requirements, sequence, dependencies, risks, acceptance criteria | No writes |
| `implementer` | `.codex/agents/implementer.toml` | `agents/implementer.md` | Approved implementation and scoped tests | Approved write scope only |
| `reviewer` | `.codex/agents/reviewer.toml` | `agents/reviewer.md` | Independent correctness, regression, maintainability, and test review | No writes |
| `security_auditor` | `.codex/agents/security_auditor.toml` | `agents/security.md` | Defensive application security and trust-boundary review | No writes |

All five native files currently contain the required `name`, `description`, and `developer_instructions` fields. Each TOML name matches its filename. The five role briefs describe the same five responsibilities.

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
| `test_engineer` | **Recommended for Phase 8** | Distinct test strategy, fixture design, test-only implementation, test execution, flakiness and coverage analysis. Must own test paths separately from application-code implementation. |
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

The test engineer must not be added until the handoff/result schema and task ownership validator can express its boundaries.

## 6. Current gaps

1. Handoff is a Markdown template only; there is no machine-validated handoff/result schema.
2. Task dependencies and cycles are not represented in a validated DAG.
3. Write-scope overlap is described in prose but not deterministically checked.
4. The five role configs do not express a typed tool-access profile.
5. Per-agent capability reductions have not been tested in a real Codex session.
6. Existing agent evaluation cases cover important behaviors, but Phase 8 needs explicit tests for role ownership, dependency cycles, write-scope conflicts, context minimization, and reviewer independence.

## 7. Phase 8 work sequence

1. Freeze the existing five-role inventory and ownership boundaries.
2. Define JSON Schemas for handoffs, agent results, and task graphs.
3. Implement a deterministic validator for role IDs, approval scope, result evidence, DAG cycles, and parallel write ownership.
4. Add the test-engineer role only after its task/file ownership can be validated.
5. Update workflow routing and handoff templates without duplicating existing skills.
6. Add evaluation cases for role fit, context boundaries, conflicts, failure recovery, and write-scope enforcement.
7. Run CI; leave actual subagent behavior as NOT_RUN until a trusted Codex session is available.

## 8. Explicit non-goals

- Do not replace Codex with CrewAI, Hermes, n8n, OpenCode, or another runtime.
- Do not create a manager agent or a competing orchestrator.
- Do not change GymSync application code, database, deployment, or production data.
- Do not install MCP servers or external services as part of this static role audit.
- Do not claim independent per-agent sandboxing.
