---
name: requirements-clarification
description: Resolve material ambiguity and define observable acceptance criteria before planning or implementing a change.
---
# Requirements Clarification

## When to use
Use when a request has multiple plausible interpretations, missing behavior rules, unclear ownership, or acceptance criteria that could change implementation. Do not force clarification when the intent is already clear and missing details can safely remain assumptions.

## Procedure
1. Inspect available conversation, project instructions, existing behavior, specifications, and relevant source before asking the user to repeat information.
2. Separate the user's goal, explicit constraints, non-goals, assumptions, and decisions already made.
3. Identify unknowns and determine whether each one materially changes correctness, risk, scope, or cost.
4. Ask one focused question at a time, prioritizing the unknown with the greatest effect on the solution.
5. If uncertainty is low-impact and a safe default is supported by evidence, state the assumption and proceed without blocking.
6. Translate confirmed requirements into observable acceptance criteria and relevant edge cases.
7. Identify roles, permissions, data ownership, failure states, migration needs, and operational constraints where relevant.

## Required output
- Goal and intended outcome.
- In-scope and out-of-scope behavior.
- Confirmed constraints and evidence-backed assumptions.
- Observable acceptance criteria and important edge cases.
- Unresolved decisions, each marked as blocking or non-blocking.

## Proceed vs stop
Proceed when remaining unknowns do not materially alter the solution and assumptions can be stated safely. Stop for clarification when an unknown changes business rules, data integrity, authorization, user-visible behavior, irreversible action, or approval scope.

## Boundaries
Do not invent requirements, ask a long list of questions at once, or expand scope under the guise of clarification.
