# Source Audit — Everything Claude Code (ECC)

- **Source:** [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) (ECC)
- **Audit provenance:** Earlier project review, carried forward on 2026-11-18; no fresh audit performed.
- **Evidence status:** PARTIAL — prior conversation record, not a complete reproducible source snapshot.
- **Revision:** Exact commit/release was not preserved in the recovered audit record.
- **Reuse rule:** No wholesale repository import.

## Recovered findings

A preliminary review on 2026-11-17 recorded 6,674 tree entries. The repository README claimed 72 agents, 327 skills, and 98 legacy shims. The review confirmed the presence of Codex-oriented surfaces including `.codex-plugin/`, `.codex/agents/`, and `.agents/skills/`, plus a navigation/routing guide, multi-agent Explorer/reviewer/documentation-researcher roles, evaluation definitions/graders/CLI, worktree orchestration, AgentShield/supply-chain checks, and MCP policy.

The review also recorded that `scripts/eval-harness.js` reported gate execution unavailable because of isolation constraints. This is not evidence that the harness passed.

An earlier selective-integration decision recorded these ECC-derived capability areas:
- Security review.
- Change-impact analysis.
- Verification-loop discipline.
- Context and decision handling.

The existing toolkit already contains corresponding foundations:
- `.agents/skills/security-review/`
- `.agents/skills/change-impact-analysis/`
- `.agents/skills/verification-gate/`
- `.agents/skills/documentation-and-decisions/`
- `.agents/skills/project-intelligence/`

These are existing toolkit implementations, not proof that ECC source files were copied.

## Adoption decision

**ADOPT selected practices; do not import the full ECC bundle.**

Carry forward:
- Security review and supply-chain awareness.
- Change-impact analysis before broad modifications.
- Evidence-backed verification loops.
- Explicit context/decision records.
- Agent role boundaries and evaluation discipline.

Do not import all advertised skills, agents, legacy shims, or configuration as a bundle. Map unique capabilities to the existing toolkit owners and add only demonstrated gaps.

## Limitations and next handling

The recovered record does not preserve exact source paths, file-level license evidence, a commit SHA, or complete detailed findings. Do not present this as a fully reproducible, revision-pinned audit. No new audit was run here because the user explicitly required avoiding repeated ECC work. If code-level reuse is later proposed, first recover or perform a narrowly scoped, user-approved file/license check rather than copying from memory.

No ECC package, plugin, or dependency is installed by this record.
