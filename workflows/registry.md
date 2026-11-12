# Workflow Registry and Routing Rules

This file is the routing index for detailed procedures. Linked workflow files remain authoritative; do not duplicate or silently replace their steps here.

## Workflow

1. Classify the request using the task categories below.
2. Assess complexity and risk independently.
3. Select the primary workflow, execution mode, relevant skills, and optional specialist agents.
4. Apply approval gates and define explicit task ownership.
5. Track non-trivial work in the active session; verify and review before reporting completion.

## Task categories

| Category | Typical signals | Primary workflow | Relevant skills | Optional specialist |
|---|---|---|---|---|
| Bug | Existing behavior is broken, inconsistent, or regressed | [Bug Investigation and Fix](bug-fix.md) | `systematic-debugging`, `risk-aware-tdd`, `verification-gate` | `repo_explorer`, then `implementer` and `reviewer` as needed |
| Feature | New user-facing or system capability | [Feature Delivery](feature-delivery.md) | `requirements-clarification`, `implementation-planning`, `change-impact-analysis`, `verification-gate` | `planner`, `implementer`, `reviewer` |
| Database/backend | Schema, persistence, API, authorization, RLS, migrations, data integrity | [Database and Backend Change](database-backend-change.md) | `change-impact-analysis`, `security-review`, `risk-aware-tdd`, `verification-gate` | `repo_explorer`, `security_auditor`, `reviewer` |
| Security | Threat modeling, vulnerability assessment, access control, tenant isolation | [Security Audit](security-audit.md) | `security-review`, `change-impact-analysis` | `security_auditor`, with `reviewer` for independent review |
| Research | Compare technologies, investigate architecture, answer a decision question | [Technical Research and Decision](technical-research.md) | `documentation-and-decisions`, `clear-technical-communication` | `repo_explorer`, `planner` |
| Release | Release candidate, deployment readiness, pre-release verification | [Release Readiness](release-readiness.md) | `verification-gate`, `code-review`, `security-review` | `reviewer`, `security_auditor` when relevant |
| Toolkit | Improve toolkit skills, agents, workflows, evals, schemas, or documentation | Select the most relevant workflow above; use this skill for coordination | `skill-authoring-and-evaluation`, plus relevant planning/review/verification skills | `planner`, `implementer`, `reviewer` |

## Classification rules

1. Follow explicit user intent when clear and safe.
2. Identify security, privacy, data-integrity, production, and irreversible-operation concerns before selecting the primary workflow. These concerns add mandatory gates.
3. Choose one primary category; record secondary categories only when they add real requirements.
4. Persisted data, schema, permissions, APIs, or server-side ownership changes require database/backend analysis.
5. Security assurance requests use the security workflow as primary.
6. Go/no-go release decisions use release readiness as primary.
7. If ambiguity changes procedure materially, ask one focused question; otherwise choose the safer plausible route and state the assumption.

## Complexity assessment

Complexity describes effort and coordination, not potential harm.

- **Simple:** One localized, well-understood, reversible change; few dependencies; obvious acceptance check.
- **Moderate:** Several files or steps, some dependencies, non-trivial behavior, or multiple acceptance checks.
- **Complex:** Cross-cutting architecture, multiple components/roles, significant dependencies, multiple agents, or substantial uncertainty.

## Risk assessment

Risk describes potential impact, reversibility, sensitivity, and blast radius.

- **Low:** Local, reversible, non-sensitive, and unlikely to affect other users or systems.
- **Medium:** Meaningful behavior or data impact, but bounded and recoverable with ordinary safeguards.
- **High:** Sensitive authorization/security path, important data integrity, broad user impact, production configuration, or difficult recovery.
- **Critical:** Potential irreversible loss, severe privacy/security exposure, destructive production operation, or broad service disruption.

When uncertain and plausible impact is high, use the higher plausible risk until evidence reduces uncertainty. A simple production permission change is not a lightweight task.

## Adaptive routing

| Complexity / risk | Route |
|---|---|
| Simple + low | Lightweight path; Codex usually works alone |
| Moderate + low/medium | Selected workflow, explicit scope, acceptance criteria, and proportionate delegation |
| Complex + any risk | Full workflow, dependency-aware plan, explicit owners, handoffs, validation, and independent review |
| Any + high/critical | Strict safety path, read-only discovery first, approval gates, independent review where available |
| Material ambiguity | `NEEDS_CLARIFICATION`; do not guess |

Risk overrides complexity.

## Routing precedence

Apply in this order:

1. Explicit user intent and approved scope.
2. Safety, privacy, authorization, data-integrity, and production-risk overrides.
3. Primary task classification.
4. Primary workflow selection.
5. Execution mode and relevant skills/agent delegation.
6. Proportionate approval, validation, independent review, and reporting.

A higher-priority rule cannot be bypassed by a lower-priority routing choice.

## Delegation decision rules

### Work alone
Codex should work alone for trivial/localized work, tightly coupled edits, work with no useful specialist fit, or when delegation overhead exceeds likely benefit.

### Delegate
Delegate when an existing specialist provides a material advantage and the assignment can be bounded with a verifiable deliverable.

### Parallel vs sequential
Parallelize independent read-only investigations or disjoint tasks with non-overlapping write ownership. Sequence dependent work, shared-file edits, planning before implementation, and implementation before independent review. Never run concurrent edits against the same file set.

### Routing matrix

| Agent | Use when | Allowed output | Boundary |
|---|---|---|---|
| `repo_explorer` | Architecture, call paths, evidence, unknowns | Read-only findings | No implementation |
| `planner` | Multi-step change needs options and acceptance criteria | Bounded plan | No implementation |
| `implementer` | User-approved plan is ready | Scoped code/docs/tests | No scope expansion or unapproved side effects |
| `reviewer` | Independent quality review is useful/required | Read-only findings and recommendation | No implementation |
| `security_auditor` | Trust boundaries, auth, data exposure, security controls | Defensive read-only assessment | No exploitative actions |

Codex remains the primary coordinator and is accountable for the final result. Agent definitions do not create isolation or override parent sandbox/tool permissions.

## Handoff contract

Use `templates/agent-handoff.md` for non-trivial assignments. Include objective, recipient, scope, non-goals, context/evidence, assumptions, exact approval status, constraints, expected output, dependencies, and parallelization status. One owner per task. The parent validates all outputs and remains accountable.

## Coordination and conflict resolution

Track delegated task state and evidence in the active session. Compare conflicting claims against exact source evidence, reproducible scenarios, tests, and agreed scope—not agent seniority. Request focused re-checks where needed. If disagreement remains, preserve both findings as unresolved; Codex makes the final engineering recommendation and escalates material product/scope decisions to the user.

## Independent review

For complex, security-sensitive, or high-impact changes, use a reviewer who did not implement the change whenever available. Supply the approved criteria and revision, not a desired verdict. Use `templates/agent-review-report.md`; report severity, status, location, scenario, evidence, impact, remediation, and verification. A clean review is scoped, not universal assurance.

## State tracking

Use the active Codex session. The orchestration skill defines state names and transitions. Session state is not persistent. Use `templates/workflow-brief.md` for complex tasks or meaningful handoffs.

## Completion standard

A workflow is complete only when approved scope and acceptance criteria are addressed, required checks and review have evidence-backed outcomes, failures/skips/unrun checks are disclosed, risks are stated, and no unapproved action was taken. Otherwise report partial, blocked, or failed.

## Stop conditions

Stop for material ambiguity; unapproved destructive, production, permission, deployment, or external side effects; unavailable required evidence; or an unsafe boundary.

## Required output

- Primary category and selected workflow.
- Complexity/risk and rationale.
- Execution mode and agent assignments, where applicable.
- Scope, approval, current state, and blockers.
- Verification and review evidence with unresolved limitations.
