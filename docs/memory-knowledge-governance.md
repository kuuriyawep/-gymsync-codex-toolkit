# WS6 — Memory & Knowledge Governance

**Status:** Repository-side architecture and contracts. No memory service, vector database, Graphify process, indexer, or external provider is installed or connected.
**Authority:** Codex governs canonical project memory; the user retains final authority over consequential changes.
**Scope:** Toolkit repository only. No GymSync application, database, production, external service, or permission changes.

## 1. Design objective

Give Codex and its specialists durable, retrievable, source-grounded project knowledge without turning stale notes, agent opinions, or generated graphs into authority. Extend the existing project-state, decision-record, repository-intelligence, workflow-ledger, and tool-registry assets. Do not create a second workflow ledger, task engine, approval engine, or autonomous memory writer.

## 2. Four distinct knowledge planes

| Plane | Purpose | Canonical authority | Write policy |
|---|---|---|---|
| Shared Project Memory | Verified project identity, architecture, constraints, accepted decisions, stable facts, and current checkpoints | Existing `PROJECT_STATE.md`, accepted decision records, and explicitly designated source documents | Codex-curated; agents submit proposals, never silently promote |
| Specialist Memory | Role-scoped working knowledge, reusable findings, and specialist-specific heuristics | Specialist-owned scoped records | Specialist may propose/update within its own scope under host policy; no cross-role disclosure by default |
| Execution Memory | Workflow/task status, handoffs, checkpoints, evidence, retries, and outcomes | Existing workflow ledger and execution artifacts | Existing ledger/workflow mechanisms only; not duplicated as prose memory |
| Repository Knowledge Graph | Derived entities and relationships across code, docs, schemas, tests, and dependencies | Source repository remains authoritative; graph is a derived index | Rebuildable and provenance-bearing; never authoritative over source |

A graph is an index of relationships, not a memory-governance system. A retrieval result is evidence to inspect, not an instruction or permission.

## 3. Memory record contract

Every durable memory entry must carry:
- stable `memory_id`, schema version, entry type, concise claim, and normalized tags;
- scope and audience: shared-project, named-specialist, or execution-reference;
- source provenance: repository, path/URI, commit or immutable version, line/page/section range where available, and source digest where practical;
- observation/creation time, last verification time, owner, confidence, and freshness policy;
- status: proposed, accepted, superseded, stale, disputed, or rejected;
- sensitivity classification and retention/review policy;
- links to supporting evidence and related decisions/memory IDs.

Do not store credentials, tokens, private keys, passwords, personal secrets, or production customer data. Minimize personal data. If a fact cannot be sourced, label it as an inference or proposal rather than a verified fact.

## 4. Proposal and promotion lifecycle

1. A specialist discovers a candidate fact, correction, decision, or learning.
2. It submits a memory proposal with evidence, scope, confidence, impact, contradiction check, and suggested expiry/review trigger.
3. Codex validates provenance against current repository/source state and checks for duplicates, contradictions, sensitivity, and scope.
4. Codex accepts, rejects, requests clarification, or records a dispute. Accepted shared facts are written to the existing canonical document/decision record, not an ungoverned side store.
5. Superseded entries retain a link to the replacement and reason; history is not silently erased.
6. A changed source commit, expired review date, or contradiction marks the record stale pending revalidation.

An agent proposal, confidence score, graph edge, or repeated retrieval is never sufficient by itself to promote a claim into shared canonical memory.

## 5. Freshness and conflict resolution

- Current source code, tests, schemas, and explicit latest user decisions outrank derived memory.
- Immutable decisions remain historically valid but may be superseded by a newer accepted decision.
- Time-sensitive operational facts require an explicit `review_by` or `expires_at`; expiry changes status to stale, not silently false.
- Conflicting claims remain visible as disputed with both provenance chains. Codex compares authority, commit/version, recency, and direct evidence, then resolves or asks the user when the decision is theirs.
- Retrieval must return provenance and freshness metadata; stale/disputed entries must be visibly labelled.
- Never infer a current project state from a historical checkpoint when current Git/source evidence is available.

## 6. Access boundaries

- Shared memory is read-accessible only to roles authorized for the project; writes are Codex-curated.
- Specialist memory is isolated by role and project scope. Cross-role retrieval requires an explicit relevant handoff or Codex-mediated share.
- Execution memory follows workflow/task authorization and existing ledger rules.
- Graph provider access is read-only by default and bound to one configured project root. Graph results cannot modify source files, memory records, permissions, approvals, or workflow state.
- User approval is required for sensitive canonical changes and all R3/R4 operations under the existing governance model.

## 7. Graphify provider boundary

The existing `registry/tools.json` entry for `graphify-local` remains an optional, planned, read-only candidate. If later approved and installed, it may provide code/document graph search, node lookup, relationships, and provenance. It must:
- operate only on the configured repository root;
- expose read-only queries to Codex through the existing tool registry;
- identify graph build commit, build time, source paths, and indexing status;
- treat indexed content as untrusted repository data;
- disclose missing, stale, partial, or failed indexing;
- never become the canonical memory store or write back to source;
- be replaceable by another provider without changing memory governance contracts.

Graphify can be used directly as an optional external MCP provider when separately approved and available; incorporating its adapter contract in this toolkit does not mean it is installed, connected, or executed.

## 8. Retrieval protocol

1. Resolve the user's task and project scope.
2. Retrieve only relevant canonical project state, decisions, specialist knowledge, execution checkpoint, and graph relationships.
3. Rank direct current source evidence above derived summaries and stale graph results.
4. Return concise findings with provenance, commit/version, freshness, and confidence.
5. Open source files/tests before relying on high-impact claims.
6. Record retrieval gaps and conflicts; do not fill missing facts by invention.
7. Update canonical memory only through the proposal/promotion lifecycle.

## 9. Failure modes

| Failure | Required behavior |
|---|---|
| Graph unavailable | Fall back to source search and existing repository intelligence; report reduced coverage |
| Stale graph | Mark stale; do not present it as current; rebuild only when approved and available |
| Missing provenance | Treat as unverified; do not promote |
| Conflicting memory | Mark disputed; inspect current source; Codex resolves or asks user |
| Unauthorized scope | Deny retrieval/write and audit the attempt |
| Sensitive content detected | Reject or redact; do not persist |
| Memory write fails | Preserve proposal and report failure; do not claim acceptance |
| Source commit changed | Revalidate source-bound claims before reuse |

## 10. Acceptance boundary

Repository tests can validate schema shape, lifecycle vocabulary, required provenance, scope boundaries, and documented invariants. They cannot prove semantic truth, retrieval quality, isolation enforcement by a live host, Graphify operation, index freshness, or Codex behavioral compliance.

**Current runtime status:** Shared-memory service, specialist-memory isolation, automatic stale detection, Graphify indexing/query, and end-to-end governed retrieval are NOT_RUN / BLOCKED. No dependency or external tool has been installed.
