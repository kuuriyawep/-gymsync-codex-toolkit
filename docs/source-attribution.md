# Source Attribution and Adaptation Register

This register records the external projects that informed the GymSync Codex Toolkit and the selected capabilities being evaluated or adapted. It distinguishes conceptual influence from code reuse permission.

The canonical synthesis and disposition decisions are maintained in [Phase 6 — Capability & Architecture Final Synthesis](phase-6-final-synthesis.md).

## Foundational source repositories

| Source | Selected influence | Disposition |
|---|---|---|
| [ECC](https://github.com/affaan-m/ECC) | Verification loops, TDD discipline, defensive security review, change-impact thinking | ADOPT selected patterns |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Skill metadata and workflow/orchestration concepts | ADAPT |
| [Matt Pocock Skills](https://github.com/mattpocock/skills) | Requirements shaping, debugging, code review, TDD, dependency-aware work | ADOPT selected patterns |
| [Superpowers](https://github.com/obra/superpowers) | Brainstorming, systematic debugging, planning, verification gates, skill testing | ADOPT selected patterns |
| [OpenCode](https://github.com/anomalyco/opencode) | Typed tool contracts, permission separation, plugin lifecycle, session boundaries | ADAPT |
| [Anthropic Skills](https://github.com/anthropics/skills) | Skill authoring and evaluation methodology | ADOPT methodology |
| [Caveman](https://github.com/JuliusBrussee/caveman) | Clarity-first reporting, controlled context/output compression, fidelity evaluation | ADAPT |

## Additional capability source

| Source | Selected influence | Disposition | Boundary |
|---|---|---|---|
| [Graphify](https://github.com/Graphify-Labs/graphify) | Repository knowledge graph and code/file relationship discovery | ADOPT as optional external capability, subject to validation | Not mandatory; does not replace durable project records or memory |
| [n8n](https://github.com/n8n-io/n8n) | Stateful workflow, lifecycle, checkpoint, retry/recovery, and human-approval patterns | ADAPT patterns only | Do not embed or install the n8n runtime as toolkit orchestrator |

## Attribution and reuse rules

1. This register records conceptual influence and architectural disposition. It is not a license grant.
2. Public availability does not grant permission to copy code, assets, prompts, documentation, or packaged dependencies.
3. Before verbatim reuse or dependency installation, verify the exact repository revision, files/package, applicable license, notices, dependencies, security posture, and compatibility.
4. Preserve required copyright and NOTICE material where applicable.
5. Do not infer a repository-wide license from a license attached to one file, package, or release.
6. Do not claim Codex compatibility from behavior observed only in another runtime.
7. No complete external repository or skill library is adopted wholesale.
8. No source package is installed or copied into GymSync by this toolkit decision.

## Explicit exclusions

- Full OpenCode and n8n runtimes as toolkit orchestrators.
- Wholesale copying of external skill libraries.
- Unrestricted agent autonomy or automatic privileged actions.
- Destructive or unrecoverable context compression.
- Mandatory Graphify installation.
- Claude-specific runtime assumptions presented as verified Codex behavior.

## Audit status and limitations

The dispositions above are architecture-level decisions based on the completed source-audit work and synthesis record. They do not certify that every upstream file, dependency, release, or license has been individually cleared for code reuse.

Exact file-level license and supply-chain review remains a prerequisite before copying implementation code or installing packages. Runtime compatibility and actual tool behavior must be tested in a trusted Codex environment.

For the reconciled capability ownership, overlap decisions, security gates, and Phase 7–11 roadmap, see [phase-6-final-synthesis.md](phase-6-final-synthesis.md).
