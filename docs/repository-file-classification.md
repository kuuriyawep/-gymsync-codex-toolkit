# Repository File Classification and Loading Policy

**Status:** Accepted repository-maintenance baseline  
**Audited branch:** `main`  
**Audit baseline:** `526df0235e18b2c1701cfa4eae525ac0d9c21bae`  
**Audit date:** 2026-11-24  
**Scope:** File inventory, focused dependency tracing, canonical-source review, and session-loading policy. No files were moved or deleted during the audit.

## Objective

Reduce unnecessary context loading without deleting useful history or breaking the toolkit's validators. The goal is not to minimize the raw file count at any cost. The goal is to make Codex load only the files needed for the current task.

## Loading levels

| Level | Load policy | Contents |
|---|---|---|
| L0 — Always | Every task/session | Root `AGENTS.md`; only the Quick Start / Current State section at the top of `PROJECT_STATE.md` |
| L1 — Task routing | Non-trivial tasks | `workflows/registry.md`, then only the selected workflow and relevant skills |
| L2 — On demand | When the task needs them | Selected `.agents/skills/*/SKILL.md`, `.codex/agents/*.toml`, templates, references, architecture docs, registries |
| L3 — Verification | When validating or changing toolkit internals | Relevant `tools/`, `tests/`, `schemas/`, `evals/`, and CI workflow files |
| L4 — Historical | Explicit historical audit or relevant decision lookup | Phase reports, source reviews, superseded plans, old audit records |

A skill being available does not mean every skill should be loaded. Native agent definitions are consulted only when Codex decides a bounded delegation is useful.

## Directory classification

| Path | Canonical role | Load policy | Decision |
|---|---|---|---|
| `AGENTS.md` | Project operating contract | L0 | KEEP |
| `PROJECT_STATE.md` | Current checkpoint plus continuity index | L0: top section only; historical sections L4 | RESTRUCTURE GRADUALLY; never require full-file startup reads |
| `.agents/skills/` | Canonical Codex-discoverable skills | L2: selected skill only | KEEP CANONICAL |
| `skills/` | Portable mirrors of canonical skills | L3: parity checks; L2 only for portability tasks | KEEP MIRRORS; do not delete as duplicates |
| `.codex/agents/` | Native Codex subagent definitions | L2: only when delegation is justified | KEEP |
| `agents/` | Human-readable role briefs | L2: when reviewing or adapting roles | KEEP; distinct from native TOML |
| `workflows/` | Workflow routing index and authoritative procedures | L1: registry, then selected procedure | KEEP |
| `tools/` | Validators, evaluators, scanners, and maintenance utilities | L3: run/read only for relevant maintenance | KEEP |
| `tests/` | Regression and contract tests | L3 | KEEP |
| `schemas/` | Machine-readable artifact contracts | L3; selected schema only | KEEP |
| `evals/` | Evaluation cases, rubrics, results, and evidence | L3/L4 depending on task | KEEP; behavioral cases are not runtime startup instructions |
| `.github/workflows/` | CI and verification automation | L3 or when diagnosing CI | KEEP |
| `templates/` | Reusable handoff, memory, and report starting points | L2: copy/adapt only when needed | ON DEMAND |
| `references/` | Supporting reference material | L2: selected reference only | ON DEMAND |
| `registry/` | Tool capability and permission declarations | L2: only for tool integration/permission work | KEEP; Graphify entry is planned, not proof of installation |
| `docs/project-intelligence.md` and memory docs | Current Markdown-based project-memory procedure | L2: project-intelligence tasks | KEEP |
| `docs/adapters/graphify-*.md` | Graphify candidate review | L4/L2 for graph integration work | KEEP AS DECISION EVIDENCE |
| `docs/phase-9-*.md`, `docs/phase-10-*.md` | Historical implementation and audit reports | L4 | HISTORICAL / ON DEMAND |
| `docs/phase-11-*.md` | Current audit and Codex runtime acceptance evidence | L4; runtime pack is L2 only during acceptance | KEEP; do not load routinely |
| `audits/source-reviews/` | Historical reviews of external repositories | L4 | ARCHIVE BY INDEX; preserve evidence |
| `learning/` | Learning notes | L2/L4 | REVIEW before promoting to canonical instructions |
| Root `AUDIT_REPORT.md` | Legacy consolidated audit record | L4 | REVIEW references before any move |
| Root README | Human entry point and navigation | L0/L1 | KEEP SHORT; link to indexes |

## Canonical-source rules

1. `.agents/skills/<name>/SKILL.md` is canonical. `skills/<name>/SKILL.md` is a generated/maintained portable mirror; use `python tools/sync_skills.py --check` to verify parity.
2. `.codex/agents/*.toml` is the native Codex configuration. `agents/*.md` is a human-readable role contract. They serve different consumers and are not duplicates.
3. `workflows/registry.md` routes tasks. The linked `workflows/*.md` file owns the actual procedure.
4. Schemas define machine-readable shape; tools implement checks; tests verify behavior. Do not treat a README or report as a substitute for these sources.
5. Current source, configuration, tests, and explicit user decisions outrank graph output, project memory, and historical reports.
6. Do not move or delete files solely because they are large. First verify inbound references, validator manifests, CI paths, and the canonical-source relationship.

## Dependency findings

- `tools/validate_toolkit.py` imports `evaluate_toolkit.py`, `validate_tool_registry.py`, `validate_agent_contracts.py`, `workflow_ledger.py`, and `validate_skill_scores.py`. These form a coupled validation layer; moving them requires coordinated code and test updates.
- The toolkit validator maintains fixed manifests for required skills and workflows. A directory reorganization can silently break integrity checks if those manifests are not updated.
- The skill mirror and native/human agent formats are purposeful duplication across different consumers, not candidates for deletion.
- CI-only tools and evaluation assets are not required to be read at every Codex session.
- Phase reports and external source reviews are evidence/history, not runtime procedures.

## Audit limitations

This is a focused source and dependency audit, not a mathematically complete inbound-link census. The repository inventory covered 225 files and approximately 1.02 MB at the audit baseline. A small number of low-usage areas (`learning/`, `AUDIT_REPORT.md`, and references not traced end-to-end) remain marked REVIEW. No deletion or file movement is authorized by this classification document.

## Maintenance rule

When a file is added, record its canonical owner, consumer, loading level, and verification method in the relevant index. When a file is proposed for archive or removal, first search references and inspect validator/CI dependencies. Preserve historical evidence unless the user explicitly authorizes deletion.
