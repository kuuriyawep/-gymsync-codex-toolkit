# Phase 8 — Skill Boundary Remediation

**Status:** Static remediation applied; deterministic validation and Codex behavioral evaluation pending  
**Branch:** `main`  
**Scope:** Debugging, test-driven implementation, final verification, and the bug-fix route

## Objective

Make the ownership boundary between three frequently co-selected skills explicit so Codex does not duplicate work, skip handoffs, or claim completion from partial evidence.

## Decisions applied

| Skill | Owns | Does not own | Handoff |
|---|---|---|---|
| `systematic-debugging` | Safe reproduction, causal tracing, root-cause confidence, alternatives, proposed regression scenario | Implementation and final acceptance | Evidence-backed diagnosis to planning / `risk-aware-tdd` |
| `risk-aware-tdd` | Approved behavior tests, focused implementation, test execution evidence | Unknown-cause diagnosis and final release verdict | Changed paths, tests, outcomes, exceptions, risks to `verification-gate` |
| `verification-gate` | Acceptance mapping, final diff/scope review, proportionate checks, honest disposition | Diagnosis and implementation | Final PASS / FAIL / BLOCKED-PARTIAL decision |

## Files updated

- `.agents/skills/systematic-debugging/SKILL.md`
- `.agents/skills/risk-aware-tdd/SKILL.md`
- `.agents/skills/verification-gate/SKILL.md`
- `skills/systematic-debugging/SKILL.md`
- `skills/risk-aware-tdd/SKILL.md`
- `skills/verification-gate/SKILL.md`
- `workflows/bug-fix.md`
- `workflows/registry.md`

The three portable skill mirrors were updated to match their canonical `.agents/skills/` sources. The bug-fix workflow now calls the skills in order and documents each handoff. The registry expresses the same sequence and allows diagnosis to be skipped only when the root cause is already established with evidence.

## Evaluation coverage added

- `evals/cases/debugging-diagnosis-before-implementation.json`
- `evals/cases/risk-aware-tdd-test-first-handoff.json`
- `evals/cases/verification-gate-final-acceptance.json`

These cases are authored evaluation scenarios, not executed behavioral results. They are intended for a trusted Codex session when available.

## Verification status

| Check | Status | Evidence |
|---|---|---|
| GitHub file updates | PASS | Updates returned commit SHAs on `main` |
| Native/portable parity | NOT_RUN | Must run `python tools/sync_skills.py --check` |
| Toolkit unit tests | NOT_RUN | Local repository runtime not attached to this session |
| Toolkit validator | NOT_RUN | Local repository runtime not attached to this session |
| Evaluation schema validation | NOT_RUN | New cases have not yet been run through the repository validator |
| GitHub Actions CI | PENDING | Wait for workflow run triggered by the commits |
| Codex behavioral evaluation | NOT_RUN — CODEX_REQUIRED | Requires a real Codex session and transcript evidence |

## Scope and safety

No GymSync application source, database, deployment, external agent framework, or installation was touched. No Codex runtime behavior is claimed as tested. Phase 8 remains open until deterministic checks pass and the new scenarios are evaluated in a real Codex session.
