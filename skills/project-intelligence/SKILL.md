---
name: project-intelligence
description: Build, retrieve, verify, and maintain evidence-backed project knowledge for Codex across sessions. Use for repository onboarding, targeted architecture discovery, task resumption, decision recall, and memory freshness checks.
---

# Project Intelligence

Use this skill to maintain a compact, evidence-backed project knowledge layer for Codex across sessions. Codex remains the primary coordinator.

## When to use
Use for repository onboarding, architecture discovery, resuming prior work, recalling project decisions, or maintaining project-memory artifacts. Do not use as a substitute for live source inspection or as a place to store credentials or personal data.

## Workflow
1. Confirm repository identity and read root instructions.
2. Read project profile and current-state checkpoint.
3. Retrieve only memory pages relevant to the task; use the repository map to locate source, tests, schemas, and configuration.
4. Verify consequential claims against current source, tests, schemas, and runtime configuration before relying on memory.
5. Label claims Verified, Assumption, Unknown, or Stale. Never silently promote assumptions.
6. Record meaningful progress, changed paths, checks actually run, blockers, and next action in the task checkpoint.
7. Preserve decision history; mark replaced decisions Superseded rather than deleting them.
8. Run `python tools/validate_project_memory.py` after memory edits; use `--strict-freshness` for high-impact decisions.

## Required output
- Repository and source scope inspected.
- Relevant memory pages retrieved and their freshness.
- Verified facts, assumptions, unknowns, and stale claims.
- Source paths supporting consequential facts.
- Checkpoint/decision changes made, if any.
- Validation command and actual outcome, or why it was not run.

## Evidence and safety
- Verified claims cite repository paths, tests, schemas, commits, or explicit user decisions.
- Memory is an index, not source of truth. Current source artifacts and explicit user instructions take precedence.
- Never store credentials, tokens, private keys, personal data, or production secrets.
- Summarize and link to source; do not duplicate large code files.
- Keep each project's memory separate.
- Do not autonomously rewrite memory or promote unreviewed learning.
- If evidence conflicts or is missing, report the uncertainty and re-verify.

## Stop conditions
Stop before recording an unverified assumption as fact, crossing project boundaries, or storing sensitive information. If required memory sources are unavailable, say so and continue only from inspectable current evidence.
