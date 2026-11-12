# Evaluation System

The toolkit uses a **hybrid, criteria-based evaluation process**. Deterministic checks validate repository artifacts; behavioral checks assess Codex behavior from an actual session transcript or equivalent evidence. These are separate evidence classes and must never be conflated.

## Quick start

```bash
python tools/evaluate_toolkit.py --list
python tools/evaluate_toolkit.py --validate
python tools/evaluate_toolkit.py --run
# Compare with a previous immutable run record
python tools/evaluate_toolkit.py --run --compare evals/results/<previous-run-id>.json
```

The runner uses only the Python standard library. It discovers `evals/cases/*.json`, validates cases against the repository's declared schema contract, and writes an immutable run record plus a Markdown report. It does **not** launch Codex, invoke a model, inspect a live conversation, or grade behavioral output.

## Evaluation layers

1. **Deterministic** — JSON/schema validity, unique IDs, case completeness, target reference shape, and repository artifact integrity where checks are explicitly implemented.
2. **Behavioral** — skill selection, routing, clarification, delegation, safety, tool use, verification honesty, and output quality. A human evaluator records observed evidence against the relevant rubric after running the prompt in a trusted Codex session.
3. **Regression** — compare case/criterion outcomes between immutable run records. A missing or unexecuted result is never treated as a pass.

## Status semantics

- `PASS`: criterion was executed and evidence supports the expected behavior.
- `FAIL`: criterion was executed and evidence demonstrates a violation.
- `BLOCKED`: evaluation could not proceed because a prerequisite or safe access was unavailable.
- `NOT_RUN`: criterion has not been evaluated.
- `NOT_APPLICABLE`: criterion does not apply to this run; include a reason.

Overall status is `FAIL` if any critical criterion fails; otherwise `BLOCKED` if a required criterion is blocked; otherwise `NOT_RUN` when behavioral evaluation remains unperformed; otherwise `PARTIAL` when some applicable criteria remain incomplete; and `PASS` only when all required applicable criteria pass. No weighted average or percentage can hide a critical failure.

## Behavioral evaluation procedure

1. Open the repository in a trusted Codex session.
2. Select a case from `evals/cases/` and use its prompt without silently changing its intent.
3. Capture the relevant transcript, commands, file diffs, and tool evidence. Redact secrets and private data.
4. Grade every applicable rubric criterion. Record PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE, rationale, and evidence reference.
5. Save the reviewed result as a **new** run record. Never overwrite historical results.
6. Generate or update the report and compare against the previous run for regression.

See `evals/rubrics/behavioral.md`, `evals/rubrics/deterministic.md`, and `templates/evaluation-report.md`.

## Evidence and limitations

Evidence references should be repository-relative paths, transcript identifiers, command records, or other reviewable artifacts. Do not embed credentials, tokens, or sensitive user data. The runner's deterministic PASS means only that the checked artifact-level condition passed; it does not establish that Codex behaved correctly.

## Run storage

- `evals/results/` — machine-readable, immutable run records.
- `evals/reports/` — human-readable reports.
- Each run has a unique run ID and records commit/version metadata when supplied. Use a new output path for every run.
