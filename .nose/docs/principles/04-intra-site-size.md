# Principle 4 — Intra-site size

**Status:** locked.

**Group.** Load — cost of holding the local edit in mind. Map: [README](README.md).

**Property.** How large the *enclosing unit* of a representation is — how much text you must load to edit that one site.

**Direction.** Smaller → cheaper and less risky. Larger → more expensive and more risky.

**Principle.** A codebase is cheaper to maintain when each representation sits in a small unit.

This is **size** only. Not included: branching/state (complexity), other reasons packed into the same unit (mixing), what you must know *outside* the unit (comprehension coupling), how many sites, where they are, or how implicit they are.

Sites, \(r\), and \(P(r)\) are those of [principle 1](01-co-change-degree.md). Size does not hunt. It measures the enclosing unit of each confirmed site.

**Enclosing unit.** Innermost function or method that contains the encoding; if the encoding is not in a function, the module body.

## Score

\[
\sum_r P(r) \cdot Z(r)
\]

Lower is cheaper.

| Symbol | Meaning |
|---|---|
| \(r\), \(P(r)\), sites | Same registry and confirmed representations as principle 1 |
| \(n(s)\) | Statement count of the enclosing unit of site \(s\) (not physical lines, not comments/blanks) |
| \(T\) | Per-language working-set bound. Python: 15 statements ([measure/python.md](../measure/python.md)) |
| \(Z(r)\) | Mean excess size: \(\frac{1}{k(r)}\sum_s \max(n(s)-T,\,0)\) |

Mean, not sum: extra sites are [principle 1](01-co-change-degree.md). A data table that is one assignment is one statement even if it lists many members — essential bulk of \(r\) is not this principle.

Frozen \(r\) are omitted with principle 1.

## How \(Z\) is obtained

1. Take confirmed sites for \(r\).
2. Resolve each to its enclosing unit.
3. Count statements in that unit (language backend).
4. Average the excess over \(T\).

Fully automatic given confirmed sites.

If you only have the mechanical floor for \(k\), \(Z\) is still well-defined on those sites but may miss a huge unknown clone. Headline uses confirmed sites.

## What does not count

- Cyclomatic / cognitive complexity of the unit — [principle 5](05-intra-site-complexity.md).
- Other live \(r\) in the same unit — [principle 6](06-concern-mixing.md).
- Line distance as a locality measure — [principle 2](02-co-change-locality.md) uses containment, not lines.
- Unreachable units that are not sites — [principle 10](10-accidental-volume.md).
- Essential member count of a single encoding (200 countries in one dict).

## What is *not* a violation

- A large *encoding* that is still one statement (the country table).
- Many tiny units (that may hurt degree if they are extra representations, not size).

## Aliases (not extra principles)

SIG unit size, “short functions,” working-set volume, “this file is too long” when the file is the enclosing unit.
