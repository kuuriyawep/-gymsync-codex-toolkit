# Database and Backend Change
1. Inspect current schema, migrations, constraints, indexes, RLS/grants, and call sites.
2. Confirm data ownership, tenant boundaries, expected state transitions, and compatibility.
3. Prefer a read-only data audit before proposing mutations.
4. Plan migration order, backfill, validation queries, rollback, and deployment coordination.
5. Obtain explicit approval before destructive SQL, production writes, or permission changes.
6. Implement least-privilege server-side logic and idempotent operations where appropriate.
7. Test valid, invalid, duplicate, unauthorized, boundary, and failure cases.
8. Verify schema and application behavior; report exactly what was and was not applied.