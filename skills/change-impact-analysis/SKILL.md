---
name: change-impact-analysis
description: Map the blast radius, dependencies, data flows, and trust boundaries of a proposed code, schema, or configuration change before implementation.
---
# Change Impact Analysis

## When to use
Use before a non-trivial change that may affect multiple modules, persisted data, APIs, configuration, roles, tenants, or external integrations. Do not use for routine explanations or as a substitute for implementation planning.

## Procedure
1. Default to read-only. Confirm the proposed change, intended behavior, scope, and known constraints.
2. Locate entry points, callers, shared components, schemas, APIs, jobs, configuration, and relevant tests.
3. Trace affected data and control flows from input through authorization, processing, persistence, and output.
4. Identify role/tenant boundaries, trust boundaries, security controls, and external integrations.
5. Check compatibility, existing records, migrations/backfills, deployment ordering, rollback, and operational dependencies.
6. Identify likely regressions, failure modes, missing tests, and unknowns.
7. Recommend the smallest safe implementation boundary and a verification plan. Do not implement the change.

## Required output
- Proposed change and scope.
- Affected components and repository evidence (paths/symbols).
- Data/control-flow and trust-boundary impact.
- Compatibility, migration, rollout, and rollback concerns.
- Regression risks, missing tests, and unknowns.
- Recommended minimal scope and verification checks.

## Stop conditions
Stop and ask one focused question if the intended behavior or target boundary is materially unclear. Do not infer hidden dependencies from names alone. Do not edit files or modify data/configuration during impact analysis.
