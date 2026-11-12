# Evaluation Taxonomy

The taxonomy describes **what** is evaluated, independently of how it is graded.

| Category | Evaluation target | Typical evidence |
|---|---|---|
| Skill correctness | Skill procedure is complete, safe, actionable, and internally consistent | Skill file, review notes |
| Skill triggering | Relevant skill is selected; irrelevant skills are not invoked | Session transcript |
| Workflow compliance | Correct workflow, gates, sequence, and completion state are followed | Transcript, workflow brief |
| Agent role compliance | Delegated roles stay within their authority and return bounded outputs | Handoff and agent outputs |
| Safety and approval | Risk is classified correctly; approvals precede restricted actions | User approval, tool/action transcript |
| Tooling and verification | Tools are appropriate; checks are actually run and reported honestly | Commands, tool results |
| Output quality | Answer is correct, clear, scoped, and evidence-backed | Final output and source evidence |
| Regression | Previously passing criteria remain passing after changes | Comparable run records |

## Risk and criticality

Risk level describes the potential impact of the evaluated task: low, medium, high, or critical. Criterion criticality describes whether a failure must fail the evaluation regardless of other results. They are related but not interchangeable. A low-risk scenario can contain a critical policy criterion, and a high-risk scenario may include non-critical explanatory criteria.

## Evaluation methods

- `deterministic-check`: a reproducible programmatic check over repository artifacts.
- `human-review`: behavioral grading by a reviewer using session evidence.
- `hybrid`: both evidence classes are required.

The method describes the intended evaluation method, not a claim that it has been executed.
