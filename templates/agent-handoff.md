# Agent Handoff Contract

Use this contract whenever Codex delegates a non-trivial task. Keep the handoff concise, concrete, and bounded. A handoff is task context, not a permission grant or a separate security boundary.

## Required fields

- **Handoff ID / task:** Short identifier and one-sentence objective.
- **Recipient:** Existing project agent name and why its specialty is relevant.
- **Objective:** Observable outcome expected from this assignment.
- **In scope:** Exact files, components, questions, or checks the agent owns.
- **Out of scope:** Explicit exclusions and work reserved for the parent coordinator.
- **Context and evidence:** Relevant paths, symbols, decisions, links, and confirmed facts.
- **Assumptions / unknowns:** Clearly label anything not yet verified.
- **Approval status:** State the exact user-approved scope and any actions that remain unapproved.
- **Constraints:** Read/write boundary, tools, safety rules, time/order dependencies, and no-go actions.
- **Expected output:** Required format, evidence, severity/risk labels, and completion criteria.
- **Dependencies:** Inputs required, upstream tasks, and whether parallel work is safe.

## Handoff rules

1. Assign one accountable owner per task. The parent Codex session remains accountable for the overall result.
2. Delegate only work that materially benefits from a specialist; do not delegate trivial work for ceremony.
3. Give agents the minimum relevant context needed to perform the assignment.
4. Do not assign overlapping write scopes to concurrent agents. Parallelize independent read-only work freely when useful.
5. Sequence tasks when one depends on another agent's output or when edits touch shared files.
6. Approval status must never be inferred from a handoff. An agent may implement only the exact approved scope.
7. Agent instructions do not create isolation or elevate permissions. The parent session's sandbox, tools, and approval settings remain authoritative.
8. If scope, ownership, approval, or a safety boundary is unclear, the agent must stop and report the blocker rather than guess.

## Required response from the agent

- **Outcome:** completed | partial | blocked | failed
- **Work performed:** concise summary; identify any files changed.
- **Findings / decisions:** actionable results, separated from assumptions.
- **Evidence:** exact paths, symbols, line references, commands, and outputs where available.
- **Checks:** passed | failed | skipped | not run, with evidence.
- **Risks / unknowns:** unresolved concerns and limitations.
- **Handoff back:** next action for the parent coordinator; identify any approval needed.

## Parent coordinator close-out

The parent validates the response against the assignment, checks scope and evidence, resolves dependencies/conflicts, and decides whether to accept, request revision, or stop. A delegated task is not complete merely because the agent says it is complete.
