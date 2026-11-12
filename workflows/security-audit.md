# Security Audit

## Scope and safety
1. Confirm target repository/system, authorized environment, requested depth, and read-only boundaries.
2. Default to passive inspection and safe local tests. Do not exploit live systems, extract real user data, change permissions, or run destructive tests without explicit authorization.
3. Record the scope and exclusions so conclusions cannot be mistaken for a full-system certification.

## Audit workflow
1. Inventory assets, actors, trust boundaries, sensitive data, entry points, and external integrations.
2. Inspect authentication, server-side authorization, tenant isolation, database policies/grants, secrets, API validation, dependencies, file handling, logging, and deployment configuration.
3. Trace critical flows end-to-end and verify controls from server-side evidence; do not rely only on hidden UI controls.
4. For each suspected issue, identify a safe validation method and distinguish confirmed findings from hypotheses.
5. Rank confirmed findings by severity and realistic exploitability/impact. Avoid overstating severity.
6. Recommend specific remediation and a verification test.
7. Recheck relevant paths after an approved fix.

## Stop conditions
- Stop if authorization or target scope is unclear.
- Stop before active exploitation, production access, data extraction, permission changes, or disruptive testing unless explicitly approved.
- Never copy secrets or sensitive records into the report.

## Required output
- Scope, environment, exclusions, and methods
- Executive summary and overall risk posture limited to reviewed scope
- Findings: severity, affected component/location, evidence, preconditions, impact, remediation, and retest
- Positive controls observed (only when evidence supports them)
- Limitations, unverified areas, and recommended next steps

A report with no findings means only that none were identified within the stated scope; it is not proof of security.