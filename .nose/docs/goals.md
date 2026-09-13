# Goal

This repo helps a human go from ideas to finished software together with an AI. The AI leads the phases. The software should meet the human’s need and stay cheap to change on the [ten atoms](principles/README.md).

**Who.** A person who talks about the product. They do not pick files, yaml, or scores. The agent is any coding agent that reads root `AGENTS.md`.

**Success.** The human accepts Phase 5. Headline \(W\) did not rise unless `product/decisions.md` names the Phase 2 id that forced it.

**Non-goals.** UX quality, security, operations, importing an existing brownfield tree, and scoring languages other than Python in this version. The atoms and \(W\) are language-neutral. Only the Python backend is implemented. Parked scorer gaps: [bugs/](../../bugs/).

Already in the seed:

- Principles: [principles/README.md](principles/README.md)
- Five-phase workflow: [workflow/README.md](workflow/README.md)
- Combined metric \(W\): [metric.md](metric.md)
- CLI: `PYTHONPATH=.nose python3 -m maintainability` (`.nose/maintainability/`). Stdlib only. Setup is `product/axes.yaml` plus `product/entry-points.yaml`. Python measurement: [measure/python.md](measure/python.md).
