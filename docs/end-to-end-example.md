# End-to-End Example: A Small Bug Fix

> Illustrative walkthrough only. This document demonstrates how the toolkit components fit together; it is not evidence that Codex executed this workflow or that any agent/runtime behavior has been tested.

## Example request

"On the settings page, saving a valid profile sometimes shows a success message but the new value is not visible after refresh. Investigate and fix it. Do not change the page design."

This example uses a hypothetical repository. The symptom and root cause below are invented for demonstration.

## 1. Intake and scope

Codex reads the target repository's `AGENTS.md` and identifies:

- **Outcome:** saved profile values persist and appear after refresh.
- **In scope:** trace the profile-save flow, reproduce the issue, implement the smallest approved fix, and add a regression test.
- **Out of scope:** redesigning settings, changing unrelated profile fields, deploying, or modifying production data.
- **Acceptance criteria:** a valid update persists; a refresh displays the saved value; validation errors remain visible; failed saves do not show success.

If the expected behavior or affected account role is unclear and materially changes the investigation, Codex asks one focused question.

## 2. Triage and routing

Codex consults `workflows/registry.md`:

- **Primary category:** Bug.
- **Primary workflow:** [Bug Investigation and Fix](../workflows/bug-fix.md).
- **Complexity:** Moderate (several layers may be involved).
- **Risk:** Medium until persistence and authorization boundaries are understood.
- **Execution mode:** Codex coordinates; a read-only `repo_explorer` may trace the save path if useful.

Complexity and risk are assessed separately. If evidence reveals a tenant-isolation or production-data issue, risk is reassessed and the stricter approval gates apply.

## 3. Discovery and diagnosis

Codex reads the selected workflow and relevant skills:

- `systematic-debugging`
- `change-impact-analysis`
- `risk-aware-tdd`
- `verification-gate`

The explorer receives a bounded read-only handoff using `templates/agent-handoff.md`: identify the settings form, submit handler, API endpoint, persistence layer, and related tests. The explorer returns exact paths and evidence, not code changes.

**Hypothetical finding:** the form submits the new value, but the API handler updates a different field name. The success response is returned even though the intended field was not changed.

Codex must verify this against current source and a safe reproduction. The example finding is not a claim about any real repository.

## 4. Plan and approval

Codex proposes a narrow fix:

1. Align the API update field with the persisted schema.
2. Return an error if the update fails or affects no authorized record.
3. Add a regression test for save → reload.
4. Run focused tests and relevant broader checks.
5. Inspect the diff for unrelated changes.

No production write, migration, permission change, deployment, or scope expansion is included. If one becomes necessary, Codex stops and requests explicit user approval before proceeding.

## 5. Implementation

After the user approves the stated code-change scope, the implementer may receive a bounded handoff. It owns only the named handler and test files. It must not redesign the page or edit files assigned to another concurrent task.

Codex remains accountable and checks the returned diff against the approved plan.

## 6. Verification and independent review

The verification gate records exact commands and outcomes:

- Focused regression test: **PASS** only if actually run and successful.
- Related API tests: **PASS / FAIL / NOT RUN**, with evidence.
- Build/type/lint checks: report the actual result.
- Manual save-and-refresh scenario: record environment and observed result.
- Final diff and scope inspection: record findings.

For a security-sensitive or cross-tenant path, a separate read-only reviewer or security auditor should inspect the completed change. Use `templates/agent-review-report.md`; a clean review is limited to the reviewed scope.

This example does not provide actual test output. No result should be marked PASS merely because the proposed fix looks plausible.

## 7. Completion report

Codex reports:

- **Outcome:** complete, partial, blocked, or failed.
- **Changed files:** exact repository paths.
- **Behavior changed:** concise description.
- **Checks:** passed, failed, skipped, or not run, with commands/evidence.
- **Review:** findings and scope limitations.
- **Residual risks:** unresolved issues and assumptions.
- **Next action:** only if work remains.

The task is complete only when the approved acceptance criteria have evidence-backed outcomes. Otherwise Codex reports a partial or blocked result rather than overstating success.

## Components used

| Component | Purpose |
|---|---|
| `AGENTS.md` | Repository authority and safety rules |
| `workflows/registry.md` | Routing and risk classification |
| `workflows/bug-fix.md` | Procedure of record |
| Skills | Focused investigation, impact, testing, and verification guidance |
| `.codex/agents/*.toml` | Optional bounded specialist roles |
| `templates/agent-handoff.md` | Assignment contract |
| `templates/agent-review-report.md` | Independent review evidence |
| Tests and validators | Reproducible verification |

