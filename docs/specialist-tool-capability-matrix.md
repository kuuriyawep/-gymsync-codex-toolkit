# WS4 — Specialist Tool Capability Matrix

**Status:** Repository-side capability mapping and contracts; live specialist tool execution is NOT_RUN / BLOCKED unless a capability has explicit session evidence.  
**Authority:** Codex remains the coordinator; the user retains final authority for gated actions.  
**Scope:** Toolkit repository only. No installations, external integrations, GymSync application changes, or production actions.

## 1. Purpose

Map specialist responsibilities to concrete capabilities, tool-operation contracts, risk levels, permission profiles, and verifiable availability. A role name or registry declaration is not proof that a tool is installed, callable, authenticated, or enforced by a runtime.

This matrix extends the existing six-agent model and `registry/tools.json`. It does not create a second agent registry, tool router, permission engine, or execution runtime.

## 2. Capability matrix

| Capability ID | Primary owner | Supporting role | Required operations | Risk ceiling by default | Current status | Verification boundary |
|---|---|---|---|---|---|---|
| `frontend.browser-automation` | `implementer` | `reviewer` | navigate approved local preview; inspect DOM/accessibility; exercise user flows; capture screenshots; compare responsive layouts | R2 in isolated preview; R3/R4 gated | BLOCKED — no approved browser automation host verified | No browser automation or screenshot test is claimed. A future host must prove target-origin allowlist, isolated session, artifact redaction, and read/write boundary |
| `backend.scenario-testing` | `implementer` | `test_engineer` | run isolated API/database scenarios; test transactions, concurrency, retries, idempotency, and failure recovery; inspect sanitized logs | R2 in disposable test environment; R3/R4 gated | BLOCKED — no approved backend runtime/database test host verified | Repository contract tests and CI do not prove live API/database behavior |
| `qa.automation` | `test_engineer` | `reviewer` | run unit/integration/e2e tests; manage fixtures; collect coverage and artifacts; reproduce regressions | R2 in isolated test environment | PARTIAL — repository CI is verified; interactive browser/e2e host is not | CI run IDs and exact commit identify what ran. Do not generalize a CI pass to unexecuted browser, production, or behavioral tests |
| `security.monitoring` | `security_auditor` | `repo_explorer` | static analysis; dependency and secret scans; configuration review; safe test-signal triage; evidence-backed incident escalation | R0/R1 by default; R2 only for approved isolated scans; R3/R4 gated | PARTIAL — repository secret scan and static quality gates are verified; continuous monitoring and live vulnerability feeds are not | A scheduled scan, alert delivery, credential revocation, permission change, deployment, or production remediation is NOT verified/authorized |
| `research.source-analysis` | `repo_explorer` | `planner` | search approved repository/docs/web sources; retrieve source excerpts; compare claims; record provenance, freshness, and uncertainty | R0/R1 | SESSION-AVAILABLE — repository/GitHub research tools are available in this working session; no persistent host availability is implied | Each result must cite source/commit/time. Tool availability must be rechecked in the target Codex runtime |

## 3. Canonical ownership and boundaries

- `repo_explorer`: read-only source discovery, evidence gathering, provenance, and research. No implementation or permission changes.
- `planner`: capability selection, task decomposition, risk classification, and acceptance criteria. No execution.
- `implementer`: approved code/configuration changes within assigned scope. No self-approval or independent merge/deploy.
- `reviewer`: independent read-only review. Must not review its own implementation as the approving reviewer.
- `security_auditor`: defensive analysis and escalation. No exploitative testing, credential revocation, production containment, or permission mutation without authorization.
- `test_engineer`: test code, fixtures, safe test execution, and evidence collection. No production implementation edits.

The capability owner is accountable for the work product, not automatically authorized to invoke every operation in the capability.

## 4. Permission profiles and risk controls

| Risk | Meaning | Default treatment |
|---|---|---|
| R0 | Read-only inspection | May proceed within configured source scope |
| R1 | Research, analysis, and proposal | May proceed; no external side effect |
| R2 | Isolated reversible change or test | Requires explicit task scope, sandbox/test target, and verification |
| R3 | Shared repository or shared-environment mutation | Codex authorization and independent review required |
| R4 | Commit/merge/deploy, destructive data operation, permission/security change, or consequential external action | Explicit user approval bound to the exact action and target |

Least-privilege rules:
1. Grant only the operations needed for the assigned task; deny by default.
2. Separate read, test, write, and consequential operations. A read capability does not imply write access.
3. Bind every operation to a configured repository, preview origin, test database, or approved resource identifier. Never accept an arbitrary caller-supplied root/target.
4. Tool credentials, if ever configured, must be referenced through a secret manager; never place secrets in registry files, prompts, logs, or artifacts.
5. Approval is operation-, target-, and scope-specific. It does not transfer to retries with changed targets or to a different operation.
6. Tool errors, missing credentials, unavailable hosts, and ambiguous targets fail closed. Do not silently fall back to a broader tool.
7. A capability declaration is not a permission grant. Runtime enforcement must be demonstrated by negative tests, not inferred from documentation.
8. Every invocation should record tool/operation ID, caller, target, risk, approval reference (if any), start/end, outcome, and redacted evidence reference.

## 5. Tool operation contract

Every registered tool operation should define:
- stable tool and operation IDs;
- capability IDs and accountable specialist owner;
- exact input and output JSON Schemas;
- allowed resource scope and target binding;
- effect classification (none/read/write/external);
- risk level and approval requirement;
- idempotency and bounded timeout/retry policy;
- availability status and evidence reference;
- failure behavior and audit fields.

The existing Graphify candidate in `registry/tools.json` remains **planned**, read-only, and not installed/runtime-verified. Its operation schemas and configured-project boundary are declarations only. Do not connect or install Graphify as part of WS4.

## 6. Availability vocabulary

- `verified`: exact operation executed successfully in the named environment with reproducible evidence.
- `session_available`: tool callable in the current session only; no persistence or target-runtime guarantee.
- `partial`: some sub-capabilities are verified while other required operations remain unavailable.
- `planned`: documented candidate; not installed or invoked.
- `blocked`: required host, credentials, approval, or safe target is absent.
- `unavailable`: explicitly tested and found unavailable in the named environment.

Never mark a capability `verified` solely because its schema parses, its registry entry exists, or a related CI workflow passes.

## 7. Verification requirements and exit gate

For each capability, verify:
1. Owner and supporting role are valid existing agents.
2. Input/output schemas are present and structurally valid.
3. Resource scope is explicit and target-bound.
4. Risk, effect, approval, idempotency, timeout, and retry are declared.
5. Positive invocation evidence exists before claiming availability.
6. Negative tests prove unauthorized operations, wrong targets, missing approval, malformed input, and unavailable tools fail closed.
7. Results include reproducible evidence and redaction checks.

WS4 can pass its repository-side contract gate while live capabilities remain BLOCKED, provided every gap is explicit. Live specialist execution, browser interaction, database scenario execution, continuous monitoring, and host permission enforcement remain NOT_RUN / BLOCKED until tested in a trusted runtime.
