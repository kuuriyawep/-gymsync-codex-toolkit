---
name: documentation-and-decisions
description: Keep project documentation and engineering decision records concise, traceable, and aligned with implemented behavior.
---
# Documentation and Decisions

## When to use
Use when a change affects architecture, data, security, dependencies, operations, interfaces, or future maintenance; when recording a material engineering choice; or when existing documentation becomes misleading.

## Procedure
1. Identify the reader, purpose, source of truth, and documentation scope.
2. Verify current behavior against source, tests, schemas, configuration, and explicit decisions. Mark planned or unverified behavior clearly.
3. Update the smallest relevant document; prefer links to authoritative detail over copying large sections.
4. For a material decision, record the context/problem, decision, alternatives considered, consequences/trade-offs, status, and date/revision when known.
5. Link evidence and related implementation changes. Keep superseded decisions discoverable and mark them as superseded rather than silently deleting history.
6. Review terminology, examples, commands, and links for accuracy.

## Required output
For a documentation update, report changed paths and the source evidence used. For a decision record, include:
- **Context:** problem and constraints.
- **Decision:** selected option and rationale.
- **Alternatives:** meaningful options rejected and why.
- **Consequences:** benefits, costs, risks, and follow-up.
- **Status/date:** proposed, accepted, superseded, or deprecated; date/revision if known.

## Stop conditions
Do not document assumptions as shipped behavior or infer an approval from discussion. If source and docs conflict, identify the discrepancy and resolve it with the owner before presenting either as authoritative. Avoid duplicating code or creating documentation without a clear maintenance owner.
