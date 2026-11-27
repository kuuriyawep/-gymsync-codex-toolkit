# Autonomous Runtime Contract

**Status:** WS2 repository-side contract; no live runtime is implemented or claimed.
**Authority:** Codex remains the sole workflow coordinator. The user retains final authority.
**Source of truth:** Existing workflow ledger, workflow event/snapshot schemas, agent task graph, approval rules, and tool permission registry. This document defines the adapter boundary; it does not replace those components.

## 1. Purpose and non-goals

Define how a future persistent event/scheduler host may activate bounded work and report lifecycle events to the existing ledger. The host transports triggers and manages execution leases; it does not independently plan, authorize, route, or approve work.

This work does not install a scheduler, event bus, worker, database, agent framework, or external integration. A valid contract is not evidence of a running service.

## 2. Lifecycle mapping

The user-approved lifecycle is Monitoring -> Activated -> Working -> Reporting/Waiting.

| Runtime lifecycle | Required behavior | Ledger relationship |
|---|---|---|
| Monitoring | Wait for an explicitly configured event source or schedule; do not run model inference continuously by default | No workflow mutation merely for waiting |
| Activated | Validate event envelope, source identity, configured subscription, timestamp, expiry, scope, and deduplication key | Create or resume a workflow through the existing ledger |
| Working | Claim only a ready task whose dependencies and approval gates are satisfied; periodically renew its lease | Record task transitions, evidence, retries, timeouts, and checkpoints in the existing ledger |
| Reporting/Waiting | Submit evidence-backed result/proposal to Codex; release lease; wait for a new event or coordinator decision | Record completion/blocking/review through the ledger |

Lifecycle labels are adapter-level states, not replacements for the ledger's workflow states.

## 3. Event activation envelope

A trigger must be represented by `schemas/runtime-event-envelope.schema.json`. The adapter must reject malformed, expired, replayed, untrusted, or out-of-subscription events before activation.

Required checks:
- Stable event ID and idempotency key scoped to the configured source.
- Authenticated source identity; an event payload cannot self-assert trusted identity.
- Explicit subscription and permitted event type.
- Issued-at and expiry timestamps with bounded clock-skew policy.
- Explicit target workflow/task reference or a configured, deterministic intake route.
- Correlation ID for tracing.
- Payload treated as untrusted data, never as instructions that override repository or user policy.

Duplicate delivery must return the prior activation outcome and must not create duplicate work. Reuse of an idempotency key with a different payload must be rejected and audited.

## 4. Task ownership and leases

A future executor must use `schemas/runtime-task-lease.schema.json` when claiming work. A lease is a time-bounded claim, not permission to execute.

Before a claim:
1. Confirm workflow is in an executable state.
2. Confirm task exists, is ready, and dependencies are complete.
3. Confirm required workflow/task approval is granted for the exact write scope.
4. Confirm the worker identity is registered and authorized for the task.
5. Confirm no unexpired lease is held by another worker.

Lease rules:
- Use a unique lease ID and monotonically increasing fencing token per task claim.
- Record worker identity, issued time, expiry, heartbeat time, and attempt number.
- Renew only while the worker remains authorized and the lease is current.
- A worker with an expired or superseded fencing token must be prevented from committing results.
- Lease expiry makes a task eligible for recovery; it does not prove the previous worker stopped.
- Non-idempotent work must not be automatically replayed solely because a lease expired. Escalate for reconciliation.
- Lease acquisition, renewal, expiry, release, and recovery must be auditable.

The existing ledger remains authoritative for task state, attempt limits, approval state, checkpoints, and evidence. Lease metadata is runtime coordination metadata and must not become a second task-state database.

## 5. Retry, timeout, cancellation, and recovery

- Apply the ledger's bounded attempt limit; never reset attempts on worker restart.
- Retry only classified transient failures and only when the task is safe to retry.
- Treat timeouts as uncertain outcomes when side effects may have occurred. Reconcile before retrying non-idempotent work.
- Cancellation is cooperative and must be checked before new tool calls and consequential operations.
- On worker crash or stale lease: stop accepting writes from the stale fencing token, inspect ledger history/checkpoint, reconcile possible side effects, then resume only eligible idempotent work.
- Restore from the ledger event log and verified snapshot; never infer state from an unverified cache.
- If the event log/snapshot is corrupt or inconsistent, fail closed and escalate rather than inventing a recovery state.
- Preserve partial evidence and failure details. Do not silently mark a task complete.

## 6. Adapter boundary

The future runtime adapter may:
- Receive and authenticate events from configured sources.
- Validate envelopes and subscription policy.
- Deduplicate event delivery.
- Ask Codex to triage/route an activation.
- Claim, heartbeat, and release execution leases.
- Invoke only tools exposed through the existing capability registry and permission policy.
- Append lifecycle/evidence records through the existing ledger interface.
- Emit telemetry and delivery receipts.

The adapter must not:
- Replace Codex as orchestrator or make autonomous scope decisions.
- Grant permissions, approve gated work, or impersonate the user.
- execute a task graph merely because it is syntactically valid.
- Bypass workflow/task approval, tool permissions, or risk controls.
- Create a parallel workflow ledger, task graph, memory store, or evaluation runner.
- Treat scheduler delivery, lease ownership, or event authenticity as user approval.

## 7. Failure handling and observability

Every activation and execution attempt should be traceable by event ID, correlation ID, workflow ID, task ID, worker ID, lease ID, and attempt. Record timestamps, decision outcomes, validation failures, retries, timeouts, cancellations, and recovery decisions without storing secrets or unnecessary personal data.

Fail closed for unknown workers, invalid signatures/identity, expired events, conflicting idempotency keys, missing approvals, stale fencing tokens, corrupt state, and uncertain non-idempotent outcomes. Escalate unresolved cases to Codex and, where the risk policy requires, to the user.

## 8. Acceptance and verification boundary

Repository-side acceptance requires:
- JSON schemas parse and enforce required identity, expiry, scope, and lease fields.
- Tests cover valid and invalid activation envelopes, duplicate/replay semantics, lease expiry/fencing, approval separation, and safe recovery rules.
- Documentation explicitly distinguishes adapter contracts from live services.
- Existing ledger behavior and schemas remain backward compatible.

Not demonstrated by repository tests:
- Persistent monitoring or scheduled activation.
- Real worker execution, lease locking, or distributed fencing.
- Host-enforced permissions or identity authentication.
- Live Codex behavioral autonomy or external messaging.

These remain **NOT_RUN / BLOCKED** until a trusted runtime host is available and separately authorized.
