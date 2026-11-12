---
name: systematic-debugging
description: Investigate bugs through evidence, reproduction, causal tracing, and regression tests before changing code.
---
# Systematic Debugging
1. Capture the exact symptom, expected behavior, actual behavior, environment, and reproduction steps.
2. Read project instructions and inspect the narrowest relevant code path.
3. Reproduce the issue where safe; record logs and failing tests.
4. Trace inputs, state transitions, persistence, and outputs. Identify the first incorrect transition.
5. Form a falsifiable root-cause hypothesis and test it.
6. Propose the smallest fix; obtain approval if scope or risk changes.
7. Add a regression test that fails before the fix.
8. Implement, run targeted tests, then relevant broader checks.
9. Report root cause, evidence, changed files, verification, and unresolved uncertainty.
Do not guess, patch symptoms blindly, or claim an unrun test passed.