# Phase 11 — Evaluation Case to Skill Coverage Matrix

**Snapshot target:** repository HEAD `f83d1c5cbf9d823fa0b4fdadc7d855a99217e011` (Package 4 starting baseline, 2026-11-24)
**Snapshot check:** comparison from the former snapshot `9f14fc7326665153a3629d86de079f7e07a45eec` to this target found no changes to canonical skill files or evaluation case specifications; the matrix metadata is refreshed to the verified baseline.  
**Scope:** all 55 authored evaluation case specifications and all 13 canonical skills.  
**Evidence class:** static mapping only; this is not a behavioral test result.

## Mapping rules

- Every case is assigned to at least one skill based on its declared target, prompt, and expected behaviors.
- Existing scorecard `case_refs` are preserved as direct mappings.
- Additional mappings are marked in the rationale where the case's behavior clearly exercises another skill boundary.
- Mapping a case to a skill does not mean that the skill has passed a runtime test.
- Runtime status remains `NOT_RUN` until a trusted Codex session produces transcript and artifact evidence.

## Coverage by skill

- `change-impact-analysis`: 1 mapped cases
- `clear-technical-communication`: 2 mapped cases
- `code-review`: 3 mapped cases
- `documentation-and-decisions`: 2 mapped cases
- `implementation-planning`: 2 mapped cases
- `project-intelligence`: 8 mapped cases
- `requirements-clarification`: 2 mapped cases
- `risk-aware-tdd`: 4 mapped cases
- `security-review`: 2 mapped cases
- `skill-authoring-and-evaluation`: 9 mapped cases
- `systematic-debugging`: 3 mapped cases
- `verification-gate`: 3 mapped cases
- `workflow-orchestration`: 24 mapped cases

## Complete case matrix

| Evaluation case | Skill mapping | Basis |
|---|---|---|
| `adaptive-autonomy-small-task-vs-substantial-approval` | `workflow-orchestration` | Existing scorecard case gap; target is workflow routing and risk-based approval. |
| `adaptive-lightweight-routing` | `workflow-orchestration` | Direct scorecard reference. |
| `agent-conflict-evidence-resolution` | `workflow-orchestration` | Direct scorecard reference. |
| `agent-failure-recovery` | `workflow-orchestration` | Direct scorecard reference. |
| `agent-output-verification-honesty` | `workflow-orchestration` | Direct scorecard reference. |
| `agent-scope-violation` | `workflow-orchestration` | Agent scope and inherited approval boundary. |
| `agent-selection-and-scope` | `workflow-orchestration` | Direct scorecard reference. |
| `agent-selection` | `workflow-orchestration` | Direct scorecard reference. |
| `ambiguous-bug-report` | `requirements-clarification`, `systematic-debugging` | Direct scorecard references; ambiguity routing and diagnosis. |
| `code-review-evidence-based-finding` | `code-review` | Direct scorecard reference. |
| `code-review-style-preference-near-miss` | `code-review` | Direct scorecard reference. |
| `complete-agent-handoff` | `workflow-orchestration` | Direct scorecard reference. |
| `conflicting-agent-findings` | `workflow-orchestration` | Direct scorecard reference. |
| `critical-failure-dominates` | `skill-authoring-and-evaluation`, `verification-gate` | Evaluation status semantics and final acceptance honesty. |
| `debugging-diagnosis-before-implementation` | `systematic-debugging`, `risk-aware-tdd` | Direct scorecard references; diagnosis-to-implementation boundary. |
| `documentation-ordinary-content-near-miss` | `documentation-and-decisions` | Direct scorecard reference. |
| `documentation-source-of-truth-decision-record` | `documentation-and-decisions` | Direct scorecard reference. |
| `evaluation-runner-honesty` | `skill-authoring-and-evaluation`, `clear-technical-communication` | Evaluation runner limits and honest reporting. |
| `handoff-approval-inheritance` | `workflow-orchestration` | Direct scorecard reference. |
| `immutable-run-history` | `skill-authoring-and-evaluation` | Evaluation runner and immutable evidence history. |
| `implementation-planning-multi-task-approval-recovery` | `implementation-planning` | Direct scorecard reference. |
| `implementation-planning-trivial-change-near-miss` | `implementation-planning` | Direct scorecard reference. |
| `independent-review-findings` | `workflow-orchestration` | Direct scorecard reference. |
| `independent-reviewer-finds-defect` | `code-review`, `workflow-orchestration` | Independent reviewer role, read-only review, evidence-backed findings. |
| `memory-decision-recall` | `project-intelligence` | Direct scorecard reference. |
| `memory-fact-vs-assumption` | `project-intelligence` | Direct scorecard reference. |
| `memory-project-isolation` | `project-intelligence` | Direct scorecard reference. |
| `memory-source-authority` | `project-intelligence` | Direct scorecard reference. |
| `memory-stale-detection` | `project-intelligence` | Direct scorecard reference. |
| `memory-targeted-retrieval` | `project-intelligence` | Direct scorecard reference. |
| `memory-task-resumption` | `project-intelligence` | Direct scorecard reference. |
| `memory-unverified-claim` | `project-intelligence` | Direct scorecard reference. |
| `parallel-work-boundaries` | `workflow-orchestration` | Parallel task independence and ownership boundaries. |
| `parallel-write-boundaries` | `workflow-orchestration` | Direct scorecard reference. |
| `preserve-existing-ui` | `change-impact-analysis`, `requirements-clarification` | Direct scorecard references; preserve scope and existing behavior. |
| `production-data-deletion` | `security-review` | Direct scorecard reference. |
| `risk-aware-tdd-test-first-handoff` | `risk-aware-tdd`, `systematic-debugging` | Direct scorecard references. |
| `risk-overrides-complexity` | `workflow-orchestration` | Direct scorecard reference. |
| `session-state-approval-gate` | `workflow-orchestration` | Direct scorecard reference. |
| `skill-authoring-boundary-and-overlap-audit` | `skill-authoring-and-evaluation` | Direct scorecard reference. |
| `skill-authoring-contract-and-coverage` | `skill-authoring-and-evaluation` | Direct scorecard reference. |
| `skill-authoring-ordinary-documentation-request` | `skill-authoring-and-evaluation` | Direct scorecard reference. |
| `skill-authoring-out-of-scope-routing` | `skill-authoring-and-evaluation` | Direct scorecard reference. |
| `skill-authoring-runtime-unavailable` | `skill-authoring-and-evaluation` | Direct scorecard reference. |
| `skill-authoring-tool-limited-skill-design` | `skill-authoring-and-evaluation` | Direct scorecard reference. |
| `tenant-isolation-review` | `security-review` | Direct scorecard reference. |
| `test-engineer-scope-and-ownership` | `workflow-orchestration`, `risk-aware-tdd` | Agent write ownership, test/implementation separation, sequencing. |
| `unverified-completion-claim` | `clear-technical-communication`, `verification-gate` | Direct scorecard references. |
| `verification-gate-final-acceptance` | `verification-gate`, `risk-aware-tdd` | Direct scorecard references. |
| `workflow-ledger-approval-and-completion-gates` | `workflow-orchestration` | Direct scorecard reference. |
| `workflow-ledger-idempotency-and-event-integrity` | `workflow-orchestration` | Direct scorecard reference. |
| `workflow-ledger-no-autonomous-execution` | `workflow-orchestration` | Direct scorecard reference. |
| `workflow-ledger-private-store-boundary` | `workflow-orchestration` | Direct scorecard reference. |
| `workflow-ledger-resume-and-recovery` | `workflow-orchestration` | Direct scorecard reference. |
| `workflow-ledger-retry-timeout-cancellation` | `workflow-orchestration` | Direct scorecard reference. |

## Audit findings

1. All 55 case specifications are mapped; no case remains unassigned.
2. The mapping exposes uneven distribution: `workflow-orchestration` carries the largest cross-cutting suite, while several specialist skills have only one or two direct cases.
3. The current scorecards are not uniformly refreshed: 12 of 13 scorecards still point to revision `f47bb2857d5fe33e390f02bf94c68ea3e3e488d5`; `project-intelligence` was refreshed separately. This matrix does not silently rewrite those historical review records.
4. Some scorecards have incomplete formal coverage labels despite having case references. Those scorecards need an explicit re-review/update before claiming the rubric's in-scope / near-miss / edge coverage gate.
5. This matrix is a planning and traceability artifact. It does not promote `NOT_RUN` to `PASS`.

## Next required action

Refresh the remaining 12 static scorecards against the current canonical skill content, repair evidence anchors that do not match actual headings, and reconcile each scorecard's case count and coverage labels with this matrix. Preserve all runtime statuses as `NOT_RUN`.
