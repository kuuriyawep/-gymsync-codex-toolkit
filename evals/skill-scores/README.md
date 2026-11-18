# Static Skill Scorecards

Each JSON file is a versioned static review of one canonical native skill.

- Rubric: `evals/rubrics/skill-quality.json` and `skill-quality.md`.
- Six dimensions, each 0–2; maximum 12.
- PASS requires at least 10/12, no dimension below 1, and no hard-fail.
- Scorecards identify the exact source revision and evidence references.
- `runtime_status: NOT_RUN` means no trusted Codex behavioral run is claimed.
- Evaluation case files are specifications, not results.
- A scorecard is a static assessment, not an independent human review or production-readiness certificate.

Run `python tools/validate_skill_scores.py` to validate scorecard schemas, totals, dispositions, case references, coverage counts, and one-scorecard-per-skill completeness.
