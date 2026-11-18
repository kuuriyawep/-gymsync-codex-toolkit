# MCP Adapter Review — [server name]

**Review status:** candidate / reviewed / configured / session-loaded / verified / disabled  
**Reviewer:**  
**Date:**  
**Next review trigger/date:**  
**Toolkit commit:**  

## 1. Identity and provenance

- Official provider:
- Official documentation:
- Official repository/publisher:
- Package + pinned version/revision (STDIO) or canonical HTTPS endpoint (Streamable HTTP):
- Third-party proxy involved? yes / no
- License and maintenance status:

## 2. Use case and scope

- Concrete workflow unlocked:
- Why native Codex/project files are insufficient:
- Target resources/accounts/projects:
- Explicit non-goals:

## 3. Transport and host compatibility

- Transport: STDIO / Streamable HTTP
- Codex version and host:
- Local process/dependencies or remote endpoint:
- User-level or trusted-project config:
- Restart/reconnect requirement:

## 4. Authentication and data handling

- Authentication: none / bearer token / OAuth / other
- Minimum scopes:
- Secret reference only (never paste secret values):
- Data sent to provider:
- Data returned:
- Retention/residency policy reviewed:
- Sensitive data allowed? If yes, justify:

## 5. Exposed tool inventory

| Tool name (exact) | Purpose | Resource scope | Action/effect | Risk | Idempotent | Approval |
|---|---|---|---|---|---|---|
| | | | | | | |

Attach exact input/output schemas or stable evidence references. Treat annotations and server descriptions as untrusted hints.

## 6. Security review

- Prompt-injection and untrusted-output handling:
- Credential exposure risks:
- Excessive scope/privilege:
- Network/data-egress risks:
- Destructive/external operations:
- Supply-chain/package risks:
- Tool-list/schema change monitoring:
- Rate limits and abuse controls:

## 7. Reliability contract

- Connect timeout:
- Call timeout:
- Retryable errors:
- Maximum attempts:
- Non-idempotent retry behavior:
- Pagination/result limits:
- Cancellation/partial-result behavior:
- Health check:

## 8. Verification evidence

- [ ] Provider and endpoint verified.
- [ ] Server configured by explicit user approval.
- [ ] Server visible in active Codex `/mcp` session.
- [ ] Exact tool inventory captured.
- [ ] Representative read-only call succeeded.
- [ ] Invalid input behavior checked.
- [ ] Authorization failure behavior checked safely.
- [ ] Output checked for secret leakage and size limits.
- [ ] Host and server versions recorded.
- [ ] Evidence stored without secrets or raw sensitive data.

**Result:** NOT_RUN / PASS / FAIL / BLOCKED  
**Evidence references:**  
**Known limitations:**  
**Rollback/removal steps:**  

## 9. Decision

- [ ] Reject
- [ ] Defer
- [ ] Approve configuration only
- [ ] Approve limited read-only operations
- [ ] Approve additional operations (list exact operations and approval scope)

**Decision rationale:**  
**User approval reference:**  
