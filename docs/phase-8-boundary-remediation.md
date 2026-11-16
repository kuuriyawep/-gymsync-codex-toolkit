# Phase 8 — Skill Boundary Remediation

**Status:** Static remediation applied; deterministic CI passed; Codex behavioral evaluation deferred  
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
| Native/portable parity | PASS | All 13 skill pairs match; CI `python tools/sync_skills.py --check` passed |
| Toolkit unit tests | PASS | GitHub Actions run #43891253601 |
| Toolkit validator | PASS | GitHub Actions run #43880479161 |
| Evaluation schema validation | PASS | GitHub Actions run #43880479161 validated cases and generated result |
| GitHub Actions CI | PASS | [Run #43891253601](https://github.com/kuuriyawep/-gymsync-codex-toolkit/actions/runs/43891253601) — all steps passed on commit `fb7967a4ce7b54a6a4731b92af221f8833be9e2c`; 38 unit tests passed and all 41 evaluation cases validated |
| Codex behavioral evaluation | NOT_RUN — CODEX_REQUIRED | Requires a real Codex session and transcript evidence |

## Scope and safety

No GymSync application source, database, deployment, external agent framework, or installation was touched. No Codex runtime behavior is claimed as tested. Deterministic checks have now passed on the latest main commit (CI run #109). Phase 8 remains open only for the real Codex behavioral evaluation; those scenarios remain `NOT_RUN — CODEX_REQUIRED`.
