# Phase 11 — Real Runtime Integration & Full-System Validation

**Status:** IMPLEMENTATION AUTHORIZED — REPOSITORY-SIDE AUDIT COMPLETE; RUNTIME ACCEPTANCE PENDING  
**Execution strategy:** Codex-first  
**Coverage:** Full toolkit  
**Execution model:** Sequential, gate-based  
**Primary orchestrator:** Codex  
**Repository:** kuuriyawep/-gymsync-codex-toolkit

> Implementation is authorized by the user's 2026-11-24 instruction to complete Phase 11 in the existing toolkit repository. Work remains confined to this repository and the approved Phase 11 scope. No GymSync application changes, secret handling, or unapproved external side effects are authorized. Runtime-dependent criteria must remain BLOCKED or NOT_RUN until backed by trusted Codex evidence.

## 1. Purpose

Phase 11 validates the existing toolkit in a real, trusted Codex runtime. It does not rebuild the toolkit or repeat completed work without new evidence.

The objective is to establish, with reproducible evidence, whether Codex can discover and understand the repository, load and follow its skills, coordinate existing agents, route and execute workflows, retrieve project knowledge, use approved tools and MCP integrations, recover from failures, and complete end-to-end tasks safely.

A capability is not considered verified merely because its files, schemas, or deterministic tests exist. Static validation, deterministic tests, runtime execution, behavioral evaluation, integration testing, and end-to-end validation are distinct evidence levels.

## 2. Confirmed decisions

| Decision | Approved direction |
|---|---|
| Runtime strategy | Codex-first; OpenCode is an optional fallback for limited comparative experiments only |
| Primary coordinator | Codex remains the single accountable orchestrator |
| Coverage | All toolkit capabilities in the approved scope |
| Execution | Sequential workstreams; each gate must pass or receive an explicit documented disposition before proceeding |
| Agent autonomy | Hybrid autonomy within approved task boundaries |
| Agent lifecycle | Persistent + task-scoped hybrid |
| Memory | Controlled hybrid memory |
| Tools | Shared core + specialist tools; central declarative registry and least privilege |
| Skills | Core + specialist + task-activated access |
| Knowledge | Hybrid knowledge architecture |
| Execution context | Shared project context with isolated task workspaces where appropriate |
| Environment | Flexible execution environments, subject to evidence and security review |
| Agent communication | Structured communication protocol; Codex controls workflow |
| Approval governance | Risk-based approval |
| User authority | High-risk actions require explicit user approval |

### Risk-based approval

- **Low risk:** reversible, bounded actions may run autonomously when repository instructions permit.
- **Medium risk:** edits must remain within an explicitly approved task scope and ownership boundary.
- **High risk:** commits, merges, deployments, destructive actions, permission changes, production writes, and consequential external side effects require explicit user approval.

A subagent handoff never expands the parent task's permissions or user approval.

## 3. Phase 10 baseline and constraints

The Phase 10 completion report records the following repository baseline:

- 13 native Codex skills and 13 portable mirrors.
- 55 evaluation case specifications. These are authored cases, not 55 completed behavioral evaluations.
- 13 first-pass, model-assisted static skill scorecards. They are document-quality reviews, not runtime proof or independent human sign-off.
- Seven prepared agent-coordination behavioral scenarios.
- Native/portable skill parity and deterministic repository quality checks.
- The latest CI run recorded in the Phase 10 report was run #44303295207, with 127 unit tests and all 10 quality-gate steps passing.
- Actual Codex behavioral validation, agent execution, runtime approval enforcement, and end-to-end behavior remained deferred / NOT_RUN pending a trusted Codex session.

The Phase 10 report also identifies coverage gaps: direct case coverage is uneven across the 13 skills, and the existing 55 cases must be mapped before adding new cases. Do not duplicate cases merely to increase counts.

**Baseline rule:** Workstream 11.1 must refresh the current repository commit, local test results, Codex CLI/session state, configured integrations, and available model/runtime capabilities. Historical observations must not be presented as current runtime facts.

## 4. Scope

### Included

1. Runtime and environment readiness.
2. Repository intelligence and context loading.
3. Compatibility and behavioral testing of all 13 skills.
4. Existing agent discovery, execution, delegation, handoff, and review.
5. Workflow routing, sequencing, checkpoints, and recovery.
6. Project memory and knowledge retrieval.
7. Tool registry, permissions, and supported MCP integrations.
8. Evaluation, security, approval governance, and recovery.
9. Full end-to-end system validation and final evidence report.

### Excluded

- GymSync application development or modification.
- Rebuilding or replacing the existing toolkit.
- Repeating Phase 10 work without a specific evidence-backed reason.
- Installing unapproved dependencies, runtimes, frameworks, or services.
- Treating OpenCode or a local model as equivalent proof of Codex behavior.
- Unapproved commits, pushes, merges, deployments, permission changes, or destructive operations.
- Fabricating runtime results or marking unrun tests as passed.
- Automatic agent self-modification or unreviewed promotion of learning/memory.

## 5. Workstream roadmap

Workstreams execute in order. Each workstream produces its deliverables, records evidence and unresolved issues, and passes its exit gate before the next workstream begins. If a gate cannot pass, stop and document the blocker; do not silently skip ahead.

### 11.1 — Runtime & Environment Readiness

**Objective:** Establish a verified, safe Codex execution environment.

**Activities**
- Record repository commit, branch, working-tree state, and applicable project instructions.
- Verify Codex CLI installation, version, trusted project/session status, and usable model availability.
- Inventory runtime capabilities, available subagents, tools, MCP servers, plugins, and permission/approval behavior.
- Distinguish Codex-native tools from externally configured MCP integrations.
- Identify environment limitations and whether a safe test workspace is available.
- Do not install, authenticate, or change runtime configuration without separate approval.

**Deliverables**
- Runtime readiness report.
- Sanitized runtime capability inventory.
- Environment and dependency constraints.
- Runtime blocker/fallback register.

**Acceptance criteria**
- Runtime identity, version, session/trust state, and model availability are backed by direct observations.
- Configured integrations are distinguished from callable integrations.
- Tool discovery is distinguished from successful tool invocation.
- Missing or inaccessible capabilities are explicitly marked BLOCKED or NOT_RUN.
- No secrets, tokens, or credentials are recorded.

**Dependencies:** Phase 10 baseline and existing runtime discovery documentation.

**Exit gate:** A trusted Codex session is usable for the approved tests, or a precise blocker and safe next step are documented. No behavioral work is claimed complete without a usable session.

### 11.2 — Repository Intelligence & Context Loading

**Objective:** Verify that Codex can accurately understand the current toolkit.

**Activities**
- Test discovery of the repository operating contract, architecture, skills, workflows, agents, registries, schemas, tests, and evaluation assets.
- Test targeted file retrieval and source-of-truth precedence.
- Test whether Codex distinguishes implemented capabilities from proposals, examples, and deferred work.
- Check for stale-context errors and unsupported assumptions.

**Deliverables**
- Repository understanding scenarios and results.
- Architecture/context retrieval report.
- Source-of-truth and stale-context findings.

**Acceptance criteria**
- Codex accurately describes the current architecture and component ownership using repository evidence.
- It identifies relevant files for representative tasks without inventing paths or capabilities.
- Current source outranks stale project memory and agent-generated claims.
- Unknowns and conflicting evidence are surfaced explicitly.

**Dependencies:** 11.1.

**Exit gate:** Required repository-intelligence scenarios have evidence-backed outcomes and no unresolved critical misunderstanding.

### 11.3 — Full Skill Compatibility & Behavioral Testing

**Objective:** Validate all 13 native skills, not just their metadata or mirror parity.

**Activities**
- Build a case-to-skill coverage matrix from the existing 55 cases.
- Identify true in-scope, near-miss, edge, and failure-mode gaps without creating duplicate cases.
- Test skill discovery, loading, trigger selection, instruction adherence, expected outputs, and prohibited behavior.
- Verify native/portable parity using existing tooling.
- Add or adapt cases only where a confirmed coverage gap requires it and only within separately approved implementation scope.

**Deliverables**
- 13-skill compatibility matrix.
- Case-to-skill and taxonomy coverage map.
- Runtime invocation evidence and skill-level results.
- Gap/overlap register and proposed non-duplicate test additions.

**Acceptance criteria**
- Every one of the 13 skills has an explicit status and evidence reference.
- Discovery, loading, and behavioral instruction-following are reported separately.
- Existing 55 cases are mapped before new cases are proposed.
- A static scorecard or mirror-parity pass is not misrepresented as runtime success.
- Unexecuted skills remain NOT_RUN; unavailable prerequisites remain BLOCKED.

**Dependencies:** 11.2.

**Exit gate:** All 13 skills have evidence-backed dispositions; critical skill-selection or instruction-following failures are fixed or explicitly accepted as blockers before proceeding.

### 11.4 — Agent Execution & Delegation

**Objective:** Verify the existing Codex-first agent model and bounded delegation.

**Activities**
- Audit current .codex/agents/ definitions and human-readable role briefs before proposing any new role.
- Execute the seven existing agent-coordination scenarios and the applicable agent-contract scenario where safe.
- Test agent selection, task boundaries, handoff contracts, result validation, approval inheritance, and return of findings to Codex.
- Test independent read-only review, evidence-based conflict resolution, and failure recovery.
- Test parallel execution only for independent tasks with non-overlapping write ownership.

**Deliverables**
- Existing-agent inventory and role/capability matrix.
- Delegation and handoff test report.
- Approval and permission-boundary evidence.
- Conflict, concurrency, and recovery findings.

**Acceptance criteria**
- Codex remains the accountable coordinator and final reporter.
- Only existing, suitable agents are used unless a gap is approved for remediation.
- Handoffs define scope, expected outputs, constraints, and verification.
- Subagents do not exceed inherited permissions or approved write boundaries.
- Conflicting findings are resolved by evidence, not agent seniority.
- High-risk actions remain approval-gated.

**Dependencies:** 11.3.

**Exit gate:** Required agent scenarios have evidence-backed dispositions; no unresolved critical permission-boundary violation remains.

### 11.5 — Intelligent Workflow Engine Validation

**Objective:** Validate workflow selection and execution using the existing workflow registry, procedures, and ledger.

**Activities**
- Test task classification and workflow routing.
- Test dependency ordering, checkpoints, ownership, and task-state recording.
- Test pause/resume and recovery using the existing workflow ledger contract.
- Verify that the ledger records state and evidence references but does not silently execute tasks.
- Test completion reporting and prevention of premature completion.

**Deliverables**
- Workflow routing and execution matrix.
- Workflow ledger behavior report.
- Dependency/checkpoint and recovery evidence.
- Workflow defects and remediation proposals.

**Acceptance criteria**
- Representative tasks route to the correct existing workflow and relevant skills.
- Dependent tasks are sequenced; only independent work is parallelized.
- State transitions and recovery follow the existing contracts.
- A failed or incomplete task is not reported as complete.
- Approval checkpoints cannot be bypassed by workflow routing.

**Dependencies:** 11.4.

**Exit gate:** Required workflow scenarios pass or have documented non-critical limitations; no critical state-integrity or approval bypass remains.

### 11.6 — Memory & Knowledge Validation

**Objective:** Verify project intelligence, retrieval, and controlled knowledge continuity.

**Activities**
- Test retrieval from project profile, repository map, architecture, inventory, constraints, and task checkpoints where present.
- Test relevance, source references, freshness, and conflict handling.
- Test separation of durable project knowledge from task-scoped context.
- Test review requirements for proposed lessons and memory updates.
- Verify that current source files remain authoritative.

**Deliverables**
- Knowledge retrieval test report.
- Retrieval relevance and evidence matrix.
- Freshness/conflict and context-isolation findings.
- Memory governance findings.

**Acceptance criteria**
- Retrieved facts are traceable to current sources or clearly marked as historical.
- Stale or conflicting knowledge is surfaced rather than silently trusted.
- Task-scoped information does not become durable knowledge without the defined review process.
- No unreviewed autonomous memory promotion occurs.

**Dependencies:** 11.5.

**Exit gate:** Required retrieval and governance scenarios have evidence-backed dispositions; critical source-of-truth or context-isolation defects are resolved or blocked.

### 11.7 — Tool Registry & MCP Integration

**Objective:** Verify declared tools, permissions, and supported runtime integrations.

**Activities**
- Audit registry/tools.json, schemas, permission references, and adapter contracts.
- Test tool discovery separately from invocation and successful completion.
- Test operation-level permission boundaries, denied actions, error handling, and approval requirements.
- Review each configured MCP server against trust, lifecycle, reliability, and verification contracts.
- Treat optional Graphify as an external candidate unless separately approved and configured; it is not a required dependency.

**Deliverables**
- Tool registry and permission audit.
- Tool/MCP capability matrix.
- Invocation evidence and failure records.
- Adapter trust/verification findings.

**Acceptance criteria**
- Every in-scope tool has a documented purpose, scope, and permission disposition.
- A configured server is not called verified until a safe invocation succeeds.
- Unavailable integrations are marked BLOCKED or NOT_RUN.
- Denied and high-risk operations respect policy.
- No secrets or sensitive raw tool output are committed.

**Dependencies:** 11.6.

**Exit gate:** All in-scope tools and integrations have evidence-backed status; no unresolved critical unauthorized-action path remains.

### 11.8 — Evaluation, Security & Recovery

**Objective:** Consolidate quality evidence and test failure/safety behavior across the toolkit.

**Activities**
- Re-run applicable deterministic validators and unit tests on the current approved revision.
- Review the 55-case suite, coverage mapping, rubric applicability, and result-comparison semantics.
- Execute trusted-session behavioral tests and grade them against existing rubrics.
- Test prompt injection/untrusted output handling, secret hygiene, least privilege, approval boundaries, and recovery.
- Review interrupted/partial tasks, malformed outputs, missing evidence, and false-success prevention.
- Record performance/reliability observations only where measured.

**Deliverables**
- Deterministic and behavioral evaluation report.
- Security and approval-governance report.
- Recovery/reliability report.
- Updated risk, coverage-gap, and known-limitations registers.

**Acceptance criteria**
- Deterministic and behavioral outcomes remain distinct.
- Every PASS has direct evidence and a criterion-level rationale.
- FAIL, BLOCKED, NOT_RUN, and NOT_APPLICABLE retain their defined meanings.
- Critical failures cannot be hidden by aggregate scores.
- No secrets, production data, or destructive side effects are used in test fixtures.
- Existing historical evaluation artifacts are not overwritten.

**Dependencies:** 11.1–11.7.

**Exit gate:** Required evaluation, security, and recovery evidence is reviewed; critical failures are resolved or explicitly accepted by the user before final integration testing.

### 11.9 — End-to-End System Validation

**Objective:** Verify the integrated toolkit from a user request through a safe, evidence-backed completion.

**Activities**
- Run representative end-to-end scenarios that exercise repository intelligence, skill selection, workflow routing, agent delegation where appropriate, tool use, memory retrieval, verification, and reporting.
- Include at least one successful bounded task and one controlled failure/recovery path.
- Include an approval-gated scenario without performing a real high-risk side effect.
- Capture the relevant prompts, runtime/session details, tool and agent events, changed-file diffs where applicable, test outputs, and evaluation rationale; redact sensitive data.
- Independently review final evidence and known limitations.

**Deliverables**
- End-to-end scenario report.
- Full capability/status matrix.
- Evidence index.
- Critical blocker and known-limitations register.
- Phase 11 final report and next-phase recommendations.

**Acceptance criteria**
- The complete lifecycle is demonstrated with direct evidence.
- Approval gates and task boundaries remain intact.
- Successful completion includes verification, not merely a generated response.
- Failure paths are accurately reported and recover without hiding prior failures.
- No unrun capability is described as working.

**Dependencies:** 11.1–11.8.

**Exit gate:** Required end-to-end scenarios are reviewed, critical blockers are resolved or explicitly accepted, and the final report accurately represents all remaining limitations.

## 6. Execution dependency and gate sequence

    Phase 10 baseline
      -> 11.1 Runtime & Environment Readiness
      -> GATE 11.1
      -> 11.2 Repository Intelligence & Context Loading
      -> GATE 11.2
      -> 11.3 Full Skill Compatibility & Behavioral Testing
      -> GATE 11.3
      -> 11.4 Agent Execution & Delegation
      -> GATE 11.4
      -> 11.5 Intelligent Workflow Engine Validation
      -> GATE 11.5
      -> 11.6 Memory & Knowledge Validation
      -> GATE 11.6
      -> 11.7 Tool Registry & MCP Integration
      -> GATE 11.7
      -> 11.8 Evaluation, Security & Recovery
      -> GATE 11.8
      -> 11.9 End-to-End System Validation
      -> FINAL ACCEPTANCE

No workstream may be marked complete solely because its files or test cases exist. Each gate requires recorded evidence and a reviewed disposition.

## 7. Verification and evidence model

Use these evidence levels and report them separately:

| Level | What it establishes | Example evidence |
|---|---|---|
| Static validation | Artifact structure and declared contracts are valid | Repository validators, schema checks, parity |
| Deterministic tests | Repeatable tests pass for the tested revision | Unit-test output, deterministic evaluator |
| Runtime tests | The real runtime discovers or invokes a capability | Trusted Codex session, invocation result |
| Behavioral tests | Codex follows the intended instructions and constraints | Transcript, tool/agent events, rubric grading |
| Integration tests | Multiple components work together | Cross-component scenario evidence |
| End-to-end tests | A complete task lifecycle works | Request, plan, execution, verification, approval, report |

Every test record should include, as applicable:

- Workstream and scenario/case ID.
- Repository commit and branch.
- Runtime/client version and model identifier.
- Date/time and test operator/evaluator.
- Preconditions and safety fixture.
- Expected and prohibited behavior.
- Actual result and status.
- Evidence references (redacted transcript excerpts, tool events, diffs, command outputs).
- Criterion-level rationale and unresolved limitations.

### Status vocabulary

- **PASS:** directly observed evidence satisfies the acceptance criterion.
- **FAIL:** the test ran and an acceptance criterion was violated.
- **BLOCKED:** a prerequisite or environmental constraint prevented execution.
- **NOT_RUN:** the test was not attempted.
- **NOT_APPLICABLE:** the criterion does not apply, with a recorded rationale.

Do not convert BLOCKED or NOT_RUN into PASS. Do not treat a static PASS as a behavioral PASS.

## 8. Global Phase 11 exit criteria

Phase 11 may be marked complete only when all of the following are true:

1. All nine workstreams have a reviewed status and evidence record.
2. All 13 skills have individual compatibility dispositions.
3. Existing agent roles and delegation behavior have been tested against the applicable scenarios.
4. Workflow routing, state integrity, and recovery have been validated.
5. Memory/knowledge retrieval, source precedence, and governance have been tested.
6. In-scope tools and MCP integrations have verified or explicitly blocked/unrun statuses.
7. Deterministic, behavioral, security, and recovery results are reported separately.
8. Required end-to-end success, failure/recovery, and approval-gated scenarios are reviewed.
9. No unresolved critical security, data-integrity, permission, or approval-bypass issue remains unless the user explicitly accepts it with a documented limitation.
10. The final report includes evidence, failures, blockers, unrun checks, and known limitations without overstating reliability.

A Phase 11 report may conclude **COMPLETE WITH ACCEPTED LIMITATIONS** only with explicit user acceptance of the listed limitations. Otherwise, unresolved required gates keep the phase open.

## 9. Planned final deliverables

The following are planned outputs; they are not created by this plan file:

- docs/phase-11-baseline.md — refreshed baseline and runtime facts.
- docs/phase-11-execution-plan.md — this approved plan.
- docs/phase-11-capability-matrix.md — workstream, skill, agent, tool, and scenario status.
- docs/phase-11-test-results.md — consolidated evidence and criterion-level outcomes.
- docs/phase-11-blockers.md — blockers, failures, and accepted limitations.
- docs/phase-11-final-report.md — final acceptance decision and next steps.
- New immutable evaluation artifacts under the existing evals/results/ and evals/reports/ conventions, when actual runs are performed.

Use existing templates, schemas, validators, and evaluation infrastructure wherever possible. Do not create duplicate frameworks or duplicate cases.

## 10. Change-control rules

- This plan does not authorize implementation or runtime configuration changes.
- Before each implementation change, state the exact files, purpose, and acceptance test; obtain user approval for changes outside an already approved bounded workstream.
- Do not modify GymSync application source.
- Do not install dependencies or external services without explicit approval.
- Do not commit, push, merge, deploy, alter permissions, or perform destructive actions without explicit approval.
- Keep historical evaluation records immutable.
- Prefer small, reviewable changes and run relevant gates after each approved change.
- If a blocker invalidates the chosen approach, stop, report evidence and alternatives, and request a decision rather than silently changing scope.

---

**Planning decision:** Approved for use as the Phase 11 execution roadmap.  
**Execution state:** NOT STARTED.  
**Implementation authorization:** NOT GRANTED by this document.


## 10. Consolidated audit disposition (2026-11-24)

The repository-side static audit of all nine workstreams is recorded in [Phase 11 Consolidated Final Audit Report](phase-11-final-audit-report.md).

**Disposition:** Repository-side audit COMPLETE; runtime acceptance BLOCKED / NOT_RUN; overall Phase 11 PARTIAL. The documented 11.1 runtime blocker was accepted as a blocker disposition so repository-side review and closeout could proceed. This does not waive or pass runtime acceptance criteria.

No local terminal tests or validators are claimed as executed by the consolidated audit. Exact-head CI evidence must be obtained from GitHub Actions after the resulting repository commits.


## 11. Repository-side closeout and Codex-only handoff (2026-11-24)

Repository-side preparation has been completed for the remaining Phase 11 work. See [Codex Runtime Acceptance Pack](phase-11-codex-runtime-acceptance.md), the single checklist for work that cannot be honestly completed without a trusted Codex runtime.

- Workflow ledger review confirms that the ledger records state and does not execute tasks. Terminal-state immutability, approved-write approval-reference requirements, and scope coverage are present.
- Added lexical path validation regression tests for normal repository-relative paths, absolute paths, traversal, Windows drive paths, and backslashes. `safe_path()` is intentionally lexical; it does not resolve filesystem targets and does not guarantee symlink containment. The ledger's scope metadata must not be described as a filesystem sandbox.
- Evaluation runner documentation and behavioral/agent rubrics were reconciled with the runtime handoff. Authored cases and static checks remain separate from live behavioral results.
- The runtime pack enumerates the exact Codex-only checks: runtime capture, repository intelligence, 13 skills, six agents/seven coordination scenarios, workflow, memory, tool/MCP, security/recovery, and one end-to-end task.
- Skill case mapping is complete as a traceability map, but formal coverage minimums are not met/labeled for every skill. The runtime pack explicitly requires those gaps to be marked BLOCKED / CASE DESIGN REQUIRED rather than fabricated.

**Repository-side closeout:** COMPLETE, subject to final exact-HEAD CI.  
**Codex runtime acceptance:** NOT_RUN / BLOCKED until trusted Codex access and evidence exist.  
**Overall Phase 11:** PARTIAL — NOT FULLY ACCEPTED.
