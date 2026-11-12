# GymSync Codex Toolkit

A curated, Codex-first engineering toolkit: repository instructions, role-bounded agents, reusable skills, delivery workflows, safety gates, and evidence-backed learning.

> Codex remains the primary agent. This toolkit does not replace it with another agent framework.

## Default delivery loop
**Explore → Clarify → Plan → Approval → Implement → Test → Review → Verify → Document**

## Repository layout
- `AGENTS.md` — repository-wide operating contract and safety rules.
- `agents/` — read-only exploration, planning, implementation, review, and security roles.
- `skills/` — reusable task procedures with Codex-friendly instructions.
- `workflows/` — end-to-end bug, feature, database, security, research, and release processes.
- `references/` — permission/approval and source-adaptation policies.
- `evals/` — acceptance checks for toolkit quality.
- `learning/inbox/` — proposed lessons awaiting review.
- `learning/approved/` — curated lessons approved for reuse.
- `templates/` — decision-record template.
- `docs/` — source influence and attribution register.

## Use with Codex
1. Clone this repository or copy the relevant files into the target project's working directory.
2. Keep `AGENTS.md` at the project root if you want its instructions to apply to that project.
3. Use a skill by opening its `SKILL.md` and following its procedure when the task matches its description.
4. Use agent role files as role prompts only where your Codex environment supports the corresponding agent workflow; they do not install agents automatically.
5. Review all instructions against the target project's own rules before use.

## Safety model
- Read-only investigation before implementation.
- Explicit approval for destructive actions, production writes, schema/permission changes, deployment, and external side effects.
- Least privilege and no secrets in prompts or commits.
- Tests and verification are reported honestly; unrun checks are never presented as passed.
- Learning is reviewed before promotion; no autonomous self-modification.

## Source policy
The toolkit adapts general ideas from public engineering repositories. It is not a wholesale copy. See [source attribution](docs/source-attribution.md) and [source adaptation policy](references/source-adaptation.md). Verify exact per-file licensing before any verbatim reuse.

## Explicit exclusions
- Graphify is intentionally not included; install it separately if desired.
- No destructive automatic file compression or rewriting.
- No changes to the GymSync application source code.
- No dependency on Claude-, Hermes-, or OpenCode-specific runtime commands.

## Quality checks
See [toolkit acceptance checks](evals/acceptance-checks.md). These checks are a checklist; they are not claimed to have been automatically executed.
