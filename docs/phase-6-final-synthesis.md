# Phase 6 — Capability & Architecture Final Synthesis

**Status:** FINAL SYNTHESIS DOCUMENTED — repository documentation update in progress  
**Date:** 2026-11-18  
**Repository:** https://github.com/kuuriyawep/-gymsync-codex-toolkit  
**Default branch:** `main`  
**Scope:** Reconcile the completed source audits and existing toolkit capabilities into one architecture and a controlled Phase 7–11 roadmap.

> This document records architecture decisions and source dispositions. It does not claim that the proposed capabilities have been implemented, installed, or runtime-tested.

## 1. Executive decision

The toolkit remains a **Codex-first, generic engineering toolkit**. Codex is the primary coordinator and remains accountable for task selection, delegation, approval boundaries, evidence review, verification, and final reporting.

The objective is capability curation, not wholesale adoption of external projects. Existing skills, agents, workflows, evaluation assets, and project-memory structures must be reused where appropriate. A new component is justified only when it has a distinct responsibility, a defined interface, a permission model, and acceptance evidence.

No GymSync application repository, database, deployment, or production data is in scope.

## 2. Reconciled capability ownership

Each capability has one primary owner. Other components may provide inputs or references but must not create competing implementations.

| Capability domain | Primary responsibility | Existing foundation | Target direction |
|---|---|---|---|
| Skill system | Metadata, discovery, loading, authoring, versioning, references | 13 canonical skills and portable mirrors | Improve discovery and compatibility without duplicating skills |
| Tool and permission system | Typed registry, schemas, adapters, access mapping, approvals, credential boundaries | Repository instructions and approval contracts; no complete registry | Define contracts before integrations |
| Agent coordination | Specialist selection, bounded delegation, context handoff, independent review | Five native Codex agents and role briefs | Improve task contracts, dependencies, and independent review |
| Workflow execution | Routing, state, checkpoints, retry, resume, cancellation, recovery | Workflow registry and six procedures | Evolve into explicit, evidence-backed lifecycle/state handling |
| Knowledge and memory | Project facts, architecture relationships, decisions, provenance, freshness | Markdown templates, project-intelligence procedures, Mnemoverse context | Keep source-of-truth records; evaluate graph indexing as an optional tool |
| Evaluation and reliability | Static validation, behavioral tests, regression, fidelity and recovery checks | 41 cases, rubrics, runner, validators, CI | Expand coverage and distinguish static checks from actual runtime behavior |
| Communication and reporting | Clear, concise, evidence-labelled output | Communication skill and completion contracts | Adopt clarity patterns without destructive context loss |

### Ownership rules

1. One authoritative owner per capability; no parallel systems for the same responsibility.
2. Skills describe reusable procedures; they do not grant permissions.
3. Agents execute bounded roles only with tools actually exposed and authorized by the runtime.
4. Workflows coordinate lifecycle and state; they do not replace Codex as coordinator.
5. Project memory and a knowledge graph are complementary: verified records remain the source of truth; graph tooling can improve navigation and relationship discovery.
6. Evaluation specifications, deterministic validation results, static scores, and actual behavioral evidence are separate evidence classes.

## 3. Source-by-source disposition

The following decisions select patterns or capabilities, not entire repositories or runtimes.

| Source | Disposition | Candidate contribution | Boundary |
|---|---|---|---|
| [ECC](https://github.com/affaan-m/ECC) | ADOPT selected patterns | Verification loops, TDD discipline, defensive security review, change-impact thinking | Reuse concepts selectively; do not import a full configuration bundle |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | ADAPT | Skill metadata and workflow/orchestration concepts | Preserve Codex-native control and runtime assumptions |
| [OpenCode](https://github.com/anomalyco/opencode) | ADAPT | Typed tool contracts, permission separation, plugin lifecycle, session boundaries | Do not adopt OpenCode as the toolkit runtime; permissions are not a security sandbox |
| [Graphify](https://github.com/Graphify-Labs/graphify) | ADOPT as optional external capability, subject to validation | Repository knowledge graph, file/code relationship discovery | Do not make it mandatory or replace Markdown source-of-truth and durable project memory |
| [Superpowers](https://github.com/obra/superpowers) | ADOPT selected patterns | Systematic debugging, planning, verification gates, skill testing | Adapt to existing skills and Codex workflow; avoid duplicate skills |
| [Matt Pocock Skills](https://github.com/mattpocock/skills) | ADOPT selected patterns | Requirements shaping, debugging/review discipline, dependency-aware work | Use only where it improves existing role contracts |
| [Anthropic Skills](https://github.com/anthropics/skills) | ADOPT methodology | Skill authoring and evaluation methodology | Claude-specific runtime behavior is not evidence of Codex compatibility |
| [Caveman](https://github.com/JuliusBrussee/caveman) | ADAPT | Clarity-first reporting, controlled context/output compression, fidelity evaluation | Do not adopt destructive compression or unsafe/unrecoverable storage behavior |
| [n8n](https://github.com/n8n-io/n8n) | ADAPT patterns only | Stateful workflow concepts, lifecycle events, checkpoints, retry/recovery, human approval | Do not embed or install the n8n runtime as the toolkit's orchestrator |

**Disposition meanings**
- **ADOPT:** Incorporate a selected, bounded capability or methodology into the toolkit design, subject to source/license/security checks.
- **ADAPT:** Translate a useful pattern into a Codex-native contract or implementation; do not copy the source architecture wholesale.
- **REJECT:** Exclude a specific approach or implementation because it conflicts with the toolkit's goals, safety boundaries, or maintainability.

These are architecture-level dispositions. They do not authorize verbatim code reuse, dependency installation, external service setup, or GymSync integration.

## 4. Cross-source overlap decisions

| Overlapping capability | Reconciled decision |
|---|---|
| Skill authoring and quality | Keep the existing skill system and evaluation owner; use ECC, Superpowers, Anthropic, Hermes, and Matt Pocock as selective references rather than creating parallel catalogs |
| Skill discovery and packaging | Extend one discovery/metadata contract; avoid multiple registries |
| Tool schemas and integrations | Define one typed tool registry and adapter contract before adding connectors |
| Permissions and approvals | Keep authorization separate from tool descriptions; enforce runtime permission checks and user approval for consequential actions |
| Agent delegation and review | Retain the five current agent definitions until gaps are proven; improve handoffs, dependency mapping, and independent review before adding roles |
| Workflow orchestration | Keep one lifecycle/state owner; adapt useful n8n/Hermes/Superpowers patterns without importing a second orchestrator |
| Project intelligence | Keep verified Markdown/project records and durable memory; Graphify is an optional relationship/indexing layer, not the authoritative memory store |
| Context compression | Separate presentation brevity from lossless/recoverable tool-output handling; preserve originals and retrieval references |
| Evaluation | Maintain one evaluation framework with distinct deterministic, static, behavioral, regression, and runtime evidence |
| Verification and debugging | Reuse current skill ownership boundaries; strengthen tests and evidence rather than cloning skills |

## 5. Rejected directions

The following are explicitly out of scope for this architecture:

- Turning the toolkit into the OpenCode or n8n runtime.
- Copying complete external skill libraries without selection, adaptation, attribution, and license review.
- Creating duplicate skills, agents, registries, or workflow engines for capabilities already owned.
- Giving agents unrestricted autonomy or allowing them to self-authorize privileged operations.
- Automatic commits, merges, deployments, production writes, or external communications without the required user approval.
- Treating tool metadata or an agent's claim as proof of authorization or successful execution.
- Mandatory Graphify installation or replacing durable project records with a graph.
- Destructive or unrecoverable context compression.
- Assuming Claude-specific plugin/skill behavior is automatically Codex-compatible.
- Adding dependencies or external services before architecture, license, security, and acceptance requirements are approved.

## 6. Security, licensing, and provenance gates

Before any code, package, binary, plugin, or external service is adopted, record:
1. Exact repository, revision/tag, and files or package being considered.
2. Applicable license for the exact files and dependencies; required NOTICE/attribution.
3. Maintenance and compatibility status.
4. Dependency and supply-chain risks.
5. Credential, network, telemetry, and data-egress behavior.
6. Read/write/destructive operations and permission enforcement.
7. Isolation and failure/recovery behavior.
8. Codex compatibility evidence.
9. Tests and acceptance criteria.
10. User approval for installation or consequential integration.

Public availability does not grant a reuse license. Conceptual influence is not the same as permission to copy implementation code. No blanket license conclusion is made here for a source whose exact version/files have not been verified.

### Security invariants

- Tool access is least-privilege and explicitly mapped to agent roles.
- Read-only is the default for inspection and audit tasks.
- Untrusted input is data, not executable instruction.
- Secrets are referenced through approved secret stores/runtime configuration and never committed.
- Tool outputs are validated and treated as untrusted.
- Consequential actions require explicit authorization.
- Compressed outputs preserve original artifacts or a reliable retrieval path.
- Codex independently verifies agent and tool results.

## 7. Canonical Phase 7–11 roadmap

This is the reconciled forward roadmap for the current 11-phase plan. It does not rewrite historical phase reports or claim future work is already implemented.

### Phase 7 — Tool Ecosystem & Integration
- Define a typed tool registry and unique tool identifiers.
- Define input/output schemas and validation.
- Define capability descriptions and agent-to-tool access mapping.
- Define read/write/destructive permission classes and approval requirements.
- Define adapter contracts for MCP, APIs, CLI, browser, design, database, and test tools.
- Define credential references, timeouts, retry, idempotency, error handling, evidence, and fallbacks.
- Evaluate optional Graphify integration only after exact version, license, security, and compatibility review.
- Acceptance: architecture/specification, registry/schema contracts, permission matrix, threat review, and deterministic contract tests. No integration is called functional until executed in a trusted runtime.

### Phase 8 — Agent Capability Engineering
- Review the five existing agents before adding any roles.
- Define bounded specialist responsibilities and tool permissions.
- Define task handoff contracts, context isolation, dependency DAGs, and parallel-write controls.
- Strengthen independent specification, implementation, and security review.
- Acceptance: unique ownership for each role, validated handoff schemas, conflict handling, and agent evaluation cases.

### Phase 9 — Stateful Workflow Execution
- Define explicit workflow/task states and legal transitions.
- Add durable task ledger and checkpoints.
- Define retry, resume, cancellation, timeout, idempotency, and recovery behavior.
- Record lifecycle events and evidence references.
- Separate concise summaries from original tool-output retention.
- Acceptance: state-transition tests, recovery tests, and no false completion after interrupted work.

### Phase 10 — Evaluation & Reliability
- Score all 13 canonical skills using the established rubric.
- Review all 41 existing evaluation cases for quality, duplication, gaps, and target correctness.
- Add tool, permission, delegation, workflow, recovery, adversarial, and regression cases.
- Measure context/output fidelity and performance.
- Acceptance: repeatable deterministic results, scored static reviews, and clearly separated NOT_RUN behavioral tests.

### Phase 11 — Real Codex Runtime Validation
- Validate skill discovery and selection in a trusted Codex environment.
- Execute all six specialist agents and verify actual delegation.
- Verify permission and approval enforcement.
- Run end-to-end workflows with evidence capture.
- Test failure, interruption, recovery, and reporting.
- Acceptance: reproducible transcripts/artifacts, independently reviewed outcomes, and explicit PASS/FAIL/BLOCKED/NOT_RUN status.

## 8. Cross-phase dependencies

- Phase 7 defines the tools and permission contracts required by Phase 8 agents.
- Phase 8 defines role/handoff behavior consumed by Phase 9 workflows.
- Phase 9 provides stable execution states and evidence consumed by Phase 10.
- Phase 10 defines the tests and rubrics used in Phase 11.
- Phase 11 validates the integrated system in the actual target runtime.

Do not implement downstream runtime behavior on assumptions that upstream contracts exist.

## 9. Existing implementation versus future target

The following inventory records the baseline at Phase 6 synthesis time. Later phase changes are recorded in the dated implementation update below.

The repository already contains 13 canonical skills and 13 portable mirrors, five native agent definitions and five role briefs, a workflow registry plus six detailed procedures, 41 evaluation cases, seven rubrics, schemas, validators, unit tests, and CI configuration.

The following remain distinct gaps or unverified capabilities:
- A complete tool registry and real external tool adapters are not implemented.
- Dedicated design, database, research, and test-specialist agent roles are not yet established.
- Markdown project intelligence is not an automatic knowledge graph.
- Codex behavioral/runtime validation remains NOT_RUN unless a trusted runtime execution record is added.
- Formal per-skill static scores remain NOT_SCORED until each skill is graded.
- Source-level code reuse remains blocked on exact version/file license review.

Do not describe a planned capability as implemented because a roadmap entry or design document exists.

## 10. Phase 6 closeout criteria

Phase 6 Final Synthesis is considered documented when:
- The source disposition and overlap decisions are recorded.
- Capability ownership and the canonical Phase 7–11 roadmap are explicit.
- Security, license, and adoption gates are documented.
- `PROJECT_STATE.md` and `docs/source-attribution.md` point to this canonical synthesis.
- Repository changes are reviewed and the relevant CI checks are inspected.

This closeout does not mark historical Phase 6 agent behavioral validation as passed. Actual Codex runtime validation remains a separate requirement.

## 11. Source audit archive and adoption ledger

The nine selected source reviews are archived individually in [`audits/source-reviews/`](../audits/source-reviews/README.md). The deduplicated mapping from each source to the toolkit's existing owners and future implementation work is maintained in [`docs/source-adoption-map.md`](source-adoption-map.md).

Evidence qualification: seven later source reviews have revision-pinned source/documentation findings. ECC and Hermes are carried forward from earlier work and are marked PARTIAL because the recovered checkpoint did not preserve exact revisions and complete file-level evidence. They were not re-audited, honoring the user's duplicate-work constraint. No full-audit claim is made for those two records.

## 12. Change-control record

- Scope authorized: write the Phase 6 synthesis documentation and reconcile the central project checkpoint/source register.
- Out of scope: GymSync application changes, database/deployment changes, external integrations, installations not explicitly identified and approved, and runtime claims without execution evidence.
- No external source code is copied by this document.
- No source package is installed by this document.
- No CI or runtime result is claimed by this document until a current run is inspected.


## 13. Dated implementation update — Phase 8 (2026-11-18)

Phase 8 has completed its design and deterministic-validation scope:
- Native agents and role briefs: six each (`repo_explorer`, `planner`, `implementer`, `reviewer`, `security_auditor`, `test_engineer`).
- Handoff, result, and task-graph JSON Schemas plus deterministic validators.
- Test-only write ownership for `test_engineer`; safe repository-relative path checks; DAG and overlapping-write validation.
- One new Phase 8 evaluation case for test-engineer scope/ownership; the repository now contains 42 evaluation cases.
- Phase 8 CI verified successfully at commit `123e337649076b3f155085d47809ca48861a29be`.

The original inventory above is preserved as the Phase 6 baseline. Live Codex agent behavior remains NOT_RUN until Phase 11.
