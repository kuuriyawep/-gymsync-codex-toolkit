# GymSync Codex Toolkit

A curated, Codex-first engineering toolkit: repository instructions, role-bounded agents, reusable skills, adaptive delivery workflows, safety gates, and evidence-backed learning.

> Codex remains the primary agent. This toolkit does not replace it with another agent framework.

## Adaptive delivery loop

For non-trivial engineering work, the toolkit uses adaptive routing:

**Intake → Triage → Discovery → Planning → Approval → Execution → Validation → Review → Completion**

Simple, low-risk, reversible tasks may use a lightweight path. High- or critical-risk actions retain strict approval and safety gates regardless of complexity. Complexity and risk are assessed separately.

The [workflow registry](workflows/registry.md) maps task categories to the existing detailed procedures. The [workflow orchestration skill](.agents/skills/workflow-orchestration/SKILL.md) defines classification, routing, session state, delegation, and completion rules.

## Repository layout

- `AGENTS.md` — repository-wide operating contract and safety rules.
- `.codex/agents/` — native project-scoped Codex subagents (TOML definitions).
- `agents/` — readable role briefs and portable reference prompts.
- `.agents/skills/` — the 12 Codex-discoverable project skills, including workflow orchestration.
- `skills/` — matching portable Markdown skill catalog for browsing and reuse.
- `workflows/registry.md` — adaptive routing index for task categories, skills, and specialist agents.
- `workflows/` — authoritative end-to-end bug, feature, database, security, research, and release procedures.
- `templates/workflow-brief.md` — session-oriented workflow checkpoint.
- `templates/agent-handoff.md` — required contract for bounded specialist assignments.
- `templates/agent-review-report.md` — structured independent review and conflict report.
- `references/` — permission/approval and source-adaptation policies.
- `evals/` — taxonomy, cases, rubrics, run records, reports, and acceptance checks.
- `learning/inbox/` — proposed lessons awaiting review.
- `learning/approved/` — curated lessons approved for reuse.
- `templates/` — reusable workflow, decision-record, and evaluation-report templates.
- `docs/` — source influence and attribution register.

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

- Graphify is intentionally not included; install it separately if desired.
- No destructive automatic file compression or rewriting.
- No changes to the GymSync application source code.
- No dependency on Claude-, Hermes-, or OpenCode-specific runtime commands.
- No external orchestration framework or persistent workflow database.

## Quality checks

See [toolkit acceptance checks](evals/acceptance-checks.md). The evaluation system distinguishes deterministic artifact checks from behavioral Codex evaluation. An artifact check passing is not evidence that model behavior passed.

## Functional tooling

Dependency-free maintenance utilities under `tools/`:

- `python tools/validate_toolkit.py` checks skill metadata, native/portable skill parity, agent TOML, workflow sections, evaluation schemas, and all evaluation cases.
- `python tools/sync_skills.py` previews differences between native skills and the portable mirror.
- `python tools/sync_skills.py --check` exits non-zero when the mirror is out of sync.
- `python tools/sync_skills.py --write` copies native skill files into the portable mirror. The native `.agents/skills/` tree is the source of truth.
- `python tools/evaluate_toolkit.py --list` lists evaluation cases.
- `python tools/evaluate_toolkit.py --validate` validates case files against the declared schema contract.
- `python tools/evaluate_toolkit.py --run` runs deterministic toolkit integrity checks and creates an immutable evidence-ready run record and Markdown report; it does not launch Codex or grade model behavior.
- `python tools/evaluate_toolkit.py --run --compare evals/results/<previous-run-id>.json` compares stable case/criterion outcomes with a prior run.

Python 3.11+ is recommended for full TOML validation. The scripts use only the Python standard library. The evaluation runner implements the JSON Schema keywords used by this repository's schemas; it is not a general-purpose full Draft 2020-12 validator.

## Continuous quality gates

GitHub Actions runs the dependency-free quality pipeline on pushes and pull requests targeting `main`. It executes unit tests, native/portable skill parity checks, the repository validator, evaluation-case validation, and a deterministic evaluation-run smoke test. The workflow has read-only repository permissions and does not merge, deploy, or modify repository settings.

See [quality gates](docs/quality-gates.md) for local commands, CI behavior, and limitations.

## Evaluation system

Read [evals/README.md](evals/README.md) for the hybrid evaluation process, [taxonomy](evals/taxonomy.md), and [rubrics](evals/rubrics/). Cases live in `evals/cases/*.json` and use `schemas/evaluation-case.schema.json`. Run records use `schemas/evaluation-result.schema.json`; rubric definitions use `schemas/evaluation-rubric.schema.json`. The existing `schemas/decision-record.schema.json` remains the engineering decision-record contract.

Behavioral checks require an actual trusted Codex session and evidence-backed human grading. The runner deliberately leaves those criteria as `NOT_RUN` until that review occurs. Historical run records are never overwritten.
