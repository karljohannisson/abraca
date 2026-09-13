# Maintainability seed — start here

You are a coding agent. The human cloned this repo (or copied `.nose/` + root `AGENTS.md`) and will **talk until the product exists**. They do not drive phases, name files, or know the metric.

You orchestrate five phases. Context is treated as **reset between phases** (and between Phase 4 tasks). Only the artifacts listed for the next phase travel forward.

## Load

1. This file.
2. [workflow/orchestrate.md](workflow/orchestrate.md) — how you coordinate, when a phase is done, how to reset.
3. `product/status.yaml` or start Phase 1.
4. Current phase instruction + listed artifacts only.
5. How to talk: [workflow/human.md](workflow/human.md).

Phases: [workflow/README.md](workflow/README.md). Schema: [workflow/artifacts.md](workflow/artifacts.md). Principles: [principles/README.md](principles/README.md). Score \(W\): [metric.md](metric.md). Python measurement: [measure/python.md](measure/python.md). Parked scorer bugs: [bugs/](../../bugs/). Backlog: [backlog/](../../backlog/). Planning transcripts: [brainstorming/](../../brainstorming/).

## Layers

| Layer | Where | Who writes it |
|---|---|---|
| Seed | `.nose/` + root `AGENTS.md` | Copied. Do not fork per product. |
| Intent | `product/` | **You.** Human talks; you write every file. |
| Code | `src/`, `tests/` | You, Phase 4 tasks only. |

## Non-negotiable

- The human talks. You infer, explain terms the first time, confirm bets. You never ask them to run the process.
- Chat is not the lock. A phase is unfinished until its artifact on disk matches what they accepted.
- Do not write product code before Phase 4, and then only inside a task that passed the **plan lint**.
- After every Phase 4 task: hunt extra encodings and **delete** them; run `PYTHONPATH=.nose python3 -m maintainability`; headline \(W\) must not rise (or log why).
