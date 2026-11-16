---
name: implementation-planning
description: Create a bounded, dependency-aware implementation plan with observable acceptance criteria, risk controls, and verification gates.
---
# Implementation Planning

## When to use
Use before a non-trivial feature, refactor, migration, or multi-file change. Trivial, localized, reversible work may use a lightweight plan.

## Procedure
1. Confirm goal, user-visible outcome, scope, non-goals, constraints, and acceptance criteria.
2. Inspect architecture, conventions, relevant source, tests, and dependency boundaries.
3. Split work into small ordered tasks; identify dependencies and one owner per task.
4. For each task, state intended behavior, expected files/surfaces, prerequisites, and completion evidence.
5. Assess complexity and risk separately. Explicitly flag schema changes, data backfills, auth/RLS, secrets, production actions, external side effects, and irreversible operations.
6. Define test strategy, review needs, rollout sequence, rollback/recovery, and unresolved decisions.
7. Identify approval gates. Ask for approval before implementation when the user requested it or when risk/policy requires it.

## Required plan
- Goal, scope, and non-goals.
- Acceptance criteria and assumptions.
- Ordered tasks with dependencies, likely files, owners, and exit criteria.
- Complexity/risk assessment and mitigations.
- Test, review, and verification plan.
- Approval gates, rollout, rollback, and unresolved decisions.

## Completion criteria
Planning is complete when each task has a verifiable outcome, dependencies are ordered, material risks and approvals are visible, and the user can judge whether the proposed scope is correct.

## Boundaries
Do not implement while planning. Do not present guessed file paths or unverified architecture as facts; label them as expected locations until inspected.
