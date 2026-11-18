# GymSync Codex Toolkit

A curated, Codex-first engineering toolkit: repository instructions, role-bounded agents, reusable skills, adaptive delivery workflows, safety gates, and evidence-backed learning.

> Codex remains the primary agent. This toolkit does not replace it with another agent framework.

## Start here

- [Toolkit Quickstart](docs/quickstart.md) — first-use sequence, adoption modes, safe task intake, and verification commands.
- [Toolkit Integration Map](docs/toolkit-integration.md) — component architecture, authority order, lifecycle, and integration invariants.
- [End-to-End Example](docs/end-to-end-example.md) — an illustrative request-to-completion workflow (not a runtime test).
- [Selective Adoption Test](docs/selective-adoption-test.md) — non-destructive preflight, acceptance criteria, and rollback checklist.
- [Installation in Codex](docs/installation.md) — how to adopt the skills and agents in a target project.
- [Phase 7 Integration Evaluation](docs/phase-7-completion-report.md) — integration review results and remaining runtime verification.
- [Phase 8 Skill Quality Audit](docs/phase-8-skill-audit.md) — 13-skill audit and remediation summary.
- [Phase 8 Completion Report](docs/phase-8-completion-report.md) — static remediation, deterministic validation, and deferred Codex runtime tests.
- [External Source Audit Index](audits/source-reviews/README.md) — nine selected repository reviews and their evidence status.
- [Phase 7 Tool Ecosystem](docs/phase-7-tool-ecosystem.md) — typed registry, permission model, and adapter acceptance criteria.
- [Phase 8 Agent Audit](docs/phase-8-agent-capability-audit.md) — agent inventory, ownership, runtime constraints, and test-engineer role.
- [Agent Tool Access Matrix](references/agent-tool-access-matrix.md) — proposed task-level role permissions and enforcement boundaries.
- [Codex Runtime Discovery](docs/codex-runtime-discovery.md) — safe local preflight for configured MCP servers and plugins.
- [MCP Adapter Contract](docs/mcp-adapter-contract.md) — MCP lifecycle, trust review, permissions, reliability, and verification gates.
- [Non-MCP Adapter Contracts](docs/non-mcp-adapter-contracts.md) — API, CLI, browser, database, design, and test adapters.
- [Graphify v0.9.112 Review](docs/adapters/graphify-v0.9.112-review.md) — pinned optional adapter candidate and runtime blockers.
- [Source-to-Toolkit Adoption Map](docs/source-adoption-map.md) — deduplicated mapping from audit findings to existing components and future phases.

## Adaptive delivery loop

For non-trivial engineering work, the toolkit uses adaptive routing:

**Intake → Triage → Discovery → Planning → Approval → Execution → Validation → Review → Completion**

Simple, low-risk, reversible tasks may use a lightweight path. High- or critical-risk actions retain strict approval and safety gates regardless of complexity. Complexity and risk are assessed separately.

The [workflow registry](workflows/registry.md) maps task categories to the existing detailed procedures. The [workflow orchestration skill](.agents/skills/workflow-orchestration/SKILL.md) defines classification, routing, session state, delegation, and completion rules.

## Repository layout

- `AGENTS.md` — repository-wide operating contract and safety rules.
- `.codex/agents/` — native project-scoped Codex subagents (TOML definitions).
- `agents/` — readable role briefs and portable reference prompts.
- `.agents/skills/` — the 13 Codex-discoverable project skills, including workflow orchestration.
- `skills/` — matching portable Markdown skill catalog for browsing and reuse.
- `workflows/registry.md` — adaptive routing index for task categories, skills, and specialist agents.
- `workflows/` — authoritative end-to-end bug, feature, database, security, research, and release procedures.
- `templates/workflow-brief.md` — session-oriented workflow checkpoint.
- `templates/agent-handoff.md` — required contract for bounded specialist assignments.
- `templates/agent-review-report.md` — structured independent review and conflict report.
- `templates/mcp-adapter-review.md` — repeatable review record for each proposed MCP server.
- `references/` — permission/approval, tool permission matrix, and source-adaptation policies.
- `registry/tools.json` — deny-by-default declarative tool inventory; currently contains one static-reviewed Graphify candidate marked `planned`, not configured or verified.
- `schemas/tool-registry.schema.json` — typed tool registry contract with operation-level resource/action/effect and input/output schema validation.
- `schemas/runtime-capability-snapshot.schema.json` — sanitized host-discovery evidence contract.
- `schemas/agent-handoff.schema.json`, `agent-result.schema.json`, and `agent-task-graph.schema.json` — typed delegation and dependency contracts.
- `evals/` — taxonomy, cases, rubrics, run records, reports, and acceptance checks.
- `learning/inbox/` — proposed lessons awaiting review.
- `learning/approved/` — curated lessons approved for reuse.
- `templates/project-memory/` — reusable project profile, repository map, architecture, inventory, constraints, and task-checkpoint templates.
- `templates/` — reusable workflow, decision-record, and evaluation-report templates.
- `docs/project-intelligence.md` and `docs/memory-maintenance.md` — persistent knowledge architecture and upkeep procedure.
- `audits/source-reviews/` — archived source-by-source audit records.
- `docs/source-adoption-map.md` — mapping from selected source capabilities to existing toolkit owners and future implementation phases.
- `docs/` — architecture, audit, and source attribution documentation.

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
- Codex remains the primary coordinator. Existing specialist agents are delegated bounded responsibilities using explicit handoff contracts.
- Codex works alone when delegation adds no material value; delegate only to a suitable existing role.
- Parallelize only independent work with non-overlapping ownership; sequence dependent work and shared-file edits.
- Resolve conflicting findings by comparing evidence, not agent seniority; preserve unresolved disagreements for parent/user decision.
- Use an independent read-only reviewer for complex, security-sensitive, or high-impact changes where available.
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

- Graphify is an optional external knowledge-graph capability under evaluation; it is not vendored or mandatory. See its source audit and adoption map.
- No destructive automatic file compression or rewriting.
- No changes to the GymSync application source code.
- No dependency on Claude-, Hermes-, or OpenCode-specific runtime commands.
- No external orchestration framework or persistent workflow database.

## Quality checks

See [toolkit acceptance checks](evals/acceptance-checks.md). The evaluation system distinguishes deterministic artifact checks from behavioral Codex evaluation. An artifact check passing is not evidence that model behavior passed.

## Functional tooling

Dependency-free maintenance utilities under `tools/`:

- `python tools/validate_tool_registry.py` checks the tool registry manifest.
- `python tools/validate_agent_contracts.py` checks the handoff, result, and task-graph schema files.
- `python tools/validate_toolkit.py` checks skill metadata, native/portable skill parity, agent TOML, workflow sections, evaluation schemas, all evaluation cases, and the skill-quality rubric's Markdown/JSON alignment plus declared trigger-coverage minimums.
- `python tools/sync_skills.py` previews differences between native skills and the portable mirror.
- `python tools/sync_skills.py --check` exits non-zero when the mirror is out of sync.
- `python tools/sync_skills.py --write` copies native skill files into the portable mirror. The native `.agents/skills/` tree is the source of truth.
- `python tools/evaluate_toolkit.py --list` lists evaluation cases.
- `python tools/evaluate_toolkit.py --validate` validates case files against the declared schema contract.
- `python tools/evaluate_toolkit.py --run` runs deterministic toolkit integrity checks and creates an immutable evidence-ready run record and Markdown report; it does not launch Codex or grade model behavior.
- `python tools/evaluate_toolkit.py --run --compare evals/results/<previous-run-id>.json` compares stable case/criterion outcomes with a prior run.
- `python tools/discover_codex_runtime.py` performs a read-only Codex CLI/MCP/plugin preflight; it never installs, authenticates, starts, or calls tools.
- `python tools/validate_project_memory.py` checks project-memory template structure, status labels, source markers, selected secret-like patterns, and dated-page freshness.

Python 3.11+ is recommended for full TOML validation. The scripts use only the Python standard library. The evaluation runner implements the JSON Schema keywords used by this repository's schemas; it is not a general-purpose full Draft 2020-12 validator.

## Continuous quality gates

GitHub Actions runs the dependency-free quality pipeline on pushes and pull requests targeting `main`. It executes unit tests, native/portable skill parity checks, the repository validator, evaluation-case validation, and a deterministic evaluation-run smoke test. The workflow has read-only repository permissions and does not merge, deploy, or modify repository settings.

See [quality gates](docs/quality-gates.md) for local commands, CI behavior, and limitations.

## Evaluation system

Read [evals/README.md](evals/README.md) for the hybrid evaluation process, [taxonomy](evals/taxonomy.md), and [rubrics](evals/rubrics/). Cases live in `evals/cases/*.json` and use `schemas/evaluation-case.schema.json`. Run records use `schemas/evaluation-result.schema.json`; rubric definitions use `schemas/evaluation-rubric.schema.json`. The existing `schemas/decision-record.schema.json` remains the engineering decision-record contract.

Behavioral checks require an actual trusted Codex session and evidence-backed human grading. The runner deliberately leaves those criteria as `NOT_RUN` until that review occurs. Historical run records are never overwritten.

## Project Intelligence

Use the [Project Intelligence skill](.agents/skills/project-intelligence/SKILL.md) to retrieve and maintain evidence-backed project knowledge across Codex sessions. The portable skill mirror is in `skills/project-intelligence/`. Start with [the architecture and retrieval protocol](docs/project-intelligence.md), then follow [the memory maintenance procedure](docs/memory-maintenance.md). The generic page templates live in `templates/project-memory/`. This is version-controlled Markdown plus a deterministic validator; it is not a vector database, automatic repository watcher, or autonomous memory agent.


Phase 6 agent coordination validation: see [`docs/agent-validation.md`](docs/agent-validation.md) and [`evals/rubrics/agent-coordination.md`](evals/rubrics/agent-coordination.md). Seven agent-behavior scenarios are prepared; execution remains `NOT_RUN — CODEX_REQUIRED` until a trusted Codex session is available.
