# PROJECT CONTROL CENTER
## Canonical Project State, Operating Manual, Architecture Audit, and Continuity Record

> **MANDATORY — READ THIS FILE BEFORE ANY WORK.**
>
> This is the central control document for the GymSync Codex Toolkit repository. Every new ChatGPT/Codex session, every continuation after a context reset, and every meaningful handoff must begin by reading this file in full, then reading `AGENTS.md`. No project work may begin until the active task, current status, constraints, and next action are understood.
>
> If this file is missing, inaccessible, contradictory, or materially stale, stop. Reconstruct the state from current repository evidence and explicit user decisions before doing any implementation or making a new plan.
>
> This document is the project's central index and operating contract. Detailed procedures, source files, schemas, test cases, and reports remain authoritative for their specific subjects. Do not copy all technical detail into this file; link to the source of truth.

**Document status:** ACTIVE — canonical project checkpoint and operating manual  
**Last full audit:** 2026-11-16  
**Last verified repository commit:** `b8aafe780a181f0f49acaed3dc23791ed9146d7c`  
**Latest CI:** PASS — run [#43918625052](https://github.com/kuuriyawep/-gymsync-codex-toolkit/actions/runs/43918625052) on the same commit  
**Repository:** `kuuriyawep/-gymsync-codex-toolkit`  
**Default branch:** `main`  
**Repository visibility:** Public (user-selected; do not change without explicit instruction)  
**Project owner / decision authority:** User  
**Primary coordinator:** Codex  
**Toolkit runtime status:** Static repository checks pass; Codex behavioral/runtime validation is still pending  
**Document maintenance rule:** Update this file after every meaningful phase transition, completed audit, approved architecture decision, or handoff.

---

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

There are five native TOML definitions:

| Agent | Role | Permission boundary |
|---|---|---|
| `repo_explorer` | Read-only repository discovery and evidence gathering | No implementation |
| `planner` | Plan, dependencies, risks, acceptance criteria | No implementation |
| `implementer` | Implement explicitly user-approved scope | No scope expansion or unapproved side effects |
| `reviewer` | Independent read-only code review | No implementation |
| `security_auditor` | Defensive read-only security assessment | No exploitation or destructive action |

These are the executable project-scoped Codex agent definitions. Actual availability and execution depend on the Codex client/runtime and trusted project configuration.

**Important:** A TOML definition is not proof that the agent has been invoked or that its behavior has passed evaluation.

### 9.6 `agents/` — readable role briefs

There are five Markdown role briefs corresponding to the five native agent definitions.

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

The current tree contains:
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

<PRIVATE-CI-STATUS>

The latest run at the time of this audit:
- Workflow: Toolkit Quality Gates.
- Run ID: `43918625052`.
- Commit: `b8aafe780a181f0f49acaed3dc23791ed9146d7c`.
- Result: SUCCESS.
- All substantive steps passed: Python setup, unit tests, native/portable skill parity, project-memory validation, toolkit validation, evaluation-case validation, deterministic evaluation generation, and generated-result validation.

This proves the checked repository-quality steps passed on that commit. It does not prove Codex runtime or behavioral evaluation.

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
9. Resolve Graphify status conflict.
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

Graphify is not included in the current attribution register; its status is unresolved as described in Finding H.

## 21. Later capability-source candidates

These repositories were raised for deeper investigation. Their earlier reviews were preliminary; do not treat the summaries below as final technical audits.

| Candidate | Potential contribution | Preliminary priority | Audit status |
|---|---|---:|---|
| `vercel-labs/skills` / find-skills | Discover skills, add/list/check/use, track compatibility and content | P0 | Preliminary review only |
| `anthropics/claude-plugins-official` | Plugin packaging, agents, skills, MCP configuration, hooks, commands | P0 | Preliminary review only |
| `n8n-io/n8n` | Workflow automation, integrations, human approval, external services | P1 | Preliminary review only |
| `nextlevelbuilder/ui-ux-pro-max-skill` | Design intelligence, UI/UX references, tokens, palettes, typography | P1 | Preliminary review only |
| `Imbad0202/academic-research-skills` | Research planning, evidence verification, synthesis, agent workflows | P1 | Preliminary review only |
| `zarazhangrui/frontend-slides` | Visual previews, HTML presentation workflows, design variants | P2 | Preliminary review only |
| `router-for-me/CLIProxyAPI` | Provider abstraction, routing, API adapters, credential management | P2 | Preliminary review only |

Additional candidate discovered during research:
- `n8n-io/skills` — a separate skills/reference repository related to n8n. Not yet fully audited or approved for adoption.

Graphify candidate:
- `Graphify-Labs/graphify` — important to the user's project/file knowledge-graph interest. The open question is whether to use it as a separate tool or adapt selected concepts into the toolkit. No installation or integration is approved.

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

## 27. Recommended ordering for future planning (proposal, not approval)

This ordering is a recommendation to discuss after the user confirms the current audit; it is not permission to begin implementation:

1. Close the current repository audit and reconcile all documentation/decision conflicts.
2. Complete the detailed external-source audits and create a capability/adoption matrix.
3. Define the target tool ecosystem architecture and permission model.
4. Decide how Project Intelligence should evolve, including the Graphify question.
5. Define future specialist agent capabilities and their actual tool access.
6. Strengthen evaluation coverage for tools, integrations, agents, and workflows.
7. Implement approved components incrementally with contract tests and evidence.
8. Run trusted Codex behavioral validation when the environment is available.
9. Perform a safe selective-adoption trial.
10. Review governance, portability, and release readiness.

Do not begin step 2 or later automatically if the user gives a different explicit next instruction.

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

**Next action:** Verify the updated `PROJECT_STATE.md` against the live repository, inspect the resulting diff for unsupported claims or contradictions, and confirm the CI run for the document-update commit. Then update this same file with that final verification evidence and the next user-approved task. Do not start external source audits or architecture implementation until the user confirms the next task.

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
