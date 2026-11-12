---
name: risk-aware-tdd
description: Apply behavior-first testing proportionate to change risk and the repository's existing test conventions.
---
# Risk-Aware TDD
1. Inspect test framework, scripts, fixtures, and current baseline.
2. Define observable behavior and edge cases.
3. Add a focused failing test where practical.
4. Implement the minimum change to satisfy it.
5. Refactor only while tests remain green.
6. Run targeted tests, then relevant integration/build/type checks.
7. For high-risk auth, payment, tenant, or data changes, test unauthorized, invalid, duplicate, boundary, and failure paths.
Do not impose arbitrary coverage thresholds. Report tests not run and why.