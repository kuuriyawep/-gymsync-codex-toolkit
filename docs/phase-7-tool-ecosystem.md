# Phase 7 — Tool Ecosystem & Integration

**Status:** IN PROGRESS — registry foundation, sanitized Codex host-discovery utility, and MCP adapter review contract authored. Live host verification remains pending.  
**Inputs:** [Phase 6 synthesis](phase-6-final-synthesis.md), [source audit index](../audits/source-reviews/README.md), [source adoption map](source-adoption-map.md)

## Objective

Create one safe, typed, Codex-first inventory for tools that Codex may use. The registry must never invent tools, grant permissions, or imply that a planned adapter is installed.

## Canonical architecture

| Component | Owner | Responsibility |
|---|---|---|
| Tool registry | `registry/tools.json` | Inventory adapter identity, transport, operations, availability, evidence |
| Schema | `schemas/tool-registry.schema.json` | Validate registry and operation metadata |
| Permission policy | `references/tool-permission-matrix.md` | Role access, resource/action/effect rules, approval defaults |
| Adapter implementation | Future `tools/adapters/` or host configuration | Call a real provider through a supported transport |
| Credential references | Runtime/secret manager | Reference secrets without storing values |
| Verification evidence | Tests and immutable evaluation records | Prove configured behavior |
| Runtime discovery | `tools/discover_codex_runtime.py` + snapshot schema | Report local Codex CLI, configured MCP server names, and installed plugin names without exposing config values |
| Adapter governance | `docs/mcp-adapter-contract.md` + review template | Enforce provider identity, transport, authentication, data-egress, per-tool review, lifecycle, and verification gates |

Codex remains the primary coordinator. No external runtime is introduced.

## Tool definition contract

Each future entry must identify:
- Stable ID, display name, purpose, provider and version.
- Transport: Codex-native, MCP, CLI, HTTP API, browser, database, filesystem, or Git.
- Capability tags and typed operations.
- Per-operation risk, idempotency, approval requirement, input schema, output schema.
- Availability: planned, configured, verified, disabled.
- Permission profile ID.
- Credential reference only; never raw secret values.
- Timeout/retry behavior where applicable.
- Evidence status and references.

The schema is a declaration/validation contract, not a runtime authorization mechanism.

## Initial registry state

`registry/tools.json` uses `default_policy: deny`. It now contains one real, pinned, static-reviewed Graphify candidate with `availability: planned`; this does not mean the package is installed, connected, or approved for use. No runtime-verified adapter is registered. Codex-native tools exposed by a particular host session must not be hard-coded as universally available.

Do not populate the registry with hypothetical MCP servers, API endpoints, shell commands, or credentials. Use the runtime discovery procedure and a per-server review before selecting a provider.

## Source-informed decisions

- **OpenCode:** adapt action/resource/effect permissions, ordered rules, typed schemas, and child-session boundaries; permission UX is not sandboxing.
- **n8n:** adapt typed tool catalogs, action schemas, deferred discovery, lifecycle/error handling, and approval gates; do not copy its runtime/nodes.
- **Anthropic MCP Builder:** adapt naming, focused output, pagination, typed schemas, actionable errors, and operation annotations; annotations are hints, not authorization.
- **Current Codex host:** use documented `codex mcp list --json`, `codex plugin list --json`, and active-session `/mcp` inspection; do not confuse configured entries with callable tools.
- **Graphify:** exact v0.9.112 candidate reviewed and registered as `planned`; only eight local graph-query tools are included as candidate operations; the proposed Codex config allowlists those eight. Three GitHub PR tools are excluded. Installation remains blocked by the `project_path` scope issue and user approval; do not vendor or silently install.
- **Superpowers/Matt Pocock/ECC:** reuse existing skill, review, TDD, and verification owners rather than adding duplicate skills.
- **Hermes:** preserve Codex-owned skill/memory lifecycle; no second runtime or memory authority.

Detailed evidence is in `audits/source-reviews/`.

## Threat model

| Threat | Mitigation |
|---|---|
| Metadata mistaken for permission | Registry is non-authoritative; runtime and user approval decide |
| Malicious MCP/plugin | Explicit trust review, least privilege, no automatic installation |
| Prompt injection in tool output | Treat tool output as untrusted data; validate before use |
| Shell/CLI injection | No shell interpolation; future adapters use argument arrays and allowlists |
| Credential leakage | Secret references only; redaction and scoped credentials |
| Destructive/external side effects | Default deny/ask, exact approval, target confirmation, evidence |
| Duplicate/conflicting adapters | Stable IDs and one owner per capability |
| Unavailable/stale tool | Availability/evidence status and safe fallback |
| False runtime claims | Separate static review from runtime verification |

## Current status

- Registry schema: authored with explicit operation-level resource scope, action, effect, risk, idempotency, approval, input schema, and output schema fields.
- Registry manifest: deny-by-default; contains one static-reviewed Graphify candidate marked `planned`.
- Permission matrix: authored.
- Threat model: documented.
- Deterministic validator: authored in `tools/validate_tool_registry.py` and wired into `tools/validate_toolkit.py`; schema enums, required operation fields, and input/output schema structure are checked.
- Unit tests: added in `tests/test_tool_registry.py` for the committed Graphify candidate, valid declarations, duplicate IDs, raw credentials, runtime evidence, destructive approval, malformed risk types, secret-path traversal, resource/action/effect invariants, and malformed input schemas.
- Runtime discovery: `tools/discover_codex_runtime.py` performs read-only CLI/MCP/plugin preflight, emits sanitized JSON, uses no shell, applies timeouts, extracts names only, discards raw command output and has mocked tests in `tests/test_runtime_discovery.py`.
- Runtime snapshot schema: `schemas/runtime-capability-snapshot.schema.json`.
- MCP adapter lifecycle and security contract: `docs/mcp-adapter-contract.md`.
- Per-server evidence template: `templates/mcp-adapter-review.md`.
- Real adapters: NOT_IMPLEMENTED.
- Graphify: STATIC_REVIEWED / PLANNED only; not installed, configured, session-loaded, or runtime-verified.
- Credentials: NOT_CONFIGURED.
- Runtime integration: NOT_RUN — utility must be run on the user's actual Codex host.
- Active-session tool inventory: NOT_CAPTURED — requires `/mcp` inspection in a live session.
- Codex behavior: NOT_RUN.

## Acceptance criteria

Phase 7 cannot close until:
1. Registry and definition schema validate.
2. Duplicate IDs and malformed operations are rejected.
3. A tool cannot be marked runtime-verified without evidence references.
4. Raw credential values are rejected; only secret references are permitted.
5. Role permission matrix is explicit and default deny.
6. Hard-deny and approval precedence are documented and tested.
7. Adapter contracts cover schemas, errors, timeouts, retries, idempotency, and fallback.
8. No adapter is described as configured/verified without runtime evidence.
9. Current CI passes on latest main.
10. User approves package/service installation and external integrations.

## Next work

Run `python tools/discover_codex_runtime.py` on the actual Codex host, then inspect `/mcp` in the active session. For Graphify, first resolve the `project_path` override scope through an OS/container sandbox or a tested pinned-path proxy. Only then request approval for the pinned package install and test. Keep Graphify marked `planned` until the user approves setup and live evidence exists.
