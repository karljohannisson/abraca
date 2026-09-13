# Five-phase workflow

The human talks. You move the work through these phases. They do not pick the phase.

| Phase | Who talks | Instruction | Artifact out |
|---|---|---|---|
| 1 Brainstorm | Human + you | [phase-1-brainstorm.md](phase-1-brainstorm.md) | `product/phase-1.md` |
| 2 Requirements | Human + you | [phase-2-requirements.md](phase-2-requirements.md) | `product/phase-2.md` |
| 3 Change axes | Human + you | [phase-3-axes.md](phase-3-axes.md) | `product/axes.yaml` |
| 4 Implement | **You only** (one task, one context) | [phase-4-plan.md](phase-4-plan.md) then [phase-4-task.md](phase-4-task.md) | `product/phase-4-plan.md`, `product/decisions.md`, code, commits |
| 5 Handover | Human + you | [phase-5-handover.md](phase-5-handover.md) | `product/phase-5.md` |

Coordination (status file, reset, advancing): [orchestrate.md](orchestrate.md).

Phase 2 makes the **product** honest (no glossed-over UX). Phases 3–4 make it **cheap to change** (registry + \(W\)). Meeting Phase 2 requirements blindly is not enough.

Phase 4 is not “design classes.” The plan is linted against the axes **before code**. Architecture is **one authority per locked axis**.
