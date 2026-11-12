# Permissions and Approval Policy
Default posture: inspect and explain before acting.
- Read-only: inspect files, trace code, run safe tests, and draft plans.
- Approval required: broad refactors, schema migrations, production writes, destructive commands, permission changes, external communications, deployment, billing, or actions with irreversible side effects.
- Least privilege: use only the repository, environment, and permissions needed for the task.
- Secrets: never print, commit, or store credentials in toolkit files.
- Scope: approval for one task does not authorize unrelated work.
- Stop conditions: unexpected data loss risk, unclear ownership, missing authorization, or a materially changed plan.
Record what was approved and what was actually performed.