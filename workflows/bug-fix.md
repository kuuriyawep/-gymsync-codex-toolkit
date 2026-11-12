# Bug Investigation and Fix

## Workflow
1. **Explore (read-only):** Read repository instructions; inspect the narrowest relevant code, tests, logs, and recent changes. Reproduce safely when possible.
2. **Clarify:** Record expected vs actual behavior, affected users/roles, environment, reproduction steps, and observable acceptance criteria.
3. **Impact:** Trace the failing path through inputs, state transitions, persistence, APIs, permissions, and dependent components.
4. **Diagnose:** State the leading root-cause hypothesis, supporting evidence, alternatives considered, and what would falsify it. Do not treat correlation as proof.
5. **Plan:** Propose the smallest fix, regression test, broader checks, affected files, and rollback approach if needed.
6. **Approval gate:** Stop for approval before expanding scope, changing production data/configuration, running destructive commands, or making irreversible/remote changes.
7. **Implement:** Add a focused regression test that demonstrates the defect; make the smallest compatible change.
8. **Review:** Check specification compliance, edge cases, authorization/data integrity, and unintended changes. Use an independent reviewer for sensitive or high-risk paths when available.
9. **Verify:** Run the focused test and relevant integration/build/type/lint checks. Inspect the final diff.
10. **Report:** Separate verified facts from assumptions and list any checks not run.

## Stop conditions
- Stop and ask one focused question if expected behavior cannot be determined from context.
- Stop before risky side effects or scope expansion.
- If reproduction is impossible, continue only with clearly labelled evidence and uncertainty; do not claim the bug is reproduced.

## Required output
- Symptom and reproduction
- Root cause and evidence (or unresolved hypothesis)
- Files/behavior changed
- Tests/checks run and exact outcomes
- Checks not run, remaining risks, and rollback notes