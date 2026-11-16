# Skill Quality Rubric

Use this rubric for static review of a skill file and its associated evaluation cases. Score each dimension from 0 to 2 and cite concrete evidence. Do not award points for length, polish, or claims that are not operationally testable.

## Scoring scale

- **0 — Missing / unsafe:** absent, contradictory, or too vague to apply; creates a material risk of incorrect routing or action.
- **1 — Partial:** present but ambiguous, incomplete, or not consistently testable.
- **2 — Clear / testable:** explicit, internally consistent, proportionate, and usable by the target runtime.

| Dimension | Score 0 | Score 1 | Score 2 |
|---|---|---|---|
| Trigger and scope boundary | No usable trigger or non-goal boundary | Trigger is broad or false-positive boundary incomplete | Intended use and important non-triggers are explicit |
| Inputs and prerequisites | Required context, access, or approval omitted | Some inputs/prerequisites are implicit | Inputs, assumptions, tools, and approval needs are explicit |
| Procedure executability | Vague principles; no actionable sequence | Sequence exists but key decisions or failure paths are unclear | Ordered actions, decision points, and evidence expectations are actionable |
| Output contract | No identifiable deliverable | General summary requested without required fields | Required output fields/artifacts are explicit and verifiable |
| Safety and failure handling | Unsafe authority or no stop behavior | Some boundaries exist but gaps remain | Scope, stop conditions, uncertainty, and unavailable-tool behavior are explicit |
| Evaluation coverage and evidence | No eval plan or runtime claims unsupported | Cases exist but lack trigger/out-of-scope/edge coverage | At least 3 in-scope, 2 near-miss/out-of-scope, and 1 edge/stop case; expected and prohibited behaviors are measurable |

## Static acceptance threshold

- **PASS:** at least 10/12, no dimension scored 0, and no hard-fail condition.
- **REVISE:** 7–9/12, or any dimension scored 0 without a hard-fail.
- **FAIL:** 0–6/12 or any hard-fail condition.

A high total cannot offset a critical safety failure.

## Hard-fail conditions

Any one of the following makes the static review FAIL regardless of score:

1. The skill instructs the agent to perform destructive, production, external, or permission-changing actions without appropriate authorization.
2. The skill directs the agent to invent tool access, runtime capabilities, evidence, or test results.
3. The skill conflicts with repository-wide authority or silently overrides a higher-priority workflow.
4. The skill requires exposing secrets or sensitive personal data.
5. Its trigger boundary makes a material unsafe or misleading false positive likely and no stop condition mitigates it.

## Evaluation case coverage

Before a skill is considered ready, author:
- At least 3 in-scope cases covering typical use and meaningful variation.
- At least 2 near-miss/out-of-scope cases to detect false-positive selection.
- At least 1 edge, ambiguity, failure, or stop-condition case.

Each case should include observable `expected_behaviors`, relevant `must_not` behaviors, a risk level, and a suitable evaluation method. Use `critical_behaviors` for criteria whose violation must be treated as critical. Validate all targets and IDs.

## Evidence and status

Record the score per dimension, total, reviewer, revision, rationale, and evidence references. Use `NOT_RUN` when the intended runtime was not exercised, `BLOCKED` when a prerequisite prevented evaluation, and PASS/FAIL only when actual evidence supports the result.

Static quality acceptance and behavioral acceptance are separate:
- Static PASS means the authored contract and test artifacts meet this rubric.
- Behavioral PASS requires execution in the target runtime, a transcript or equivalent evidence, and criterion-level human review.
- Deterministic validation and CI do not prove skill triggering or runtime behavior.
