---
name: code-review
description: Perform an independent, evidence-based review for correctness, specification compliance, security regressions, and unintended changes.
---
# Code Review

## When to use
Use to assess a proposed or completed code change against its specification, risk, and existing behavior. Review is read-only; implementation belongs to the designated implementer.

## Inputs
- Approved scope and acceptance criteria.
- Diff or exact revision under review.
- Relevant project instructions, surrounding code, and test evidence.

## Review procedure
1. Confirm the revision and approved scope. Inspect the complete diff before judging individual lines.
2. Review in this order: specification/acceptance compliance; correctness and edge cases; error handling and data integrity; authentication, authorization, tenant isolation, and secrets; compatibility, performance, and regression risk; tests and maintainability.
3. Trace each suspected defect to an exact changed line and a concrete triggering scenario.
4. Separate confirmed defects from hypotheses, questions, and style preferences. Do not report speculative concerns as proven bugs.
5. Check whether tests exercise the changed behavior and meaningful failure paths. Do not treat test presence as proof of correctness.
6. Recheck findings against current source and remove duplicates or findings already disproven by evidence.

## Required finding format
- **Severity:** Critical / High / Medium / Low.
- **Confidence:** Confirmed / Likely / Unverified.
- **Location:** file and line/symbol.
- **Scenario:** exact preconditions or input that triggers the issue.
- **Evidence:** source, test, trace, or reproducible observation.
- **Impact:** concrete consequence and affected boundary.
- **Recommendation:** smallest appropriate correction.
- **Verification:** test or check that would confirm the correction.

## Stop conditions
If the diff, approved scope, or relevant context is unavailable, report the limitation instead of guessing. Do not edit code, alter data, run destructive tests, or broaden the review beyond the requested scope.
