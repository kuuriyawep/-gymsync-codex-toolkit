# Quality Gates

## Local verification

Run from the repository root with Python 3.11 or newer:

```bash
python -m unittest discover -s tests -v
python tools/sync_skills.py --check
python tools/validate_toolkit.py
python tools/evaluate_toolkit.py --validate
python tools/evaluate_toolkit.py --run --revision "$(git rev-parse HEAD)"
```

The final command creates a new JSON record under `evals/results/` and a Markdown report under `evals/reports/`. Run IDs are unique by default. Existing records and reports are never overwritten.

## GitHub Actions

`.github/workflows/quality.yml` runs for pushes and pull requests targeting `main`. The job:

1. Runs the standard-library unit tests.
2. Checks native/portable skill parity.
3. Runs the full toolkit validator, including TOML parsing.
4. Validates evaluation cases and rubrics.
5. Creates a deterministic evaluation-run record as an end-to-end smoke test.\n6. Validates the generated record schema and cross-field consistency.

The workflow uses `contents: read`. It does not push commits, merge pull requests, deploy, or change repository settings.

## Security and reliability boundaries

- Evaluation output paths must resolve within the repository root.
- Run record and report creation uses exclusive file creation; existing artifacts are not replaced.\n- Saved evaluation results can be validated independently, including unique IDs, criterion totals, per-case statuses, and overall status.
- If creating the second artifact fails, an artifact created by that same attempt is removed on a best-effort basis.
- The runner still does not provide cross-filesystem transactions or execute behavioral Codex evaluations.
- Behavioral criteria remain `NOT_RUN` until a real trusted Codex session is reviewed with evidence.
- The workflow's CI result proves only the checks it actually executes; it is not a behavioral or production security certification.

## Limitations

The toolkit's JSON Schema validator intentionally supports the subset of keywords used by its checked-in schemas. It is not a complete Draft 2020-12 implementation. CI currently uses Python 3.11 on Ubuntu; additional operating systems and Python versions are not certified by this workflow.
