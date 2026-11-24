# GymSync Intelligent Agent Ecosystem — Architecture Specification

**Status:** USER-APPROVED TARGET ARCHITECTURE; repository specification in progress  
**Authority:** The user is the final decision authority. Codex is the single accountable orchestrator.  
**Scope:** This specification governs the reusable Codex toolkit repository only. It does not authorize changes to the GymSync application, production systems, external services, or credentials.  
**Architecture principle:** **Autonomy without losing governance.**

## 1. Purpose and target

Evolve the existing Codex-first toolkit into a proactive, event-driven, multi-agent engineering ecosystem. Agents should continuously monitor assigned signals, reason about problems and opportunities, collaborate with specialists, and propose useful work without waiting for a new user prompt. They must remain subordinate to Codex and must never bypass user approval.

This is an evolution of existing repository capabilities, not a greenfield rebuild. Preserve and integrate the existing skills, agents, workflows, schemas, registries, memory/evaluation assets, and their established ownership boundaries. Do not create parallel routers, task engines, handoff contracts, memory stores, or evaluation runners where an existing component can be extended.

## 2. Approved operating decisions

| Dimension | Approved decision | Required interpretation |
|---|---|---|
| Autonomy | HIGH | Continuous/event-driven monitoring and analysis; no requirement for a fresh user command to discover issues |
| WhatsApp | BIDIRECTIONAL | User may address Codex or a named agent; Codex/agents may send authorized reports and requests |
| Initiative | PROACTIVE PROPOSALS | Agents can propose tasks; Codex accepts, rejects, or defers; user approval remains required for gated actions |
| Authority | Codex central | Codex owns routing, arbitration, approvals, final verification, and final reporting |
| Final authority | Human | User retains final authority for consequential actions |

High autonomy does not mean unrestricted execution, always-on model inference, or bypassing the approval engine. Prefer event-driven activation and scheduled checks over continuously running expensive model processes.

## 3. Authority and governance model

1. User: final authority for scope, risk acceptance, and gated operations.
2. Codex Orchestrator: central coordinator; owns task intake, triage, assignments, arbitration, approval routing, verification, and final reports.
3. Specialist agents: bounded reasoning and execution within their assigned roles and inherited permissions.
4. Runtime services: event delivery, scheduling, tool invocation, memory retrieval, messaging, and observability; they do not acquire decision authority merely by being services.

An agent cannot grant itself permissions, expand scope, impersonate the user, approve its own high-risk proposal, or treat a handoff as authorization. Agent-generated content, repository data, web content, and tool output are untrusted inputs until validated.

## 4. Common Agent Intelligence Standard

Every specialist uses a common nine-capability contract while retaining domain-specific reasoning:

1. **Identity** — stable agent ID, role, version, owner, scope, and declared authority.
2. **Knowledge** — relevant project context, source references, constraints, and freshness.
3. **Reasoning** — explicit problem framing, hypotheses, options, dependencies, and rationale.
4. **Self-critique** — challenge assumptions, identify missing evidence, failure modes, and alternative explanations.
5. **Tools** — capability-registry-driven access with least privilege and operation-level permissions.
6. **Memory** — read/write policy for shared, specialist, and execution memory; no unreviewed shared-memory mutation.
7. **Collaboration** — structured consultation, delegation, review, disagreement, and escalation.
8. **Initiative** — detect and submit deduplicated proposals; no unilateral authority to accept gated work.
9. **Evaluation** — measurable outcomes, evidence, rubric results, and recorded failure lessons.

Agent outputs should use structured reports: task/context, findings, evidence, confidence/unknowns, recommendation, risk, changed artifacts (if authorized), verification, and escalation needs.

## 5. Agent lifecycle and autonomy protocol

Use an event-driven lifecycle:

- **Monitoring:** wait for assigned events, scheduled checks, repository changes, alerts, or explicit messages.
- **Activated:** validate trigger, identity, scope, deduplicate event, load relevant knowledge, and check permissions.
- **Working:** reason, research, consult, or execute approved bounded work; checkpoint meaningful state.
- **Reporting / Waiting:** submit result or proposal to Codex; wait for decision, missing input, or next event.

Required controls: idempotency keys, task leases/ownership, bounded retries, timeouts, cancellation, checkpoints, recovery, stale-task detection, duplicate suppression, and escalation. Persistent background execution is a runtime-service responsibility; a repository document or workflow ledger alone is not proof of a live runtime.

## 6. Initiative and Opportunity Engine

Agents may identify three proposal classes:

- **Problem:** defect, incident, risk, regression, or unmet requirement.
- **Improvement:** quality, maintainability, reliability, performance, or workflow enhancement.
- **Opportunity:** new capability or beneficial future work.

Every proposal record must contain: proposal ID; proposer/agent; type; concise title; reason; evidence/source references; expected benefit; risk and impact; effort estimate; affected components; required specialist agents; dependencies; proposed verification; approval level; deduplication fingerprint; status; Codex decision and rationale.

Codex triages each proposal as **ACCEPT**, **REJECT**, or **DEFER**. Acceptance authorizes only the next explicitly defined planning/execution boundary, not any higher-risk action. Repeated or materially equivalent proposals must be merged or linked rather than flooding the queue.

## 7. Agent-to-agent communication protocol

Supported interaction patterns:

- **Consultation:** request specialist advice without transferring task ownership.
- **Delegated review:** assign a bounded independent review and require evidence.
- **Incident escalation:** notify Codex of a time-sensitive or high-risk finding.
- **Conflict resolution:** preserve differing conclusions and evidence; Codex arbitrates and records the decision.

Each communication record captures sender, recipient, timestamp/event ID, task/proposal ID, purpose, scope, question/request, evidence references, response, agreements, conflicts, and Codex's final decision. Agents may disagree; no agent wins by rank or confidence alone.

## 8. WhatsApp Intelligence Gateway

Target architecture:

`Codex / Agents -> Shared Messaging API -> Identity, Routing & Permission Layer -> n8n Workflows -> Twilio WhatsApp API -> User`

Required capabilities: inbound user messages; routing to Codex or a named agent; outbound status reports; screenshots/media; approval requests; authorized commands; delivery receipts and failure handling.

Required security controls: sender identity verification; agent identity; per-command authorization; explicit approval confirmation bound to the exact action and payload; replay/duplicate protection; audit logs; rate limits; sensitive-data redaction; safe attachment handling; and fail-closed behavior when identity or delivery state is uncertain. Agents must never impersonate the user or convert a message receipt into approval.

**Current status:** design target only. No WhatsApp, Twilio, or n8n integration is claimed or authorized by this document.

## 9. Memory and knowledge architecture

Keep three distinct scopes:

- **Shared Project Memory:** verified architecture, decisions, constraints, component map, and durable project facts.
- **Specialist Memory:** role-specific procedures, domain findings, and reusable lessons.
- **Execution Memory:** task-scoped events, checkpoints, tool outputs, decisions, and recovery state.

Graphify is a candidate knowledge-graph provider for repository relationships, not a replacement for the memory governance layer. The graph should support traceable links among files, symbols, dependencies, decisions, agents, workflows, and evidence. Memory owns curated facts and decisions; graph indexing helps navigation and relationship discovery.

Agents may suggest memory updates but cannot directly overwrite canonical shared memory. Updates require provenance, validation, freshness checks, conflict handling, and governed promotion. Preserve source references and distinguish verified facts from inference.

## 10. Specialist capability and permission matrix

| Specialist | Core intelligence | Required tool capabilities (when available) | Default boundary |
|---|---|---|---|
| Research | source synthesis, evidence quality, alternatives | web research, repository search, documentation analysis | read/analyze; no unapproved writes |
| Frontend | UX reasoning, implementation, visual regression | browser automation, Playwright, screenshots, visual comparison | isolated approved changes |
| Backend | API/data-flow reasoning, business rules, concurrency | terminal, DB inspection, API tests, logs | isolated approved changes; no production writes |
| QA | independent test design, regression, reproducibility | test runners, Playwright, coverage, fixtures | tests/fixtures/evals within approved scope |
| Security | threat modeling, defensive detection, remediation guidance | static analysis, dependency/secret scanning, vulnerability tests | defensive read/analyze; no destructive exploitation |

Shared capabilities: repository graph, governed memory, Git operations, workflow/task state, evaluation, messaging, reporting, and approval requests. Maintain a capability registry and least-privilege mapping. Tool discovery, configuration, and successful invocation are separate states; an adapter is not verified until a safe invocation is evidenced.

## 11. Intelligence evaluation

Evaluate observable outcomes, not self-reported confidence. Dimensions:

- reasoning quality and evidence discipline;
- tool selection and successful tool proficiency;
- initiative relevance, novelty, and deduplication;
- collaboration quality and conflict handling;
- reliability, recovery, and truthful reporting;
- governance compliance and permission-boundary adherence.

Use existing evaluation cases, rubrics, runner, and result conventions where possible. Add only non-duplicate cases for confirmed gaps. Include specialist-specific scenarios, including backend payment/business-rule cases (for example, old debt plus a renewal payment), concurrent requests, database consistency, and independent QA review. Preserve failure memory and immutable historical results.

## 12. Risk and approval governance

| Risk level | Typical activity | Default policy |
|---|---|---|
| R0 | Read repository/docs, inspect metadata | automatic within scope |
| R1 | Analyze, research, draft plan, propose | automatic; report to Codex |
| R2 | Changes in isolated worktree or disposable test fixture | policy-bounded; explicit task authorization and verification |
| R3 | Shared branch/repository changes, shared state | Codex authorization and required review; user approval where repository policy requires |
| R4 | Commit/merge/deploy, production or destructive database operation, permission/security changes, external consequential communication | explicit user approval bound to exact action |

Use isolated worktrees, checkpoints, and rollback plans for changes. Agents cannot modify the risk policy or their own permissions. Existing repository-specific approval rules remain in force; this matrix does not weaken them.

## 13. Failure, recovery, and escalation

On unsafe or failed work: stop the affected action; preserve a checkpoint; report the failure and evidence; diagnose; consult another specialist where useful; propose bounded recovery options; and wait for authorization if recovery exceeds the approved scope.

The runtime must handle retries with limits, timeouts, checkpoint recovery, partial completion, duplicate task prevention, write conflicts, unavailable agents/tools, messaging failure, false positives, and escalation. Never convert an interrupted or uncertain action into a success state.

## 14. Infrastructure boundaries

The target ecosystem has these separable services:

- **Codex Orchestrator** — decision authority and coordination.
- **Agent Runtime** — specialist execution sessions.
- **Event Bus** — event delivery and deduplication.
- **Scheduler** — periodic monitoring and scheduled triggers.
- **Tool Registry** — capability discovery, schemas, permissions, health.
- **Shared Memory** and **Agent Memory** — governed knowledge stores.
- **Communication Gateway** — identity-aware inbound/outbound messaging.
- **Approval Engine** — human authorization and action binding.
- **Evaluation Engine** — deterministic and behavioral evaluation.
- **Observability** — event, task, tool, decision, and delivery audit trails.

Codex intelligence is distinct from infrastructure that persists between sessions. Event monitoring, scheduling, background execution, and WhatsApp delivery require runtime services beyond a chat session. Do not represent repository-side schemas or a workflow ledger as a deployed service.

## 15. Existing toolkit mapping — preserve and extend

The current repository audit records 13 native skills and portable mirrors, six agent definitions and role briefs, seven workflow files (including the registry), handoff/task-graph schemas, a workflow ledger, tool registry/permission references, project-memory templates, repository-intelligence architecture, and 55 evaluation case specifications. These are repository artifacts, not proof of live agent execution.

| Existing component | Ecosystem responsibility | Integration direction |
|---|---|---|
| `AGENTS.md` + `PROJECT_STATE.md` | authority, project continuity, hard boundaries | retain as root control documents; link this spec |
| `.codex/agents/*.toml` + `agents/*.md` | six specialist/coordination roles | map current six roles to specialist needs; preserve role boundaries; identify gaps before adding roles |
| `.agents/skills/` + `skills/` | reusable intelligence procedures | extend relevant existing skills; keep portable mirrors synchronized |
| `workflows/registry.md` + workflow docs | task routing and procedures | integrate event/proposal lifecycle without creating a second router |
| handoff and task-graph schemas | delegation and dependencies | extend existing contracts for consultation, review, proposal, and event metadata only where needed |
| `tools/workflow_ledger.py` | workflow state/checkpoints/events | preserve as state utility; do not claim it is a persistent event bus/runtime |
| `registry/tools.json` + permission references | capability and permission declarations | evolve into specialist capability mapping; host enforcement still requires runtime proof |
| project-memory templates + memory docs | curated shared/specialist/execution memory | define scope and promotion governance; avoid a duplicate memory store |
| repository-intelligence architecture | graph/provider boundary | keep provider-neutral; Graphify remains optional until separately authorized and tested |
| `evals/`, rubrics, evaluator | intelligence, reliability, governance evaluation | map existing cases first; add only evidenced coverage gaps |
| GitHub Actions quality workflow | repository static quality gate | keep static checks distinct from live behavioral/runtime acceptance |

Current six roles: `repo_explorer`, `planner`, `implementer`, `reviewer`, `security_auditor`, and `test_engineer`. Do not replace these merely to match labels such as Research, Frontend, Backend, QA, or Security. Map capabilities and identify whether an existing role can safely own each responsibility before proposing a new agent.

## 16. Seven gated implementation workstreams

Workstreams are sequentially gated. Each must have a defined scope, file-level change plan, acceptance criteria, dependency check, and evidence record before being marked complete.

| Workstream | Objective | Core deliverables | Exit gate |
|---|---|---|---|
| **WS1 — Agent Intelligence Core** | common agent architecture, advanced reasoning, self-critique/what-if, specialist intelligence, structured reports | Agent Intelligence Standard; role-to-capability mapping; shared output contract; non-duplicate skill/agent updates | all existing roles mapped; common contract validated statically; specialist differences and boundaries preserved |
| **WS2 — Autonomous Runtime** | lifecycle, event activation, scheduled monitoring, persistent background execution, checkpoints/recovery | lifecycle/event contracts; runtime boundary and adapter design; idempotency/retry/recovery requirements | event lifecycle and failure semantics are testable; no false claim of deployed background runtime |
| **WS3 — Agent Collaboration** | agent messaging, consultation, independent reviews, conflict resolution, proposal management | collaboration protocol; proposal schema/queue contract; decision and communication log | consultation/review/escalation and proposal triage are represented and validated |
| **WS4 — Specialist Tool Intelligence** | frontend browser automation, backend scenario testing, QA automation, security monitoring, research | capability matrix; tool schemas; least-privilege policy; verification requirements | each capability has owner, schema, risk, and verifiable status; unavailable tools remain blocked |
| **WS5 — WhatsApp Communication** | Codex/agent-to-user and user-to-agent, reports/media, approval requests, identity/security | gateway architecture; message envelope; routing/authentication/approval and audit contracts | secure design and test plan pass; external integration only after explicit user approval |
| **WS6 — Memory & Knowledge** | shared/specialist memory, graph integration, validation, cross-agent retrieval | memory schema/promotion policy; Graphify provider adapter boundary; provenance/freshness rules | memory scopes and governance validate; no unreviewed shared-memory writes |
| **WS7 — Intelligence Evaluation & Governance** | benchmarks, autonomy/reliability tests, security boundaries, end-to-end simulation, human approval verification, release gate | coverage map; benchmark scenarios; governance/recovery tests; integrated simulation report | all required scenarios have evidence-backed statuses; critical risks resolved or explicitly accepted |

Dependencies: WS1 -> WS2 -> WS3 -> WS4 -> WS5 -> WS6 -> WS7. Cross-cutting design reviews may occur earlier, but a later workstream cannot be declared complete before its dependencies and exit gates are satisfied.

## 17. Required integrated simulation

The final simulation must include this controlled scenario:

1. Security specialist detects a critical backend vulnerability from a safe test signal.
2. It records evidence and escalates to Codex.
3. Codex triages and delegates bounded analysis to Backend and QA specialists.
4. Backend proposes a fix; no production change occurs.
5. QA independently validates the fix and regression behavior.
6. Codex reviews evidence, resolves any disagreement, and prepares a report.
7. WhatsApp gateway delivers the authorized report/approval request through verified identity controls.

Also test failure paths: agent/runtime unavailable, conflicting findings, messaging delivery failure, duplicate events, false positive, unauthorized action attempt, partial execution/recovery, and Codex runtime unavailable. If the live Codex runtime is unavailable, mark behavioral portions BLOCKED/NOT_RUN; repository-side contract validation may continue.

## 18. Non-negotiable invariants

- Codex remains the central coordinator and accountable reporter.
- User remains final authority for gated actions.
- No blind execution, self-approval, or permission escalation.
- No duplicated intelligence infrastructure; extend canonical components.
- Evidence is required before any PASS or completion claim.
- Proactive monitoring and proposals are encouraged; consequential execution remains governed.
- Agent disagreement is preserved and resolved by evidence.
- Runtime capability is never inferred from documentation or registry declarations.
- No GymSync application changes or external service installation/integration without separate explicit authorization.

## 19. Implementation and evidence rules

For each workstream:
1. Inspect current canonical files and latest Git state before editing.
2. Map existing components and identify duplication risk.
3. Define bounded changes and observable acceptance criteria.
4. Implement the smallest coherent extension to existing contracts.
5. Run available repository static checks and deterministic tests; record exact commit and output.
6. Keep runtime/behavioral tests BLOCKED or NOT_RUN when no trusted Codex runtime is available.
7. Update `PROJECT_STATE.md` with status, evidence, limitations, and one next action.
8. Do not claim a workstream complete until its exit gate is met.

**Environment constraint:** The user does not currently have access to a Codex runtime for live behavioral testing. Continue repository-side architecture and static implementation where possible; do not ask the user to run Codex CLI commands or fabricate runtime results. External runtime services and the n8n trial must not be started without explicit authorization.

## 20. Immediate execution order

1. Register this document as the canonical approved ecosystem architecture.
2. Reconcile `PROJECT_STATE.md` and `docs/toolkit-integration.md` to point to this architecture and set WS1 as the active workstream; retain Phase 11 documents as historical/runtime acceptance material, not the primary roadmap.
3. Execute WS1 by extending existing agent contracts/skills only after inspecting their exact current contents and mapping all six roles.
4. Proceed through WS2–WS7 using the gates above.

---

**Approval record:** The user explicitly approved the architecture decisions and seven-workstream roadmap in the conversation on 2026-11-25.  
**Current implementation status:** Architecture specification authored; implementation workstreams are not yet complete.
