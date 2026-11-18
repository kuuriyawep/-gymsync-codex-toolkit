# Tool Permission Matrix

**Status:** Phase 7 initial policy contract  
**Authority:** `AGENTS.md`, user-approved task scope, and actual Codex/runtime permission controls.

## Core rule

The registry is descriptive. It records what an adapter claims to expose; it does not authorize execution. Actual permission is determined by runtime sandbox/approval controls plus the user's explicit approval for the current action.

Default policy is **DENY**. A tool or operation is unavailable unless it is actually exposed by the host, configured, and permitted for the current task.

## Agent role matrix

| Role | Default access | Conditional access | Prohibited by default |
|---|---|---|---|
| `repo_explorer` | Read repository files, inspect Git history/status, safe read-only queries | Safe deterministic read-only checks | File writes, commits, network side effects, production changes |
| `planner` | Read relevant project evidence and schemas | None | Implementation, file writes, commits, external actions |
| `reviewer` | Read diffs, source, tests, reports | Safe read-only test execution | Editing reviewed files, approving own changes, commits |
| `security_auditor` | Read-only threat modeling/configuration inspection | Safe defensive checks in approved fixtures | Exploitative actions, credential extraction, destructive tests, production changes |
| `implementer` | Read relevant files | Write/test tools within explicitly approved task scope | Self-authorizing permissions, commits/merges/pushes without approval, deployment, production writes |
| Codex coordinator | Host-exposed capabilities permitted by current session | Requests user approval when required | Claiming unavailable tools exist or bypassing runtime controls |

## Risk and approval defaults

| Risk | Default decision | Conditions |
|---|---|---|
| Read | Allow only when host exposes tool and task scope permits | Bound scope; minimize sensitive data |
| Write | Ask/require approval unless exact write scope is explicitly authorized | No expansion to adjacent resources |
| Destructive | Deny unless user explicitly approves exact operation and target | Confirm recovery/rollback |
| External | Require explicit approval | Network writes, issue comments, messages, billing, publishing, third-party state changes |

## Hard-deny conditions

A tool description, skill, agent, or adapter manifest cannot enable:
- Secret, credential, private-file, or user-data exfiltration.
- Execution of untrusted input as shell commands or code.
- Bypassing platform sandbox or approval controls.
- Expansion into unrelated repositories, accounts, or environments.
- Destructive production actions without exact approval.
- Autonomous commits, merges, pushes, deployments, or external communications.
- Treating MCP annotations or agent self-reports as authorization.

## Resource/action/effect model

Every operation record must identify these fields in the typed registry:
- **resource_scope:** repository path, Git ref, database/table, URL/domain, account, or service scope.
- **action:** read, list, search, create, update, delete, execute, publish.
- **effect:** none, local write, remote read, remote state change, external communication, or production-data mutation.

Permission decisions consider all three. Multi-resource operations use the most restrictive applicable decision. Deny/hard-deny takes precedence over allow.

## Credentials

- Store only references such as `env:VARIABLE_NAME` or `secret://provider/path`.
- Never store raw tokens, passwords, private keys, or credential values.
- Record minimum required scope and destination.
- Do not pass credentials to subagents unless the runtime explicitly supports scoped secret access and the task requires it.
- Document network/data-egress behavior before configuration.

## Adapter acceptance requirements

Before an adapter can be marked `verified`, it must have:
1. Exact provider, package/revision, and transport.
2. Input/output schemas.
3. Operations with resource/action/effect and risk.
4. Permission profile and approval behavior.
5. Credential reference or explicit no-credential statement.
6. Timeout, retry, idempotency, error semantics.
7. Evidence from a real configured runtime.
8. Tests for denied, allowed, approval-required, malformed input, timeout, and failure behavior.

A schema-valid manifest is not proof that a tool is installed, connected, authorized, or runtime-verified.
