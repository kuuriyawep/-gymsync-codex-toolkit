---
name: skill-authoring-and-evaluation
description: Design, review, and evaluate portable Codex skills using explicit trigger boundaries, executable procedures, measurable quality criteria, and evidence-backed evaluation cases.
---
# Skill Authoring and Evaluation

## When to use
Use when creating, materially revising, auditing, or evaluating a reusable skill for Codex or a documented portable skill catalog.

Do not use for ordinary project documentation, one-off prompts, agent role definitions, or workflow procedures unless the requested artifact is explicitly a skill. Do not assume a skill can invoke tools or capabilities unavailable in its target environment.

## Required skill contract
Every skill must define, at a level proportionate to its risk and complexity:

1. **Identity:** valid frontmatter `name` and concise, action-oriented `description` that helps Codex select the skill.
2. **Trigger boundary:** when to use it and important non-triggers / out-of-scope tasks.
3. **Inputs and prerequisites:** required context, approvals, access, tools, and assumptions.
4. **Procedure:** ordered, actionable steps with clear decision points; avoid vague verbs such as "handle appropriately" without an observable action.
5. **Output contract:** required deliverable fields or artifacts, not merely "provide a summary".
6. **Safety and failure handling:** boundaries, stop conditions, uncertainty handling, and what to do when prerequisites or tools are unavailable.
7. **Handoffs:** identify the next owner or authoritative workflow where the skill is one phase of a larger process. Avoid duplicating another skill's ownership.

Keep the file concise. Omit sections that genuinely do not apply, but make the behavior explicit rather than relying on inference.

## Authoring procedure
1. Identify the target runtime, user, task, trigger phrases, non-goals, and capabilities actually available.
2. Inspect repository-wide instructions, existing workflows, related skills, and naming conventions. Reuse existing procedures; do not create overlapping skills without a demonstrated gap.
3. Define the skill's unique responsibility and boundaries against adjacent skills/workflows.
4. Draft the skill contract above. Use concrete actions, evidence requirements, and decision/stop conditions.
5. Design evaluation cases before declaring the skill ready:
   - At least 3 representative in-scope prompts across typical use and meaningful variation.
   - At least 2 near-miss or out-of-scope prompts to test false-positive triggering.
   - At least 1 edge, ambiguity, failure, or stop-condition prompt.
   - Each case must state observable expected behaviors and prohibited behaviors; mark critical behaviors explicitly where safety or integrity is at stake.
6. Score the skill using `evals/rubrics/skill-quality.md`. A static review is not a behavioral test.
7. Validate case JSON, target references, unique IDs, native/portable parity, and repository quality gates. Preserve cases as versioned eval artifacts.
8. When the target runtime is available, run the cases in a trusted Codex session, capture transcript and supporting artifacts, grade each criterion, and revise only against observed failures.

## Measurable quality gate
Use the six dimensions in `evals/rubrics/skill-quality.md`, each scored 0–2:
- Trigger and scope boundary.
- Inputs and prerequisites.
- Procedure executability.
- Output contract.
- Safety and failure handling.
- Evaluation coverage and evidence discipline.

A skill passes static quality review only when it scores at least 10/12, has no dimension scored 0, and triggers no hard-fail condition in the rubric. Record the score and evidence; do not infer a score from file length or stylistic preference.

Runtime behavioral status remains `NOT_RUN` until the skill is exercised in its intended environment and transcript/evidence is reviewed. Static PASS, JSON validation, or CI success does not establish runtime behavior.

## Required output
For a new or revised skill, report:
- Target runtime and intended task.
- Trigger phrases and non-trigger boundary.
- Related skills/workflows and unique ownership.
- Contract review against the seven required elements.
- Quality score by dimension, total /12, and evidence.
- Evaluation cases created or changed, including in-scope and out-of-scope coverage.
- Deterministic checks actually run and outcomes.
- Runtime status: PASS / FAIL / BLOCKED / NOT_RUN, with evidence or reason.
- Remaining gaps and recommended next action.

## Stop conditions
Stop and clarify if target runtime or intended skill behavior materially changes the design. Do not invent tool commands, permissions, APIs, or model capabilities. Stop before introducing a new dependency, framework, external service, or agent runtime without approval. If no behavioral runtime is available, prepare evals and mark runtime evaluation `NOT_RUN`; never claim it passed.

## Evaluation honesty
- A case file is a test specification, not a test result.
- A deterministic validator proves only the artifact properties it checks.
- Behavioral PASS requires an actual target-runtime session and reviewable evidence.
- Never fabricate transcripts, outputs, command results, or scores.
