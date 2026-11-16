# Project Intelligence and Persistent Memory

## Purpose
Project Intelligence gives Codex a compact, evidence-backed knowledge layer reusable across sessions. It improves repository orientation and task continuity without replacing source inspection or making Codex subordinate to an external agent framework.

## Architecture
1. **Repository Map** — important modules, entry points, tests, and configuration.
2. **Project Memory** — verified architecture, system inventory, constraints, and durable decisions.
3. **Task Continuity** — a concise checkpoint of objective, progress, evidence, blockers, and next action.
4. **Knowledge Retrieval** — a targeted read sequence that loads relevant pages and verifies claims against current source.

Canonical templates live in `templates/project-memory/`. The Codex-discoverable skill is `.agents/skills/project-intelligence/SKILL.md`; `skills/project-intelligence/SKILL.md` is the portable mirror.

## Retrieval protocol
1. Confirm repository identity and read root instructions.
2. Read the project profile and current task checkpoint.
3. Use the repository map to select relevant architecture, inventory, constraints, and decision pages.
4. Inspect current source, tests, schemas, and configuration before consequential claims or edits.
5. Record conflicts, assumptions, unknowns, and stale knowledge explicitly.
6. Update the checkpoint at meaningful handoff points.

This is a retrieval discipline, not a claim that a vector database or automatic index exists. The initial implementation uses version-controlled Markdown and a deterministic local validator.

## Evidence and authority
- Verified claims need inspectable references: repository paths, tests, schemas, commits, or explicit user decisions.
- Memory is subordinate to current source-of-truth artifacts.
- Do not copy large code files into memory; summarize and link.
- Keep each project's knowledge in that project's repository.
- Never store credentials, tokens, private keys, personal data, or production secret values.

## Lifecycle and freshness
Use **Proposed → Verified → Approved** where a claim or memory change requires review. Decision records use Proposed, Accepted, Rejected, Superseded, and Deprecated. A validator can check structure and date freshness but cannot prove truth.

Record `Last verified` dates and the commit inspected. Revalidate affected pages when relevant source changes. The validator warns on old dated entries by default; `--strict-freshness` makes them fail. Placeholder dates are ignored.

## Validation
```bash
python tools/validate_project_memory.py
python tools/validate_project_memory.py --strict-freshness
python -m unittest discover -s tests -v
```

The validator checks required template files, expected headings, status labels, source-reference presence, and selected secret-like patterns. It is a guardrail, not a semantic or security audit.

## Boundaries
This implementation does not install Graphify, add an external database, create embeddings/vector search, launch Codex, automatically inspect new commits, autonomously rewrite memory, or integrate n8n/CrewAI/WhatsApp/Twilio. It does not change GymSync application source.
