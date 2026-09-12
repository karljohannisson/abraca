# Principle 7 — Comprehension coupling

**Status:** locked.

**Group.** Load. Map: [README](README.md).

**Property.** How much *same-repo* knowledge you must understand **but not edit** in order to change a site.

**Direction.** Thinner, encapsulated collaborators → cheaper and less risky. Broader leaked graph → more expensive and more risky.

**Principle.** A codebase is cheaper to maintain when a local edit does not require reading the internals of the rest of the system.

This is **comprehension of non-sites**. Not included: extra representations you *do* edit (degree), distance of those edits (locality), implicit agreement among them (strength), size/complexity *inside* the unit, or other \(r\) sitting *in* the unit (mixing).

Sites, \(r\), and \(P(r)\) are those of [principle 1](01-co-change-degree.md). Same **enclosing unit** as [principle 4](04-intra-site-size.md).

High fan-in *onto* a stable authority is not this principle (that is reuse of one encoding). This is **efferent** knowledge: what the unit reaches for.

## Score

\[
\sum_r P(r) \cdot H(r)
\]

Lower is cheaper.

| Symbol | Meaning |
|---|---|
| \(r\), \(P(r)\), sites | Same registry and confirmed representations as principle 1 |
| Fan-out \(h(s)\) | Number of distinct **same-repo** definitions the enclosing unit of \(s\) *directly* references, excluding: names defined in that unit itself; other confirmed sites of **this** \(r\); stdlib and third-party |
| \(H(r)\) | Mean \(h(s)\) over confirmed sites of \(r\) |

Direct references only (names, attributes, imports used). Not the transitive import graph — that collapses a whole app into one number.

Cycles are not a separate principle: a cycle-mate you reference is already in \(h(s)\); a cycle-mate you do *not* reference is not required to edit this site.

## How \(H\) is obtained

1. Take confirmed sites for \(r\).
2. Collect Name / Attribute / import uses in the enclosing unit.
3. Resolve to same-repo definitions when static resolution allows.
4. Drop exclusions; count distinct defs; average.

**Automatic floor:** statically resolved project refs. Dynamic `getattr`, import-by-string, plugin entry points under-count until confirmed.

Headline uses confirmed sites and confirmed resolutions. Unresolved project imports still count as the imported module (one def).

## What does not count

- Uses of **this** \(r\)’s authority from *other* units — those units are not enclosing this site. (If this site *is* an extra encoding, the authority is excluded as a site of \(r\).)
- Parameter count as “unit interfacing” except insofar as those parameters’ *types* are same-repo defs the body references.
- Test fan-in / how many tests re-run — [principle 9](09-checkability.md).
- Org ownership of the collaborator.

## What is *not* a violation

- Calling a stable authority whose secret stays hidden (`for code in COUNTRIES`).
- Stdlib / third-party APIs (not properties of *this* codebase).

## Aliases (not extra principles)

Efferent coupling, leaked abstractions, “to change this you must know that,” SIG module coupling as outbound, design-structure *row width* (not clustering — that is locality).
