# Source Audit — Caveman

- **Source:** [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)
- **Audited revision:** `main`, commit `a192894723a8f47e7f504c7b5041967ff1f18e55`
- **Date:** 2026-11-18
- **CLI package:** `@caveman-ai/cli 4.1.0`
- **Go module requirement:** Go 1.26.11
- **License noted:** Apache-2.0 from v3.0.0 onward; older releases differ.
- **Evidence status:** Source/documentation inspection; no runtime tests.

## Findings

Caveman is a broad context/token optimization platform, not merely a concise-response skill. Two distinct parts:
1. Response compression with clarity exceptions and verbatim preservation of code, commands, paths, and errors.
2. A local context engine/proxy/MCP that classifies tool outputs, uses type-specific compressors, stores exact originals in local CCR, and provides recovery handles.

The engine exposes Compress/Retrieve/Detect/Stats and has 16 default compressors for structured and unstructured outputs. Its safer behavior stores the original first and passes it through unchanged if parsing fails, storage is unavailable, output is unsafe, or compression is not beneficial. Unknown mode fails closed to record.

Privacy/security concerns:
- CCR recovery data is unencrypted and can contain prompts/secrets; a recovery handle is not encryption/authentication.
- CLI telemetry is default-on for interactive use, with opt-out.
- Managed Cloud routing sends full request/response content through cloud.
- Non-loopback proxy listeners require authentication.
- The skill-only component does not make network calls; the file compression command can send selected content to a configured provider and overwrite the file after backup.
- Codex profile claims are limited; dummy-auth checks do not prove live-provider/task-quality behavior.

## Adoption decision

**ADAPT only bounded design patterns**: type-specific compressor interface, explicit recovery contract, fail-closed defaults, and fidelity evaluation. Use concise communication as opt-in only.

**REJECT** the full Go runtime/proxy/MCP/CLI, default-on telemetry, unencrypted recovery storage as-is, arbitrary automatic context compression, and file-rewrite workflows.

## Phase mapping

- Phase 7: modular capability/adapter and recovery contracts.
- Phase 8: optional opt-in communication policy.
- Phase 9: bounded tool-output summaries with recovery handles.
- Phase 10: fidelity, three-arm comparison, adversarial fixtures, recovery/fail-closed tests.
- Phase 11: real Codex skill/hook/profile/route/retrieval validation.

No Caveman package or runtime is installed.
