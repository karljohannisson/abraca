# Principle 1 — Co-change degree

**Status:** locked.

**Property.** For a single reason to change, how many distinct *representations* of that knowledge must be edited.

**Direction.** Fewer representations → cheaper and less risky. More → more expensive and more risky.

**Principle.** A codebase is cheaper to maintain when each reason to change maps to as few edit sites as possible — ideally one.

This is **degree** only. Not included: distance between sites, strength/implicitness of the dependency, how hard each local edit is, findability, or proof of completeness.

## Score

\[
\sum_r P(r) \cdot \max(k(r) - 1,\, 0)
\]

Lower is cheaper.

| Symbol | Meaning |
|---|---|
| \(r\) | A declared, independent, expectable **change axis** (not every requirement, not every value) |
| \(P(r)\) | Likelihood that reason occurs over the life of the system, in \([0, 1]\) |
| \(k(r)\) | Number of **representations** of that knowledge that would have to be edited |
| \(k(r)-1\) | Extra sites after the one unavoidable edit |

Frozen decisions (\(P \approx 0\)) are omitted from the registry even if duplicated. Unexpectable reasons cannot appear in the sum.

## What counts as \(r\)

Independent decisions you are willing to design for, clustered by **what can change without the others**, not by spec phrasing or by record fields.

Example (countries):

- In: “the *set* of countries may grow” (new ISO code issued).
- In, if it can happen alone: “a display name may change.”
- Out: “the token `US` might be reassigned.”

One real-world event is one \(r\) even if several fields are filled. If code list and name list are **separate copies of the same set**, that event has \(k=2\), not two reasons. If names can change **without** a new country, that is a second axis.

## What counts as a site

A place that **encodes** the knowledge, not a place that **reads** a single encoding.

For “new country codes may be added”:

| Code | Site? |
|---|---|
| `COUNTRIES = {"US": "United States", "GB": "United Kingdom"}` | Yes — this *is* the set |
| `for code, name in COUNTRIES.items():` | No — adding a code does not edit this |
| `if code in ("US", "GB", "DE"):` | Yes — a second copy of the set |
| `if code == "US": apply_us_tax()` | No *for this* \(r\) — that is “US is special”, a different axis |

## Registry (required setup)

Not a full requirements-to-code matrix. Only change axes.

For each \(r\):

- id and short statement
- \(P(r)\) (or high / medium / low)
- change shape (set grows, field value changes, formula replaced, …)
- **exactly one authority** (`encodes`): the enum, table, or module allowed to know it
- optional **verifies**: acceptance tests tagged with the req id
- **no `uses` links**

Req→test is coverage. The authority is the intended single site. The metric is how many sites actually exist.

## How \(k\) is obtained

Automatic \(k\) is not a claim. Confirmed \(k\) is.

1. **Seed** — members and shape from the authority (do not hand-maintain the member list).
2. **Mechanical expansion** — other scopes that re-encode those *same tokens* (member literals, parallel lists, switches, tests that recopy the set). High precision, incomplete recall. This is a **floor**.
3. **Hunt + confirm** — agent or human searches for other encodings (synonyms, subsets, SQL, config). Confirmed hits raise \(k\).

Headline score uses **confirmed** \(k\). “Scanner found nothing extra” is **not** proof of \(k=1\) unless a hunt was done. On messy code the automatic floor under-counts; label it as a lower bound.

What the scanner *can* find given an authority: magic strings and second lists that reuse the same tokens. What it cannot reliably find: the same knowledge in a different language (`"USA"` vs `"US"`, `is_domestic()`, numeric codes, implied by a timezone).

## Aliases (not extra principles)

DRY / SPOT as “one representation per reason”, shotgun surgery, copy-paste of the same knowledge, Ousterhout change amplification, ISO 25010 modularity-as-ripple, SIG duplication when it is the same reason in many places.
