---
name: security-review
description: Conduct a defensive application security review across identity, data, APIs, dependencies, and deployment boundaries.
---
# Security Review
- Identify assets, actors, trust boundaries, and attack surfaces.
- Check authentication separately from authorization.
- Verify server-side role and tenant checks; never trust client-only gates.
- Inspect input validation, injection, secrets, logs, storage, rate limits, dependencies, and error leakage.
- For databases, inspect row-level security, grants, service-role usage, and migration safety.
- Rank findings Critical/High/Medium/Low with evidence, impact, remediation, and verification.
Read-only by default; obtain approval before changing controls or testing live targets.