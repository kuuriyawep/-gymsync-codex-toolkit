---
name: risk-aware-tdd
description: Implement an approved behavior change using focused regression or acceptance tests first where practical, with test depth proportionate to risk and repository conventions.
---
# Risk-Aware TDD

## When to use
Use when implementing a bug fix or behavior change that can be expressed as observable expected behavior and tested in the repository.

For diagnosis of an unknown defect, use `systematic-debugging` first. For final acceptance evidence across all changed surfaces, use `verification-gate`.

## Inputs and prerequisites
- Approved scope and expected behavior or acceptance criteria.
- Relevant diagnosis/root-cause findings for a bug fix, when available.
- Existing test framework, scripts, fixtures, and project conventions.
- Known risk areas, especially authentication, authorization, payments, tenant isolation, and persisted data.

If expected behavior or approval is materially unclear, stop and request clarification/approval rather than inventing requirements.

## Procedure
1. Inspect the existing test framework, scripts, fixtures, conventions, and current baseline. Do not introduce a new framework without approval.
2. Translate the approved behavior into focused test cases, including relevant edge and failure paths.
3. Add a test that demonstrates the missing or incorrect behavior and confirm it fails for the intended reason, where practical.
4. If a failing test cannot reasonably be written first (for example, a UI/manual-only behavior or unavailable test harness), state why and define an alternative reproducible check before implementation.
5. Implement the smallest change within the approved scope. Do not broaden requirements or refactor unrelated code.
6. Run the focused test and inspect failures. Fix the cause rather than weakening assertions to obtain a pass.
7. Refactor only when behavior remains covered and checks stay green.
8. Increase test depth with risk. For high-risk auth, payment, tenant, or data changes, cover unauthorized, invalid, duplicate, boundary, and failure paths as applicable.
9. Hand the completed change and exact test evidence to `verification-gate` for final cross-surface verification.

## Required output
- **Approved behavior:** scope and acceptance criteria implemented.
- **Tests:** cases added/changed and why they cover the behavior.
- **Test-first evidence:** pre-fix failure and post-fix result, when practical; otherwise the reason test-first was not feasible.
- **Implementation:** concise summary and changed paths.
- **Execution record:** exact commands/checks and actual outcomes.
- **Exceptions:** deviations from test-first, tests not run, and reasons.
- **Residual risk:** unresolved issues and follow-up verification.

## Handoff to verification
Provide the approved criteria, changed paths, regression/acceptance tests, pre-fix and post-fix evidence where available, exact commands and outcomes, deviations, unrun checks, and remaining risks. This is implementation evidence, not a release verdict; the final acceptance decision belongs to `verification-gate`.

## Boundaries and stop conditions
- TDD owns focused behavior tests and implementation validation; it does not replace root-cause diagnosis or the final verification gate.
- Do not impose arbitrary coverage thresholds or add unrelated tests.
- Do not modify production data, deploy, alter permissions, or perform destructive actions without explicit approval.
- If the baseline is broken, the test environment is unavailable, or a failure is unrelated, report it separately; do not mislabel it as a regression caused by the change.
- Never claim a test passed unless it was actually run.
