# Source Audit — Matt Pocock Skills

- **Source:** [mattpocock/skills](https://github.com/mattpocock/skills)
- **Audited revision:** `main`, commit `5863806dd4e15c63174bee4e7515a4256792ecfa`
- **Date:** 2026-11-12
- **Plugin version:** 1.3.2
- **License noted:** MIT
- **Inventory noted:** 27 promoted skills
- **Evidence status:** Read-only source review; no Codex install/runtime test.

## Findings

Selected unique patterns:
- Two-axis independent Standards/Spec review.
- User-vs-model skill invocation metadata.
- Concise handoff with secret redaction.
- Domain glossary and ADR discipline.
- Public-interface test seam selection.

Patterns to adapt:
- Task dependency DAG/frontier and fresh-context parallel implementers.
- Wayfinder decision maps.
- Tight red-capable debugging loops.
- Architecture HTML review.
- Optional per-repository configuration.

No behavior-evaluation harness or tests directory was found; package scripts primarily manage Changesets/version synchronization.

Side-effect warnings:
- Implement workflows commit.
- Implement-spec creates an integration branch and merges.
- Ticket/spec flows can publish and label issues.
- Triage can comment, relabel, or close issues.
- These actions must not bypass the user's approval requirement.

The source documents Codex plugin installation, but the audit did not execute it. Do not force all 27 skills into the toolkit or force a grilling workflow onto every change.

## Adoption decision

**ADOPT selected review, handoff, glossary/ADR, and public-interface test-seam patterns. ADAPT DAG scheduling, fresh-context parallelism, and wayfinder maps. REJECT wholesale import and unapproved issue/Git side effects.**

## Phase mapping

- Phase 7: invocation metadata and configuration.
- Phase 8: bounded delegation and parallel implementers.
- Phase 9: wayfinder, handoff, and architecture workflow.
- Phase 10: seam-based TDD, review, debugging, and evaluation.
- Phase 11: Codex plugin compatibility/runtime checks.

No plugin or source package is installed by this audit.
