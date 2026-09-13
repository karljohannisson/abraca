# Phase 3 — Change axes

**Cold agent loads:** this file, `product/status.yaml`, `product/phase-1.md`, `product/phase-2.md`.

You analyse those artifacts and infer **independent reasons the product may change or grow** over its life. The human confirms, corrects, and adds. They will not name things like “API protocols”; you must.

This artifact **is** the maintainability registry. Phase 4 cannot measure without it. You do **not** pick class names or file paths here.

## Do

1. Extract axes the artifacts already named (including “this should be a change axis because …”).
2. **Infer** unnamed independent reasons that are expectable for this kind of product. Each bet: `plain`, `because`, `origin: inferred`. What happens if we ignore it.
3. Independence: if A cannot happen without B, **one** axis. Probe in domain language (table below).
4. Frequency: ask 1–5 (5 = often over the life of the product, 1 = rare but possible). Never / they refuse → **not a row**; it belongs in Phase 1 “what this is not” or Phase 2 parked. Map into `p` (scorer):

   | frequency | `p` |
   |---|---|
   | 5 | 1.0 |
   | 4 | 0.75 |
   | 3 | 0.5 |
   | 2 | 0.25 |
   | 1 | 0.1 |

5. Shape, in their words, then you store the enum ([artifacts.md](artifacts.md)): another of the same kind → `set_grows`; different kind that needs its own handling → `new_variant`; look/wording/formula → `formula_value`; rename/fields → `signature_rename`; don’t know yet → `unknown` + `dormant`.
6. Now / later / never: later = `dormant` (no code in Phase 4); never = Frozen, not a row; now = `locked`.
7. Link each row to Phase 2 ids (`requirements: [FR-3, DR-1]`). That is why the axis exists, not a uses-map.
8. Recap **only the list of reasons** in ordinary language, mark inferred ones, wait. Then write `product/axes.yaml`.

Do not implement a framework because “this often changes.” Do not write `src/`.

## Domain probes (never jargon)

| You need | Ask |
|---|---|
| Split vs merge | “Could you add a new vendor without changing how the messages look?” |
| Frequency | “From 1 (rare but possible) to 5 (this will keep happening), how often?” |
| Shape | “Another of the same kind, or a different kind of thing?” |
| Now / later / never | “Make room now, remember it but don’t build it, or off the table?” |
| One product vs two | “Same program, or a separate product?” |
| Human-suggested axis | “If X happens, does anything else on this list have to change with it?” |

## `product/axes.yaml`

Every row: `id`, `plain`, `statement`, `because`, `origin` (`brief` · `human` · `inferred`), `frequency`, `p`, `shape`, `status` (`locked` · `dormant`), `requirements`, `authority: null` (Phase 4 fills it), `verifies: []`.

No leftover `proposed` after the recap. No two locked rows that only change together. No frozen reason as a row.

## Done

- Human accepted the recap of independent reasons, frequencies, now/later/never.
- Yaml matches that recap; inferred rows they accepted are `locked` or `dormant` as agreed.
- Independence and shape are set (`unknown` only on dormant).

Then `phase: 4`, `phase_name: implement`, `next_instructions: .nose/docs/workflow/phase-4-plan.md`, artifacts = status + phase-1 + phase-2 + `product/axes.yaml`, reset, continue.
