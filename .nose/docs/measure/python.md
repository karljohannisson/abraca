# Python measurement

How the language-neutral atoms in [principles/](../principles/README.md) and [metric.md](../metric.md) are filled for Python. The backend is `.nose/maintainability/languages/python.py`. Adding another language means a sibling module plus a suffix in `languages/__init__.py`, not a new atom.

## Files

`*.py` under `code_roots`. `product/entry-points.yaml` `exclude` always includes `.nose` when that directory exists at the product root.

## Grains

| Atom | Python grain |
|---|---|
| Size \(T\) | 15 `ast.stmt` in the enclosing unit. Nested `def`/`class` are other units. |
| Complexity | Sonar/Campbell on that unit. A `class` body scores 0. |
| Coupling | Direct same-repo names after resolving imports. Stdlib and third-party do not count. |
| Checkability fail-loud | `shape: new_variant` only. Exhaustive `match` whose subject is the authority. No `_` wildcard. `shape: signature_rename` has no fail-loud: the backend cannot observe type/attribute errors, so a verifies test that reads the authority scores \(V=1\), never \(V=0\) (unlike `set_grows`, where reading alone gives \(V=0\)). |
| Volume | Module-import closure. A live import marks every statement in that file reached. Nested dead functions in a live file do not add mass. |
| Findability | Identifier tokens from `statement` and axis `id` vs qualified names and first docstring lines. |

## Entry-point defaults

If `entry_points` has no `path`, roots include `**/__main__.py`, `main.py`, `app.py`, and `[project.scripts]` targets in `pyproject.toml` when that file exists. Live authorities and `verifies` are always roots. The CLI still requires `product/axes.yaml`.

## Authority site

The authority site is the **module** of `authority.path`, not the enclosing function of `authority.symbol`. Tracked in [bugs/authority-site-is-module.md](../../../bugs/authority-site-is-module.md).

## Not implemented

`shape: signature_rename` fail-loud (type or attribute errors). The scorer reflects this honestly: a verifies test that reads the authority gives \(V=1\), not \(V=0\) — the fail-loud half of the shape is unmeasured. Tracked in [bugs/signature-rename-fail-loud.md](../../../bugs/signature-rename-fail-loud.md).

## CLI

From the product root:

```
PYTHONPATH=.nose python3 -m maintainability
PYTHONPATH=.nose python3 -m maintainability --max-w 1.2
```

Exit 0: score printed. Exit 1: headline \(W\) exceeds `--max-w` or `product/status.yaml` `w_baseline` when that field is a number. Exit 2: missing or invalid registry.
