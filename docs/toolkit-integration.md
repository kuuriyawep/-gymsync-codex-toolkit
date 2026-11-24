# Toolkit Integration Map

## Purpose

This document explains how the toolkit's existing components fit together. It is an integration guide, not a new runtime or orchestration framework. Codex remains the primary coordinator and execution host.

**Canonical target architecture:** [GymSync Intelligent Agent Ecosystem](intelligent-agent-ecosystem-architecture.md). That approved specification defines the nine-capability Agent Intelligence Standard, event-driven lifecycle, proposal engine, collaboration, WhatsApp gateway, memory, specialist tools, risk governance, evaluation, and seven gated workstreams. This file maps the existing repository components into that architecture; it does not establish a competing design.

**Active roadmap:** WS1–WS7 in the canonical specification. Phase 11 documents are retained as historical audit and runtime-acceptance records, not as the primary implementation roadmap. The user currently has no Codex runtime for live behavioral testing, so distinguish repository-side static evidence from runtime acceptance.

For a worked illustrative lifecycle, see the [end-to-end example](end-to-end-example.md).

## Component architecture

```text
User request
    |
    v
AGENTS.md  ---- repository-wide authority, safety, communication
    |
    v
Workflow Orchestration Skill
    |
    +---- workflows/registry.md ---- task category and route
    |             |
    |             +---- workflows/*.md ---- authoritative procedure
    |
    +---- relevant skills in .agents/skills/
    |
    +---- registry/tools.json + tool permission matrix ---- declared adapters and operation contracts
    |             +---- tools/discover_codex_runtime.py ---- sanitized host preflight (not runtime authorization)
    |             +---- docs/mcp-adapter-contract.md ---- trust, lifecycle, and adapter verification gates
    |             +---- templates/mcp-adapter-review.md ---- per-server review evidence
    |
    +---- optional .codex/agents/*.toml
    |             |
    |             +---- bounded handoff via templates/agent-handoff.md
    |             +---- independent review via templates/agent-review-report.md
    |
    +---- project knowledge via Project Intelligence
    |             |
    |             +---- templates/project-memory/*
    |             +---- docs/memory-maintenance.md
    |
    v
Implementation / research / review
    |
    v
Verification and evidence
    |
    +---- tools/ validators and deterministic evaluation
    +---- evals/cases/* + rubrics for behavioral evaluation
    +---- immutable evals/results and evals/reports
    |
    v
Completion report: outcomes, evidence, risks, blockers, next action
```

## Authority and precedence

When instructions conflict, apply this order:

1. Platform/runtime safety and permission controls.
2. The user's explicit request and approval for the current task.
3. The target repository's own source, tests, schemas, configuration, and project instructions.
4. This toolkit's `AGENTS.md`, registry, skills, and workflows, where compatible.
5. Project memory, prior notes, and agent-generated claims.

Project memory is an index and continuity aid, not a substitute for current source inspection. A specialist agent's output is evidence to review, not an instruction with higher authority than Codex or the user.

## End-to-end task lifecycle

| Stage | Primary component | Required result |
|---|---|---|
| Intake and scope | `AGENTS.md` + orchestration skill | Objective, constraints, non-goals, target environment |
| Triage | `workflows/registry.md` | Primary category; complexity and risk assessed separately |
| Discovery | Selected workflow + relevant skills | Current-source evidence, assumptions, unknowns |
| Planning | Workflow + `templates/workflow-brief.md` when useful | Ordered steps, acceptance criteria, ownership |
| Approval | User + repository safety rules | Exact approval for gated actions |
| Execution | Codex; optional specialist subagents | Changes within approved scope |
| Review | Reviewer/security role + review template | Independent findings, or explicit reason unavailable |
| Verification | Workflow + `tools/` + tests | Commands, outputs, failures, skipped checks |
| Behavioral evaluation | `evals/cases/` + applicable rubric | Criterion-level evidence from actual Codex session |
| Completion | Codex | Accurate status, changed files, limitations, next action |

## How to select components

- **Always:** follow the target project's instructions and applicable safety rules.
- **For non-trivial work:** use orchestration and select one primary workflow from the registry.
- **Skills:** read the complete skill file when its description matches the task. Skills provide procedures; they do not independently authorize actions.
- **Agents:** delegate only if a defined role materially improves the result and the task has a bounded deliverable.
- **Templates:** use proportionately. A template is a structure, not a mandatory form for every small task.
- **Project memory:** retrieve only relevant pages, then verify important claims against current source.
- **Evaluation:** deterministic checks validate artifacts; behavioral rubrics grade observed Codex behavior. Never conflate the two.

## Configuration and portability

| Artifact | Expected use | Portability note |
|---|---|---|
| `AGENTS.md` | Repository instructions | Merge carefully; target project rules take precedence where they conflict |
| `.agents/skills/` | Skill discovery | Codex-specific project discovery path |
| `.codex/agents/` | Custom subagents | Codex-specific TOML definitions; availability depends on client/runtime |
| `agents/*.md` | Human-readable role references | Not executable subagent configuration |
| `skills/` | Portable skill catalog | Mirrors native skill files; use sync checker |
| `workflows/`, `templates/`, `references/` | Human-readable procedures and assets | Can be selectively copied and adapted |
| `tools/`, `tests/`, `schemas/`, `evals/` | Local maintenance and evaluation | Run from a compatible Python environment; no hosted execution |

## Integration invariants

1. Codex remains the single accountable coordinator.
2. No agent handoff expands user approval or runtime permissions.
3. One accountable owner per task; concurrent writes must not overlap.
4. Current source and tests outrank stale project memory.
5. Every consequential claim has evidence or is labeled uncertain.
6. Failed, skipped, blocked, and unrun checks remain visible.
7. Deterministic PASS does not imply behavioral PASS.
8. Historical evaluation records are immutable; new runs create new artifacts.
9. No autonomous self-modification or silent promotion of learning notes.
10. The toolkit must not silently install dependencies, external frameworks, or services.

## Integration health checks

Run the repository's checks from the root:

```bash
python -m unittest discover -s tests -v
python tools/sync_skills.py --check
python tools/validate_project_memory.py
python tools/validate_tool_registry.py
python tools/discover_codex_runtime.py
python tools/validate_toolkit.py
python tools/evaluate_toolkit.py --validate
```

These checks validate only what their implementations cover. For actual Codex discovery, agent selection, handoffs, permission inheritance, and behavioral quality, use trusted-session tests in `evals/cases/` and grade with the applicable rubric.

## Out of scope

The registry is declarative only. The runtime discovery script only lists sanitized local Codex CLI configuration; it does not install or authenticate MCP servers, start services, or call tools. It does not install Graphify, add vector search, create a persistent workflow database, install n8n/CrewAI, configure WhatsApp/Twilio, add paid APIs, create autonomous agents outside Codex, deploy, or change GymSync application source.