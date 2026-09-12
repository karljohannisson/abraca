# Principle 6 — Concern mixing

**Status:** locked.

**Group.** Load. Map: [README](README.md).

**Property.** How many *other* live change axes have a representation in the same enclosing unit as this site.

**Direction.** One reason per unit → cheaper and less risky. More live reasons in the same unit → more expensive and more risky.

**Principle.** A codebase is cheaper to maintain when a unit is closed over a single reason to change.

This is **mixing** only — the dual of [principle 2](02-co-change-locality.md): same \(r\) should live together; different \(r\) should not. Not included: size, complexity, external fan-out, or packing extra *copies of this* \(r\) (that is degree).

Sites, \(r\), and \(P(r)\) are those of [principle 1](01-co-change-degree.md). Same **enclosing unit** as [principle 4](04-intra-site-size.md). Only **declared live** axes count. Unknown undeclared reasons in the unit under-count; they show up later as size/complexity or as new \(r\).

## Score

\[
\sum_r P(r) \cdot M(r)
\]

Lower is cheaper.

| Symbol | Meaning |
|---|---|
| \(r\), \(P(r)\), sites | Same registry and confirmed representations as principle 1 |
| \(R(u)\) | Set of live axes that have at least one confirmed site in unit \(u\) |
| \(M(r)\) | Mean over sites \(s\) of \(\max(\lvert R(u(s))\rvert - 1,\, 0)\) |

A unit that only encodes \(r\) contributes \(0\) for that site. A unit that also encodes tax and retries contributes \(2\).

Mean, not sum: extra sites are principle 1.

## How \(M\) is obtained

1. Map every confirmed site of every live \(r'\) to its enclosing unit.
2. For each site of \(r\), count other live \(r'\) in that unit.
3. Average.

Automatic given the confirmed site map. No extra hunt. Incomplete hunts under-count mixing (an unlabeled encoding in the unit is invisible).

## What does not count

- Two representations of the *same* \(r\) in one unit — that is \(k\), and locality \(L=0\) if they share innermost scope.
- Helpers in the same unit that are **uses**, not encodings, of another axis.
- Frozen \(r\) (\(P\approx 0\)) in the unit — omitted with principle 1.
- “This function does many steps” with only one declared axis — size/complexity, not mixing.

## What is *not* a violation

- Colocating fields that cannot change independently (one \(r\), one record).
- A façade that only *uses* other authorities.

## Aliases (not extra principles)

SRP as “one reason per unit,” cohesion, Common Closure’s dual (different reasons → different components), “this module knows too many secrets.”
