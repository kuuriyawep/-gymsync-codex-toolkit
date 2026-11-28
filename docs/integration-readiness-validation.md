# Integration Readiness & End-to-End Validation

**Status:** MERGED into main via PR #23; repository-side deterministic contract validation PASS (exact-head CI run #380, 12/12 quality gates); live behavioral execution BLOCKED / NOT_RUN.  
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
| Schema structure and conditional constraints | Deterministic tests inspect required fields, conditional rules, and closed contracts | PASS — exact-head CI run #378 |
| Scenario completeness | Deterministic tests validate ordered stages, ownership, evidence, prohibitions, and all listed failure paths | PASS — exact-head CI run #380 |
| Cross-contract execution | Trusted runtime demonstrates event-to-report lifecycle and consistent identifiers | BLOCKED / NOT_RUN |
| Host permission enforcement | Runtime proves denied unauthorized actions and exact-action approval binding | BLOCKED / NOT_RUN |
| WhatsApp delivery and identity | Authorized safe test proves inbound/outbound identity, dedupe, delivery receipts, and fail-closed behavior | BLOCKED / NOT_RUN |
| Human acceptance | User reviews evidence and explicitly accepts residual risks | NOT_RUN |

A repository test can prove that the contract is internally represented and structurally consistent. It cannot prove that agents actually collaborate, runtime permissions are enforced, or messages are delivered.

## 5. Memory proposal hardening

The memory proposal schema now requires a non-empty target memory ID for `revise`, `supersede`, `mark_stale`, and `dispute`; requires a non-empty decision maker and rationale for `accepted` and `rejected`; and prevents specialist-role metadata from being attached to non-specialist scope. These are schema constraints, not proof of semantic correctness or live Codex governance.

## 6. Architecture reconciliation

This document is the merged integration-readiness addendum to the seven-workstream architecture. PR #23 is merged at `e48c7349a73c4830b8d54a5d505e483907799798` (source head `dae5f5a8f8424aec3406ea7cbe7d104fb392199e`). Exact-head CI run #380 (`46095000958`) passed all 12 repository quality gates. The canonical architecture and `PROJECT_STATE.md` have been reconciled to this post-merge state. Runtime and behavioral acceptance remain BLOCKED / NOT_RUN until a trusted runtime exists.

## 7. Exit criteria

- Memory schema edge cases have deterministic regression coverage.
- The integrated scenario and all failure paths have deterministic repository-side coverage.
- Exact-head CI passes and the full PR diff is reviewed. **Complete:** PR #23 exact-head run #380 passed 12/12; PR #23 merged.
- Canonical architecture and project checkpoint agree on WS1–WS7 completion, integration-readiness closeout, evaluation inventory, and next action. **Complete:** checkpoint reconciliation merged through this follow-up branch/PR.
- No behavioral/runtime PASS is claimed without direct execution evidence.
