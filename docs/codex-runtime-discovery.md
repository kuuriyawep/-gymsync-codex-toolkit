# Codex Runtime Discovery

**Status:** Phase 7 implementation — read-only preflight utility  
**Purpose:** Distinguish installed/configured capabilities from tools actually available to an active Codex session.

## Verified platform facts

The current Codex documentation describes:
- `codex mcp list --json` for listing configured MCP servers.
- `codex plugin list --json` for listing installed plugins.
- `codex mcp add` for registering a stdio command or Streamable HTTP endpoint.
- `codex mcp login` for OAuth-enabled HTTP servers.
- `/mcp` in the TUI for viewing active MCP servers.
- MCP configuration in `~/.codex/config.toml`; trusted projects can also use `.codex/config.toml`.

Sources (checked 2026-11-18):
- [Codex CLI command reference](https://learn.chatgpt.com/docs/cli/reference)
- [Codex MCP configuration guide](https://learn.chatgpt.com/docs/extend/mcp)
- [Codex configuration basics](https://learn.chatgpt.com/docs/config-file/config-basic)

The removed `codex mcp-server` host command is not the same as the MCP client feature. Codex continues to support connecting to external MCP servers. Do not build against the removed host command.

## Utility

Run from a trusted Codex host:

```bash
python tools/discover_codex_runtime.py
```

Optionally save a sanitized snapshot:

```bash
python tools/discover_codex_runtime.py --output runtime-capabilities.json
```

The script:
1. Checks whether `codex` is on PATH.
2. Reads only `codex --version`.
3. Calls `codex mcp list --json` and extracts server names only.
4. Calls `codex plugin list --json` and extracts installed plugin names only.
5. Reports exit status, parse status, and names only; raw command output and derived hashes are not retained.

It does **not** read `config.toml`, inspect environment values, print URLs/commands, expose secrets, install packages, authenticate, start servers, or call tools. It uses argument arrays, never a shell, and applies a 15-second timeout per command.

## Evidence boundaries

| Observation | What it proves | What it does not prove |
|---|---|---|
| Codex executable found | CLI is on PATH | Correct account, permissions, or successful use |
| `codex mcp list` succeeds | Configured server entries can be listed | Server process starts, authentication works, or tools respond |
| Server name appears | A server is configured | Tool inventory, trust, or operation-level access |
| Plugin appears in installed list | Plugin is installed in local Codex config | Its MCP servers are enabled or callable |
| `/mcp` shows a server in active session | Session has loaded/connected that server | Every operation is safe or authorized |
| Safe representative tool call succeeds | That exact operation worked in that environment at that time | Other tools/operations are verified |

The snapshot intentionally sets `active_session_tool_inventory` to `not-captured`. An operator must inspect `/mcp` in the actual Codex session and record the tool names and evidence separately. Never infer active tools from a configured server list.

## Security constraints

- Never paste `config.toml`, bearer tokens, OAuth tokens, API keys, environment values, or raw command output into the repository.
- Record only provider/server identifiers, transport, approved capabilities, operation schemas, and secret references.
- A tool's MCP annotations are descriptive hints, not permission grants.
- Start with read-only tools and the smallest required allowlist.
- Require explicit approval for writes, destructive actions, external communication, and production data changes.
- Re-check tool definitions after server updates; treat changed tool descriptions/schemas as a trust-boundary change.
- A failed or unknown discovery result remains unknown; it is not an empty inventory.

## Phase 7 handoff

1. Run the preflight on the user's actual Codex machine.
2. Inspect the active session using `/mcp`.
3. Select one high-value, read-only integration.
4. Review its official provider, transport, authentication, scopes, data egress, and operation schemas.
5. Add the adapter as `configured` only after a deliberate setup; mark it `verified` only after a real, safe call and evidence capture.
