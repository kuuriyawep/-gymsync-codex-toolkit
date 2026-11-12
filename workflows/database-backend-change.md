# Database and Backend Change

## Workflow
1. **Inspect (read-only):** Review schema, migrations, constraints, indexes, RLS/policies/grants, triggers/functions, API call sites, and existing records relevant to the change.
2. **Model:** Confirm tenant/data ownership, roles, invariants, state transitions, idempotency, and expected behavior for existing and new records.
3. **Audit:** Prefer read-only queries and representative fixtures before proposing mutations. Never infer production data state from mock data.
4. **Plan:** Specify migration order, compatibility window, backfill strategy, validation queries, rollback/forward-fix plan, and deployment sequence.
5. **Approval gate:** Obtain explicit approval before destructive SQL, production writes, backfills, permission/RLS changes, secret rotation, or deployment.
6. **Implement:** Use least-privilege server-side operations, validated inputs, transactional boundaries, and idempotency where appropriate.
7. **Test:** Cover valid, invalid, duplicate/retry, unauthorized, cross-tenant, boundary, concurrency, and failure cases as relevant.
8. **Verify:** Check schema/policies and application behavior. Use safe read-only validation after changes where possible.
9. **Report:** State precisely which files/migrations/commands were applied, where, and what remains pending.

## Stop conditions
- Stop if data ownership, tenant boundary, or expected accounting/state behavior is ambiguous.
- Do not run production mutations or destructive migrations without explicit approval and a rollback plan.
- Do not expose database credentials, tokens, or personal data.

## Required output
- Current-state findings and evidence
- Invariants and proposed state transitions
- Migration/change plan and compatibility risks
- Approval status and execution environment
- Validation queries/tests and exact outcomes
- Applied vs unapplied changes, rollback path, and residual risks