# Source Audit — Anthropic Skills

- **Source:** [anthropics/skills](https://github.com/anthropics/skills)
- **Audited revision:** `main`, commit `e4bb5d960d87126ff3b3a8af1a104b7db67560ba`
- **Date:** 2026-11-18
- **Inventory noted:** 544 tree entries, 448 blobs, 19 skills.
- **License:** No root LICENSE; 18 of 19 skill folders had per-skill LICENSE.txt files, inspected headers Apache-2.0. One skill (`doc-coauthoring`) lacked a license file. Third-party dependencies have separate notices/licenses.
- **Evidence status:** Source/documentation inspection; no runtime tests.

## Findings

This is a Claude-focused examples/document-processing repository, not a general Codex toolkit. It has a Claude plugin marketplace manifest with five plugins and no documented Codex plugin manifest/runtime support.

The standout capability is `skill-creator`:
- Capture intent and success criteria.
- Progressive disclosure: metadata, concise skill body, on-demand references/scripts/assets.
- Start with 2–3 realistic prompts.
- Compare with-skill against baseline/old-skill.
- Human review through an HTML eval viewer.
- Objective assertions and evidence-based graders.
- Aggregate pass rate, time, tokens, mean/stddev and deltas.
- Detect non-discriminating/flaky assertions.
- Blind A/B comparison and iterative improvement.
- Train/holdout split for trigger optimization.
- Positive and hard-negative near-miss trigger prompts.
- Precision/recall/accuracy and repeated runs.

Other patterns:
- MCP Builder: naming/discoverability, focused outputs/pagination, typed schemas, actionable errors, and readOnly/destructive/idempotent/openWorld annotations. Annotations are hints, not security guarantees.
- Web app testing: reconnaissance-first Playwright, screenshots and browser logs; its server helper uses `shell=True`, so untrusted command strings are unsafe.
- Frontend design: plan → critique against brief → build → screenshot/self-critique.
- Document skills: deterministic scripts, schema validation, rendering checks, output-specific QA.

Codex incompatibility:
- Skill-creator scripts use `claude -p`, Claude Code events/auth, and `.claude/commands`; they are not portable Codex harnesses unchanged.
- Webapp server helper uses shell execution.
- Per-skill licensing and bundled dependency notices must be checked individually.

## Adoption decision

**ADOPT evaluation methodology; ADAPT MCP tool-design, browser-test, frontend critique, and progressive-disclosure patterns. REJECT unmodified Claude-specific scripts and document skills as core toolkit additions unless later required.**

## Phase mapping

- Phase 7: skill metadata/packaging, tool schemas and MCP design.
- Phase 9: user review, test prompt curation, browser/design workflow.
- Phase 10: Codex-native evaluation harness, A/B, graders, trigger precision/recall, held-out sets, flaky-eval detection.
- Phase 11: real Codex behavior/runtime validation.

No Anthropic package/plugin is installed.
