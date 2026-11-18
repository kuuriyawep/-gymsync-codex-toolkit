# Agent Result

Use this structure when returning a completed, partial, blocked, or failed handoff. Keep evidence references exact and report every check honestly.

- **Handoff ID:**
- **Agent:**
- **Outcome:** complete | partial | blocked | failed
- **Summary:**

## Work performed
- Description:
- Evidence references:

## Findings
For each finding:
- Title:
- Severity: critical | high | medium | low | info
- Status: confirmed | likely | question | informational
- Location:
- Evidence references:
- Impact:
- Remediation:

## Changed files
List exact repository-relative paths. Read-only roles must return an empty list. Implementer changes must remain inside the handoff's approved write scope.

## Checks
For each check:
- Name:
- Status: passed | failed | skipped | not_run
- Evidence references:

A passed check requires evidence references. Never claim an unrun check passed.

## Risks and unknowns
- Remaining risks:
- Unknowns:
- Limitations:

## Next action
- Parent coordinator action:
- Approval needed: true | false

The structured result must validate against `schemas/agent-result.schema.json`. The parent coordinator independently validates the result against the original handoff and actual diff.
