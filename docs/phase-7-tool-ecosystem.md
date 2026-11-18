# Phase 7 — Tool Ecosystem & Integration

**Status:** IN PROGRESS — initial registry contract, deny-by-default manifest, permission matrix, validator, and unit tests authored; latest CI pending  
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

`registry/tools.json` intentionally starts with an empty `tools` array and `default_policy: deny`. The repository has no verified third-party tool adapters registered at this point. Codex-native tools exposed by a particular host session must not be hard-coded as universally available.

Do not populate the registry with hypothetical MCP servers, API endpoints, shell commands, or credentials.

## Source-informed decisions

- **OpenCode:** adapt action/resource/effect permissions, ordered rules, typed schemas, and child-session boundaries; permission UX is not sandboxing.
- **n8n:** adapt typed tool catalogs, action schemas, deferred discovery, lifecycle/error handling, and approval gates; do not copy its runtime/nodes.
- **Anthropic MCP Builder:** adapt naming, focused output, pagination, typed schemas, actionable errors, and operation annotations; annotations are hints, not authorization.
- **Graphify:** optional external adapter candidate; do not vendor or silently install.
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

- Registry schema: authored.
- Registry manifest: initialized empty, deny-by-default.
- Permission matrix: authored.
- Threat model: documented.
- Deterministic validator: authored in `tools/validate_tool_registry.py` and wired into `tools/validate_toolkit.py`.
- Unit tests: added in `tests/test_tool_registry.py` for empty registry, valid declaration, duplicate IDs, raw credentials, runtime evidence, destructive approval, malformed risk types, and secret-path traversal.
- Real adapters: NOT_IMPLEMENTED.
- Credentials: NOT_CONFIGURED.
- Runtime integration: NOT_RUN.
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

Inspect CI for the latest main commit. After it passes, review exact host-exposed integrations and choose one adapter only when its provider, transport, permissions, and runtime availability are evidenced. Keep the registry empty until a real adapter is selected and configured.
