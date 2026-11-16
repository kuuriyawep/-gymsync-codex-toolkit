---
name: security-review
description: Conduct a defensive application security review across identity, data, APIs, dependencies, and deployment boundaries with evidence-based severity and confidence.
---
# Security Review

## When to use
Use for defensive review of application security, identity/access control, tenant isolation, data exposure, dependency risk, or deployment configuration. This skill is read-only by default.

## Procedure
1. Define review scope, assets, actors, trust boundaries, threat assumptions, and exposed attack surfaces.
2. Check authentication separately from authorization. Verify server-side role and tenant checks; do not trust client-only gates.
3. Inspect input validation, injection paths, secrets, logs, storage, rate limits, dependency posture, error leakage, and external integrations as relevant.
4. For databases, inspect row-level security, grants, service-role usage, ownership constraints, and migration safety.
5. For each suspected issue, identify exact location, preconditions, exploitability within the authorized scope, affected asset, and concrete impact.
6. Assign severity (Critical/High/Medium/Low) and confidence (Confirmed/Likely/Unverified) separately. Explain both ratings.
7. Recommend proportionate remediation and a safe verification method. Prefer static analysis and controlled test environments.

## Required finding format
- **Severity and rationale**
- **Confidence and evidence**
- **Affected asset / trust boundary**
- **Location and triggering scenario**
- **Impact**
- **Recommended remediation**
- **Safe verification**
- **Residual uncertainty**

## Stop conditions and safety boundary
Stop before testing live targets, exploiting vulnerabilities, changing controls, accessing real user data, or running destructive/security-impacting commands without explicit approval. Do not perform persistence, exfiltration, privilege escalation, or other actions outside defensive verification scope. If authorization or scope is unclear, remain read-only and ask.
