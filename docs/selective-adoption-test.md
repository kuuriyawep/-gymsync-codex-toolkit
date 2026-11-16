# Selective Adoption Usability Test

## Status

**Static checklist prepared; no target repository has been modified and no Codex runtime test has been executed.**

This test defines how to validate selective adoption without overwriting a target project's existing configuration. It is intentionally non-destructive.

## Test objective

Verify that a maintainer can adopt only the required toolkit components into an unrelated repository while preserving its instructions, configuration, memory, and evaluation history.

## Preconditions

- Choose a disposable test repository or temporary copy, not the production project.
- Record the target repository's current commit and working-tree status.
- Inventory existing `AGENTS.md`, `.agents/`, `.codex/`, `workflows/`, `templates/`, `evals/`, and `schemas/` paths.
- Do not run copy/merge operations against a dirty or unbacked-up target.
- Do not copy this toolkit's project memory or historical evaluation results into the target.

## Test cases

| ID | Scenario | Expected result | Evidence to capture |
|---|---|---|---|
| AD-01 | Target already has `AGENTS.md` | Existing file is preserved; toolkit rules are reviewed and selectively merged, never blindly overwritten | Before/after diff |
| AD-02 | Target already has `.agents/skills/` | Existing skills remain; only selected, non-conflicting toolkit skills are added | Directory diff and skill inventory |
| AD-03 | Target already has `.codex/agents/` | Existing agent TOML files remain; naming collisions are resolved explicitly | TOML inventory and diff |
| AD-04 | Adopt workflow orchestration | `workflows/registry.md` and referenced workflow/template files are present | Link/path check |
| AD-05 | Adopt project intelligence | Generic memory templates and validator are present; target-specific memory is authored independently | Path check; no copied personal/project data |
| AD-06 | Adopt evaluation tooling | Schemas, cases/rubrics, runner, and report template are included as a coherent set | Validator output and evaluation paths |
| AD-07 | Omit optional companion files | Instructions identify unavailable procedures; no missing file is silently assumed | Missing-path report |
| AD-08 | Target contains existing evaluation history | Existing records remain unchanged; new records use target-specific IDs and repository identity | Before/after hash comparison |
| AD-09 | Codex opens target workspace | Project discovery is checked in a trusted Codex session; unsupported features are reported honestly | Session transcript and discovered components |
| AD-10 | Roll back adoption | Only files introduced by the test are removed; original target files are restored from backup | Final diff and clean status |

## Acceptance criteria

A selective adoption is acceptable only when:

1. No pre-existing target file was overwritten without explicit review and approval.
2. Existing target instructions remain authoritative where conflicts exist.
3. Every adopted skill's referenced companion paths are available, or the limitation is documented.
4. Agent names and referenced role definitions resolve consistently.
5. Project memory and evaluation evidence remain target-specific.
6. No dependency, service, external framework, or remote side effect is introduced implicitly.
7. The target working tree shows only the intended adoption changes.
8. Runtime discovery claims are backed by an actual trusted Codex session.

## Static checks available before Codex

The toolkit repository can verify its own skill parity, agent TOML syntax, workflow structure, evaluation schemas, and internal documentation links. Those checks do **not** prove that a different repository's instructions will merge cleanly or that a Codex client will discover every component.

## Runtime checks requiring Codex

Mark AD-09 **NOT_RUN — CODEX_REQUIRED** until a trusted Codex session is available. Do not replace this with a mock response or infer success from the presence of files.

## Rollback rule

Use a disposable clone or temporary copy. If an adoption test fails, restore the target from the recorded baseline or discard the disposable copy. Never run a broad cleanup command against an unknown target tree.
