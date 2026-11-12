# Toolkit Acceptance Checks
## Instruction hierarchy
- [ ] Codex remains the primary agent.
- [ ] Repository instructions define scope, approval, and safety boundaries.
- [ ] Agents have distinct roles and do not imply unavailable tools.

## Skills
- [ ] Each skill has valid YAML frontmatter with name and description.
- [ ] Trigger descriptions are specific and non-overlapping where practical.
- [ ] Steps are actionable and include safety/stop conditions.
- [ ] No unsupported Claude/Hermes/OpenCode-only command is required.

## Workflows
- [ ] Bug, feature, backend/database, security, research, and release workflows exist.
- [ ] Risky/destructive actions require explicit approval.
- [ ] Verification reports distinguish passed, failed, skipped, and not run.

## Learning and provenance
- [ ] Learning inbox is separate from approved lessons.
- [ ] No autonomous silent self-modification.
- [ ] Source influence and license verification requirements are documented.
- [ ] Graphify is excluded.

## Repository quality
- [ ] README explains installation/use and scope.
- [ ] Links and paths resolve.
- [ ] No secrets or user-private data are committed.