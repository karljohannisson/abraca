# Principle 5 — Intra-site complexity

**Status:** locked.

**Property.** How much control-flow and nesting sit inside the enclosing unit of a representation — how gnarly that one local edit is.

**Direction.** Straighter → cheaper and less risky. More branching, nesting, and state-twisting → more expensive and more risky.

**Principle.** A codebase is cheaper to maintain when each representation sits in a unit whose control flow is easy to hold in mind.

This is **complexity** only. Not included: how many statements (size), mixed reasons, external knowledge, test coverage, or the co-change triple.

Sites, \(r\), and \(P(r)\) are those of [principle 1](01-co-change-degree.md). Same **enclosing unit** as [principle 4](04-intra-site-size.md).

CRAP combines this atom with coverage. Coverage is [principle 9](09-checkability.md), not this.

## Score

\[
\sum_r P(r) \cdot C(r)
\]

Lower is cheaper.

| Symbol | Meaning |
|---|---|
| \(r\), \(P(r)\), sites | Same registry and confirmed representations as principle 1 |
| \(\mathrm{cog}(s)\) | **Sonar cognitive complexity** (Campbell) of the enclosing unit of site \(s\) |
| \(C(r)\) | Mean \(\mathrm{cog}(s)\) over confirmed sites of \(r\) |

Linear straight-line code scores \(0\). No excess threshold: zero *is* the bound.

Cognitive complexity, not McCabe: nested `if` costs more than a flat `elif` chain; boolean operators and recursion increment. That matches load, not path-count for tests.

Mean, not sum: extra sites are principle 1.

## How \(C\) is obtained

1. Take confirmed sites for \(r\).
2. Resolve each enclosing unit.
3. Compute cognitive complexity on that AST.
4. Average.

Fully automatic given confirmed sites. Headline uses confirmed sites. A missed clone in a gnarly function under-counts.

## What does not count

- Statement count — principle 4. A long script of sequential calls can be \(C=0\) and large \(Z\).
- Coverage, tests, types — principle 9. A well-tested state machine still scores here.
- Mixing other \(r\) into the unit — principle 6. A branchy function about *one* reason is still this principle.
- Comprehension of callees — [principle 7](07-comprehension-coupling.md).

## What is *not* a violation

- A tiny state machine that really is the secret of this \(r\) (it still *costs* here; do not move that cost to size or mixing).
- Data-only units (one dict): \(\mathrm{cog}=0\).

## Aliases (not extra principles)

McCabe as a stand-in, SIG unit complexity, “this function is too branchy,” cognitive load *of the unit’s control flow* (not Ousterhout’s whole cognitive load).
