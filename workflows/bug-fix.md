# Bug Investigation and Fix

## Workflow
1. **Explore (read-only):** Read repository instructions; inspect the narrowest relevant code, tests, logs, and recent changes. Reproduce safely when possible.
2. **Clarify:** Record expected vs actual behavior, affected users/roles, environment, reproduction steps, and observable acceptance criteria. Resolve material ambiguity before consequential action.
3. **Diagnose (when cause is unknown):** Apply `systematic-debugging`. It owns safe reproduction, causal tracing, root-cause confidence, alternatives, and the proposed regression scenario. It must not implement the fix. If a reliable root cause is already established, record its evidence and do not repeat diagnosis unnecessarily.
4. **Plan:** Define the smallest correction, regression/acceptance tests, broader checks, affected files, risks, and rollback approach. Carry the diagnosis evidence and uncertainty into the plan.
5. **Approval gate:** Stop for approval before expanding scope, changing production data/configuration, running destructive commands, or making irreversible/remote changes. Approval is limited to the stated scope.
6. **Implement:** Apply `risk-aware-tdd` to the approved behavior. Inspect the existing test conventions, add a focused failing regression test first where practical, then make the smallest compatible change. If test-first is infeasible, record why and define an alternative check.
7. **Review:** Check specification compliance, edge cases, authorization/data integrity, and unintended changes. Use an independent reviewer for sensitive or high-risk paths when available.
8. **Verify:** Apply `verification-gate` as the final cross-surface acceptance check. Map criteria to evidence, inspect the final diff, run proportionate checks, and classify each check as `PASSED`, `FAILED`, `SKIPPED`, or `NOT_RUN`.
9. **Report:** Separate diagnosis evidence, implementation evidence, and final acceptance status. List changed files, exact checks/outcomes, unrun checks, unresolved risks, and rollback notes.

## Skill ownership and handoffs
- `systematic-debugging` → diagnosis only; hands evidence, confidence, alternatives, and a regression scenario to planning/implementation.
- `risk-aware-tdd` → approved test and implementation work; hands changed paths and exact test evidence to verification.
- `verification-gate` → final acceptance evidence and disposition; does not diagnose or implement.
- Do not ask multiple skills to own the same phase. Codex remains the coordinator and validates each handoff.

## Stop conditions
- Stop and ask one focused question if expected behavior cannot be determined from context.
- Stop before risky side effects or scope expansion.
- If reproduction is impossible, continue only with clearly labelled evidence and uncertainty; do not claim the bug is reproduced.
- If root cause remains unresolved, do not silently turn a hypothesis into an approved implementation requirement.
- If required verification tooling or evidence is unavailable, report partial/blocked completion rather than claiming a pass.

## Required output
- Symptom and reproduction status
- Root cause, confidence, and evidence (or unresolved hypothesis)
- Proposed correction and regression scenario
- Approval status and scope
- Files/behavior changed
- Tests/checks run and exact outcomes
- Checks not run, remaining risks, and rollback notes
