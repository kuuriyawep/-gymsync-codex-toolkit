# Workflow Registry and Routing Rules

This file is the routing index for the detailed procedures in this directory. The linked workflow files remain authoritative; do not duplicate or silently replace their steps here.

## Workflow

1. Classify the request using the task categories below.
2. Assess complexity and risk independently.
3. Select the primary workflow and relevant skills/agents.
4. Apply the adaptive routing matrix and required approval gates.
5. Track non-trivial work in the active session and verify before reporting completion.

## Task categories

| Category | Typical signals | Primary workflow | Relevant skills | Optional specialist |
|---|---|---|---|---|
| Bug | Existing behavior is broken, inconsistent, or regressed | [Bug Investigation and Fix](bug-fix.md) | `systematic-debugging`, `risk-aware-tdd`, `verification-gate` | `repo_explorer`, then `implementer` and `reviewer` as needed |
| Feature | New user-facing or system capability | [Feature Delivery](feature-delivery.md) | `requirements-clarification`, `implementation-planning`, `change-impact-analysis`, `verification-gate` | `planner`, `implementer`, `reviewer` |
| Database/backend | Schema, persistence, API, authorization, RLS, migrations, data integrity | [Database and Backend Change](database-backend-change.md) | `change-impact-analysis`, `security-review`, `risk-aware-tdd`, `verification-gate` | `repo_explorer`, `security_auditor`, `reviewer` |
| Security | Threat modeling, vulnerability assessment, access control, tenant isolation | [Security Audit](security-audit.md) | `security-review`, `change-impact-analysis` | `security_auditor`, with `reviewer` for independent review |
| Research | Compare technologies, investigate architecture, answer a decision question | [Technical Research and Decision](technical-research.md) | `documentation-and-decisions`, `clear-technical-communication` | `repo_explorer`, `planner` |
| Release | Release candidate, deployment readiness, pre-release verification | [Release Readiness](release-readiness.md) | `verification-gate`, `code-review`, `security-review` | `reviewer`, `security_auditor` when relevant |
| Toolkit | Improve this toolkit's skills, agents, workflows, evals, schemas, or documentation | Select the most relevant workflow above; use this skill for coordination | `skill-authoring-and-evaluation`, plus relevant planning/review/verification skills | `planner`, `implementer`, `reviewer` |

## Classification rules

1. Follow explicit user intent when it is clear and safe.
2. Identify security, privacy, data-integrity, production, and irreversible-operation concerns before selecting the primary workflow. These concerns add mandatory gates even when another category is primary.
3. Choose one primary category based on the task's principal outcome. Record secondary categories when they add real requirements.
4. If the task changes persisted data, schema, permissions, APIs, or server-side ownership, include database/backend analysis even if the request is phrased as a feature or bug.
5. If the task's main purpose is to assess risk or prove/disprove a security property, use the security workflow as primary.
6. If the task's main purpose is a go/no-go release decision, use release readiness as primary.
7. If classification remains ambiguous and the distinction changes the procedure materially, ask one focused question. Otherwise choose the safer plausible route and state the assumption.

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

When risk is uncertain and the plausible impact is high, use the higher plausible risk until evidence reduces uncertainty.

## Adaptive routing matrix

| Complexity and risk | Route |
|---|---|
| Simple + low | Lightweight path: focused discovery, bounded action, proportionate verification, concise report |
| Moderate + low/medium | Selected workflow with explicit scope, acceptance criteria, plan, and verification |
| Complex + any risk | Full selected workflow, dependency-aware plan, session state tracking, and review |
| Any complexity + high/critical | Strict safety path: read-only discovery first, explicit risk analysis, approval before gated action, independent review where available |
| Any combination with material ambiguity | `NEEDS_CLARIFICATION`; do not guess a safety- or behavior-critical requirement |

Risk overrides complexity. A simple production permission change is not a lightweight task.

## Routing precedence

Apply in this order:

1. Explicit user intent and approved scope.
2. Safety, privacy, authorization, data-integrity, and production-risk overrides.
3. Primary task classification.
4. Primary workflow selection.
5. Relevant skills and optional agent delegation.
6. Proportionate approval, validation, review, and reporting.

A higher-priority rule cannot be bypassed by a lower-priority routing choice.

## Agent boundaries

| Agent | Allowed responsibility | Boundary |
|---|---|---|
| `repo_explorer` | Read-only discovery and evidence | No implementation |
| `planner` | Requirements, risks, options, sequence, acceptance criteria | No implementation |
| `implementer` | Approved implementation | No scope expansion or unapproved side effects |
| `reviewer` | Independent correctness, regression, maintainability, and security review | Review findings; do not silently rewrite scope |
| `security_auditor` | Threat modeling and security findings | No exploitative actions |

Codex remains the primary coordinator. Delegate only when useful. Parallel work must be independent; avoid overlapping concurrent writes. Subagents inherit the parent session's sandbox and approval settings.

## State tracking

Use the active Codex session for task state. The orchestration skill defines state names and transition rules. Do not represent session state as durable across sessions. Use `templates/workflow-brief.md` for complex tasks or explicit handoffs; otherwise a concise session summary is sufficient.

## Completion standard

A workflow is complete only when:
- The approved scope and acceptance criteria have been addressed.
- Required checks and reviews have evidence-backed outcomes.
- Failed, skipped, and unrun checks are disclosed.
- Remaining risks, blockers, and limitations are stated.
- No unapproved action was taken.

If any required condition is unmet, report the task as partial, blocked, or failed rather than verified complete.


## Stop conditions

- Stop for material ambiguity that changes task routing, expected behavior, or safety.
- Stop before any unapproved destructive, production, permission, deployment, or external side effect.
- Stop when the selected workflow or required evidence is unavailable; report the limitation rather than bypassing the gate.

## Required output

- Primary category and selected workflow.
- Complexity and risk with concise rationale.
- Relevant skills/agents and approval requirements.
- Current session state, blockers, and next action for non-trivial work.
- Verification outcome and unresolved limitations at completion.
