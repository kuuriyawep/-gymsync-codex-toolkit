---
name: verification-gate
description: Verify delivered work with reproducible checks and honest reporting before claiming completion.
---
# Verification Gate
- Derive checks from acceptance criteria and changed surfaces.
- Run the narrowest relevant tests first, then broader tests/build/type/lint checks as appropriate.
- Inspect diffs for unintended changes, secrets, generated files, and scope creep.
- Verify migrations and configuration are consistent without applying production changes unless approved.
- Record exact commands and outcomes.
- Separate passed, failed, skipped, and not-run checks.
Never claim success based only on code inspection or an expected result.