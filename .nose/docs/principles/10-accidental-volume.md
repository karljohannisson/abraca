# Principle 10 — Accidental volume

**Status:** locked.

**Group.** Mass — standing search tax from code that should not exist. Map: [README](README.md).

**Property.** How much code exists that is not reachable from declared entry points — mass that is not serving any live behavior.

**Direction.** Less unreachable mass → cheaper and less risky. More → more expensive and more risky (search tax, false findability peaks, load of dead paths).

**Principle.** A codebase is cheaper to maintain when it does not retain code that nothing live can reach.

This is **waste mass**. Not included: essential size of the domain, duplicated *knowledge* (that is still reachable — [principle 1](01-co-change-degree.md)), how large a *live* unit is ([principle 4](04-intra-site-size.md)), or undeclared \(r\) that is reachable (that is a missing registry entry, not waste).

This score is a **system** property, not \(\sum_r\). It taxes every future orientation and load.

## Score

\[
u = \frac{\text{unreachable statements}}{\text{total statements}}
\]

Lower is cheaper. \(u\in[0,1]\).

| Symbol | Meaning |
|---|---|
| Statement | Same statement grain as principle 4 |
| Entry points | Declared roots (setup) |
| Reachable | Statically referenced, transitively, from an entry point (and from live authorities, which are roots too) |
| Unreachable | Statements not in that closure |

Live authorities are roots so a library encoding is not “dead” just because app entry has not imported it *yet* if it is in the registry. A public package must declare its exported API as entry points.

## Setup (required)

**Entry points:** modules/functions that start the program or form the public API. If yaml lists no `path`, Python defaults are `**/__main__.py`, `main.py`, `app.py`, and `pyproject.toml` `[project.scripts]`. Packages meant to be imported should list `__all__` or an explicit export set. The CLI still requires `product/axes.yaml`.

Python reachability is **module-import closure**. A live import marks the whole file reached. Nested unused functions in a live file do not add mass. Details: [measure/python.md](../measure/python.md).

## How \(u\) is obtained

1. Index all statements.
2. From entry points + live authorities, follow static same-repo references (imports, names, attributes).
3. \(u =\) statements outside the closure / all statements.

**Automatic floor:** static reachability from the language backend. Dynamics (`importlib`, plugins, string imports) mark live code dead until confirmed. Headline uses **confirmed** unreachable (scanner proposals + confirm), same rule as \(k\). “Vulture found it” is not headline without confirm when the project uses plugins.

Do not count as unreachable: `TYPE_CHECKING` stubs that are referenced, `__all__` exports of a declared API, tests for live authorities (`verifies` and tests that import those modules). Tests for *only* dead code die with it.

## What does not count

- Reachable duplication — principle 1.
- A huge reachable function — principle 4.
- Verbose essential encodings (the 200-country dict, reachable).
- Third-party / stdlib.

## What is *not* a violation

- Problem-sized live code.
- Feature flags that are still referenced (the dead *branch* may still be reachable to the interpreter; unused flags *after* the flag is gone are waste once unreferenced).

## Aliases (not extra principles)

Dead code, YAGNI leftovers, unused functions/modules, SIG volume *as waste fraction* (not raw LOC of the problem).
