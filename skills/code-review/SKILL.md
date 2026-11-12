---
name: code-review
description: Perform an evidence-based review for correctness, specification compliance, and regressions.
---
# Code Review
Review in this order:
1. Spec and acceptance-criteria compliance.
2. Correctness, edge cases, error handling, and data integrity.
3. Auth, authorization, tenant isolation, and secret handling.
4. Regression risk, API/schema compatibility, and performance.
5. Test coverage and maintainability.
Findings must include severity, exact location, triggering scenario, impact, and suggested fix. Prioritize defects over style. Do not edit code during review.