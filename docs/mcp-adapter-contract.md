# MCP Adapter Contract

**Status:** Phase 7 design contract — no server is installed by this document.  
**Applies to:** MCP servers connected to Codex CLI, IDE extension, or ChatGPT desktop app.

## 1. Adapter lifecycle

`candidate → reviewed → configured → session-loaded → verified → monitored → disabled/removed`

These are evidence states, not automatic permissions:
- **candidate:** provider/use-case identified; no trust decision.
- **reviewed:** provider, source, transport, authentication, scopes, data egress, tool schemas, and risks inspected.
- **configured:** user deliberately added the server to the Codex host.
- **session-loaded:** active Codex session reports the server under `/mcp`.
- **verified:** one or more explicitly approved representative operations passed with evidence.
- **monitored:** tool definitions, provider version, auth, health, and failures are rechecked.
- **disabled/removed:** access revoked; stale registry entries and credentials are not silently retained.

The registry's `availability` field remains `planned`, `configured`, `verified`, or `disabled`. Record intermediate lifecycle states in review/evidence records; do not overload the registry enum.

## 2. Required adapter identity

Every reviewed adapter must record:
- Provider and official documentation URL.
- Official server repository or publisher identity.
- Package name and pinned version/revision for stdio; canonical HTTPS endpoint for Streamable HTTP.
- Transport: `stdio` or `streamable-http`.
- Runtime/host compatibility and minimum Codex version if known.
- Data classification and destination.
- Authentication type and minimum scopes; credential values are never recorded.
- Owner, review date, next review trigger, and removal procedure.

A third-party proxy is not an official provider endpoint. Treat it as a separate provider with its own trust and data-processing review.

## 3. Connection configuration

Codex's supported MCP client configuration is host-level:
- User configuration: `~/.codex/config.toml`.
- Trusted project configuration: `.codex/config.toml`.
- CLI management: `codex mcp add/list/get/login/logout/remove`.
- Active session inspection: `/mcp`.

Supported transports:
- **STDIO:** local process, command, arguments, optional environment variables and working directory.
- **Streamable HTTP:** HTTPS endpoint; authentication may use bearer token environment references or supported OAuth flows.

Never place secrets in the toolkit repository, `AGENTS.md`, plugin archives, shell history, screenshots, or task prompts. The setup operator enters/authenticates secrets locally using the host's supported mechanism.

Project-scoped configuration is loaded only for trusted projects. Prefer user-level configuration for personal tools and project-level configuration only when the server is intentionally project-specific.

## 4. Tool inventory and schema review

At discovery time, capture:
- Exact server name and provider identity.
- Tool names and descriptions exactly as exposed.
- Input schema and output schema, if provided.
- Pagination behavior and cursors.
- Annotations such as read-only/destructive hints.
- Whether the server advertises tool-list change notifications.
- The time and server version/revision at which the inventory was captured.

Treat all server-provided descriptions, schemas, annotations, instructions, resources, and outputs as untrusted data. Annotations are hints, not authorization. A server's `instructions` field is context, not higher-priority policy.

Review every tool individually. Map each operation to:
- Resource(s) and permitted scope.
- Action: read, list, search, create, update, delete, execute, publish.
- Effect: none, local write, remote state change, external communication, or production/data mutation.
- Risk, idempotency, approval, rate limits, and rollback/recovery.
- Input constraints, output limits, and sensitive-data handling.

A tool is not approved merely because it appears in `tools/list`.

## 5. Permission policy

- Start with the smallest read-only tool allowlist that supports one real workflow.
- Keep destructive and external actions disabled or approval-gated.
- Require approval for writes unless the exact low-risk write scope is explicitly approved.
- Never let a child agent or MCP server grant itself additional permissions.
- The host sandbox, approval mode, and user authorization remain authoritative.
- Re-review after tool description/schema changes, provider ownership changes, endpoint changes, package upgrades, or authentication-scope changes.

## 6. Reliability contract

Each adapter review must specify:
- Connect and call timeout.
- Maximum retry attempts and retryable error classes.
- Retry policy for non-idempotent calls (default: no automatic retry).
- Idempotency key support where available.
- Pagination and maximum result size.
- Rate-limit handling and backoff.
- Error normalization: unavailable, unauthorized, approval-required, invalid-input, timeout, rate-limited, server-error, protocol-error.
- Cancellation behavior and partial-result semantics.
- Health-check behavior that does not mutate state.

Never automatically retry a destructive, payment, messaging, publishing, or other non-idempotent operation.

## 7. Verification gates

Before `configured`:
- Complete provider trust, license, security, data-egress, and scope review.
- User explicitly approves the exact server and transport.
- Confirm local/remote dependencies and version pinning.

Before `verified`:
- Confirm the server is visible in the active Codex session.
- Capture the exposed tool inventory.
- Test a representative read-only call with non-sensitive input.
- Test invalid input and expected authorization failure where safe.
- Verify output is bounded and does not leak secrets.
- Record host/Codex version, server version, tool name, sanitized inputs, outcome, and timestamp.

Write or destructive operation tests require separate explicit approval and a safe disposable target.

## 8. Disable and incident response

Immediately disable or remove a server if:
- Provider identity or endpoint changes unexpectedly.
- Tool definitions expand or change without review.
- Credentials may be exposed.
- Unexpected external writes or data egress occur.
- The server becomes compromised, unmaintained, or unsupported.

Revoke OAuth/API credentials at the provider, remove host configuration, restart affected Codex sessions, and preserve sanitized incident evidence. Do not leave a stale registry entry marked verified.

## 9. Official Codex references

- [MCP configuration and supported transports](https://learn.chatgpt.com/docs/extend/mcp)
- [Codex CLI MCP commands](https://learn.chatgpt.com/docs/cli/reference)
- [Codex configuration basics](https://learn.chatgpt.com/docs/config-file/config-basic)
