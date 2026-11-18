# Phase 10 — Evaluation & Reliability

**Status:** IN PROGRESS — inventory and first-pass gap map completed; per-skill scoring and reliability hardening remain open.

## 1. Scope and audit rules

Phase 10 improves the evaluation system already in the repository. It must not duplicate existing cases, rubrics, validators, or tests. Static repository checks and behavioral Codex evaluation are separate evidence classes. No behavioral PASS may be recorded without a real trusted Codex session and reviewable evidence.

## 2. Repository inventory (2026-11-18)

| Asset | Inventory |
|---|---:|
| Native Codex skills | 13 |
| Portable skill mirrors | 13 |
| Native/portable pairs | 13 |
| Evaluation case specifications | 42 |
| Rubric files | 7 (4 Markdown, 3 structured JSON) |
| Evaluation result/report artifacts tracked in Git | 0 |
| Phase 9 workflow-ledger unit tests | 31 |
| Latest verified CI run | #44297943897 — 10 substantive quality-gate steps passed |

The 42 cases are authored specifications, not completed behavioral evaluations. The absence of committed run records is not evidence of a pass; it means no historical run record is currently tracked in the repository. CI creates and validates a deterministic smoke-test result during the run, but that result is not a trusted Codex behavioral evaluation.

## 3. Existing evaluation architecture

- `tools/evaluate_toolkit.py` discovers cases, validates case and rubric JSON contracts, prepares deterministic results, records behavioral criteria as NOT_RUN, writes immutable JSON/Markdown artifacts, validates saved result records, and supports comparison with an earlier run.
- `tools/validate_toolkit.py` validates repository structure, schemas, skill mirrors, and the structured skill-authoring coverage minimums.
- `evals/rubrics/deterministic.md` defines artifact-level checks.
- `evals/rubrics/behavioral.md` defines real-session behavior grading.
- `evals/rubrics/agent-coordination.md` defines delegation-specific behavior.
- `evals/rubrics/skill-quality.md` defines six static dimensions with a 10/12 threshold and no zero dimension.
- Three structured JSON rubric contracts exist for behavioral, deterministic, and skill-quality; agent-coordination is Markdown-only.
- CI currently runs unit tests, skill mirror parity, project-memory validation, toolkit validation, case/rubric validation, deterministic evaluation generation, and result validation.

## 4. First-pass findings

### Confirmed strengths

1. Deterministic and behavioral results are explicitly separated.
2. NOT_RUN, BLOCKED, FAIL, PASS, and NOT_APPLICABLE have distinct semantics.
3. Critical failures dominate the overall verdict; averages cannot hide them.
4. Saved results are checked for duplicate IDs, per-case status consistency, overall status, and summary counts.
5. Run records/reports use exclusive creation and output paths are constrained to the repository.
6. Skill-authoring case coverage has enforced minimums: 3 in-scope, 2 near-miss, and 1 edge case.
7. Native/portable skill parity is checked in CI.

### Gaps to verify or improve

1. **Static quality scoring breadth:** the six-dimension skill-quality rubric exists, but the current CI does not demonstrate that all 13 skills have individually scored review records. The current coverage enforcement is specifically focused on the skill-authoring target. Do not infer that every skill has passed static scoring.
2. **Behavioral evidence:** all runtime behavior remains unverified until trusted Codex sessions are run. Seven agent-coordination scenarios are explicitly deferred.
3. **Result history:** no result/report artifacts are currently tracked. Decide which baseline runs should be retained after review, without fabricating past results.
4. **Regression comparison:** inspect comparison semantics for missing cases, changed criterion IDs, and status downgrades; ensure missing evidence never appears as improvement.
5. **Schema validator limits:** the repository intentionally implements a subset of JSON Schema Draft 2020-12. Test that unsupported keywords cannot silently create false confidence, and keep the limitation visible.
6. **Runner failure safety:** review interruption between JSON and Markdown creation, cleanup behavior, concurrent run IDs, symlink/path edge cases, and corrupted prior records.
7. **Coverage mapping:** map the 42 cases to the 13 skills and evaluation taxonomy to identify true gaps and redundant scenarios before adding any case.
8. **Cross-platform reliability:** current CI is Python 3.11 on Ubuntu; Windows, macOS, and additional Python versions are not certified.

## 5. Phase 10 work plan

1. Complete a case-to-skill/taxonomy coverage matrix; identify overlap and missing behavior.
2. Apply the static skill-quality rubric to each of the 13 native skills and record evidence-based scores. Verify portable mirrors separately through parity checks; do not score duplicate copies as separate skills.
3. Audit evaluator comparison, schema subset, output atomicity, path handling, and malformed-input behavior.
4. Add only non-duplicative tests for confirmed defects or uncovered failure modes.
5. Run the full CI pipeline on the exact final commit and review its logs.
6. Produce a Phase 10 report with PASS/FAIL/NOT_RUN distinctions and a Phase 11 handoff.

## 6. Explicit non-goals

- Do not claim real Codex behavioral validation from static tests.
- Do not launch autonomous agents or external schedulers.
- Do not change GymSync.
- Do not add duplicate evaluation cases merely to increase counts.
- Do not overwrite historical evaluation records.
- Do not claim full Draft 2020-12 compatibility.

## 7. Exit criteria

Phase 10 is complete only when the 13-skill static review is evidence-backed, case coverage and overlap are mapped, evaluator reliability gaps are either fixed or explicitly accepted, the exact-head CI passes, and all unexecuted live Codex scenarios remain clearly marked NOT_RUN for Phase 11.
