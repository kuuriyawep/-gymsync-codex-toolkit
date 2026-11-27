# WS3 — Agent Collaboration Protocol

**Status:** Repository-side contract and test implementation; live multi-agent behavior is NOT_RUN / BLOCKED.  
**Authority:** User is final decision authority. Codex is the sole accountable coordinator and arbiter.  
**Related architecture:** [Intelligent Agent Ecosystem Architecture](intelligent-agent-ecosystem-architecture.md), [Agent Intelligence Standard](agent-intelligence-standard.md), [Autonomous Runtime Contract](autonomous-runtime-contract.md).

## 1. Purpose and non-goals

Define auditable collaboration between the six existing specialist roles. Extend the existing handoff, result, task-graph, and workflow-ledger concepts; do not create another router, task engine, agent registry, or execution runtime. No new agents are introduced by WS3.

This contract describes records and decision rules. It does not itself send messages, start agents, enforce host permissions, or provide background execution.

## 2. Interaction types

| Type | Meaning | Ownership effect |
|---|---|---|
| Consultation | Ask a specialist for advice or evidence | Does not transfer task ownership |
| Delegated review | Ask an independent reviewer to assess a bounded artifact/change | Review is a separate bounded assignment; implementation owner remains accountable for implementation |
| Disagreement | Preserve materially different conclusions and their evidence | No ownership or permission change |
| Incident escalation | Raise a time-sensitive safety, security, integrity, or availability concern to Codex | Does not authorize remediation or broaden scope |

Every interaction receives a stable `interaction_id`; every immutable event receives a unique `record_id`. Related events reference the same interaction and prior record IDs. Retries must reuse the interaction's deduplication identity; a materially new request gets a new interaction ID.

## 3. Consultation protocol

1. Requester identifies the target specialist, task/workflow, question, purpose, bounded read/write scope, relevant evidence, and response expected.
2. Codex checks role fit, task scope, permissions, availability, and whether the request duplicates an existing interaction.
3. A consultation request is recorded before dispatch. A consultation is advisory: it cannot change the task owner, approved scope, or workflow state.
4. Recipient returns a response, evidence references, confidence/unknowns, and any disagreement or escalation need.
5. Codex validates the response against source evidence and records whether it is accepted, rejected, deferred, or needs more evidence.

A recipient may decline or be unavailable. Do not silently treat no response as agreement.

## 4. Delegated review protocol

- Codex creates a distinct review assignment with one accountable reviewer, explicit artifact/commit scope, read-only permissions, acceptance criteria, and deadline/timeout policy supplied by the runtime.
- Reviewer must be independent of the implementation being reviewed; do not ask the implementer to approve their own work.
- Review output identifies finding severity, exact locations, evidence, impact, and remediation. Findings are not automatically accepted as true; Codex validates them.
- The implementation task remains owned by its original implementer. Review completion does not merge, commit, deploy, or authorize changes.
- If reviewer availability or independence cannot be established, report BLOCKED/NOT_RUN rather than inventing a review result.

## 5. Disagreement and arbitration

1. Preserve each position separately, including author, rationale, evidence, assumptions, uncertainty, and potential counterexample.
2. Ask for targeted evidence or a bounded independent review when useful.
3. Codex compares reproducibility, source authority, evidence quality, scope, and risk. Seniority, confidence, or majority vote alone is not a decision rule.
4. Codex records the outcome and rationale. Outcomes: accept, reject, defer, needs_more_evidence, no_action.
5. An unresolved disagreement remains explicitly unresolved and is reported to the user when it affects correctness, safety, or a consequential decision.

Codex may arbitrate technical recommendations within approved scope. User approval remains mandatory for R3/R4 or other gated actions under repository governance. A decision record is not an approval token.

## 6. Incident escalation

Escalate promptly to Codex when a specialist detects a credible critical/high security issue, data-integrity threat, unauthorized access, secret exposure, destructive side effect, or significant service risk.

Escalation record must include severity, affected workflow/task, concise facts, evidence references, deduplication fingerprint, immediate containment recommendation, and uncertainty. Do not include secrets or unnecessary sensitive payloads.

- Critical/high: notify Codex immediately; Codex pauses affected work where safe, validates, and routes to the user/authorized response path.
- Medium/low: record and route through normal triage unless urgency justifies escalation.
- Agents may recommend containment but cannot independently change permissions, revoke credentials, alter production, deploy, or perform other gated actions unless explicitly authorized.
- Duplicate alerts with the same fingerprint are linked/updated, not multiplied. A new material development gets a new record linked to the incident.
- Incident closure requires Codex decision, evidence of disposition, and any required user approval reference.

## 7. Audit record requirements

Use `schemas/collaboration-record.schema.json`. Records are append-only event facts; corrections are new linked records, not silent edits. Capture sender/recipient, interaction and workflow/task IDs, event/status, timestamp, purpose, bounded scope, request/response, evidence, related records, and Codex decision where applicable.

Never store credentials, full transcripts, raw sensitive production data, or secrets. Evidence references should point to approved repository paths, commit IDs, test reports, or redacted artifact IDs.

The existing workflow ledger remains the workflow-state record. Collaboration records are payload/contracts for collaboration evidence, not a parallel workflow ledger. A future adapter may append references/events to the existing ledger; no ledger event types or runtime execution are added by this workstream.

## 8. Failure and safety handling

- Duplicate request: return/link the existing interaction; do not dispatch a second copy.
- Recipient unavailable/timeout: record unavailable or blocked; Codex may choose another existing specialist if scope and independence remain valid.
- Malformed or untrusted response: reject/quarantine it and request a corrected structured result.
- Scope/permission violation: stop the affected interaction, record the violation, and escalate to Codex; never widen scope automatically.
- Conflicting evidence: preserve both sides and request targeted verification.
- Codex unavailable: agents do not self-arbitrate, self-approve, or continue gated actions. Preserve the event for later Codex triage.
- Delivery failure: record failure and retry only under bounded, idempotent runtime policy.

## 9. Acceptance boundary

Repository tests can validate schema shape, required fields, event vocabulary, and governance clauses. They cannot prove agent-to-agent delivery, independence, arbitration quality, incident response latency, or runtime enforcement. Those remain NOT_RUN / BLOCKED until a trusted Codex/runtime host exists and behavioral evaluations are executed.
