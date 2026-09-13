# Product files

You write every file. The human talks. Not a requirements-to-code matrix. No `uses` links between code modules.

| File | Phase | Role |
|---|---|---|
| `product/status.yaml` | all | Where a cold agent starts; listed artifacts |
| `product/phase-1.md` | 1 | Invariant core, what this is not, notes for 2, parked |
| `product/phase-2.md` | 2 | Atomic MECE v1 requirements + pictures |
| `product/axes.yaml` | 3 | Change axes (the registry \(W\) reads) |
| `product/phase-4-plan.md` | 4 | MECE task DAG, linted against axes (orchestrator only) |
| `product/current-task.md` | 4 | The one task the current task agent may see |
| `product/decisions.md` | 4–5 | Judgment calls every later task reads |
| `product/entry-points.yaml` | 4 | Program starts / public API; metric roots |
| `product/phase-5.md` | 5 | Handover in the human’s language |

`.nose/docs/principles/` is seed, not product intent.

Templates: [templates/](templates/).

## `axes.yaml` fields

| Field | Who | Notes |
|---|---|---|
| `id`, `plain`, `statement`, `because`, `origin`, `frequency`, `p`, `shape`, `status`, `requirements` | Phase 3 agent; human confirms the **plain recap** | `p` from frequency table in [phase-3-axes.md](phase-3-axes.md) |
| `authority.symbol`, `authority.path` | Phase 4 **authority task** | null after Phase 3 |
| `verifies` | Phase 4 task that adds the test | paths |
| `extra_sites` | Task agent hunt | Prefer **delete**. Not a human form. `confirmed` only if a software collaborator keeps an extra |

`origin`: `brief` · `human` · `inferred`.

`status`: `locked` (design for it) · `dormant` (no code until shape is known). No `proposed` after Phase 3 recap.

`p`: numeric in \([0,1]\) (from frequency) or `high` / `medium` / `low` (1.0 / 0.5 / 0.25). Scorer accepts both and rejects non-finite or out-of-range numbers. `frequency` is ignored by the scorer, as are `plain`, `because`, `origin`, `requirements`.

`shape` ([principle 9](../principles/09-checkability.md)):

| Value | Domain cue |
|---|---|
| `set_grows` | another of the same kind |
| `new_variant` | different kind that needs its own handling |
| `signature_rename` | rename or change fields |
| `formula_value` | wording, layout, or the number we show |
| `unknown` | only with `dormant` |

Exactly one authority per locked row, filled in Phase 4. Members live in code, not yaml.

`entry-points.yaml`: `code_roots`, `exclude` (the loader always adds `.nose` when that directory exists at the product root), `entry_points`, optional `confirmed_live`, `deployables`. Run from product root: `PYTHONPATH=.nose python3 -m maintainability`. Python grains: [measure/python.md](../measure/python.md).

## Layout after a clone

```
AGENTS.md                 # orchestrator entry
.nose/                    # seed
product/                  # you create; status.yaml first
src/<name>/               # Phase 4
tests/                    # Phase 4 verifies
```
