# PROJECT CONTROL CENTER
## Canonical Project State, Operating Manual, Architecture Audit, and Continuity Record

> **MANDATORY — READ THIS FILE BEFORE ANY WORK.**
>
> This is the central control document for the GymSync Codex Toolkit repository. Every new ChatGPT/Codex session, continuation after a context reset, and meaningful handoff must begin with the **Quick Start / Current State** section below, then read `AGENTS.md`. Retrieve only the linked source files relevant to the active task; read the full history only for broad audits or when explicitly required. No project work may begin until the active task, constraints, and next action are understood.
>
> If this file is missing, inaccessible, contradictory, or materially stale, stop. Reconstruct the state from current repository evidence and explicit user decisions before doing any implementation or making a new plan.
>
> This document is the project's central index and operating contract. Detailed procedures, source files, schemas, test cases, and reports remain authoritative for their specific subjects. Do not copy all technical detail into this file; link to the source of truth.

**Document status:** ACTIVE — canonical project checkpoint and operating manual  
**Last architecture decision:** 2026-11-25 — user-approved GymSync Intelligent Agent Ecosystem specification  
**Canonical architecture:** [Intelligent Agent Ecosystem Architecture](docs/intelligent-agent-ecosystem-architecture.md)  
**Repository:** `kuuriyawep/-gymsync-codex-toolkit`  
**Default branch:** `main`  
**Repository visibility:** GitHub API reported Public on 2026-11-28, conflicting with the user's Private intent; unresolved. Do not change without explicit approval.  
**Project owner / final decision authority:** User  
**Primary coordinator:** Codex  
**Toolkit runtime status:** Repository-side artifacts exist; live Codex runtime is unavailable to the user, so behavioral/runtime acceptance remains BLOCKED / NOT_RUN  
**CI policy:** Inspect GitHub Actions for the exact current HEAD; prior PASS results do not transfer to later commits.  
**Document maintenance rule:** Update after each meaningful workstream transition, approved decision, completed audit, or handoff.

## QUICK START / CURRENT STATE

- **Primary roadmap:** The seven gated workstreams in `docs/intelligent-agent-ecosystem-architecture.md`. This is the approved target architecture and supersedes the earlier Phase 11 readiness audit as the active development roadmap.
- **Current active workstream:** WS3 — Agent Collaboration. WS1 merged via PR #15; WS2 merged via PR #16 (merge commit `306698dbee9a1fed142dcdb7504a85a02479c6a8`). The independent QA/security audit may be supplied later and does not block starting or continuing work; assess and address its findings when received.
- **Architecture decisions:** HIGH event-driven autonomy; bidirectional WhatsApp; proactive proposals triaged by Codex; Codex remains central coordinator; user retains final authority. Full constraints and protocols are in the canonical architecture document.
- **Existing toolkit inventory:** 13 native skills and 13 portable mirrors (all content hashes match); six native agents and six role briefs; 62 evaluation case specifications; workflow ledger, schemas, tool registry, memory/repository-intelligence documentation, and deterministic quality workflow. These counts describe repository artifacts, not completed behavioral evaluations.
- **Preservation rule:** Extend existing workflows, handoff/task-graph schemas, tool registry, memory templates, repository-intelligence layer, and evaluation runner. Do not create parallel routers, task engines, handoff contracts, memory stores, or evaluation systems.
- **Current agent roles:** `repo_explorer`, `planner`, `implementer`, `reviewer`, `security_auditor`, and `test_engineer`. Preserve role boundaries; map capability ownership before proposing additional roles.
- **Runtime limitation:** User does not currently have a Codex runtime for live behavioral tests. Continue repository-side design, static implementation, and GitHub CI. Never ask the user to run Codex CLI commands or claim runtime behavior passed without evidence.
- **Integration status:** WhatsApp/Twilio/n8n, Graphify runtime, persistent background execution, and live permission enforcement are not verified or installed. Do not start the n8n trial, install tools, or integrate external services without separate explicit approval.
- **Phase 11 status:** Historical repository-side audit/closeout material remains available. Runtime acceptance remains BLOCKED / NOT_RUN; Phase 11 is not a substitute for the seven-workstream roadmap.
- **Hard boundary:** Toolkit repository only. No GymSync application, database, production, deployment, or external-service changes.
- **WS1 progress:** canonical architecture and role mapping are recorded in `docs/intelligent-agent-ecosystem-architecture.md` and `docs/agent-intelligence-standard.md`. All six native agent TOML definitions and six Markdown role briefs now reference the common intelligence contract and role-specific reporting/proposal behavior. Existing read/write and approval boundaries are preserved. This is repository-side instruction alignment, not runtime validation.
- **WS1 remaining gate:** confirm expanded and legacy result payloads both validate, review the complete PR diff, and verify exact-head CI. Runtime behavior remains BLOCKED / NOT_RUN without a Codex runtime.
- **Immediate next action:** complete WS3 collaboration contracts, tests, checkpoint update, exact-head CI, and independent review. Do not merge without explicit user approval. Audit findings supplied later must be assessed and addressed.



## WS1 continuation checkpoint — 2026-11-28

- Native/portable parity audit: 13 native skills and 13 portable mirrors; all 13 corresponding Git blob hashes match. No missing, extra, or divergent skill files.
- Exact-head CI for commit `6e063c5e95c0cf1119296cc3c3d664e04c110999` passed all quality steps, including unit tests, native/portable parity, project-memory validation, secret scan, toolkit validation, evaluation-case validation, deterministic evaluation generation, and result validation.
- Added regression coverage for the complete optional intelligence report payload and rejection of an invalid tool-invocation status. This change is on WS1 branch and requires a fresh exact-head CI result.
- Legacy result compatibility remains explicitly tested through the existing `validate_result` contract.
- Seven new behavioral evaluation specifications are present; they remain specifications, not runtime results.
- No live Codex agent execution, background monitoring, WhatsApp integration, or runtime autonomy is claimed.

# PART I — WHY THIS PROJECT EXISTS

## 1. Origin and motivation

This project was started to create a dedicated, reusable Codex toolkit rather than repeatedly giving Codex long instructions in every new chat or project.

The underlying problem is continuity and execution quality:
- Large engineering projects contain many files, decisions, constraints, dependencies, and unfinished tasks.
- A new AI session can lose the exact stopping point, repeat earlier planning, misunderstand decisions, or re-read large parts of the repository.
- Generic prompts alone do not provide reliable workflows, ownership boundaries, verification rules, reusable project knowledge, or measurable evaluation.
- Multiple agents are not useful merely because they can be named. They need bounded roles, actual available tools, clear permissions, verifiable deliverables, and a coordinator that checks their work.
- A toolkit that only produces plans or documentation is insufficient for the user's long-term goal of performing substantial real engineering work.

The repository therefore began as a **Codex-first engineering toolkit**: a reusable system of project instructions, skills, specialist roles, workflows, evaluation assets, memory patterns, and maintenance tools.

## 2. Main purpose

Build one professional, extensible toolkit that helps Codex understand a project, plan work, use available specialists, execute approved tasks, verify outcomes, retain important project knowledge, and resume work across sessions without repeatedly starting over.

Codex must remain the primary coordinator. Other agents and tools may support Codex, but must not silently replace it or become an independent authority.

## 3. Six capability dimensions

The user wants all six dimensions developed together as one coherent system:

1. **Intelligent workflow engine** — understand the request, classify it, assess risk and complexity, select the right procedure, track progress, and prevent work from skipping required gates.
2. **Evaluation and testing system** — test repository artifacts deterministically and assess real Codex behavior with evidence, rubrics, repeatable cases, and regression comparisons.
3. **Knowledge and memory system** — maintain verified project context, architecture, decisions, constraints, source references, and a reliable task checkpoint across sessions.
4. **Delegation and multi-agent review** — use specialists for bounded work, manage dependencies and parallelism, independently review important changes, and resolve disagreements using evidence.
5. **Tooling and verification** — give agents access to real, approved capabilities through suitable tools and integrations; verify their results rather than trusting self-reported success.
6. **Professional documentation and architecture** — keep the system understandable, modular, auditable, maintainable, and safe to extend.

These six dimensions are the project's long-term quality model. They are not evidence that every capability is already implemented.

## 4. Desired end state

The intended system should allow Codex to:
- Understand a repository before making changes.
- Retrieve relevant project knowledge instead of re-reading everything.
- Select a suitable workflow and skill automatically when appropriate.
- Decide whether to work alone or delegate to an existing specialist.
- Give specialists clear task ownership, inputs, boundaries, and deliverables.
- Use real tools when those tools are available, authorized, and correctly configured.
- Coordinate research, design, implementation, database work, testing, security review, and final review.
- Inspect evidence, diffs, logs, screenshots, and test output.
- Stop and request user approval for consequential actions.
- Report precisely what was done, what passed, what failed, what was not run, and what remains.
- Preserve a durable checkpoint so a new session resumes from the actual state.

**Critical distinction:** The desired end state is more capable than the current repository. The audit below explicitly separates implemented capabilities, documented procedures, prepared-but-unexecuted tests, and future work.

---

# PART II — PROJECT IDENTITY, AUTHORITY, AND HARD RULES

## 5. Project identity

This repository is a generic Codex engineering toolkit. Although the repository name contains “gymsync”, the toolkit is not currently a GymSync-specific skill pack.

The user wants to consolidate useful, reusable engineering capabilities from external repositories and adapt them carefully for Codex. The intention is not to copy whole projects or install every framework.

## 6. Authority hierarchy

When instructions or records conflict, use this order:

1. Platform/runtime safety and permission controls.
2. The user's latest explicit decision and the exact approval granted for the current task.
3. Current repository source, tests, schemas, configuration, and latest Git state.
4. `AGENTS.md` — repository-wide operating contract.
5. The applicable workflow, skill, schema, rubric, or technical specification.
6. This file — central project state, constraints, audit findings, roadmap, and resume point.
7. Historical reports, prior conversation summaries, agent statements, and older notes.

If two authoritative sources conflict, do not silently select one. Record the conflict, inspect evidence, and ask the user when the decision is theirs.

## 7. Non-negotiable user constraints

- Work only in this toolkit repository unless the user explicitly expands scope.
- Do not modify the GymSync application repository, its source code, database, deployment, or production data.
- Do not install dependencies, external tools, frameworks, agent runtimes, or services unless explicitly approved.
- Do not integrate n8n, CrewAI, Graphify, WhatsApp/Twilio, or other external systems merely because they appear in the backlog.
- Codex remains the primary coordinator and is accountable for final results.
- Do not create a GymSync-specific skill yet; keep the toolkit generic.
- Do not restart or replace the existing toolkit. Improve the work already completed.
- Do not create a branch or pull request unless requested. Default branch is `main`.
- Obtain explicit user approval before commits or consequential changes unless the user has explicitly authorized the exact action. The current request explicitly authorized the expansion of this project-state document.
- No agent handoff grants additional permissions or changes the parent session's sandbox.
- No production write, destructive operation, permission change, deployment, external communication, or irreversible side effect without explicit approval.
- Never claim a test, audit, agent run, Codex behavior, or integration passed unless it was actually executed and evidence is available.
- Do not allow new ideas or newly discovered repositories to displace the active task automatically.
- Keep completed work, active work, backlog, and runtime-pending work clearly separate.
- Do not change phases, milestones, or acceptance criteria without evidence and appropriate user approval.
- Do not store secrets, access tokens, private keys, credentials, personal data, or production customer data in this repository.

---

# PART III — HOW THE TOOLKIT WORKS

## 8. High-level architecture

The existing architecture is a collection of repository-native components coordinated by Codex:

```text
User request
    |
    v
PROJECT_STATE.md  ---- project status, decisions, active task, constraints
    |
    v
AGENTS.md         ---- mandatory repository operating rules
    |
    v
Workflow Orchestration Skill
    |
    v
workflows/registry.md
    |
    +---- select one primary workflow
    |         |
    |         +---- bug-fix.md
    |         +---- feature-delivery.md
    |         +---- database-backend-change.md
    |         +---- security-audit.md
    |         +---- technical-research.md
    |         +---- release-readiness.md
    |
    +---- load relevant specialist skills
    |
    +---- optional Codex subagents in .codex/agents/
    |         |
    |         +---- bounded handoff
    |         +---- independent review
    |
    +---- retrieve relevant project knowledge
    |
    v
Approved research / planning / implementation
    |
    v
Tests + validators + review + evidence
    |
    +---- deterministic checks
    +---- behavioral evaluation cases and rubrics
    |
    v
Completion report
    |
    v
Update PROJECT_STATE.md and relevant detailed records
```

This is the documented control flow. It does not mean every step is automatically executed by a separate software service. Codex interprets and coordinates the repository instructions in its actual runtime.

## 9. Component-by-component explanation

### 9.1 `PROJECT_STATE.md` — central control center

**Purpose:** Preserve project identity, origin, decisions, current architecture, progress, audit findings, constraints, milestones, and next action across sessions.

**Why it exists:** Conversation history alone is not a reliable technical project database. This file gives every new session a stable, version-controlled starting point.

**Required behavior:**
- Read at the beginning of every session.
- Check the latest Git commit and relevant source before relying on old claims.
- Identify the active task before proposing new work.
- Update after meaningful progress, decisions, phase transitions, and handoffs.
- Keep one clear next action.
- Never invent completed work or test results.

This file is the main project index and operating manual. It is not a substitute for inspecting source code, tests, or detailed reports.

### 9.2 `AGENTS.md` — mandatory operating contract

**Purpose:** Tell Codex the repository-wide rules it must follow.

It defines:
- Codex's coordinator role.
- Adaptive workflow and approval rules.
- Safety, scope, and secret-handling constraints.
- Agent boundaries.
- Evaluation and evidence honesty.
- Skill usage and learning rules.
- Mandatory reading of `PROJECT_STATE.md` before any work.

**Authority:** It governs repository behavior. The detailed workflow registry and workflow files own routing and procedures; this file should not duplicate every technical procedure.

### 9.3 `.agents/skills/` — canonical skills

**Purpose:** Reusable procedures Codex can discover in a project workspace.

There are 13 canonical skills:

| Skill | Responsibility |
|---|---|
| `change-impact-analysis` | Map affected components, data flows, dependencies, trust boundaries, compatibility, and rollback concerns before implementation |
| `clear-technical-communication` | Communicate findings, evidence, uncertainty, decisions, and execution status clearly |
| `code-review` | Independently inspect changes for correctness, security, regressions, and test gaps |
| `documentation-and-decisions` | Maintain traceable documentation and engineering decision records |
| `implementation-planning` | Produce bounded, dependency-aware plans with acceptance criteria and verification |
| `project-intelligence` | Retrieve and maintain evidence-backed project knowledge across sessions |
| `requirements-clarification` | Resolve material ambiguity and define observable acceptance criteria |
| `risk-aware-tdd` | Test approved behavior changes and implement focused changes with risk-proportionate verification |
| `security-review` | Perform defensive security review of identity, authorization, data, APIs, dependencies, and deployment boundaries |
| `skill-authoring-and-evaluation` | Create, audit, score, and evaluate reusable skills |
| `systematic-debugging` | Reproduce and diagnose defects, trace causes, and prepare regression scenarios |
| `verification-gate` | Perform final acceptance checks and report evidence-backed PASS / FAIL / BLOCKED status |
| `workflow-orchestration` | Coordinate routing, task state, delegation, approval gates, and completion |

**Ownership rule:** Skills provide specialist procedures. They do not independently authorize actions or override repository-wide rules.

**Important boundary already implemented:**
- `systematic-debugging` owns diagnosis.
- `risk-aware-tdd` owns approved behavior tests and implementation.
- `verification-gate` owns final acceptance.
This prevents the three skills from duplicating each other's responsibilities.

### 9.4 `skills/` — portable skill mirrors

**Purpose:** Provide a portable catalog of the same skills for browsing and selective adoption.

**Source of truth:** `.agents/skills/` is canonical. The portable `skills/` directory must match it exactly.

**Verification:** `python tools/sync_skills.py --check` checks parity. `--write` copies canonical files to the mirror and should only be used when intentionally synchronizing.

The latest full tree audit found 13 canonical skill files and 13 portable mirrors. The tree showed matching blob SHA values for all corresponding pairs.

### 9.5 `.codex/agents/` — executable Codex subagent definitions

The earlier architecture snapshot contained five native TOML definitions. The later Phase 11 inventory supersedes that count: six native definitions are present, including `test_engineer`. The six current roles are listed below:

| Agent | Role | Permission boundary |
|---|---|---|
| `repo_explorer` | Read-only repository discovery and evidence gathering | No implementation |
| `planner` | Plan, dependencies, risks, acceptance criteria | No implementation |
| `implementer` | Implement explicitly user-approved scope | No scope expansion or unapproved side effects |
| `reviewer` | Independent read-only code review | No implementation |
| `security_auditor` | Defensive read-only security assessment | No exploitation or destructive action |
| `test_engineer` | Owns approved test files, fixtures, evaluation cases, and safe test execution | No production implementation edits |

These are the executable project-scoped Codex agent definitions. Actual availability and execution depend on the Codex client/runtime and trusted project configuration.

**Important:** A TOML definition is not proof that the agent has been invoked or that its behavior has passed evaluation.

### 9.6 `agents/` — readable role briefs

There are six Markdown role briefs corresponding to the six native agent definitions.

**Purpose:** Human-readable role documentation and portable reference prompts.

**Important:** These Markdown files are not the executable subagent definitions. The canonical runtime configuration is in `.codex/agents/`.

### 9.7 `workflows/` — task procedures and routing

There are seven workflow files: one registry and six detailed workflows.

| File | Purpose |
|---|---|
| `registry.md` | Classify requests, assess risk/complexity, select workflow, skills, and agent roles |
| `bug-fix.md` | Diagnose, plan, approve, implement, review, and verify a defect correction |
| `feature-delivery.md` | Deliver a feature through requirements, impact analysis, planning, implementation, testing, and documentation |
| `database-backend-change.md` | Protect schema, data integrity, APIs, authorization, tenant boundaries, and migration safety |
| `security-audit.md` | Perform scoped, defensive, evidence-based security review |
| `technical-research.md` | Compare technical options and record an evidence-backed recommendation |
| `release-readiness.md` | Assess release checks, migration/rollback readiness, risks, and go/no-go status |

**Why both a registry and detailed workflows exist:**
- The registry answers: “Which workflow should be selected?”
- The detailed workflow answers: “How should that task be performed?”
- Skills supply focused specialist procedures.
- Codex coordinates the complete lifecycle.

**Routing rule:** Assess complexity and risk separately. High/critical risk overrides a simple task classification.

### 9.8 `templates/` — reusable work contracts

Templates currently cover:
- Agent handoff.
- Independent agent review.
- Engineering decision records.
- Evaluation reports.
- Workflow/session briefs.
- Project profile.
- Repository map.
- Architecture.
- System inventory.
- Constraints.
- Current task state.
- Decision-record index.

**Purpose:** Make outputs consistent without forcing every small task into unnecessary paperwork.

### 9.9 `docs/` — explanatory and milestone documentation

The documentation set includes:
- Quickstart and installation.
- Toolkit integration map.
- End-to-end illustrative example.
- Selective adoption test.
- Source attribution.
- Quality gates.
- Project Intelligence and memory maintenance.
- Phase 6 agent validation.
- Phase 7 integration evaluation.
- Phase 8 skill audit, remediation, and completion.

Detailed reports are evidence records. They should not be rewritten merely to make the project look more complete. Update them only when the underlying evidence or decision changes.

### 9.10 `evals/` — evaluation system

The earlier inventory snapshot contained 41 evaluation case JSON files. The later Phase 11 audit supersedes this count: 55 evaluation case specifications are present. The following list records the earlier inventory baseline, not current counts:
- 41 evaluation case JSON files.
- 7 rubric files.
- Taxonomy and evaluation instructions.
- Acceptance checks.
- Prepared result/report storage locations are created by the runner when used.

Evaluation has distinct layers:

1. **Deterministic validation:** checks repository artifacts, JSON contracts, case identity, target references, rubric contracts, and selected integrity properties.
2. **Static skill-quality review:** six dimensions scored 0–2; static PASS requires at least 10/12, no zero dimension, and no hard-fail.
3. **Behavioral evaluation:** checks actual Codex behavior using a trusted session, transcript/artifacts, and human grading.
4. **Regression comparison:** compares saved run criteria without overwriting historical evidence.

A case file is a test specification, not a result. CI validation does not prove that Codex selected a skill, invoked an agent, respected an approval gate, or behaved correctly.

### 9.11 `schemas/` — structured contracts

Four schemas are present:
- Evaluation case.
- Evaluation result.
- Evaluation rubric.
- Engineering decision record.

**Purpose:** Give evaluation and decision artifacts a consistent machine-readable shape.

The evaluation runner implements the subset of JSON Schema keywords used by these repository schemas. It is not a complete general-purpose Draft 2020-12 validator.

### 9.12 `tools/` — local maintenance and evaluation scripts

Four Python scripts are present:

| Script | What it does | What it does not do |
|---|---|---|
| `validate_toolkit.py` | Checks skill metadata/parity, agent TOML, workflow sections, evaluation schemas/cases/rubrics, and declared coverage contracts | Does not run Codex agents or judge their behavior |
| `evaluate_toolkit.py` | Lists/validates evaluation cases, validates result records, creates deterministic run records/reports, and compares saved outcomes | Does not launch Codex, invoke a model, or grade behavioral output |
| `validate_project_memory.py` | Checks memory template structure, selected status labels, source markers, secret-like patterns, and dated-page freshness | Does not prove that memory claims are true or secure |
| `sync_skills.py` | Checks or synchronizes portable mirrors from canonical skills | Does not author or evaluate skill quality |

These scripts use the Python standard library. Python 3.11+ is recommended for full TOML parsing.

### 9.13 `tests/` — automated unit tests

Four test files are present:
- Evaluation runner tests.
- Project-memory validator tests.
- Skill-quality coverage/rubric contract tests.
- Agent-coordination criticality contract tests.

The latest CI run executed the test suite successfully. The latest historical report records 38 passing unit tests on the earlier code-bearing revision. Do not assume that exact test count is permanent; use the latest run's logs for exact counts.

### 9.14 `.github/workflows/quality.yml` — continuous integration

The GitHub Actions quality pipeline runs on pushes and pull requests targeting `main`.

It currently:
1. Sets up Python 3.11.
2. Runs unit tests.
3. Checks native/portable skill parity.
4. Validates project memory.
5. Validates the toolkit.
6. Validates evaluation cases.
7. Generates a deterministic evaluation record.
8. Validates the generated result record.

Workflow permissions are `contents: read`. CI does not merge, deploy, commit, or change repository settings.

### 9.15 `references/` — policy references

- `permissions-and-approval.md` defines default read-only posture, approval requirements, least privilege, secret handling, and stop conditions.
- `source-adaptation.md` defines how external source material may be inspected and adapted without blind copying or unlicensed verbatim reuse.

### 9.16 `learning/` — controlled learning

The repository separates:
- `learning/inbox/` — proposed lessons awaiting review.
- `learning/approved/` — lessons approved for reuse.

This is a controlled learning structure, not an autonomous self-modifying system. No lesson should silently rewrite toolkit instructions.

---

# PART IV — THE REQUIRED END-TO-END WORK PROCESS

## 10. How every non-trivial task must run

The normal documented lifecycle is:

`INTAKE → TRIAGE → DISCOVERY → PLANNING → APPROVAL → EXECUTION → VALIDATION → REVIEW → COMPLETION`

Use `NEEDS_CLARIFICATION`, `AWAITING_APPROVAL`, `BLOCKED`, or `FAILED` when required. Do not skip a failed gate.

### Step 0 — Session recovery (mandatory)

1. Read this complete `PROJECT_STATE.md`.
2. Read `AGENTS.md`.
3. Inspect the latest branch and commit.
4. Locate the current active task and its detailed workflow/report.
5. Check whether the last task was completed, partially completed, blocked, or awaiting approval.
6. Resume that task. Do not start a new phase because a new chat has started.

### Step 1 — Intake

Extract:
- What the user wants.
- Why the outcome matters.
- Target repository/environment.
- Exact scope and non-goals.
- Existing decisions and constraints.
- Expected deliverable.
- What would count as completion.

Use prior conversation/project state where available. Do not ask the user to repeat known facts.

### Step 2 — Triage

1. Select one primary task category in `workflows/registry.md`.
2. Record secondary concerns only when they add real requirements.
3. Assess complexity separately from risk.
4. Choose a lightweight path only for simple, low-risk, reversible work.
5. High/critical risk always triggers stricter gates.

### Step 3 — Discovery and clarification

1. Read the selected workflow and relevant skills.
2. Inspect current source, tests, schemas, configuration, and relevant documentation.
3. Use read-only discovery first.
4. Separate VERIFIED facts, ASSUMPTIONS, HYPOTHESES, UNKNOWNS, and STALE claims.
5. Ask one focused question only when a missing decision materially changes correctness, risk, scope, or cost.

### Step 4 — Planning

For non-trivial work, define:
- Ordered tasks.
- Expected files/components.
- Dependencies.
- One accountable owner per task.
- Acceptance criteria.
- Test and review plan.
- Risks and mitigations.
- Rollback/recovery.
- Approval gates.

A plan is not approval to implement.

### Step 5 — Approval

Obtain explicit approval before:
- Destructive commands or data deletion.
- Production writes or backfills.
- Schema migrations or permission/RLS changes.
- Deployment.
- External communication or side effects.
- Broad refactors or material scope expansion.
- New dependencies, frameworks, external services, or agent runtimes.

Approval must identify the action and scope. Old approval does not authorize a new task.

### Step 6 — Execution

Codex decides whether to work alone or delegate.

Delegate only if:
- An existing specialist fits the work.
- The task can be bounded.
- Inputs and expected output are explicit.
- Ownership is clear.
- The work can be verified.

Use `templates/agent-handoff.md` for meaningful assignments.

Parallelize only independent work with non-overlapping write ownership. Sequence dependent work and shared-file edits. The implementer cannot expand scope or assume approval from the handoff.

### Step 7 — Review

For complex, security-sensitive, or high-impact work:
- Use an independent read-only reviewer where available.
- Provide the exact revision and acceptance criteria.
- Do not tell the reviewer what verdict to return.
- Compare findings with source and test evidence.
- Keep unresolved disagreements visible.

### Step 8 — Verification

1. Map each acceptance criterion to evidence.
2. Inspect the complete final diff.
3. Run focused tests first, then proportionate broader checks.
4. Record exact commands and actual outputs.
5. Classify checks as PASSED, FAILED, SKIPPED, NOT_RUN, or BLOCKED.
6. Never convert missing evidence into PASS.

### Step 9 — Documentation and continuity

Update the relevant detailed documentation, evaluation record, decision record, or memory page when the work changes durable project knowledge.

Update this file with:
- What changed.
- Exact paths.
- Evidence and commit.
- Checks actually run.
- Decisions and approvals.
- Remaining gaps.
- One next action.

### Step 10 — Completion report

Report:
- Outcome: COMPLETE / PARTIAL / BLOCKED / FAILED.
- Scope and workflow used.
- Files changed.
- Evidence.
- Checks run and outcomes.
- Checks not run and why.
- Review findings.
- Residual risks.
- Next action, if work remains.

A task is not complete because an agent says it is complete. Codex must verify the evidence.

---

# PART V — FULL REPOSITORY AUDIT

## 11. Audit scope and method

**Audit type:** Static repository and architecture audit.  
**Audit date:** 2026-11-16.  
**Repository revision inspected:** `b8aafe780a181f0f49acaed3dc23791ed9146d7c`.

Inspected:
- Complete recursive Git tree.
- Repository metadata and default branch.
- Root instructions and README.
- All 13 canonical skill files.
- All five native agent definitions and five role briefs.
- Workflow registry and six detailed workflow files.
- Main architecture, installation, quickstart, adoption, quality, memory, and source documentation.
- Phase 6, 7, and 8 reports.
- Evaluation guide, taxonomy, rubrics, and acceptance checklist.
- Evaluation schemas and decision-record schema.
- Validator, memory validator, skill synchronizer, and evaluation runner source.
- Unit-test files and GitHub Actions workflow.
- Templates and policy references.
- Recent commits, pull requests, branch protection state, and latest CI run.

**Audit limitation:** All 191 tree entries were inventoried. All 13 canonical skill contents were reviewed and the tree showed matching native/mirror blob SHAs. Core architecture, workflows, agent definitions, validators, tests, and CI were inspected. The 41 evaluation case files were inventoried and the evaluation contracts/validator logic were reviewed, but this audit did not individually behavior-grade all 41 prompts. No local test execution or trusted Codex runtime session was performed by this audit; CI evidence is reported separately below.

## 12. Repository inventory

The recursive Git tree was complete and not truncated.

| Inventory item | Count |
|---|---:|
| Total tree entries | 191 |
| Files | 142 |
| Directories | 49 |
| Canonical skills | 13 |
| Portable skill mirrors | 13 |
| Native Codex agent definitions | 5 |
| Markdown role briefs | 5 |
| Workflow files including registry | 7 |
| Evaluation cases | 41 |
| Rubric files | 7 |
| Schemas | 4 |
| Documentation files | 14 |
| Template files | 13 |
| Unit-test files | 4 |
| Maintenance/evaluation scripts | 4 |

Top-level structure:
```text
.agents/
.codex/
.github/
AGENTS.md
PROJECT_STATE.md
README.md
agents/
docs/
evals/
learning/
references/
schemas/
skills/
templates/
tests/
tools/
workflows/
```

## 13. Current implementation assessment

| Capability | Current state | Audit conclusion |
|---|---|---|
| Repository-wide operating rules | Implemented in `AGENTS.md` | Present |
| Mandatory cross-session checkpoint | Implemented in `PROJECT_STATE.md` and referenced by `AGENTS.md` | Present; this file is now expanded into the central control center |
| Native Codex skill catalog | 13 canonical skills | Present |
| Portable skill catalog | 13 mirrors | Present; matching blob SHAs observed |
| Native Codex subagents | 5 TOML definitions | Present; runtime use still requires Codex validation |
| Agent role briefs | 5 Markdown files | Present |
| Workflow routing | Registry + 6 detailed procedures | Present |
| Handoff and independent review contracts | Templates and agent rules | Present |
| Deterministic evaluation | Runner, schemas, rubrics, 41 cases | Present; CI verified current commit |
| Static skill quality scoring | Rubric and coverage checks | Contract present; individual formal scores remain NOT_SCORED |
| Behavioral evaluation | Cases and human-review rubrics | Prepared; actual Codex behavior NOT_RUN |
| Project knowledge templates | Generic profile/map/architecture/inventory/constraints/current-state templates | Present; templates are not a populated full technical map of every external target project |
| Project memory validator | Python validator and unit tests | Present; structural guardrail only |
| Local tool scripts | Four Python scripts | Present; they are repository maintenance/evaluation utilities, not a general agent tool ecosystem |
| Continuous integration | GitHub Actions workflow | Present; current commit run passed |
| Actual Figma/browser/terminal/API/database tool adapters | No dedicated toolkit integration registry/adapters found in inspected tree | NOT IMPLEMENTED |
| Dedicated designer/database/researcher agent roles | Not among current five native agents | NOT IMPLEMENTED |
| External orchestration runtime | Explicitly excluded from current architecture | NOT IMPLEMENTED |
| Safe selective adoption runtime trial | Checklist only | NOT_RUN |
| Full Codex skill/agent runtime validation | Requires trusted Codex session | NOT_RUN |

## 14. Key audit findings and gaps

### Finding A — The toolkit is a strong instruction/workflow foundation, not yet a full tool-enabled agent platform

**Severity:** HIGH relative to the user's end goal.  
**Evidence:** Current top-level architecture contains skills, TOML agents, workflow Markdown, templates, evaluation scripts, and CI. No dedicated registry of external tools, tool adapters, permission manifests, credential references, or executable integration layer was identified in the inspected repository tree.

**Meaning:** Current agents are guided by instructions and can use whatever tools the parent Codex environment actually provides. The repository itself does not yet provide a unified system for registering, assigning, validating, and governing Figma, browser, terminal, Git, API, database, or other external capabilities.

**Required direction:** Design a tool ecosystem and capability/permission contract before claiming that the toolkit can perform all the real-world work the user wants. Do not install or integrate tools until the design and source audits are approved.

### Finding B — Only five specialist roles currently exist

**Severity:** MEDIUM/HIGH.  
**Evidence:** Five native definitions exist: Explorer, Planner, Implementer, Reviewer, Security Auditor.

**Meaning:** These roles cover core engineering coordination but do not yet provide dedicated design, research, database, test automation, or integration-specialist ownership.

**Required direction:** Decide whether future work should add specialist roles or extend current agents with tool-backed capabilities. Avoid adding agents whose tools and outputs are not defined.

### Finding C — Project Intelligence is currently Markdown-based, not an automatic knowledge graph or database

**Severity:** HIGH relative to the user's cross-session knowledge goal.  
**Evidence:** `docs/project-intelligence.md`, `docs/memory-maintenance.md`, `templates/project-memory/`, and `tools/validate_project_memory.py`.

**Meaning:** The existing system offers structured Markdown templates, retrieval discipline, evidence labels, freshness checks, and a current-state template. It does not automatically index every source file, create embeddings, maintain a vector database, watch Git changes, or autonomously update project knowledge.

**Required direction:** Preserve the current lightweight system as a source-of-truth layer. Evaluate Graphify and other knowledge-graph options separately; resolve the existing Graphify decision conflict before adopting or excluding it permanently.

### Finding D — Runtime behavior remains unverified

**Severity:** HIGH for any claim of production readiness.  
**Evidence:** `docs/agent-validation.md`, Phase 7/8 reports, evaluation cases, and behavioral rubrics.

**Meaning:** Static file presence and CI cannot prove skill selection, correct delegation, approval enforcement, parallel-write safety, independent review, or truthful runtime reporting.

**Required direction:** When a trusted Codex environment is available, run the prepared behavioral cases one at a time, capture transcripts and artifacts, grade them, and preserve immutable results.

### Finding E — Static skill-quality scores are not recorded

**Severity:** MEDIUM.  
**Evidence:** `evals/rubrics/skill-quality.md` and `skill-quality.json` define a six-dimension 0–2 rubric; Phase 8 completion report says formal per-skill scores are NOT SCORED.

**Required direction:** Perform the 13 skill reviews dimension-by-dimension with evidence. Do not infer a score from the fact that the skill files were edited or CI passed.

### Finding F — The evaluation case inventory is larger than the executed behavioral evidence

**Severity:** MEDIUM.  
**Evidence:** 41 case files are present; evaluation runner deliberately marks behavioral criteria NOT_RUN until reviewed Codex evidence is provided.

**Required direction:** Keep authored cases, deterministic validation, static scores, and actual runtime results as separate evidence types. Review case quality and overlap as a dedicated task.

### Finding G — External source audits are not yet consolidated into a complete adoption decision

**Severity:** MEDIUM/HIGH.  
**Evidence:** `docs/source-attribution.md` records conceptual influences from the original foundational repositories. Later capability-source candidates are tracked in this file but do not yet have complete technical audit reports.

**Required direction:** Complete the source-by-source technical audits before deciding what to adopt. Verify license, maintenance, security, dependencies, compatibility, and actual code behavior; do not blindly copy.

### Finding H — Graphify status is inconsistent and needs a deliberate decision

**Severity:** MEDIUM.  
**Evidence:** Current README and `evals/acceptance-checks.md` state that Graphify is intentionally excluded. Earlier user context identified Graphify as important to repository/file knowledge and asked whether it should be used directly or incorporated.

**Required direction:** Treat this as an unresolved decision, not as a settled user rejection. Do not install, integrate, or permanently remove it from consideration until the user resolves the intended approach after the source audit.

### Finding I — The source attribution register and later source inventory cover different groups

**Severity:** MEDIUM.  
**Evidence:** `docs/source-attribution.md` lists ECC, Hermes Agent, Matt Pocock Skills, Superpowers, OpenCode, Anthropic Skills, and Caveman. The later capability-source inventory includes CLIProxyAPI, n8n, Claude Plugins Official, UI UX Pro Max, Frontend Slides, Academic Research Skills, and Vercel Skills.

**Required direction:** Maintain two clearly named categories: foundational conceptual influences and candidate capability sources. Update attribution only after the exact source and adaptation are verified.

### Finding J — Repository governance needs attention

**Severity:** MEDIUM.  
**Evidence:** GitHub repository metadata reports the default `main` branch with branch protection disabled. Repository metadata reports no declared license, and the recursive tree did not show a root LICENSE file.

**Meaning:** The repository is public, but public visibility does not itself grant a reuse license. The lack of branch protection means GitHub does not enforce required checks/reviews before changes to main.

**Required direction:** Decide whether to add an explicit license and whether to enable branch protection / required CI checks. These are governance decisions and must not be changed without user approval.

### Finding K — Full Markdown link integrity is not yet certified

**Severity:** LOW/MEDIUM.  
**Evidence:** Earlier Phase 7 report explicitly records a full repository-wide Markdown link audit as NOT RUN.

**Required direction:** Run a complete internal link/path check as a dedicated verification task. Existing targeted checks do not equal a full audit.

### Finding L — Current CI supports one environment configuration

**Severity:** LOW/MEDIUM.  
**Evidence:** `.github/workflows/quality.yml` uses Ubuntu and Python 3.11.

**Meaning:** The repository's automated quality pipeline does not certify Windows/macOS or other Python versions.

**Required direction:** Treat additional platforms/versions as future compatibility work only if the user needs them.

## 15. Repository governance and Git state

Verified repository metadata at audit time:
- Repository is public.
- Default branch is `main`.
- Branch protection is disabled.
- No root license file appeared in the inspected tree; GitHub repository metadata returned no detected license.
- The repository had no open issues at the time of the metadata query.
- Pull request #7 was merged; PR #6 was closed without merge; PRs #1, #2, #3, and #5 were merged; PR #4 was closed without merge.

Recent main commits before/at this audit:
- `b8aafe780a181f0f49acaed3dc23791ed9146d7c` — mandatory checkpoint rule in AGENTS.md.
- `98362804724847665e7007744e616b4e2d297932` — initial PROJECT_STATE.md.
- `1bf38d4a4896715314dc779e1ff8ec51e4b9f417` — Phase 8 verification wording.
- `d518ece9ad9daa78d5d1e475300863c7157a0300` — Phase 8 CI wording.
- `e200bb647cf9971dd9958eca7256d6d7eb160fde` — Phase 8 CI evidence consolidation.

Do not assume old feature branches or closed PRs represent current main-branch state. Inspect the latest branch and commit before acting.

## 16. Latest CI evidence

## CI status for the expanded checkpoint

- Previous checkpoint commit `b8aafe780a181f0f49acaed3dc23791ed9146d7c`: PASS, run [#43918625052](https://github.com/kuuriyawep/-gymsync-codex-toolkit/actions/runs/43918625052).
- Expanded checkpoint commit `253710c93ae4795ccb5dbf405e39a2516b20c9c3`: CI run [#43920439162](https://github.com/kuuriyawep/-gymsync-codex-toolkit/actions/runs/43920439162) was IN_PROGRESS when this checkpoint was authored. Re-check the run before marking this documentation task fully verified.

Recent successful CI evidence for the checkpoint work:
- Run [#43918625052](https://github.com/kuuriyawep/-gymsync-codex-toolkit/actions/runs/43918625052) passed on audit-baseline commit `b8aafe780a181f0f49acaed3dc23791ed9146d7c`.
- Run [#43920439162](https://github.com/kuuriyawep/-gymsync-codex-toolkit/actions/runs/43920439162) passed on expanded checkpoint commit `253710c93ae4795ccb5dbf405e39a2516b20c9c3`.
- Run [#43920500428](https://github.com/kuuriyawep/-gymsync-codex-toolkit/actions/runs/43920500428) passed on checkpoint update commit `cfcc19f6e633c8989d3c20c3293510d8d9575a0b`.
- Run [#43920585918](https://github.com/kuuriyawep/-gymsync-codex-toolkit/actions/runs/43920585918) passed on checkpoint update commit `1c59fea06c5ee1260d913813406a4d50246f663d`.

All substantive quality-gate steps passed on those recorded revisions. For any later commit, inspect its own Actions run before claiming CI PASS. CI does not prove Codex runtime or behavioral evaluation.

Earlier Phase 8 evidence remains useful historical context: CI run #109 passed on code-bearing commit `fb7967a4ce7b54a6a4731b92af221f8833be9e2c` with 38 unit tests, 41 cases validated, and zero validator warnings. The latest run above supersedes that run as the newest CI evidence for the current main commit.

---

# PART VI — PHASE HISTORY AND CURRENT STATUS

## 17. Historical milestones

The project has been developed in phases. The records below distinguish completed static work from tests that still require a real Codex runtime.

| Phase | Purpose | Current recorded status |
|---|---|---|
| Phase 1 | Initial repository foundation and operating rules | COMPLETE according to prior project record; verify original phase report if exact history is needed |
| Phase 2 | Advanced evaluation system | MERGED / STATIC FOUNDATION COMPLETE; see PR #2 and current eval assets |
| Phase 3 | Delegation and multi-agent review | MERGED / STATIC FOUNDATION COMPLETE; see PR #3 and agent contracts |
| Phase 4 | Intelligent/adaptive workflow engine | MERGED / STATIC FOUNDATION COMPLETE; see workflow registry and procedures |
| Phase 5 | Project Intelligence and persistent memory | MERGED / STATIC FOUNDATION COMPLETE; see PR #5 and memory docs/templates |
| Phase 6 | Agent coordination validation | PREPARED; actual behavioral validation NOT_RUN |
| Phase 7 | Final integration evaluation | Static integration review documented; runtime and selective adoption pending |
| Phase 8 | Skill quality audit and remediation | Static remediation COMPLETE; static per-skill scores NOT_SCORED; Codex behavioral evaluation NOT_RUN |

**Phase-number warning:** Older reports sometimes refer to Phase 6 in different contexts (agent validation versus later skill remediation branches). Use the exact report title and commit evidence, not phase number alone, when resolving history.

## 18. Remaining verification backlog

These are known outstanding checks, not completed work:

1. Formal six-dimension static quality score for each of the 13 canonical skills.
2. Actual Codex skill discovery and selection.
3. Runtime execution of the five specialist agents.
4. Seven Phase 6 agent-coordination behavioral scenarios.
5. Behavioral evaluation of workflow orchestration and safety/approval behavior.
6. Safe selective-adoption trial in a disposable target repository.
7. Full Markdown link integrity audit.
8. Review the 41 evaluation cases for quality, duplication, missing scenarios, and target correctness.
9. Archive all selected source reviews and reconcile their adoption mapping into the toolkit.
10. Review repository license and branch-protection governance with the user.

Do not mark any item complete until its evidence is recorded.

---

# PART VII — EXTERNAL SOURCE RESEARCH AND ADOPTION

## 19. Source review policy

The user wants useful capabilities from multiple repositories consolidated into one coherent Codex toolkit.

The objective is **curation and adaptation**, not wholesale copying.

For every source, inspect:
- Repository structure and actual source files.
- Skills, agents, plugins, hooks, tools, APIs, CLIs, and workflows.
- Dependencies and external services.
- License and NOTICE requirements for the exact material.
- Security, credential handling, permission boundaries, and destructive behavior.
- Maintenance status, compatibility, and platform assumptions.
- What is already covered by this toolkit.
- What is unique and valuable.
- What can be adapted for Codex.
- What should be rejected and why.
- Evidence supporting every adoption recommendation.

No source should be installed, copied into the toolkit, or integrated into GymSync merely because its README describes an attractive feature.

## 20. Foundational repositories recorded in source attribution

The existing `docs/source-attribution.md` records these conceptual influences:

1. `affaan-m/ECC` — verification loops, security review, TDD, change-impact analysis.
2. `NousResearch/hermes-agent` — skill metadata and workflow orchestration patterns.
3. `mattpocock/skills` — debugging, code review, TDD, and requirements shaping.
4. `obra/superpowers` — brainstorming, systematic debugging, planning, and verification gates.
5. `anomalyco/opencode` — separation of read-only exploration/planning and implementation permissions.
6. `anthropics/skills` — skill authoring and evaluation methodology.
7. `JuliusBrussee/caveman` — clarity-first communication and concise review reporting.

These are registered as conceptual influences. Exact file-level license review is still required before verbatim reuse.

Graphify is now recorded in docs/source-attribution.md as an optional external knowledge-graph capability, subject to exact version, license, security, and Codex-compatibility validation. It is not mandatory and does not replace durable project records. The canonical disposition is in docs/phase-6-final-synthesis.md.

## 21. Selected external source audit set and archive

The selected nine-source set is archived in [audits/source-reviews/README.md](audits/source-reviews/README.md). The detailed findings are stored in one report per source, and the deduplicated implementation mapping is in [docs/source-adoption-map.md](docs/source-adoption-map.md).

Selected sources:
1. `affaan-m/everything-claude-code` (ECC) — prior partial review carried forward; selected security review, change-impact, verification-loop, and context/decision practices.
2. `NousResearch/hermes-agent` — prior partial review carried forward; selected memory and skill-lifecycle practices.
3. `anomalyco/opencode` — revision-pinned review; adapt typed tool contracts, permission boundaries, plugin lifecycle, lazy discovery, and child sessions.
4. `Graphify-Labs/graphify` — revision-pinned review; optional external knowledge graph, not vendored and not mandatory.
5. `obra/superpowers` — revision-pinned review; adopt selected verification/debugging/skill-TDD/review practices and adapt task-ledger/worktree patterns.
6. `mattpocock/skills` — revision-pinned review; adopt selected review/handoff/ADR/test-seam patterns and adapt dependency-DAG/fresh-context work.
7. `anthropics/skills` — revision-pinned review; adopt evaluation methodology and adapt MCP/design/browser patterns to Codex.
8. `JuliusBrussee/caveman` — revision-pinned review; adapt bounded recoverable compression and fidelity-evaluation patterns only.
9. `n8n-io/n8n` — revision-pinned review; adapt workflow/tool/evaluation architecture only; do not copy or install the n8n runtime.

### Audit evidence qualification

Seven later reviews preserve source revision identifiers and detailed source/documentation findings. ECC and Hermes are carried forward from earlier project work and are explicitly marked PARTIAL because the recovered checkpoint did not preserve exact revisions and complete file-level evidence. They were not re-audited, honoring the user's strict no-duplicate-work instruction. Do not describe those two records as full revision-pinned audits.

The earlier candidate list (Vercel Skills, Claude Plugins Official, UI UX Pro Max, Academic Research Skills, Frontend Slides, CLIProxyAPI, and n8n skills) is not silently promoted into the selected nine-source set. Their audit/adoption status must be tracked separately if the user later selects them.

## 22. Preliminary source priority interpretation

- **P0:** foundational discovery and plugin/extension architecture that may shape the toolkit's extensibility.
- **P1:** capabilities that could materially improve workflows, research, and design.
- **P2:** specialized capabilities that may be useful after core architecture is stable.

Priority means review order, not permission to install or a decision to discard lower-priority repositories.

---

# PART VIII — FUTURE ARCHITECTURE TARGETS

## 23. Tool ecosystem (not yet implemented)

The user's goal is for agents to do real work, not merely describe how work could be done.

A future tool ecosystem may need to support:
- Codex-native tools.
- MCP servers and clients.
- Direct APIs.
- CLI tools.
- Browser automation.
- Local terminal and Git operations.
- Figma/design tools.
- Test runners and browser test automation.
- SQL/database inspection and controlled migrations.
- Security scanners and dependency analysis.
- Notifications and workflow automation, if approved.

Before implementing this layer, define:
1. Tool registry and unique tool identifiers.
2. Capability description and supported operations.
3. Agent-to-tool access mapping.
4. Read/write/destructive permission classification.
5. Approval requirements and runtime permission source.
6. Credential reference and secret-handling contract.
7. Input/output schemas and validation.
8. Timeout, retry, idempotency, and error handling.
9. Evidence/logging requirements.
10. Fallback behavior when a tool is unavailable.
11. Mock/contract tests and runtime acceptance criteria.
12. Codex coordinator ownership and final verification.

Do not invent tool access. The agent may use only tools actually exposed by the current environment and authorized for the task.

## 24. Specialist capability targets

The user has discussed future specialist responsibilities such as:

| Specialist area | Intended work | Required capability before claiming it is functional |
|---|---|---|
| Researcher | Research technologies, inspect repositories, verify sources, compare options | Search/documentation/repository tools and citation/evidence contract |
| Designer | Create and inspect real UI designs and prototypes | Design-tool access such as Figma, asset handling, preview/evaluation workflow |
| Developer | Implement approved code changes | Terminal, Git, code editing, project context, tests |
| Database specialist | Inspect schemas, queries, RLS, migrations, data integrity | Authorized database tools, read-only defaults, migration/approval controls |
| Tester | Run unit, integration, browser, and end-to-end tests | Test runners, browser automation, logs, screenshots, fixtures |
| Security specialist | Defensive security analysis | Static/security scanners, source access, safe test environment |
| Reviewer | Independently inspect code and evidence | Read-only diff/source/test access |
| Coordinator/manager | Maintain task state, delegate, reconcile evidence, report | Codex session control, checkpoint, task and handoff contracts |

These are future capability targets, not current native agents. No new agent should be added without a unique responsibility, tool contract, permission model, evaluation cases, and a clear reason it is better than extending an existing role.

## 25. Codex remains the orchestrator

Future architecture must preserve these rules:
- Codex understands the task and repository context.
- Codex chooses whether to delegate.
- Codex defines bounded tasks and checks outputs.
- Codex resolves technical disagreements using evidence.
- Codex verifies work and owns the final report.
- The user retains approval authority for consequential actions.
- External frameworks may support workflows only if explicitly approved; they do not become the project's primary authority by default.

---

# PART IX — ROADMAP CONTROL

## 26. How roadmap changes are handled

The phase history above is factual project history. The future roadmap must be reconciled with that history before introducing new phase numbers.

Do not casually create a new phase because a new repository or idea appears.

For every proposed next milestone:
1. Identify which of the six capability dimensions it advances.
2. Check whether the capability already exists.
3. Identify dependencies and unresolved decisions.
4. Define measurable deliverables.
5. Define acceptance criteria and evidence.
6. Separate static completion from runtime validation.
7. Estimate risks and tool/environment prerequisites.
8. Obtain user agreement on the scope and order.
9. Add it to the active roadmap only after agreement.

## 27. Canonical forward roadmap

The former proposal in this section is superseded by the user-approved Phase 6 Final Synthesis. The canonical forward roadmap is now in [docs/phase-6-final-synthesis.md](docs/phase-6-final-synthesis.md):

1. Phase 7 — Tool Ecosystem & Integration.
2. Phase 8 — Agent Capability Engineering.
3. Phase 9 — Stateful Workflow Execution.
4. Phase 10 — Evaluation & Reliability.
5. Phase 11 — Real Codex Runtime Validation.

The detailed deliverables, dependencies, security gates, and acceptance criteria in that synthesis are authoritative for future planning. This roadmap does not imply implementation or installation.

---

# PART X — SESSION RULES AND CHECKPOINT MAINTENANCE

## 28. Mandatory new-session protocol

Every new session must do this in order:

1. Read this entire file.
2. Read `AGENTS.md`.
3. Confirm repository identity and default branch.
4. Inspect latest commit and current GitHub Actions status.
5. Inspect the active task and the relevant detailed source documents.
6. Compare the user's latest instruction with the recorded active task.
7. Resume the unfinished task unless the user explicitly redirects it.
8. If the task identity is unclear, ask one focused clarification rather than guessing.
9. Never ask the user to repeat information already recorded here or in the current project context.

## 29. Mandatory task-start record

Before substantial work, identify:
- Task title.
- Why it is being done.
- Scope and non-goals.
- Expected output.
- Relevant files and systems.
- Risk and complexity.
- Approval status.
- Acceptance criteria.
- Dependencies and blockers.
- What will not be changed.

Do not create an unnecessary form for trivial work; keep the task definition concise but explicit.

## 30. Mandatory task-end update

After meaningful work, update this file with:
- Current date.
- Latest commit inspected.
- Active task and status.
- Completed items and evidence.
- Exact changed paths.
- Tests/checks actually run and results.
- Decisions and approval scope.
- Remaining issues.
- One recommended next action.
- Any newly discovered source repositories or capability requirements.

If detailed findings are extensive, create or update a dedicated report and link it here. This file must still contain the executive summary and current disposition.

## 31. Evidence labels

Use these labels consistently:

- **VERIFIED:** directly supported by current source, executed check, official record, or explicit user decision.
- **LIKELY:** strong inference with supporting evidence, but not conclusively established.
- **ASSUMPTION:** temporary premise used to proceed; must be visible and testable.
- **UNKNOWN:** insufficient evidence.
- **STALE:** previously verified but potentially outdated.
- **NOT_RUN:** required action or test has not been attempted.
- **BLOCKED:** a prerequisite or approval is unavailable.
- **NOT_SCORED:** a defined rubric exists but the review score has not been performed.
- **COMPLETE:** the stated scope and acceptance criteria are satisfied with evidence.
- **PARTIAL:** some, but not all, criteria are satisfied.

Never promote ASSUMPTION or LIKELY to VERIFIED without new evidence.

## 32. Commit and change control

- The user approves consequential work and commits according to the current conversation and repository rules.
- Do not commit broad changes under an approval for a narrow documentation task.
- Keep changes focused and inspect the diff.
- Do not rewrite historical evaluation records.
- Preserve old decisions and mark superseded decisions instead of deleting history.
- Do not update a report to say a test passed unless the evidence exists.
- Do not make GymSync changes under any toolkit approval.

---

# PART XI — CURRENT ACTIVE TASK AND RESUME POINT

## 33. Active task

**Task:** Expand the original short `PROJECT_STATE.md` into a complete project control center, operating manual, architecture guide, continuity record, and repository audit.

**Reason:** The user wants a central document that prevents loss of project context between chats and makes the toolkit's purpose, history, architecture, current state, constraints, and next steps clear from beginning to end.

**Scope authorized in the current request:**
- Audit the toolkit repository.
- Explain why the project started and what it is intended to become.
- Explain the architecture and how components work together.
- Record the current implementation state and remaining gaps.
- Record project rules, instructions, and session-resumption process.
- Make this file mandatory before any project work.

**Out of scope:**
- No GymSync application changes.
- No installations.
- No new external integrations.
- No new agents or skills.
- No new phase implementation.
- No source repository adoption.
- No changes to branch protection, license, or repository visibility.

**Audit result:** The comprehensive document is now written from the inspected repository evidence and existing project decisions.

## 34. Current state after this document update

- Initial checkpoint existed and was mandatory through `AGENTS.md`.
- Full repository tree and core architecture were audited.
- This file has been expanded into the central project control center.
- Latest verified CI run on the pre-update checkpoint commit was successful.
- The expanded document itself must now be committed and its CI result checked before the document-update task can be called fully complete.
- No GymSync app code, database, or deployment has been changed.
- No tools or external frameworks have been installed.
- No Codex behavioral tests have been run.

## 35. Single next action

**Next action:** Begin Phase 7 — Tool Ecosystem & Integration — by inspecting current tool/integration-related files and defining the typed registry, adapter, permission, credential-reference, and evidence contracts. Do not install external packages or connect services until the target is explicitly identified, license/security checks are complete, and the required approval is recorded.

---

# PART XII — AUTHORITATIVE REFERENCE LINKS

- [Repository](https://github.com/kuuriyawep/-gymsync-codex-toolkit)
- [README](https://github.com/kuuriyawep/-gymsync-codex-toolkit/blob/main/README.md)
- [AGENTS.md](https://github.com/kuuriyawep/-gymsync-codex-toolkit/blob/main/AGENTS.md)
- [Workflow registry](https://github.com/kuuriyawep/-gymsync-codex-toolkit/blob/main/workflows/registry.md)
- [Toolkit integration map](https://github.com/kuuriyawep/-gymsync-codex-toolkit/blob/main/docs/toolkit-integration.md)
- [Quickstart](https://github.com/kuuriyawep/-gymsync-codex-toolkit/blob/main/docs/quickstart.md)
- [Project Intelligence](https://github.com/kuuriyawep/-gymsync-codex-toolkit/blob/main/docs/project-intelligence.md)
- [Memory maintenance](https://github.com/kuuriyawep/-gymsync-codex-toolkit/blob/main/docs/memory-maintenance.md)
- [Agent validation](https://github.com/kuuriyawep/-gymsync-codex-toolkit/blob/main/docs/agent-validation.md)
- [Phase 7 report](https://github.com/kuuriyawep/-gymsync-codex-toolkit/blob/main/docs/phase-7-completion-report.md)
- [Phase 8 skill audit](https://github.com/kuuriyawep/-gymsync-codex-toolkit/blob/main/docs/phase-8-skill-audit.md)
- [Phase 8 completion report](https://github.com/kuuriyawep/-gymsync-codex-toolkit/blob/main/docs/phase-8-completion-report.md)
- [Evaluation system](https://github.com/kuuriyawep/-gymsync-codex-toolkit/blob/main/evals/README.md)
- [Quality gates](https://github.com/kuuriyawep/-gymsync-codex-toolkit/blob/main/docs/quality-gates.md)
- [Source attribution](https://github.com/kuuriyawep/-gymsync-codex-toolkit/blob/main/docs/source-attribution.md)
- [Latest verified CI run at audit time](https://github.com/kuuriyawep/-gymsync-codex-toolkit/actions/runs/43918625052)

---

# PART XIII — PHASE 6 FINAL SYNTHESIS CLOSEOUT (2026-11-18)

## 36. Canonical synthesis

The completed architecture reconciliation is recorded in:
- [Phase 6 — Capability & Architecture Final Synthesis](docs/phase-6-final-synthesis.md)
- [Source Attribution and Adaptation Register](docs/source-attribution.md)

The synthesis establishes:
- One primary owner for each capability domain.
- Source-by-source ADOPT / ADAPT / REJECT dispositions.
- Cross-source overlap decisions to prevent duplicate skills, agents, registries, and workflow engines.
- Security, provenance, licensing, and installation gates.
- The canonical Phase 7–11 forward roadmap and acceptance criteria.

The synthesis is the canonical forward architecture decision. It does not rewrite historical reports or convert prepared behavioral tests into passed tests.

## 37. Phase 6 synthesis task record

**Task:** Document and reconcile the Phase 6 Capability & Architecture Final Synthesis.

**User authorization:** The user approved writing the synthesis document and reconciling the central checkpoint and source-attribution register.

**Files changed:**
- docs/phase-6-final-synthesis.md — new canonical synthesis.
- docs/source-attribution.md — updated source dispositions, boundaries, and reuse rules.
- PROJECT_STATE.md — updated Graphify disposition, canonical roadmap, and resume point.

**Commits created by the GitHub contents API:**
- Synthesis document: 12397b438c48170157f9849f36d298625ca9a879.
- Source register: b280071b5729b63ca06cb1f21e5a1e8090cff952.
- The PROJECT_STATE update commit is recorded after its write succeeds.

**Checks:** Documentation write responses are recorded. Latest HEAD and CI for the final documentation state must be inspected before claiming repository-level validation. No local tests, Codex runtime tests, or behavioral tests are claimed here.

**Not done:** No GymSync application changes, database changes, deployments, external packages, Graphify, n8n, or other integrations have been installed or connected by this documentation task.

## 38. Installation request clarification

The user also asked to install the work, but the installation target was not specified unambiguously. The possible targets are materially different:
- Install Graphify as an optional repository knowledge-graph tool.
- Install or configure the toolkit's Codex skills/agents in a Codex environment.
- Install a different source package or integration.

Do not guess which target the user intended. Ask for the exact installation target before installing anything. The source/license/security gates in the canonical synthesis remain mandatory.

## 39. Current status and resume point

- Phase 6 Final Synthesis content: documented.
- Source attribution reconciliation: documented.
- Central project checkpoint: updated in this commit sequence.
- Repository-wide final validation: pending latest HEAD/CI inspection.
- Phase 6 closeout: pending confirmation that the final documentation state passes the repository's applicable checks.
- Phase 7: not started.
- Installation: blocked pending clarification of the exact target.
- GymSync app: untouched.

**Single next action:** Inspect the final main HEAD and its GitHub Actions result; then ask which exact target the user wants installed before any installation action.


---

# PART XIV — SOURCE AUDIT ARCHIVE AND CONSOLIDATION (2026-11-18)

## 40. User-authorized consolidation

The user clarified that "install the completed work and audits" means consolidating the completed source-audit work and selected capability decisions into this existing toolkit repository, not installing Graphify or another unrelated package.

### New audit artifacts

Nine source review records were added under `audits/source-reviews/`:
- `01-ecc.md`
- `02-hermes-agent.md`
- `03-opencode.md`
- `04-graphify.md`
- `05-superpowers.md`
- `06-matt-pocock.md`
- `07-anthropic-skills.md`
- `08-caveman.md`
- `09-n8n.md`
- `README.md` — source audit index and evidence qualification.

### Consolidation artifacts

- `docs/source-adoption-map.md` — maps selected source capabilities to current toolkit owners, implementation gaps, non-adoption decisions, and future phases.
- `docs/source-attribution.md` — links the audit archive and records audit completeness limitations.
- `docs/phase-6-final-synthesis.md` — links the source archive and adoption map.
- `README.md` — exposes the audit archive and adoption map.
- `PROJECT_STATE.md` — records the selected nine-source set and current resume point.

### Existing implementation reused; no duplicate imports

The current toolkit already has 13 canonical skills and portable mirrors, five Codex agent definitions, seven workflow documents, 41 evaluation cases, seven rubrics, schemas, validators, tests, and CI.

The source-adoption map identifies the existing owners for security review, change impact, debugging, TDD, code review, verification, decision capture, project intelligence, skill evaluation, workflow routing, agent handoffs, and approval rules. These components are reused rather than cloned from upstream sources.

### Evidence and safety qualifications

- Seven later source reviews have revision-pinned source/documentation findings.
- ECC and Hermes are legacy/partial records because exact revisions and complete file-level evidence were not recovered; no repeat audit was performed.
- Source code was not copied into the toolkit by this documentation consolidation.
- No third-party package, plugin, Graphify, Caveman, OpenCode, Hermes, Superpowers, or n8n runtime was installed.
- No GymSync application/database/deployment files were changed.
- No Codex behavioral/runtime success is claimed.
- License and dependency checks remain mandatory before any future code/package reuse.

### Commits

The following commits were returned by the GitHub contents API while adding the audit archive and adoption mapping:
- ECC report: `332678f93c245af2805b3952edadd45f2cdb6564`
- Hermes report: `b98dbfa8b149a3bfda7cd379b8a647484a7a60c3`
- OpenCode report: `d579157a11c16f1851e77753fcb848542a4fc811`
- Graphify report: `c8313766088edd9181e9ba41383fd58bab7dcece`
- Superpowers report: `673804e09aab22aea6cbf1853b532ab658db9451`
- Matt Pocock report: `d6ed93fcca2a7cb19f9460c9d14a6371bcfb8a2a`
- Anthropic Skills report: `e84644c6b908b24c02c5ed819d2dc680858ec0c8`
- Caveman report: `37dfc86fef791a66dfb17a8f191193cccf555672`
- n8n report: `df63df2bad2f5725e0e726665e4786526213409d`
- Audit index: `edfe0c148614d93cc6a0ee138aa7a44ed947496f`
- Source adoption map: `d81dc1821d1184eeb6af15053b9074fb5041312c`
- README: `81d57d8a720996cb033f24d0580c4cc78d5f6af2`
- Source attribution: `0d1ff199012880a5ec0084816be15fa76f060907`
- Phase 6 synthesis: `34afda045b5f5db0064a01a0f9b6e8be850abda9`

This list is an audit trail of sequential content updates; latest `main` HEAD must be checked separately.

## 41. Current status and resume point

- Source audit archive: recorded for all nine selected repositories.
- ECC/Hermes evidence: PARTIAL legacy records; not re-audited.
- Seven later source reports: revision-pinned source/documentation reviews recorded.
- Source-to-toolkit adoption map: documented and linked.
- Existing skill/agent/workflow/evaluation foundations: inventoried and mapped; no duplicate source bundles imported.
- External package installation: NOT DONE; not implied by "install the work".
- Phase 6 synthesis and audit consolidation: documentation work complete; final repository CI/validation for latest HEAD must still be inspected.
- Phase 7: next phase, not started in this consolidation.
- GymSync application: untouched.

**Single next action:** Run/inspect the toolkit's current quality gates on the latest main HEAD. If they pass, close the documentation consolidation and begin Phase 7 — Tool Ecosystem & Integration — using the source-adoption map as the implementation backlog.


---

# PART XV — PHASE 7 TOOL ECOSYSTEM KICKOFF (2026-11-18)

## 42. Phase 7 authorization and initial implementation

The user directed that the completed source audit work be consolidated into the toolkit and that work then proceed to the next phase. Phase 7 — Tool Ecosystem & Integration — has started.

### Files added

- `schemas/tool-registry.schema.json` — Draft 2020-12 typed registry schema.
- `registry/tools.json` — initial registry with no hypothetical tools and `default_policy: deny`.
- `references/tool-permission-matrix.md` — role-level access, risk, resource/action/effect, approval, hard-deny, and credential-reference policy.
- `docs/phase-7-tool-ecosystem.md` — architecture, source-informed design, threat model, current status, and acceptance criteria.
- `tools/validate_tool_registry.py` — deterministic manifest validator; does not execute tools or connect providers.
- `tests/test_tool_registry.py` — tests for valid/empty registry, duplicate IDs, raw credentials, runtime evidence, destructive approval, malformed risk values, and secret-path traversal.

### Files updated

- `tools/validate_toolkit.py` — invokes the tool registry validator as part of toolkit validation.
- `README.md` — exposes the Phase 7 design, registry, schema, and validation command.
- `docs/toolkit-integration.md` — connects the registry and permission matrix to the existing component map and health checks.
- `docs/phase-7-tool-ecosystem.md` — records the implementation status and next action.

### Safety decisions

- Registry metadata does not grant permission.
- Runtime exposure and platform sandbox/approval controls remain authoritative.
- Default policy is deny.
- Registry is intentionally empty until actual adapters are selected/configured and supported by evidence.
- Raw credentials are rejected; only environment/secret references are permitted.
- Destructive and external operations require approval.
- No shell execution, MCP server, API, database, browser, Graphify, or external service has been installed or connected.

### Validation status

- GitHub Actions for the latest code-bearing commit before the final test update: run #44292691809 was in progress at the time of this checkpoint.
- Latest main commit after the test update: `ecce6ac77bd6eb0e19c3fde56bf2ca65b11d2a18`.
- The run for baseline commit `b70e222a1d89ccf9e816bd3b6b7c1fbc22dd16e5` completed SUCCESS: [run #44292786044](https://github.com/kuuriyawep/-gymsync-codex-toolkit/actions/runs/44292786044). All 10 substantive steps passed, including unit tests, skill parity, project-memory validation, toolkit validation, evaluation-case validation, deterministic run generation, and result validation.
- This CI result validates the baseline commit only; any later commit needs its own run.
- No local test execution is claimed.

## 43. Current active task

**Active phase:** Phase 7 — Tool Ecosystem & Integration.

**Completed in this phase so far:** Initial registry schema, deny-by-default manifest, permission matrix, threat model, deterministic validator, tests, and documentation wiring.

**Remaining:** Latest CI inspection; harden any failures; then select/configure a real adapter only after checking actual host availability and user-approved provider scope.

**Single next action:** Inspect CI for the latest documentation checkpoint, then continue Phase 7 by defining and validating the first real adapter contract only for a provider the user has selected and the current Codex runtime actually exposes.


## 44. CI evidence update

GitHub Actions run [#44292786044](https://github.com/kuuriyawep/-gymsync-codex-toolkit/actions/runs/44292786044) completed with conclusion `success` for baseline commit `b70e222a1d89ccf9e816bd3b6b7c1fbc22dd16e5`. The job's substantive steps all completed successfully:
- Unit tests.
- Native/portable skill parity.
- Project-memory validator.
- Toolkit validator, including the new tool-registry validator.
- Evaluation-case validation.
- Deterministic evaluation generation.
- Generated result validation.

This is deterministic repository CI evidence, not proof of actual Codex runtime tool availability, adapter connectivity, or behavioral performance.


## 45. Phase 7 — runtime discovery implementation (2026-11-18)

### Official Codex behavior reviewed

Current official Codex documentation confirms:
- `codex mcp list --json` lists configured MCP server entries.
- `codex plugin list --json` lists installed plugins.
- `codex mcp add` supports stdio and Streamable HTTP transports.
- `codex mcp login` supports OAuth-capable Streamable HTTP servers.
- `/mcp` in the active TUI displays active MCP servers.
- User configuration is in `~/.codex/config.toml`; trusted projects may also use `.codex/config.toml`.
- The removed `codex mcp-server` command was the host/server mode; Codex still supports connecting to external MCP servers as a client.

Official references are linked in `docs/codex-runtime-discovery.md`.

### Added files

- `tools/discover_codex_runtime.py` — read-only preflight of Codex CLI version, configured MCP server names, and installed plugin names.
- `schemas/runtime-capability-snapshot.schema.json` — sanitized evidence schema.
- `tests/test_runtime_discovery.py` — tests missing CLI, safe name extraction, secret/endpoint redaction, unknown output shape, timeout, and non-zero command behavior.
- `docs/codex-runtime-discovery.md` — operating procedure, official references, and evidence boundaries.

### Updated files

- `tools/validate_toolkit.py` — requires runtime discovery utility, schema, and documentation.
- `README.md` — links the runtime discovery procedure and describes its command.
- `docs/toolkit-integration.md` — adds the preflight to the architecture and health checks.
- `docs/phase-7-tool-ecosystem.md` — records actual Codex commands and separates configured servers from active callable tools.

### Safety properties

The utility does not read `config.toml`, expose environment values, print endpoint URLs or command arguments, install packages, authenticate, start MCP servers, or invoke tools. It calls only:
- `codex --version`
- `codex mcp list --json`
- `codex plugin list --json`

Commands use argument arrays (no shell), a 15-second timeout, and sanitized output. Unknown JSON shapes are reported as unrecognized, not as an empty list.

### Evidence boundary

This is implementation plus mocked unit-test coverage. It is NOT a live runtime test. The user must run the utility on the actual Codex host and inspect `/mcp` in the active session. No provider adapter is registered or installed yet.


## 46. Phase 7 — MCP adapter governance contract (2026-11-18)

### Added files

- `docs/mcp-adapter-contract.md` — lifecycle from candidate through reviewed/configured/session-loaded/verified/monitored/disabled; provider identity, transports, tool schema review, resource/action/effect mapping, permissions, reliability, verification, and incident response.
- `templates/mcp-adapter-review.md` — structured per-server review and explicit approval record.

### Design decisions

- Codex is an MCP client for external servers; do not build on the removed `codex mcp-server` host command.
- Supported connection types for this design are STDIO and Streamable HTTP.
- Configured server entries are not proof of live connectivity or callable tools.
- Tool descriptions, instructions, annotations, schemas, and outputs from a remote server are untrusted data.
- MCP annotations are hints, not authorization.
- Start with one read-only workflow and a narrow tool allowlist.
- Tool-definition changes trigger re-review.
- Never automatically retry non-idempotent or destructive actions.
- No MCP server has been installed, authenticated, started, or called by this change.

### Current Phase 7 deliverables

Registry and permission contract, safe host preflight, snapshot schema, mocked tests, MCP adapter lifecycle contract, and review template are now in the repository. Live runtime discovery and the first actual provider selection remain outstanding.


## 47. Runtime discovery redaction hardening (2026-11-18)

The Codex preflight was tightened after reviewing its data-minimization boundary:
- Removed the SHA-256 digest of raw CLI output; hashes of potentially sensitive output are unnecessary.
- The report retains only command status, parse status, and recognized server/plugin names.
- Non-empty JSON lists with unknown entry shapes now produce `unrecognized`, not a misleading zero count.
- Added a regression test for unknown non-empty entry shapes.
- Updated the snapshot schema and runtime discovery documentation.

No host config values, endpoints, process arguments, environment values, raw stdout, stderr, or derived output fingerprints are retained.


## 48. Phase 7 operation-level permission contract

The tool registry operation schema now requires explicit:
- `resource_scope` — bounded resources/accounts/paths the operation may access.
- `action` — read/list/search/create/update/delete/execute/publish.
- `effect` — none/local-write/remote-read/remote-state-change/external-communication/production-data-mutation.
- Existing risk, idempotency, and approval fields.

The validator now checks schema/validator enum parity and enforces:
- Destructive and external risk always require explicit approval.
- Side-effecting operations cannot declare `approval: none`.
- Create/update/delete/publish cannot claim a read-only effect.
- Read-risk operations cannot claim local/remote/production write effects.
- Every operation must declare at least one resource scope.

These are contract-level checks, not a sandbox. The host's actual permission controls remain authoritative.


## 49. Graphify v0.9.112 static adapter review (2026-11-18)

### Decision

Graphify is registered as one **planned** optional MCP adapter candidate. It is not installed, authenticated, started, connected, or runtime-verified.

### Evidence reviewed

- Exact release: `v0.9.112`, source commit `340268a70a83588d6b3c6de1fffb05326350ef1d`.
- Python range: `>=3.11,<3.15`.
- Package: `graphifyy`; MCP extra available; stdio server entry point `graphify-mcp`.
- License: Apache-2.0 with legacy MIT portions and NOTICE.
- PyPI Trusted Publishing provenance and artifact hashes recorded.
- GHSA-pcc4-rvhr-2pr8 fixed-version threshold is 0.9.70; reviewed release is later.
- Query logging is opt-in in the reviewed source; proposed environment override is `GRAPHIFY_QUERY_LOG_DISABLE=1`.
- MCP source exposes 11 tools: 8 graph-query tools and 3 GitHub PR tools. Only the eight local graph-query tools are registered as candidate operations; the PR tools are excluded.

### Blocking security issue

Graphify MCP tools accept optional `project_path` overrides. The server validates graph files within a `graphify-out` directory, but that is not a single-project boundary. Before runtime approval, use an OS/container sandbox restricted to the intended project or build and test a pinned-path proxy that rejects overrides.

### Repository changes

- `docs/adapters/graphify-v0.9.112-review.md` — exact package, license, provenance, security, data egress, tool inventory, proposed allowlist, and verification checklist.
- `registry/tools.json` — one Graphify candidate with eight typed read-only operations, `availability: planned`, and static-review evidence.
- `tests/test_tool_registry.py` — verifies the committed candidate is not misreported as verified.
- `README.md`, `docs/phase-7-tool-ecosystem.md`, and `docs/source-adoption-map.md` — reflect the candidate's true status.

### Installation status

NOT INSTALLED. No package installation or Codex MCP configuration has been performed. User approval and resolution of the path-scope issue are required before a proof of concept.


## 50. Registry input/output schema enforcement (2026-11-18)

Operation-level `input_schema` and `output_schema` are now required fields in the registry schema. The deterministic validator checks their structural object schema shape, property declarations, and required-property references. The Graphify candidate's eight operations already carry both schemas.

Added a regression test proving malformed input-schema required properties are rejected. This is structural validation of the toolkit's supported schema subset; it is not a full Draft 2020-12 JSON Schema engine.


## 51. Registry schema validation CI correction (2026-11-18)

The first CI run after making input/output schemas mandatory found a validator implementation mismatch: the JSON Schema contract required both fields, but the per-operation validator's required-key set had not been updated. The validator now requires both fields at the instance level as well. Added a regression test for a missing output schema.

CI failure was a genuine contract-validation defect, not a Graphify runtime issue. Re-run the full quality gates on the corrected commit before treating the registry schema work as passing.


## 52. Non-MCP adapter contracts (2026-11-18)

Added `docs/non-mcp-adapter-contracts.md` to complete the Phase 7 adapter design coverage for:
- HTTP APIs.
- CLI executables.
- Browser automation.
- Databases.
- Design/collaboration tools.
- Test and verification runners.

Each contract defines provider identity, resource boundaries, operation schemas, risk/effect/approval, credentials, timeouts, output bounds, retry/idempotency, untrusted-output handling, verification evidence, and disable/revocation rules. No new provider was installed or connected.


## 53. Phase 7 design closeout and Phase 8 handoff (2026-11-18)

### Phase 7 closeout

Phase 7 design/contract acceptance criteria are complete:
- Typed deny-by-default registry with unique IDs.
- Operation-level resource scope, action, effect, risk, idempotency, approval, input schema, and output schema.
- Structural schema/registry validation and negative tests.
- Explicit role permission matrix and hard-deny/approval precedence.
- Threat model and credential-reference boundary.
- MCP lifecycle and per-server review contract.
- API, CLI, browser, database, design, and test adapter contracts.
- Safe Codex host-discovery utility and sanitized snapshot schema.
- Graphify v0.9.112 pinned static review and planned candidate; no package installed.
- No planned/configured adapter is misreported as runtime-verified.

### Final CI evidence

GitHub Actions run [#44294887222](https://github.com/kuuriyawep/-gymsync-codex-toolkit/actions/runs/44294887222) completed SUCCESS for commit `985052a22bf7135784f519105a3c67465ced6c6a`. All substantive quality-gate steps passed:
- Unit tests.
- Native/portable skill parity.
- Project-memory validation.
- Toolkit validation.
- Evaluation-case validation.
- Deterministic evaluation generation.
- Generated evaluation result validation.

The immediately preceding schema-validator commit also passed run [#44294805527](https://github.com/kuuriyawep/-gymsync-codex-toolkit/actions/runs/44294805527).

This closes Phase 7 architecture/contract design only. It does not prove live Codex MCP connectivity or Graphify runtime behavior.

### Deferred runtime work

- Run `tools/discover_codex_runtime.py` on the actual Codex host.
- Inspect the active session with `/mcp`.
- Resolve Graphify's `project_path` override scope using an OS/container sandbox or tested pinned-path proxy.
- Obtain explicit approval before installing Graphify or another provider.
- Perform runtime proof-of-concept and capture evidence in Phase 11.

### Current phase

**Phase 8 — Agent Capability Engineering.**

Next task: inspect the five existing native Codex agents and their role briefs before adding or changing any role. No GymSync application repository, database, deployment, or production data is in scope.


## 54. Phase 8 — initial agent capability audit (2026-11-18)

### Existing five-agent audit

Reviewed all five native TOML agents and matching role briefs:
- `repo_explorer` / `agents/explore.md`
- `planner` / `agents/planner.md`
- `implementer` / `agents/implementer.md`
- `reviewer` / `agents/reviewer.md`
- `security_auditor` / `agents/security.md`

All five native definitions have the required fields and their names match their filenames. The role briefs map to the same five owners. No duplicate native IDs or missing role briefs were found.

### Important Codex runtime constraint

Current official Codex documentation confirms custom agents inherit parent sandbox, approval, provider, and MCP servers; they cannot independently override those controls. Supported feature reductions exist, but no per-agent sandbox or MCP isolation is created. Role instructions are behavioral contracts, not hard security boundaries.

Official source: https://learn.chatgpt.com/docs/agent-configuration/subagents

### Decisions

- Preserve the five existing roles and clarify ownership boundaries.
- Keep Codex as the sole coordinator; do not create a manager agent.
- Recommend a dedicated `test_engineer` only after handoff schemas and write ownership validation exist.
- Defer docs researcher until an approved docs tool is available; defer designer and database specialist until repeatable workflows justify them.
- Do not add roles or change existing agent TOML files in this initial audit step.

### Added files

- `docs/phase-8-agent-capability-audit.md` — existing role inventory, overlap resolution, Codex constraints, candidate role decisions, gaps, and Phase 8 sequence.
- `references/agent-tool-access-matrix.md` — proposed role-to-tool task profiles and actual enforcement layers.

### Active Phase 8 task

Define JSON Schemas for handoffs, agent results, and dependency DAGs; implement deterministic checks for unique ownership, approval scope, read-only result integrity, dependency cycles, and overlapping parallel write scopes.

No GymSync application files, databases, deployments, or production data were touched.


## 55. Phase 8 contract validation integration (2026-11-18)

- Added `validate_agent_contracts.py` to the main toolkit validation path.
- Main validator now checks that the five native TOML agents have matching canonical role briefs.
- Required Phase 8 role audit and tool-access matrix documents are checked.
- README now documents the three JSON schemas and the validator command.
- Added schema files and tests are already committed; latest successful contract-test run is #44295437418 for commit `af1aafadd5fd90414d5917c898029c733f3c2415`.

The next CI run must verify this integrated validation path before adding any new agent.


## 56. Phase 8 — test engineer role added (2026-11-18)

### New agent

- `.codex/agents/test_engineer.toml` — executable Codex custom agent for test strategy, fixtures, test harnesses, coverage, flakiness, and safe test execution.
- `agents/test_engineer.md` — matching role brief.

### Role boundary

The test engineer may write only approved test files, fixtures, or evaluation cases. It must not edit production implementation code, production configuration, or production data. The handoff validator checks test-only paths; the task graph validator checks write ownership and dependency sequencing. These remain procedural controls under the parent sandbox, not independent per-agent isolation.

### Existing role updates

- Implementer now yields test-file ownership to test_engineer when that role is assigned; application-code and test-file write scopes remain disjoint.
- Workflow routing now selects test_engineer for independent test ownership when it materially improves a task.
- `AGENTS.md`, Phase 8 audit, tool-access matrix, and handoff schemas include the new role.

### Validation updates

- Handoff, result, and task-graph schemas now recognize test_engineer.
- Validator allows approved test-only writes and rejects production-code paths for test_engineer.
- Tests cover valid test ownership and rejected production-path writes.
- Main toolkit validation requires the test engineer TOML and role brief.

No new runtime tool or external service was installed. Live agent behavior remains NOT_RUN until a trusted Codex session is available.


## 57. Phase 8 role-boundary refinement (2026-11-18)

- Corrected the Phase 8 audit inventory to six executable agents and six matching briefs.
- Clarified reviewer/security-auditor separation: reviewer owns general correctness, regression, maintainability, and test quality; security_auditor owns dedicated threat/auth/data-exposure assessment.
- Added a test_engineer behavioral evaluation case for test-only ownership and non-overlapping writes.
- Added a positive validator test for approved test-file changes by test_engineer.
- Updated repository-wide agent boundaries and workflow routing.


## 58. Phase 8 path-scope and reviewer-boundary hardening (2026-11-18)

- Agent handoff and task-graph validators now reject absolute paths, Windows drive paths, backslashes, and `.`/`..` traversal in write scopes.
- Result validation rejects unsafe changed-file paths.
- Added regression tests for test-engineer and implementer path traversal.
- Reviewer instructions now focus on correctness, regressions, maintainability, and test quality; security indicators are escalated to the dedicated security_auditor.


## 59. Phase 8 design closeout; Phase 9 handoff (2026-11-18)

### Phase 8 status

**DESIGN COMPLETE — deterministic repository validation passed.**

- Six native Codex agents and six matching role briefs.
- Test engineer added with test-only write ownership.
- Reviewer/security-auditor boundaries clarified.
- Typed handoff, result, and task graph schemas.
- Deterministic validator for approval scope, result evidence, safe repository-relative paths, dependency cycles, and parallel write overlap.
- Workflow registry, role access matrix, handoff/result templates, task graph example, and test-engineer evaluation case updated.
- Full CI run [#44296291486](https://github.com/kuuriyawep/-gymsync-codex-toolkit/actions/runs/44296291486) passed for commit `123e337649076b3f155085d47809ca48861a29be`.

### Deferred to Phase 11

Real Codex agent execution, inherited sandbox/approval behavior, capability feature reductions, parallel scheduling behavior, and behavioral evaluation remain NOT_RUN. The role matrix and validator do not create independent agent sandboxes.

### Current phase

**Phase 9 — Stateful Workflow Execution.**

Next task: design the workflow state machine, durable task ledger/checkpoints, event evidence model, retries, resume, cancellation, timeouts, idempotency, and recovery tests. Preserve Codex as the only coordinator. Do not change GymSync.


## 60. Phase 9 — Stateful Workflow Execution started (2026-11-18)

### Existing capability audit

- `.agents/skills/workflow-orchestration/SKILL.md` defines session-only primary states and handoff guidance.
- `templates/workflow-brief.md` is a manual session checkpoint.
- `PROJECT_STATE.md` is the durable project-level checkpoint.
- `templates/project-memory/current-state.md` and `tools/validate_project_memory.py` support evidence-backed project memory.
- Phase 8 task graph schemas validate dependencies and write ownership but do not persist runtime task events.

These are complementary existing components; Phase 9 must not duplicate or replace them.

### Phase 9 design artifact

- `docs/phase-9-stateful-workflow-execution.md` — explicit state machine, task states, event ledger, snapshot, idempotency, approval gates, recovery, retention, and implementation sequence.
- `schemas/workflow-event.schema.json` — append-only event contract with hash-chain fields.
- `schemas/workflow-snapshot.schema.json` — rebuildable workflow/task state projection.
- README links updated.

### Key decisions

- Codex remains the only coordinator and single writer.
- Event log is source of truth; snapshot is rebuildable.
- Local private store only; no cloud database or service.
- Every mutation requires an idempotency key.
- Raw tool output and secrets are not stored.
- Completion requires all tasks complete, validation passed, and required review passed.
- Interrupted, failed, blocked, timed-out, or cancelled work cannot be reported as complete.

### Active task

Implement the deterministic workflow ledger and tests for state transitions, hash-chain integrity, idempotency, snapshot recovery, approval gates, retries, cancellation, and no false completion. Actual Codex workflow behavior remains reserved for Phase 11.


## 62. Phase 9 resume, validation, and orchestration integration (2026-11-18)

- Added verified `resume` operation; it checks the event chain and snapshot and explicitly does not execute tasks.
- Added workflow schema self-validation and wired it into `tools/validate_toolkit.py`.
- Added tests for resume, schema validity, approval denial, active-task completion blocking, task timeout state, and retry limits.
- Added transitive dependency handling for sequential overlapping writes.
- Added cross-platform guard around file descriptor permission handling.
- Updated workflow-orchestration skill and workflow brief template with private-store and resume/recovery rules.
- CI for these latest updates is pending; do not claim the latest integration passed until its exact-head run completes.


## 63. Phase 9 portable skill and documentation parity (2026-11-18)

- Synchronized `skills/workflow-orchestration/SKILL.md` with the native `.agents/skills/` version after the native skill gained the Phase 9 ledger section.
- Updated README workflow-state explanation to distinguish session-only lightweight state from the optional local event-sourced ledger.
- Fixed the functional-tooling command list and clarified that no hosted database/service is introduced.
- Added durable ledger fields to `templates/workflow-brief.md`.
- Corrected duplicate Phase 9 documentation section numbering.
- Latest-head CI remains pending.


## 64. Phase 9 private-store hardening (2026-11-18)

- Ledger now rejects stores inside any Git working tree, not only inside the toolkit repository.
- On POSIX, store and workflow directories must have private mode `0700`; ledger, snapshot, and lock files use restrictive permissions. Windows relies on filesystem ACLs.
- Documentation now states the hash chain is tamper-evident, not digitally signed, and includes the task transition table.
- Added tests for Git-worktree exclusion and insecure directory permissions.
- CI for this hardening commit is pending.


## 65. Phase 9 closeout; Phase 10 handoff (2026-11-18)

### Phase 9 status

**IMPLEMENTATION COMPLETE — repository CI verified.**

- Append-only event ledger and hash-chain.
- Snapshot replay, verification, resume, and explicit recovery.
- Workflow/task state transitions, approvals, dependency and overlapping-write gates.
- Retry, timeout, cancellation, evidence, validation/review, and completion gates.
- Private local store outside Git worktrees.
- Native/portable workflow skill parity and workflow-brief template integration.
- 117 unit tests passed; all 10 substantive CI steps passed.

Latest verified run: [#44297943897](https://github.com/kuuriyawep/-gymsync-codex-toolkit/actions/runs/44297943897), commit `6f4069dc65314bf4057e7b545d9d1958b22f67d5`.

### Deferred

Live Codex end-to-end behavior, agent scheduling, actual approval enforcement, and concurrent-agent recovery remain NOT_RUN until Phase 11.

### Current phase

**Phase 10 — Evaluation & Reliability.**

First action: inventory all 13 skills, 42 evaluation cases, 7 rubrics, current run records, and Phase 7–9 contract tests. Score static quality and map gaps without duplicating existing coverage.


## 66. Phase 10 evaluation and reliability audit started (2026-11-18)

- Confirmed inventory: 13 native skills, 13 portable mirrors, 42 evaluation cases, 7 rubric files (4 Markdown and 3 JSON), 31 Phase 9 ledger tests.
- No evaluation result/report artifacts are currently tracked in Git. CI's deterministic smoke-test output is ephemeral and is not a behavioral evaluation.
- Reviewed evaluation architecture, status semantics, rubric structure, skill-authoring coverage enforcement, result-record consistency checks, immutable output behavior, and current CI stages.
- First-pass strengths and open gaps are documented in `docs/phase-10-evaluation-reliability.md`.
- Static scoring of all 13 skills, complete case-to-skill mapping, comparison edge cases, schema-subset limitations, and output-path/failure handling audits remain open.
- Do not claim Phase 10 complete until the exit criteria in the audit document are met.


## 67. Phase 10 skill inventory and coverage gap (2026-11-18)

- Inspected the content of all 13 native skills: change-impact-analysis, clear-technical-communication, code-review, documentation-and-decisions, implementation-planning, project-intelligence, requirements-clarification, risk-aware-tdd, security-review, skill-authoring-and-evaluation, systematic-debugging, verification-gate, and workflow-orchestration.
- Confirmed 13 portable counterparts are present; CI is responsible for byte-for-byte parity.
- Identified a scope mismatch: the skill-quality rubric describes case coverage as a skill quality dimension, but the current structured coverage gate targets only `skill-authoring-and-evaluation`. It does not certify 3/2/1 evaluation coverage for all 13 skills.
- Formal per-skill scores are intentionally not assigned yet; first map the existing 42 cases to their targets and taxonomy to avoid unsupported scores or duplicate cases.
- Exact-head CI passed for Phase 10 kickoff commit `b189529c75f291bd30ecb1874446baa247e2fff6`, run [#44298384589](https://github.com/kuuriyawep/-gymsync-codex-toolkit/actions/runs/44298384589).


---

# PART XVI — PHASE 11 KICKOFF & WORKSTREAM 11.1 BASELINE (2026-11-21)

## 68. User-approved Phase 11 execution plan

The user approved the Phase 11 roadmap with these decisions:
- Runtime strategy: Codex-first.
- Coverage: all toolkit capabilities.
- Execution: sequential, gate-based workstreams.
- Codex remains the primary orchestrator.
- OpenCode is an optional limited fallback/comparison only; it is not equivalent proof of Codex behavior.

The approved plan is recorded in `docs/phase-11-execution-plan.md`. It defines nine workstreams, deliverables, acceptance criteria, dependencies, evidence requirements, and exit gates.

## 69. Workstream 11.1 — repository-side baseline

**Status:** PARTIAL — repository baseline verified; actual user-host runtime evidence BLOCKED / awaiting fresh snapshot.

**Baseline report:** `docs/phase-11-baseline.md`.

### Verified repository facts at 2026-11-21

- Repository: `kuuriyawep/-gymsync-codex-toolkit`.
- Default branch: `main`; visibility remains Public by prior user decision.
- Phase 11 plan commit: `d19a48c9080f269282990688d6cce57e3a1517cf`.
- Baseline report commit: `3430789ab95cdc9f03f24c29e7c740ca8b443350`.
- Latest inspected recursive tree was complete (not truncated).
- Current inventory: 13 canonical skills and 13 portable mirrors; six native agent definitions and six matching role briefs; workflow, registry, adapter, evaluation, schema, test, and CI assets are present.
- Exact-HEAD CI for the plan commit passed: run `#44944018499`; all substantive workflow steps succeeded. This is deterministic repository CI only.

### Runtime boundary

Reviewed `docs/codex-runtime-discovery.md`, `tools/discover_codex_runtime.py`, and `tests/test_runtime_discovery.py`.

The utility is read-only and reports CLI version, configured MCP server names, and installed plugin names. It does not expose configuration values/secrets or prove active-session tool availability. The actual session inventory must be captured separately using `/mcp`.

Prior user-reported Codex CLI and `/mcp` observations from 2026-11-18 are historical and must not be treated as current. This assistant cannot execute commands on the user's local Codex host or inspect their active Codex TUI session.

### Outstanding 11.1 criteria

- Fresh Codex CLI version and sanitized runtime discovery snapshot: BLOCKED / awaiting user-host evidence.
- Current configured MCP/plugin inventory: BLOCKED / awaiting fresh snapshot.
- Active Codex session `/mcp` inventory: BLOCKED / awaiting user-host evidence.
- Model availability and safe representative tool invocation: NOT_RUN.

No installation, authentication, runtime configuration, provider connection, or GymSync application change was performed.

## 70. Historical active-task pointer — superseded by the 2026-11-24 closeout

> This section preserves an earlier checkpoint. Its 11.1 active-workstream pointer and instruction not to begin 11.2 are historical and are superseded by sections 71–79. The current task is Package 4, as recorded in section 79.

## 70A. Historical active task and next action

**Active phase:** Phase 11 — Real Runtime Integration & Full-System Validation.  
**Active workstream:** 11.1 — Runtime & Environment Readiness.  
**Status:** PARTIAL / BLOCKED on fresh user-host runtime evidence.

**Single next action:** On the actual Codex host, run `python tools/discover_codex_runtime.py`, inspect `/mcp` in the active Codex TUI, and provide only the sanitized JSON plus non-sensitive CLI/model/server/tool names and connection statuses. Do not share tokens, config files, environment values, or raw authentication output.

Do not begin 11.2 until the 11.1 exit gate is satisfied or the user explicitly accepts a documented runtime blocker.


## 71. Phase 11 consolidated repository-side audit closeout (2026-11-24)

- Completed static/read-only audit coverage for all nine workstreams, 11.1–11.9.
- Added `docs/phase-11-final-audit-report.md` with scope, evidence boundary, workstream dispositions, P0/P1/P2 findings, and the required trusted-runtime acceptance sequence.
- Repository-side audit is complete; Phase 11 is **PARTIAL — NOT FULLY ACCEPTED** because current Codex runtime, live agent/skill/workflow/MCP behavior, runtime security enforcement, and end-to-end evidence remain BLOCKED or NOT_RUN.
- The report does not claim that terminal tests or local validators were executed during this audit.
- No GymSync application changes, installations, authentication, or production-data access occurred.
- The previous active-workstream pointer to 11.1 is superseded by this consolidated status. Runtime acceptance remains an outstanding gate.

**Current Phase 11 disposition:** Repository-side audit COMPLETE; runtime acceptance BLOCKED / NOT_RUN; overall PARTIAL.


## 72. Phase 11 repository remediation checkpoint (2026-11-24)

- Added the consolidated audit report at `docs/phase-11-final-audit-report.md`; linked it and the Phase 11 plan/baseline from README.
- Updated the execution plan to reflect the user's implementation authorization and the accepted 11.1 blocker disposition.
- Reconciled the project-state active-workstream pointer: the repository-side audit spans 11.1–11.9; runtime acceptance remains blocked.
- Added explicit `coverage` labels to the two previously unlabeled memory cases. Updated the project-intelligence scorecard's taxonomy counts to 5 in-scope, 2 near-miss, and 1 edge. Its historical target revision remains stale and the score still requires a fresh review.
- Hardened `tools/workflow_ledger.py` so no event can be appended after terminal COMPLETION or CANCELLED state. Added regression assertions for late checkpoint attempts in both terminal states.
- Changes are committed directly to `main`; no branch or PR was created.
- Exact-head CI status for the latest repository commit has not been retrieved; the GitHub combined-status endpoint returned an empty statuses list. No local test execution is claimed.
- Remaining P1 work includes approval provenance, real-path/symlink containment, permission-profile enforcement, Graphify path enforcement, secret scanning, scorecard revision refresh, and complete case-to-skill mapping.
- Runtime-dependent 11.1–11.9 acceptance remains BLOCKED / NOT_RUN pending a trusted Codex session.

**Current disposition:** repository-side audit and selected static remediations COMPLETE; deterministic verification PENDING; runtime acceptance BLOCKED / NOT_RUN; overall Phase 11 PARTIAL.


## 73. Phase 11 workflow approval hardening (2026-11-24)

- Updated `tools/workflow_ledger.py`: a task with non-empty write_scope and approval_status=approved must now include a non-empty approval_reference, in addition to approved_scope covering write_scope.
- Added `test_approved_write_task_requires_approval_reference` to `tests/test_workflow_ledger.py`.
- This validates presence and scope metadata only; it does not cryptographically or independently prove user approval provenance. Runtime/caller enforcement remains required.
- The earlier terminal-state guard and its regression assertions remain in place.
- GitHub Actions run lookup and combined-status lookup for latest inspected commit returned empty arrays. CI status is UNKNOWN/NOT_RETRIEVED; tests have not been run by this audit.
- Runtime-dependent Phase 11 acceptance remains BLOCKED / NOT_RUN.

**Next action:** Continue remaining repository-side hardening and inspect current CI workflow configuration; do not claim tests passed without execution evidence.


## 74. Phase 11 deterministic CI pipeline added (2026-11-24)

- Added `.github/workflows/ci.yml`, triggered on pushes to main, pull requests, and manual dispatch.
- Pipeline uses Python 3.11 and runs: compileall for tools/tests; unittest discovery; `tools/validate_toolkit.py`; `tools/validate_project_memory.py`; and `tools/evaluate_toolkit.py --validate`.
- Updated the consolidated Phase 11 report to describe the pipeline and clearly state that a configured pipeline is not a passing run.
- First workflow execution has not been confirmed. The commit workflow-run lookup and combined status endpoint returned empty results at the time checked. CI = PENDING/UNKNOWN, not PASS.
- No tests were executed locally by this audit. Runtime acceptance remains BLOCKED / NOT_RUN.

**Next action:** Inspect the first completed CI run; fix deterministic failures with focused changes, then continue remaining Phase 11 static remediation.


## 75. Phase 11 deterministic CI verified (2026-11-24)

- Inspected the existing `.github/workflows/quality.yml` (Toolkit Quality Gates). It already provides the stronger deterministic pipeline; the duplicate `.github/workflows/ci.yml` added during this session was removed to avoid duplicate CI runs.
- GitHub Actions run `45269054140` completed SUCCESS on exact HEAD `c3cf42d99c8cbdf8384a2a80e21f461ee51279a3`.
- Reported successful steps: unit tests; native/portable skill parity; project-memory validation; toolkit validation; evaluation case validation; deterministic evaluation record generation; generated result validation.
- This is evidence-backed deterministic repository PASS for that exact commit. It is not Codex runtime or behavioral PASS.
- Consolidated Phase 11 report updated with the run evidence.

**Current disposition:** deterministic repository quality gates PASS on commit c3cf42d; runtime acceptance remains BLOCKED / NOT_RUN; overall Phase 11 PARTIAL.


## 76. Phase 11 exact-head quality-gate verification refreshed (2026-11-24)

- Rechecked GitHub Actions run 45269149011 and its job steps. The existing Python 3.11 quality-gates job completed SUCCESS; all steps passed, including unit tests, native/portable skill parity, project-memory validation, toolkit validation, evaluation-case validation, deterministic evaluation record generation, and generated-result validation.
- The run tested exact commit db8cec7e5bb1689d6db7a7bedd4049de75e2cc42. The consolidated Phase 11 report now points to this newer exact-head evidence; run 45269054140 on c3cf42d is retained as historical.
- This is deterministic CI evidence only. It does not validate live Codex skill activation, delegation, runtime permissions, MCP calls, approval provenance, or end-to-end behavior.
- Current source audit confirms AGENTS.md requires the complete PROJECT_STATE.md as the cross-session checkpoint, while project-intelligence retrieves only task-relevant memory pages after reading the checkpoint. These are complementary instructions; no change is needed.
- Current repository-side work remains focused on case-to-skill coverage mapping, scorecard freshness, and path/tool boundary review. Do not refresh historical scorecard target revisions without actually re-reviewing their corresponding skill content.

**Current disposition:** deterministic quality gates PASS on db8cec7e; repository-side audit/remediation remains in progress; runtime acceptance BLOCKED / NOT_RUN; overall Phase 11 PARTIAL.


## 77. Phase 11 first three repository-side work packages (2026-11-24)

- Refreshed the 12 previously stale static skill scorecards against the current canonical skill content and repaired evidence anchors that pointed to non-existent headings. The project-intelligence scorecard had already been refreshed. This does not establish runtime behavior or independent human review.
- Added `evals/skill-case-matrix.md` mapping all 55 evaluation cases to the 13 canonical skills. The matrix records cross-cutting mappings and identifies uneven coverage; it is a traceability index, not test execution.
- Re-audited Graphify's registry boundary: all eight operation input schemas omit caller-controlled `project_path`; the validator rejects it; a regression test asserts the rejection. Graphify remains planned, not installed or runtime verified.
- Updated the Phase 11 final audit report and README index.

**Current disposition:** repository-side work packages 1–3 substantially complete; exact-head CI still queued for the latest commits; runtime acceptance remains BLOCKED / NOT_RUN; overall Phase 11 PARTIAL.


## 78. Phase 11 repository-side closeout and Codex runtime handoff (2026-11-24)

- Completed static audit of workflow ledger, evaluation runner, behavioral rubrics, agent-coordination rubric, tool registry, and memory validator boundaries.
- Added regression tests for lexical path validation: accepted repository-relative paths; rejected absolute, traversal, Windows-drive, and backslash paths. Explicitly documented that `safe_path()` is lexical only and does not provide symlink containment or sandboxing.
- Added `docs/phase-11-codex-runtime-acceptance.md` as the single **CODEX-ONLY** checklist for runtime preflight, repository intelligence, 13 skills, six agents/seven scenarios, workflow, memory, tools/MCP, security/recovery, E2E, and immutable evidence records.
- Linked the runtime pack from README and the Phase 11 execution plan and final audit report.
- The 55-case-to-13-skill traceability matrix is complete. Formal minimum coverage is still uneven; no coverage labels were fabricated. The runtime pack marks missing skill coverage as BLOCKED / CASE DESIGN REQUIRED.
- Exact-head deterministic CI must be rechecked after the latest commits. No Codex runtime was available in this workstream, so no behavioral test is claimed.

**Repository-side preparation:** COMPLETE pending exact-head CI.  
**Codex-only runtime:** NOT_RUN / BLOCKED.  
**Overall Phase 11:** PARTIAL — NOT FULLY ACCEPTED.  
**Next action:** verify CI for the latest main commit; then execute the Codex-only pack when a trusted Codex session is available.


## 79. Phase 11 Package 4 — Knowledge & Documentation (2026-11-24)

**Status:** IN PROGRESS — scoped work is on branch `phase-11-package-4-knowledge-documentation`; not merged.

**Branch base:** `f83d1c5cbf9d823fa0b4fdadc7d855a99217e011` (verified `main` HEAD after Package 3 merge).

**Approved scope:**
- **P1-04 — Project checkpoint integrity:** replace the mandatory full-history startup read with a compact authoritative Quick Start and targeted source retrieval; preserve historical records while explicitly marking superseded pointers and inventory counts.
- **P2-04 — Matrix metadata:** update the evaluation case-to-skill matrix snapshot to the verified baseline. The comparison from former snapshot `9f14fc7326665153a3629d86de079f7e07a45eec` to the Package 4 base found no canonical skill-file or evaluation-case-specification changes.
- **P2-05 — Phase 11 report contradictions:** reconcile current dispositions with later repository-side work, without changing runtime blockers or claiming unrun tests.
- **P2-06 — Phase 10 inventory:** label the 2026-11-18 inventory as a historical snapshot, not a current inventory.

**Completed changes so far:**
- `AGENTS.md`: startup now reads the Quick Start and uses task-relevant source retrieval instead of requiring the entire historical state file every session.
- `evals/skill-case-matrix.md`: snapshot target updated to the verified Package 4 base; comparison basis documented.
- `docs/phase-10-evaluation-reliability.md`: inventory section explicitly marked historical; later counts are called out.
- `PROJECT_STATE.md`: Quick Start and historical-state reconciliation are updated.
- `docs/phase-11-final-audit-report.md`: baseline findings now have explicit later dispositions in section 12; verification remains pending.

**Verification:** GitHub Actions run `45386287145` completed SUCCESS on PR-head commit `a0b233d8359c47828ca86643a41337a27d0b010e`; the unit-test and all other quality-gate steps passed. This is deterministic repository CI, not Codex runtime acceptance. The final checkpoint update requires a new exact-head run.

**Safety and approval:** no GymSync files, application code, database, or production data are in scope. No installation or external integration is authorized. Do not merge this branch to `main` until the user explicitly approves after reviewing the final diff and CI evidence.

**Single next action:** await the user's review and explicit merge decision; keep PR #12 open and unmerged until approval.


---

# PART IV — STEP 11 ARCHITECTURE INTEGRATION & READINESS AUDIT

**Audit date:** 2026-11-25  
**Audit type:** Read-only repository and architecture integration review  
**Inspected main baseline:** `b2f66b960c08f003ba0b3033d000459c3b1552a5`  
**Latest CI inspected:** run `45456774700`, SUCCESS on that exact baseline  
**Scope:** Steps 2–10 architecture specifications mapped against existing toolkit sources. No GymSync repository or application was accessed or changed.

## 14. Step-to-repository mapping

| Architecture step | Existing repository foundation | Disposition |
|---|---|---|
| 2 — Adaptive routing | Workflow orchestration skill, workflow registry, agent definitions | Existing foundation; adaptive behavior still requires runtime evidence |
| 3 — Agent collaboration | Six agent definitions, handoff template/schema, task graph, coordination evaluations | Contracts and scenarios exist; live delegation not verified |
| 4 — Autonomy and initiative | Approval policy, agent boundaries, workflow gates | Policy foundation exists; proactive runtime behavior not verified |
| 5 — Communication | Communication concepts and workflow reporting | External bidirectional gateway remains design-only |
| 6 — Task orchestration | Workflow ledger, state/event contracts, dependency and recovery logic | Repository-side orchestration foundation exists; Codex execution is not proven |
| 7 — Memory and knowledge | Project-memory templates, maintenance guidance, repository-intelligence architecture | Retrieval discipline and graph-provider design exist; live retrieval and Graphify are unverified |
| 8 — Evaluation and reliability | Evaluation cases, rubrics, scorecards, runner, deterministic CI | Evaluation infrastructure exists; behavioral scoring requires trusted Codex evidence |
| 9 — Tooling and execution | Tool registry, schemas, permission references, runtime discovery utility | Declarative contracts exist; host-level enforcement and sandbox isolation are not proven |
| 10 — Documentation and governance | Project state, decision-record template, integration map, quality workflow | Documentation and governance foundations exist; release governance is not a complete autonomous release system |

## 15. Existing sources of truth — avoid duplicate implementation

- `AGENTS.md`: repository-wide operating contract and approval boundaries.
- `workflows/registry.md`: primary workflow selection and routing.
- `schemas/agent-handoff.schema.json` and existing handoff template: handoff contract.
- `schemas/agent-task-graph.schema.json`: task/dependency graph contract.
- `tools/workflow_ledger.py`: repository-side workflow state, event and recovery utility.
- `registry/tools.json` and the existing tool permission matrix: declarative tool inventory and operation policy.
- `evals/`, existing rubrics and `tools/evaluate_toolkit.py`: evaluation case and deterministic evaluation system.
- `docs/repository-intelligence-architecture.md`: provider-neutral repository graph architecture and Graphify adoption boundary.
- `docs/toolkit-integration.md`: component integration map, authority, lifecycle and health checks.
- `templates/decision-record.md`: existing decision-record structure.

New work must extend these sources where justified. Do not create a second router, workflow ledger, tool registry, handoff contract, memory authority, evaluation runner, or graph architecture without an evidence-backed gap and an explicit design decision.

## 16. Cross-component dependency order

1. Establish current project state and source authority.
2. Classify the task and select the existing workflow.
3. Build a bounded task plan with ownership, dependencies and acceptance criteria.
4. Retrieve relevant project knowledge and verify it against current source.
5. Select existing agents and tools within the parent task's permissions.
6. Execute in the host runtime; repository schemas and policies do not themselves enforce host permissions.
7. Collect diffs, logs, test results and other reproducible evidence.
8. Perform independent review and applicable security checks.
9. Evaluate results against acceptance criteria and regression suites.
10. Update documentation, decision records and the canonical project checkpoint.

Communication is an optional reporting/approval transport around this lifecycle; it must not become a second orchestrator or bypass Codex/user authority.

## 17. Readiness and unresolved gaps

| Area | Repository-side status | Runtime status |
|---|---|---|
| Agent definitions and role boundaries | Present | Actual delegation NOT_RUN |
| Collaboration and handoff contracts | Present | Handoff behavior NOT_RUN |
| Workflow ledger and dependency contracts | Present | Live orchestration NOT_RUN |
| Project memory and graph design | Present | Retrieval/Graphify NOT_VERIFIED |
| Evaluation cases and deterministic runner | Present | Behavioral evaluation NOT_RUN |
| Tool registry and permission policy | Present | Host enforcement NOT_VERIFIED |
| WhatsApp/n8n communication | Design/backlog only | NOT_RUN |
| Release and governance documentation | Foundation present | Full release lifecycle NOT_VERIFIED |

Critical distinctions:
- A declarative tool permission is not a sandbox or host authorization boundary.
- A workflow ledger is not by itself an agent execution runtime.
- An evaluation case specification is not an executed evaluation.
- A static scorecard is not proof of Codex behavior.
- A Graphify registry candidate is not a connected or verified Graphify adapter.
- A documentation/release checklist is not evidence that a release was built, approved or published.

## 18. Branch, pull request and CI disposition

- Main baseline inspected: `b2f66b960c08f003ba0b3033d000459c3b1552a5`.
- Latest main CI inspected: run `45456774700`, SUCCESS on that exact SHA.
- PR #8 (`toolkit-full-test`) was observed as an open, divergent verification-only proposal in the audit context. Its workflow duplicates neither a missing toolkit capability nor an approved replacement for the existing `.github/workflows/quality.yml`; do not merge it without a fresh comparison and a separate CI decision.
- No branches were deleted, no PRs merged, and no repository settings changed during this audit.

## 19. Step 11 acceptance disposition

| ID | Criterion | Status |
|---|---|---|
| INT-01 | Verify main baseline | PASS |
| INT-02 | Inventory existing architecture foundations | PASS |
| INT-03 | Map Steps 2–10 to repository sources | PASS |
| INT-04 | Identify duplicate-system risks | PASS |
| INT-05 | Map cross-component dependencies | PASS |
| INT-06 | Identify runtime and integration gaps | PASS |
| INT-07 | Inspect relevant branch/PR state | PASS — snapshot only; refresh before any action |
| INT-08 | Inspect latest main CI for audited baseline | PASS |
| INT-09 | Reconcile canonical project checkpoint | COMPLETED BY THIS UPDATE; new commit CI still pending |
| INT-10 | Approve a specific implementation workstream | NOT_GRANTED by this audit |
| INT-11 | Complete trusted Codex runtime acceptance | BLOCKED / NOT_RUN |

## 20. Final Step 11 disposition

**Repository-side architecture integration audit: COMPLETE.**  
**Checkpoint reconciliation: UPDATED in this document.**  
**Runtime acceptance: BLOCKED / NOT_RUN.**  
**Implementation of new runtime capabilities: NOT_STARTED.**

The next implementation task must be selected as a bounded workstream from the gaps above and must extend existing source-of-truth components. The audit does not authorize GymSync changes, installations, external integrations, permission changes, deployments, or broad refactors.



## WS1 implementation checkpoint — 2026-11-27

- Active branch: `ws1/agent-intelligence-core`, based on main `6ae02e704e667c71cfed3c58cf66fefec0c9ec55`.
- Extended `schemas/agent-result.schema.json` with optional, backward-compatible structured fields: reasoning, self-critique, actual tool-use status, memory sources/proposals, collaboration, initiative proposals, and evaluation evidence/status.
- Updated `templates/agent-result.md` and `docs/agent-intelligence-standard.md` to document the extended result contract and preserve governance (proposals are not authorization; memory updates are proposals, not silent writes).
- Added `tests/test_agent_intelligence_report_contract.py` to check capability field declarations, optional-field compatibility, legacy result acceptance by the existing validator, and template requirements.
- **Not yet verified:** no local test execution and no GitHub Actions run for this branch yet. CI and behavioral/runtime validation remain pending.


## WS2 Autonomous Runtime — implementation checkpoint (2026-11-28)

- User authorized the previously presented WS2 scope: lifecycle, event activation, task leases/ownership, bounded retries/timeouts/cancellation, recovery, adapter boundary, and tests.
- Active branch: `ws2/autonomous-runtime`, based on the post-WS1 `main`.
- Added `docs/autonomous-runtime-contract.md` defining Monitoring -> Activated -> Working -> Reporting/Waiting and the future runtime adapter boundary. It explicitly states that no live runtime is implemented or claimed.
- Added `schemas/runtime-event-envelope.schema.json` for source/event identity, event type, issued/expiry timestamps, idempotency, correlation, subscription, target, and untrusted payload.
- Added `schemas/runtime-task-lease.schema.json` for worker/task ownership, fencing token, attempt, heartbeat, expiry, release/revocation state, and approval reference. Lease possession is explicitly not authorization.
- Added `tests/test_autonomous_runtime_contracts.py` with structural and governance assertions. Exact-head GitHub Actions run #46076542547 passed all 12 quality-gate steps after the final schema/test corrections, including the complete unit-test suite, skill parity, project-memory validation, secret scan, toolkit validation, evaluation validation, deterministic evaluation generation, and result validation.
- Existing workflow ledger, event/snapshot schemas, task graph, approval gates, retry/timeout, checkpoint, and recovery remain the source of truth; no second task engine or ledger was introduced.
- Not yet implemented/verified: persistent event monitoring, scheduler integration, distributed lease enforcement, live worker execution, host-enforced identity/permissions, or Codex behavioral autonomy.
- Repository visibility remains unresolved: GitHub API reported Public on 2026-11-28 despite the user's Private intent. No settings were changed.
- PR #16 is open and Ready for Review: https://github.com/kuuriyawep/-gymsync-codex-toolkit/pull/16. Current head: `0d43683a68ba523efaa5e627d37ce68264a87dae`; base: `main`; 5 files changed, 414 additions, 3 deletions. No merge or branch deletion has occurred.
- User (`kuuriyawep`) has confirmed they are the independent reviewer and that a formal, in-depth Independent QA & Security Audit is underway. The audit report must be received and assessed before any merge to `main`.
- Manual static review completed; GitHub currently shows no submitted review records or inline review threads. This does not replace or claim completion of the user's external independent audit.
- Exact-head GitHub Actions run #46076609942 (run number 350): SUCCESS; all 12 quality-gate steps passed on the current head.
- Next action: wait for the formal audit report, address any substantiated findings within approved scope, rerun exact-head CI after changes, and obtain explicit user approval before merge. Do not start WS3 before WS2 closeout.
