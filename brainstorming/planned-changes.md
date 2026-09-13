# In-flight seed changes (do not collide)

Status: **implemented on branch `feat/language-neutral-metric`**. PR not opened (no git/GitHub credentials in this session). Another agent can still use `product/`.

Owner of this plan: the session that wrote this file. Path to hand another agent: `.reviews/planned-changes.md`.

## What this is

The seed (`.nose/` plus root `AGENTS.md`) will change so that:

1. `goals.md` is only the product goal (today’s Goal 0). Goals 1–4 go away. They already live as docs.
2. Principles and \(W\) stay language-neutral. Python is one measurement backend. A later React plus Python tree should be scoreable without rewriting atoms.
3. The current Python scorer stops lying on checkability, coupling, volume defaults, and \(P\) bounds.
4. Tests run with the stdlib. The \(W\) gate can fail the process, not only the prompt.

Parked: a token/correctness/maintainability benchmark, restoring the deleted chat app, statement-level dead-code analysis, a JavaScript backend, CI.

## Collision rule for a parallel agent

| You may write | Do not write |
|---|---|
| `product/**` (empty on purpose; a new product idea belongs here) | `.nose/maintainability/**` |
| `src/**`, root `tests/**` if you are building a product | `.nose/tests/**` |
| `.reviews/**` except this file | `.reviews/planned-changes.md` |
| Root `README.md` only if you must, and say so | `.nose/docs/goals.md` |
| | `.nose/docs/metric.md` |
| | `.nose/docs/principles/**` |
| | `.nose/docs/workflow/phase-4-task.md` |
| | `.nose/docs/workflow/phase-4-plan.md` |
| | `.nose/docs/workflow/phase-5-handover.md` |
| | `.nose/docs/workflow/artifacts.md` |
| | `.nose/docs/README.md` (one CLI line may change) |
| | `.nose/pyproject.toml` |

If your idea needs a scorer change, stop and wait. Do not fork `maintainability/`.

## Target layout

```
.nose/docs/goals.md              product goal only
.nose/docs/principles/           language-neutral atoms (already mostly)
.nose/docs/metric.md             language-neutral W; measurement backends named, not mixed in
.nose/docs/measure/python.md     NEW. Python grains (T=15, ast.stmt, match, import)

.nose/maintainability/
  __init__.py                    VERSION; drop "goal 4"
  __main__.py                    CLI; W-vs-baseline exit
  yaml_lite.py                   unchanged except as needed
  registry.py                    language-free; validate p in [0,1] finite
  combined.py                    language-free W math (keep)
  model.py                       NEW. Corpus, Mod, Unit, Site, Ref. No ast.
  atoms.py                       scores a model.Corpus only. No ast.
  sites.py                       builds sites from Corpus + registry. No ast.
  languages/
    __init__.py                  pick backend by file suffix
    python.py                    parse, units, refs, fail-loud, volume walk, complexity
  complexity.py                  DELETE after move into languages/python.py
  corpus.py                      shrink or delete after model.py exists
```

Public call stays:

```
PYTHONPATH=.nose python3 -m maintainability
PYTHONPATH=.nose python3 -m maintainability --root DIR
```

Adding a language later means one file under `languages/` plus a suffix in the picker. Not a new atom. Not a new \(W\).

## Data shape

Language-neutral:

- `Axis` (already): id, statement, p in [0,1], shape, status, authority path/symbol, verifies, extra_sites
- `Unit`: qname, kind (`module` | `class` | `function`), path, lineno span, statement_count, complexity, language id
- `Mod`: path, qname, language id, units, symbols, source text
- `Corpus`: modules, by_path, symbols
- `Site`: axis_id, path, lineno, unit_qname, origin, strength, is_authority
- `Ref`: from unit_qname to same-repo target qname (fan-out and volume)

Python-only, behind `languages/python.py`:

- `ast.parse`, import edges, `match` exhaustiveness, Sonar complexity on Python AST, `T=15`

A mixed tree is one `Corpus` with modules of more than one language. Locality already has deployable as \(L=5\). Frontend vs backend should be two `deployables` in `entry-points.yaml`, not a second metric.

This wave still only *parses* `*.py`. The types and file split are what make a later `*.ts` / `*.tsx` backend a local add.

## Waves

Each wave ends in a check. Do not start the next until that check is green.

### Wave 0. Claims and docs

Check: `goals.md` has one goal. `metric.md` does not say “any Python codebase” or “Goal 3”. Principles 4, 7, 9, 10 name the property in language-neutral terms and point at `measure/python.md` for grains.

- Rewrite `.nose/docs/goals.md` as the product spec. User is a non-software human plus an arbitrary coding agent. Success is accepted Phase 5 plus a non-rising headline \(W\) on the registry that product built. Non-goals: UX, security, ops, brownfield import, non-Python measurement in this version.
- Delete numbered items 1–4 from `goals.md`. Point at `principles/README.md`, `workflow/README.md`, `metric.md`, and the CLI in one “Already in the seed” paragraph. Do not keep them as locked research goals.
- Split `.nose/docs/metric.md`: formulas stay. Move “Python application” to `.nose/docs/measure/python.md`.
- Principle 4: \(T\) is a per-language working-set bound. Python uses 15. Do not hard-wire 15 as the principle.
- Principle 9: fail-loud for `signature_rename` is specified, not implemented. Say that. Keep `new_variant` as the implemented Python case (`match` without `_`).
- Principle 10: volume is **module-import closure** (whole file live if imported). Defaults if yaml entry points are empty: `**/__main__.py`, `main.py`, `app.py`, and `[project.scripts]` when a `pyproject.toml` exists. Delete the claim that volume runs with no registry. The CLI still requires `product/axes.yaml`.
- `__init__.py` docstring: drop “goal 4”.

### Wave 1. Honest Python scorer plus the language seam

Check: new tests fail on trunk’s bugs and pass on the new code. `python3 -m unittest discover -s .nose/tests` collects and passes. Fixture still scores. CLI on repo root still exits 2 without a registry.

Fixes in `languages/python.py` (today’s bugs, moved):

1. `_match_subject_is_auth` returns True only when the match subject names the authority. Unrelated `match` must not affect \(V\).
2. Fan-out counts a name only if it resolves to a project module. `import requests; requests.get` does not raise \(H\).
3. `registry._parse_axis` rejects non-finite \(p\) and \(p \notin [0,1]\).
4. Volume roots: yaml `entry_points` plus live authorities plus `verifies`, and the documented defaults when the yaml list is empty. Grain stays file-level. Nested dead functions in a live file still do not add mass (documented, not a bug).
5. `SKIP_DIRS` includes `.nose`.
6. `ClassDef` complexity stays 0 unless we find a cheap correct fix. Prefer documenting it in `measure/python.md` over a fake class score.

Refactor:

- `atoms.py` / `sites.py` / `combined.py` / `registry.py` import `model`, not `ast`.
- `build_corpus` dispatches by suffix. Today only `.py`.
- Authority site remains the **module** unit (current `sites.py` 33–35) unless a later wave changes it. Document that. Do not silently switch to the symbol unit in this stack.

Tests (stdlib, `def test_*` collected). New cases with literal outputs:

- Unrelated `match` does not drop \(V\) for `new_variant`.
- Third-party `import` does not increase coupling versus a no-import twin.
- `p: 1.5`, `p: -0.1`, non-finite yaml fail at load with a clear error.
- Empty `entry_points` still finds `__main__.py` / `main.py` when present.
- `combined()` cases already in `test_combined.py` stay.

Runner: wrap or rename so `python3 -m unittest discover -s .nose/tests` runs them. No pytest dependency.

### Wave 2. Fail-closed \(W\) gate

Check: CLI exit 1 when headline \(W\) exceeds `--max-w` (or `product/status.yaml` `w_baseline` when that flag is omitted and the field is set). Exit 0 when first run and baseline is null. Exit 2 still means missing registry.

- `__main__.py` reads optional `--max-w FLOAT`. If omitted, read `status.w_baseline` when the file exists.
- Do not parse the Phase 4 plan. One gate only.
- Update `phase-4-task.md` verify step 4 to treat a nonzero CLI exit as failed. Keep the `decisions.md` exception as `--max-w` with the new value plus a decision row, not a silent pass.

### Wave 3. Recorded example, empty product

Check: `product/` still only `.gitkeep`. A short `.nose/docs/measure/example.md` points at `.nose/tests/fixtures/dup` and shows the commands plus the current fixture \(W\) numbers after wave 1 (re-measure; do not copy 0.7833 if the fixes change it).

- Do not restore `src/chat/`.
- Do not put a self-review in `product/`.
- Leave `.reviews/` as process files. Do not gitignore them in this stack unless asked.

### Wave 4. Not in this stack

- Benchmark of token cost, correctness versus Phase 2, and later change-tasks.
- JavaScript / TSX parser.
- Statement-level volume.
- Plan-lint executable.
- CI workflow.
- Scoring Nose itself.

## Intended diffs by file (wave 0–3)

Create:

- `.nose/docs/measure/python.md`
- `.nose/docs/measure/example.md`
- `.nose/maintainability/model.py`
- `.nose/maintainability/languages/__init__.py`
- `.nose/maintainability/languages/python.py`
- `.nose/tests/test_checkability_match.py` (name may vary)
- `.nose/tests/test_fanout_third_party.py`
- `.nose/tests/test_p_bounds.py`
- `.nose/tests/test_volume_defaults.py`
- `.nose/tests/test_cli_max_w.py`

Edit:

- `.nose/docs/goals.md`
- `.nose/docs/metric.md`
- `.nose/docs/principles/README.md` (Python grains → measure doc)
- `.nose/docs/principles/04-intra-site-size.md`
- `.nose/docs/principles/07-comprehension-coupling.md` (same-repo only, already; point at Python resolver)
- `.nose/docs/principles/09-checkability.md`
- `.nose/docs/principles/10-accidental-volume.md`
- `.nose/docs/workflow/phase-4-task.md`
- `.nose/docs/workflow/phase-4-plan.md` (CLI may exit 1)
- `.nose/docs/workflow/phase-5-handover.md`
- `.nose/docs/workflow/artifacts.md` (p validation; exclude `.nose` is now coded)
- `.nose/maintainability/__init__.py`
- `.nose/maintainability/__main__.py`
- `.nose/maintainability/registry.py`
- `.nose/maintainability/atoms.py`
- `.nose/maintainability/sites.py`
- `.nose/maintainability/corpus.py` (delete or leave as thin re-export)
- existing three test modules (collection)

Delete after move:

- `.nose/maintainability/complexity.py`

Unchanged on purpose:

- `AGENTS.md`, root `README.md` unless a one-line CLI note is required
- workflow phases 1–3, `human.md`, `orchestrate.md`
- principles 01, 02, 03, 05, 06, 08 except README table grains
- `yaml_lite.py` unless inf parsing must fail at the registry boundary (prefer fail in `_parse_axis`)
- `product/`

## Checks (re-run after each wave)

```
PYTHONPATH=.nose python3 -m unittest discover -s .nose/tests -v
PYTHONPATH=.nose python3 -m maintainability --root .
# expect exit 2, missing product registry

PYTHONPATH=.nose python3 -m maintainability --root .nose/tests/fixtures/dup
# expect exit 0 and a printed W
```

Wave 2 extra:

```
PYTHONPATH=.nose python3 -m maintainability --root .nose/tests/fixtures/dup --max-w 0
# expect exit 1
```

## Why this shape

Principles stay the domain. \(W\) stays a pure function of atom totals. A language is a parser that fills `Corpus`. Mixing Python AST into `atoms.py` is what made “any language” a lie.

Module-level volume and no JS parser in this stack is laziness. The seam is the option. A full multi-language analyzer is not.

## Open decisions (defaults if nobody answers)

- Authority site stays the module unit.
- `signature_rename` fail-loud stays unimplemented.
- No pytest.
- No PR until waves 0–3 exist as commits on a branch.

Update this file if the plan moves.
