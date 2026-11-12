---
name: implementation-planning
description: Create a bounded, dependency-aware implementation plan with approval and verification gates.
---
# Implementation Planning
- Confirm goal, scope, non-goals, and acceptance criteria.
- Inspect architecture and conventions.
- Split work into small tasks ordered by dependencies.
- For each task state expected files, behavior, risks, and tests.
- Explicitly flag schema changes, data backfills, auth/RLS, secrets, production actions, and irreversible operations.
- Include rollback and release sequencing where applicable.
- Ask for approval before implementation when requested or when risk warrants it.
Do not implement while planning.