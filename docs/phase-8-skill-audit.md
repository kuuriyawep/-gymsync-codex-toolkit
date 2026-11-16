# Phase 8 — Skill Quality Audit

**Status:** Static audit and remediation complete; latest deterministic CI passed; Codex behavioral evaluation remains pending  
**Branch:** `main`  
**Scope:** 13 canonical skills under `.agents/skills/`, checked against `AGENTS.md` and `workflows/registry.md`  
**Method:** Read-only content review  
**Runtime status:** `NOT_RUN — CODEX_REQUIRED`

## Executive summary

The toolkit has a coherent foundation: repository-wide authority is defined in `AGENTS.md`, routing is centralized in `workflows/registry.md`, and most skills emphasize evidence, scope control, and honest verification.

The main quality gap is not missing subject coverage. It is inconsistent operational specificity across skills: trigger boundaries, prerequisites, expected deliverables, stop/failure behavior, and handoff points are not equally explicit.

The highest-value next step is to clarify boundaries and interfaces between overlapping skills before adding more skills.

## Skill-by-skill findings

| Skill | Static assessment | Improvement priority |
|---|---|---|
| `change-impact-analysis` | Strong concise impact-analysis sequence; asks for evidence and unknowns. Expected report structure and explicit stop conditions are implicit. | Medium |
| `clear-technical-communication` | Useful cross-cutting communication guidance. Trigger and output contract are broad and may be difficult to evaluate consistently. | Low |
| `code-review` | Good review ordering and finding fields. Could define confidence/evidence standards and distinguish confirmed defects from hypotheses. | Medium |
| `documentation-and-decisions` | Good traceability and anti-drift rules. A minimal decision-record output contract would improve consistency. | Medium |
| `implementation-planning` | Clear scope, dependency, risk, approval, and rollback concerns. Could define a compact required plan structure and completion criteria. | Medium |
| `project-intelligence` | Strongest evidence and memory governance. Clear source-of-truth hierarchy, freshness labels, and privacy boundary. | Low |
| `requirements-clarification` | Good one-question-at-a-time and no-scope-invention rules. Could define when to proceed with stated assumptions versus stop for clarification. | Medium |
| `risk-aware-tdd` | Good behavior-first sequence and risk-proportionate tests. Its boundary with debugging and verification needs sharper wording; test-first may not be practical in every repository. | High |
| `security-review` | Good defensive scope and authentication/authorization distinction. Could standardize evidence, confidence, severity rationale, and safe test boundaries. | Medium |
| `skill-authoring-and-evaluation` | Correctly emphasizes triggers, representative prompts, out-of-scope tests, and no false evaluation claims. Needs a measurable rubric and explicit eval artifact contract. | High |
| `systematic-debugging` | Strong causal investigation and reproduction discipline. Its overlap with TDD should be clarified: diagnosis first, regression test/fix after root cause. | High |
| `verification-gate` | Good evidence-based final reporting. It should remain the final cross-workflow gate, not duplicate implementation/TDD procedures. | High |
| `workflow-orchestration` | Comprehensive coordinator contract and clear approval/delegation boundaries. Some concepts repeat `AGENTS.md` and registry content; preserve authority while reducing procedural duplication. | High |

## Cross-skill findings

### 1. Boundary overlap

- `systematic-debugging` owns symptom capture, reproduction, causal tracing, and root-cause hypothesis.
- `risk-aware-tdd` owns behavior-first regression testing and implementation validation.
- `verification-gate` owns final acceptance evidence and honest status reporting.

These roles are compatible but should be stated explicitly in all three skills and the registry.

### 2. Uneven skill contracts

Some skills define detailed workflows while others are short principles. Across the set, the following contract elements are inconsistent:

- Trigger and non-trigger conditions.
- Required inputs and prerequisites.
- Expected output/deliverable.
- Stop conditions and failure handling.
- Evidence and uncertainty labels.
- Handoff to another skill or workflow.

Not every skill needs a long document. Each should, however, make these elements clear enough for a Codex session to apply it reliably.

### 3. Evaluation quality

`skill-authoring-and-evaluation` correctly requires representative, edge, and out-of-scope prompts. The next revision should define measurable scoring criteria and preserve test cases as eval artifacts. Static validators and CI do not establish real Codex behavior.

### 4. Authority and duplication

`AGENTS.md` defines repository-wide rules; `workflows/registry.md` routes tasks; detailed workflow files own procedures; skills provide specialist procedures. `workflow-orchestration` should point to these sources rather than becoming a second copy of them.

## Recommended remediation order

1. Clarify the boundary contract for debugging, TDD, and verification.
2. Strengthen the authoring/evaluation skill with a measurable rubric and explicit eval outputs.
3. Standardize a lightweight skill contract: trigger, non-goals, prerequisites, procedure, output, stop/failure behavior.
4. Improve review and security evidence/confidence reporting.
5. Tighten planning, requirements, impact-analysis, and decision-record outputs.
6. Review orchestration for duplication against `AGENTS.md` and the registry.
7. Re-check native/portable parity and run repository quality gates after approved edits.

## Verification and limitations

- 13 canonical skill files were retrieved from `.agents/skills/` on `main`.
- `AGENTS.md` and `workflows/registry.md` were reviewed as governing context.
- This report is a static review, not a Codex behavioral evaluation.
- No skill files were modified as part of this audit.
- No GymSync application files were accessed or changed.
- Codex behavioral tests remain `NOT_RUN — CODEX_REQUIRED`.
- The safe selective-adoption trial remains pending.

## Remediation outcome

The audit recommendations were applied across all 13 canonical skills and their portable mirrors. The highest-priority debugging/TDD/verification boundary was made explicit; the skill-authoring/evaluation contract now includes a measurable static rubric and required evaluation-case mix; remaining skills received proportionate trigger, input, output, evidence, safety, and stop-condition improvements; and workflow orchestration now defers routing authority to the registry rather than duplicating it.

See [Phase 8 Completion Report](phase-8-completion-report.md) for the exact changed areas and verification status.

## Exit status

Static remediation and deterministic verification are complete. The latest main-branch CI run (#109, commit `fb7967a4ce7b54a6a4731b92af221f8833be9e2c`) passed: 38 unit tests passed, all 41 evaluation cases validated, and the toolkit quality pipeline completed with zero warnings. Phase 8 is not behaviorally complete: the prepared scenarios still require execution in a trusted Codex session. Codex runtime evaluation remains `NOT_RUN — CODEX_REQUIRED`.
