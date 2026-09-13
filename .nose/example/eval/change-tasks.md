# Later change-tasks: the eval after the example run

The example run (`../product/`, `../src/world/`) is one finished loop. It proves a
cold agent can *build* the tiny product. It does **not** prove the next change is
cheap — which is what maintainability means. These two change tasks are the eval:
a future agent executes one (or both) against the finished tree, and we record
what the change actually cost.

This is a table, not a framework: one markdown card per task, one recording table
at the bottom. No new tooling, no scorer changes, no CI.

Ground rules for the executor:

- Work in a copy of `.nose/example/` (or a branch of the repo); do not rewrite the
  recorded example in place.
- Do not change the scorer or the seed workflow docs. A change task may touch only
  `src/world/`, `tests/`, and the `product/` files the card names.
- Re-run the scorer and tests the same way as in `../README.md` ("Verify it
  scores") before and after.

---

## Task L001 — add the `Asia` region (axis: `regions`, shape: `set_grows`)

- id: L001
- change: Add one entry to the `regions` authority so `world Asia` prints its
  countries, one per line. Only data that is already the authority's job — no new
  module, no new axis.
- example before:
  ```
  $ world Europe
  Germany
  France
  $ world Asia
  unknown region: Asia   (exit 1)
  ```
- acceptance:
  - `world Asia` prints countries one per line (pick any real Asian countries);
    `world Europe` unchanged; unknown-region behavior unchanged (FR-2).
  - The only edited source file is `src/world/regions.py`; the CLI (`src/world/__main__.py`)
    is **not** edited. If it was, the change was not local — record that.
  - `tests/test_regions.py` gains a case reading the authority (no recopied token
    list in a test string — that is an extra site; the scorer will catch it).
  - `PYTHONPATH=.nose python3 -m maintainability --root .nose/example` still exits 0
    and headline `W` does not rise above the pre-change value.
- axis exercised: `regions` (`set_grows`, p=0.75, locked) — the axis exists
  precisely for this change; Phase 2 said "more regions later".
- product files to update: `product/decisions.md` (one line: Asia added), nothing else.

## Task L002 — change the unknown-region wording (axis: none — formula/wording change)

- id: L002
- change: The unknown-region message changes from
  `unknown region: <NAME>` to `no such region: <NAME> (try one of: <regions>)`,
  where `<regions>` is the comma-separated list of region names read **from the
  authority**, not recopied.
- example before:
  ```
  $ world Atlantis
  unknown region: Atlantis   (exit 1)
  ```
- acceptance:
  - Exit code still nonzero for unknown regions (FR-2 still holds).
  - The list in the message comes from `REGIONS` in `src/world/regions.py`; a
    recopied literal list in `__main__.py` would be an extra site of `regions` —
    the scorer must still report floor `k=1` for `regions` (no extra sites).
  - `tests/test_cli.py` updated for the new wording, reading the authority where
    the list is asserted.
  - `PYTHONPATH=.nose python3 -m maintainability --root .nose/example` still exits 0;
    record whether headline `W` rose and why (wording grew one statement of the CLI).
- axis exercised: none directly — this is a wording/formula change inside the
  using unit. It tests that a *cosmetic* change is cheap and that it does not
  accidentally create an extra site of `regions`.
- product files to update: `product/decisions.md` (one line: wording changed),
  `product/phase-2.md` DR-1 example block (keep the recorded spec honest).

---

## Eval recording table

Fill one row per executed task. `tokens` = the agent's spend on the task if
measurable; otherwise write `n/a`.

| task | tokens | Phase 2 still holds? | headline W before | headline W after | W rose? | extra sites found | notes |
|---|---|---|---|---|---|---|---|
| L001 (add Asia, set_grows) | | | 0.4286 | | | | |
| L002 (wording change) | | | 0.4286 | | | | |

"Phase 2 still holds?" = does the finished product still satisfy every FR/TR/DR in
`../product/phase-2.md` after the change (run the tests; read the diff).

Baseline `w_baseline` in `../product/status.yaml` is 0.75 (a cap set at Phase 4);
the recorded example's measured headline W is 0.4286. Record the *measured* W in
the table, and note whether it stayed under `w_baseline`.
