# Source Audit — Hermes Agent

- **Source:** [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- **Audit provenance:** Earlier project review, carried forward on 2026-11-18; no fresh audit performed.
- **Evidence status:** PARTIAL — the recovered project record preserves selected capability decisions but not a complete source snapshot.
- **Revision:** Exact commit/release was not preserved in the recovered record.
- **Reuse rule:** Adapt concepts; do not import the runtime.

## Recovered findings and prior decisions

The prior toolkit planning record selected Hermes-derived ideas around:
- Memory lifecycle and durable context handling.
- Skill lifecycle, metadata, discovery, and loading.
- Workflow/orchestration patterns.

The earlier decision was to incorporate useful memory and skill-lifecycle patterns into the Codex-first toolkit, not to replace Codex with Hermes or make Hermes an independent coordinator.

Existing toolkit foundations that overlap these areas include:
- `.agents/skills/project-intelligence/`
- `.agents/skills/skill-authoring-and-evaluation/`
- `docs/project-intelligence.md`
- `docs/memory-maintenance.md`
- `templates/project-memory/`
- `AGENTS.md` and `workflows/registry.md`

These existing artifacts are the toolkit's own implementations. The recovered record does not prove verbatim code reuse from Hermes.

## Adoption decision

**ADAPT memory and skill-lifecycle patterns into the existing toolkit.**

Preserve:
- Codex as the primary coordinator.
- Explicit provenance and freshness for project knowledge.
- Skill discovery/loading as a governed lifecycle.
- User approval and permission boundaries.
- Project-specific memory separation.

Reject:
- Replacing the toolkit's Codex-native control plane with the Hermes runtime.
- Treating agent memory as automatically trusted or as a substitute for current repository evidence.
- Duplicating existing project-intelligence and skill-authoring systems.

## Limitations and next handling

The recovered record does not contain a revision-pinned source inventory, exact source paths, detailed security review, or file-level license assessment. Do not claim those items were verified. No repeat audit was run because the user explicitly required that already-completed Hermes work not be repeated. Any later code reuse requires a narrowly scoped source/license review.

No Hermes runtime, package, or service is installed by this record.
