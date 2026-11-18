# Source Audit — Superpowers

- **Source:** [obra/superpowers](https://github.com/obra/superpowers)
- **Audited revision:** `main`, commit `22f0b463e7a5e579904dd6211a520321035526f7`
- **Release:** v7.0.2
- **License noted:** MIT
- **Audit date:** 2026-11-18
- **Evidence status:** Source/documentation inspection; no runtime install/tests.

## Findings

Superpowers is a cross-harness agentic software-development methodology with 15 composable skills and a Codex plugin manifest. It is not an agent runtime or a complete tool registry. The manifest points at `./skills/` and has `hooks: {}`. Codex subagent support requires runtime configuration and harness support.

Strong selected patterns:
- Verification-before-completion using fresh command/output evidence.
- Systematic debugging with root-cause diagnosis before fixes.
- TDD for skills: baseline pressure scenario, author skill, rerun adversarial evaluation.
- Two-stage review: specification compliance, then code quality.
- Human choice at branch finishing: merge, push, or keep.
- Small independently testable plans with exact paths/tests.
- Fresh-context implementer plus separate reviewer.
- Durable task ledger for context-compaction recovery.
- Worktree isolation for parallel work.

Important overrides:
- Do not adopt mandatory skill invocation before every response.
- Do not adopt continuous execution without pauses.
- Do not adopt implementer auto-commit.
- User approval remains required before commits, merges, pushes, and consequential actions.
- Do not copy the full 15-skill suite into a toolkit that already has 13 canonical skills, 5 agents, and existing workflows/evals.

The behavior-evaluation harness is not included in this repository; a separate superpowers-evals repository is referenced. Optional visual companion/telemetry behavior should be reviewed before use.

## Adoption decision

**ADOPT selected verification/debugging/skill-TDD/review patterns; ADAPT planning, delegation, worktree, and ledger patterns. REJECT wholesale skill import and automatic commit behavior.**

## Phase mapping

- Phase 7: Codex plugin packaging/manifest and skill compatibility patterns.
- Phase 8: fresh-context delegation, bounded task briefs, independent review.
- Phase 9: approved design → plan → TDD execution → review → finish; worktree/ledger recovery.
- Phase 10: skill pressure tests, adversarial multi-session evaluations, regression.
- Phase 11: real Codex plugin/discovery/multi-agent runtime validation.

No Superpowers plugin or package is installed by this audit.
