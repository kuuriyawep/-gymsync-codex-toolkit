# WS5 — WhatsApp Intelligence Gateway Contract

**Status:** Repository-side design and contract only. No WhatsApp, Twilio, or n8n integration is installed, connected, or invoked by this workstream.  
**Authority:** Codex is the sole coordinator; the user retains final authority for gated actions.  
**Scope:** Toolkit repository only. No external messaging, credentials, account changes, or GymSync application changes.

## 1. Purpose and architecture

Define a secure, provider-neutral message contract for two-way communication between the user and Codex/authorized specialists. Preserve the approved target flow:

`Codex / Agents -> Shared Messaging API -> Identity, Routing & Permission Layer -> n8n Workflows -> Twilio WhatsApp API -> User`

The provider adapter is a transport, not an authority. It must not decide task scope, approve work, or independently invoke consequential actions. Codex remains the single router and decision-maker. A future implementation must use the existing runtime event, collaboration, workflow ledger, and approval concepts rather than create parallel orchestration or audit systems.

## 2. Supported message classes

| Class | Direction | Behavior | Authorization |
|---|---|---|---|
| `user_command` | inbound | Submit a user instruction to Codex intake; optionally address a named existing agent through Codex | Verified sender identity; Codex validates scope and permissions |
| `status_report` | outbound | Progress, completion, blocker, and evidence summary | Codex-authorized report; redact sensitive data |
| `incident_alert` | outbound | Urgent security, integrity, or availability alert | Verified agent identity and evidence; alert is not permission to remediate |
| `approval_request` | outbound | Present one exact gated action and its target/payload digest | Codex-generated request; user confirmation must bind to immutable request |
| `approval_response` | inbound | Approve or reject the referenced exact request | Verified user identity, unexpired request, exact request ID and digest |
| `media_artifact` | outbound | Deliver screenshot, preview, or report attachment | Allowlisted artifact reference, size/type checks, redaction, expiry |

Unknown message classes are rejected. Inbound user content, media, and quoted messages are untrusted data; they cannot override system, repository, or task policy.

## 3. Identity and routing

1. Resolve the inbound provider sender identifier to a pre-verified user identity using a trusted allowlist/identity store. Display name, profile photo, message text, and phone number supplied in message content are not proof of identity.
2. Reject unknown, unlinked, revoked, or ambiguous senders. Do not auto-enroll identities from inbound messages.
3. Agent identities are service identities bound to the six existing roles. Never present an agent as the user or send a message that implies user approval.
4. Route all user commands to Codex intake first. A named-agent mention is a routing hint, not a direct authorization or permission grant.
5. Bind each inbound event to provider message ID, verified sender ID, received timestamp, conversation ID, and idempotency key. Deduplicate retries before dispatch.
6. Enforce per-user, per-command, per-conversation, and global rate limits. Apply bounded retry/backoff to provider delivery; do not retry non-idempotent commands as new work.

## 4. Approval binding protocol

An approval request must include:
- immutable `approval_request_id`;
- workflow/task/proposal reference;
- exact action verb and operation identifier;
- exact target/resource identifier;
- canonical payload digest and payload version;
- risk level and concise impact statement;
- expiry timestamp;
- one-time challenge/nonce;
- Codex issuer identity and evidence references.

An approval response must reference the exact request ID and digest and contain an explicit `approve` or `reject` decision. Free-form replies such as “ok”, message reactions, read receipts, quoted text, or delivery receipts are never approval. The adapter must authenticate the sender, verify the challenge, check expiry and unused status, and atomically consume the approval response. Any changed action, target, payload digest, or expiry requires a new request. Approval authorizes only the stated operation and does not grant general permissions.

## 5. Message delivery and media safety

- Outbound reports are sent only after Codex validates the content and redacts credentials, tokens, private keys, personal data, and sensitive production data.
- Media must use an approved artifact reference, content-type allowlist, maximum size, malware scanning where supported, short-lived access, and access logging.
- Do not send raw logs, environment files, database dumps, secrets, or unredacted screenshots.
- Delivery status is tracked as queued, sent, delivered, read (if provider supports), failed, or expired. Provider receipt states are transport evidence only; they do not prove user consent or approval.
- Delivery failure is recorded and retried only under bounded idempotent policy. After retry exhaustion, notify Codex through the existing event path and surface a fallback report in the primary workspace.
- Do not claim a message was delivered until a provider delivery receipt confirms it.

## 6. Audit and privacy

Use existing runtime event envelopes and collaboration/workflow records as the canonical audit references. A future messaging adapter should persist a minimal message audit record containing:
- provider and provider message ID;
- internal message/event ID and correlation ID;
- verified sender/recipient identity references;
- message class, timestamp, routing decision, and authorization result;
- approval request ID/digest when applicable;
- delivery state and retry count;
- redacted artifact/evidence references;
- rejection/failure reason.

Do not persist full sensitive message bodies by default. Apply retention limits, access controls, encryption in transit/at rest, and redaction before logs or artifacts leave the trusted environment. Never place credentials in prompts, repository files, logs, or WhatsApp messages.

## 7. Failure and abuse handling

| Condition | Required behavior |
|---|---|
| Unknown or ambiguous sender | Reject; no dispatch; security audit event |
| Duplicate provider message | Return existing outcome; do not create duplicate work |
| Expired/replayed approval response | Reject; preserve audit evidence |
| Approval digest mismatch | Reject; require a new exact request |
| Unknown command or unauthorized target | Reject; do not broaden scope |
| Agent unavailable | Codex reports blocked/unavailable; no silent reassignment across permission boundaries |
| Codex unavailable | Queue safely or reject with clear status; no agent self-approval/arbitration |
| Provider outage or delivery failure | Bounded retry; record state; fallback report to primary workspace |
| Unsafe attachment | Quarantine/reject; never forward |
| Rate-limit abuse | Throttle, audit, and escalate when appropriate |

Fail closed whenever identity, target, approval binding, payload integrity, or delivery state is uncertain.

## 8. Test and acceptance boundary

Repository tests validate message schema shape, message-class vocabulary, approval binding fields, and documented security invariants. They do not prove sender authentication, webhook signature validation, provider delivery, atomic replay protection, media scanning, or end-to-end user experience.

Before any external integration, a separate explicit user approval is required for the provider, account, phone number, n8n workflow, credentials/secret storage, data retention, and allowed message types. Credentials must be supplied through an approved secret manager, never committed to Git. A future integration must first pass a sandbox test with positive and negative identity/approval/deduplication cases.

**Current runtime status:** WhatsApp/Twilio/n8n connectivity, webhook authentication, actual delivery, and interactive approval are NOT_RUN / BLOCKED.
