# Example: one recorded nose run

This tree is a **finished product**, recorded so a cold agent can see one complete
loop: axes → authorities → handover. Read `product/` in phase order:
`status.yaml` → `phase-1.md` → `phase-2.md` → `axes.yaml` → `phase-4-plan.md` →
`decisions.md` → `entry-points.yaml` → `phase-5.md`. It is the dup fixture's idea
(countries) grown into a coherent tiny product: **world** prints the countries of a
region.

- `product/axes.yaml` — Phase 3 output: one locked axis (`regions`, "the list of
  regions may grow", p=0.75) and one dormant (`greetings`). Authorities are filled
  in, as they are after Phase 4.
- `product/phase-4-plan.md` — the MECE task list, lint box by box: T001 encodes
  `regions` (authority `src/world/regions.py`), T002 uses it (the CLI).
- `src/world/` — the code that came out: one authority per locked axis, the CLI
  reads only through it. Tests read the authority instead of recopied member
  tokens — recopying them in a test string is exactly the "extra site" the scorer
  catches (try it: replace `REGIONS[first_region]` in `tests/test_cli.py` with
  `["Germany", "France"]` and watch `regions` go to k=2).
- `product/phase-5.md` — the handover in the human's language.

## Verify it scores

From the **repo root** (this tree's parent):

```
PYTHONPATH=.nose python3 -m maintainability --root .nose/example
```

```
W (headline) 0.4286   [0,5] lower=cheaper
W (floor)    0.4286   scanner only; not proof of zero extras
```

Floor equals headline: no extra sites, no confirmed extras. Mass 0.4286 is only
statement volume of a tiny corpus — expected at this size, not a defect. Run the
tests too: `cd .nose/example && PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'`
(5 tests pass).

A fresh clone does **not** copy this tree; its `product/` starts empty at
`phase: 1`. This tree exists to imitate, not to seed.
