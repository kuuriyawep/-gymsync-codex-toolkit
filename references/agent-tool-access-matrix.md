# Agent Tool Access Matrix

**Status:** Phase 8 proposed task-level profiles; not an independent runtime permission system.

## Core rule

Codex custom agents inherit the parent session's sandbox, approval policy, provider, and MCP servers. The matrix defines what each role should use for its assigned task. It does not create a per-agent security boundary.

## Role profiles

| Role | Profile ID | Permitted task-level capabilities | Prohibited task-level actions |
|---|---|---|---|
| `repo_explorer` | `repo-readonly` | Read approved repository files, Git metadata, test definitions/results, approved read-only graph queries | File writes, commits, remote mutations, deployments, production access |
| `planner` | `planning-readonly` | Read relevant source, instructions, project memory, tests, and audit evidence | File writes, implementation, commits, external side effects |
| `implementer` | `approved-scoped-write` | Read relevant files; edit exact approved code/docs/test paths; run approved local tests | Scope expansion, unrelated refactors, commits/pushes/merges/deployments/production writes without separate approval |
| `reviewer` | `independent-review-readonly` | Read diff, source, tests, logs, generated artifacts | Edit reviewed files, commit, deploy, alter remote state |
| `security_auditor` | `defensive-security-readonly` | Read auth/authz, RLS/grants, APIs, dependencies, secrets handling, logs with redaction | Exploit live systems, exfiltrate secrets/data, change permissions, destructive tests |
| `test_engineer` | `test-scope-write` | Read code; edit owned test files/fixtures/evaluation cases; run approved tests in disposable environments | Production code edits, production data, uncontrolled network, external side effects

## Enforcement layers

1. **Parent sandbox:** actual filesystem/network/process boundary for the entire session.
2. **Parent approval policy:** controls when the session must stop for permission.
3. **MCP server allowlist:** restricts tools exposed by a configured server at the parent level.
4. **Capability reductions:** custom agent feature flags may disable supported features such as shell, apps, plugins, memories, or permission-request tools.
5. **Handoff and task validator:** checks declared owner, scope, approval, dependencies, and result evidence.
6. **Independent review:** detects whether the actual diff exceeded the assigned scope.

Only layers 1–4 are runtime/host controls. Handoff schemas and reviewer checks are procedural controls and must never be represented as a sandbox.

## Least-privilege defaults

- No agent receives a separate credential set through this matrix.
- Do not give agents raw secrets or broad environment dumps.
- External tools are available only if configured and exposed by the parent session.
- Read-only roles return findings; they do not edit files.
- A write task must have one owner and exact approved write paths.
- Shared-file changes are sequenced, not run concurrently.
- The parent Codex session validates outputs and owns final decisions.
