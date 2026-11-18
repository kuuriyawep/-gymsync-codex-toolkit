# Source-to-Toolkit Adoption Map

**Purpose:** Translate the nine source reviews into one deduplicated implementation plan for the existing Codex-first toolkit.

This is an integration ledger, not a claim that every source capability has already been implemented. Existing toolkit artifacts remain the primary implementation. Source repositories are evidence/reference inputs.

## 1. Existing capability owners

| Capability | Current owner/artifacts | Current status |
|---|---|---|
| Security review | `.agents/skills/security-review/`, `agents/security.md`, `.codex/agents/security_auditor.toml`, `workflows/security-audit.md` | EXISTS — strengthen only where source findings expose a concrete gap |
| Change impact | `.agents/skills/change-impact-analysis/` | EXISTS |
| Root-cause debugging | `.agents/skills/systematic-debugging/` | EXISTS |
| TDD and regression discipline | `.agents/skills/risk-aware-tdd/` | EXISTS |
| Code review | `.agents/skills/code-review/`, reviewer agent | EXISTS |
| Final verification | `.agents/skills/verification-gate/` | EXISTS |
| Decision/context records | `.agents/skills/documentation-and-decisions/` | EXISTS |
| Project knowledge and memory | `.agents/skills/project-intelligence/`, `docs/project-intelligence.md`, `docs/memory-maintenance.md`, `templates/project-memory/` | EXISTS — Markdown/Mnemoverse; not a graph |
| Skill authoring/evaluation | `.agents/skills/skill-authoring-and-evaluation/`, `evals/`, `schemas/`, `tools/evaluate_toolkit.py` | EXISTS — Codex behavioral evaluation remains distinct/pending |
| Requirements and planning | `.agents/skills/requirements-clarification/`, `.agents/skills/implementation-planning/`, planner agent | EXISTS |
| Workflow routing | `.agents/skills/workflow-orchestration/`, `workflows/registry.md`, workflow procedures | EXISTS — persistent state machine is not yet implemented |
| Agent roles and handoffs | `.codex/agents/`, `agents/`, `templates/agent-handoff.md`, `templates/agent-review-report.md` | EXISTS — runtime behavior pending |
| Permission and approval rules | `references/permissions-and-approval.md`, `AGENTS.md` | EXISTS — not a sandbox or complete typed tool registry |
| Tool registry/adapters | No complete central typed registry or real external adapter layer identified | GAP — Phase 7 |
| Durable workflow ledger/state transitions | Workflow briefs/checkpoints exist; no persistent execution database/state machine identified | GAP — Phase 9 |
| Recoverable tool-output compression | No secure original-store/retrieval-handle system identified | GAP — evaluate selectively in Phase 9/10 |
| Optional repository knowledge graph | No Graphify adapter installed | OPTIONAL — Phase 7 design, Phase 11 runtime validation |

## 2. Source contribution → existing owner → action

| Source | Contribution selected | Existing owner / destination | Action |
|---|---|---|---|
| ECC | Security review, change impact, verification loop, context/decision discipline | Security review, change-impact-analysis, verification-gate, documentation-and-decisions, project-intelligence | Reuse current implementations; compare against legacy source notes; add only missing acceptance details |
| Hermes Agent | Memory and skill lifecycle | Project-intelligence, memory-maintenance, skill-authoring-and-evaluation, skill discovery layout | Preserve the Codex-native lifecycle; do not introduce a second memory/runtime owner |
| OpenCode | Typed tool contracts, action/resource/effect permissions, plugin lifecycle, child sessions, lazy loading | Permission reference, Phase 7 tool registry/adapters, Phase 8 agents, Phase 9 workflows | ADAPT contracts; never treat permission prompts as sandboxing |
| Graphify | Repository code/file relationship graph, provenance, incremental refresh | Optional Phase 7 adapter; project-intelligence remains source of truth | Keep external and optional; no vendoring or mandatory dependency |
| Superpowers | Verification-before-completion, systematic debugging, skill TDD, two-stage review, task ledger/worktrees | Verification-gate, systematic-debugging, skill-authoring-and-evaluation, code-review, workflow orchestration | Reuse/strengthen existing skills; ADAPT ledger/worktree patterns; retain user approval before Git side effects |
| Matt Pocock | Standards/spec review, task DAG, fresh-context delegation, handoff redaction, ADR/glossary, test seams | Reviewer agent, planner/implementer agents, handoff template, decision records, TDD/evals | ADOPT unique review criteria; ADAPT DAG/frontier and handoffs; reject automatic issue/Git side effects |
| Anthropic Skills | Skill evaluation lifecycle, A/B, objective graders, trigger precision/recall, holdout sets; MCP schema guidance | Skill-authoring-and-evaluation, evaluation schemas/cases/rubrics; Phase 7 tool contracts; Phase 10 evaluation | ADOPT methodology; reimplement for Codex; do not import Claude-specific scripts unchanged |
| Caveman | Type-aware compression, original preservation/retrieval, fail-closed behavior, fidelity eval | Phase 9/10 context/output handling and evals | ADAPT only after storage security and retrieval controls are designed; no unencrypted CCR |
| n8n | Typed tool catalogs, action schemas, lifecycle events, suspend/resume/cancel, attempt ledger, approval, workflow evals | Phase 7 registry/permissions; Phase 8 delegation; Phase 9 stateful workflows; Phase 10 evals | ADAPT architecture patterns only; do not copy/install n8n runtime or nodes |

## 3. Capabilities already integrated versus future work

### Already represented in toolkit artifacts

- Security review, change-impact analysis, debugging, TDD, code review, and final verification.
- Project intelligence, decision capture, and memory maintenance.
- Skill authoring and evaluation structure.
- Bounded agent roles, handoff templates, and independent review procedures.
- Workflow routing and task procedures.
- Permission and approval rules.
- Deterministic evaluation cases, schemas, rubrics, validators, and CI.

The presence of these artifacts means the toolkit has a static foundation. It does not prove Codex behavior or runtime integration.

### Still requires implementation/design

- One typed tool registry with unique IDs and input/output schemas.
- Explicit action/resource/effect permissions mapped to agent roles.
- Tool adapters with credential references, timeout, idempotency, error normalization, evidence, and fallback contracts.
- Plugin/MCP lifecycle and lazy tool discovery.
- Fresh-context delegation and dependency-DAG contracts beyond the existing role briefs.
- Durable workflow state machine, task ledger, retry/resume/cancel, and recovery.
- Secure, recoverable tool-output handling if compression is adopted.
- Expanded source-informed evaluation cases and measured behavioral evaluation.
- Actual Codex runtime validation.

## 4. Non-adoption and safety decisions

- Do not import 15 Superpowers skills or 27 Matt Pocock skills wholesale.
- Do not import the full OpenCode, Hermes, Caveman, or n8n runtime.
- Do not copy Anthropic's Claude-specific `claude -p` harness unchanged.
- Do not copy n8n Sustainable Use/Enterprise source code into this toolkit.
- Do not install Graphify automatically or make it mandatory.
- Do not use Caveman's unencrypted recovery database as-is.
- Do not enable default-on telemetry or cloud content routing without explicit review.
- Do not adopt auto-commit, auto-merge, issue-writing, or deployment behavior.
- Tool annotations and permission UX are not a security sandbox.
- User approval is still required for commits, merges, pushes, deployments, destructive operations, and consequential external effects.

## 5. Phase sequencing

- **Phase 7 — Tool Ecosystem & Integration:** typed registry, schemas, permission model, adapters, plugin/MCP boundary, optional Graphify adapter design.
- **Phase 8 — Agent Capability Engineering:** specialist role boundaries, fresh-context handoffs, dependency DAG, parallel-write controls, independent review.
- **Phase 9 — Stateful Workflow Execution:** state machine, task ledger, lifecycle events, checkpoints, retry/resume/cancel, recoverable output references.
- **Phase 10 — Evaluation & Reliability:** source-informed tests, A/B and holdout evaluation, fidelity, security, failure/recovery, regression.
- **Phase 11 — Real Codex Runtime Validation:** real skill/tool/agent/workflow behavior, permissions, approval, Graphify optional integration and recovery validation.

Phase work must reuse current owners and avoid duplicate registries, skills, agents, and workflow engines.
