# Principle 3 — Co-change strength

**Status:** locked.

**Property.** For a single reason to change, how *implicit* the agreement is among the sites that must move together — Page-Jones’s scale of form, not how many sites or how far apart they are.

**Direction.** Weaker / more explicit → cheaper and less risky. Stronger / more implicit → more expensive and more risky.

**Principle.** A codebase is cheaper to maintain when the sites that share a reason to change agree in a form you can see and rename, not in a form you have to infer.

This is **strength** only. Not included: how many sites, distance between sites, how hard each local edit is, findability, proof of completeness, or fan-in as edge count.

When \(k(r)=1\), there is no inter-site agreement to score. Strength only has cost once principle 1 has extra sites.

Sites, \(r\), \(P(r)\), and the authority are those of [principle 1](01-co-change-degree.md). This principle does not hunt and does not count. It labels **how** each extra site agrees with the authority.

The named connascence kinds are points on this scale, not extra principles.

## Score

\[
\sum_r P(r) \cdot S(r)
\]

Lower is cheaper.

| Symbol | Meaning |
|---|---|
| \(r\), \(P(r)\), authority, sites | Same registry and **confirmed representations** as principle 1 (not uses) |
| Extra site | A confirmed site that is not the authority |
| \(S(r)\) | Rank of the **strongest** extra site, with Name as zero |

Classify each extra site by the **weakest form that fully explains it** (the most explicit agreement you can actually use to maintain it). If it shares the authority’s tokens, it is Name even if the lists are also index-aligned.

| \(S\) | Worst extra site vs authority |
|---|---|
| 0 | \(k\le 1\), or every extra site is **Name** (same tokens / identifiers, including a duplicate `Literal`/`Enum` of those members) |
| 1 | **Meaning** — same knowledge, different language (`"USA"` vs `"US"`, `is_domestic()`, magic `3`, numeric 840) |
| 2 | **Position** — must stay index/arity-aligned, **without** those names (parallel `names[]`, tuple slots, column order) |
| 3 | **Algorithm** — a second procedure/ruleset that must stay equivalent |
| 4 | **Dynamic** — execution order, timing, identity, multi-value constraint |

Name-level extras cost **0 here**. Their cost is principle 1 (and [principle 2](02-co-change-locality.md) if they are far). This score only moves when agreement is worse than grep.

Two `"US"` copies in one function: \(k-1=1\), \(L=0\), \(S=0\).
`"US"` vs `"USA"` vs `is_domestic()`: same \(k\) possible, \(S=1\).
Code enum plus a token-free `names[]` that must insert at the same index: \(S=2\).

Frozen decisions (\(P \approx 0\)) are omitted with principle 1. A live \(r\) with \(k=1\) contributes \(0\) here.

## How \(S\) is obtained

1. Take confirmed extra sites for \(r\).
2. Label each vs the authority using the table (weakest form that explains the site).
3. \(S(r)=\max\) of those labels.

Headline uses **confirmed** sites and **confirmed** labels. A missed meaning-clone raises both \(k\) and \(S\); both headline numbers are lower bounds until the hunt is done.

## What can be automatic

| Label | Automatic? |
|---|---|
| Name | **Yes.** Same mechanical expansion as principle 1 (member literals, parallel lists of those tokens, switches, recopied tests). |
| Position | **Heuristic only.** Same cardinality as the authority, `zip`, tuple-unpack, positional fields, no member tokens. Candidate until confirmed. |
| Meaning | **No.** Hunt + confirm. Optional domain packs (ISO alpha-2/alpha-3/numeric) can propose candidates; they are setup, not a general scanner. |
| Algorithm | **No.** AST clone / similar-control-flow can propose; confirm whether it is the same \(r\). |
| Dynamic | **No.** |

The **automatic floor** is:

- extra sites the token scanner found → Name → contribute \(0\)
- unconfirmed position heuristics → may propose \(S=2\), not headline
- everything else → invisible

“Scanner says \(S=0\)” means “no extra site we *already have* is stronger than Name.” It is not proof that \(S=0\), the same way “scanner found no extra tokens” is not proof that \(k=1\).

On messy code this floor is worse than principle 1’s: the sites that justify this principle are exactly the ones the scanner cannot label.

## Setup (beyond principle 1)

None required. Optional: domain synonym tables to *propose* Meaning candidates. Labels still need confirm to enter the headline.

## What does not count

- Uses of the authority (`for code in COUNTRIES`) — not sites, no label.
- Fan-in / number of extras — principle 1.
- Distance — principle 2.
- How gnarly the local function is.
- Pairwise strength among extras; only extra → authority.
- Unconfirmed heuristic hits.

Call-site positional coupling is this principle **for a different** \(r\): “parameter order of \(f\) may change.” Those call sites *are* representations of order. It is not a free-floating “API tightness” rule.

## What is *not* a violation

- **Uses** of a single authority — name coupling to the authority is the intended weak form.
- One site that internally uses a strong form (a positional tuple inside the country table). That is the encoding’s local shape; a later intra-site principle may care.
- Independently evolving values that only look related. Treating them as connascent *invents* an \(r\) and can raise future degree.

## Aliases (not extra principles)

Connascence-of-X as separate principles, implicit coupling, magic numbers/strings, stringly-typed APIs, temporal coupling, “agreement on meaning vs name.”
