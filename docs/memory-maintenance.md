# Memory maintenance procedure

## When to update
Update project memory when a task discovers a durable architecture fact, changes a module boundary, alters a schema or integration contract, resolves a material unknown, or reaches a meaningful task handoff.

Do not update it for every small code edit. Keep the current-state checkpoint concise.

## Update procedure
1. Identify the exact memory page affected.
2. Inspect current source, tests, schemas, configuration, and relevant user decisions.
3. Draft the smallest useful change.
4. Label claims Verified, Assumption, Unknown, or Stale.
5. Add source references and verification date/commit.
6. Preserve decision history; mark replaced decisions Superseded.
7. Run the project-memory validator and relevant tests.
8. Review the diff for secrets, personal data, duplicated source content, and unsupported claims.
9. Obtain approval where required by the repository's approval policy.

## Revalidation triggers
Revisit a page when its cited file or contract changes, a referenced test is removed or altered, a decision is superseded, or its freshness window expires. A changed commit alone does not automatically invalidate every memory page.

## Session handoff
At the end of substantial work, update `current-state.md` with objective, owner, completed work, changed paths, verified findings, checks actually run, decisions/approval status, blockers, and one clear next action.

A new Codex session should read the checkpoint, retrieve only relevant memory, and verify current repository state before continuing.

## Recovery from stale or conflicting memory
Do not guess. Mark the claim Stale, inspect current source, update the evidence, and record unresolved conflict. If the source of truth cannot be determined, report uncertainty and ask for a decision.
