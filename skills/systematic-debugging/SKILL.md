---
name: systematic-debugging
description: Diagnose an existing defect by reproducing it safely, tracing the failing behavior to its earliest incorrect cause, and producing evidence-backed root-cause findings before implementation.
---
# Systematic Debugging

## When to use
Use when existing behavior is broken, inconsistent, or regressed and the cause is not already established.

Do not use as the primary procedure for a new feature, routine code review, or final release verification. For a known cause and an approved fix, use the implementation and testing procedure directly.

## Inputs
- Expected and actual behavior, if known.
- Environment, affected roles/data, and reproduction steps, if available.
- Relevant project instructions, source, logs, and existing tests.

Inspect available context before asking the user to repeat information. Ask one focused question only when a missing fact materially blocks safe diagnosis.

## Procedure
1. Capture the exact symptom, expected behavior, actual behavior, environment, scope, and reproduction steps. Mark unavailable details as unknown.
2. Read repository instructions and inspect the narrowest relevant code path, tests, logs, and recent changes.
3. Reproduce the issue where safe. Record the exact setup and observed result. If reproduction is unsafe or impossible, state that limitation.
4. Trace inputs, state transitions, persistence, APIs, permissions, and outputs. Locate the earliest incorrect transition supported by evidence.
5. Form a falsifiable root-cause hypothesis. Record supporting evidence, plausible alternatives, and what observation would disprove the hypothesis.
6. Distinguish confirmed root cause from likely cause and unresolved hypothesis. Do not treat correlation, a suspicious line, or an agent opinion as proof.
7. Recommend the smallest plausible correction and the regression behavior that should be tested. Hand implementation to the approved workflow or implementer; this skill does not itself authorize code changes.
8. If new evidence changes scope or risk, stop and route through the applicable clarification and approval gates.

## Required output
- Symptom: expected vs actual behavior.
- Reproduction: steps and observed result, or why it was not reproduced.
- Investigation scope: relevant paths, tests, logs, and evidence inspected.
- Root cause: confirmed, likely, or unresolved, with evidence.
- Alternatives considered and remaining unknowns.
- Proposed minimal correction and regression-test scenario.
- Risks, blockers, and recommended next owner/step.

## Boundaries and stop conditions
- Diagnosis owns reproduction and causal analysis; it does not own implementation or final acceptance verification.
- Do not edit files, change data/configuration, or run destructive/live actions as part of diagnosis unless separately authorized under the applicable workflow.
- Stop before risky side effects, scope expansion, or actions with unclear ownership.
- Never invent reproduction, logs, source evidence, or test outcomes.
