# Feature Delivery

## Workflow
1. **Explore:** Read project instructions and inspect existing UX, architecture, conventions, related flows, tests, and data models.
2. **Clarify:** Define user problem, roles, primary/alternate flows, constraints, non-goals, and observable acceptance criteria.
3. **Impact:** Map frontend, backend, database, authentication/authorization, integrations, analytics, and compatibility impacts.
4. **Plan:** Break delivery into small vertical slices. For each task specify intended behavior, likely files, dependencies, tests, and risks.
5. **Approval gate:** Present the plan before implementation when requested. Obtain explicit approval before scope expansion, schema/data changes, permission changes, production actions, or irreversible remote effects.
6. **Implement:** Deliver one approved slice at a time. Preserve established UX and architecture unless redesign is explicitly in scope.
7. **Test:** Cover happy paths, validation, permissions, empty/loading/error states, duplicate submissions, and relevant boundaries.
8. **Review:** Compare the diff against every acceptance criterion; inspect security, data integrity, regressions, and maintainability.
9. **Verify:** Run targeted tests and relevant broader checks; inspect the final diff and changed files.
10. **Document:** Update user-facing or technical docs when behavior, setup, operations, or decisions changed.

## Stop conditions
- Ask one focused question when a material product decision is unresolved.
- Do not silently replace existing behavior or expand the feature.
- Stop before unapproved migrations, production writes, deployment, or external side effects.

## Required output
- Requirement brief and non-goals
- Approved implementation plan
- Delivered slices and changed files
- Acceptance criteria status (pass/fail/not verified)
- Tests/checks run and not run
- Remaining risks and follow-up decisions