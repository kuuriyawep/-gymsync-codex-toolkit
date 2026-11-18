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
| Evaluation case specifications | 54 |
| Rubric files | 7 (4 Markdown, 3 structured JSON) |
| Static skill scorecards | 13 (one per native skill; model-assisted static reviews) |
| Evaluation result/report artifacts tracked in Git | 0 |
| Phase 9 workflow-ledger unit tests | 31 |
| Latest verified CI run | #44303295207 — 127 unit tests and all 10 quality-gate steps passed |

The 54 cases are authored specifications, not completed behavioral evaluations. The absence of committed run records is not evidence of a pass; it means no historical run record is currently tracked in the repository. CI creates and validates a deterministic smoke-test result during the run, but that result is not a trusted Codex behavioral evaluation.

## 3. Existing evaluation architecture

- `tools/evaluate_toolkit.py` discovers cases, validates case and rubric JSON contracts, prepares deterministic results, records behavioral criteria as NOT_RUN, writes immutable JSON/Markdown artifacts, validates saved result records, and supports comparison with an earlier run.
- `tools/validate_toolkit.py` validates repository structure, schemas, skill mirrors, and the structured skill-authoring coverage minimums.
- `evals/rubrics/deterministic.md` defines artifact-level checks.
- `evals/rubrics/behavioral.md` defines real-session behavior grading.
- `evals/rubrics/agent-coordination.md` defines delegation-specific behavior.
- `evals/rubrics/skill-quality.md` defines six static dimensions with a 10/12 threshold and no zero dimension.
- Three structured JSON rubric contracts exist for behavioral, deterministic, and skill-quality; agent-coordination is Markdown-only.
- CI currently runs unit tests, skill mirror parity, project-memory validation, toolkit validation, case/rubric validation, deterministic evaluation generation, and result validation.

## 4. Skill inventory and initial review

The 13 native skill artifacts inspected are:

1. `change-impact-analysis`
2. `clear-technical-communication`
3. `code-review`
4. `documentation-and-decisions`
5. `implementation-planning`
6. `project-intelligence`
7. `requirements-clarification`
8. `risk-aware-tdd`
9. `security-review`
10. `skill-authoring-and-evaluation`
11. `systematic-debugging`
12. `verification-gate`
13. `workflow-orchestration`

All 13 portable counterparts are present. Their content is maintained as native/portable pairs; CI checks synchronization. A first-pass six-dimension static scorecard now exists for each of the 13 native skills under `evals/skill-scores/`. These are model-assisted document reviews, not independent human reviews or behavioral evaluations. They reference skill revision `f47bb2857d5fe33e390f02bf94c68ea3e3e488d5`; subsequent commits added scorecards and their validator without changing the reviewed skill files. Every scorecard keeps runtime status `NOT_RUN`. Their coverage evidence is uneven: some skills have only one or two direct cases, and only selected suites have formal coverage labels. The scores therefore describe static contract quality at the reviewed revision, not complete test coverage or runtime readiness.

### Static scorecard snapshot

All 13 native skills now have a first-pass static scorecard. The current scorecards total 140/156 and all 13 meet the rubric's static PASS threshold. This is a model-assisted static assessment, not an independent human review. All 13 runtime statuses remain NOT_RUN.

| Skill | Score | Direct cases | Formal labels (in-scope / near-miss / edge) |
|---|---:|---:|---:|
| change-impact-analysis | 10/12 | 1 | 0 / 0 / 0 |
| clear-technical-communication | 10/12 | 1 | 0 / 0 / 0 |
| code-review | 11/12 | 2 | 1 / 1 / 0 |
| documentation-and-decisions | 10/12 | 2 | 1 / 1 / 0 |
| implementation-planning | 10/12 | 2 | 1 / 1 / 0 |
| project-intelligence | 12/12 | 8 | 3 / 2 / 1 |
| requirements-clarification | 10/12 | 2 | 0 / 0 / 0 |
| risk-aware-tdd | 11/12 | 3 | 0 / 0 / 0 |
| security-review | 10/12 | 2 | 0 / 0 / 0 |
| skill-authoring-and-evaluation | 12/12 | 6 | 3 / 2 / 1 |
| systematic-debugging | 11/12 | 3 | 0 / 0 / 0 |
| verification-gate | 11/12 | 2 | 0 / 0 / 0 |
| workflow-orchestration | 12/12 | 19 | 3 / 2 / 1 |

The formal label counts use the case-level coverage field; unlabelled cases remain useful references but do not count toward the three-category coverage minimum. A score of PASS with a coverage score of 1 means the skill's written contract passed the static threshold while its dedicated evaluation coverage is still incomplete.

### Coverage-enforcement discrepancy

The skill-quality rubric describes evaluation coverage as part of the quality of a skill and the authoring skill describes a representative case set. However, the structured `coverage_requirements.target_skill` currently points specifically to `skill-authoring-and-evaluation`, and the validator applies the 3/2/1 minimums to that target. It does not prove that each of the other 12 skills has its own 3 in-scope, 2 near-miss, and 1 edge case. Treat this as a real coverage gap to resolve deliberately, not as a reason to duplicate 78 cases blindly. First map existing 54 cases to skills and taxonomy, then decide proportionate per-skill coverage requirements.

## 5. First-pass findings

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
5. **Schema validator limits:** the repository intentionally implements a subset of JSON Schema Draft 2020-12. The evaluator now rejects unsupported schema keywords rather than silently ignoring them; `minimum`, `maximum`, `minItems`, and `maxItems` are enforced, with regression tests. Full Draft 2020-12 compatibility remains out of scope.
6. **Runner failure safety:** review interruption between JSON and Markdown creation, cleanup behavior, concurrent run IDs, symlink/path edge cases, and corrupted prior records.
7. **Coverage mapping:** map the 54 cases to the 13 skills and evaluation taxonomy to identify true gaps and redundant scenarios before adding any case.
8. **Cross-platform reliability:** current CI is Python 3.11 on Ubuntu; Windows, macOS, and additional Python versions are not certified.

## 6. Phase 10 work plan

1. Complete a case-to-skill/taxonomy coverage matrix; identify overlap and missing behavior. **Inventory updated; complete case-to-skill/taxonomy mapping remains open.**
2. Apply the static skill-quality rubric to each of the 13 native skills and record evidence-based scores. Verify portable mirrors separately through parity checks; do not score duplicate copies as separate skills. **First-pass scorecards recorded (13/13 PASS, model-assisted); independent review and coverage remediation remain open.**
3. Audit evaluator comparison, schema subset, output atomicity, path handling, and malformed-input behavior.
4. Add only non-duplicative tests for confirmed defects or uncovered failure modes.
5. Run the full CI pipeline on the exact final commit and review its logs.
6. Produce a Phase 10 report with PASS/FAIL/NOT_RUN distinctions and a Phase 11 handoff.

## 7. Explicit non-goals

- Do not claim real Codex behavioral validation from static tests.
- Do not launch autonomous agents or external schedulers.
- Do not change GymSync.
- Do not add duplicate evaluation cases merely to increase counts.
- Do not overwrite historical evaluation records.
- Do not claim full Draft 2020-12 compatibility.

## 8. Exit criteria

Phase 10 is complete only when the 13-skill static review is evidence-backed, case coverage and overlap are mapped, evaluator reliability gaps are either fixed or explicitly accepted, the exact-head CI passes, and all unexecuted live Codex scenarios remain clearly marked NOT_RUN for Phase 11.
