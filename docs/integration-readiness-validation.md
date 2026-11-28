# Integration Readiness & End-to-End Validation

**Status:** Repository-side contract validation in progress; live behavioral execution BLOCKED / NOT_RUN.  
**Scope:** Toolkit repository only. No GymSync application/database, production systems, external services, credentials, or permissions.  
**Authority:** Codex remains the central coordinator; the user retains final authority for consequential actions.

## 1. Purpose

This cross-cutting validation closes the gap between individually documented workstream contracts and one traceable integrated scenario. It extends existing schemas, workflow records, evaluation cases, and CI tests; it does not introduce another router, task engine, approval engine, event bus, or runtime.

## 2. Canonical scenario

The machine-readable scenario is `evals/cases/integrated-security-backend-qa-approval-report.json`. Its ordered path is:

1. Security records a critical finding from a safe synthetic signal.
2. Codex validates evidence, deduplicates, classifies risk, and delegates bounded work.
3. Backend proposes an isolated fix without production access.
4. QA independently validates the fix and regression behavior.
5. Codex arbitrates evidence and preserves unresolved disagreement.
6. The user approves an exact R4 action only when one is actually requested.
7. The WhatsApp gateway may deliver a redacted, identity-verified report or approval request; delivery is not approval.

The scenario also enumerates unavailable specialists/runtime, conflicting findings, delivery failure, duplicate/replayed events, false positives, unauthorized actions, partial recovery, and unavailable Codex.

## 3. Cross-contract invariants

- Each stage has an explicit owner, predecessor, required evidence, and prohibited behavior.
- Event, task, handoff, result, review, approval, and report identifiers must remain traceable; an implementation adapter must validate references against the canonical contracts before execution.
- A specialist handoff does not grant authority or permissions.
- QA remains independent from implementation ownership.
- Approval is bound to one exact action and payload; it is not reusable and cannot be supplied by an agent.
- Messaging identity, deduplication, expiry, redaction, and delivery state fail closed.
- No production data, production write, real vulnerability exploitation, or external message is used by this repository-side simulation.

## 4. Evidence and acceptance

| Layer | Acceptance | Current status |
|---|---|---|
| Schema structure and conditional constraints | Deterministic tests inspect required fields, conditional rules, and closed contracts | Pending CI |
| Scenario completeness | Deterministic tests validate ordered stages, ownership, evidence, prohibitions, and all listed failure paths | Pending CI |
| Cross-contract execution | Trusted runtime demonstrates event-to-report lifecycle and consistent identifiers | BLOCKED / NOT_RUN |
| Host permission enforcement | Runtime proves denied unauthorized actions and exact-action approval binding | BLOCKED / NOT_RUN |
| WhatsApp delivery and identity | Authorized safe test proves inbound/outbound identity, dedupe, delivery receipts, and fail-closed behavior | BLOCKED / NOT_RUN |
| Human acceptance | User reviews evidence and explicitly accepts residual risks | NOT_RUN |

A repository test can prove that the contract is internally represented and structurally consistent. It cannot prove that agents actually collaborate, runtime permissions are enforced, or messages are delivered.

## 5. Memory proposal hardening

The memory proposal schema now requires a non-empty target memory ID for `revise`, `supersede`, `mark_stale`, and `dispute`; requires a non-empty decision maker and rationale for `accepted` and `rejected`; and prevents specialist-role metadata from being attached to non-specialist scope. These are schema constraints, not proof of semantic correctness or live Codex governance.

## 6. Architecture reconciliation

This document is the current integration-readiness addendum to the seven-workstream architecture. The canonical architecture's historical implementation-status statements and immediate execution order must be reconciled to the post-WS7 repository state before this work is considered fully closed. The current project checkpoint remains authoritative for merged workstream status; runtime and behavioral acceptance remain blocked until a trusted runtime exists.

## 7. Exit criteria

- Memory schema edge cases have deterministic regression coverage.
- The integrated scenario and all failure paths have deterministic repository-side coverage.
- Exact-head CI passes and the full PR diff is reviewed.
- Canonical architecture and project checkpoint agree on WS1–WS7 completion, current workstream, evaluation inventory, and next action.
- No behavioral/runtime PASS is claimed without direct execution evidence.
