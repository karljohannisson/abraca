# Principle 2 — Co-change locality

**Status:** locked.

**Group.** Edit. Map: [README](README.md).

**Property.** For a single reason to change, how far apart the edit sites sit in the program’s containment tree (function ⊂ type ⊂ module ⊂ package ⊂ deployable).

**Direction.** Closer → cheaper and less risky. More spread → more expensive and more risky.

**Principle.** A codebase is cheaper to maintain when the sites that must change together live as close together as the language’s nesting allows.

This is **locality** only. Not included: how many sites ([degree](01-co-change-degree.md)), [strength](03-co-change-strength.md), how hard each local edit is ([size](04-intra-site-size.md), [complexity](05-intra-site-complexity.md)), [findability](08-findability.md), [checkability](09-checkability.md), or who owns the files.

When \(k(r)=1\), spread is zero. Locality only has cost once principle 1 has extra sites.

Sites, \(r\), and \(P(r)\) are those of [principle 1](01-co-change-degree.md). This principle does not hunt and does not count. It only asks how large a box those confirmed representations sit in.

## Score

\[
\sum_r P(r) \cdot L(r)
\]

Lower is cheaper. \(L(r)=0\) when \(k(r)\le 1\).

| Symbol | Meaning |
|---|---|
| \(r\), \(P(r)\), sites | Same registry and **confirmed representations** as principle 1 (not uses) |
| \(L(r)\) | Size of the **smallest enclosing box** in the containment tree |

\(L\) is not hop-count, not \(\sum\) pairwise distance, not line distance. Those either mix in \(k\) or punish deep packages.

Frozen decisions (\(P \approx 0\)) are omitted with principle 1. A live \(r\) with \(k=1\) contributes \(0\) here.

## What \(L\) is

Each site gets a path from the AST + filesystem:

`deployable / package… / module / class? / function?`

Innermost scope that **contains the encoding**. A module-level dict → module body, not a fake function.

\(L(r)\) is the coarsest level at which those paths still differ:

| \(L\) | Smallest box that contains every confirmed site |
|---|---|
| 0 | One site, or every site in the **same innermost scope** (same function, or same module body) |
| 1 | Same class, different methods |
| 2 | Same module, not the same class/body |
| 3 | Same package (common package ancestor **below** the deployable root) |
| 4 | Same deployable, different top-level packages |
| 5 | Crosses deployable |

Two extra lists in one function: \(k-1=1\), \(L=0\) — pain is degree only.
Same two lists in two services: \(k-1=1\), \(L=5\).

## Setup (beyond principle 1)

Optional, with defaults:

- **Deployables** — path prefixes. Default: the whole repo is one, so \(L\le 4\).
- **Code roots** — strip `src/`, `lib/`, or a declared unique root so `src/a` vs `src/b` is \(L=4\), not “same package `src`”.

No extra per-site links. No uses.

## How \(L\) is obtained

Fully determined once principle 1’s confirmed set exists.

1. Take confirmed sites for \(r\).
2. Resolve each to a path (file + enclosing class/function).
3. Read \(L\) off the table. Automatic.

If you only have the mechanical **floor** for \(k\), \(L\) is a **lower bound** too: a missed clone in another package can only raise \(L\). Headline score uses confirmed sites. Same rule as principle 1.

## What does not count

- Call sites of the authority (not representations).
- Line distance inside a module ([size](04-intra-site-size.md) of the enclosing unit, not this).
- Import-graph hops (different topology).
- Git co-change (proxy for unknown \(r\), not this).
- Team/ownership.
- A `verifies` test that **iterates** the enum — not a site, so not in the box. A test that **recopies** the set is a site; `tests/` vs `src/` is usually \(L=4\). That is intended. Colocate or stop recopying.

## What is *not* a violation

- One large module that holds a single reason. That may hurt [size](04-intra-site-size.md) / [complexity](05-intra-site-complexity.md) and score well here.
- Independently evolving similar code that you *should not* colocate. Forcing those together raises future co-change degree for *different* \(r\).

## Aliases (not extra principles)

Common Closure, “change together → stay together,” clustered vs shotgun layout, spatial coupling, DSM clustering of a change.
