# Principle 8 — Findability

**Status:** locked.

**Property.** Cost to land on the **authority** for a reason (or, for a defect, on the encoding that is wrong), starting from a statement of that reason — not from the registry pointer.

**Direction.** The authority is the unique obvious hit → cheaper and less risky. Buried, misnamed, or out-ranked by clones → more expensive and more risky.

**Principle.** A codebase is cheaper to maintain when a stated reason to change leads to the one intended site.

This is **orient**, before the edit. Not included: hunting extra sites (that is completeness of \(k\)), implicitness of extras (strength), or proving the edit (checkability).

The registry’s `encodes` link is **ground truth for scoring**, not an input to search. Maintainers who already have the map skip this cost; the metric asks whether the *code* is navigable without it.

## Score

\[
\sum_r P(r) \cdot F(r)
\]

Lower is cheaper.

| Symbol | Meaning |
|---|---|
| \(r\), \(P(r)\), authority | Same registry as principle 1; authority is the intended start |
| Search | Deterministic ranker over project symbols (modules, classes, functions, module-level assignments) |
| \(\mathrm{rank}(r)\) | 1-based position of the authority in that ranking |
| \(F(r)\) | \(\min(\mathrm{rank}(r)-1,\, 50)\); if the authority is not in the index, \(F=50\) |

\(F=0\) means the authority is the unique top hit.

## Search procedure (the metric’s definition)

1. **Query tokens.** From \(r\)’s short statement (and id slug): lowercase identifier-style tokens, stopwords dropped. Do **not** include the authority’s path or name unless those words already appear in the statement.
2. **Index.** Every module, class, function, and module-level assignment in the project. Score = how many query tokens occur as substrings of the qualified name, then of the first docstring/comment line.
3. **Order.** Higher score first; ties broken by qualified name (stable).
4. **Hit.** The authority’s defining symbol. Extra clones may out-rank it; that *raises* \(F\). That is intended: a better-named copy is a findability failure even though degree already counts the copy.

## How \(F\) is obtained

Automatic given the registry statement + a symbol index. No hunt.

Headline uses this ranker. A better human search (IDE, memory) is not the metric. Domain synonym packs are optional **query expansion** (setup); if used, they must be declared so \(F\) stays reproducible.

## What does not count

- Rank of extra sites except as competitors that steal rank from the authority.
- Symptom→cause via a failing test traceback — that is a *tactic* that checkability enables, not a second atom. (If there is no \(r\) yet, diagnosis starts from the failing check; once you name the \(r\), this principle applies.)
- Whether extra sites can be proven complete.

## What is *not* a violation

- An authority named in the same words as the statement even if the file is deep (depth is locality *after* you know the sites).
- A registry map used by people; the code can still score well or poorly on \(F\).

## Aliases (not extra principles)

Analysability as “where do I start,” navigability, “screaming architecture” at symbol grain, Ousterhout unknown unknowns *for the first site* (unknown *extras* remain strength + incomplete \(k\)).
