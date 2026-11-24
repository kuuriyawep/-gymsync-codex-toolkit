# Evaluation System

The toolkit uses a **hybrid, criteria-based evaluation process**. Deterministic checks validate repository artifacts; behavioral checks assess Codex behavior from an actual session transcript or equivalent evidence. These are separate evidence classes and must never be conflated.

## Quick start

```bash
python tools/evaluate_toolkit.py --list
python tools/evaluate_toolkit.py --validate
python tools/evaluate_toolkit.py --run
python tools/evaluate_toolkit.py --run --compare evals/results/<previous-run-id>.json
```

The runner uses only the Python standard library. Saved result records can be checked with `--validate-result`; this validates the result schema, unique IDs, per-case status derivation, overall status, and summary counts. It discovers `evals/cases/*.json`, validates cases against the declared schema contract, and writes an immutable run record plus Markdown report. It runs repository integrity validation and prepares behavioral criteria as NOT_RUN. It does **not** launch Codex, invoke a model, inspect a live conversation, or grade behavioral output.

## Evaluation layers

1. **Deterministic** — JSON/schema validity, unique IDs, target references, and repository artifact integrity where implemented.
2. **Static skill quality** — skill contracts and their evaluation coverage are scored using `evals/rubrics/skill-quality.md`. The static score is not a behavioral result.
3. **Behavioral** — routing, skill triggering, workflow compliance, agent boundaries, safety, verification honesty, and output quality are graded from a real trusted Codex session.
4. **Regression** — compare criterion outcomes between immutable run records. Missing or unexecuted results are never treated as a pass.

## Status semantics

- `PASS`: criterion was executed and evidence supports expected behavior.
- `FAIL`: criterion was executed and evidence demonstrates a violation.
- `BLOCKED`: evaluation could not proceed because a prerequisite or safe access was unavailable.
- `NOT_RUN`: criterion has not been evaluated.
- `NOT_APPLICABLE`: criterion does not apply; include a reason.

Overall status is `FAIL` if any criterion fails; otherwise `BLOCKED` if a required criterion is blocked; otherwise `NOT_RUN` when behavioral evaluation remains unperformed or no criteria apply; otherwise `PARTIAL` when applicable criteria remain incomplete; and `PASS` only when all required applicable criteria pass. No weighted average or percentage can hide a critical failure.

## Skill authoring and static quality review

Use `.agents/skills/skill-authoring-and-evaluation/SKILL.md` when creating, materially revising, auditing, or evaluating a reusable skill.

The static skill-quality rubric scores exactly six dimensions from 0–2: trigger/scope, inputs/prerequisites, procedure, output contract, safety/failure handling, and evaluation coverage/evidence discipline. The Markdown rubric and structured JSON definition use the same six criterion IDs, scoring scale, acceptance threshold, and hard-fail policy. Static PASS requires at least 10/12, no zero scores, and no hard-fail condition. See `evals/rubrics/skill-quality.md` and `evals/rubrics/skill-quality.json`.

A skill's evaluation set must include at least 3 in-scope prompts, 2 near-miss/out-of-scope prompts, and 1 edge/ambiguity/failure/stop-condition prompt. Cases targeting the skill-authoring rubric must label each case with `coverage` (`in-scope`, `near-miss`, or `edge`); `tools/validate_toolkit.py` enforces the structured rubric's declared minimum counts. Each case must define observable expected and prohibited behaviors. These authored cases are test specifications, not test results.

## Behavioral evaluation procedure

1. Open the repository in a trusted Codex session.
2. Select a case from `evals/cases/` and use its prompt without silently changing intent.
3. Capture transcript, commands, file diffs, and tool evidence. Redact secrets and private data.
4. Grade every applicable criterion: PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE, rationale, and evidence reference.
5. Save the reviewed result as a **new** run record. Never overwrite historical results.
6. Generate/update the report and compare against the previous run for regression.

For delegation cases, record which agent was selected, the complete handoff, task ownership/dependencies, parallelization, reviewer role, and evidence used to resolve conflicts. A behavioral case is not passed merely because expected artifacts exist; the actual Codex session must demonstrate the behavior.

See `evals/rubrics/behavioral.md`, `evals/rubrics/deterministic.md`, `evals/rubrics/agent-coordination.md`, and `evals/rubrics/skill-quality.md`, plus matching JSON rubric definitions. Rubrics are validated against `schemas/evaluation-rubric.schema.json`.

## Evidence and limitations

Evidence references should be repository-relative paths, transcript identifiers, command records, or other reviewable artifacts. Do not embed credentials, tokens, or sensitive user data. Deterministic PASS means only that the checked artifact-level condition passed; it does not establish that Codex behaved correctly. Static skill-quality PASS does not establish runtime skill triggering or execution.

## Run storage

- `evals/results/` — machine-readable, immutable run records.
- `evals/reports/` — human-readable reports.
- Each run has a unique run ID and records commit/version metadata when supplied.
- Run record and report files are created with exclusive-create semantics; an existing artifact is never overwritten, including when two runs race for the same ID.
- Custom `--output` paths must resolve inside the repository. Paths outside the repository are rejected.

### GitHub Actions artifact retention

The `Toolkit Quality Gates` workflow uploads each generated deterministic CI run record
(`evals/results/ci-<run-id>-<attempt>.json`) together with its human-readable report
(`evals/reports/ci-<run-id>-<attempt>.md`) as one GitHub Actions artifact.
Artifact names include both the workflow run ID and attempt number, so reruns remain
separate and prior evidence is not overwritten. Artifacts are retained for 30 days.
The upload step runs even when an earlier step fails; if generation did not produce
both files, the workflow emits a warning rather than masking the original failure.

Download artifacts from the relevant GitHub Actions run's **Artifacts** section.
These files represent deterministic repository checks only; behavioral criteria remain
`NOT_RUN` until evaluated from a trusted Codex session.

Phase 6 adds seven agent-coordination behavioral scenarios. Use `evals/rubrics/agent-coordination.md` and `docs/agent-validation.md`. These remain NOT_RUN until exercised in a trusted Codex session.
