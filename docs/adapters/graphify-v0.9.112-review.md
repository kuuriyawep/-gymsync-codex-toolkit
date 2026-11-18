# Graphify MCP Adapter Review — v0.9.112

**Decision:** REVIEWED CANDIDATE — NOT INSTALLED; NOT APPROVED FOR RUNTIME USE  
**Review date:** 2026-11-18  
**Source repository:** https://github.com/Graphify-Labs/graphify  
**Reviewed revision:** `v0.9.112`, commit `340268a70a83588d6b3c6de1fffb05326350ef1d`  
**PyPI package:** `graphifyy==0.9.112`  
**Toolkit registry:** `graphify-local`, availability `planned`

## 1. Identity and provenance

- Official publisher/repository: Graphify Labs / Graphify-Labs/graphify.
- Release: v0.9.112, published 2026-11-17.
- Python: `>=3.11,<3.15`.
- Package: `graphifyy`.
- CLI entry points: `graphify`, `graphify-mcp`.
- MCP extra: `mcp>=1,<3`, `starlette>=1.3.1,<2`, `anyio>=4.14.2`.
- Release wheel: 2.0 MB; source archive: 3.5 MB.
- PyPI Trusted Publishing provenance identifies the GitHub Actions publisher, repository, workflow, and exact source commit.
- The Git tag object itself is unsigned. Prefer the PyPI attestation and exact commit provenance over trusting the tag signature.

Wheel SHA-256:
`ad6a9152fb6d9c5d85a77ffcaf29e18c5634a7d5ca474edb218cbc68b062241d`

Source archive SHA-256:
`67aad04f70aa3afc9ff6961f82d7cca5b04fb6b9446a3cddcb7b16483fbdb59b`

Evidence:
- [Release v0.9.112](https://github.com/Graphify-Labs/graphify/releases/tag/v0.9.112)
- [Pinned pyproject.toml](https://github.com/Graphify-Labs/graphify/blob/340268a70a83588d6b3c6de1fffb05326350ef1d/pyproject.toml)
- [PyPI package and provenance](https://pypi.org/project/graphifyy/0.9.112/)

## 2. License review

Package metadata declares Apache-2.0 and explicitly ships:
- `LICENSE`
- `LICENSE-MIT`
- `NOTICE`

The NOTICE says portions contributed before relicensing remain available under MIT terms. Do not copy source files into this toolkit without file-level license and notice review. Installing the package as an external dependency is distinct from vendoring its code.

## 3. Security and data handling

### Known advisory

GHSA-pcc4-rvhr-2pr8 affected versions below 0.9.70 and concerns a Fortran preprocessor include-path bypass that could read files outside an untrusted source tree. The advisory lists 0.9.70 as fixed; reviewed v0.9.112 is above that fixed version.

- [GitHub security advisory](https://github.com/Graphify-Labs/graphify/security/advisories)
- [OSV advisory details](https://osv.dev/vulnerability/GHSA-pcc4-rvhr-2pr8)

This confirms the known advisory's fixed-version threshold; it is not a claim that the package has no other vulnerabilities.

### Data egress

- AST/code extraction is described as local and deterministic.
- Semantic extraction may send selected source/document/media content to the configured model/backend.
- URL ingestion makes outbound requests only for user-supplied URLs.
- HTTP MCP is opt-in; this candidate uses STDIO only.
- Query logging is opt-in in the reviewed `graphify/querylog.py`. Set `GRAPHIFY_QUERY_LOG_DISABLE=1` in the MCP server environment as a defense-in-depth override.
- Response-body logging requires a separate environment flag; do not enable it for proprietary source.

### Local path scope

Graphify's MCP tools accept an optional `project_path` argument. The server validates graph paths under a `graphify-out` directory, but the server process can still be asked to select another project graph. This is not a strict single-repository sandbox.

Before runtime approval, either:
1. Run the server in an OS/container sandbox whose readable roots are restricted to the intended project; or
2. Build and test a narrow local proxy that pins one graph path and rejects `project_path` overrides.

Do not treat prompt instructions or registry metadata as a security boundary.

## 4. MCP transport and tool inventory

The server supports STDIO and Streamable HTTP. Candidate transport is **STDIO only**. Do not expose HTTP or bind a network listener for this toolkit integration.

The source defines 11 tools:

| Tool | Candidate decision | Reason |
|---|---|---|
| `query_graph` | Allowlist candidate | Local graph search |
| `get_node` | Allowlist candidate | Local node lookup |
| `get_section` | Allowlist candidate | Reads source section/page referenced by graph |
| `get_neighbors` | Allowlist candidate | Local relationship lookup |
| `get_community` | Allowlist candidate | Local community lookup |
| `god_nodes` | Allowlist candidate | Local graph ranking |
| `graph_stats` | Allowlist candidate | Local statistics |
| `shortest_path` | Allowlist candidate | Local graph path query |
| `list_prs` | Exclude | Calls GitHub CLI and accesses remote PR metadata |
| `get_pr_impact` | Exclude | Calls GitHub CLI and fetches PR files/metadata |
| `triage_prs` | Exclude | Calls GitHub CLI and fetches multiple PRs/files |

The eight candidate tools are read-only graph queries. The three PR tools are excluded from the proposed Codex allowlist; they are not required for repository knowledge retrieval.

The MCP server returns text content blocks. The Graphify server source does not provide a richer per-tool output schema; the toolkit registry records the MCP text-result envelope and exact input schemas as reviewed from the pinned source.

## 5. Proposed Codex policy (not executed)

After explicit installation approval, the proposed server command is:

```bash
uv tool install 'graphifyy[mcp]==0.9.112'
codex mcp add graphify --env GRAPHIFY_QUERY_LOG_DISABLE=1 -- graphify-mcp --graph /ABSOLUTE/PROJECT/PATH/graphify-out/graph.json
```

Then configure the server with a narrow tool allowlist in the user's local `~/.codex/config.toml`:

```toml
[mcp_servers.graphify]
enabled = true
enabled_tools = [
  "query_graph",
  "get_node",
  "get_section",
  "get_neighbors",
  "get_community",
  "god_nodes",
  "graph_stats",
  "shortest_path",
]
default_tools_approval_mode = "prompt"
startup_timeout_sec = 20
tool_timeout_sec = 60
```

This configuration is an example only. Do not commit local paths, secrets, or user-specific `config.toml` content to this repository. The optional `project_path` argument remains a scope concern until the host process is isolated or a tested pinned-path proxy is used.

## 6. Toolkit integration boundary

Graphify complements but does not replace:
- Version-controlled Markdown project records.
- The toolkit's Project Intelligence skill.
- Mnemoverse durable decision/context memory.
- Current source inspection and tests.

Recommended use after approval:
- Build/update the graph only when needed.
- Query graph relationships for navigation and impact discovery.
- Verify important findings against source files and tests.
- Treat graph provenance/confidence labels as evidence metadata, not truth.
- Fall back to direct file search when the graph is missing or stale.

## 7. Verification checklist

- [x] Exact release and source commit identified.
- [x] Package metadata and Python compatibility reviewed.
- [x] Apache-2.0 / legacy MIT / NOTICE reviewed.
- [x] Known GHSA fixed-version threshold checked.
- [x] PyPI Trusted Publishing provenance and artifact hashes recorded.
- [x] MCP tool inventory inspected from pinned source.
- [x] Query logging default and disable override inspected.
- [x] Three GitHub PR tools identified for exclusion.
- [ ] User approves package installation.
- [ ] Package installed in a disposable/trusted environment.
- [ ] Graph built from the intended project only.
- [ ] Server starts over STDIO.
- [ ] Active Codex `/mcp` session exposes only the approved tools.
- [ ] `project_path` scope is constrained by OS sandbox or tested proxy.
- [ ] Representative query, timeout, invalid input, and stale graph behavior tested.

**Final status:** STATIC REVIEW PASS WITH RUNTIME BLOCKERS. The candidate is suitable for a controlled read-only proof of concept only after the path-scope issue is resolved and the user approves installation. It is not installed, connected, or runtime-verified.
