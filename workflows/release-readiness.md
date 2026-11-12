# Release Readiness

## Workflow
1. Confirm release scope, target environment, version/commit, and acceptance criteria.
2. Inspect the complete diff, configuration, migrations, dependency changes, permissions, and secret exposure.
3. Run available tests, build, type checks, lint, and relevant security checks; record exact commands and outcomes.
4. Verify critical user journeys, authorization/tenant boundaries, error handling, and migration compatibility.
5. Confirm operational readiness: backups where relevant, rollback/forward-fix plan, monitoring, logging, and ownership.
6. Classify every check as passed, failed, skipped, or not applicable, with evidence.
7. List blockers, accepted risks, and required decisions.
8. Obtain explicit approval before deployment, production writes, or irreversible remote actions.
9. Report readiness as **ready**, **conditionally ready**, or **blocked**.

## Stop conditions
- Do not deploy or trigger production actions as part of a readiness review unless explicitly authorized.
- A skipped critical check is not a pass.
- Do not declare readiness when a release blocker remains unresolved.

## Required output
- Release identifier, scope, and environment
- Acceptance criteria and critical journey status
- Checks run with exact results; skipped checks and reasons
- Migration/rollback and operational readiness
- Blockers and accepted risks
- Readiness decision with concise evidence