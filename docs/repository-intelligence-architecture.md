# Universal Repository Intelligence Architecture

**Status:** Design approved for implementation planning; no Graphify installation or runtime integration has been performed.  
**Design decision:** One reusable toolkit-owned intelligence layer, with a separate project configuration and graph for each target repository. GymSync is the first intended target, but its graph/configuration belongs inside the GymSync repository—not inside this universal toolkit.

## 1. Problem

Large repositories force Codex to repeatedly rediscover file roles, entry points, dependencies, ownership, and change impact. Markdown project memory helps continuity, but the current implementation is a retrieval discipline—not an automatically generated dependency graph or repository index.

The intelligence layer should reduce unnecessary file reads while keeping current source and tests authoritative.

## 2. Architecture

```text
Universal Codex Toolkit
  ├── Repository Intelligence skill and workflow
  ├── Graph adapter contract
  ├── Index/graph validation and freshness checks
  ├── File classification and impact-analysis rules
  └── Project configuration template
             |
             | configured project root (strictly bound)
             v
Target Repository A                 Target Repository B
  ├── own config                      ├── own config
  ├── own generated graph             ├── own generated graph
  ├── own project memory              ├── own project memory
  └── own source/tests                └── own source/tests

GymSync is Target Repository A. Its graph and configuration must not be committed into this toolkit or shared with another target project.
```

The shared layer is universal. Project-specific facts, graph nodes, file paths, module names, and repository memory stay with their respective target repository.

## 3. Graph and metadata model

The graph should distinguish at least three relationship families:

- **Runtime dependency:** imports, calls, routes, events, data flow, configuration, and execution relationships.
- **Technical dependency:** build/test dependencies, schema ownership, generated mirrors, CI consumers, and validation contracts.
- **Knowledge relationship:** documentation references, decision records, architecture ownership, historical evidence, and task-to-source mappings.

Each indexed file/node should expose, where applicable:

- normalized repository-relative path and stable node identifier;
- file role and classification;
- canonical / mirror / generated / historical status;
- direct dependency and consumer edges;
- language and artifact type;
- source provenance: extracted, inferred, or ambiguous;
- confidence and evidence location;
- content hash and last indexed commit;
- last verified timestamp and indexer version.

Do not collapse inferred relationships into facts. Preserve provenance and ambiguity explicitly.

## 4. Query contract for Codex

The adapter should support bounded operations such as:

1. `search(question, filters, token_budget)` — find likely relevant nodes.
2. `lookup(path_or_id)` — inspect one node and metadata.
3. `dependencies(path_or_id, direction, depth)` — trace direct or transitive dependencies.
4. `affected(path_or_id)` — list likely impacted consumers/tests/docs.
5. `explain(path_or_id)` — return the relationship path and evidence.
6. `status()` — report index version, source commit, freshness, excluded paths, and errors.
7. `refresh(scope)` — update a bounded scope only when explicitly allowed by the configured workflow.

Every result must include source paths and provenance. Codex must open the actual source file before making a consequential claim or edit.

## 5. Freshness and fallback

- Store the source commit and content hashes represented by the graph.
- Detect dirty/uncommitted changes and graph/source revision mismatch.
- Refresh only the affected scope when safe; do not rebuild the whole graph for every question.
- Mark stale or partial indexes clearly; never silently present them as current.
- If the graph is unavailable, stale, ambiguous, or fails validation, fall back to normal repository search and direct source inspection.
- A graph is an index, not a replacement for source code, tests, schemas, configuration, or user decisions.

## 6. Graphify adoption boundary

The existing review of Graphify v0.9.112 recommends an optional external tool plus a small toolkit-owned adapter—not copying the full Graphify repository into this toolkit.

Potentially reusable capabilities include local AST extraction, cross-file relationship mapping, graph queries, incremental content-hash refresh, provenance, and affected-path analysis. Before adoption, verify the exact version, license/NOTICE obligations, runtime behavior, supported languages, graph isolation, query logging, and data-egress settings.

Rules:

- Do not vendor-copy Graphify source into the toolkit.
- Keep Graphify as an optional adapter/provider, not a mandatory toolkit dependency.
- Bind each Graphify process to exactly one configured project root; never accept arbitrary caller-supplied roots.
- Prefer local code-only extraction. Any semantic/model-backed extraction or network egress requires explicit review and user approval.
- Do not store source snippets, secrets, production data, or private project content in shared logs or cross-project graphs.
- Keep the adapter contract provider-neutral so another graph engine can replace Graphify later.

## 7. GymSync first-target plan

GymSync is the first target for a project-specific graph profile. When separately authorized, its own repository should contain its project identity, include/exclude policy, graph output location, sensitive-path exclusions, language settings, and source commit/freshness metadata.

Do not create the GymSync graph in this toolkit. Do not read or index GymSync source as part of the current toolkit documentation change. The project-specific configuration and graph build are a separate task against the GymSync repository, requiring its own approval and validation.

## 8. Implementation sequence

1. Define the provider-neutral adapter and project-config schema.
2. Implement file classification and graph freshness contracts without installing a provider.
3. Add deterministic tests for project-root isolation, stale index detection, provenance, bounded query results, and safe fallback.
4. Evaluate Graphify as an optional provider in a disposable non-production repository.
5. Only after approval, configure a target project and generate its isolated graph.
6. Test Codex retrieval and change-impact accuracy in a trusted Codex runtime; do not claim runtime acceptance from static CI.

## 9. Acceptance criteria

- A query for a task returns a small, relevant set of paths rather than the whole repository.
- Every result carries path/provenance evidence and a freshness status.
- Project A cannot read, merge, or query Project B's graph through the adapter.
- Stale or missing graphs cause an explicit fallback, not false confidence.
- Codex verifies claims against source and tests.
- No mandatory Graphify dependency, automatic network egress, or autonomous writes are introduced.
