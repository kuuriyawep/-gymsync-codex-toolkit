# Phase 8 — Skill Quality Audit and Remediation Completion

**Status:** Static remediation complete; final CI result pending; Codex behavioral evaluation deferred  
**Branch:** `main`  
**Scope:** All 13 canonical skills, their 13 portable mirrors, related bug-fix routing, evaluation rubric/cases, and documentation

## Objective

Address the findings from the 13-skill audit by clarifying overlapping responsibilities, standardizing operational contracts, adding measurable skill-quality criteria, and preserving evaluation evidence without claiming unavailable runtime tests.

## Remediation completed

### 1. Skill boundaries

The three overlapping skills now have explicit, non-overlapping ownership:

| Skill | Owns | Handoff |
|---|---|---|
| `systematic-debugging` | Symptom capture, safe reproduction, causal tracing, root-cause confidence, alternatives | Evidence-backed diagnosis and regression scenario to planning / implementation |
| `risk-aware-tdd` | Approved behavior tests, focused implementation, test execution evidence | Changed paths, tests, outcomes, exceptions, risks to verification |
| `verification-gate` | Final acceptance mapping, diff/scope review, proportionate checks, honest disposition | PASS / FAIL / BLOCKED-PARTIAL decision |

The bug-fix workflow and registry now encode the same sequence. Diagnosis can be skipped only when the root cause is already established with evidence.

### 2. Contracts across all 13 skills

All canonical skills under `.agents/skills/` and all portable mirrors under `skills/` were updated or confirmed with proportionate operational contracts:

- Trigger and important non-trigger boundaries.
- Inputs, prerequisites, assumptions, and approvals.
- Actionable procedures and decision points.
- Required outputs or finding/plan formats.
- Evidence, uncertainty, and failure handling.
- Stop conditions and ownership boundaries.
- Handoffs where the skill is one stage of a larger workflow.

The workflow-orchestration skill now points to `AGENTS.md`, `workflows/registry.md`, and the selected workflow as authority sources instead of duplicating routing definitions.

### 3. Measurable skill authoring and evaluation

Updated `skill-authoring-and-evaluation` to require a seven-part skill contract and a repeatable evaluation set:

- At least 3 representative in-scope prompts.
- At least 2 near-miss or out-of-scope prompts.
- At least 1 edge, ambiguity, failure, or stop-condition prompt.

Added `evals/rubrics/skill-quality.md` and `skill-quality.json`. Six dimensions are scored 0–2: trigger/scope, inputs/prerequisites, procedure executability, output contract, safety/failure handling, and evaluation coverage/evidence discipline.

Static PASS requires at least 10/12, no zero dimension, and no hard-fail condition. Static acceptance is explicitly separate from behavioral runtime PASS.

### 4. Evaluation coverage

Added three boundary scenarios and three skill-authoring/evaluation scenarios:

- `debugging-diagnosis-before-implementation.json`
- `risk-aware-tdd-test-first-handoff.json`
- `verification-gate-final-acceptance.json`
- `skill-authoring-contract-and-coverage.json`
- `skill-authoring-out-of-scope-routing.json`
- `skill-authoring-runtime-unavailable.json`

Updated the behavioral rubric and evaluation guide to distinguish static quality from runtime behavior.

## Files and areas updated

- 13 canonical skills: `.agents/skills/*/SKILL.md`
- 13 portable mirrors: `skills/*/SKILL.md`
- `workflows/bug-fix.md`
- `workflows/registry.md`
- `evals/rubrics/skill-quality.md`
- `evals/rubrics/skill-quality.json`
- `evals/rubrics/behavioral.md`
- `evals/rubrics/behavioral.json`
- `evals/README.md`
- Six new cases under `evals/cases/`
- `docs/phase-8-skill-audit.md`
- `docs/phase-8-boundary-remediation.md`
- `README.md`

## Verification status

| Check | Status | Evidence / next step |
|---|---|---|
| GitHub updates | PASS | Commits created on `main`; files are being re-read for parity and schema checks |
| Native/portable skill parity | PENDING | Verify all 13 pairs and run `python tools/sync_skills.py --check` in CI |
| Evaluation JSON syntax | PENDING | Validate all six new cases and structured rubric through `python tools/evaluate_toolkit.py --validate` |
| Toolkit validator and unit tests | PENDING | Await final GitHub Actions run |
| GitHub Actions quality pipeline | PENDING | Final run URL to be recorded after it completes |
| Static skill quality scores | NOT SCORED | A reviewer must score each skill dimension-by-dimension using the new rubric; file changes alone do not establish a score |
| Codex behavioral evaluation | NOT_RUN — CODEX_REQUIRED | Requires a trusted Codex session, exact case prompts, transcript/artifacts, and criterion-level review |
| Selective adoption trial | NOT_RUN | Separate preflight/trial; no GymSync project was changed |

## Safety and exclusions

- No GymSync application source, database, deployment, or user data was changed.
- No dependency, external agent framework, or third-party runtime was installed.
- No production or external side effects were performed.
- No Codex behavioral PASS is claimed.
- The toolkit remains Codex-first; Codex is not replaced by another orchestrator.

## Completion decision

The **static remediation work is complete**. The Phase 8 milestone remains open pending final deterministic CI and the future trusted Codex behavioral run. If the user does not yet have Codex available, keep the behavioral cases ready and report them as NOT_RUN rather than treating them as a blocker to the already completed static authoring work.
