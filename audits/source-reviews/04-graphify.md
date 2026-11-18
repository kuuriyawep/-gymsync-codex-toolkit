# Source Audit — Graphify

- **Source:** [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify)
- **Audited branch/revision:** `v8`, commit `340268a70a83588d6b3c6de1fffb05326350ef1d`
- **Package noted:** `graphifyy 0.9.112`
- **Audit date:** 2026-11-18
- **License noted:** Apache-2.0 with legacy MIT portions and NOTICE requirements; inspect exact files before reuse.
- **Evidence status:** Source/documentation review; no install or runtime tests.

## Findings

Graphify provides a persistent repository knowledge graph:
- Local tree-sitter AST extraction for approximately 40 languages.
- Graph outputs including `graph.json`, `GRAPH_REPORT.md`, and HTML visualization.
- Queries for `query`, `path`, `explain`, and `affected`.
- Cross-file and cross-document relationships.
- Provenance labels `EXTRACTED`, `INFERRED`, and `AMBIGUOUS`, with confidence.
- Content-hash incremental cache/update/watch.
- Optional local MCP stdio server and multi-repository graph merge.
- Graph health and shrink guards.

Security/privacy:
- Advisory GHSA-pcc4-rvhr-2pr8 affected versions below 0.9.70; the audited v8 revision was 0.9.112 and included a mitigation in the Fortran extractor.
- Code-only indexing is local; semantic extraction of documents/media can send content to the configured model/provider.
- Documentation says query logging is on by default, while the audited implementation/tests indicate opt-in logging by default OFF. Treat this as a documentation inconsistency and verify the installed version.
- Graph data is an index/relationship view, not an authority for project decisions.

## Adoption decision

**ADOPT as an optional external tool; ADAPT a small toolkit-owned adapter; do not vendor the Graphify project.**

Graphify complements, but does not replace:
- Version-controlled Markdown project records.
- Mnemoverse durable decision memory.
- Current-source inspection.

## Phase mapping

- Phase 7: optional CLI/MCP adapter, version check, graph freshness, scoped query, provenance, fallback to file search.
- Phase 9: query existing graph first; refresh only when stale/needed; avoid expensive rebuilds for one-off questions.
- Phase 10: query accuracy, ambiguity, stale detection, provenance, cache-update and graph-integrity tests.
- Phase 11: actual Codex skill/CLI/MCP handoff validation.

No Graphify install or integration is performed by this audit.
