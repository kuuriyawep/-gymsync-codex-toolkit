---
name: change-impact-analysis
description: Map the blast radius and trust boundaries of a proposed code, schema, or configuration change.
---
# Change Impact Analysis
Default to read-only.
1. Locate entry points, callers, shared components, schemas, APIs, jobs, and tests.
2. Trace affected data and control flows.
3. Identify role/tenant boundaries, security controls, and external integrations.
4. Check compatibility, existing records, migrations, rollback, and deployment ordering.
5. List likely regressions and missing tests.
6. Recommend the smallest safe change and verification plan.
Cite repository evidence; label unknowns. Do not edit files.