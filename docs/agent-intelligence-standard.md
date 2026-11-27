# WS1 — Agent Intelligence Core: Role Mapping and Contract

**Status:** WS1 design/mapping artifact — static repository review only  
**Parent specification:** [Intelligent Agent Ecosystem Architecture](intelligent-agent-ecosystem-architecture.md)  
**Authority:** Codex is the coordinator; the user is the final decision authority.

## 1. Purpose

Apply one common intelligence contract to the six existing agents without flattening their specialist roles or creating duplicate agents. This document is the WS1 role-to-capability map and the basis for the next bounded implementation changes.

## 2. Common nine-capability contract

Every agent must demonstrate these capabilities in its role-appropriate way:

| Capability | Minimum expected behavior |
|---|---|
| Identity | Declare stable role, task ownership, scope, non-goals, and authority boundary |
| Knowledge | Inspect relevant current sources; cite paths/symbols; distinguish verified facts, inference, and unknowns |
| Reasoning | Frame the problem, compare options, identify dependencies, and explain why a recommendation follows from evidence |
| Self-critique | Challenge assumptions; identify missing evidence, counterexamples, edge cases, and what could invalidate the conclusion |
| Tools | Use only declared, available, authorized tools; distinguish discovery/configuration from successful invocation |
| Memory | Retrieve relevant context; propose durable lessons with provenance; never silently overwrite canonical shared memory |
| Collaboration | Consult or hand off to a suitable specialist with bounded scope; preserve disagreement and return evidence to Codex |
| Initiative | Raise deduplicated problem/improvement/opportunity proposals; do not self-approve or begin gated work |
| Evaluation | Report observable outcomes, exact checks, failures, limitations, and confidence tied to evidence |

This is a shared minimum contract, not a requirement that every agent independently execute every capability. Tool use, memory writes, implementation, and communication remain role- and permission-bounded.

## 3. Existing agent mapping

| Existing agent | Primary ecosystem responsibility | Nine-capability emphasis | Explicit non-goals / boundary |
|---|---|---|---|
| `repo_explorer` | Research and repository intelligence | Identity, Knowledge, Reasoning, Self-critique, Tools (read-only), Memory retrieval, Collaboration, Initiative proposals, evidence reporting | Read-only discovery; no implementation, commit, deployment, or remote mutation |
| `planner` | Codex planning support and proposal analysis | Identity, Knowledge, Reasoning, Self-critique, Collaboration, Initiative triage input, Evaluation of plan completeness | Planning only; no file edits or execution; Codex makes accept/reject/defer decisions |
| `implementer` | Approved frontend/backend engineering tasks | Identity, Knowledge, Reasoning, Self-critique, Tools, Collaboration, execution checkpoint proposals, verification reporting | Only exact approved scope; no permission/schema/production/deploy changes without required user approval; no test-file ownership when test_engineer owns it |
| `reviewer` | Independent quality review and cross-agent challenge | Identity, Knowledge, Reasoning, Self-critique, read-only Tools, Collaboration, defect/improvement proposals, Evaluation | Read-only; does not replace test_engineer or security_auditor; no implementation |
| `security_auditor` | Defensive security intelligence and escalation | Identity, Knowledge, threat reasoning, Self-critique, read-only security Tools, Collaboration, incident/risk proposals, evidence evaluation | Defensive read-only; no live exploitation, exfiltration, permission change, or destructive testing |
| `test_engineer` | QA, test design, fixtures, harnesses, regression and evaluation cases | Identity, Knowledge, scenario reasoning, Self-critique, approved test Tools, Collaboration, coverage-gap proposals, Evaluation | Owns only approved test/fixture/eval paths; no production implementation or production data changes |

### Capability gaps and deliberate non-duplication

- **Codex Orchestrator is not one of the six specialist agents.** It owns intake, proposal decisions, routing, approval, conflict arbitration, and final reporting.
- **Research is already represented** by `repo_explorer`; do not add a second general researcher without evidence of a distinct capability gap.
- **QA is represented** by `test_engineer`, with `reviewer` as independent code review. These are complementary, not interchangeable.
- **Security is represented** by `security_auditor`.
- **Frontend and Backend are not currently separate named agents.** The existing `implementer` is a generic approved implementation role. It can handle bounded frontend or backend work when its handoff explicitly names the domain, required tools, and acceptance criteria. A split into dedicated specialists is a later proposal only if measured workload/tool/permission differences justify it.
- **Planner is not an autonomous project manager.** It advises; Codex decides and coordinates.
- None of the existing agent definitions proves a persistent runtime, event bus, WhatsApp gateway, or independent permission sandbox.

## 4. Required structured agent report

All agent handoffs should converge on the existing `schemas/agent-result.schema.json` and `templates/agent-result.md`. WS1 extends the existing result schema with optional structured fields for reasoning, self-critique, tools actually used, memory provenance/proposals, collaboration, initiative proposals, and evaluation. These are additive and preserve the existing required fields for compatibility. The common report content is:

1. Task ID, agent ID/role, parent coordinator, and bounded assignment.
2. Outcome: completed, partial, blocked, failed, or proposal-only.
3. Scope performed and explicit non-goals respected.
4. Findings/recommendation with evidence references.
5. Reasoning summary, alternatives considered, and assumptions.
6. Self-critique: uncertainty, missing evidence, counterexample, and potential failure.
7. Tools used, invocation status, and permission level; never imply an unavailable tool ran.
8. Files changed (if authorized) and checkpoint/recovery reference.
9. Verification: exact check/test, result, failures, skips, and limitations.
10. Memory candidates with source/provenance; no direct canonical shared-memory mutation.
11. Collaboration events, specialist responses, conflicts, and unresolved questions.
12. Proposal (if any): class, benefit, risk, effort, dependencies, required approval, deduplication key.
13. Escalation or decision required from Codex/user.

The report must not force read-only agents to invent changed files, tests, or implementation outcomes. Fields may be marked not applicable with a reason.

## 5. Initiative behavior by role

| Agent | Valid proactive proposal examples | Must not do |
|---|---|---|
| repo_explorer | stale docs, architectural inconsistency, missing dependency map, undocumented source-of-truth | modify the repository to fix findings |
| planner | missing prerequisite, safer sequencing, scope ambiguity, measurable acceptance gap | accept its own proposal or start implementation |
| implementer | implementation risk, technical debt discovered in approved scope, missing rollback/test requirement | expand current scope to fix adjacent issues |
| reviewer | confirmed defect, regression risk, maintainability improvement, test gap | edit reviewed code |
| security_auditor | vulnerability/risk escalation, unsafe trust boundary, dependency exposure | exploit live targets or change permissions |
| test_engineer | untested edge case, flaky test, missing regression coverage, weak fixture isolation | modify production implementation |

All proposals are submitted to Codex's proposal triage. Duplicate proposals should reference the canonical proposal/task rather than generate repeated notifications.

## 6. WS1 acceptance criteria

WS1 can be marked complete only when:

- All six existing native definitions and role briefs are mapped to this standard.
- The common report/handoff content is aligned with existing schemas, without creating a competing handoff format.
- Each agent's instructions reference or implement the common standard while preserving its write/read boundaries.
- Research, planning, implementation, review, security, and QA responsibilities have clear ownership and no overlapping write scopes.
- Frontend/backend specialist gaps are explicitly handled without premature agent proliferation.
- Static schema/format/consistency checks pass for changed files.
- Runtime behavior remains BLOCKED / NOT_RUN until a trusted Codex runtime is available.

## 7. Current evidence and remaining WS1 work

The six native TOML definitions and six Markdown role briefs now reference this standard while preserving their role-specific permissions and write boundaries. The shared result schema and report template include optional structured sections for reasoning, self-critique, tools actually invoked, memory provenance/proposals, collaboration, initiative proposals, and evaluation. Seven WS1 behavioral evaluation cases cover these capabilities.

Exact-head GitHub Actions quality gates passed on commit `a48e2073b5a96b3f85c3a38dd66d6754a41ff398` (run [#46071358582](https://github.com/kuuriyawep/-gymsync-codex-toolkit/actions/runs/46071358582)). The run passed unit tests, native/portable parity, project-memory validation, secret scanning, toolkit validation, evaluation-case validation, deterministic evaluation generation, and generated-result validation.

The native/portable audit found 13 matching skill pairs with identical Git blob hashes and no missing or extra skill files. Regression tests cover the legacy result payload, the complete optional intelligence payload, invalid tool-use status rejection, native-agent standard references, role-brief references, and template governance. The full PR diff has been reviewed against WS1's repository-side scope. Runtime behavior remains BLOCKED / NOT_RUN until a trusted Codex runtime is available. No live agent invocation, persistent autonomy, or external integration is claimed.
