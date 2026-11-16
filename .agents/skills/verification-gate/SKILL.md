---
name: verification-gate
description: Perform the final evidence-based acceptance check for completed work, inspect scope and regressions, and report passed, failed, skipped, and unrun checks accurately.
---
# Verification Gate

## When to use
Use after implementation or another deliverable is ready for acceptance, before reporting it complete or release-ready.

This is the final verification procedure. It does not diagnose an unknown defect, implement fixes, or replace focused test design during TDD.

## Inputs
- User-approved scope and observable acceptance criteria.
- Changed files, diff, or delivered artifact.
- Tests/checks already run and their actual outputs.
- Relevant project instructions and risk constraints.

If acceptance criteria are missing, derive only what is directly supported by the approved request and existing specifications. Mark gaps as unresolved; do not invent acceptance criteria.

## Procedure
1. Map each acceptance criterion to one or more concrete checks and identify the changed surfaces those checks cover.
2. Inspect the final diff or artifact for unintended changes, secrets, generated noise, scope creep, and compatibility concerns.
3. Run the narrowest relevant checks first, then broader integration, build, type, lint, or end-to-end checks when proportionate and available.
4. Verify configuration and migration consistency without applying production changes unless explicitly approved.
5. For high-risk changes, confirm that required security, authorization, data-integrity, failure, and independent-review evidence exists. Missing evidence remains a gap.
6. Record exact commands or manual procedures, environment where relevant, and actual outcomes.
7. Classify every check as `PASSED`, `FAILED`, `SKIPPED`, or `NOT_RUN`. Explain skipped/unrun checks and blockers.
8. Compare results against acceptance criteria. Report partial or blocked completion when required checks are missing or failing.

## Required output
- Acceptance criteria and corresponding evidence.
- Diff/scope inspection result.
- Checks run: exact command/procedure and outcome.
- Checks skipped or not run: reason and impact.
- Review/security evidence required by the task and any gaps.
- Remaining defects, risks, limitations, and release blockers.
- Overall disposition: `PASS`, `FAIL`, or `BLOCKED/PARTIAL`, with rationale.

## Boundaries and stop conditions
- Verification owns final acceptance evidence and honest reporting; it does not implement fixes or convert an unrun check into a pass.
- A passing subset of checks does not establish whole-system correctness or production security.
- Stop and report a blocker if required tooling, test data, permissions, or environment is unavailable.
- Do not run destructive, production, deployment, or external side-effect checks without explicit approval.
- Never claim success based only on code inspection, expected behavior, or another agent's unsupported assertion.
