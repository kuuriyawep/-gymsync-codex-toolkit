# Deterministic Evaluation Rubric

Use only for checks that can be reproduced from repository artifacts without interpreting model behavior.

| Criterion | PASS evidence | FAIL evidence | Critical |
|---|---|---|---|
| Case parses | Valid UTF-8 JSON object | Invalid JSON or non-object root | Yes |
| Case schema | All declared schema constraints pass | Any required schema constraint fails | Yes |
| Case identity | Unique, stable kebab-case ID | Missing or duplicate ID | Yes |
| Case discoverability | Case is under `evals/cases/*.json` | Case is outside discovery scope | No |
| Target references | Every declared repository-relative target resolves | A declared target is missing or escapes repository root | No |
| Run provenance | Run ID and target revision are recorded or explicitly unknown | Provenance is fabricated or contradictory | Yes |
| Result integrity | Every status is from the allowed vocabulary and has a reason/evidence policy | Invalid status or unsupported pass claim | Yes |

A deterministic PASS applies only to the named artifact-level criterion. It must not be reused as evidence of successful Codex behavior.
