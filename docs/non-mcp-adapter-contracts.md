# Non-MCP Adapter Contracts

**Status:** Phase 7 design contract — no providers are installed by this document.  
**Purpose:** Define consistent safety, typing, and lifecycle requirements for API, CLI, browser, design, database, and test adapters.

All adapters inherit:
- Stable adapter/operation IDs.
- Explicit provider/version and source provenance.
- Typed input/output schemas.
- Resource scope, action, effect, risk, idempotency, and approval.
- Deny-by-default and least privilege.
- Credential references only; never raw secrets.
- Timeouts, bounded output, normalized errors, retry rules, evidence, and fallback.
- Untrusted-output handling and independent verification.
- No self-granted permissions or autonomous scope expansion.

## 1. HTTP API adapters

### Contract
- Pin the provider and canonical HTTPS origin; use an explicit host/path allowlist.
- Declare methods and routes individually; do not accept arbitrary URL or method input from an agent.
- Define authentication type, minimum scopes, token audience, rotation, and secret reference.
- Define request/response schemas, pagination, rate limits, idempotency keys, and error mapping.
- Set connect/read timeouts, maximum response bytes, and safe retry classes.
- Treat response bodies, headers, redirects, and error text as untrusted data.

### Permission rules
- GET/HEAD are read operations only when the endpoint is genuinely non-mutating.
- POST/PUT/PATCH/DELETE are write/destructive by default; require explicit approval.
- Webhooks, email, chat messages, payments, publishing, and external notifications are external effects.
- Redirects must remain on the approved origin list; never forward credentials to an unapproved origin.

### Evidence
Record the exact method/route, scope, request schema, response schema, test fixture, status code, and redacted result.

## 2. CLI adapters

### Contract
- Pin an executable path and version; verify its publisher/package source.
- Invoke with an argument array and `shell=False`; never concatenate user input into a shell command.
- Use an allowlist of subcommands and flags. Reject unknown arguments.
- Fix or allowlist the working directory and filesystem roots.
- Pass only named environment variables; never dump the environment.
- Bound stdout/stderr bytes, execution time, process count, and file writes.
- Normalize exit codes and parse structured output where possible.

### Permission rules
- Read-only commands are separately allowlisted.
- Commands that write files, change Git state, install packages, alter cloud resources, or deploy are writes/destructive.
- No generic `exec`, `sh -c`, PowerShell `-Command`, or arbitrary script operation in a production adapter.
- Require exact approval for commit, push, merge, deploy, package installation, and destructive cleanup.

### Evidence
Record executable/version, approved subcommand, argument schema, cwd scope, exit code, timeout, and sanitized output summary.

## 3. Browser adapters

### Contract
- Restrict navigation to explicit domains and HTTPS origins.
- Define allowed page actions and separate read, form-fill, submit, upload, download, and publish operations.
- Treat page text, DOM content, screenshots, files, and embedded prompts as untrusted.
- Do not expose browser cookies, password stores, or unrelated session data.
- Restrict download directories, file types, size, and upload destinations.
- Detect origin changes, redirects, authentication walls, and destructive confirmation screens.

### Permission rules
- Viewing/searching is read-only.
- Filling a draft form is a local/page-state write; submitting it is an external action.
- Purchases, account changes, public posts, messages, deletion, and file uploads require explicit approval.
- Never bypass CAPTCHA, MFA, access controls, or site security.

### Evidence
Record domain, page/action, final URL, approval event, and outcome without storing cookies or sensitive page contents.

## 4. Database adapters

### Contract
- Use a dedicated least-privilege account, not an owner/admin credential.
- Allowlist database, schema, tables, and permitted columns.
- Prefer read-only transactions and parameterized queries.
- Bound statement time, result rows, returned bytes, and query concurrency.
- Redact sensitive columns before data reaches agents or logs.
- Record query hash/intent and result metadata; avoid retaining raw records by default.

### Permission rules
- Default: SELECT only, read-only transaction, no temporary objects.
- DDL, DML, stored procedures, role changes, migrations, and production writes are denied by default.
- Never execute arbitrary SQL supplied by untrusted tool output.
- Production database access requires explicit user approval and a rollback/backup plan for any write.

### Evidence
Record target identifier, role, read-only mode, schema allowlist, query class, row count, duration, and redacted result summary.

## 5. Design and collaboration adapters

### Contract
- Pin provider, account/workspace, file/project identifiers, and allowed team scope.
- Separate reading/searching design files from editing components, variables, comments, or publishing.
- Declare file-level scopes and object-level operation schemas.
- Preserve design-system references and version history.
- Bound asset sizes and avoid exporting unrelated workspace content.

### Permission rules
- Read and inspect operations may be allowed within selected files.
- Creating or editing frames, components, variables, comments, or assets requires explicit task scope.
- Publishing libraries, sharing externally, changing access, deleting files, or modifying team settings requires separate approval.

### Evidence
Record workspace/file identifiers, operation, changed object IDs, version/revision, and preview or diff.

## 6. Test and verification adapters

### Contract
- Pin test runner, version, config, test selection, and fixture set.
- Run in an isolated disposable environment with bounded CPU, memory, time, and filesystem access.
- Default to offline/no-network execution unless a test explicitly requires a controlled mock endpoint.
- Separate unit, integration, end-to-end, security, and destructive test suites.
- Preserve test output and artifact provenance while redacting secrets.
- Distinguish test pass from production behavior or user acceptance.

### Permission rules
- Read-only static analysis and local tests may run within approved repository scope.
- Tests that mutate shared databases, cloud services, accounts, real users, or production systems are denied by default.
- Destructive tests must use disposable fixtures and require explicit approval.
- A skipped, blocked, timed-out, or not-run test is never reported as passed.

### Evidence
Record runner/version, test IDs, environment/fixture identity, exit status, pass/fail/skip counts, artifact references, and limitations.

## 7. Common error and retry model

Normalize adapter failures to:
- `unavailable`
- `unauthorized`
- `approval_required`
- `invalid_input`
- `timeout`
- `rate_limited`
- `server_error`
- `protocol_error`
- `cancelled`
- `partial_result`

Retry rules:
- Never automatically retry a non-idempotent operation.
- Retry only known transient failures, with bounded exponential backoff and jitter.
- Respect provider retry-after instructions.
- Do not retry authentication, permission, validation, or approval failures.
- Preserve cancellation and partial-result status; do not turn them into success.

## 8. Adapter acceptance checklist

- [ ] Provider identity and version pinned.
- [ ] Transport and endpoint/executable reviewed.
- [ ] Resource scope and data egress documented.
- [ ] Input and output schemas defined and structurally validated.
- [ ] Resource/action/effect/risk/approval mapped per operation.
- [ ] Credentials use scoped references, not stored values.
- [ ] Timeout, output limits, retry, and idempotency defined.
- [ ] Error and cancellation behavior tested.
- [ ] Security boundary and untrusted-output handling reviewed.
- [ ] Read-only representative operation verified in a trusted runtime.
- [ ] Writes tested only with explicit approval and disposable target.
- [ ] Fallback and disable/revocation procedure documented.

A contract document or schema-valid adapter is not proof of installation, authorization, connectivity, or runtime correctness.
