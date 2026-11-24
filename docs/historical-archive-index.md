# Historical Documentation and Audit Index

This page separates the toolkit's construction history from the procedures Codex uses when working in a target repository.

**Loading policy:** Historical reports are on demand. Do not load them during ordinary task startup. Use them only when a task requires historical decisions, provenance, an audit trail, or a specific implementation rationale.

## Historical phase reports

| Area | Location | When to read |
|---|---|---|
| Phase 6 synthesis and source adoption | `docs/phase-6-*.md`, `docs/source-adoption-map.md`, `docs/source-attribution.md` | Historical source selection or rationale |
| Phase 7 integration and tool ecosystem | `docs/phase-7-*.md` | Tool registry or integration history |
| Phase 8 skill and agent audits | `docs/phase-8-*.md` | Skill/agent audit history |
| Phase 9 stateful workflow engine | `docs/phase-9-stateful-workflow-execution.md` | Workflow ledger design or migration |
| Phase 10 evaluation reliability | `docs/phase-10-evaluation-reliability.md` | Evaluation history and prior reliability decisions |
| Phase 11 execution and final audit | `docs/phase-11-execution-plan.md`, `docs/phase-11-final-audit-report.md`, `docs/phase-11-baseline.md` | Audit evidence and repository-side closeout |
| Phase 11 Codex runtime acceptance | `docs/phase-11-codex-runtime-acceptance.md` | Only during a trusted Codex runtime acceptance session |

## External source reviews

- Index: [External Source Audit Index](../audits/source-reviews/README.md)
- Graphify review: [Graphify adapter review](adapters/graphify-v0.9.112-review.md)
- These are source-review records, not proof that any reviewed tool is installed or running.

## Current operational sources (not historical)

- [Toolkit Quickstart](quickstart.md)
- [Repository File Classification](repository-file-classification.md)
- [Universal Repository Intelligence Architecture](repository-intelligence-architecture.md)
- [Project Intelligence retrieval protocol](project-intelligence.md)
- [Workflow registry](../workflows/registry.md)

## Preservation rule

Do not delete or move historical reports merely to make the repository appear smaller. Reduce routine context loading by using this index and the documented loading levels. Before any later archival move, verify inbound links, scripts, validator manifests, CI references, and historical evidence requirements.
