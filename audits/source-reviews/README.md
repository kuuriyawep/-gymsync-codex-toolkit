# External Source Audit Index

**Canonical location:** `audits/source-reviews/`  
**Synthesis:** [Phase 6 Final Synthesis](../docs/phase-6-final-synthesis.md)  
**Adoption map:** [Source-to-toolkit adoption map](../docs/source-adoption-map.md)  
**Register:** [Source attribution](../docs/source-attribution.md)  
**Checkpoint:** [PROJECT_STATE.md](../PROJECT_STATE.md)

This index archives the selected repository reviews so that later phases can consume the evidence without repeating research or blindly importing upstream projects.

## Audit inventory

| # | Source | Review record | Evidence status | Disposition |
|---:|---|---|---|---|
| 1 | [ECC](https://github.com/affaan-m/everything-claude-code) | [01-ecc.md](01-ecc.md) | PARTIAL — legacy review carried forward; exact revision and full file-level evidence not recovered | ADOPT selected practices |
| 2 | [Hermes Agent](https://github.com/NousResearch/hermes-agent) | [02-hermes-agent.md](02-hermes-agent.md) | PARTIAL — prior capability selection; exact revision and full technical audit not recovered | ADAPT memory/skill lifecycle |
| 3 | [OpenCode](https://github.com/anomalyco/opencode) | [03-opencode.md](03-opencode.md) | Source/docs review; pinned revision | ADAPT |
| 4 | [Graphify](https://github.com/Graphify-Labs/graphify) | [04-graphify.md](04-graphify.md) | Source/docs review; pinned revision | ADOPT optional external tool; ADAPT adapter |
| 5 | [Superpowers](https://github.com/obra/superpowers) | [05-superpowers.md](05-superpowers.md) | Source/docs review; pinned revision | ADOPT selected practices; ADAPT workflows |
| 6 | [Matt Pocock Skills](https://github.com/mattpocock/skills) | [06-matt-pocock.md](06-matt-pocock.md) | Source review; pinned revision | ADOPT selected patterns; ADAPT DAG/delegation |
| 7 | [Anthropic Skills](https://github.com/anthropics/skills) | [07-anthropic-skills.md](07-anthropic-skills.md) | Source/docs review; pinned revision | ADOPT evaluation methodology; ADAPT tool/design patterns |
| 8 | [Caveman](https://github.com/JuliusBrussee/caveman) | [08-caveman.md](08-caveman.md) | Source/docs review; pinned revision | ADAPT bounded compression/recovery/evaluation patterns |
| 9 | [n8n](https://github.com/n8n-io/n8n) | [09-n8n.md](09-n8n.md) | Source/docs review; pinned revision | ADAPT workflow/tool/evaluation patterns |

## Evidence interpretation

- The nine source folders are now represented in the repository.
- Seven later source reviews have revision-pinned source/documentation evidence.
- ECC and Hermes are legacy reviews. The user explicitly instructed that already-completed work must not be repeated. Their known prior selections are recorded, but the recovered context did not contain enough detail to certify exact revisions, all file paths, or file-level licensing.
- Do not describe the two legacy records as full revision-pinned audits.
- No upstream source code has been copied by creating these records.
- No upstream plugin, package, runtime, or service has been installed.
- No Codex runtime compatibility is inferred from static source review.

## How later phases must use this archive

1. Read the relevant source report before implementing a capability.
2. Check [source-adoption-map.md](../docs/source-adoption-map.md) to find the existing toolkit owner and avoid duplicates.
3. Preserve upstream revision and licensing notes.
4. Reuse concepts where appropriate; copy code only after exact file/revision/license and dependency review.
5. Add an implementation only when the capability is missing and the user-approved phase includes it.
6. Record tests and runtime evidence separately from source-audit findings.
